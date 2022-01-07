# Generating SQL Scripts (a.k.a. “Offline Mode”)

**生成SQL脚本(又称离线模式)**

A major capability of Alembic is to generate migrations as SQL scripts, instead of running them against the database - this is also referred to as offline mode. This is a critical feature when working in large organizations where access to DDL is restricted, and SQL scripts must be handed off to DBAs. Alembic makes this easy via the `--sql` option passed to any `upgrade` or `downgrade` command. We can, for example, generate a script that revises up to rev `ae1027a6acf`:

> Alembic 的一个主要功能是将迁移生成为 SQL 脚本，而不是针对数据库运行它们 - 这也称为离线模式。 在限制访问 DDL 且 SQL 脚本必须交给 DBA 的大型组织中工作时，这是一项关键功能。 Alembic 通过传递给任何`upgrade` 或 `downgrade`命令的 `--sql` 选项使这变得容易。 例如，我们可以生成一个脚本，修改为修订版 `ae1027a6acf`：

```sql
$ alembic upgrade ae1027a6acf --sql
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL
);

INFO  [alembic.context] Running upgrade None -> 1975ea83b712
CREATE TABLE account (
    id SERIAL NOT NULL,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(200),
    PRIMARY KEY (id)
);

INFO  [alembic.context] Running upgrade 1975ea83b712 -> ae1027a6acf
ALTER TABLE account ADD COLUMN last_transaction_date TIMESTAMP WITHOUT TIME ZONE;

INSERT INTO alembic_version (version_num) VALUES ('ae1027a6acf');

COMMIT;
```

While the logging configuration dumped to standard error, the actual script was dumped to standard output - so in the absence of further configuration (described later in this section), we’d at first be using output redirection to generate a script:

> 当日志配置转发到标准错误时，实际的脚本消息被转发到标准输出 - 所以在没有进一步配置的情况下（本节稍后描述），我们首先使用输出重定向来生成脚本：

```bash
alembic upgrade ae1027a6acf --sql > migration.sql
```
