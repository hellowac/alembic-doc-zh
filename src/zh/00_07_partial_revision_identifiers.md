# Partial Revision Identifiers

**部分修订标识符**

Any time we need to refer to a revision number explicitly, we have the option to use a partial number. As long as this number uniquely identifies the version, it may be used in any command in any place that version numbers are accepted:

> 任何时候我们需要明确引用修订号，我们都可以选择使用部分编号。 只要这个数字唯一标识版本，它就可以在任何接受版本号的地方用在任何命令中：

```bash
alembic upgrade ae1
```

Above, we use `ae1` to refer to revision `ae1027a6acf`. Alembic will stop and let you know if more than one version starts with that prefix.

> 上面，我们使用 `ae1` 来指代修订版 `ae1027a6acf`。 如果有多个版本以该前缀开头，Alembic 将停止并通知您。
