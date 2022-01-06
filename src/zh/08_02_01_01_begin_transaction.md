# begin_transaction

**begin_transaction**() → Union\[_ProxyTransaction, AbstractContextManager\]

[begin_transaction()]: #alembic.runtime.environment.EnvironmentContext.begin_transaction
[is_transactional_ddl()]: #alembic.runtime.environment.EnvironmentContext.is_transactional_ddl
[is_offline_mode()]: #alembic.runtime.environment.EnvironmentContext.is_offline_mode
[DefaultImpl.emit_begin()]: ../en/ddl.html#alembic.ddl.impl.DefaultImpl.emit_begin
[DefaultImpl.emit_commit()]: ../en/ddl.html#alembic.ddl.impl.DefaultImpl.emit_commit
[sqlalchemy.engine.Connection.begin()]: https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Connection.begin
[sqlalchemy.engine.Transaction]: https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Transaction
[Connection]: https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Connection

Return a context manager that will enclose an operation within a “transaction”, as defined by the environment’s offline and transactional DDL settings.

e.g.:

```python
with context.begin_transaction():
    context.run_migrations()
```

begin_transaction() is intended to “do the right thing” regardless of calling context:

* If **[is_transactional_ddl()]** is `False`, returns a “do nothing” context manager which otherwise produces no transactional state or directives.
* If **[is_offline_mode()]** is `True`, returns a context manager that will invoke the **[DefaultImpl.emit_begin()]** and **[DefaultImpl.emit_commit()]** methods, which will produce the string directives `BEGIN` and `COMMIT` on the output stream, as rendered by the target backend (e.g. SQL Server would emit `BEGIN` TRANSACTION).
* Otherwise, calls **[sqlalchemy.engine.Connection.begin()]** on the current online connection, which returns a **[sqlalchemy.engine.Transaction]** object. This object demarcates a real transaction and is itself a context manager, which will roll back if an exception is raised.

> **Note:** that a custom `env.py` script which has more specific transactional needs can of course manipulate the **[Connection]** directly to produce transactional state in “online” mode.
