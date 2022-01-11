# More Label Syntaxes

**更多标注语法**

[Relative Migration Identifiers]: ../zh/00_08_relative_migration_identifiers.md

The `heads` symbol can be combined with a branch label, in the case that your labeled branch itself breaks off into multiple branches:

> `heads` 符号可以与分支标签结合使用，以防你的标签分支本身分裂成多个分支：

```bash
alembic upgrade shoppingcart@heads
```

Relative identifiers, as introduced in **[Relative Migration Identifiers]**, work with labels too. For example, upgrading to `shoppingcart@+2` means to upgrade from current heads on “shoppingcart” upwards two revisions:

> **[Relative Migration Identifiers]** 中介绍的相对标识符也适用于标签。 例如，升级到 `shoppingcart@+2` 意味着将“shoppingcart”上的当前头像向上升级两个版本：

```bash
alembic upgrade shoppingcart@+2
```

This kind of thing works from history as well:

> 这也适用于历史：

```bash
alembic history -r current:shoppingcart@+2
```

The newer `relnum+delta` format can be combined as well, for example if we wanted to list along `shoppingcart` up until two revisions before the head:

> 更新的 `relnum+delta` 格式也可以组合，例如，如果我们想沿着 `shoppingcart` 列出直到head之前的两个修订：

```bash
alembic history -r :shoppingcart@head-2
```
