# Using Asyncio with Alembic

**将 Asyncio 与 Alembic 结合使用**

SQLAlchemy version 1.4 introduced experimental support for asyncio, allowing use of most of its interface from async applications. Alembic currently does not provide an async api directly, but it can use an use SQLAlchemy Async engine to run the migrations and autogenerate.

> SQLAlchemy 1.4 版引入了对 `asyncio` 的实验性支持，允许在异步应用程序中使用其大部分接口。 Alembic 目前不直接提供异步 API，但它可以使用 SQLAlchemy 异步引擎来运行迁移和自动生成。

New configurations can use the template “async” to bootstrap an environment which can be used with async DBAPI like asyncpg, running the command:

> 新配置可以使用模板 `“async”` 来引导一个环境，该环境可以与 `asyncpg` 之类的异步 DBAPI 一起使用，运行命令：

```bash
alembic init -t async <script_directory_here>
```

Existing configurations can be updated to use an async DBAPI by updating the `env.py` file that’s used by Alembic to start its operations. In particular only `run_migrations_online` will need to be updated to be something like the example below:

> 通过更新 Alembic 用于启动其操作的 `env.py` 文件，可以更新现有配置以使用异步 DBAPI。 特别是只有 `run_migrations_online` 需要更新为类似于以下示例的内容：

```python
import asyncio

# ... no change required to the rest of the code


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
```

An asnyc application can also interact with the Alembic api directly by using the SQLAlchemy `run_sync` method to adapt the non-async api of Alembic to an async consumer.

> asnyc 应用程序也可以通过使用 SQLAlchemy 的 `run_sync` 方法直接与 Alembic api 交互，以使 Alembic 的非异步 api 适应异步使用者。
