# Controlling the Module Prefix

[EnvironmentContext.configure.sqlalchemy_module_prefix]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.sqlalchemy_module_prefix
[EnvironmentContext.configure.user_module_prefix]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.user_module_prefix

When types are rendered, they are generated with a **module prefix**, so that they are available based on a relatively small number of imports. The rules for what the prefix is is based on the kind of datatype as well as configurational settings. For example, when Alembic renders SQLAlchemy types, it will by default prefix the type name with the prefix `sa.`:

```python
Column("my_column", sa.Integer())
```

The use of the sa. prefix is controllable by altering the value of **[EnvironmentContext.configure.sqlalchemy_module_prefix]**:

```python
def run_migrations_online():
    # ...

    context.configure(
                connection=connection,
                target_metadata=target_metadata,
                sqlalchemy_module_prefix="sqla.",
                # ...
                )

    # ...
```

In either case, the `sa.` prefix, or whatever prefix is desired, should also be included in the imports section of `script.py.mako`; it also defaults to `import sqlalchemy as sa.`

For user-defined types, that is, any custom type that is not within the `sqlalchemy.` module namespace, by default Alembic will use the **value of \_\_module\_\_ for the custom type**:

```python
Column("my_column", myapp.models.utils.types.MyCustomType())
```

The imports for the above type again must be made present within the migration, either manually, or by adding it to `script.py.mako`.

The above custom type has a long and cumbersome name based on the use of `__module__` directly, which also implies that lots of imports would be needed in order to accommodate lots of types. For this reason, it is recommended that user-defined types used in migration scripts be made available from a single module. Suppose we call it `myapp.migration_types`:

```python
# myapp/migration_types.py

from myapp.models.utils.types import MyCustomType
```

We can first add an import for `migration_types` to our `script.py.mako`:

```python
from alembic import op
import sqlalchemy as sa
import myapp.migration_types
${imports if imports else ""}
```

We then override Alembic’s use of `__module__` by providing a fixed prefix, using the **[EnvironmentContext.configure.user_module_prefix]** option:

```python
def run_migrations_online():
    # ...

    context.configure(
                connection=connection,
                target_metadata=target_metadata,
                user_module_prefix="myapp.migration_types.",
                # ...
                )

    # ...
```

Above, we now would get a migration like:

```python
Column("my_column", myapp.migration_types.MyCustomType())
```

Now, when we inevitably refactor our application to move `MyCustomType` somewhere else, we only need modify the `myapp.migration_types` module, instead of searching and replacing all instances within our migration scripts.
