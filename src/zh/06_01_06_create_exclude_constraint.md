# create_exclude_constraint

**create_exclude_constraint**(*constraint_name*:  [str], *table_name*:  [str], *elements: Any, **kw: Any) → Optional\[Table\]

[str]: https://docs.python.org/3/library/stdtypes.html#str

Issue an alter to create an EXCLUDE constraint using the current migration context.

> **Note:** This method is Postgresql specific, and additionally requires at least SQLAlchemy 1.0.

e.g.:

```python
from alembic import op

op.create_exclude_constraint(
    "user_excl",
    "user",

    ("period", '&&'),
    ("group", '='),
    where=("group != 'some group'")

)
```

> **Note** that the expressions work the same way as that of the `ExcludeConstraint` object itself; if plain strings are passed, quoting rules must be applied manually.

**Parameters:**

* ***name*** – Name of the constraint.
* ***table_name*** – String name of the source table.
* ***elements*** – exclude conditions.
* ***where*** – SQL expression or SQL string with optional WHERE clause.
* ***deferrable*** – optional bool. If set, emit DEFERRABLE or NOT DEFERRABLE when issuing DDL for this constraint.
* ***initially*** – optional string. If set, emit INITIALLY <value> when issuing DDL for this constraint.
* ***schema*** – Optional **schema** name to operate within.
