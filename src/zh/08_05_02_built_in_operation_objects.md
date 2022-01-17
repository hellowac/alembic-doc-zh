# Built-in Operation Objects

[Operations]: ../en/../ops.html#alembic.operations.Operations
[MigrateOperation]: #alembic.operations.ops.MigrateOperation
[Operations.register_operation()]: ../en/../ops.html#alembic.operations.Operations.register_operation
[Operation Plugins]: #operation-plugins
[Customizing Revision Generation]: ../en/autogenerate.html#customizing-revision

The migration operations present on **[Operations]** are themselves delivered via operation objects that represent an operation and its arguments. All operations descend from the **[MigrateOperation]** class, and are registered with the **[Operations]** class using the **[Operations]**.register_operation() class decorator. The **[MigrateOperation]** objects also serve as the basis for how the autogenerate system renders new migration scripts.

**See also:**

* **[Operation Plugins]**

* **[Customizing Revision Generation]**

The built-in operation objects are listed below.

----

[str]: https://docs.python.org/3/library/stdtypes.html#str
[Operations]: ../en/../ops.html#alembic.operations.Operations
[Operations.add_column()]: ../en/../ops.html#alembic.operations.Operations.add_column
[BatchOperations]: ../en/../ops.html#alembic.operations.BatchOperations
[BatchOperations.add_column()]: ../en/../ops.html#alembic.operations.BatchOperations.add_column

* *class* alembic.operations.ops.**AddColumnOp**(*table_name*:  [str], *column*:  Column, *schema*:  Optional\[[str]\] = None, **kw) → Optional\[Table\] Optional\[Table\]

    Represent an add column operation.

  * *classmethod* **add_column**(*operations*:  Operations, *table_name*:  [str], *column*:  Column, *schema*:  Optional\[[str]\] = None) → Optional\[Table\]

    This method is proxied on the **[Operations]** class, via the **[Operations.add_column()]** method.

  * *classmethod* **batch_add_column**(*operations*:  BatchOperations, *column*:  Column, *insert_before*:  Optional\[[str]\] = None, *insert_after*:  Optional\[[str]\] = None) → Optional\[Table\]

    This method is proxied on the **[BatchOperations]** class, via the **[BatchOperations.add_column()]** method.

----

* *class* alembic.operations.ops.**AddConstraintOp**

    Represent an add constraint operation.

----

[alembic.operations.base.Operations]: ../en/../ops.html#alembic.operations.Operations
[str]: https://docs.python.org/3/library/stdtypes.html#str
[bool]: https://docs.python.org/3/library/functions.html#bool
[alembic.operations.base.BatchOperations]: ../en/../ops.html#alembic.operations.BatchOperations
[None]: https://docs.python.org/3/library/constants.html#None
[Operations]: ../en/../ops.html#alembic.operations.Operations
[Operations.alter_column()]: ../en/../ops.html#alembic.operations.Operations.alter_column
[BatchOperations]: ../en/../ops.html#alembic.operations.BatchOperations
[BatchOperations.alter_column()]: ../en/../ops.html#alembic.operations.BatchOperations.alter_column

