## The Environment Context

[EnvironmentContext]: #alembic.runtime.environment.EnvironmentContext
[EnvironmentContext.configure()]: #alembic.runtime.environment.EnvironmentContext.configure
[MigrationContext]: #alembic.runtime.migration.MigrationContext
[Config]: ../en/config.html#alembic.config.Config
[alembic.command]: ../en/commands.html#module-alembic.command
[MigrationContext.run_migrations()]: #alembic.runtime.migration.MigrationContext.run_migrations
[ScriptDirectory]: ../en/script.html#alembic.script.ScriptDirectory

The **[EnvironmentContext]** class provides most of the API used within an `env.py` script. Within `env.py`, the instantated **[EnvironmentContext]** is made available via a special proxy module called `alembic.context`. That is, you can import `alembic.context` like a regular Python module, and each name you call upon it is ultimately routed towards the current **[EnvironmentContext]** in use.

In particular, the key method used within `env.py` is **[EnvironmentContext.configure()]**, which establishes all the details about how the database will be accessed.

### *class* alembic.runtime.environment.**EnvironmentContext**(*config*: Config, *script*: ScriptDirectory, *\*\*kw*)

A configurational facade made available in an `env.py` script.

The **[EnvironmentContext]** acts as a facade to the more nuts-and-bolts objects of **[MigrationContext]** as well as certain aspects of **[Config]**, within the context of the `env.py` script that is invoked by most Alembic commands.

EnvironmentContext is normally instantiated when a command in **[alembic.command]** is run. It then makes itself available in the `alembic.context` module for the scope of the command. From within an `env.py` script, the current **[EnvironmentContext]** is available by importing this module.

EnvironmentContext also supports programmatic usage. At this level, it acts as a Python context manager, that is, is intended to be used using the `with:` statement. A typical use of **[EnvironmentContext]**:

```python
from alembic.config import Config
from alembic.script import ScriptDirectory

config = Config()
config.set_main_option("script_location", "myapp:migrations")
script = ScriptDirectory.from_config(config)

def my_function(rev, context):
    '''do something with revision "rev", which
    will be the current database revision,
    and "context", which is the MigrationContext
    that the env.py will create'''

with EnvironmentContext(
    config,
    script,
    fn = my_function,
    as_sql = False,
    starting_rev = 'base',
    destination_rev = 'head',
    tag = "sometag"
):
    script.run_env()
```

The above script will invoke the `env.py` script within the migration environment. If and when `env.py` calls **[MigrationContext.run_migrations()]**, the `my_function()` function above will be called by the **[MigrationContext]**, given the context itself as well as the current revision in the database.

> **Note:** For most API usages other than full blown invocation of migration scripts, the **[MigrationContext]** and **[ScriptDirectory]** objects can be created and used directly. The **[EnvironmentContext]** object is only needed when you need to actually invoke the `env.py` module present in the migration environment.

Construct a new **[EnvironmentContext]**.

**Parameters:**

* ***config*** – a **[Config]** instance.
* ***script*** – a **[ScriptDirectory]** instance.
* ***\*\*kw*** – keyword options that will be ultimately passed along to the **[MigrationContext]** when **[EnvironmentContext.configure()]** is called.
