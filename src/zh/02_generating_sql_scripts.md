# Generating SQL Scripts (a.k.a. “Offline Mode”)

**生成SQL脚本(又称离线模式)**

A major capability of Alembic is to generate migrations as SQL scripts, instead of running them against the database - this is also referred to as offline mode. This is a critical feature when working in large organizations where access to DDL is restricted, and SQL scripts must be handed off to DBAs. Alembic makes this easy via the `--sql` option passed to any `upgrade` or `downgrade` command. We can, for example, generate a script that revises up to rev `ae1027a6acf`:

```bash
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

```bash
alembic upgrade ae1027a6acf --sql > migration.sql
```
