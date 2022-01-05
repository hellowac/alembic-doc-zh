# drop_index

**drop_index**(*index_name*:  [str], *table_name*:  Optional\[[str]\] = None, *schema*:  Optional\[[str]\] = None, **kw) → Optional\[Table\]

[str]: https://docs.python.org/3/library/stdtypes.html#str
[quoted_name]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name
[Dialects]: https://docs.sqlalchemy.org/en/14/dialects/index.html#dialect-toplevel

Issue a “drop index” instruction using the current migration context.

e.g.:

```python
drop_index("accounts")
```

**Parameters:**

* ***index_name*** – name of the index.
* ***table_name*** – name of the owning table. Some backends such as Microsoft SQL Server require this.
* ***schema*** – Optional **schema** name to operate within. To control quoting of the **schema** outside of the default behavior, use the SQLAlchemy construct **[quoted_name]**.
* ***\*\*kw*** – Additional keyword arguments not mentioned above are dialect specific, and passed in the form `<dialectname>_<argname>`. See the documentation regarding an individual dialect at **[Dialects]** for detail on documented arguments.
