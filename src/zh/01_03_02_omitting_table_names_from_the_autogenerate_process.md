# Omitting Table Names from the Autogenerate Process

[EnvironmentContext.configure.include_name]: http://localhost:3002/en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.include_name
[EnvironmentContext.configure.include_object]: http://localhost:3002/en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.include_object
[Operations.drop_table()]: http://localhost:3002/en/ops.html#alembic.operations.Operations.drop_table
[MetaData]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.MetaData
[tables]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.MetaData.tables

The **[EnvironmentContext.configure.include_name]** hook is also most appropriate to limit the names of tables in the target database to be considered. If a target database has many tables that are not part of the **[MetaData]**, the autogenerate process will normally assume these are extraneous tables in the database to be dropped, and it will generate a **[Operations.drop_table()]** operation for each. To prevent this, the **[EnvironmentContext.configure.include_name]** hook may be used to search for each name within the **[tables]** collection of the **[MetaData]** object and ensure names which aren’t present are not included:

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

The **[EnvironmentContext.configure.include_name]** hook only refers to **reflected** objects, and not those located within the target **[MetaData]** collection. For more fine-grained rules that include both **[MetaData]** and reflected object, the **[EnvironmentContext.configure.include_object]** hook discussed in the next section is more appropriate.

> New in version 1.5: added the **[EnvironmentContext.configure.include_name]** hook.
