# drop_column

**drop_column**(*table_name*:  [str], *column_name*:  [str], *schema*:  Optional\[[str]\] = None, **kw) → Optional\[Table\]

[str]: https://docs.python.org/3/library/stdtypes.html#str
[quoted_name]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name

Issue a “drop column” instruction using the current migration context.

e.g.:

```python
drop_column('organization', 'account_id')
```

**Parameters:**

* ***table_name*** – name of table
* ***column_name*** – name of column
* ***schema*** – Optional **schema** name to operate within. To control quoting of the **schema** outside of the default behavior, use the SQLAlchemy construct **[quoted_name]**.
* ***mssql_drop_check*** – Optional boolean. When `True`, on Microsoft SQL Server only, first drop the CHECK constraint on the column using a SQL-script-compatible block that selects into a @variable from sys.check_constraints, then exec’s a separate DROP CONSTRAINT for that constraint.
* ***mssql_drop_default*** – Optional boolean. When `True`, on Microsoft SQL Server only, first drop the DEFAULT constraint on the column using a SQL-script-compatible block that selects into a @variable from sys.default_constraints, then exec’s a separate DROP CONSTRAINT for that default.
* ***mssql_drop_foreign_key*** – Optional boolean. When `True`, on Microsoft SQL Server only, first drop a single FOREIGN KEY constraint on the column using a SQL-script-compatible block that selects into a @variable from sys.foreign_keys/sys.foreign_key_columns, then exec’s a separate DROP CONSTRAINT for that default. Only works if the column has exactly one FK constraint which refers to it, at the moment.