* *class* alembic.operations.ops.**AlterColumnOp**(*table_name*:  [str], *column_name*:  [str], *schema*:  Optional\[[str]\] = None, *existing_type*:  Optional\[Any\] = None, *existing_server_default*:  Any = False, *existing_nullable*:  Optional\[[bool]\] = None, *existing_comment*:  Optional\[[str]\] = None, *modify_nullable*:  Optional\[[bool]\] = None, *modify_comment*:  Optional\[Union\[[str], [bool]\]\] = False, *modify_server_default*:  Any = False, *modify_name*:  Optional\[[str]\] = None, *modify_type*:  Optional\[Any\] = None, \*\*kw)

    Represent an alter column operation.

  * *class* alembic.operations.ops.**alter_column batch_alter_column**(*operations*:  [alembic.operations.base.Operations], *table_name*:  [str], *column_name*:  [str], *nullable*:  Optional\[[bool]\] = None, *comment*:  Optional\[Union\[[str], [bool]\]\] = False, *server_default*:  Any = False, *new_column_name*:  Optional\[[str]\] = None, *type_*:  Optional\[Union\[TypeEngine, Type\[TypeEngine\]\]\] = None, *existing_type*:  Optional\[Union\[TypeEngine, Type\[TypeEngine\]\]\] = None, *existing_server_default*:  Optional\[Union\[[str], [bool], Identity, Computed\]\] = False, *existing_nullable*:  Optional\[[bool]\] = None, *existing_comment*:  Optional\[[str]\] = None, *schema*:  Optional\[[str]\] = None,\*\*kw) → Optional\[Table\]
  
    This method is proxied on the **[Operations]** class, via the **[Operations.alter_column()]** method.

  * *class* alembic.operations.ops.**batch_alter_column**(  *operations*:  [alembic.operations.base.BatchOperations], *column_name*:  [str], *nullable*:  Optional\[[bool]\] = None, *comment*:  [bool] = False, *server_default*:  Union\[Function, [bool]\] = False, *new_column_name*:  Optional\[[str]\] = None, *type_*:  Optional\[Union\[TypeEngine, Type\[TypeEngine\]\]\] = None, *existing_type*:  Optional\[Union\[TypeEngine, Type\[TypeEngine\]\]\] = None, *existing_server_default*:  [bool] = False, *existing_nullable*:  [None] = [None], *existing_comment*:  [None] = [None], *insert_before*:  [None] = [None], *insert_after*:  [None] = [None],\*\*kw) → Optional\[Table\]

    This method is proxied on the **[BatchOperations]** class, via the **[BatchOperations.alter_column()]** method.

----

* *class* alembic.operations.ops.**AlterTableOp**(*table_name*:  [str], *schema*:  Optional\[[str]\] = None)

    Represent an alter table operation.

----

[alembic.operations.base.Operations]: ../en/../ops.html#alembic.operations.Operations
[dict]: https://docs.python.org/3/library/stdtypes.html#dict
[bool]: https://docs.python.org/3/library/functions.html#bool
[Operations]: ../en/../ops.html#alembic.operations.Operations
[Operations.bulk_insert()]: ../en/../ops.html#alembic.operations.Operations.bulk_insert

* *class* alembic.operations.ops.**BulkInsertOp**(*table*:  Union\[Table, TableClause\], *rows*:  List\[[dict]\], *multiinsert*:  [bool] = True) → None

    Represent a bulk insert operation.

  * *classmethod* **bulk_insert**(*operations*:  [alembic.operations.base.Operations], *table*:  Union\[Table, TableClause\], *rows*:  List\[[dict]\], *multiinsert*:  [bool] = True) → [None]

    This method is proxied on the **[Operations]** class, via the **[Operations.bulk_insert()]** method.

----

[str]: https://docs.python.org/3/library/stdtypes.html#str
[BatchOperations]: ../en/../ops.html#alembic.operations.BatchOperations
[BatchOperations.create_check_constraint()]: ../en/../ops.html#alembic.operations.BatchOperations.create_check_constraint
[Operations]: ../en/../ops.html#alembic.operations.Operations
[Operations.create_check_constraint()]: ../en/../ops.html#alembic.operations.Operations.create_check_constraint

* *class* alembic.operations.ops.**CreateCheckConstraintOp**(*constraint_name*:  Optional\[[str]\], *table_name*:  [str], *condition*:  Union\[[str], TextClause, ColumnElement\[Any\]\], *schema*:  Optional\[[str]\] = None, \*\*kw)

    Represent a create check constraint operation.

  * *classmethod* **batch_create_check_constraint**(*operations*:  BatchOperations, *constraint_name*:  [str], *condition*:  TextClause, \*\*kw) → [None]

      This method is proxied on the **[BatchOperations]** class, via the **[BatchOperations.create_check_constraint()]** method.

  * *classmethod* **create_check_constraint**(*operations*:  Operations, *constraint_name*:  Optional\[[str]\], *table_name*:  [str], *condition*:  Union\[[str], BinaryExpression\], *schema*:  Optional\[[str]\] = None, \*\*kw) → [None]

      This method is proxied on the **[Operations]** class, via the **[Operations.create_check_constraint()]** method.

