# Including unnamed UNIQUE constraints

**包含未命名的 UNIQUE 约束**

[table_args]: ../zh/06_01_03_batch_alter_table.md#table_args

A similar, but frustratingly slightly different, issue is that in the case of UNIQUE constraints, we again have the issue that SQLite allows unnamed UNIQUE constraints to exist on the database, however in this case, SQLAlchemy prior to version 1.0 doesn’t reflect these constraints at all. It does properly reflect named unique constraints with their names, however.

> 一个类似但令人沮丧的稍微不同的问题是，在 UNIQUE 约束的情况下，我们再次遇到 SQLite 允许数据库上存在未命名的 UNIQUE 约束的问题，但是在这种情况下，1.0 版之前的 SQLAlchemy 没有反映这些 根本没有约束。 但是，它确实正确地反映了命名的唯一约束及其名称。

So in this case, the workaround for foreign key names is still not sufficient prior to SQLAlchemy 1.0. If our table includes unnamed unique constraints, and we’d like them to be re-created along with the table, we need to include them directly, which can be via the **[table_args]** argument:

> 所以在这种情况下，外键名称的解决方法在 SQLAlchemy 1.0 之前仍然不够。 如果我们的表包含未命名的唯一约束，并且我们希望它们与表一起重新创建，我们需要直接包含它们，这可以通过 **[table_args]** 参数：

```python
with self.op.batch_alter_table(
        "bar", table_args=(UniqueConstraint('username'),)
    ):
    batch_op.add_column(Column('foo', Integer))
```
