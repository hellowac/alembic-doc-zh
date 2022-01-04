# Getting the Start Version

Notice that our migration script started at the base - this is the default when using offline mode, as no database connection is present and there’s no `alembic_version` table to read from.

One way to provide a starting version in offline mode is to provide a range to the command line. This is accomplished by providing the “version” in `start:end` syntax:

```bash
alembic upgrade 1975ea83b712:ae1027a6acf --sql > migration.sql
```

The `start:end` syntax is only allowed in offline mode; in “online” mode, the `alembic_version` table is always used to get at the current version.

It’s also possible to have the `env.py` script retrieve the “last” version from the local environment, such as from a local file. A scheme like this would basically treat a local file in the same way `alembic_version` works:

```python
if context.is_offline_mode():
    version_file = os.path.join(os.path.dirname(config.config_file_name), "version.txt")
    if os.path.exists(version_file):
        current_version = open(version_file).read()
    else:
        current_version = None
    context.configure(dialect_name=engine.name, starting_rev=current_version)
    context.run_migrations()
    end_version = context.get_revision_argument()
    if end_version and end_version != current_version:
        open(version_file, 'w').write(end_version)
```
