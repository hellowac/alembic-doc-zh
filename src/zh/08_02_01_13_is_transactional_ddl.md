# is_transactional_ddl

**is_transactional_ddl**()

[configure()]: #alembic.runtime.environment.EnvironmentContext.configure
[MigrationContext]: #alembic.runtime.migration.MigrationContext

Return True if the context is configured to expect a transactional DDL capable backend.

This defaults to the type of database in use, and can be overridden by the `transactional_ddl` argument to configure()

This function requires that a **[MigrationContext]** has first been made available via **[configure()]**.
