# Omitting Schema Names from the Autogenerate Process

[EnvironmentContext.configure.include_schemas]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.include_schemas
[get_schema_names()]: https://docs.sqlalchemy.org/en/14/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_schema_names
[Inspector]: https://docs.sqlalchemy.org/en/14/core/reflection.html#sqlalchemy.engine.reflection.Inspector
[Specifying the Schema Name]: https://docs.sqlalchemy.org/en/14/core/metadata.html#schema-table-schema-name
[get_table_names()]: https://docs.sqlalchemy.org/en/14/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_table_names
[Table]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table
[get_columns()]: https://docs.sqlalchemy.org/en/14/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_columns
[get_indexes()]: https://docs.sqlalchemy.org/en/14/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_indexes
[get_unique_constraints()]: https://docs.sqlalchemy.org/en/14/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_unique_constraints
[get_foreign_keys()]: https://docs.sqlalchemy.org/en/14/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_foreign_keys

[MetaData]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.MetaData
[EnvironmentContext.configure.include_schemas]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.include_schemas
[EnvironmentContext.configure.include_name]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.include_name

As the above set of database objects are typically to be compared to the contents of a single **[MetaData]** object, particularly when the **[EnvironmentContext.configure.include_schemas]** flag is enabled there is an important need to filter out unwanted “schemas”, which for some database backends might be the list of all the databases present. This filtering is best performed using the **[EnvironmentContext.configure.include_name]** hook, which provides for a callable that may return a boolean true/false indicating if a particular schema name should be included:

> 由于上述数据库对象集通常与单个 **[MetaData]** 对象的内容进行比较，特别是在启用 **[EnvironmentContext.configure.include_schemas]** 标志时，非常需要过滤掉不需要的“模式”，这对于某些数据库后端 可能是所有存在的数据库的列表。 最好使用 **[EnvironmentContext.configure.include_name]** 钩子执行此过滤，它提供了一个可调用对象，该可调用对象可能返回一个布尔值 true/false，指示是否应包含特定的模式名称：

```python
def include_name(name, type_, parent_names):
    if type_ == "schema":
        # note this will not include the default schema
        return name in ["schema_one", "schema_two"]
    else:
        return True

context.configure(
    # ...
    include_schemas = True,
    include_name = include_name
)
```

Above, when the list of schema names is first retrieved, the names will be filtered through the above `include_name` function so that only schemas named `"schema_one"` and `"schema_two"` will be considered by the autogenerate process.

> 上面，当第一次检索模式名称列表时，将通过上述 `include_name` 函数过滤名称，以便自动生成过程仅考虑名为`“schema_one”`和“`schema_two”`的模式。

In order to include **the default schema**, that is, the schema that is referred towards by the database connection **without** any explicit schema being specified, the name passed to the hook is `None`. To alter our above example to also include the default schema, we compare to `None` as well:

> 为了包含默认架构，即数据库连接所引用的架构，而没有指定任何显式架构，传递给钩子的名称为 `None`。 为了将上面的示例更改为也包含默认模式，我们还将与 `None` 进行比较：

```python
def include_name(name, type_, parent_names):
    if type_ == "schema":
        # this **will* include the default schema
        return name in [None, "schema_one", "schema_two"]
    else:
        return True

context.configure(
    # ...
    include_schemas = True,
    include_name = include_name
)
```
