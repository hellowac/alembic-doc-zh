# Working with Explicit Branches

**使用显式分支**

[Relative Migration Identifiers]: ../en/tutorial.html#relative-migrations

The `alembic upgrade` command hinted at other options besides merging when dealing with multiple heads. Let’s back up and assume we’re back where we have as our heads just `ae1027a6acf` and `27c6a30d7c24`:

```bash
$ alembic heads
27c6a30d7c24
ae1027a6acf
```

Earlier, when we did `alembic upgrade head`, it gave us an error which suggested `please specify a specific target revision, '<branchname>@head' to narrow to a specific head, or 'heads' for all heads` in order to proceed without merging. Let’s cover those cases.
