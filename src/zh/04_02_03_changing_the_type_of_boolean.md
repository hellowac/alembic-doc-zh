# Changing the Type of Boolean, Enum and other implicit CHECK datatypes

**更改布尔、枚举和其他隐式 CHECK 数据类型的类型**

[Boolean]: https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Boolean
[Enum]: https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Enum
[BatchOperations.drop_column()]: ../zh/06_02_10_drop_column.md

The SQLAlchemy types **[Boolean]** and **[Enum]** are part of a category of types known as “schema” types; this style of type creates other structures along with the type itself, most commonly (but not always) a CHECK constraint.

> SQLAlchemy 类型 **[Boolean]** 和 **[Enum]** 是称为 “schema” 类型的类型类别的一部分； 这种类型的类型会与类型本身一起创建其他结构，最常见的（但不总是）是 CHECK 约束。

Alembic handles dropping and creating the CHECK constraints here automatically, including in the case of batch mode. When changing the type of an existing column, what’s necessary is that the existing type be specified fully:

> Alembic 在此处自动处理删除和创建 CHECK 约束，包括在批处理模式的情况下。 更改现有列的类型时，需要完全指定现有类型：

```python
with self.op.batch_alter_table("some_table") as batch_op:
    batch_op.alter_column(
        'q', type_=Integer,
        existing_type=Boolean(create_constraint=True, constraint_name="ck1"))
```

When dropping a column that includes a named CHECK constraint, as of Alembic 1.7 this named constraint must also be provided using a similar form, as there is no ability for Alembic to otherwise link this reflected CHECK constraint as belonging to a particular column:

> 当删除包含命名 CHECK 约束的列时，从 Alembic 1.7 开始，此命名约束也必须使用类似的形式提供，因为 Alembic 无法以其他方式将此反映的 CHECK 约束链接为属于特定列：

```python
with self.op.batch_alter_table("some_table") as batch_op:
    batch_op.drop_column(
        'q',
        existing_type=Boolean(create_constraint=True, constraint_name="ck1"))
    )
```

> *Changed in version 1.7*: The **[BatchOperations.drop_column()]** operation can accept an `existing_type` directive where a “schema type” such as **[Boolean]** and **[Enum]** may be specified such that an associated named constraint can be removed.

> 版本1.7更新：**[BatchOperations.drop_column()]** 操作可以接受 `existing_type` 指令，其中可以指定诸如布尔和枚举之类的“模式类型”，以便可以删除关联的命名约束。
