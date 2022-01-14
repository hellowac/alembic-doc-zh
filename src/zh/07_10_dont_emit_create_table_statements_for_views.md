# Don’t emit CREATE TABLE statements for Views

[Table]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table
[include_object]: ../zh/08_02_01_02_configure.md#include_object
[EnvironmentContext.configure()]: ../zh/08_02_01_02_configure.md

It is sometimes convenient to create **[Table]** instances for views so that they can be queried using normal SQLAlchemy techniques. Unfortunately this causes Alembic to treat them as tables in need of creation and to generate spurious `create_table()` operations. This is easily fixable by flagging such Tables and using the **[include_object]** hook to exclude them:

> 有时为视图创建 **[Table]** 实例很方便，以便可以使用普通的 SQLAlchemy 技术来查询它们。 不幸的是，这导致 Alembic 将它们视为需要创建的表并生成虚假的 `create_table()` 操作。 这很容易通过标记此类表并使用 **[include_object]** 钩子排除它们来解决：

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

> 最后，在 `env.py` 中将您的 `include_object` 作为关键字参数传递给 **[EnvironmentContext.configure()]**。
