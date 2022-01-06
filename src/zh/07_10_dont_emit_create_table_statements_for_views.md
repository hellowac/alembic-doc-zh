# Don’t emit CREATE TABLE statements for Views

[Table]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table
[include_object]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.include_object
[EnvironmentContext.configure()]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure

It is sometimes convenient to create **[Table]** instances for views so that they can be queried using normal SQLAlchemy techniques. Unfortunately this causes Alembic to treat them as tables in need of creation and to generate spurious `create_table()` operations. This is easily fixable by flagging such Tables and using the **[include_object]** hook to exclude them:

```python
my_view = Table('my_view', metadata, autoload=True, info=dict(is_view=True))    # Flag this as a view
```

Then define `include_object` as:

```python
def include_object(object, name, type_, reflected, compare_to):
    """
    Exclude views from Alembic's consideration.
    """

    return not object.info.get('is_view', False)
```

Finally, in `env.py` pass your `include_object` as a keyword argument to **[EnvironmentContext.configure()]**.
