# create_table_comment

**create_table_comment**(*table_name*:  [str], *comment*:  Optional\[[str]\], *existing_comment*:  [None] = [None], *schema*:  Optional\[[str]\] = None) → Optional\[Table\]

[str]: https://docs.python.org/3/library/stdtypes.html#str
[None]: https://docs.python.org/3/library/constants.html#None
[Operations.drop_table_comment()]: ../zh/06_01_17_drop_table_comment.md
[Operations.alter_column.comment]: ../zh/06_01_02_alter_column.md#params.comment

Emit a COMMENT ON operation to set the comment for a table.

*New in version 1.0.6.*

**Parameters:**

* ***table_name*** – string name of the target table.
* ***comment*** – string value of the **comment** being registered against the specified table.
* ***existing_comment*** – String value of a comment already registered on the specified table, used within autogenerate so that the operation is reversible, but not required for direct use.

**See also:**

* **[Operations.drop_table_comment()]**
* **[Operations.alter_column.comment]**
