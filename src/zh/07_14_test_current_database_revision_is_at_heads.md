# Test current database revision is at head(s)

[MigrationContext.get_current_heads()]: ../en/api/runtime.html#alembic.runtime.migration.MigrationContext.get_current_heads
[ScriptDirectory.get_heads()]: ../en/api/script.html#alembic.script.ScriptDirectory.get_heads

A recipe to determine if a database schema is up to date in terms of applying Alembic migrations. May be useful for test or installation suites to determine if the target database is up to date. Makes use of the **[MigrationContext.get_current_heads()]** as well as **[ScriptDirectory.get_heads()]** methods so that it accommodates for a branched revision tree:

```python
from alembic import config, script
from alembic.runtime import migration
from sqlalchemy import engine


def check_current_head(alembic_cfg, connectable):
    # type: (config.Config, engine.Engine) -> bool
    directory = script.ScriptDirectory.from_config(alembic_cfg)
    with connectable.begin() as connection:
        context = migration.MigrationContext.configure(connection)
        return set(context.get_current_heads()) == set(directory.get_heads())

e = engine.create_engine("mysql://scott:tiger@localhost/test", echo=True)
cfg = config.Config("alembic.ini")
print(check_current_head(cfg, e))
```

**See also:**

* **[MigrationContext.get_current_heads()]**

* **[ScriptDirectory.get_heads()]**
