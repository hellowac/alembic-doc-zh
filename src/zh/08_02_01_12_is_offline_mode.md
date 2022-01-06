# is_offline_mode

**is_offline_mode**() → bool


[MigrationContext]: #alembic.runtime.migration.MigrationContext


Return True if the current migrations environment is running in “offline mode”.

This is `True` or `False` depending on the `--sql` flag passed.

This function does not require that the **[MigrationContext]** has been configured.