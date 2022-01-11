# Dropping Unnamed or Named Foreign Key Constraints

**删除未命名或命名的外键约束**

[BatchOperations.drop_constraint()]: ../en/ops.html#alembic.operations.BatchOperations.drop_constraint
[ForeignKey]: https://docs.sqlalchemy.org/en/14/core/constraints.html#sqlalchemy.schema.ForeignKey
[ForeignKeyConstraint]: https://docs.sqlalchemy.org/en/14/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint
[Operations.batch_alter_table()]: ../en/ops.html#alembic.operations.Operations.batch_alter_table
[naming_convention]: ../en/ops.html#alembic.operations.Operations.batch_alter_table.params.naming_convention
[Integration of Naming Conventions into Operations, Autogenerate]: ../en/naming.html#autogen-naming-conventions

SQLite, unlike any other database, allows constraints to exist in the database that have no identifying name. On all other backends, the target database will always generate some kind of name, if one is not given.

> 与任何其他数据库不同，SQLite 允许数据库中存在没有标识名称的约束。 在所有其他后端，如果没有给出，目标数据库将始终生成某种名称。

The first challenge this represents is that an unnamed constraint can’t by itself be targeted by the **[BatchOperations.drop_constraint()]** method. An unnamed FOREIGN KEY constraint is implicit whenever the **[ForeignKey]** or **[ForeignKeyConstraint]** objects are used without passing them a name. Only on SQLite will these constraints remain entirely unnamed when they are created on the target database; an automatically generated name will be assigned in the case of all other database backends.

> 这代表的第一个挑战是未命名的约束本身不能被 **[BatchOperations.drop_constraint()]** 方法定位。 每当使用 **[ForeignKey]** 或 **[ForeignKeyConstraint]** 对象而不传递名称时，未命名的 FOREIGN KEY 约束是隐式的。 只有在 SQLite 上，这些约束在目标数据库上创建时才会完全保持未命名； 对于所有其他数据库后端，将分配一个自动生成的名称。

A second issue is that SQLAlchemy itself has inconsistent behavior in dealing with SQLite constraints as far as names. Prior to version 1.0, SQLAlchemy omits the name of foreign key constraints when reflecting them against the SQLite backend. So even if the target application has gone through the steps to apply names to the constraints as stated in the database, they still aren’t targetable within the batch reflection process prior to SQLAlchemy 1.0.

> 第二个问题是 SQLAlchemy 本身在处理 SQLite 约束时的行为不一致，就名称而言。 在 1.0 版之前，SQLAlchemy 在将外键约束反映到 SQLite 后端时省略了它们的名称。 因此，即使目标应用程序已经完成了将名称应用于数据库中所述的约束的步骤，它们仍然不能在 SQLAlchemy 1.0 之前的批处理反射过程中成为目标。

Within the scope of batch mode, this presents the issue that the **[BatchOperations.drop_constraint()]** method requires a constraint name in order to target the correct constraint.

> 在批处理模式的范围内，这提出了 **[BatchOperations.drop_constraint()]** 方法需要一个约束名称才能定位正确的约束的问题。

In order to overcome this, the **[Operations.batch_alter_table()]** method supports a **[naming_convention]** argument, so that all reflected constraints, including foreign keys that are unnamed, or were named but SQLAlchemy isn’t loading this name, may be given a name, as described in Integration of Naming Conventions into Operations, Autogenerate. Usage is as follows:

> 为了克服这个问题，**[Operations.batch_alter_table()]** 方法支持一个命名约定参数，以便所有反映的约束，包括未命名的外键，或已命名但 SQLAlchemy 未加载此名称的外键，都可以指定一个名称，如 将命名约定集成到操作中，自动生成中进行了描述。 用法如下：

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

> 请注意，命名约定功能至少需要 **SQLAlchemy 0.9.4** 的支持。
