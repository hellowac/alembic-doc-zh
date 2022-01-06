## The Migration Context

[MigrationContext]: ../en/api/runtime.html#alembic.runtime.migration.MigrationContext
[on_version_apply]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.on_version_apply
[str]: https://docs.python.org/3/library/stdtypes.html#str
[EnvironmentContext.get_context()]: #alembic.runtime.environment.EnvironmentContext.get_context
[MigrationContext.configure()]: #alembic.runtime.migration.MigrationContext.configure
[MigrationContext.get_current_revision()]: #alembic.runtime.migration.MigrationContext.get_current_revision
[Operations]: ../en/ops.html#alembic.operations.Operations

The [MigrationContext] handles the actual work to be performed against a database backend as migration operations proceed. It is generally not exposed to the end-user, except when the [on_version_apply] callback hook is used.

### *class* alembic.runtime.migration.MigrationContext(*dialect*: Dialect, *connection*: Optional\[Connection\], *opts*: Dict\[[str], Any\], *environment_context*: Optional\[EnvironmentContext\] = None)

Represent the database state made available to a migration script.

MigrationContext is the front end to an actual database connection, or alternatively a string output stream given a particular database dialect, from an Alembic perspective.

When inside the `env.py` script, the **[MigrationContext]** is available via the **[EnvironmentContext.get_context()]** method, which is available at `alembic.context`:

```python
# from within env.py script
from alembic import context
migration_context = context.get_context()
```

For usage outside of an `env.py` script, such as for utility routines that want to check the current version in the database, the **[MigrationContext.configure()]** method to create new **[MigrationContext]** objects. For example, to get at the current revision in the database using **[MigrationContext]**.get_current_revision():

```python
# in any application, outside of an env.py script
from alembic.migration import MigrationContext
from sqlalchemy import create_engine

engine = create_engine("postgresql://mydatabase")
conn = engine.connect()

context = MigrationContext.configure(conn)
current_rev = context.get_current_revision()
```

The above context can also be used to produce Alembic migration operations with an **[Operations]** instance:

```python
# in any application, outside of the normal Alembic environment
from alembic.operations import Operations
op = Operations(context)
op.alter_column("mytable", "somecolumn", nullable=True)
```
