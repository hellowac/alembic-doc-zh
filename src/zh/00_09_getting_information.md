# Getting Information

**获取信息**

With a few revisions present we can get some information about the state of things.

> 通过一些修改，我们可以获得一些关于迁移版本状态的信息。

First we can view the current revision:

> 首先我们可以查看当前版本：

```bash
$ alembic current
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
Current revision for postgresql://scott:XXXXX@localhost/test: 1975ea83b712 -> ae1027a6acf (head), Add a column
```

`head` is displayed only if the revision identifier for this database matches the head revision.

> 仅当此数据库的修订标识符与头部修订匹配时才显示 `head`。

We can also view history with `alembic history`; the `--verbose` option (accepted by several commands, including `history`, `current`, `heads` and `branches`) will show us full information about each revision:

> 我们也可以用`alembic history`命令查看历史； `--verbose` 选项（多个命令都接受改选项，包括 `history`、`current`、`heads` 和 `branches`）将向我们显示每个版本的完整信息：

```bash
$ alembic history --verbose

Rev: ae1027a6acf (head)
Parent: 1975ea83b712
Path: /path/to/yourproject/alembic/versions/ae1027a6acf_add_a_column.py

    add a column

    Revision ID: ae1027a6acf
    Revises: 1975ea83b712
    Create Date: 2014-11-20 13:02:54.849677

Rev: 1975ea83b712
Parent: <base>
Path: /path/to/yourproject/alembic/versions/1975ea83b712_add_account_table.py

    create account table

    Revision ID: 1975ea83b712
    Revises:
    Create Date: 2014-11-20 13:02:46.257104
```