----

[alembic.operations.base.BatchOperations]: ../en/../ops.html#alembic.operations.BatchOperations
[str]: https://docs.python.org/3/library/stdtypes.html#str
[None]: https://docs.python.org/3/library/constants.html#None
[bool]: https://docs.python.org/3/library/functions.html#bool
[BatchOperations]: ../en/../ops.html#alembic.operations.BatchOperations
[BatchOperations.create_foreign_key()]: ../en/../ops.html#alembic.operations.BatchOperations.create_foreign_key
[Operations]: ../en/../ops.html#alembic.operations.Operations
[Operations.create_foreign_key()]: ../en/../ops.html#alembic.operations.Operations.create_foreign_key

* *class* alembic.operations.ops.**CreateForeignKeyOp**(*constraint_name*:  Optional\[[str]\], *source_table*:  [str], *referent_table*:  [str], *local_cols*:  List\[[str]\], *remote_cols*:  List\[[str]\], \*\*kw)

    Represent a create foreign key constraint operation.

  * *class* **batch_create_foreign_key**(*operations*:  [alembic.operations.base.BatchOperations], *constraint_name*:  [str], *referent_table*:  [str], *local_cols*:  List\[[str]\], *remote_cols*:  List\[[str]\], *referent_schema*:  Optional\[[str]\] = None, *onupdate*:  [None] = [None], *ondelete*:  [None] = [None], *deferrable*:  [None] = [None], *initially*:  [None] = [None], *match*:  [None] = [None],\*\*dialect_kw) → None Optional\[Table\]

    This method is proxied on the **[BatchOperations]** class, via the **[BatchOperations.create_foreign_key()]** method.

  * *class* **create_foreign_key**(*operations*:  Operations, *constraint_name*:  Optional\[[str]\],*source_table*:  [str], *referent_table*:  [str],*local_cols*:  List\[[str]\], *remote_cols*:  List\[[str]\],*onupdate*:  Optional\[[str]\] = None,*ondelete*:  Optional\[[str]\] = None,*deferrable*:  Optional\[[bool]\] = None,*initially*:  Optional\[[str]\] = None,*match*:  Optional\[[str]\] = None,*source_schema*:  Optional\[[str]\] = None, *referent_schema*:  Optional\[[str]\] = None, \*\*dialect_kw) → None Optional\[Table\]

    This method is proxied on the **[Operations]** class, via the **[Operations.create_foreign_key()]** method.

----

[str]: https://docs.python.org/3/library/stdtypes.html#str
[alembic.operations.base.Operations]: ../en/../ops.html#alembic.operations.Operations
[bool]: https://docs.python.org/3/library/functions.html#bool
[BatchOperations]: ../en/../ops.html#alembic.operations.BatchOperations
[BatchOperations.create_index()]: ../en/../ops.html#alembic.operations.BatchOperations.create_index
[Operations]: ../en/../ops.html#alembic.operations.Operations
[Operations.create_index()]: ../en/../ops.html#alembic.operations.Operations.create_index

