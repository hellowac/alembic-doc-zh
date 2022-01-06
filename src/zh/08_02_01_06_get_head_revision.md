# get_head_revision

**get_head_revision**() → Optional\[Union\[str, Tuple\[str, ...\]\]\]


[EnvironmentContext.get_head_revisions()]: #alembic.runtime.environment.EnvironmentContext.get_head_revisions
[MigrationContext]: #alembic.runtime.migration.MigrationContext


Return the hex identifier of the ‘head’ script revision.

If the script directory has multiple heads, this method raises a CommandError; **[EnvironmentContext.get_head_revisions()]** should be preferred.

This function does not require that the **[MigrationContext]** has been configured.

**See also:**

* **[EnvironmentContext.get_head_revisions()]** 