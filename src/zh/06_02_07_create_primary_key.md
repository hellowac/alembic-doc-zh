# create_primary_key

**create_primary_key**(*constraint_name*:  [str], *columns*:  List\[[str]\]) → None

[str]: https://docs.python.org/3/library/stdtypes.html#str
[Operations.create_primary_key()]: ../zh/06_01_09_create_primary_key.md

Issue a “create primary key” instruction using the current batch migration context.

The batch form of this call omits the `table_name` and `schema` arguments from the call.

**See also:**

* **[Operations.create_primary_key()]**
