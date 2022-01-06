# get_x_argument

**get_x_argument**(*as_dictionary*:  Literal\[False\] = False) → List\[str\]

**get_x_argument**(*as_dictionary*:  Literal\[True\] = False) → Dict\[str, str\]

[MigrationContext]: #alembic.runtime.migration.MigrationContext
[EnvironmentContext.get_tag_argument()]: #alembic.runtime.environment.EnvironmentContext.get_tag_argument
[Config.cmd_opts]: ../en/config.html#alembic.config.Config.cmd_opts

Return the value(s) passed for the `-x` argument, if any.

The `-x` argument is an open ended flag that allows any user-defined value or values to be passed on the command line, then available here for consumption by a custom `env.py` script.

The return value is a list, returned directly from the `argparse` structure. If `as_dictionary=True` is passed, the `x` arguments are parsed using `key=value` format into a dictionary that is then returned.

For example, to support passing a database URL on the command line, the standard `env.py` script can be modified like this:

```python
cmd_line_url = context.get_x_argument(
    as_dictionary=True).get('dbname')
if cmd_line_url:
    engine = create_engine(cmd_line_url)
else:
    engine = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix='sqlalchemy.',
            poolclass=pool.NullPool)
```

This then takes effect by running the `alembic` script as:

```bash
alembic -x dbname=postgresql://user:pass@host/dbname upgrade head
```

This function does not require that the **[MigrationContext]** has been configured.

**See also:**

* **[EnvironmentContext.get_tag_argument()]**
* **[Config.cmd_opts]**
