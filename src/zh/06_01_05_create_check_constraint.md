# create_check_constraint

**create_check_constraint**(*constraint_name*:  Optional\[[str]\], *table_name*:  [str], *condition*:  Union\[[str], BinaryExpression\], *schema*:  Optional\[[str]\] = None, **kw) → Optional\[Table\]

[str]: https://docs.python.org/3/library/stdtypes.html#str
[sqlalchemy.schema.CheckConstraint]: https://docs.sqlalchemy.org/en/14/core/constraints.html#sqlalchemy.schema.CheckConstraint
[Configuring Constraint Naming Conventions]: https://docs.sqlalchemy.org/en/14/core/constraints.html#constraint-naming-conventions
[quoted_name]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name

Issue a “create check constraint” instruction using the current migration context.

e.g.:

```python
from alembic import op
from sqlalchemy.sql import column, func

op.create_check_constraint(
    "ck_user_name_len",
    "user",
    func.len(column('name')) > 5
)
```

CHECK constraints are usually against a SQL expression, so ad-hoc table metadata is usually needed. The function will convert the given arguments into a **[sqlalchemy.schema.CheckConstraint]** bound to an anonymous table in order to emit the CREATE statement.

**Parameters:**

* ***name*** – Name of the check constraint. The `name` is necessary so that an ALTER statement can be emitted. For setups that use an automated naming scheme such as that described at **[Configuring Constraint Naming Conventions]**, `name` here can be `None`, as the event listener will apply the `name` to the constraint object when it is associated with the table.
* ***table_name*** – String name of the source table.
* ***condition*** – SQL expression that’s the **condition** of the constraint. Can be a string or SQLAlchemy expression language structure.
* ***deferrable*** – optional bool. If set, emit DEFERRABLE or NOT DEFERRABLE when issuing DDL for this constraint.
* ***initially*** – optional string. If set, emit INITIALLY <value> when issuing DDL for this constraint.
* ***schema*** – Optional **schema** name to operate within. To control quoting of the **schema** outside of the default behavior, use the SQLAlchemy construct **[quoted_name]**.
