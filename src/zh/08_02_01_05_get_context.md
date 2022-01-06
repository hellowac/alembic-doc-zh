# get_context

**get_context**() → alembic.runtime.migration.MigrationContext

[MigrationContext]: #alembic.runtime.migration.MigrationContext
[EnvironmentContext.configure()]: #alembic.runtime.environment.EnvironmentContext.configure

Return the current **[MigrationContext]** object.

If **[EnvironmentContext.configure()]** has not been called yet, raises an exception.
