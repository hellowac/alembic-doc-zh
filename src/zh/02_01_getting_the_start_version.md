# Getting the Start Version

**获取起始版本**

Notice that our migration script started at the base - this is the default when using offline mode, as no database connection is present and there’s no `alembic_version` table to read from.

One way to provide a starting version in offline mode is to provide a range to the command line. This is accomplished by providing the “version” in `start:end` syntax:

> 请注意，我们的迁移脚本从base开始 - 这是使用离线模式时的默认设置，因为不存在数据库连接并且没有 `alembic_version` 表可供读取。
>
> 在离线模式下提供起始版本的一种方法是为命令行提供范围。 这是通过在 `start:end` 语法中提供 “version” (版本)来实现的：

```bash
alembic upgrade 1975ea83b712:ae1027a6acf --sql > migration.sql
```

The `start:end` syntax is only allowed in offline mode; in “online” mode, the `alembic_version` table is always used to get at the current version.

It’s also possible to have the `env.py` script retrieve the “last” version from the local environment, such as from a local file. A scheme like this would basically treat a local file in the same way `alembic_version` works:

> `start:end` 语法只允许在离线模式下使用； 在“online”(在线)模式下，总是使用 `alembic_version` 表来获取当前版本。
>
> 也可以让 `env.py` 脚本从本地环境（例如本地文件）中检索“last”(最后)版本。 像这样的方案基本上会以与 `alembic_version` 相同的方式处理本地文件：

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
