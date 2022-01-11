# Working with Explicit Branches

**使用显式分支**

[Relative Migration Identifiers]: ../en/tutorial.html#relative-migrations

The `alembic upgrade` command hinted at other options besides merging when dealing with multiple heads. Let’s back up and assume we’re back where we have as our heads just `ae1027a6acf` and `27c6a30d7c24`:

> `alembic upgrade` 命令暗示了在处理多个 `head` 时除了合并之外的其他选项。 让我们备份并假设我们回到了我们头脑中只有 `ae1027a6acf` 和 `27c6a30d7c24` 的地方：

```bash
$ alembic heads
27c6a30d7c24
ae1027a6acf
```

Earlier, when we did `alembic upgrade head`, it gave us an error which suggested `please specify a specific target revision, '<branchname>@head' to narrow to a specific head, or 'heads' for all heads` in order to proceed without merging. Let’s cover those cases.

> 早些时候，当我们做 alembic upgrade head 时，它给了我们一个错误提示 `请指定特定的目标修订，'<branchname>@head'缩小到特定的head，或“heads”用于所有head` 以便在不合并的情况下继续进行。 让我们涵盖这些情况。
