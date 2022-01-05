# drop_constraint

**drop_constraint**(*constraint_name*:  [str], *type_*:  Optional\[[str]\] = None) → None

[str]: https://docs.python.org/3/library/stdtypes.html#str
[Operations.drop_constraint()]: ../zh/06_01_14_drop_constraint.md

Issue a “drop constraint” instruction using the current batch migration context.

The batch form of this call omits the `table_name` and `schema` arguments from the call.

**See also:**

* **[Operations.drop_constraint()]**
