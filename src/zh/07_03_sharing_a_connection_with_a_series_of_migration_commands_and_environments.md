# Sharing a Connection with a Series of Migration Commands and Environments

**与一系列迁移命令和环境共享连接**

[Commands]: ../en/api/commands.html#alembic-command-toplevel
[Connection]: https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Connection
[Config.attributes]: ../en/api/config.html#alembic.config.Config.attributes
[Config]: ../en/api/config.html#alembic.config.Config
[Engine]: https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Engine
[connect()]: https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Connection.connect

It is often the case that an application will need to call upon a series of commands within **[Commands]**, where it would be advantageous for all operations to proceed along a single transaction. The connectivity for a migration is typically solely determined within the `env.py` script of a migration environment, which is called within the scope of a command.

The steps to take here are:

1. Produce the **[Connection]** object to use.
2. Place it somewhere that `env.py` will be able to access it. This can be either a. a module-level global somewhere, or b. an attribute which we place into the **[Config.attributes]** dictionary (if we are on an older Alembic version, we may also attach an attribute directly to the **[Config]** object).
3. The `env.py` script is modified such that it looks for this **[Connection]** and makes use of it, in lieu of building up its own **[Engine]** instance.

We illustrate using **[Config.attributes]**:

```python
from alembic import command, config

cfg = config.Config("/path/to/yourapp/alembic.ini")
with engine.begin() as connection:
    cfg.attributes['connection'] = connection
    command.upgrade(cfg, "head")
```

Then in `env.py`:

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
