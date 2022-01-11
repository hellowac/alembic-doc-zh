# Controlling the Module Prefix

[EnvironmentContext.configure.sqlalchemy_module_prefix]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.sqlalchemy_module_prefix
[EnvironmentContext.configure.user_module_prefix]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.user_module_prefix

When types are rendered, they are generated with a **module prefix**, so that they are available based on a relatively small number of imports. The rules for what the prefix is is based on the kind of datatype as well as configurational settings. For example, when Alembic renders SQLAlchemy types, it will by default prefix the type name with the prefix `sa.`:

> 渲染类型时，会使用 **模块前缀** 生成它们，以便它们基于相对少量的导入可用。 前缀的规则基于数据类型的种类以及配置设置。 例如，当 Alembic 呈现 SQLAlchemy 类型时，默认情况下，它会在类型名称前加上前缀 `sa.`：

```python
Column("my_column", sa.Integer())
```

The use of the sa. prefix is controllable by altering the value of **[EnvironmentContext.configure.sqlalchemy_module_prefix]**:

> 使用`sa.`前缀可以通过改变 **[EnvironmentContext.configure.sqlalchemy_module_prefix]** 的值来控制：

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

> 在任何一种情况下，`sa.` 前缀，或任何需要的前缀，也应该包含在 `script.py.mako` 的导入部分中； 它还默认为`import sqlalchemy as sa.`

For user-defined types, that is, any custom type that is not within the `sqlalchemy.` module namespace, by default Alembic will use the **value of \_\_module\_\_ for the custom type**:

> 对于用户定义的类型，即不在 `sqlalchemy.` 模块命名空间内的任何自定义类型，默认情况下，Alembic 将使用 **value of \_\_module\_\_ 作为自定义类型**：

```python
Column("my_column", myapp.models.utils.types.MyCustomType())
```

The imports for the above type again must be made present within the migration, either manually, or by adding it to `script.py.mako`.

> 上述类型的导入必须再次出现在迁移中，要么手动，要么通过将其添加到 `script.py.mako`。

The above custom type has a long and cumbersome name based on the use of `__module__` directly, which also implies that lots of imports would be needed in order to accommodate lots of types. For this reason, it is recommended that user-defined types used in migration scripts be made available from a single module. Suppose we call it `myapp.migration_types`:

> 基于直接使用 `__module__` ，上述自定义类型的名称又长又麻烦，这也意味着需要大量导入才能容纳大量类型。 因此，建议将迁移脚本中使用的用户定义类型提供给单个模块。 假设我们称之为 `myapp.migration_types`：

```python
# myapp/migration_types.py

from myapp.models.utils.types import MyCustomType
```

We can first add an import for `migration_types` to our `script.py.mako`:

> 我们可以首先将 `migration_types` 的导入添加到 `script.py.mako` 中：

```python
from alembic import op
import sqlalchemy as sa
import myapp.migration_types
${imports if imports else ""}
```

We then override Alembic’s use of `__module__` by providing a fixed prefix, using the **[EnvironmentContext.configure.user_module_prefix]** option:

> 然后，我们通过使用 **[EnvironmentContext.configure.user_module_prefix]** 选项提供固定前缀来覆盖 Alembic 对 `__module__` 的使用：

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

> 经过上面设置，我们现在会得到如下迁移：

```python
Column("my_column", myapp.migration_types.MyCustomType())
```

Now, when we inevitably refactor our application to move `MyCustomType` somewhere else, we only need modify the `myapp.migration_types` module, instead of searching and replacing all instances within our migration scripts.

> 现在，当我们不可避免地重构我们的应用程序以将 `MyCustomType` 移动到其他地方时，我们只需要修改 `myapp.migration_types` 模块，而不是搜索和替换迁移脚本中的所有实例。
