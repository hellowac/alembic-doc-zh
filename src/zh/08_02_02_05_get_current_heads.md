# get_current_heads

**get_current_heads**() → Tuple\[str, ...\]

[MigrationContext.get_current_revision()]: #alembic.runtime.migration.MigrationContext.get_current_revision
[MigrationContext]: #alembic.runtime.migration.MigrationContext

Return a tuple of the current ‘head versions’ that are represented in the target database.

For a migration stream without branches, this will be a single value, synonymous with that of **[MigrationContext.get_current_revision()]**. However when multiple unmerged branches exist within the target database, the returned tuple will contain a value for each head.

If this **[MigrationContext]** was configured in “offline” mode, that is with `as_sql=True`, the `starting_rev` parameter is returned in a one-length tuple.

If no version table is present, or if there are no revisions present, an empty tuple is returned.
