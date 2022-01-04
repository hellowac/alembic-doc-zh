# Omitting Based on Object

[EnvironmentContext.configure.include_object]: http://localhost:3002/en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.include_object
[Table]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table
[MetaData]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.MetaData
[Column]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column
[info]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column.info

The [EnvironmentContext.configure.include_object] hook provides for object-level inclusion/exclusion rules based on the **[Table]** object being reflected as well as the elements within it. This hook can be used to limit objects both from the local **[MetaData]** collection as well as from the target database. The limitation is that when it reports on objects in the database, it will have fully reflected that object, which can be expensive if a large number of objects will be omitted. The example below refers to a fine-grained rule that will skip changes on **[Column]** objects that have a user-defined flag `skip_autogenerate` placed into the **[info]** dictionary:

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
