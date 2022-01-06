# Using Asyncio with Alembic

SQLAlchemy version 1.4 introduced experimental support for asyncio, allowing use of most of its interface from async applications. Alembic currently does not provide an async api directly, but it can use an use SQLAlchemy Async engine to run the migrations and autogenerate.

New configurations can use the template “async” to bootstrap an environment which can be used with async DBAPI like asyncpg, running the command:

```bash
alembic init -t async <script_directory_here>
```

Existing configurations can be updated to use an async DBAPI by updating the `env.py` file that’s used by Alembic to start its operations. In particular only `run_migrations_online` will need to be updated to be something like the example below:

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
