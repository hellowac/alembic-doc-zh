# configure

**configure**(*connection*:  Optional\[Connection\] = None, *url*:  Optional\[[str]\] = None, *dialect_name*:  Optional\[[str]\] = None, *dialect*:  Optional\[Dialect\] = None, *environment_context*:  Optional\[EnvironmentContext\] = None, *dialect_opts*:  Optional\[Dict\[[str], [str]\]\] = None, *opts*:  Optional\[Any\] = None) → MigrationContext

[str]: https://docs.python.org/3/library/stdtypes.html#str
[MigrationContext]: #alembic.runtime.migration.MigrationContext
[EnvironmentContext.configure()]: #alembic.runtime.environment.EnvironmentContext.configure
[Connection]: https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Connection
[sqlalchemy.engine.url.URL]: https://docs.sqlalchemy.org/en/14/core/engines.html#sqlalchemy.engine.URL

Create a new **[MigrationContext]**.

This is a factory method usually called by **[EnvironmentContext.configure()]**.

**Parameters:**

* ***connection*** – a **[Connection]** to use for SQL execution in “online” mode. When present, is also used to determine the type of dialect in use.
* ***url*** – a string database **url**, or a **[sqlalchemy.engine.url.URL]** object. The type of dialect to be used will be derived from this if `connection` is not passed.
* ***dialect_name*** – string name of a dialect, such as “postgresql”, “mssql”, etc. The type of dialect to be used will be derived from this if `connection` and `url` are not passed.
* ***opts*** – dictionary of options. Most other options accepted by **[EnvironmentContext.configure()]** are passed via this dictionary.
