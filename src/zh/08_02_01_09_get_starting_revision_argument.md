# get_starting_revision_argument

**get_starting_revision_argument**() → Optional\[Union\[str, Tuple\[str, ...\]\]\]


[MigrationContext]: #alembic.runtime.migration.MigrationContext


Return the ‘starting revision’ argument, if the revision was passed using `start:end`.

This is only meaningful in “offline” mode. Returns `None` if no value is available or was configured.

This function does not require that the **[MigrationContext]** has been configured.