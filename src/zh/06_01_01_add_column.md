# add_column

**add_column**(*table_name*:  [str], *column*:  Column, *schema*:  Optional\[[str]\] = None) → Optional\[Table\]

[str]: https://docs.python.org/3/library/stdtypes.html#str
[Column]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column
[ForeignKey]: https://docs.sqlalchemy.org/en/14/core/constraints.html#sqlalchemy.schema.ForeignKey
[sqlalchemy.schema.Column]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column
[quoted_name]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name

Issue an “add column” instruction using the current migration context.

> 使用当前迁移上下文发出“添加列”指令。

e.g.:

```python
from alembic import op
from sqlalchemy import Column, String

op.add_column('organization',
    Column('name', String())
)
```

The provided **[Column]** object can also specify a **[ForeignKey]**, referencing a remote table name. Alembic will automatically generate a stub “referenced” table and emit a second ALTER statement in order to add the constraint separately:

> 提供的 **[Column]**  对象还可以指定一个 **[ForeignKey]**，引用一个远程表名。 Alembic 将自动生成一个存根“引用”表并发出第二个 ALTER 语句，以便单独添加约束：

```python
from alembic import op
from sqlalchemy import Column, INTEGER, ForeignKey

op.add_column('organization',
    Column('account_id', INTEGER, ForeignKey('accounts.id'))
)
```

> **Note** that this statement uses the **[Column]** construct as is from the SQLAlchemy library. In particular, `default` values to be created on the database side are specified using the `server_default` parameter, and not `default` which only specifies Python-side defaults:

> **注意：** 该语句使用 SQLAlchemy 库中的 **[Column]** 构造。 特别是，要在数据库端创建的默认值是使用 `server_default` 参数指定的，而不是 `default` ，它只指定 Python 端的默认值：

**Parameters:**

**参数:**

* ***table_name*** – String name of the parent table.
* ***column*** – a **[sqlalchemy.schema.Column]** object representing the new column.
* ***schema*** – Optional **schema** name to operate within. To control quoting of the **schema** outside of the default behavior, use the SQLAlchemy construct **[quoted_name]**.

> * ***table_name*** – 父表的字符串名称。
> * ***column*** – 表示新列的 **[sqlalchemy.schema.Column]** 对象。
> * ***schema*** – 要在其中操作的可选 **schema** 名称。 要控制默认行为之外的 **schema** 引用，请使用 SQLAlchemy 构造 **[quoted_name]**。
