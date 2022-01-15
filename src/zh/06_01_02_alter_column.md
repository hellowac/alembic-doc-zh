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

> 使用当前迁移上下文发出“alter column”指令。

Generally, only that aspect of the column which is being changed, i.e. name, type, nullability, default, needs to be specified. Multiple changes can also be specified at once and the backend should “do the right thing”, emitting each change either separately or together as the backend allows.

> 通常，只需要指定正在更改的列的某些方面，即名称、类型、可空性、默认值。 也可以一次指定多个更改，并且后端应该“做正确的事情”，在后端允许的情况下单独或一起发出每个更改。

MySQL has special requirements here, since MySQL cannot ALTER a column without a full specification. When producing MySQL-compatible migration files, it is recommended that the `existing_type`, `existing_server_default`, and `existing_nullable` parameters be present, if not being altered.

> MySQL 在这里有特殊要求，因为 MySQL 不能在没有完整规范的情况下 ALTER 列。 在生成与 MySQL 兼容的迁移文件时，如果未更改，建议提供 `existing_type`、`existing_server_default` 和 `existing_nullable` 参数。

Type changes which are against the SQLAlchemy “schema” types **[Boolean]** and **[Enum]** may also add or drop constraints which accompany those types on backends that don’t support them natively. The `existing_type` argument is used in this case to identify and remove a previous constraint that was bound to the type object.

> 与 SQLAlchemy “schema” 类型 **[Boolean]** 和 **[Enum]** 相抵触的类型更改也可能会添加或删除伴随这些类型在本机不支持它们的后端上的约束。 `在这种情况下，existing_type` 参数用于识别和删除绑定到类型对象的先前约束。

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

**参数:**

* ***table_name*** – 目标表的字符串名称。
* ***column_name*** – 目标列的字符串名称，因为它在操作开始之前就存在。
* ***nullable*** – 可选; 指定为 `True` 或 `False` 改变列的可空性.
* ***server_default*** – 可选; 指定字符串 `SQL 表达式`、**[text()]** 或 **[DefaultClause]** 以指示对列默认值的更改。 设置为 `None` 以删除默认值。
* ***comment***<a name="params.comment"></a> – 可选; 要添加到列的新注释的字符串文本。
  > *版本 1.0.6.新增*
* ***new_column_name*** – 可选; 在此处指定字符串名称以指示列重命名操作中的新名称。
* ***type_*** – 可选; 一个 **[TypeEngine]** 类型对象，用于指定对列类型的更改。 对于也指示约束（即 **[Boolean]**、**[Enum]**）的 SQLAlchemy 类型，也会生成约束。
* ***autoincrement*** – 设置列的 `AUTO_INCREMENT` 标志； 目前被MySQL方言所理解。
* ***existing_type*** – 可选; 一个 **[TypeEngine]** 类型对象来指定以前的类型。 这对于所有未指定新类型的 MySQL 列更改操作以及在 SQL Server 列上更改可空性时都是必需的。 如果类型是所谓的 SQLlchemy “schema” 类型，它也可以定义一个约束（即**[Boolean]**、**[Enum]**），以便可以删除约束。
* ***existing_server_default*** – 可选; 列的现有默认值。 如果未更改现有默认值，则在 MySQL 上是必需提供的； 否则 MySQL 将删除默认值。
* ***existing_nullable*** – 可选; 列的现有可空性。 如果没有更改现有的可空性，则在 MySQL 上是必需提供的； 否则 MySQL 将其设置为 `NULL`。
* ***existing_autoincrement*** – 可选; 列的现有自动增量。 用于 MySQL 系统更改指定 `AUTO_INCREMENT` 的列。
* ***existing_comment*** – 要维护的列上现有注释的字符串文本。 如果未更改列上的现有注释，则在 MySQL 上是必需的。
  > *版本 1.0.6.新增*
* ***schema*** – 要在其中操作的可选 **schema** 名称。 要控制默认行为之外的模式引用，请使用 SQLAlchemy 构造 **[quoted_name]**。
* ***postgresql_using*** – 字符串参数，它将指示要在 ALTER COLUMN 中的 Postgresql 特定的 USING 子句中呈现的 SQL 表达式。 该字符串被直接视为原始 SQL，它必须在表达式中显式地包含任何必要的标记引用或转义。
