# Running our First Migration

**运行我们的第一次迁移**

We now want to run our migration. Assuming our database is totally clean, it’s as yet unversioned. The `alembic upgrade` command will run upgrade operations, proceeding from the current database revision, in this example `None`, to the given target revision. We can specify `1975ea83b712` as the revision we’d like to upgrade to, but it’s easier in most cases just to tell it “the most recent”, in this case `head`:

> 我们现在想要运行我们的迁移。 假设我们的数据库完全干净，它还没有版本化。 `alembic upgrade` 命令将运行升级操作，从当前数据库修订版（在本例中为“**None**”）到给定的目标修订版。 我们可以指定 `1975ea83b712` 作为我们想要升级到的修订版，但在大多数情况下，告诉它“**最新的**”更容易，在这种情况下是 `head`：

```bash
$ alembic upgrade head
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
INFO  [alembic.context] Running upgrade None -> 1975ea83b712
```

Wow that rocked! Note that the information we see on the screen is the result of the logging configuration set up in `alembic.ini` - logging the `alembic` stream to the console (standard error, specifically).

> 哇，震撼！ 请注意，我们在屏幕上看到的信息是在 `alembic.ini` 中设置的日志配置的结果 - 将 `alembic` 流记录到控制台（特别是标准错误）。

The process which occurred here included that Alembic first checked if the database had a table called `alembic_version`, and if not, created it. It looks in this table for the current version, if any, and then calculates the path from this version to the version requested, in this case `head`, which is known to be `1975ea83b712`. It then invokes the `upgrade()` method in each file to get to the target revision.

> 此处发生的过程包括 Alembic 首先检查数据库是否有名为“**alembic_version**”的表，如果没有，则创建它。 它在此表中查找当前版本（如果有），然后计算从该版本到请求版本的路径，在本例中为 `head`，已知为 `1975ea83b712`。 然后它调用每个文件中的 `upgrade()` 方法以获取目标修订版。
