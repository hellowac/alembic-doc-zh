# begin_transaction

**begin_transaction**(*_per_migration*:  [bool] = False) → Union\[alembic.runtime.migration._ProxyTransaction, AbstractContextManager\]

[bool]: https://docs.python.org/3/library/functions.html#bool
[MigrationContext.begin_transaction()]: #alembic.runtime.migration.MigrationContext.begin_transaction
[MigrationContext.run_migrations()]: #alembic.runtime.migration.MigrationContext.run_migrations
[EnvironmentContext.configure.transactional_ddl]: #alembic.runtime.environment.EnvironmentContext.configure.params.transactional_ddl
[EnvironmentContext.configure.transaction_per_migration]: #alembic.runtime.environment.EnvironmentContext.configure.params.transaction_per_migration
[MigrationContext.autocommit_block()]: #alembic.runtime.migration.MigrationContext.autocommit_block

Begin a logical transaction for migration operations.

This method is used within an `env.py` script to demarcate where the outer “transaction” for a series of migrations begins. Example:

```python
def run_migrations_online():
    connectable = create_engine(...)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
```

Above, **[MigrationContext.begin_transaction()]** is used to demarcate where the outer logical transaction occurs around the **[MigrationContext.run_migrations()]** operation.

A “Logical” transaction means that the operation may or may not correspond to a real database transaction. If the target database supports transactional DDL (or **[EnvironmentContext.configure.transactional_ddl]** is true), the **[EnvironmentContext.configure.transaction_per_migration]** flag is not set, and the migration is against a real database connection (as opposed to using “offline” `--sql` mode), a real transaction will be started. If `--sql` mode is in effect, the operation would instead correspond to a string such as “BEGIN” being emitted to the string output.

The returned object is a Python context manager that should only be used in the context of a `with:` statement as indicated above. The object has no other guaranteed API features present.

**See also:**

* **[MigrationContext.autocommit_block()]**
