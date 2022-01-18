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

## Postgresql

* *class* alembic.ddl.postgresql. **CreateExcludeConstraintOp** (*constraint_name:* *Optional\[**[str]**\]*, *table_name:* *Union\[**[str]**, quoted_name\]*, *elements:* *Union\[Sequence\[Tuple\[**[str]**, **[str]**\]\], Sequence\[Tuple\[ColumnClause, **[str]**\]\]\]*, *where:* *Optional\[Union\[BinaryExpression, **[str]**\]\] = None*, *schema:* *Optional\[**[str]**\] = None*, *_orig_constraint:* *Optional\[ExcludeConstraint\] = None*, \*\*kw)

    Bases:   **[alembic.operations.ops.AddConstraintOp]**

    Represent a create exclude constraint operation.

  * *classmethod*  **batch_create_exclude_constraint** (operations, constraint_name, \*elements, \*\*kw)

    This method is proxied on the   **[BatchOperations]**   class, via the   **[BatchOperations.create_exclude_constraint()]**   method.

  * **constraint_type**  *= 'exclude'*

  * *classmethod*  **create_exclude_constraint** (*operations:* *Operations*, *constraint_name:* ***[str]***, *table_name:* ***[str]***, *\*elements:* *Any*, *\*\*kw:* *Any*) → Optional\[Table\]

    This method is proxied on the   **[Operations]**   class, via the   **[Operations.create_exclude_constraint()]**   method.

  * *classmethod*  **from_constraint** (*constraint:* ***[sqlalchemy.dialects.postgresql.ext.ExcludeConstraint]***) → **[alembic.ddl.postgresql.CreateExcludeConstraintOp]**

  * **to_constraint** (*migration_context:* *Optional\[MigrationContext\] = None*) → ExcludeConstraint

* *class* alembic.ddl.postgresql. **PostgresqlColumnType** (*name:* ***[str]***, *column_name:* ***[str]***, *type_:* *TypeEngine*, \*\*kw)

    Bases:   **[alembic.ddl.base.AlterColumn]**

  * *class* alembic.ddl.postgresql. **PostgresqlImpl** (*dialect:* *Dialect*, *connection:* *Optional\[Connection\]*, *as_sql:* ***[bool]***, *transactional_ddl:* *Optional\[**[bool]**\]*, *output_buffer:* *Optional\[StringIO\]*, *context_opts:* *Dict\[**[str]**, Any\]*)

    Bases:   **[alembic.ddl.impl.DefaultImpl]**

  * **alter_column** (*table_name:* ***[str]***, *column_name:* ***[str]***, *nullable:* *Optional\[**[bool]**\] = None*, *server_default:* *Union\[_ServerDefault, Literal\[False\]\] = False*, *name:* *Optional\[**[str]**\] = None*, *type_:* *Optional\[TypeEngine\] = None*, *schema:* *Optional\[**[str]**\] = None*, *autoincrement:* *Optional\[**[bool]**\] = None*, *existing_type:* *Optional\[TypeEngine\] = None*, *existing_server_default:* *Optional\[_ServerDefault\] = None*, *existing_nullable:* *Optional\[**[bool]**\] = None*, *existing_autoincrement:* *Optional\[**[bool]**\] = None*, *\*\*kw:* *Any*) → **[None]**

  * **autogen_column_reflect** (inspector, table, column_info)

    A hook that is attached to the âcolumn_reflectâ event for whena Table is reflected from the database during the autogenerateprocess.

    Dialects can elect to modify the information gathered here.

  * **compare_server_default** (inspector_column, metadata_column, rendered_metadata_default, rendered_inspector_default)

  * **correct_for_autogen_constraints** (conn_unique_constraints, conn_indexes, metadata_unique_constraints, metadata_indexes)

  * **create_index** (index)

  * **identity_attrs_ignore**  *: Tuple\[**[str]**, ...\]*  *= ('on_null', 'order')*

  * **memo**  *: **[dict]***

  * **prep_table_for_batch** (batch_impl, table)

    perform any operations needed on a table before a newone is created to replace it in batch mode.

    the PG dialect uses this to drop constraints on the tablebefore the new one uses those same names.

  * **render_type** (*type_:* *TypeEngine*, *autogen_context:* *AutogenContext*) → Union\[**[str]**, Literal\[False\]\]

  * **transactional_ddl**  *= True*

  * **type_synonyms**  *: Tuple\[Set\[**[str]**\], ...\]*  *= ({'DECIMAL', 'NUMERIC'}, {'DOUBLE PRECISION', 'FLOAT'})*

* alembic.ddl.postgresql. **visit_column_comment** (*element:* *ColumnComment*, *compiler:* *PGDDLCompiler*, \*\*kw) → **[str]**

* alembic.ddl.postgresql. **visit_column_type** (*element:* ***[alembic.ddl.postgresql.PostgresqlColumnType]***, *compiler:* *PGDDLCompiler*, \*\*kw) → **[str]**

* alembic.ddl.postgresql. **visit_identity_column** (*element:* *IdentityColumnDefault*, *compiler:* *PGDDLCompiler*, \*\*kw)

* alembic.ddl.postgresql. **visit_rename_table** (*element:* ***[alembic.ddl.base.RenameTable]***, *compiler:* *PGDDLCompiler*, \*\*kw) → **[str]**
