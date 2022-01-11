# Commands

[Tutorial]: ../zh/00_tutorial.md
[教程]: ../zh/00_tutorial.md
[Commands]: ../zh/08_04_commands.md
[Config]: ../zh/08_03_configuration.md
[Config.attributes]: ../en/config.html#alembic.config.Config.attributes
[Sharing a Connection with a Series of Migration Commands and Environments]: ../zh/07_03_sharing_a_connection_with_a_series_of_migration_commands_and_environments.md
[与一系列迁移命令和环境共享连接]: ../zh/07_03_sharing_a_connection_with_a_series_of_migration_commands_and_environments.md
[ScriptDirectory]: ../zh/08_07_script_directory.md
[MigrationContext]: ../zh/08_02_02_the_migration_context.md

> **Note:** this section discusses the **internal API of Alembic** as regards its command invocation system. This section is only useful for developers who wish to extend the capabilities of Alembic. For documentation on using Alembic commands, please see **[Tutorial]**.

> **注意**：本节讨论 **Alembic的内部API** 关于其命令调用系统。 本节仅对希望扩展 Alembic 功能的开发人员有用。 有关使用 Alembic 命令的文档，请参阅 **[教程]**.

Alembic commands are all represented by functions in the **[Commands]** package. They all accept the same style of usage, being sent the **[Config]** object as the first argument.

> Alembic 命令全部由 **[Commands]** 包中的函数表示。 它们都接受相同的使用方式，将 **[Config]** 对象作为第一个参数发送。

Commands can be run programmatically, by first constructing a **[Config]** object, as in:

> 命令可以通过首先构造一个 **[Config]** 对象以编程方式运行，如下所示：

```python
from alembic.config import Config
from alembic import command
alembic_cfg = Config("/path/to/yourapp/alembic.ini")
command.upgrade(alembic_cfg, "head")
```

In many cases, and perhaps more often than not, an application will wish to call upon a series of Alembic commands and/or other features. It is usually a good idea to link multiple commands along a single connection and transaction, if feasible. This can be achieved using the **[Config.attributes]** dictionary in order to share a connection:

> 在许多情况下，也许更多时候，应用程序会希望调用一系列 Alembic 的命令以及其他功能。 如果可行，沿单个连接和事务并链接多个命令通常是一个好主意。 这可以使用 **[Config.attributes]** 字典来实现，以便共享连接：

```python
with engine.begin() as connection:
    alembic_cfg.attributes['connection'] = connection
    command.upgrade(alembic_cfg, "head")
```

This recipe requires that `env.py` consumes this connection argument; see the example in **[Sharing a Connection with a Series of Migration Commands and Environments]** for details.

> 这个示例片段要求 `env.py` 使用这个 `connection` 参数； 有关详细信息，请参阅[与一系列迁移命令和环境共享连接]中的示例。

To write small API functions that make direct use of database and script directory information, rather than just running one of the built-in commands, use the **[ScriptDirectory]** and **[MigrationContext]** classes directly.

> 要编写直接使用数据库和脚本目录信息的小型 API 函数，而不仅仅是运行内置命令之一，请直接使用 **[ScriptDirectory]** 和 **[MigrationContext]** 类。
