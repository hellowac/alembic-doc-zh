# Customizing the Environment

[EnvironmentContext.is_offline_mode()]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.is_offline_mode
[EnvironmentContext.configure()]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure

Users of the `--sql` option are encouraged to hack their env.py files to suit their needs. The env.py script as provided is broken into two sections: `run_migrations_online()` and `run_migrations_offline()`. Which function is run is determined at the bottom of the script by reading **[EnvironmentContext.is_offline_mode()]**, which basically determines if the `--sql` flag was enabled.

For example, a multiple database configuration may want to run through each database and set the output of the migrations to different named files - the **[EnvironmentContext.configure()]** function accepts a parameter `output_buffer` for this purpose. Below we illustrate this within the `run_migrations_offline()` function:

```python
from alembic import context
import myapp
import sys

db_1 = myapp.db_1
db_2 = myapp.db_2

def run_migrations_offline():
    """Run migrations *without* a SQL connection."""

    for name, engine, file_ in [
        ("db1", db_1, "db1.sql"),
        ("db2", db_2, "db2.sql"),
    ]:
        context.configure(
                    url=engine.url,
                    transactional_ddl=False,
                    output_buffer=open(file_, 'w'))
        context.execute("-- running migrations for '%s'" % name)
        context.run_migrations(name=name)
        sys.stderr.write("Wrote file '%s'" % file_)

def run_migrations_online():
    """Run migrations *with* a SQL connection."""

    for name, engine in [
        ("db1", db_1),
        ("db2", db_2),
    ]:
        connection = engine.connect()
        context.configure(connection=connection)
        try:
            context.run_migrations(name=name)
            session.commit()
        except:
            session.rollback()
            raise

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```
