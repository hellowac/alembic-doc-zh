# create_check_constraint

**create_check_constraint**(*constraint_name*:  [str], *condition*:  TextClause, **kw) → Optional\[Table\]

[str]: https://docs.python.org/3/library/stdtypes.html#str
[Operations.create_check_constraint()]: ../zh/06_01_05_create_check_constraint.md

Issue a “create check constraint” instruction using the current batch migration context.

The batch form of this call omits the `source` and `schema` arguments from the call.

**See also:**

* **[Operations.create_check_constraint()]**
