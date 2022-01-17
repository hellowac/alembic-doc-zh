# Sharing a Connection with a Series of Migration Commands and Environments

**与一系列迁移命令和环境共享连接**

[Commands]: ../zh/08_04_commands.md
[Connection]: https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Connection
[Config.attributes]: ../zh/08_03_01_attributes.md
[Config]: ../en/api/config.html#alembic.config.Config
[Engine]: https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Engine
[connect()]: https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Connection.connect

It is often the case that an application will need to call upon a series of commands within **[Commands]**, where it would be advantageous for all operations to proceed along a single transaction. The connectivity for a migration is typically solely determined within the `env.py` script of a migration environment, which is called within the scope of a command.

> 通常情况下，应用程序需要调用 **[Commands]** 中的一系列命令，在这种情况下，所有操作都沿单个事务进行是有利的。 迁移的连接性通常仅在迁移环境的 `env.py` 脚本中确定，该脚本在命令范围内调用。

The steps to take here are:

> 这里要采取的步骤是：

1. Produce the **[Connection]** object to use.
2. Place it somewhere that `env.py` will be able to access it. This can be either a. a module-level global somewhere, or b. an attribute which we place into the **[Config.attributes]** dictionary (if we are on an older Alembic version, we may also attach an attribute directly to the **[Config]** object).
3. The `env.py` script is modified such that it looks for this **[Connection]** and makes use of it, in lieu of building up its own **[Engine]** instance.

> 1. 生成要使用的 **[Connection]** 对象。
> 2. 将它放在 `env.py` 能够访问它的地方。 这可以是全局的模块级的 `a.a` 或 `b.`，然后我们将其作为属性放入 **[Config.attributes]** 字典。（如果我们使用的是较旧的 Alembic 版本，我们也可以将属性直接附加到 **[Config]** 对象）。
> 3. 修改了 `env.py` 脚本，使其查找此 **[Connection]** 并使用它，而不是构建自己的 **[Engine]** 实例。

We illustrate using **[Config.attributes]**:

> 我们使用 **[Config.attributes]** 进行说明：

```python
from alembic import command, config

cfg = config.Config("/path/to/yourapp/alembic.ini")
with engine.begin() as connection:
    cfg.attributes['connection'] = connection
    command.upgrade(cfg, "head")
```

Then in `env.py`:

> 然后在 `env.py` 中：

```python
def run_migrations_online():
    connectable = config.attributes.get('connection', None)

    if connectable is None:
        # only create Engine if we don't have a Connection
        # from the outside
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix='sqlalchemy.',
            poolclass=pool.NullPool)

    context.configure(
        connection=connectable,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()
```

> *Changed in version 1.4*: Prior to this version, we used a “branched connection”, by calling **[connect()]**. This is now deprecated and unnecessary, since we no longer have to guess if the given “connection” is an `Engine` or `Connection`, it is always a `Connection`.

> *版本1.4更新*: 在此版本之前，我们通过调用 **[connect()]** 使用 *“分支连接”* 。 现在已弃用且不必要，因为我们不再需要猜测给定的 `connection` 是 `Engine`的实例还是`Connection`的实例，它始终是`Connection`的实例。
