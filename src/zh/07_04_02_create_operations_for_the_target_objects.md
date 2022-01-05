# Create Operations for the Target Objects

**为目标对象创建操作**

[Operations]: ../zh/06_01_operations.md
[Operations.register_operation()]: ../zh/06_01_25_register_operation.md
[Operations.implementation_for()]: ../zh/06_01_22_implementation_for.md
[Operations.execute()]: ../zh/06_01_18_execute.md

We’ll use the **[Operations]** extension API to make new operations for create, drop, and replace of views and stored procedures. Using this API is also optional; we can just as well make any kind of Python function that we would invoke from our migration scripts. However, using this API gives us operations built directly into the Alembic `op.*` namespace very nicely.

The most intricate class is below. This is the base of our “replaceable” operation, which includes not just a base operation for emitting CREATE and DROP instructions on a `ReplaceableObject`, it also assumes a certain model of “reversibility” which makes use of references to other migration files in order to refer to the “previous” version of an object:

```python
from alembic.operations import Operations, MigrateOperation

class ReversibleOp(MigrateOperation):
    def __init__(self, target):
        self.target = target

    @classmethod
    def invoke_for_target(cls, operations, target):
        op = cls(target)
        return operations.invoke(op)

    def reverse(self):
        raise NotImplementedError()

    @classmethod
    def _get_object_from_version(cls, operations, ident):
        version, objname = ident.split(".")

        module = operations.get_context().script.get_revision(version).module
        obj = getattr(module, objname)
        return obj

    @classmethod
    def replace(cls, operations, target, replaces=None, replace_with=None):

        if replaces:
            old_obj = cls._get_object_from_version(operations, replaces)
            drop_old = cls(old_obj).reverse()
            create_new = cls(target)
        elif replace_with:
            old_obj = cls._get_object_from_version(operations, replace_with)
            drop_old = cls(target).reverse()
            create_new = cls(old_obj)
        else:
            raise TypeError("replaces or replace_with is required")

        operations.invoke(drop_old)
        operations.invoke(create_new)
```

The workings of this class should become clear as we walk through the example. To create usable operations from this base, we will build a series of stub classes and use **[Operations.register_operation()]** to make them part of the `op.*` namespace:

```python
@Operations.register_operation("create_view", "invoke_for_target")
@Operations.register_operation("replace_view", "replace")
class CreateViewOp(ReversibleOp):
    def reverse(self):
        return DropViewOp(self.target)


@Operations.register_operation("drop_view", "invoke_for_target")
class DropViewOp(ReversibleOp):
    def reverse(self):
        return CreateViewOp(self.target)


@Operations.register_operation("create_sp", "invoke_for_target")
@Operations.register_operation("replace_sp", "replace")
class CreateSPOp(ReversibleOp):
    def reverse(self):
        return DropSPOp(self.target)


@Operations.register_operation("drop_sp", "invoke_for_target")
class DropSPOp(ReversibleOp):
    def reverse(self):
        return CreateSPOp(self.target)
```

To actually run the SQL like “CREATE VIEW” and “DROP SEQUENCE”, we’ll provide implementations using **[Operations.implementation_for()]** that run straight into **[Operations.execute()]**:

```python
@Operations.implementation_for(CreateViewOp)
def create_view(operations, operation):
    operations.execute("CREATE VIEW %s AS %s" % (
        operation.target.name,
        operation.target.sqltext
    ))


@Operations.implementation_for(DropViewOp)
def drop_view(operations, operation):
    operations.execute("DROP VIEW %s" % operation.target.name)


@Operations.implementation_for(CreateSPOp)
def create_sp(operations, operation):
    operations.execute(
        "CREATE FUNCTION %s %s" % (
            operation.target.name, operation.target.sqltext
        )
    )


@Operations.implementation_for(DropSPOp)
def drop_sp(operations, operation):
    operations.execute("DROP FUNCTION %s" % operation.target.name)
```

All of the above code can be present anywhere within an application’s source tree; the only requirement is that when the `env.py` script is invoked, it includes imports that ultimately call upon these classes as well as the **[Operations.register_operation()]** and **[Operations.implementation_for()]** sequences.
