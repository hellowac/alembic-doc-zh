# Create Operations for the Target Objects

**为目标对象创建操作**

[Operations]: ../zh/06_01_operations.md
[Operations.register_operation()]: ../zh/06_01_25_register_operation.md
[Operations.implementation_for()]: ../zh/06_01_22_implementation_for.md
[Operations.execute()]: ../zh/06_01_18_execute.md

We’ll use the **[Operations]** extension API to make new operations for create, drop, and replace of views and stored procedures. Using this API is also optional; we can just as well make any kind of Python function that we would invoke from our migration scripts. However, using this API gives us operations built directly into the Alembic `op.*` namespace very nicely.

> 我们将使用 **[Operations]** 扩展 API 来创建、删除和替换视图和存储过程的新操作。 使用此 API 也是可选的； 我们也可以创建从迁移脚本中调用的任何类型的 Python 函数。 然而，使用这个 API 可以很好地为我们提供直接内置到 Alembic `op.*` 命名空间中的操作。

The most intricate class is below. This is the base of our “replaceable” operation, which includes not just a base operation for emitting CREATE and DROP instructions on a `ReplaceableObject`, it also assumes a certain model of “reversibility” which makes use of references to other migration files in order to refer to the “previous” version of an object:

> 最复杂的`Class`如下。 这是我们“可替换”操作的基础，它不仅包括在可替换对象上发出 `CREATE` 和 `DROP` 指令的基本操作，它还假设了某种“可逆性”模型，该模型利用对其他迁移文件的引用来实现。 参考对象的“先前”版本：

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

> 当我们通过这个例子时，这个类的工作应该会变得很清楚。 为了从这个基础创建可用的操作，我们将构建一系列存根类并使用 **[Operations.register_operation()]** 使它们成为 `op.*` 命名空间的一部分：

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

> 要实际运行像 “CREATE VIEW” 和 “DROP SEQUENCE” 这样的 SQL，我们将使用直接运行到 **[Operations.execute()]** 的 **[Operations.implementation_for()]** 提供实现：

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

> 上述所有代码都可以出现在应用程序源代码树中的任何位置； 唯一的要求是，当调用 `env.py` 脚本时，它包含最终调用这些类以及 `Operations.register_operation()` 和 `Operations.implementation_for()` 序列的导入。
