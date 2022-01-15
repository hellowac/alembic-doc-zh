# alembic.operations.Operations

*class* alembic.operations.**Operations**(*migration_context*: MigrationContext, *impl*: Optional\[BatchOperationsImpl\] = None)

[MigrationContext]: ../en/api/runtime.html#alembic.runtime.migration.MigrationContext
[Operations]: ../zh/06_01_operations.md
[EnvironmentContext.run_migrations()]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.run_migrations
[Operations.register_operation()]: ../zh/06_01_25_register_operation.md

Define high level migration operations.

> 定义高级迁移操作。

Each operation corresponds to some schema migration operation, executed against a particular **[MigrationContext]** which in turn represents connectivity to a database, or a file output stream.

> 每个操作对应于一些模式迁移操作，针对特定的 **[MigrationContext]** 执行，而后者又表示与数据库或文件输出流的连接。

While **[Operations]** is normally configured as part of the **[EnvironmentContext.run_migrations()]** method called from an `env.py` script, a standalone **[Operations]** instance can be made for use cases external to regular Alembic migrations by passing in a **[MigrationContext]**:

> 虽然 **[Operations]** 通常配置为从 `env.py` 脚本调用的 **[EnvironmentContext.run_migrations()]** 方法的一部分，但可以通过传入 **[MigrationContext]** 为常规 Alembic 迁移之外的用例创建独立的 **[Operations]实例**：

```python
from alembic.migration import MigrationContext
from alembic.operations import Operations

conn = myengine.connect()
ctx = MigrationContext.configure(conn)
op = Operations(ctx)

op.alter_column("t", "c", nullable=True)
```

> **Note** that as of 0.8, most of the methods on this class are produced dynamically using the **[Operations.register_operation()]** method.
>
> 请注意，从 0.8 开始，此类中的大多数方法都是使用 **[Operations.register_operation()]** 方法动态生成的。

Construct a new **[Operations]**

> 构建一个新的 **[Operations]**

**参数:**

*migration_context* – a **[MigrationContext]** instance. (一个 **[MigrationContext]** 实例)
