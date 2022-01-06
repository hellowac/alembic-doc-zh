# Commands

[Tutorial]: ../en/tutorial.html
[Commands]: #alembic-command-toplevel
[Config]: ../en/config.html#alembic.config.Config
[Config.attributes]: ../en/config.html#alembic.config.Config.attributes
[Sharing a Connection with a Series of Migration Commands and Environments]: ../en/../cookbook.html#connection-sharing
[ScriptDirectory]: ../en/script.html#alembic.script.ScriptDirectory
[MigrationContext]: ../en/runtime.html#alembic.runtime.migration.MigrationContext

> **Note:** this section discusses the **internal API of Alembic** as regards its command invocation system. This section is only useful for developers who wish to extend the capabilities of Alembic. For documentation on using Alembic commands, please see **[Tutorial]**.

Alembic commands are all represented by functions in the **[Commands]** package. They all accept the same style of usage, being sent the **[Config]** object as the first argument.

Commands can be run programmatically, by first constructing a **[Config]** object, as in:

```python
from alembic.config import Config
from alembic import command
alembic_cfg = Config("/path/to/yourapp/alembic.ini")
command.upgrade(alembic_cfg, "head")
```

In many cases, and perhaps more often than not, an application will wish to call upon a series of Alembic commands and/or other features. It is usually a good idea to link multiple commands along a single connection and transaction, if feasible. This can be achieved using the **[Config.attributes]** dictionary in order to share a connection:

```python
with engine.begin() as connection:
    alembic_cfg.attributes['connection'] = connection
    command.upgrade(alembic_cfg, "head")
```

This recipe requires that `env.py` consumes this connection argument; see the example in **[Sharing a Connection with a Series of Migration Commands and Environments]** for details.

To write small API functions that make direct use of database and script directory information, rather than just running one of the built-in commands, use the **[ScriptDirectory]** and **[MigrationContext]** classes directly.
