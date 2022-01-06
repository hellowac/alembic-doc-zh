# Don’t generate any DROP TABLE directives with autogenerate

[EnvironmentContext.configure.include_object]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.include_object

When running autogenerate against a database that has existing tables outside of the application’s autogenerated metadata, it may be desirable to prevent autogenerate from considering any of those existing tables to be dropped. This will prevent autogenerate from detecting tables removed from the local metadata as well however this is only a small caveat.

The most direct way to achieve this using the **[EnvironmentContext.configure.include_object]** hook. There is no need to hardcode a fixed “whitelist” of table names; the hook gives enough information in the given arguments to determine if a particular table name is not part of the local `MetaData` being autogenerated, by checking first that the type of object is `"table"`, then that `reflected` is `True`, indicating this table name is from the local database connection, not the `MetaData`, and finally that `compare_to` is `None`, indicating autogenerate is not comparing this `Table` to any `Table` in the local `MetaData` collection:

```python
# in env.py

def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and reflected and compare_to is None:
        return False
    else:
        return True


context.configure(
    # ...
    include_object = include_object
)
```