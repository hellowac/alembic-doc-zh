# More Label Syntaxes

**更多标注语法**

[Relative Migration Identifiers]: ../en/tutorial.html#relative-migrations

The `heads` symbol can be combined with a branch label, in the case that your labeled branch itself breaks off into multiple branches:

```bash
alembic upgrade shoppingcart@heads
```

Relative identifiers, as introduced in **[Relative Migration Identifiers]**, work with labels too. For example, upgrading to `shoppingcart@+2` means to upgrade from current heads on “shoppingcart” upwards two revisions:

```bash
alembic upgrade shoppingcart@+2
```

This kind of thing works from history as well:

```bash
alembic history -r current:shoppingcart@+2
```

The newer `relnum+delta` format can be combined as well, for example if we wanted to list along `shoppingcart` up until two revisions before the head:

```bash
alembic history -r :shoppingcart@head-2
```
