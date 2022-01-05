# Changing the Type of Boolean, Enum and other implicit CHECK datatypes

**更改布尔、枚举和其他隐式 CHECK 数据类型的类型**

[Boolean]: https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Boolean
[Enum]: https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Enum
[BatchOperations.drop_column()]: ../en/ops.html#alembic.operations.BatchOperations.drop_column

The SQLAlchemy types **[Boolean]** and **[Enum]** are part of a category of types known as “schema” types; this style of type creates other structures along with the type itself, most commonly (but not always) a CHECK constraint.

Alembic handles dropping and creating the CHECK constraints here automatically, including in the case of batch mode. When changing the type of an existing column, what’s necessary is that the existing type be specified fully:

```python
with self.op.batch_alter_table("some_table") as batch_op:
    batch_op.alter_column(
        'q', type_=Integer,
        existing_type=Boolean(create_constraint=True, constraint_name="ck1"))
```

When dropping a column that includes a named CHECK constraint, as of Alembic 1.7 this named constraint must also be provided using a similar form, as there is no ability for Alembic to otherwise link this reflected CHECK constraint as belonging to a particular column:

```python
with self.op.batch_alter_table("some_table") as batch_op:
    batch_op.drop_column(
        'q',
        existing_type=Boolean(create_constraint=True, constraint_name="ck1"))
    )
```

> *Changed in version 1.7*: The **[BatchOperations.drop_column()]** operation can accept an `existing_type` directive where a “schema type” such as **[Boolean]** and **[Enum]** may be specified such that an associated named constraint can be removed.
