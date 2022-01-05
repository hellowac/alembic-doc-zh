# alter_column

**alter_column**(*table_name*:  [str], *column_name*:  [str], *nullable*:  Optional\[[bool]\] = None, *comment*:  Optional\[Union\[[str], [bool]\]\] = False, *server_default*:  Any = False, *new_column_name*:  Optional\[[str]\] = None, *type_*:  Optional\[Union\[TypeEngine, Type\[TypeEngine\]\]\] = None, *existing_type*:  Optional\[Union\[TypeEngine, Type\[TypeEngine\]\]\] = None, *existing_server_default*:  Optional\[Union\[[str], [bool], Identity, Computed\]\] = False, *existing_nullable*:  Optional\[[bool]\] = None, *existing_comment*:  Optional\[[str]\] = None, *schema*:  Optional\[[str]\] = None, **kw) → Optional\[Table\]

[str]: https://docs.python.org/3/library/stdtypes.html#str
[bool]: https://docs.python.org/3/library/functions.html#bool
[Boolean]: https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Boolean
[Enum]: https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Enum
[text()]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.text
[DefaultClause]: https://docs.sqlalchemy.org/en/14/core/defaults.html#sqlalchemy.schema.DefaultClause
[TypeEngine]: https://docs.sqlalchemy.org/en/14/core/type_api.html#sqlalchemy.types.TypeEngine
[quoted_name]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name

Issue an “alter column” instruction using the current migration context.

Generally, only that aspect of the column which is being changed, i.e. name, type, nullability, default, needs to be specified. Multiple changes can also be specified at once and the backend should “do the right thing”, emitting each change either separately or together as the backend allows.

MySQL has special requirements here, since MySQL cannot ALTER a column without a full specification. When producing MySQL-compatible migration files, it is recommended that the `existing_type`, `existing_server_default`, and `existing_nullable` parameters be present, if not being altered.

Type changes which are against the SQLAlchemy “schema” types **[Boolean]** and **[Enum]** may also add or drop constraints which accompany those types on backends that don’t support them natively. The `existing_type` argument is used in this case to identify and remove a previous constraint that was bound to the type object.

**Parameters:**

* ***table_name*** – string name of the target table.
* ***column_name*** – string name of the target column, as it exists before the operation begins.
* ***nullable*** – Optional; specify `True` or `False` to alter the column’s nullability.
* ***server_default*** – Optional; specify a string SQL expression, **[text()]**, or **[DefaultClause]** to indicate an alteration to the column’s default value. Set to `None` to have the default removed.
* ***comment***<a name="params.comment"></a> – optional string text of a new comment to add to the column.
  * *New in version 1.0.6.*
* ***new_column_name*** – Optional; specify a string name here to indicate the new name within a column rename operation.
* ***type_*** – Optional; a **[TypeEngine]** type object to specify a change to the column’s type. For SQLAlchemy types that also indicate a constraint (i.e. **[Boolean]**, Enum), the constraint is also generated.
* ***autoincrement*** – set the `AUTO_INCREMENT` flag of the column; currently understood by the MySQL dialect.
* ***existing_type*** – Optional; a **[TypeEngine]** type object to specify the previous type. This is required for all MySQL column alter operations that don’t otherwise specify a new type, as well as for when nullability is being changed on a SQL Server column. It is also used if the type is a so-called SQLlchemy “schema” type which may define a constraint (i.e. **[Boolean]**, Enum), so that the constraint can be dropped.
* ***existing_server_default*** – Optional; The existing default value of the column. Required on MySQL if an existing default is not being changed; else MySQL removes the default.
* ***existing_nullable*** – Optional; the existing nullability of the column. Required on MySQL if the existing nullability is not being changed; else MySQL sets this to NULL.
* ***existing_autoincrement*** – Optional; the existing autoincrement of the column. Used for MySQL’s system of altering a column that specifies `AUTO_INCREMENT`.
* ***existing_comment*** – string text of the existing comment on the column to be maintained. Required on MySQL if the existing comment on the column is not being changed.
  * *New in version 1.0.6.*
* ***schema*** – Optional **schema** name to operate within. To control quoting of the **schema** outside of the default behavior, use the SQLAlchemy construct **[quoted_name]**.
* ***postgresql_using*** – String argument which will indicate a SQL expression to render within the Postgresql-specific USING clause within ALTER COLUMN. This string is taken directly as raw SQL which must explicitly include any necessary quoting or escaping of tokens within the expression.
