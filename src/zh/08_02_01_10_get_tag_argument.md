# get_tag_argument

**get_tag_argument**() → Optional\[str\]

[MigrationContext]: #alembic.runtime.migration.MigrationContext
[EnvironmentContext.get_x_argument()]: #alembic.runtime.environment.EnvironmentContext.get_x_argument

Return the value passed for the `--tag` argument, if any.

The `--tag` argument is not used directly by Alembic, but is available for custom `env.py` configurations that wish to use it; particularly for offline generation scripts that wish to generate tagged filenames.

This function does not require that the **[MigrationContext]** has been configured.

**See also:**

[EnvironmentContext.get_x_argument()] - a newer and more open ended system of extending `env.py` scripts via the command line.