* *class* alembic.operations.ops.**CreateIndexOp batch_create_index create_index**(*index_name*:  [str], *table_name*:  [str], *columns*:  Sequence\[Union\[[str], TextClause, ColumnElement\[Any\]\]\], *schema*:  Optional\[[str]\] = None, *unique*:  [bool] = False, \*\*kw)
    Represent a create index operation.

  * *classmethod* **CreateIndexOp**(kw, *operations*:  BatchOperations, *index_name*:  [str], *columns*:  List\[[str]\], \*\*kw, ) → Optional\[Table\]

    This method is proxied on the **[BatchOperations]** class, via the **[BatchOperations.create_index()]** method.
  
  * *classmethod* **create_index**(*operations*:  [alembic.operations.base.Operations], *index_name*:  [str], *table_name*:  [str], *columns*:  Sequence\[Union\[[str], TextClause, Function\]\], *schema*:  Optional\[[str]\] = None, *unique*:  [bool] = False, \*\*kw) → Optional\[Table\]

    This method is proxied on the **[Operations]** class, via the **[Operations.create_index()]** method.

----

[alembic.operations.base.BatchOperations]: ../en/../ops.html#alembic.operations.BatchOperations
[str]: https://docs.python.org/3/library/stdtypes.html#str
[BatchOperations]: ../en/../ops.html#alembic.operations.BatchOperations
[BatchOperations.create_primary_key()]: ../en/../ops.html#alembic.operations.BatchOperations.create_primary_key
[Operations]: ../en/../ops.html#alembic.operations.Operations
[Operations.create_primary_key()]: ../en/../ops.html#alembic.operations.Operations.create_primary_key

* *class* alembic.operations.ops.**CreatePrimaryKeyOp**(*constraint_name*:  Optional\[[str]\], *table_name*:  [str], *columns*:  Sequence\[[str]\], *schema*:  Optional\[[str]\] = None, \*\*kw)

    Represent a create primary key operation.

  * *classmethod* **batch_create_primary_key**(*operations*:  [alembic.operations.base.BatchOperations], *constraint_name*:  [str],*columns*:  List\[[str]\],) → None

    This method is proxied on the **[BatchOperations]** class, via the **[BatchOperations.create_primary_key()]** method.

  * *classmethod* **create_primary_key**(*operations*:  Operations,*constraint_name*:  Optional\[[str]\], *table_name*:  [str],*columns*:  List\[[str]\],*schema*:  Optional\[[str]\] = None) → Optional\[Table\]

    This method is proxied on the **[Operations]** class, via the **[Operations.create_primary_key()]** method.

----

[str]: https://docs.python.org/3/library/stdtypes.html#str
[None]: https://docs.python.org/3/library/constants.html#None
[BatchOperations]: ../en/../ops.html#alembic.operations.BatchOperations
[BatchOperations.create_table_comment()]: ../en/../ops.html#alembic.operations.BatchOperations.create_table_comment
[Operations]: ../en/../ops.html#alembic.operations.Operations
[Operations.create_table_comment()]: ../en/../ops.html#alembic.operations.Operations.create_table_comment

* *class* alembic.operations.ops.**CreateTableCommentOp**(*table_name*:  [str], *comment*:  Optional\[[str]\], *schema*:  Optional\[[str]\] = None, *existing_comment*:  Optional\[[str]\] = None, operations, comment, existing_comment=None)

    Represent a COMMENT ON table operation.

  * *classmethod*  **batch_create_table_comment**(operations, comment, existing_comment=None)

    This method is proxied on the **[BatchOperations]** class, via the **[BatchOperations.create_table_comment()]** method.

  * *classmethod*  **create_table_comment**(*operations*:  Operations, *table_name*:  [str],*comment*:  Optional\[[str]\],*existing_comment*:  [None] = [None], *schema*:  Optional\[[str]\] = None) → Optional\[Table\]

    This method is proxied on the **[Operations]** class, via the **[Operations.create_table_comment()]** method.

  * **reverse**()

    Reverses the COMMENT ON operation against a table.

----

[str]: https://docs.python.org/3/library/stdtypes.html#str
[Operations]: ../en/../ops.html#alembic.operations.Operations
[Operations.create_table()]: ../en/../ops.html#alembic.operations.Operations.create_table

