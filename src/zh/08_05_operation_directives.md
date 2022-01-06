# Operation Directives

[Operation Reference]: ../en/../ops.html#ops
[Operations]: ../en/../ops.html#alembic.operations.Operations
[MigrationContext]: ../en/runtime.html#alembic.runtime.migration.MigrationContext
[Operation Plugins]: #operation-plugins

> **Note:** this section discusses the **internal API of Alembic** as regards the internal system of defining migration operation directives. This section is only useful for developers who wish to extend the capabilities of Alembic. For end-user guidance on Alembic migration operations, please see **[Operation Reference]**.

Within migration scripts, actual database migration operations are handled via an instance of **[Operations]**. The **[Operations]** class lists out available migration operations that are linked to a **[MigrationContext]**, which communicates instructions originated by the **[Operations]** object into SQL that is sent to a database or SQL output stream.

Most methods on the **[Operations]** class are generated dynamically using a “plugin” system, described in the next section **[Operation Plugins]**. Additionally, when Alembic migration scripts actually run, the methods on the current **[Operations]** object are proxied out to the `alembic.op` module, so that they are available using module-style access.

For an overview of how to use an **[Operations]** object directly in programs, as well as for reference to the standard operation methods as well as “batch” methods, see **[Operation Reference]**.
