# Viewing History Ranges

**查看历史范围**

Using the `-r` option to `alembic history`, we can also view various slices of history. The `-r` argument accepts an argument `[start]:[end]`, where either may be a revision number, symbols like `head`, `heads` or `base`, `current` to specify the current revision(s), as well as negative relative ranges for `[start]` and positive relative ranges for `[end]`:

> 使用 `alembic history` 的 `-r` 选项，我们还可以查看历史片段。 `-r` 参数接受一个参数 `[start]:[end]`，其中可以是一个修订号，像 `head`、`heads` 或 `base`、`current` 这样的符号来指定当前的修订版本，以及`[start]` 的负相对范围和`[end]` 的正相对范围：

```bash
alembic history -r1975ea:ae1027
```

A relative range starting from three revisions ago up to current migration, which will invoke the migration environment against the database to get the current migration:

> 从前三个修订版本到当前迁移版本的相对范围，它将针对数据库调用迁移环境以获取当前迁移：

```bash
alembic history -r-3:current
```

View all revisions from `1975` to the `head`:

> 查看从`1975`到`head`的所有修订：

```bash
alembic history -r1975ea:
```
