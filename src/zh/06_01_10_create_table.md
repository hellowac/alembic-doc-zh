# create_table

**create_table**(*table_name*:  [str], *columns, **kw) → Optional\[Table\]

[str]: https://docs.python.org/3/library/stdtypes.html#str
[sqlalchemy.schema.Table]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table
[create_table()]: ../zh/06_01_10_create_table.md
[Column]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column
[Table]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table
[Operations.bulk_insert()]: ../zh/06_01_04_bulk_insert.md
[Constraint]: https://docs.sqlalchemy.org/en/14/core/constraints.html#sqlalchemy.schema.Constraint
[Index]: https://docs.sqlalchemy.org/en/14/core/constraints.html#sqlalchemy.schema.Index
[quoted_name]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name

Issue a “create table” instruction using the current migration context.

This directive receives an argument list similar to that of the traditional **[sqlalchemy.schema.Table]** construct, but without the metadata:

```python
from sqlalchemy import INTEGER, VARCHAR, NVARCHAR, Column
from alembic import op

op.create_table(
    'account',
    Column('id', INTEGER, primary_key=True),
    Column('name', VARCHAR(50), nullable=False),
    Column('description', NVARCHAR(200)),
    Column('timestamp', TIMESTAMP, server_default=func.now())
)
```

> **Note:** that **[create_table()]** accepts **[Column]** constructs directly from the SQLAlchemy library. In particular, `default` values to be created on the database side are specified using the `server_default` parameter, and not `default` which only specifies Python-side defaults:

```python
from alembic import op
from sqlalchemy import Column, TIMESTAMP, func

# specify "DEFAULT NOW" along with the "timestamp" column
op.create_table('account',
    Column('id', INTEGER, primary_key=True),
    Column('timestamp', TIMESTAMP, server_default=func.now())
)
```

The function also returns a newly created **[Table]** object, corresponding to the table specification given, which is suitable for immediate SQL operations, in particular **[Operations.bulk_insert()]**:

```python
from sqlalchemy import INTEGER, VARCHAR, NVARCHAR, Column
from alembic import op

account_table = op.create_table(
    'account',
    Column('id', INTEGER, primary_key=True),
    Column('name', VARCHAR(50), nullable=False),
    Column('description', NVARCHAR(200)),
    Column('timestamp', TIMESTAMP, server_default=func.now())
)

op.bulk_insert(
    account_table,
    [
        {"name": "A1", "description": "account 1"},
        {"name": "A2", "description": "account 2"},
    ]
)
```

**Parameters:**

* ***table_name*** – Name of the table
* ****columns*** – collection of **[Column]** objects within the table, as well as optional **[Constraint]** objects and **[Index]** objects.
* ***schema*** – Optional **schema** name to operate within. To control quoting of the **schema** outside of the default behavior, use the SQLAlchemy construct **[quoted_name]**.
* *****kw*** – Other keyword arguments are passed to the underlying **[sqlalchemy.schema.Table]** object created for the command.

**Returns:** the **[Table]** object corresponding to the parameters given.
