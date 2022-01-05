# drop_table

**drop_table**(*table_name*:  [str], *schema*:  Optional\[[str]\] = None, **kw: Any) → None

[str]: https://docs.python.org/3/library/stdtypes.html#str
[quoted_name]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name
[sqlalchemy.schema.Table]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table

Issue a “drop table” instruction using the current migration context.

e.g.:

```python
drop_table("accounts")
```

**Parameters:**

* ***table_name*** – Name of the table
* ***schema*** – Optional **schema** name to operate within. To control quoting of the **schema** outside of the default behavior, use the SQLAlchemy construct **[quoted_name]**.
* ***\*\*kw*** – Other keyword arguments are passed to the underlying **[sqlalchemy.schema.Table]** object created for the command.
