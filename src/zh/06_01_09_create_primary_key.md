# create_primary_key

**create_primary_key**(*constraint_name*:  Optional\[[str]\], *table_name*:  [str], *columns*:  List\[[str]\], *schema*:  Optional\[[str]\] = None) → Optional\[Table\]

[str]: https://docs.python.org/3/library/stdtypes.html#str
[Table]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table
[PrimaryKeyConstraint]: https://docs.sqlalchemy.org/en/14/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint
[AddConstraint]: https://docs.sqlalchemy.org/en/14/core/ddl.html#sqlalchemy.schema.AddConstraint
[Configuring Constraint Naming Conventions]: https://docs.sqlalchemy.org/en/14/core/constraints.html#constraint-naming-conventions
[quoted_name]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name

Issue a “create primary key” instruction using the current migration context.

e.g.:

```python
from alembic import op

op.create_primary_key(
            "pk_my_table", "my_table",
            ["id", "version"]
        )
```

This internally generates a **[Table]** object containing the necessary columns, then generates a new **[PrimaryKeyConstraint]** object which it then associates with the **[Table]**. Any event listeners associated with this action will be fired off normally. The **[AddConstraint]** construct is ultimately used to generate the ALTER statement.

**Parameters:**

* ***constraint_name*** – Name of the primary key constraint. The `name` is necessary so that an ALTER statement can be emitted. For setups that use an automated naming scheme such as that described at **[Configuring Constraint Naming Conventions]** `name` here can be `None`, as the event listener will apply the `name` to the constraint object when it is associated with the table.
* ***table_name*** – String name of the target table.
* ***columns*** – a list of string column names to be applied to the primary key constraint.
* ***schema*** – Optional **schema** name to operate within. To control quoting of the **schema** outside of the default behavior, use the SQLAlchemy construct **[quoted_name]**.
