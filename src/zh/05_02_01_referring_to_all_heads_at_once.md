# Referring to all heads at once

**一次引用到所有的head**

The `heads` identifier is a lot like `head`, except it explicitly refers to all `heads` at once. That is, it’s like telling Alembic to do the operation for both `ae1027a6acf` and `27c6a30d7c24` simultaneously. If we started from a fresh database and ran upgrade `heads` we’d see:

```bash
$ alembic upgrade heads
INFO  [alembic.migration] Context impl PostgresqlImpl.
INFO  [alembic.migration] Will assume transactional DDL.
INFO  [alembic.migration] Running upgrade  -> 1975ea83b712, create account table
INFO  [alembic.migration] Running upgrade 1975ea83b712 -> ae1027a6acf, add a column
INFO  [alembic.migration] Running upgrade 1975ea83b712 -> 27c6a30d7c24, add shopping cart table
```

Since we’ve upgraded to `heads`, and we do in fact have more than one head, that means these two distinct `heads` are now in our `alembic_version` table. We can see this if we run `alembic current`:

```bash
$ alembic current
ae1027a6acf (head)
27c6a30d7c24 (head)
```

That means there’s two rows in `alembic_version` right now. If we downgrade one step at a time, Alembic will **delete** from the `alembic_version` table each branch that’s closed out, until only one branch remains; then it will continue updating the single value down to the previous versions:

```bash
$ alembic downgrade -1
INFO  [alembic.migration] Running downgrade ae1027a6acf -> 1975ea83b712, add a column

$ alembic current
27c6a30d7c24 (head)

$ alembic downgrade -1
INFO  [alembic.migration] Running downgrade 27c6a30d7c24 -> 1975ea83b712, add shopping cart table

$ alembic current
1975ea83b712 (branchpoint)

$ alembic downgrade -1
INFO  [alembic.migration] Running downgrade 1975ea83b712 -> , create account table

$ alembic current
```
