# Affecting the Rendering of Types Themselves

[EnvironmentContext.configure.user_module_prefix]: ../zh/08_02_01_02_configure.md#user_module_prefix
[EnvironmentContext.configure.render_item]: ../zh/08_02_01_02_configure.md#render_item
[AutogenContext]: ../zh/08_06_03_autogenerating_custom_operation_directives.md
[AutogenContext.imports]: ../zh/08_06_03_autogenerating_custom_operation_directives.md#imports

The methodology Alembic uses to generate SQLAlchemy and user-defined type constructs as Python code is plain old `__repr__()`. SQLAlchemy’s built-in types for the most part have a `__repr__()` that faithfully renders a Python-compatible constructor call, but there are some exceptions, particularly in those cases when a constructor accepts arguments that aren’t compatible with `__repr__()`, such as a pickling function.

> Alembic 用来生成 SQLAlchemy 和 用户自定义的类型的构造方法是 Python 的旧的生成文本的 `__repr__()` 方法。 SQLAlchemy 的内置类型大部分都有一个 `__repr__()`，它忠实地呈现与 Python 兼容的构造函数调用，但也有一些例外，特别是在构造函数接受与 `__repr__()` 不兼容的参数的情况下，例如 pick 函数。

When building a custom type that will be rendered into a migration script, it is often necessary to explicitly give the type a `__repr__()` that will faithfully reproduce the constructor for that type. This, in combination with **[EnvironmentContext.configure.user_module_prefix]**, is usually enough. However, if additional behaviors are needed, a more comprehensive hook is the **[EnvironmentContext.configure.render_item]** option. This hook allows one to provide a callable function within `env.py` that will fully take over how a type is rendered, including its module prefix:

> 在构建将呈现到迁移脚本中的自定义类型时，通常需要显式地为该类型指定一个 `__repr__()`，以便忠实地重现该类型的构造函数。 这与 **[EnvironmentContext.configure.user_module_prefix]** 结合使用通常就足够了。 但是，如果需要额外的行为，更全面的钩子是 **[EnvironmentContext.configure.render_item]** 选项。 这个钩子允许在 `env.py` 中提供一个可调用函数，它将完全接管一个类型的呈现方式，包括它的模块前缀：

```python
def render_item(type_, obj, autogen_context):
    """Apply custom rendering for selected items."""

    if type_ == 'type' and isinstance(obj, MySpecialType):
        return "mypackage.%r" % obj

    # default rendering for other objects
    return False

def run_migrations_online():
    # ...

    context.configure(
                connection=connection,
                target_metadata=target_metadata,
                render_item=render_item,
                # ...
                )

    # ...
```

In the above example, we’d ensure our `MySpecialType` includes an appropriate `__repr__()` method, which is invoked when we call it against `"%r"`.

> 在上面的示例中，我们将确保我们的 `MySpecialType` 包含一个适当的 `__repr__()` 方法，当我们针对 `"%r"` 调用它时会调用它。

The callable we use for **[EnvironmentContext.configure.render_item]** can also add imports to our migration script. The **[AutogenContext]** passed in contains a datamember called **[AutogenContext.imports]**, which is a Python `set()` for which we can add new imports. For example, if `MySpecialType` were in a module called `mymodel.types`, we can add the import for it as we encounter the type:

> 我们用于 **[EnvironmentContext.configure.render_item]** 的可调用对象也可以将导入添加到我们的迁移脚本中。 传入的 **[AutogenContext]** 包含一个名为 **[AutogenContext.imports]** 的数据成员，它是一个 Python `set()`，我们可以为其添加新的导入。 例如，如果 `MySpecialType` 在名为 `mymodel.types` 的模块中，我们可以在遇到类型时为其添加导入：

```python
def render_item(type_, obj, autogen_context):
    """Apply custom rendering for selected items."""

    if type_ == 'type' and isinstance(obj, MySpecialType):
        # add import for this type
        autogen_context.imports.add("from mymodel import types")
        return "types.%r" % obj

    # default rendering for other objects
    return False
```

The finished migration script will include our imports where the `${imports}` expression is used, producing output such as:

> 完成的迁移脚本将包含我们的导入，其中使用了 `${imports}` 表达式，产生如下输出：

```python
from alembic import op
import sqlalchemy as sa
from mymodel import types

def upgrade():
    op.add_column('sometable', Column('mycolumn', types.MySpecialType()))
```
