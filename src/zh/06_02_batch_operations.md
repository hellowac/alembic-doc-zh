# alembic.operations.BatchOperations

*class* alembic.operations.**BatchOperations**(*migration_context*:  MigrationContext, *impl*:  Optional\[BatchOperationsImpl\] = None)

[Operations]: ../zh/06_01_operations.md
[Operations.batch_alter_table()]: ../zh/06_01_03_batch_alter_table.md
[Operations.register_operation()]: ../zh/06_01_25_register_operation.md
[MigrationContext]: ../en/api/runtime.html#alembic.runtime.migration.MigrationContext

Modifies the interface **[Operations]** for batch mode.

This basically omits the `table_name` and `schema` parameters from associated methods, as these are a given when running under batch mode.

**See also: [Operations.batch_alter_table()]**

> **Note:** that as of 0.8, most of the methods on this class are produced dynamically using the **[Operations.register_operation()]** method.

Construct a new [Operations]

**Parameters:**

* ***migration_context*** – a **[MigrationContext]** instance.
