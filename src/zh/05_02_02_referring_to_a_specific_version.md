# Referring to a Specific Version

**引用特定版本**

We can pass a specific version number to `upgrade`. Alembic will ensure that all revisions upon which this version depends are invoked, and nothing more. So if we `upgrade` either to `27c6a30d7c24` or `ae1027a6acf` specifically, it guarantees that `1975ea83b712` will have been applied, but not that any “sibling” versions are applied:

> 我们可以将特定的版本号传递给`upgrade`。 Alembic 将确保调用此版本所依赖的所有修订，仅此而已。 因此，如果我们将`upgrade` 升级到`27c6a30d7c24` 或`ae1027a6acf`，它保证会应用`1975ea83b712`，但不会应用任何 “兄弟” 版本：

```bash
$ alembic upgrade 27c6a
INFO  [alembic.migration] Running upgrade  -> 1975ea83b712, create account table
INFO  [alembic.migration] Running upgrade 1975ea83b712 -> 27c6a30d7c24, add shopping cart table
```

With `1975ea83b712` and `27c6a30d7c24` applied, `ae1027a6acf` is just a single additional step:

> 应用 `1975ea83b712` 和 `27c6a30d7c24` 后，`ae1027a6acf` 只是一个额外的步骤：

```bash
$ alembic upgrade ae102
INFO  [alembic.migration] Running upgrade 1975ea83b712 -> ae1027a6acf, add a column
```
