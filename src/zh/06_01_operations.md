# alembic.operations.Operations

*class* alembic.operations.**Operations**(*migration_context*: MigrationContext, *impl*: Optional\[BatchOperationsImpl\] = None)

[MigrationContext]: ../en/api/runtime.html#alembic.runtime.migration.MigrationContext
[Operations]: ../zh/06_01_operations.md
[EnvironmentContext.run_migrations()]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.run_migrations
[Operations.register_operation()]: ../zh/06_01_25_register_operation.md

Define high level migration operations.

Each operation corresponds to some schema migration operation, executed against a particular **[MigrationContext]** which in turn represents connectivity to a database, or a file output stream.

While **[Operations]** is normally configured as part of the **[EnvironmentContext.run_migrations()]** method called from an `env.py` script, a standalone **[Operations]** instance can be made for use cases external to regular Alembic migrations by passing in a MigrationContext:

```python
from alembic.migration import MigrationContext
from alembic.operations import Operations

conn = myengine.connect()
ctx = MigrationContext.configure(conn)
op = Operations(ctx)

op.alter_column("t", "c", nullable=True)
```

> **Note** that as of 0.8, most of the methods on this class are produced dynamically using the **[Operations.register_operation()]** method.

Construct a new Operations

*migration_context* – a **[MigrationContext]** instance.
