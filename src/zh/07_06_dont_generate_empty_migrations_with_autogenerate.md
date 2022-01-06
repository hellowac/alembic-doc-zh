# Don’t Generate Empty Migrations with Autogenerate

**不要使用 Autogenerate 生成空迁移**

[EnvironmentContext.configure.process_revision_directives]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.process_revision_directives
[MigrationContext.configure()]: ../en/api/runtime.html#alembic.runtime.migration.MigrationContext.configure
[MigrationScript]: ../en/api/operations.html#alembic.operations.ops.MigrationScript

A common request is to have the `alembic revision --autogenerate` command not actually generate a revision file if no changes to the schema is detected. Using the **[EnvironmentContext.configure.process_revision_directives]** hook, this is straightforward; place a `process_revision_directives` hook in **[MigrationContext.configure()]** which removes the single **[MigrationScript]** directive if it is empty of any operations:

```python
def run_migrations_online():

    # ...

    def process_revision_directives(context, revision, directives):
        if config.cmd_opts.autogenerate:
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []


    # connectable = ...

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives
        )

        with context.begin_transaction():
            context.run_migrations()
```
