# create_index

**create_index**(*index_name*:  [str], *table_name*:  [str], *columns*:  Sequence\[Union\[[str], TextClause, Function\]\], *schema*:  Optional\[[str]\] = None, *unique*:  [bool] = False, **kw) → Optional\[Table\]

[str]: https://docs.python.org/3/library/stdtypes.html#str
[bool]: https://docs.python.org/3/library/functions.html#bool
[sqlalchemy.sql.expression.text()]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.text
[text()]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.text
[quoted_name]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name
[Dialects]: https://docs.sqlalchemy.org/en/14/dialects/index.html#dialect-toplevel

Issue a “create index” instruction using the current migration context.

e.g.:

```python
from alembic import op

op.create_index('ik_test', 't1', ['foo', 'bar'])
```

Functional indexes can be produced by using the **[sqlalchemy.sql.expression.text()]** construct:

```python
from alembic import op
from sqlalchemy import text

op.create_index('ik_test', 't1', [text('lower(foo)')])
```

**Parameters:**

* ***index_name*** – name of the index.
* ***table_name*** – name of the owning table.
* ***columns*** – a list consisting of string column names and/or **[text()]** constructs.
* ***schema*** – Optional **schema** name to operate within. To control quoting of the **schema** outside of the default behavior, use the SQLAlchemy construct **[quoted_name]**.
* ***unique*** – If True, create a **unique** index.
* ***quote*** – Force quoting of this column’s name on or off, corresponding to `True` or `False`. When left at its default of `None`, the column identifier will be quoted according to whether the name is case sensitive (identifiers with at least one upper case character are treated as case sensitive), or if it’s a reserved word. This flag is only needed to force quoting of a reserved word which is not known by the SQLAlchemy dialect.
* ***\*\*kw*** – Additional keyword arguments not mentioned above are dialect specific, and passed in the form `<dialectname>_<argname>`. See the documentation regarding an individual dialect at **[Dialects]** for detail on documented arguments.
