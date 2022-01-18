[sqlalchemy.schema.DDLElement]: https://docs.sqlalchemy.org/en/14/core/ddl.html#sqlalchemy.schema.DDLElement
[Custom SQL Constructs and Compilation Extension]: https://docs.sqlalchemy.org/en/14/core/compiler.html#sqlalchemy-ext-compiler-toplevel
[Operation Directives]: operations.html#alembic-operations-toplevel
[str]: https://docs.python.org/3/library/stdtypes.html#str
[sqlalchemy.sql.schema.Column]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column
[sqlalchemy.sql.elements.quoted_name]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name
[bool]: https://docs.python.org/3/library/functions.html#bool
[AddColumn]: #alembic.ddl.base.AddColumn
[ColumnDefault]: #alembic.ddl.base.ColumnDefault
[ColumnName]: #alembic.ddl.base.ColumnName
[ColumnNullable]: #alembic.ddl.base.ColumnNullable
[ColumnType]: #alembic.ddl.base.ColumnType
[ComputedColumnDefault]: #alembic.ddl.base.ComputedColumnDefault
[DropColumn]: #alembic.ddl.base.DropColumn
[IdentityColumnDefault]: #alembic.ddl.base.IdentityColumnDefault
[RenameTable]: #alembic.ddl.base.RenameTable
[None]: https://docs.python.org/3/library/constants.html#None
[dict]: https://docs.python.org/3/library/stdtypes.html#dict
[EnvironmentContext.begin_transaction()]: runtime.html#alembic.runtime.environment.EnvironmentContext.begin_transaction
[EnvironmentContext.run_migrations()]: runtime.html#alembic.runtime.environment.EnvironmentContext.run_migrations
[alembic.ddl.impl.DefaultImpl]: #alembic.ddl.impl.DefaultImpl
[alembic.ddl.mysql.MySQLImpl]: #alembic.ddl.mysql.MySQLImpl
[alembic.ddl.base.AlterColumn]: #alembic.ddl.base.AlterColumn
[alembic.ddl.mysql.MySQLChangeColumn]: #alembic.ddl.mysql.MySQLChangeColumn
[alembic.operations.ops.AddConstraintOp]: operations.html#alembic.operations.ops.AddConstraintOp
[BatchOperations]: ../ops.html#alembic.operations.BatchOperations
[BatchOperations.create_exclude_constraint()]: ../ops.html#alembic.operations.BatchOperations.create_exclude_constraint
[Operations]: ../ops.html#alembic.operations.Operations
[Operations.create_exclude_constraint()]: ../ops.html#alembic.operations.Operations.create_exclude_constraint
[sqlalchemy.dialects.postgresql.ext.ExcludeConstraint]: https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ExcludeConstraint
[alembic.ddl.postgresql.CreateExcludeConstraintOp]: #alembic.ddl.postgresql.CreateExcludeConstraintOp
[alembic.ddl.postgresql.PostgresqlColumnType]: #alembic.ddl.postgresql.PostgresqlColumnType
[alembic.ddl.base.RenameTable]: #alembic.ddl.base.RenameTable
[http://bugs.python.org/issue10740]: http://bugs.python.org/issue10740

# DDL Internals

These are some of the constructs used to generate migrationinstructions.  The APIs here build off of the   **[sqlalchemy.schema.DDLElement]**  and   **[Custom SQL Constructs and Compilation Extension]**   systems.

For programmatic usage of Alembicâs migration directives, the easiestroute is to use the higher level functions given by   **[Operation Directives]**  .

* *class* alembic.ddl.base. **AddColumn** (*name:* ***[str]***, *column:* ***[sqlalchemy.sql.schema.Column]***, *schema:* *Optional\[Union\[**[sqlalchemy.sql.elements.quoted_name]**, **[str]**\]\] = None*)

* *class* alembic.ddl.base. **AlterColumn** (*name:* ***[str]***, *column_name:* ***[str]***, *schema:* *Optional\[**[str]**\] = None*, *existing_type:* *Optional\[TypeEngine\] = None*, *existing_nullable:* *Optional\[**[bool]**\] = None*, *existing_server_default:* *Optional\[Union\[TextClause, FetchedValue, Function, **[str]**\]\] = None*, *existing_comment:* *Optional\[**[str]**\] = None*)

* *class* alembic.ddl.base. **AlterTable** (*table_name:* ***[str]***, *schema:* *Optional\[Union\[**[sqlalchemy.sql.elements.quoted_name]**, **[str]**\]\] = None*)

    Represent an ALTER TABLE statement.

    Only the string name and optional schema name of the tableis required, not a full Table object.

* *class* alembic.ddl.base. **ColumnComment** (*name:* ***[str]***, *column_name:* ***[str]***, *comment:* *Optional\[**[str]**\]*, \*\*kw)

* *class* alembic.ddl.base. **ColumnDefault** (*name:* ***[str]***, *column_name:* ***[str]***, *default:* *Optional\[Union\[TextClause, FetchedValue, Function, **[str]**\]\]*, \*\*kw)

* *class* alembic.ddl.base. **ColumnName** (*name:* ***[str]***, *column_name:* ***[str]***, *newname:* ***[str]***, \*\*kw)

* *class* alembic.ddl.base. **ColumnNullable** (*name:* ***[str]***, *column_name:* ***[str]***, *nullable:* ***[bool]***, \*\*kw)

* *class* alembic.ddl.base. **ColumnType** (*name:* ***[str]***, *column_name:* ***[str]***, *type_:* *TypeEngine*, \*\*kw)

* *class* alembic.ddl.base. **ComputedColumnDefault** (*name:* ***[str]***, *column_name:* ***[str]***, *default:* *Optional\[Computed\]*, \*\*kw)

* *class* alembic.ddl.base. **DropColumn** (*name:* ***[str]***, *column:* ***[sqlalchemy.sql.schema.Column]***, *schema:* *Optional\[**[str]**\] = None*)

* *class* alembic.ddl.base. **IdentityColumnDefault** (*name:* ***[str]***, *column_name:* ***[str]***, *default:* *Optional\[Identity\]*, *impl:* *DefaultImpl*, \*\*kw)

* *class* alembic.ddl.base. **RenameTable** (*old_table_name:* ***[str]***, *new_table_name:* *Union\[**[sqlalchemy.sql.elements.quoted_name]**, **[str]**\]*, *schema:* *Optional\[Union\[**[sqlalchemy.sql.elements.quoted_name]**, **[str]**\]\] = None*)

* alembic.ddl.base. **add_column** (*compiler:* *DDLCompiler*, *column:* *Column*, \*\*kw) → **[str]**

* alembic.ddl.base. **alter_column** (*compiler:* *DDLCompiler*, *name:* ***[str]***) → **[str]**

* alembic.ddl.base. **alter_table** (*compiler:* *DDLCompiler*, *name:* ***[str]***, *schema:* *Optional\[**[str]**\]*) → **[str]**

* alembic.ddl.base. **drop_column** (*compiler:* *DDLCompiler*, *name:* ***[str]***, \*\*kw) → **[str]**

* alembic.ddl.base. **format_column_name** (*compiler:* *DDLCompiler*, *name:* *Optional\[Union\[quoted_name, **[str]**\]\]*) → Union\[quoted_name, **[str]**\]

* alembic.ddl.base. **format_server_default** (*compiler:* *DDLCompiler*, *default:* *Optional\[Union\[TextClause, FetchedValue, Function, **[str]**\]\]*) → **[str]**

* alembic.ddl.base. **format_table_name** (*compiler:* *Compiled*, *name:* *Union\[quoted_name, **[str]**\]*, *schema:* *Optional\[Union\[quoted_name, **[str]**\]\]*) → Union\[quoted_name, **[str]**\]

* alembic.ddl.base. **format_type** (*compiler:* *DDLCompiler*, *type_:* *TypeEngine*) → **[str]**

* alembic.ddl.base. **quote_dotted** (*name:* *Union\[**[sqlalchemy.sql.elements.quoted_name]**, **[str]**\]*, *quote:* *functools.partial*) → Union\[**[sqlalchemy.sql.elements.quoted_name]**, **[str]**\]

    quote the elements of a dotted name

* alembic.ddl.base. **visit_add_column** (*element:* ***[AddColumn]***, *compiler:* *DDLCompiler*, \*\*kw) → **[str]**

* alembic.ddl.base. **visit_column_default** (*element:* ***[ColumnDefault]***, *compiler:* *DDLCompiler*, \*\*kw) → **[str]**

* alembic.ddl.base. **visit_column_name** (*element:* ***[ColumnName]***, *compiler:* *DDLCompiler*, \*\*kw) → **[str]**

* alembic.ddl.base. **visit_column_nullable** (*element:* ***[ColumnNullable]***, *compiler:* *DDLCompiler*, \*\*kw) → **[str]**

* alembic.ddl.base. **visit_column_type** (*element:* ***[ColumnType]***, *compiler:* *DDLCompiler*, \*\*kw) → **[str]**

* alembic.ddl.base. **visit_computed_column** (*element:* ***[ComputedColumnDefault]***, *compiler:* *DDLCompiler*, \*\*kw)

* alembic.ddl.base. **visit_drop_column** (*element:* ***[DropColumn]***, *compiler:* *DDLCompiler*, \*\*kw) → **[str]**

* alembic.ddl.base. **visit_identity_column** (*element:* ***[IdentityColumnDefault]***, *compiler:* *DDLCompiler*, \*\*kw)

* alembic.ddl.base. **visit_rename_table** (*element:* ***[RenameTable]***, *compiler:* *DDLCompiler*, \*\*kw) → **[str]**

* *class* alembic.ddl.impl. **DefaultImpl** (*dialect:* *Dialect*, *connection:* *Optional\[Connection\]*, *as_sql:* ***[bool]***, *transactional_ddl:* *Optional\[**[bool]**\]*, *output_buffer:* *Optional\[StringIO\]*, *context_opts:* *Dict\[**[str]**, Any\]*)

    Provide the entrypoint for major migration operations,including database-specific behavioral variances.

    While individual SQL/DDL constructs already providefor database-specific implementations, variances hereallow for entirely different sequences of operationsto take place for a particular migration, such asSQL Serverâs special âIDENTITY INSERTâ step forbulk inserts.

  * **add_column** (*table_name:* ***[str]***, *column:* *Column*, *schema:* *Optional\[Union\[quoted_name, **[str]**\]\] = None*) → **[None]**

  * **add_constraint** (*const:* *Any*) → **[None]**

  * **alter_column** (*table_name:* ***[str]***, *column_name:* ***[str]***, *nullable:* *Optional\[**[bool]**\] = None*, *server_default:* *Union\[_ServerDefault, Literal\[False\]\] = False*, *name:* *Optional\[**[str]**\] = None*, *type_:* *Optional\[TypeEngine\] = None*, *schema:* *Optional\[**[str]**\] = None*, *autoincrement:* *Optional\[**[bool]**\] = None*, *comment:* *Optional\[Union\[**[str]**, Literal\[False\]\]\] = False*, *existing_comment:* *Optional\[**[str]**\] = None*, *existing_type:* *Optional\[TypeEngine\] = None*, *existing_server_default:* *Optional\[_ServerDefault\] = None*, *existing_nullable:* *Optional\[**[bool]**\] = None*, *existing_autoincrement:* *Optional\[**[bool]**\] = None*, *\*\*kw:* *Any*) → **[None]**

  * **autogen_column_reflect** (inspector, table, column_info)

    A hook that is attached to the âcolumn_reflectâ event for whena Table is reflected from the database during the autogenerateprocess.

    Dialects can elect to modify the information gathered here.

  * *property*  **bind**  *: Optional\[Connection\]*

  * **bulk_insert** (*table:* *Union\[TableClause, Table\]*, *rows:* *List\[**[dict]**\]*, *multiinsert:* ***[bool]** = True*) → **[None]**

  * **cast_for_batch_migrate** (existing, existing_transfer, new_type)

  * **command_terminator**  *= ';'*

  * **compare_server_default** (inspector_column, metadata_column, rendered_metadata_default, rendered_inspector_default)

  * **compare_type** (*inspector_column:* *Column*, *metadata_column:* *Column*) → **[bool]**

    Returns True if there ARE differences between the types of the twocolumns. Takes impl.type_synonyms into account between retrospectedand metadata types

  * **correct_for_autogen_constraints** (*conn_uniques:* *Set\[UniqueConstraint\]*, *conn_indexes:* *Set\[Index\]*, *metadata_unique_constraints:* *Set\[UniqueConstraint\]*, *metadata_indexes:* *Set\[Index\]*) → **[None]**

  * **correct_for_autogen_foreignkeys** (*conn_fks:* *Set\[ForeignKeyConstraint\]*, *metadata_fks:* *Set\[ForeignKeyConstraint\]*) → **[None]**

  * **create_column_comment** (*column:* *ColumnElement*) → **[None]**

  * **create_index** (*index:* *Index*) → **[None]**

  * **create_table** (*table:* *Table*) → **[None]**

  * **create_table_comment** (*table:* *Table*) → **[None]**

  * **drop_column** (*table_name:* ***[str]***, *column:* *Column*, *schema:* *Optional\[**[str]**\] = None*, \*\*kw) → **[None]**

  * **drop_constraint** (*const:* *Constraint*) → **[None]**

  * **drop_index** (*index:* *Index*) → **[None]**

  * **drop_table** (*table:* *Table*) → **[None]**

  * **drop_table_comment** (*table:* *Table*) → **[None]**

  * **emit_begin** () → **[None]**

    Emit the string   `BEGIN`  , or the backend-specificequivalent, on the current connection context.

    This is used in offline mode and typicallyvia   **[EnvironmentContext.begin_transaction()]**  .

  * **emit_commit** () → **[None]**

    Emit the string   `COMMIT`  , or the backend-specificequivalent, on the current connection context.

    This is used in offline mode and typicallyvia   **[EnvironmentContext.begin_transaction()]**  .

  * **execute** (*sql:* *Union\[Update, TextClause, **[str]**\]*, *execution_options:* ***[None]** = **[None]***) → **[None]**

  * *classmethod*  **get_by_dialect** (*dialect:* *Dialect*) → Any

  * **identity_attrs_ignore**  *: Tuple\[**[str]**, ...\]*  *= ('on_null',)*

  * **prep_table_for_batch** (*batch_impl:* *ApplyBatchImpl*, *table:* *Table*) → **[None]**

    perform any operations needed on a table before a newone is created to replace it in batch mode.

    the PG dialect uses this to drop constraints on the tablebefore the new one uses those same names.

  * **rename_table** (*old_table_name:* ***[str]***, *new_table_name:* *Union\[**[str]**, quoted_name\]*, *schema:* *Optional\[Union\[quoted_name, **[str]**\]\] = None*) → **[None]**

  * **render_ddl_sql_expr** (*expr:* *ClauseElement*, *is_server_default:* ***[bool]** = False*, \*\*kw) → **[str]**

    Render a SQL expression that is typically a server default,index expression, etc.

    > *New in version 1.0.11.*
  * **render_type** (*type_obj:* *TypeEngine*, *autogen_context:* *AutogenContext*) → Union\[**[str]**, Literal\[False\]\]

  * **requires_recreate_in_batch** (*batch_op:* *BatchOperationsImpl*) → **[bool]**

    Return True if the given   `BatchOperationsImpl`  would need the table to be recreated and copied in order toproceed.

    Normally, only returns True on SQLite when operations otherthan add_column are present.

  * **start_migrations** () → **[None]**

    A hook called when   **[EnvironmentContext.run_migrations()]**  is called.

    Implementations can set up per-migration-run state here.

  * **static_output** (*text:* ***[str]***) → **[None]**

  * **transactional_ddl**  *= False*

  * **type_arg_extract**  *: Sequence\[**[str]**\]*  *= ()*

  * **type_synonyms**  *: Tuple\[Set\[**[str]**\], ...\]*  *= ({'DECIMAL', 'NUMERIC'},)*

* *class* alembic.ddl.impl. **ImplMeta** (*classname:* ***[str]***, *bases:* *Tuple\[Type\[**[alembic.ddl.impl.DefaultImpl]**\]\]*, *dict_:* *Dict\[**[str]**, Any\]*)
* *class* alembic.ddl.impl. **Params** (token0, tokens, args, kwargs)

    Create new instance of Params(token0, tokens, args, kwargs)

  * *property*  **args**

    Alias for field number 2

  * *property*  **kwargs**

    Alias for field number 3

  * *property*  **token0**

    Alias for field number 0

  * *property*  **tokens**

    Alias for field number 1
