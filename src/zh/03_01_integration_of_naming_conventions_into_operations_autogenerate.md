# Integration of Naming Conventions into Operations, Autogenerate

[Operations]: ../en/ops.html#alembic.operations.Operations
[Operations.f()]: ../en/ops.html#alembic.operations.Operations.f
[Configuring Constraint Naming Conventions]: https://docs.sqlalchemy.org/en/14/core/constraints.html#constraint-naming-conventions

As of Alembic 0.6.4, the naming convention feature is integrated into the **[Operations]** object, so that the convention takes effect for any constraint that is otherwise unnamed. The naming convention is passed to **[Operations]** using the **MigrationsContext.configure.target_metadata** parameter in `env.py`, which is normally configured when autogenerate is used:

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

```python
op.add_column('sometable', Column('q', Boolean(name='q_bool')))
```

The Boolean type will render a CHECK constraint with the name `"ck_sometable_q_bool"`, assuming the backend in use does not support native boolean types.

We can also use op directives with constraints and not give them a name at all, if the naming convention doesn’t require one. The value of `None` will be converted into a name that follows the appropriate naming conventions:

```python
def upgrade():
    op.create_unique_constraint(None, 'some_table', 'x')
```

When autogenerate renders constraints in a migration script, it renders them typically with their completed name. If using at least Alembic 0.6.4 as well as SQLAlchemy 0.9.4, these will be rendered with a special directive **[Operations.f()]** which denotes that the string has already been tokenized:

```python
def upgrade():
    op.create_unique_constraint(op.f('uq_const_x'), 'some_table', 'x')
```

For more detail on the naming convention feature, see [Configuring Constraint Naming Conventions].
