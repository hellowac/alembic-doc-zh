# create_foreign_key

**create_foreign_key**(*constraint_name*:  [str], *referent_table*:  [str], *local_cols*:  List\[[str]\], *remote_cols*:  List\[[str]\], *referent_schema*:  Optional\[[str]\] = None, *onupdate*:  [None] = [None], *ondelete*:  [None] = [None], *deferrable*:  [None] = [None], *initially*:  [None] = [None], *match*:  [None] = [None], **dialect_kw) → None

[str]: https://docs.python.org/3/library/stdtypes.html#str
[None]: https://docs.python.org/3/library/constants.html#None
[Operations.create_foreign_key()]: ../zh/06_01_07_create_foreign_key.md

Issue a “create foreign key” instruction using the current batch migration context.

The batch form of this call omits the `source` and `source_schema` arguments from the call.

e.g.:

```python
with batch_alter_table("address") as batch_op:
    batch_op.create_foreign_key(
                "fk_user_address",
                "user", ["user_id"], ["id"])
```

**See also:**

* **[Operations.create_foreign_key()]**