* *class* alembic.operations.ops.**CreateTableOp**(*table_name*:  [str], *columns*:  Sequence\[Union\[Column, Constraint\]\], *schema*:  Optional\[[str]\] = None, *_namespace_metadata*:  Optional\[MetaData\] = None, *_constraints_included*:  [bool] = False, \*\*kw) <a name="CreateTableOp"></a>

    Represent a create table operation.

  * *classmethod*  **create_table**(*operations*:  Operations,*table_name*:  [str], *columns, \*\*kw) → Optional\[Table\]

    This method is proxied on the **[Operations]** class, via the **[Operations.create_table()]** method.

----

[alembic.operations.base.BatchOperations]: ../en/../ops.html#alembic.operations.BatchOperations
[str]: https://docs.python.org/3/library/stdtypes.html#str
[alembic.operations.base.Operations]: ../en/../ops.html#alembic.operations.Operations
[BatchOperations]: ../en/../ops.html#alembic.operations.BatchOperations
[BatchOperations.create_unique_constraint()]: ../en/../ops.html#alembic.operations.BatchOperations.create_unique_constraint
[Operations]: ../en/../ops.html#alembic.operations.Operations
[Operations.create_unique_constraint()]: ../en/../ops.html#alembic.operations.Operations.create_unique_constraint

* *class* alembic.operations.ops.**CreateUniqueConstraintOp**(*constraint_name*:  Optional\[[str]\], *table_name*:  [str], *columns*:  Sequence\[[str]\], *schema*:  Optional\[[str]\] = None, \*\*kw)

    Represent a create unique constraint operation.

  * *classmethod* **batch_create_unique_constraint**(*operations*:  [alembic.operations.base.BatchOperations], *constraint_name*:  [str],*columns*:  Sequence\[[str]\], \*\*kw) → Any

    This method is proxied on the **[BatchOperations]** class, via the **[BatchOperations.create_unique_constraint()]** method.

  * *classmethod* **create_unique_constraint**(*operations*:  [alembic.operations.base.Operations], *constraint_name*:  Optional\[[str]\], *table_name*:  [str], *columns*:  Sequence\[[str]\], *schema*:  Optional\[[str]\] = None,\*\*kw) → Any

    This method is proxied on the **[Operations]** class, via the **[Operations.create_unique_constraint()]** method.

----

[Customizing Revision Generation]: ../en/autogenerate.html#customizing-revision

* *class* alembic.operations.ops.**DowngradeOps**(*ops*:  Sequence\[[alembic.operations.ops.MigrateOperation]\] = (), *downgrade_token*:  [str] = 'downgrades')

    contains a sequence of operations that would apply to the ‘downgrade’ stream of a script.

    > **See also:** **[Customizing Revision Generation]**

----

[str]: https://docs.python.org/3/library/stdtypes.html#str
[BatchOperations]: ../en/../ops.html#alembic.operations.BatchOperations
[BatchOperations.drop_column()]: ../en/../ops.html#alembic.operations.BatchOperations.drop_column
[Operations]: ../en/../ops.html#alembic.operations.Operations
[Operations.drop_column()]: ../en/../ops.html#alembic.operations.Operations.drop_column

*class* alembic.operations.ops.**DropColumnOp batch_drop_column drop_column**(*table_name*:  [str], *column_name*:  [str], *schema*:  Optional\[[str]\] = None, *_reverse*:  Optional\[[alembic.operations.ops.AddColumnOp]\] = None, \*\*kw)

    Represent a drop column operation.

* *classmethod* **batch_drop_column**(*operations*:  BatchOperations, *column_name*:  [str], \*\*kw) → Optional\[Table\]

This method is proxied on the **[BatchOperations]** class, via the **[BatchOperations.drop_column()]** method.

* *classmethod* **drop_column**(*operations*:  Operations, *table_name*:  [str], *column_name*:  [str], *schema*:  Optional\[[str]\] = None, \*\*kw) → Optional\[Table\]

