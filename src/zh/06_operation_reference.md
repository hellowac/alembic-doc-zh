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

The directives here are used within user-defined migration files, within the `upgrade()` and `downgrade()` functions, as well as any functions further invoked by those.

All directives exist as methods on a class called **[Operations]**. When migration scripts are run, this object is made available to the script via the `alembic.op` datamember, which is a proxy to an actual instance of **[Operations]**. Currently, `alembic.op` is a real Python module, populated with individual proxies for each method on **[Operations]**, so symbols can be imported safely from the `alembic.op` namespace.

The **[Operations]** system is also fully extensible. See **[Operation Plugins]** for details on this.

A key design philosophy to the **[Operation Directives]** methods is that to the greatest degree possible, they internally generate the appropriate SQLAlchemy metadata, typically involving **[Table]** and **[Constraint]** objects. This so that migration instructions can be given in terms of just the string names and/or flags involved. The exceptions to this rule include the **[add_column()]** and **[create_table()]** directives, which require full **[Column]** objects, though the table metadata is still generated here.

The functions here all require that a **[MigrationContext]** has been configured within the `env.py` script first, which is typically via **[EnvironmentContext.configure()]**. Under normal circumstances they are called from an actual migration script, which itself would be invoked by the **[EnvironmentContext.run_migrations()]** method.
