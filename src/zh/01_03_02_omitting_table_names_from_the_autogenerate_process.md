# Omitting Table Names from the Autogenerate Process

[EnvironmentContext.configure.include_name]: http://localhost:3002/en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.include_name
[EnvironmentContext.configure.include_object]: http://localhost:3002/en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.include_object
[Operations.drop_table()]: http://localhost:3002/en/ops.html#alembic.operations.Operations.drop_table
[MetaData]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.MetaData
[tables]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.MetaData.tables

The **[EnvironmentContext.configure.include_name]** hook is also most appropriate to limit the names of tables in the target database to be considered. If a target database has many tables that are not part of the **[MetaData]**, the autogenerate process will normally assume these are extraneous tables in the database to be dropped, and it will generate a **[Operations.drop_table()]** operation for each. To prevent this, the **[EnvironmentContext.configure.include_name]** hook may be used to search for each name within the **[tables]** collection of the **[MetaData]** object and ensure names which aren’t present are not included:

> **[EnvironmentContext.configure.include_name]** 钩子也最适合限制目标数据库中的表名。 如果目标数据库有许多不属于元数据的表，自动生成过程通常会假定这些是数据库中要删除的无关表，并且将为每个表生成一个 **[Operations.drop_table()]**  操作。 为了防止这种情况，**[EnvironmentContext.configure.include_name]** 钩子可用于搜索 **[MetaData]** 对象的**表集合**(**[tables]**)中的每个名称，并确保不包含不存在的名称：

```python
target_metadata = MyModel.metadata

def include_name(name, type_, parent_names):
    if type_ == "table":
        return name in target_metadata.tables
    else:
        return True

context.configure(
    # ...
    target_metadata = target_metadata,
    include_name = include_name,
    include_schemas = False
)
```

The above example is limited to table names present in the default schema only. In order to search within a **[MetaData]** collection for schema-qualified table names as well, a table present in the non default schema will be present under a name of the form `<schemaname>.<tablename>`. The **[EnvironmentContext.configure.include_name]** hook will present this schema name on a per-tablename basis in the `parent_names` dictionary, using the key `"schema_name"` that refers to the name of the schema currently being considered, or `None` if the schema is the default schema of the database connection:

> 上面的示例仅限于默认模式中存在的表名。 为了在 **[MetaData]** 集合中搜索模式限定的表名，非默认模式中的表将以 `<schemaname>.<tablename>` 形式的名称出现。 **[EnvironmentContext.configure.include_name]** 钩子将在 `parent_names` 字典中基于每个表名显示此模式名称，使用键`“schema_name”`表示当前正在考虑的模式的名称，或者如果数据库连接模式是默认模式，则为 `None`：

```python
# example fragment

if parent_names["schema_name"] is None:
    return name in target_metadata.tables
else:
    # build out schema-qualified name explicitly...
    return (
        "%s.%s" % (parent_names["schema_name"], name) in
        target_metadata.tables
    )
```

However more simply, the `parent_names` dictionary will also include the dot-concatenated name already constructed under the key `"schema_qualified_table_name"`, which will also be suitably formatted for tables in the default schema as well with the dot omitted. So the full example of omitting tables with schema support may look like:

> 然而更简单地说，`parent_names` 字典还将包括已经在键`“schema_qualified_table_name”`下构建的点连接名称，该名称也将适用于默认模式中的表以及过滤点的格式。 因此，过滤具有模式支持的表的完整示例可能如下所示：

```python
target_metadata = MyModel.metadata

def include_name(name, type_, parent_names):
    if type_ == "schema":
        return name in [None, "schema_one", "schema_two"]
    elif type_ == "table":
        # use schema_qualified_table_name directly
        return (
            parent_names["schema_qualified_table_name"] in
            target_metadata.tables
        )
    else:
        return True

context.configure(
    # ...
    target_metadata = target_metadata,
    include_name = include_name,
    include_schemas = True
)
```

The `parent_names` dictionary will also include the key `"table_name"` when the name being considered is that of a column or constraint object local to a particular table.

> 当所考虑的名称是特定表本地的列或约束对象的名称时，`parent_names` 字典还将包括键`“table_name”`。

The **[EnvironmentContext.configure.include_name]** hook only refers to **reflected** objects, and not those located within the target **[MetaData]** collection. For more fine-grained rules that include both **[MetaData]** and reflected object, the **[EnvironmentContext.configure.include_object]** hook discussed in the next section is more appropriate.

> **[EnvironmentContext.configure.include_name]** 钩子仅引用反射对象，而不是位于目标 **[MetaData]** 集合中的对象。 对于同时包含 **[MetaData]** 和反射对象的更细粒度的规则，下一节讨论的 **[EnvironmentContext.configure.include_object]** 钩子更合适。

> New in version 1.5: added the **[EnvironmentContext.configure.include_name]** hook.

> 版本1.5更新: 新增 **[EnvironmentContext.configure.include_name]** 钩子