This method is proxied on the **[Operations]** class, via the **[Operations.drop_column()]** method.

----

[alembic.operations.base.BatchOperations]: ../en/../ops.html#alembic.operations.BatchOperations
[str]: https://docs.python.org/3/library/stdtypes.html#str
[BatchOperations]: ../en/../ops.html#alembic.operations.BatchOperations
[BatchOperations.drop_constraint()]: ../en/../ops.html#alembic.operations.BatchOperations.drop_constraint
[Operations]: ../en/../ops.html#alembic.operations.Operations
[Operations.drop_constraint()]: ../en/../ops.html#alembic.operations.Operations.drop_constraint

* *class* alembic.operations.ops.**DropConstraintOp**(*constraint_name*:  Optional\[[str]\], *table_name*:  [str], *type_*:  Optional\[[str]\] = None, *schema*:  Optional\[[str]\] = None, *_reverse*:  Optional\[[alembic.operations.ops.AddConstraintOp]\] = None)

    Represent a drop constraint operation.

  * *classmethod* **batch_drop_constraint drop_constraint**(*operations*:  [alembic.operations.base.BatchOperations], *constraint_name*:  [str], *type_*:  Optional\[[str]\] = None) → None

    This method is proxied on the **[BatchOperations]** class, via the **[BatchOperations.drop_constraint()]** method.

  * *classmethod* **batch_drop_constraint drop_constraint**(*operations*:  Operations, *constraint_name*:  [str], *table_name*:  [str], *type_*:  Optional\[[str]\] = None, *schema*:  Optional\[[str]\] = None) → Optional\[Table\]

    This method is proxied on the **[Operations]** class, via the **[Operations.drop_constraint()]** method.

----

[alembic.operations.base.BatchOperations]: ../en/../ops.html#alembic.operations.BatchOperations
[str]: https://docs.python.org/3/library/stdtypes.html#str
[BatchOperations]: ../en/../ops.html#alembic.operations.BatchOperations
[BatchOperations.drop_index()]: ../en/../ops.html#alembic.operations.BatchOperations.drop_index
[Operations]: ../en/../ops.html#alembic.operations.Operations
[Operations.drop_index()]: ../en/../ops.html#alembic.operations.Operations.drop_index

* *class* alembic.operations.ops.**DropIndexOp**(*index_name*:  Union\[quoted_name, [str], conv\], *table_name*:  Optional\[[str]\] = None, *schema*:  Optional\[[str]\] = None, *_reverse*:  Optional\[[CreateIndexOp]\] = None, \*\*kw) <a name="CreateIndexOp"></a>

    Represent a drop index operation.

  * *classmethod* **batch_drop_index**(*operations*:  [alembic.operations.base.BatchOperations], *index_name*:  [str], \*\*kw) → Optional\[Table\]

    This method is proxied on the **[BatchOperations]** class, via the **[BatchOperations.drop_index()]** method.

  * *classmethod* **drop_index**(*operations*:  Operations, *index_name*:  [str], *table_name*:  Optional\[[str]\] = None, *schema*:  Optional\[[str]\] = None,\*\*kw) → Optional\[Table\]

    This method is proxied on the **[Operations]** class, via the **[Operations.drop_index()]** method.

----

[str]: https://docs.python.org/3/library/stdtypes.html#str
[BatchOperations]: ../en/../ops.html#alembic.operations.BatchOperations
[BatchOperations.drop_table_comment()]: ../en/../ops.html#alembic.operations.BatchOperations.drop_table_comment
[Operations]: ../en/../ops.html#alembic.operations.Operations
[Operations.drop_table_comment()]: ../en/../ops.html#alembic.operations.Operations.drop_table_comment

