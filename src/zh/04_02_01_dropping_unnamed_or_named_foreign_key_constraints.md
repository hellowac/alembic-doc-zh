# Dropping Unnamed or Named Foreign Key Constraints

**删除未命名或命名的外键约束**

[BatchOperations.drop_constraint()]: ../en/ops.html#alembic.operations.BatchOperations.drop_constraint
[ForeignKey]: https://docs.sqlalchemy.org/en/14/core/constraints.html#sqlalchemy.schema.ForeignKey
[ForeignKeyConstraint]: https://docs.sqlalchemy.org/en/14/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint
[Operations.batch_alter_table()]: ../en/ops.html#alembic.operations.Operations.batch_alter_table
[naming_convention]: ../en/ops.html#alembic.operations.Operations.batch_alter_table.params.naming_convention
[Integration of Naming Conventions into Operations, Autogenerate]: ../en/naming.html#autogen-naming-conventions

SQLite, unlike any other database, allows constraints to exist in the database that have no identifying name. On all other backends, the target database will always generate some kind of name, if one is not given.

The first challenge this represents is that an unnamed constraint can’t by itself be targeted by the **[BatchOperations.drop_constraint()]** method. An unnamed FOREIGN KEY constraint is implicit whenever the **[ForeignKey]** or **[ForeignKeyConstraint]** objects are used without passing them a name. Only on SQLite will these constraints remain entirely unnamed when they are created on the target database; an automatically generated name will be assigned in the case of all other database backends.

A second issue is that SQLAlchemy itself has inconsistent behavior in dealing with SQLite constraints as far as names. Prior to version 1.0, SQLAlchemy omits the name of foreign key constraints when reflecting them against the SQLite backend. So even if the target application has gone through the steps to apply names to the constraints as stated in the database, they still aren’t targetable within the batch reflection process prior to SQLAlchemy 1.0.

Within the scope of batch mode, this presents the issue that the **[BatchOperations.drop_constraint()]** method requires a constraint name in order to target the correct constraint.

In order to overcome this, the **[Operations.batch_alter_table()]** method supports a **[naming_convention]** argument, so that all reflected constraints, including foreign keys that are unnamed, or were named but SQLAlchemy isn’t loading this name, may be given a name, as described in Integration of Naming Conventions into Operations, Autogenerate. Usage is as follows:

```python
naming_convention = {
    "fk":
    "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
with self.op.batch_alter_table(
        "bar", naming_convention=naming_convention) as batch_op:
    batch_op.drop_constraint(
        "fk_bar_foo_id_foo", type_="foreignkey")
```

Note that the naming convention feature requires at least **SQLAlchemy 0.9.4** for support.
