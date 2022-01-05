# execute

**execute**(*sqltext*:  Union\[[str], TextClause, Update\], *execution_options*:  [None] = [None]) → Optional\[Table\]

[str]: https://docs.python.org/3/library/stdtypes.html#str
[None]: https://docs.python.org/3/library/constants.html#None
[sqlalchemy.sql.expression.table()]: https://docs.sqlalchemy.org/en/14/core/selectable.html#sqlalchemy.sql.expression.table
[sqlalchemy.sql.expression.column()]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.column
[Table]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table
[inline_literal()]: ../zh/06_01_23_inline_literal.md
[sqlalchemy.sql.expression.text()]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.text
[sqlalchemy.sql.expression.insert()]: https://docs.sqlalchemy.org/en/14/core/dml.html#sqlalchemy.sql.expression.insert
[sqlalchemy.sql.expression.update()]: https://docs.sqlalchemy.org/en/14/core/dml.html#sqlalchemy.sql.expression.update
[sqlalchemy.sql.expression.delete()]: https://docs.sqlalchemy.org/en/14/core/dml.html#sqlalchemy.sql.expression.delete
[SQL Expression Language Tutorial (1.x API)]: https://docs.sqlalchemy.org/en/14/core/tutorial.html#sqlexpression-toplevel
[sqlalchemy.engine.Connection.execution_options()]: https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Connection.execution_options

Execute the given SQL using the current migration context.

The given SQL can be a plain string, e.g.:

```python
op.execute("INSERT INTO table (foo) VALUES ('some value')")
```

Or it can be any kind of Core SQL Expression construct, such as below where we use an update construct:

```python
from sqlalchemy.sql import table, column
from sqlalchemy import String
from alembic import op

account = table('account',
    column('name', String)
)
op.execute(
    account.update().\\
        where(account.c.name==op.inline_literal('account 1')).\\
        values({'name':op.inline_literal('account 2')})
        )
```

Above, we made use of the SQLAlchemy **[sqlalchemy.sql.expression.table()]** and **[sqlalchemy.sql.expression.column()]** constructs to make a brief, ad-hoc table construct just for our UPDATE statement. A full **[Table]** construct of course works perfectly fine as well, though note it’s a recommended practice to at least ensure the definition of a table is self-contained within the migration script, rather than imported from a module that may break compatibility with older migrations.

In a SQL script context, the statement is emitted directly to the output stream. There is no return result, however, as this function is oriented towards generating a change script that can run in “offline” mode. Additionally, parameterized statements are discouraged here, as they will not work in offline mode. Above, we use **[inline_literal()]** where parameters are to be used.

For full interaction with a connected database where parameters can also be used normally, use the “bind” available from the context:

```python
from alembic import op
connection = op.get_bind()

connection.execute(
    account.update().where(account.c.name=='account 1').
    values({"name": "account 2"})
)
```

Additionally, when passing the statement as a plain string, it is first coerceed into a **[sqlalchemy.sql.expression.text()]** construct before being passed along. In the less likely case that the literal SQL string contains a colon, it must be escaped with a backslash, as:

```python
op.execute("INSERT INTO table (foo) VALUES ('\:colon_value')")
```

**Parameters:**

* ***sqltext*** – Any legal SQLAlchemy expression, including:
  * a string
  * a **[sqlalchemy.sql.expression.text()]** construct.
  * a **[sqlalchemy.sql.expression.insert()]** construct.
  * a **[sqlalchemy.sql.expression.update()]**, **[sqlalchemy.sql.expression.insert()]**, or **[sqlalchemy.sql.expression.delete()]** construct.
  * Pretty much anything that’s “executable” as described in **[SQL Expression Language Tutorial (1.x API)]**.
  > **Note:** when passing a plain string, the statement is coerced into a **[sqlalchemy.sql.expression.text()]** construct. This construct considers symbols with colons, e.g. `:foo` to be bound parameters. To avoid this, ensure that colon symbols are escaped, e.g. `\:foo`.
* ***execution_options*** – Optional dictionary of execution options, will be passed to **[sqlalchemy.engine.Connection.execution_options()]**.
