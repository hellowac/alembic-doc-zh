# autocommit_block

**autocommit_block**() → Iterator\[None\]

[Operations.get_context()]: ../en/../ops.html#alembic.operations.Operations.get_context
[MigrationContext]: #alembic.runtime.migration.MigrationContext
[MigrationContext.autocommit_block()]: #alembic.runtime.migration.MigrationContext.autocommit_block
[EnvironmentContext.transaction_per_migration]: #alembic.runtime.environment.EnvironmentContext.params.transaction_per_migration

Enter an “autocommit” block, for databases that support AUTOCOMMIT isolation levels.

This special directive is intended to support the occasional database DDL or system operation that specifically has to be run outside of any kind of transaction block. The PostgreSQL database platform is the most common target for this style of operation, as many of its DDL operations must be run outside of transaction blocks, even though the database overall supports transactional DDL.

The method is used as a context manager within a migration script, by calling on **[Operations.get_context()]** to retrieve the **[MigrationContext]**, then invoking **[MigrationContext]**.autocommit_block() using the `with:` statement:

```python
def upgrade():
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE mood ADD VALUE 'soso'")
```

Above, a PostgreSQL “ALTER TYPE..ADD VALUE” directive is emitted, which must be run outside of a transaction block at the database level. The **[MigrationContext.autocommit_block()]** method makes use of the SQLAlchemy `AUTOCOMMIT` isolation level setting, which against the psycogp2 DBAPI corresponds to the `connection.autocommit` setting, to ensure that the database driver is not inside of a DBAPI level transaction block.

> **Warning:** As is necessary, the database transaction preceding the block is unconditionally committed. This means that the run of migrations preceding the operation will be committed, before the overall migration operation is complete.
>
> It is recommended that when an application includes migrations with “autocommit” blocks, that **[EnvironmentContext.transaction_per_migration]** be used so that the calling environment is tuned to expect short per-file migrations whether or not one of them has an autocommit block.

> *New in version 1.2.0.*
