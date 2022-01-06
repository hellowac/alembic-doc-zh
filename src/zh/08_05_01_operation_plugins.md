# Operation Plugins

[MigrateOperation]: #alembic.operations.ops.MigrateOperation
[Operations.register_operation()]: ../en/../ops.html#alembic.operations.Operations.register_operation
[Operations.implementation_for()]: ../en/../ops.html#alembic.operations.Operations.implementation_for
[Operations.execute()]: ../en/../ops.html#alembic.operations.Operations.execute
[Custom SQL Constructs and Compilation Extension]: https://docs.sqlalchemy.org/en/14/core/compiler.html#sqlalchemy-ext-compiler-toplevel
[MigrationContext.run_migrations()]: ../en/runtime.html#alembic.runtime.migration.MigrationContext.run_migrations
[Autogenerating Custom Operation Directives]: ../en/autogenerate.html#autogen-custom-ops

The Operations object is extensible using a plugin system. This system allows one to add new `op.<some_operation>` methods at runtime. The steps to use this system are to first create a subclass of **[MigrateOperation]**, register it using the **[Operations.register_operation()]** class decorator, then build a default “implementation” function which is established using the **[Operations.implementation_for()]** decorator.

Below we illustrate a very simple operation `CreateSequenceOp` which will implement a new method `op.create_sequence()` for use in migration scripts:

```python
from alembic.operations import Operations, MigrateOperation

@Operations.register_operation("create_sequence")
class CreateSequenceOp(MigrateOperation):
    """Create a SEQUENCE."""

    def __init__(self, sequence_name, schema=None):
        self.sequence_name = sequence_name
        self.schema = schema

    @classmethod
    def create_sequence(cls, operations, sequence_name, **kw):
        """Issue a "CREATE SEQUENCE" instruction."""

        op = CreateSequenceOp(sequence_name, **kw)
        return operations.invoke(op)

    def reverse(self):
        # only needed to support autogenerate
        return DropSequenceOp(self.sequence_name, schema=self.schema)

@Operations.register_operation("drop_sequence")
class DropSequenceOp(MigrateOperation):
    """Drop a SEQUENCE."""

    def __init__(self, sequence_name, schema=None):
        self.sequence_name = sequence_name
        self.schema = schema

    @classmethod
    def drop_sequence(cls, operations, sequence_name, **kw):
        """Issue a "DROP SEQUENCE" instruction."""

        op = DropSequenceOp(sequence_name, **kw)
        return operations.invoke(op)

    def reverse(self):
        # only needed to support autogenerate
        return CreateSequenceOp(self.sequence_name, schema=self.schema)
```

Above, the `CreateSequenceOp` and `DropSequenceOp` classes represent new operations that will be available as `op.create_sequence()` and `op.drop_sequence()`. The reason the operations are represented as stateful classes is so that an operation and a specific set of arguments can be represented generically; the state can then correspond to different kinds of operations, such as invoking the instruction against a database, or autogenerating Python code for the operation into a script.

In order to establish the migrate-script behavior of the new operations, we use the **[Operations.implementation_for()]** decorator:

```python
@Operations.implementation_for(CreateSequenceOp)
def create_sequence(operations, operation):
    if operation.schema is not None:
        name = "%s.%s" % (operation.schema, operation.sequence_name)
    else:
        name = operation.sequence_name
    operations.execute("CREATE SEQUENCE %s" % name)


@Operations.implementation_for(DropSequenceOp)
def drop_sequence(operations, operation):
    if operation.schema is not None:
        name = "%s.%s" % (operation.schema, operation.sequence_name)
    else:
        name = operation.sequence_name
    operations.execute("DROP SEQUENCE %s" % name)
```

Above, we use the simplest possible technique of invoking our DDL, which is just to call **[Operations.execute()]** with literal SQL. If this is all a custom operation needs, then this is fine. However, options for more comprehensive support include building out a custom SQL construct, as documented at **[Custom SQL Constructs and Compilation Extension]**.

With the above two steps, a migration script can now use new methods `op.create_sequence()` and `op.drop_sequence()` that will proxy to our object as a classmethod:

```python
def upgrade():
    op.create_sequence("my_sequence")

def downgrade():
    op.drop_sequence("my_sequence")
```

The registration of new operations only needs to occur in time for the `env.py` script to invoke MigrationContext.run_migrations(); within the module level of the `env.py` script is sufficient.

**See also:**

[Autogenerating Custom Operation Directives] - how to add autogenerate support to custom operations.
