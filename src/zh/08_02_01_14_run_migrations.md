# run_migrations

**run_migrations**(**kw) → None

[MigrationContext]: #alembic.runtime.migration.MigrationContext
[configure()]: #alembic.runtime.environment.EnvironmentContext.configure

Run migrations as determined by the current command line configuration as well as versioning information present (or not) in the current database connection (if one is present).

The function accepts optional `**kw` arguments. If these are passed, they are sent directly to the `upgrade()` and `downgrade()` functions within each target revision file. By modifying the `script.py.mako` file so that the `upgrade()` and `downgrade()` functions accept arguments, parameters can be passed here so that contextual information, usually information to identify a particular database in use, can be passed from a custom `env.py` script to the migration functions.

This function requires that a **[MigrationContext]** has first been made available via **[configure()]**.
