# Configuration

[Tutorial]: ../en/../tutorial.html
[Config]: #alembic.config.Config
[ScriptDirectory]: ../en/script.html#alembic.script.ScriptDirectory
[EnvironmentContext]: ../en/runtime.html#alembic.runtime.environment.EnvironmentContext
[Commands]: ../en/commands.html#alembic-command-toplevel
[MigrationContext]: ../en/runtime.html#alembic.runtime.migration.MigrationContext
[Operations]: ../en/../ops.html#alembic.operations.Operations
[EnvironmentContext.config]: ../en/runtime.html#alembic.runtime.environment.EnvironmentContext.config
[alembic.command]: ../en/commands.html#module-alembic.command
[Config.attributes]: #alembic.config.Config.attributes
[Config.file_config]: #alembic.config.Config.file_config
[Sharing a Connection with a Series of Migration Commands and Environments]: ../en/../cookbook.html#connection-sharing

> **Note:** this section discusses the **internal API of Alembic** as regards internal configuration constructs. This section is only useful for developers who wish to extend the capabilities of Alembic. For documentation on configuration of an Alembic environment, please see **[Tutorial]**.

The **[Config]** object represents the configuration passed to the Alembic environment. From an API usage perspective, it is needed for the following use cases:

* to create a **[ScriptDirectory]**, which allows you to work with the actual script files in a migration environment
* to create an **[EnvironmentContext]**, which allows you to actually run the `env.py` module within the migration environment
* to programmatically run any of the commands in the **[Commands]** module.

The **[Config]** is not needed for these cases:

* to instantiate a **[MigrationContext]** directly - this object only needs a SQLAlchemy connection or dialect name.
* to instantiate a **[Operations]** object - this object only needs a **[MigrationContext]**.

**Config**(*file_*:  Optional\[str\] = None, *ini_section*:  str = 'alembic', *output_buffer*:  Optional\[TextIO\] = None, *stdout*:  TextIO = <_io.TextIOWrapper name='<stdout>' mode='w' encoding='UTF-8'>, *cmd_opts*:  Optional\[argparse.Namespace\] = None,*config_args*:  sqlalchemy.util._collections._immutabledict_py_fallback.<locals>.immutabledict = {}, *attributes*:  Optional\[dict\] = None)

Represent an Alembic configuration.

Within an `env.py` script, this is available via the **[EnvironmentContext.config]** attribute, which in turn is available at `alembic.context`:

```python
from alembic import context

some_param = context.config.get_main_option("my option")
```

When invoking Alembic programatically, a new **[Config]** can be created by passing the name of an .ini file to the constructor:

```python
from alembic.config import Config
alembic_cfg = Config("/path/to/yourapp/alembic.ini")
```

With a **[Config]** object, you can then run Alembic commands programmatically using the directives in **[alembic.command]**.

The **[Config]** object can also be constructed without a filename. Values can be set programmatically, and new sections will be created as needed:

```python
from alembic.config import Config
alembic_cfg = Config()
alembic_cfg.set_main_option("script_location", "myapp:migrations")
alembic_cfg.set_main_option("sqlalchemy.url", "postgresql://foo/bar")
alembic_cfg.set_section_option("mysection", "foo", "bar")
```

> **Warning:** When using programmatic configuration, make sure the `env.py` file in use is compatible with the target configuration; including that the call to Python `logging.fileConfig()` is omitted if the programmatic configuration doesn’t actually include logging directives.

For passing non-string values to environments, such as connections and engines, use the **[Config.attributes]** dictionary:

```python
with engine.begin() as connection:
    alembic_cfg.attributes['connection'] = connection
    command.upgrade(alembic_cfg, "head")
```

**Parameters:**

* ***file_*** – name of the .ini file to open.
* ***ini_section*** – name of the main Alembic section within the .ini file
* ***output_buffer*** – optional file-like input buffer which will be passed to the **[MigrationContext]** - used to redirect the output of “offline generation” when using Alembic programmatically.
* ***stdout*** – buffer where the “print” output of commands will be sent. Defaults to `sys.stdout`.
* ***config_args*** – A dictionary of keys and values that will be used for substitution in the alembic config file. The dictionary as given is **copied** to a new one, stored locally as the attribute `.config_args`. When the **[Config.file_config]** attribute is first invoked, the replacement variable `here` will be added to this dictionary before the dictionary is passed to `ConfigParser()` to parse the .ini file.
* ***attributes*** – optional dictionary of arbitrary Python keys/values, which will be populated into the **[Config.attributes]** dictionary.

**See also:**

* **[Sharing a Connection with a Series of Migration Commands and Environments]**

Construct a new [Config]
