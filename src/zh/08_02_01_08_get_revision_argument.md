# get_revision_argument

**get_revision_argument**() → Optional\[Union\[str, Tuple\[str, ...\]\]\]


[MigrationContext]: #alembic.runtime.migration.MigrationContext


Get the ‘destination’ revision argument.

This is typically the argument passed to the `upgrade` or `downgrade` command.

If it was specified as `head`, the actual version number is returned; if specified as `base`, `None` is returned.

This function does not require that the **[MigrationContext]** has been configured.