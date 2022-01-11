# Integration of Naming Conventions into Operations, Autogenerate

[Operations]: ../zh/06_01_operations.md
[Operations.f()]: ../zh/06_01_19_f.md
[Configuring Constraint Naming Conventions]: https://docs.sqlalchemy.org/en/14/core/constraints.html#constraint-naming-conventions
[配置约束命名约定]: https://docs.sqlalchemy.org/en/14/core/constraints.html#constraint-naming-conventions

As of Alembic 0.6.4, the naming convention feature is integrated into the **[Operations]** object, so that the convention takes effect for any constraint that is otherwise unnamed. The naming convention is passed to **[Operations]** using the **MigrationsContext.configure.target_metadata** parameter in `env.py`, which is normally configured when autogenerate is used:

> 从 Alembic 0.6.4 开始，命名约定功能集成到 **[Operations]** 对象中，因此约定对任何未命名的约束生效。 命名约定使用 `env.py` 中的 **MigrationsContext.configure.target_metadata** 参数传递给 **[Operations]** ，通常在使用 autogenerate 时配置：

```python
# in your application's model:

meta = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
      })
Base = declarative_base(metadata=meta)

# .. in your Alembic env.py:

# add your model's MetaData object here
# for 'autogenerate' support
from myapp import mymodel
target_metadata = mymodel.Base.metadata

# ...

def run_migrations_online():

    # ...

    context.configure(
                connection=connection,
                target_metadata=target_metadata
                )
```

Above, when we render a directive like the following:

> 以上，当我们渲染一个指令时：

```python
op.add_column('sometable', Column('q', Boolean(name='q_bool')))
```

The Boolean type will render a CHECK constraint with the name `"ck_sometable_q_bool"`, assuming the backend in use does not support native boolean types.

> 假设使用的后端不支持原生布尔类型，布尔类型将呈现名为 `“ck_sometable_q_bool”` 的 CHECK 约束。

We can also use op directives with constraints and not give them a name at all, if the naming convention doesn’t require one. The value of `None` will be converted into a name that follows the appropriate naming conventions:

> 如果命名约定不需要，我们也可以使用带有约束的 `op` 指令而不给它们命名。 `None` 的值将转换为遵循适当命名约定的名称：

```python
def upgrade():
    op.create_unique_constraint(None, 'some_table', 'x')
```

When autogenerate renders constraints in a migration script, it renders them typically with their completed name. If using at least Alembic 0.6.4 as well as SQLAlchemy 0.9.4, these will be rendered with a special directive **[Operations.f()]** which denotes that the string has already been tokenized:

> 当自动生成在迁移脚本中呈现约束时，它通常使用完整的名称呈现它们。 如果至少使用 Alembic 0.6.4 和 SQLAlchemy 0.9.4，这些将使用特殊指令 **[Operations.f()]** 呈现，表示字符串已经被标记：

```python
def upgrade():
    op.create_unique_constraint(op.f('uq_const_x'), 'some_table', 'x')
```

For more detail on the naming convention feature, see [Configuring Constraint Naming Conventions].

> 有关命名约定功能的更多详细信息，请参阅[配置约束命名约定]。
