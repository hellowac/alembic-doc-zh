# Affecting the Rendering of Types Themselves

[EnvironmentContext.configure.user_module_prefix]: /en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.user_module_prefix
[EnvironmentContext.configure.render_item]: /en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.render_item
[AutogenContext]: ../en/api/autogenerate.html#alembic.autogenerate.api.AutogenContext
[AutogenContext.imports]: ../en/api/autogenerate.html#alembic.autogenerate.api.AutogenContext.imports

The methodology Alembic uses to generate SQLAlchemy and user-defined type constructs as Python code is plain old `__repr__()`. SQLAlchemy’s built-in types for the most part have a `__repr__()` that faithfully renders a Python-compatible constructor call, but there are some exceptions, particularly in those cases when a constructor accepts arguments that aren’t compatible with `__repr__()`, such as a pickling function.

When building a custom type that will be rendered into a migration script, it is often necessary to explicitly give the type a `__repr__()` that will faithfully reproduce the constructor for that type. This, in combination with **[EnvironmentContext.configure.user_module_prefix]**, is usually enough. However, if additional behaviors are needed, a more comprehensive hook is the **[EnvironmentContext.configure.render_item]** option. This hook allows one to provide a callable function within `env.py` that will fully take over how a type is rendered, including its module prefix:

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

The callable we use for **[EnvironmentContext.configure.render_item]** can also add imports to our migration script. The **[AutogenContext]** passed in contains a datamember called **[AutogenContext.imports]**, which is a Python `set()` for which we can add new imports. For example, if `MySpecialType` were in a module called `mymodel.types`, we can add the import for it as we encounter the type:

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

```python
from alembic import op
import sqlalchemy as sa
from mymodel import types

def upgrade():
    op.add_column('sometable', Column('mycolumn', types.MySpecialType()))
```