* *class* alembic.operations.ops.**DropTableCommentOp batch_drop_table_comment drop_table_comment reverse**(*table_name*:  [str], *schema*:  Optional\[[str]\] = None, *existing_comment*:  Optional\[[str]\] = None)

    Represent an operation to remove the comment from a table.

  * *classmethod* **batch_drop_table_comment**(operations, existing_comment=None)

    This method is proxied on the **[BatchOperations]** class, via the **[BatchOperations]**.drop_table_comment() method.

  * *classmethod* **drop_table_comment**(*operations*:  Operations, *table_name*:  [str],*existing_comment*:  Optional\[[str]\] = None, *schema*:  Optional\[[str]\] = None) → Optional\[Table\]

    This method is proxied on the **[Operations]** class, via the **[Operations]**.drop_table_comment() method.

  * **reverse**()

    Reverses the COMMENT ON operation against a table.

----

[alembic.operations.base.Operations]: ../en/../ops.html#alembic.operations.Operations
[str]: https://docs.python.org/3/library/stdtypes.html#str
[Operations]: ../en/../ops.html#alembic.operations.Operations
[Operations.drop_table()]: ../en/../ops.html#alembic.operations.Operations.drop_table

* *class* alembic.operations.ops.**DropTableOp drop_table**(*table_name*:  [str], *schema*:  Optional\[[str]\] = None, *table_kw*:  Optional\[MutableMapping\[Any, Any\]\] = None, *_reverse*:  Optional\[[alembic.operations.ops.CreateTableOp]\] = None) → None

    Represent a drop table operation.

* *classmethod*  **drop_table**(*operations*:  [alembic.operations.base.Operations], *table_name*:  [str],*schema*:  Optional\[[str]\] = None, **kw: Any) → None

    This method is proxied on the **[Operations]** class, via the **[Operations.drop_table()]** method.

----

[alembic.operations.base.Operations]: ../en/../ops.html#alembic.operations.Operations
[str]: https://docs.python.org/3/library/stdtypes.html#str
[None]: https://docs.python.org/3/library/constants.html#None
[Operations]: ../en/../ops.html#alembic.operations.Operations
[Operations.execute()]: ../en/../ops.html#alembic.operations.Operations.execute

* *class* alembic.operations.ops.**ExecuteSQLOp execute**(*sqltext*:  Union\[Update, [str], Insert, TextClause\], *execution_options*:  [None] = [None])

    Represent an execute SQL operation.

  * **execute**(*operations*:  [alembic.operations.base.Operations], *sqltext*:  Union\[[str], TextClause, Update\], *execution_options*:  [None] = [None]) → Optional\[Table\]

    This method is proxied on the **[Operations]** class, via the **[Operations.execute()]** method.

----

[Built-in Operation Objects]: #operation-objects
[Operation Plugins]: #operation-plugins
[Customizing Revision Generation]: ../en/autogenerate.html#customizing-revision
[MigrateOperation]: #alembic.operations.ops.MigrateOperation

* *class* alembic.operations.ops.**MigrateOperation**

    base class for migration command and organization objects.

    This system is part of the operation extensibility API.

    > **See also:** **[Built-in Operation Objects]**
    >
    > * **[Operation Plugins]**
    >
    > * **[Customizing Revision Generation]**

  * **info**

    A dictionary that may be used to store arbitrary information along with this **[MigrateOperation]** object.

----

[MigrationScript]: #MigrationScript
[UpgradeOps]: #alembic.operations.ops.UpgradeOps
[DowngradeOps]: #alembic.operations.ops.DowngradeOps
[Customizing Revision Generation]: ../en/autogenerate.html#customizing-revision
[MigrationScript.downgrade_ops_list]: #alembic.operations.ops.MigrationScript.downgrade_ops_list
[MigrationScript.downgrade_ops]: #alembic.operations.ops.MigrationScript.downgrade_ops
[MigrationScript.upgrade_ops_list]: #alembic.operations.ops.MigrationScript.upgrade_ops_list
[MigrationScript.upgrade_ops]: #alembic.operations.ops.MigrationScript.upgrade_ops

