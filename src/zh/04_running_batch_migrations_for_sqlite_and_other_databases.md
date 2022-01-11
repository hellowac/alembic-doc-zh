# Running “Batch” Migrations for SQLite and Other Databases

**在SQLite和其他数据中运行"批处理"迁移脚本**

[Operations.batch_alter_table()]: ../zh/06_01_03_batch_alter_table.md
[Operations.add_column()]: ../zh/06_01_01_add_column.md

The SQLite database presents a challenge to migration tools in that it has almost no support for the ALTER statement which relational schema migrations rely upon. The rationale for this stems from philosophical and architectural concerns within SQLite, and they are unlikely to be changed.

> SQLite 数据库对迁移工具提出了挑战，因为它几乎不支持关系模式迁移所依赖的 ALTER 语句。 这样做的理由源于 SQLite 中的哲学和架构问题，它们不太可能被改变。

Migration tools are instead expected to produce copies of SQLite tables that correspond to the new structure, transfer the data from the existing table to the new one, then drop the old table. For our purposes here we’ll call this **“move and copy”** workflow, and in order to accommodate it in a way that is reasonably predictable, while also remaining compatible with other databases, Alembic provides the **batch** operations context.

> 相反，迁移工具应该生成与新结构相对应的 SQLite 表副本，将数据从现有表传输到新表，然后删除旧表。 出于我们的目的，我们将这里称为 **“移动和复制”** 工作流，并且为了以合理可预测的方式适应它，同时保持与其他数据库的兼容性，Alembic 提供了 **批处理** 操作上下文。

Within this context, a relational table is named, and then a series of mutation operations to that table alone are specified within the block. When the context is complete, a process begins whereby the **“move and copy”** procedure begins; the existing table structure is reflected from the database, a new version of this table is created with the given changes, data is copied from the old table to the new table using “INSERT from SELECT”, and finally the old table is dropped and the new one renamed to the original name.

> 在此上下文中，一个关系表被命名，然后在块中指定对该表的一系列变异操作。 当上下文完成时，一个过程开始，**“移动和复制”** 过程开始； 现有的表结构反映在数据库中，使用给定的更改创建该表的新版本，使用 “INSERT from SELECT” 将数据从旧表复制到新表，最后旧表被删除，新表重命名为原始名称。

The **[Operations.batch_alter_table()]** method provides the gateway to this process:

> **[Operations.batch_alter_table()]** 方法提供了此过程的上下文：

```python
with op.batch_alter_table("some_table") as batch_op:
    batch_op.add_column(Column('foo', Integer))
    batch_op.drop_column('bar')
```

When the above directives are invoked within a migration script, on a SQLite backend we would see SQL like:

> 当在迁移脚本中调用上述指令时，在 SQLite 后端我们会看到如下 SQL：

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

> 在其他后端，我们会看到执行通常的 ALTER 语句，就好像没有批处理指令一样 - 默认情况下，批处理上下文仅在使用 SQLite 并且存在除 **[Operations.add_column()]** 之外的迁移指令（这是 SQLite 支持的一种列级 ALTER 语句）时才执行 **“移动和复制”** 过程。 **[Operations.batch_alter_table()]** 可以配置为在所有情况下无条件地运行 **“移动和复制”**，包括在 SQLite 以外的数据库上； 更多内容如下。
