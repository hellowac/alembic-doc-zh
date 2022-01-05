# create_unique_constraint

**create_unique_constraint**(*constraint_name*:  [str], *columns*:  Sequence\[[str]\], **kw) → Any

[str]: https://docs.python.org/3/library/stdtypes.html#str
[Operations.create_unique_constraint()]: ../zh/06_01_12_create_unique_constraint.md

Issue a “create unique constraint” instruction using the current batch migration context.

The batch form of this call omits the `source` and `schema` arguments from the call.

**See also:**

* **[Operations.create_unique_constraint()]**
