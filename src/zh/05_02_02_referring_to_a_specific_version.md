# Referring to a Specific Version

**引用特定版本**

We can pass a specific version number to `upgrade`. Alembic will ensure that all revisions upon which this version depends are invoked, and nothing more. So if we `upgrade` either to `27c6a30d7c24` or `ae1027a6acf` specifically, it guarantees that `1975ea83b712` will have been applied, but not that any “sibling” versions are applied:

```bash
$ alembic upgrade 27c6a
INFO  [alembic.migration] Running upgrade  -> 1975ea83b712, create account table
INFO  [alembic.migration] Running upgrade 1975ea83b712 -> 27c6a30d7c24, add shopping cart table
```

With `1975ea83b712` and `27c6a30d7c24` applied, `ae1027a6acf` is just a single additional step:

```bash
$ alembic upgrade ae102
INFO  [alembic.migration] Running upgrade 1975ea83b712 -> ae1027a6acf, add a column
```
