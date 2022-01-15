# Operation Reference

**操作参考**

[Operations]: ../zh/06_01_operations.md
[Operation Plugins]: ../en/api/operations.html#operation-plugins
[Operation Directives]: ../en/api/operations.html#alembic-operations-toplevel
[Table]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table
[Constraint]: https://docs.sqlalchemy.org/en/14/core/constraints.html#sqlalchemy.schema.Constraint
[add_column()]: #alembic.operations.Operations.add_column
[create_table()]: #alembic.operations.Operations.create_table
[Column]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column
[MigrationContext]: ../en/api/runtime.html#alembic.runtime.migration.MigrationContext
[EnvironmentContext.configure()]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure
[EnvironmentContext.run_migrations()]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.run_migrations

This file provides documentation on Alembic migration directives.

> 此文件提供有关 Alembic 迁移指令的文档。

The directives here are used within user-defined migration files, within the `upgrade()` and `downgrade()` functions, as well as any functions further invoked by those.

> 此处的指令用于 **用户定义的迁移文件**、**upgrade()** 和 **downgrade()** 函数以及由这些函数进一步调用的任何函数。

All directives exist as methods on a class called **[Operations]**. When migration scripts are run, this object is made available to the script via the `alembic.op` datamember, which is a proxy to an actual instance of **[Operations]**. Currently, `alembic.op` is a real Python module, populated with individual proxies for each method on **[Operations]**, so symbols can be imported safely from the `alembic.op` namespace.

> 所有指令都作为称为 **[Operations]** 的类上的方法存在。 运行迁移脚本时，该对象通过 `alembic.op` 数据成员对脚本可用，该数据成员是操作的实际实例的代理。 目前，`alembic.op` 是一个真正的 Python 模块，为操作上的每个方法填充了单独的代理，因此可以从 `alembic.op` 命名空间安全地导入符号。

The **[Operations]** system is also fully extensible. See **[Operation Plugins]** for details on this.

> **[Operations]系统** 也是完全可扩展的。 有关这方面的详细信息，请参阅 **[Operation Plugins]** 。

A key design philosophy to the **[Operation Directives]** methods is that to the greatest degree possible, they internally generate the appropriate SQLAlchemy metadata, typically involving **[Table]** and **[Constraint]** objects. This so that migration instructions can be given in terms of just the string names and/or flags involved. The exceptions to this rule include the **[add_column()]** and **[create_table()]** directives, which require full **[Column]** objects, though the table metadata is still generated here.

> **[Operation Directives]** 方法的一个关键设计理念是尽可能地在内部生成适当的 SQLAlchemy 元数据，通常涉及 **[Table]** 和 **[Constraint]** 对象。 这样就可以仅根据所涉及的字符串名称和/或标志给出迁移指令。 此规则的例外情况包括 **[add_column()]** 和 **[create_table()]** 指令，它们需要完整的 **[Column]** 对象，但仍会在此处生成表元数据。

The functions here all require that a **[MigrationContext]** has been configured within the `env.py` script first, which is typically via **[EnvironmentContext.configure()]**. Under normal circumstances they are called from an actual migration script, which itself would be invoked by the **[EnvironmentContext.run_migrations()]** method.

> 这里的函数都需要首先在 `env.py` 脚本中配置 **[MigrationContext]**，这通常是通过 **[EnvironmentContext.configure()]**。 在正常情况下，它们是从实际的迁移脚本中调用的，该脚本本身将由 **[EnvironmentContext.run_migrations()]** 方法调用。
