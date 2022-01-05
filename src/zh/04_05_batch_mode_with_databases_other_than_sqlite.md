# Batch mode with databases other than SQLite

**SQLite 以外的数据库的批处理模式**

[Operations.batch_alter_table.table_args]: ../en/ops.html#alembic.operations.Operations.batch_alter_table.params.table_args

There’s an odd use case some shops have, where the “move and copy” style of migration is useful in some cases for databases that do already support ALTER. There’s some cases where an ALTER operation may block access to the table for a long time, which might not be acceptable. “move and copy” can be made to work on other backends, though with a few extra caveats.

The batch mode directive will run the “recreate” system regardless of backend if the flag `recreate='always'` is passed:

```python
with op.batch_alter_table("some_table", recreate='always') as batch_op:
    batch_op.add_column(Column('foo', Integer))
```

The issues that arise in this mode are mostly to do with constraints. Databases such as Postgresql and MySQL with InnoDB will enforce referential integrity (e.g. via foreign keys) in all cases. Unlike SQLite, it’s not as simple to turn off referential integrity across the board (nor would it be desirable). Since a new table is replacing the old one, existing foreign key constraints which refer to the target table will need to be unconditionally dropped before the batch operation, and re-created to refer to the new table afterwards. Batch mode currently does not provide any automation for this.

The Postgresql database and possibly others also have the behavior such that when the new table is created, a naming conflict occurs with the named constraints of the new table, in that they match those of the old table, and on Postgresql, these names need to be unique across all tables. The Postgresql dialect will therefore emit a “DROP CONSTRAINT” directive for all constraints on the old table before the new one is created; this is “safe” in case of a failed operation because Postgresql also supports transactional DDL.

Note that also as is the case with SQLite, CHECK constraints need to be moved over between old and new table manually using the **[Operations.batch_alter_table.table_args]** parameter.
