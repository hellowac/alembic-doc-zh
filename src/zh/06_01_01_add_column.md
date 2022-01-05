# add_column

**add_column**(*table_name*:  [str], *column*:  Column, *schema*:  Optional\[[str]\] = None) → Optional\[Table\]

[str]: https://docs.python.org/3/library/stdtypes.html#str
[Column]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column
[ForeignKey]: https://docs.sqlalchemy.org/en/14/core/constraints.html#sqlalchemy.schema.ForeignKey
[sqlalchemy.schema.Column]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column
[quoted_name]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name

Issue an “add column” instruction using the current migration context.

e.g.:

```python
from alembic import op
from sqlalchemy import Column, String

op.add_column('organization',
    Column('name', String())
)
```

The provided **[Column]** object can also specify a **[ForeignKey]**, referencing a remote table name. Alembic will automatically generate a stub “referenced” table and emit a second ALTER statement in order to add the constraint separately:

```python
from alembic import op
from sqlalchemy import Column, INTEGER, ForeignKey

op.add_column('organization',
    Column('account_id', INTEGER, ForeignKey('accounts.id'))
)
```

> **Note** that this statement uses the **[Column]** construct as is from the SQLAlchemy library. In particular, `default` values to be created on the database side are specified using the `server_default` parameter, and not `default` which only specifies Python-side defaults:

**Parameters:**

* ***table_name*** – String name of the parent table.
* ***column*** – a **[sqlalchemy.schema.Column]** object representing the new column.
* ***schema*** – Optional **schema** name to operate within. To control quoting of the **schema** outside of the default behavior, use the SQLAlchemy construct **[quoted_name]**.
