# Relative Migration Identifiers

**相对迁移标识符**

Relative upgrades/downgrades are also supported. To move two versions from the current, a decimal value “+N” can be supplied:

> 还支持相对升级/降级。 要从当前移动两个版本，可以提供十进制值“+N”：

```bash
alembic upgrade +2
```

Negative values are accepted for downgrades:

> 降级接受负值：

```bash
alembic downgrade -1
```

Relative identifiers may also be in terms of a specific revision. For example, to upgrade to revision `ae1027a6acf` plus two additional steps:

> 相对标识符也可以是特定版本。 例如，要升级到修订版 `ae1027a6acf` 加上两个额外的步骤：

```bash
alembic upgrade ae10+2
```
