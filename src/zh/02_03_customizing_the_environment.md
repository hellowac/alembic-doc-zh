# Customizing the Environment

[EnvironmentContext.is_offline_mode()]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.is_offline_mode
[EnvironmentContext.configure()]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure

Users of the `--sql` option are encouraged to hack their env.py files to suit their needs. The env.py script as provided is broken into two sections: `run_migrations_online()` and `run_migrations_offline()`. Which function is run is determined at the bottom of the script by reading **[EnvironmentContext.is_offline_mode()]**, which basically determines if the `--sql` flag was enabled.

For example, a multiple database configuration may want to run through each database and set the output of the migrations to different named files - the **[EnvironmentContext.configure()]** function accepts a parameter `output_buffer` for this purpose. Below we illustrate this within the `run_migrations_offline()` function:

> 鼓励使用 `--sql` 选项的用户修改他们的 `env.py` 文件以满足他们的需要。 提供的 `env.py` 脚本分为两部分：`run_migrations_online()` 和 `run_migrations_offline()`。 运行哪个函数是在脚本底部通过读取 **[EnvironmentContext.is_offline_mode()]** 确定的，它基本上确定是否启用了 `--sql` 标志。
>
> 例如，多数据库配置可能希望通过每个数据库运行并将迁移的输出设置为不同的命名文件 - 为此，**[EnvironmentContext.configure()]** 函数接受一个参数 `output_buffer`。 下面我们在 `run_migrations_offline()` 函数中说明这一点：

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
