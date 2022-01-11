# Omitting Based on Object

[EnvironmentContext.configure.include_object]: http://localhost:3002/en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.include_object
[Table]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table
[MetaData]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.MetaData
[Column]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column
[info]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column.info

The **[EnvironmentContext.configure.include_object]** hook provides for object-level inclusion/exclusion rules based on the **[Table]** object being reflected as well as the elements within it. This hook can be used to limit objects both from the local **[MetaData]** collection as well as from the target database. The limitation is that when it reports on objects in the database, it will have fully reflected that object, which can be expensive if a large number of objects will be omitted. The example below refers to a fine-grained rule that will skip changes on **[Column]** objects that have a user-defined flag `skip_autogenerate` placed into the **[info]** dictionary:

> **[EnvironmentContext.configure.include_object]** 钩子提供了基于被反映的 **[Table]** 对象以及其中的元素的对象级包含/排除规则。 此钩子可用于限制来自本地 **[MetaData]** 集合以及来自目标数据库的对象。 限制是，当它报告数据库中的对象时，它会完全反映该对象，如果将省略大量对象，这可能会很昂贵。 下面的示例引用了一个细粒度的规则，该规则将跳过对 **[Column]** 对象的更改，这些对象将用户定义的标志 `skip_autogenerate` 放置到 **[info]** 字典中：

```python
def include_object(object, name, type_, reflected, compare_to):
    if (type_ == "column" and
        not reflected and
        object.info.get("skip_autogenerate", False)):
        return False
    else:
        return True

context.configure(
    # ...
    include_object = include_object
)
```
