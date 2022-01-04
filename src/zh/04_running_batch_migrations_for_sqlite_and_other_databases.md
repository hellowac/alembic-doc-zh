# Running “Batch” Migrations for SQLite and Other Databases

**在SQLite和其他数据中运行"Batch"迁移脚本**

[Operations.batch_alter_table()]: ../en/ops.html#alembic.operations.Operations.batch_alter_table
[Operations.add_column()]: ../en/ops.html#alembic.operations.Operations.add_column

The SQLite database presents a challenge to migration tools in that it has almost no support for the ALTER statement which relational schema migrations rely upon. The rationale for this stems from philosophical and architectural concerns within SQLite, and they are unlikely to be changed.

Migration tools are instead expected to produce copies of SQLite tables that correspond to the new structure, transfer the data from the existing table to the new one, then drop the old table. For our purposes here we’ll call this **“move and copy”** workflow, and in order to accommodate it in a way that is reasonably predictable, while also remaining compatible with other databases, Alembic provides the **batch** operations context.

Within this context, a relational table is named, and then a series of mutation operations to that table alone are specified within the block. When the context is complete, a process begins whereby the **“move and copy”** procedure begins; the existing table structure is reflected from the database, a new version of this table is created with the given changes, data is copied from the old table to the new table using “INSERT from SELECT”, and finally the old table is dropped and the new one renamed to the original name.

The **[Operations.batch_alter_table()]** method provides the gateway to this process:

```python
with op.batch_alter_table("some_table") as batch_op:
    batch_op.add_column(Column('foo', Integer))
    batch_op.drop_column('bar')
```

When the above directives are invoked within a migration script, on a SQLite backend we would see SQL like:

```sql
CREATE TABLE _alembic_batch_temp (
  id INTEGER NOT NULL,
  foo INTEGER,
  PRIMARY KEY (id)
);
INSERT INTO _alembic_batch_temp (id) SELECT some_table.id FROM some_table;
DROP TABLE some_table;
ALTER TABLE _alembic_batch_temp RENAME TO some_table;
```

On other backends, we’d see the usual ALTER statements done as though there were no batch directive - the batch context by default only does the “move and copy” process if SQLite is in use, and if there are migration directives other than **[Operations.add_column()]** present, which is the one kind of column-level ALTER statement that SQLite supports. **[Operations.batch_alter_table()]** can be configured to run “move and copy” unconditionally in all cases, including on databases other than SQLite; more on this is below.
