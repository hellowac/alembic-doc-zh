# drop_constraint

**drop_constraint**(*constraint_name*:  [str], *table_name*:  [str], *type_*:  Optional\[[str]\] = None, *schema*:  Optional\[[str]\] = None) → Optional\[Table\]

[str]: https://docs.python.org/3/library/stdtypes.html#str
[quoted_name]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name

Drop a constraint of the given name, typically via DROP CONSTRAINT.

**Parameters:**

* ***constraint_name*** – name of the constraint.
* ***table_name*** – table name.
* ***type_*** – optional, required on MySQL. can be ‘foreignkey’, ‘primary’, ‘unique’, or ‘check’.
* ***schema*** – Optional **schema** name to operate within. To control quoting of the **schema** outside of the default behavior, use the SQLAlchemy construct **[quoted_name]**.
