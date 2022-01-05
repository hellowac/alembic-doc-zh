# bulk_insert

**bulk_insert**(*table*:  Union\[Table, TableClause\], *rows*:  List\[[dict]\], *multiinsert*:  [bool] = True) → None

[dict]: https://docs.python.org/3/library/stdtypes.html#dict
[bool]: https://docs.python.org/3/library/functions.html#bool
[Operations.inline_literal()]: ../zh/06_01_23_inline_literal.md
[Operations.bulk_insert()]: ../zh/06_01_04_bulk_insert.md
[multiinsert]: ../zh/06_01_04_bulk_insert.md#params.multiinsert

Issue a “bulk insert” operation using the current migration context.

This provides a means of representing an INSERT of multiple rows which works equally well in the context of executing on a live connection as well as that of generating a SQL script. In the case of a SQL script, the values are rendered inline into the statement.

e.g.:

```python
from alembic import op
from datetime import date
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Date

# Create an ad-hoc table to use for the insert statement.
accounts_table = table('account',
    column('id', Integer),
    column('name', String),
    column('create_date', Date)
)

op.bulk_insert(accounts_table,
    [
        {'id':1, 'name':'John Smith',
                'create_date':date(2010, 10, 5)},
        {'id':2, 'name':'Ed Williams',
                'create_date':date(2007, 5, 27)},
        {'id':3, 'name':'Wendy Jones',
                'create_date':date(2008, 8, 15)},
    ]
)
```

When using –sql mode, some datatypes may not render inline automatically, such as dates and other special types. When this issue is present, **[Operations.inline_literal()]** may be used:

```python
op.bulk_insert(accounts_table,
    [
        {'id':1, 'name':'John Smith',
                'create_date':op.inline_literal("2010-10-05")},
        {'id':2, 'name':'Ed Williams',
                'create_date':op.inline_literal("2007-05-27")},
        {'id':3, 'name':'Wendy Jones',
                'create_date':op.inline_literal("2008-08-15")},
    ],
    multiinsert=False
)
```

When using **[Operations.inline_literal()]** in conjunction with **[Operations.bulk_insert()]**, in order for the statement to work in “online” (e.g. non –sql) mode, the **[multiinsert]** flag should be set to `False`, which will have the effect of individual INSERT statements being emitted to the database, each with a distinct VALUES clause, so that the “inline” values can still be rendered, rather than attempting to pass the values as bound parameters.

**Parameters:**

* ***table*** – a **table** object which represents the target of the INSERT.
* ***rows*** – a list of dictionaries indicating rows.
* ***multiinsert*** – when at its default of True and –sql mode is not enabled, the INSERT statement will be executed using “executemany()” style, where all elements in the list of dictionaries are passed as bound parameters in a single list. Setting this to False results in individual INSERT statements being emitted per parameter set, and is needed in those cases where non-literal values are present in the parameter sets.
