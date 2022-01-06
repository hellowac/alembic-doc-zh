# get_current_revision

**get_current_revision**() → Optional\[str\]

[MigrationContext.get_current_heads()]: #alembic.runtime.migration.MigrationContext.get_current_heads
[MigrationContext]: #alembic.runtime.migration.MigrationContext

Return the current revision, usually that which is present in the `alembic_version` table in the database.

This method intends to be used only for a migration stream that does not contain unmerged branches in the target database; if there are multiple branches present, an exception is raised. The **[MigrationContext.get_current_heads()]** should be preferred over this method going forward in order to be compatible with branch migration support.

If this **[MigrationContext]** was configured in “offline” mode, that is with `as_sql=True`, the `starting_rev` parameter is returned instead, if any.
