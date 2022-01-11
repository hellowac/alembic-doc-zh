# Batch mode with databases other than SQLite

**SQLite 以外的数据库的批处理模式**

[Operations.batch_alter_table.table_args]: ../en/ops.html#alembic.operations.Operations.batch_alter_table.params.table_args

There’s an odd use case some shops have, where the “move and copy” style of migration is useful in some cases for databases that do already support ALTER. There’s some cases where an ALTER operation may block access to the table for a long time, which might not be acceptable. “move and copy” can be made to work on other backends, though with a few extra caveats.

> 一些商店有一个奇怪的用例，其中“移动和复制”风格的迁移在某些情况下对于已经支持 ALTER 的数据库很有用。 在某些情况下，ALTER 操作可能会长时间阻止对表的访问，这可能是不可接受的。 “移动和复制” 可以在其他后端工作，尽管有一些额外的警告。

The batch mode directive will run the “recreate” system regardless of backend if the flag `recreate='always'` is passed:

> 如果传递了标志 `recreate='always'`，批处理模式指令将运行 “recreate” 系统，而不管后端如何：

```python
with op.batch_alter_table("some_table", recreate='always') as batch_op:
    batch_op.add_column(Column('foo', Integer))
```

The issues that arise in this mode are mostly to do with constraints. Databases such as Postgresql and MySQL with InnoDB will enforce referential integrity (e.g. via foreign keys) in all cases. Unlike SQLite, it’s not as simple to turn off referential integrity across the board (nor would it be desirable). Since a new table is replacing the old one, existing foreign key constraints which refer to the target table will need to be unconditionally dropped before the batch operation, and re-created to refer to the new table afterwards. Batch mode currently does not provide any automation for this.

> 这种模式下出现的问题主要与约束有关。 在所有情况下，带有 InnoDB 的 Postgresql 和 MySQL 等数据库都将强制执行引用完整性（例如通过外键）。 与 SQLite 不同，全面关闭参照完整性并不那么简单（也不是可取的）。 由于新表正在替换旧表，因此需要在批处理操作之前无条件地删除引用目标表的现有外键约束，然后重新创建以引用新表。 批处理模式目前不为此提供任何自动化。

The Postgresql database and possibly others also have the behavior such that when the new table is created, a naming conflict occurs with the named constraints of the new table, in that they match those of the old table, and on Postgresql, these names need to be unique across all tables. The Postgresql dialect will therefore emit a “DROP CONSTRAINT” directive for all constraints on the old table before the new one is created; this is “safe” in case of a failed operation because Postgresql also supports transactional DDL.

> Postgresql 数据库和可能的其他数据库也有这样的行为，即在创建新表时，与新表的命名约束发生命名冲突，因为它们与旧表的约束匹配，并且在 Postgresql 上，这些名称需要 在所有表中都是唯一的。 因此，在创建新表之前，Postgresql 方言将为旧表上的所有约束发出“DROP CONSTRAINT”指令； 这在操作失败的情况下是“安全的”，因为 Postgresql 还支持事务 DDL。

Note that also as is the case with SQLite, CHECK constraints need to be moved over between old and new table manually using the **[Operations.batch_alter_table.table_args]** parameter.

> 请注意，与 SQLite 的情况一样，需要使用  **[Operations.batch_alter_table.table_args]** 参数在新旧表之间手动移动 CHECK 约束。
