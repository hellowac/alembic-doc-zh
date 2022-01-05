# create_foreign_key

**create_foreign_key**(*constraint_name*:  Optional\[[str]\], *source_table*:  [str], *referent_table*:  [str], *local_cols*:  List\[[str]\], *remote_cols*:  List\[[str]\], *onupdate*:  Optional\[[str]\] = None, *ondelete*:  Optional\[[str]\] = None, *deferrable*:  Optional\[[bool]\] = None, *initially*:  Optional\[[str]\] = None, *match*:  Optional\[[str]\] = None, *source_schema*:  Optional\[[str]\] = None, *referent_schema*:  Optional\[[str]\] = None, **dialect_kw) → Optional\[Table\]

[str]: https://docs.python.org/3/library/stdtypes.html#str
[bool]: https://docs.python.org/3/library/functions.html#bool
[Table]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table
[ForeignKeyConstraint]: https://docs.sqlalchemy.org/en/14/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint
[AddConstraint]: https://docs.sqlalchemy.org/en/14/core/ddl.html#sqlalchemy.schema.AddConstraint
[Configuring Constraint Naming Conventions]: https://docs.sqlalchemy.org/en/14/core/constraints.html#constraint-naming-conventions

Issue a “create foreign key” instruction using the current migration context.

e.g.:

```python
from alembic import op
op.create_foreign_key(
            "fk_user_address", "address",
            "user", ["user_id"], ["id"])
```

This internally generates a **[Table]** object containing the necessary columns, then generates a new **[ForeignKeyConstraint]** object which it then associates with the **[Table]**. Any event listeners associated with this action will be fired off normally. The **[AddConstraint]** construct is ultimately used to generate the ALTER statement.

**Parameters:**

* ***constraint_name*** – Name of the foreign key constraint. The `name` is necessary so that an ALTER statement can be emitted. For setups that use an automated naming scheme such as that described at **[Configuring Constraint Naming Conventions]**, `name` here can be `None`, as the event listener will apply the `name` to the constraint object when it is associated with the table.
* ***source_table*** – String name of the source table.
* ***referent_table*** – String name of the destination table.
* ***local_cols*** – a list of string column names in the source table.
* ***remote_cols*** – a list of string column names in the remote table.
* ***onupdate*** – Optional string. If set, emit ON UPDATE `<value>` when issuing DDL for this constraint. Typical values include CASCADE, DELETE and RESTRICT.
* ***ondelete*** – Optional string. If set, emit ON DELETE `<value>` when issuing DDL for this constraint. Typical values include CASCADE, DELETE and RESTRICT.
* ***deferrable*** – optional bool. If set, emit DEFERRABLE or NOT DEFERRABLE when issuing DDL for this constraint.
* ***source_schema*** – Optional schema name of the source table.
* ***referent_schema*** – Optional schema name of the destination table.
