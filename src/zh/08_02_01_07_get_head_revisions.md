# get_head_revisions

**get_head_revisions**() → Optional\[Union\[str, Tuple\[str, ...\]\]\]


[MigrationContext]: #alembic.runtime.migration.MigrationContext


Return the hex identifier of the ‘heads’ script revision(s).

This returns a tuple containing the version number of all heads in the script directory.

This function does not require that the **[MigrationContext]** has been configured.