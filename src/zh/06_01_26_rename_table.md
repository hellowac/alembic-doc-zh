# rename_table

**rename_table**(*old_table_name*:  [str], *new_table_name*:  [str], *schema*:  Optional\[[str]\] = None) → Optional\[Table\]

[str]: https://docs.python.org/3/library/stdtypes.html#str
[quoted_name]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name

Emit an ALTER TABLE to rename a table.

**Parameters:**

* ***old_table_name*** – old name.
* ***new_table_name*** – new name.
* ***schema*** – Optional **schema** name to operate within. To control quoting of the **schema** outside of the default behavior, use the SQLAlchemy construct **[quoted_name]**.
