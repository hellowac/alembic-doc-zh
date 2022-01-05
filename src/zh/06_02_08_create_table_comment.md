# create_table_comment

**create_table_comment**(comment, existing_comment=None)

Emit a COMMENT ON operation to set the comment for a table using the current batch migration context.

> *New in version 1.6.0.*

**Parameters:**

* ***comment*** – string value of the **comment** being registered against the specified table.
* ***existing_comment*** – String value of a comment already registered on the specified table, used within autogenerate so that the operation is reversible, but not required for direct use.
