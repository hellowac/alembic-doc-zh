# Including unnamed UNIQUE constraints

**包含未命名的 UNIQUE 约束**

[table_args]: ../en/ops.html#alembic.operations.Operations.batch_alter_table.params.table_args

A similar, but frustratingly slightly different, issue is that in the case of UNIQUE constraints, we again have the issue that SQLite allows unnamed UNIQUE constraints to exist on the database, however in this case, SQLAlchemy prior to version 1.0 doesn’t reflect these constraints at all. It does properly reflect named unique constraints with their names, however.

So in this case, the workaround for foreign key names is still not sufficient prior to SQLAlchemy 1.0. If our table includes unnamed unique constraints, and we’d like them to be re-created along with the table, we need to include them directly, which can be via the **[table_args]** argument:

```python
with self.op.batch_alter_table(
        "bar", table_args=(UniqueConstraint('username'),)
    ):
    batch_op.add_column(Column('foo', Integer))
```
