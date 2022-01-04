# Downgrading

**降级**

We can illustrate a downgrade back to nothing, by calling `alembic downgrade` back to the beginning, which in Alembic is called `base`:

> 我们可以通过调用 `alembic downgrade` 回到最初始状态, 来演示降级到迁移最初始状态，在 Alembic 中称为 `base`：

```bash
$ alembic downgrade base
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
INFO  [alembic.context] Running downgrade ae1027a6acf -> 1975ea83b712
INFO  [alembic.context] Running downgrade 1975ea83b712 -> None
```

Back to nothing - and up again:

> 降级到最初始状态 - 然后再次升级:

```bash
$ alembic upgrade head
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
INFO  [alembic.context] Running upgrade None -> 1975ea83b712
INFO  [alembic.context] Running upgrade 1975ea83b712 -> ae1027a6acf
```