* *class* alembic.operations.ops.**MigrationScript**(*rev_id*:  Optional\[[str]\], *upgrade_ops*:  [alembic.operations.ops.UpgradeOps], *downgrade_ops*:  [alembic.operations.ops.DowngradeOps], *message*:  Optional\[[str]\] = None, *imports*:  Set\[[str]\] = {}, *head*:  Optional\[[str]\] = None, *splice*:  Optional\[[bool]\] = None, *branch_label*:  Optional\[[str]\] = None, *version_path*:  Optional\[[str]\] = None, *depends_on*:  Optional\[Union\[[str], Sequence\[[str]\]\]\] = None) <a name="MigrationScript"></a>

    represents a migration script.

    E.g. when autogenerate encounters this object, this corresponds to the production of an actual script file.

    A normal **[MigrationScript]** object would contain a single **[UpgradeOps]** and a single **[DowngradeOps]** directive. These are accessible via the `.upgrade_ops` and `.downgrade_ops` attributes.

    In the case of an autogenerate operation that runs multiple times, such as the multiple database example in the “multidb” template, the `.upgrade_ops` and `.downgrade_ops` attributes are disabled, and instead these objects should be accessed via the `.upgrade_ops_list` and `.downgrade_ops_list` list-based attributes. These latter attributes are always available at the very least as single-element lists.

    > **See also:** **[Customizing Revision Generation]**

  * *property* **downgrade_ops**

    An instance of **[DowngradeOps]**.

    > **See also:** **[MigrationScript.downgrade_ops_list]**

  * *property* **downgrade_ops_list:** List\[[alembic.operations.ops.DowngradeOps]\]
  
    A list of **[DowngradeOps]** instances.

    This is used in place of the **[MigrationScript.downgrade_ops]** attribute when dealing with a revision operation that does multiple autogenerate passes.

  * *property* **upgrade_ops**

    An instance of **[UpgradeOps]**.

    > **See also:** **[MigrationScript.upgrade_ops_list]**

  * *property* **upgrade_ops_list**

    A list of **[UpgradeOps]** instances.

    This is used in place of the **[MigrationScript.upgrade_ops]** attribute when dealing with a revision operation that does multiple autogenerate passes.

----

* *class* alembic.operations.ops.**ModifyTableOps**(*table_name*:  [str], *ops*:  Sequence\[[alembic.operations.ops.MigrateOperation]\], *schema*:  Optional\[[str]\] = None) <a name="ModifyTableOps"></a>

    Contains a sequence of operations that all apply to a single Table.

----

* *class* alembic.operations.ops.**OpContainer**(*ops*:  Sequence\[[alembic.operations.ops.MigrateOperation]\] = ())

    Represent a sequence of operations operation.

----

[str]: https://docs.python.org/3/library/stdtypes.html#str
[Operations]: ../en/../ops.html#alembic.operations.Operations
[Operations.rename_table()]: ../en/../ops.html#alembic.operations.Operations.rename_table

* *class* alembic.operations.ops.**RenameTableOp rename_table**(*old_table_name*:  [str], *new_table_name*:  [str], *schema*:  Optional\[[str]\] = None)

    Represent a rename table operation.

  * **rename_table**(*operations*:  Operations, *old_table_name*:  [str], *new_table_name*:  [str], *schema*:  Optional\[[str]\] = None) → Optional\[Table\]

    This method is proxied on the **[Operations]** class, via the **[Operations]**.rename_table() method.

----

[Customizing Revision Generation]: ../en/autogenerate.html#customizing-revision

* *class* alembic.operations.ops.**UpgradeOps**(*ops*:  Sequence\[[alembic.operations.ops.MigrateOperation]\] = (), *upgrade_token*:  [str] = 'upgrades') <a name="UpgradeOps"></a>

    contains a sequence of operations that would apply to the ‘upgrade’ stream of a script.

    > **See also:** **[Customizing Revision Generation]**
