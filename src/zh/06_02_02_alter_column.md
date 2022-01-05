# alter_column

**alter_column**(*column_name*:  [str], *nullable*:  Optional\[[bool]\] = None, *comment*:  [bool] = False, *server_default*:  Union\[Function, [bool]\] = False, *new_column_name*:  Optional\[[str]\] = None, *type_*:  Optional\[Union\[TypeEngine, Type\[TypeEngine\]\]\] = None, *existing_type*:  Optional\[Union\[TypeEngine, Type\[TypeEngine\]\]\] = None, *existing_server_default*:  [bool] = False, *existing_nullable*:  [None] = [None], *existing_comment*:  [None] = [None], *insert_before*:  [None] = [None], *insert_after*:  [None] = [None], **kw) → Optional\[Table\]

[str]: https://docs.python.org/3/library/stdtypes.html#str
[bool]: https://docs.python.org/3/library/functions.html#bool
[None]: https://docs.python.org/3/library/constants.html#None
[Operations.alter_column()]: ../zh/06_01_02_alter_column.md
[BatchOperations.alter_column.insert_before]: #alembic.operations.BatchOperations.alter_column.params.insert_before
[BatchOperations.alter_column.insert_after]: #alembic.operations.BatchOperations.alter_column.params.insert_after

Issue an “alter column” instruction using the current batch migration context.

Parameters are the same as that of **[Operations.alter_column()]**, as well as the following option(s):

**Parameters:**

* ***insert_before*** – String name of an existing column which this column should be placed before, when creating the new table.
    > *New in version 1.4.0.*
* ***insert_after*** – String name of an existing column which this column should be placed after, when creating the new table. If both **[BatchOperations.alter_column.insert_before]** and **[BatchOperations.alter_column.insert_after]** are omitted, the column is inserted after the last existing column in the table.
    > *New in version 1.4.0.*

**See also:**

* **[Operations.alter_column()]**
