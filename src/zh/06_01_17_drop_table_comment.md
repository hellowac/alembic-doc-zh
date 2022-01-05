# drop_table_comment

**drop_table_comment**(*table_name*:  [str], *existing_comment*:  Optional\[[str]\] = None, *schema*:  Optional\[[str]\] = None) → Optional\[Table\]

[str]: https://docs.python.org/3/library/stdtypes.html#str
[Operations.create_table_comment()]: ../zh/06_01_11_create_table_comment.md
[Operations.alter_column.comment]: ../zh/06_01_02_alter_column.md#params.comment

Issue a “drop table comment” operation to remove an existing comment set on a table.

*New in version 1.0.6.*

**Parameters:**

* ***table_name*** – string name of the target table.
* ***existing_comment*** – An optional string value of a comment already registered on the specified table.

**See also:**

* **[Operations.create_table_comment()]**
* **[Operations.alter_column.comment]**
