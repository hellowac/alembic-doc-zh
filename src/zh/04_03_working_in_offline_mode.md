# Working in Offline Mode

**在离线模式下工作**

[Operations.batch_alter_table()]: ../en/ops.html#alembic.operations.Operations.batch_alter_table
[copy_from]: ../en/ops.html#alembic.operations.Operations.batch_alter_table.params.copy_from

In the preceding sections, we’ve seen how much of an emphasis the “move and copy” process has on using reflection in order to know the structure of the table that is to be copied. This means that in the typical case, “online” mode, where a live database connection is present so that **[Operations.batch_alter_table()]** can reflect the table from the database, is required; the `--sql` flag **cannot** be used without extra steps.

To support offline mode, the system must work without table reflection present, which means the full table as it intends to be created must be passed to **[Operations.batch_alter_table()]** using copy_from:

```python
meta = MetaData()
some_table = Table(
    'some_table', meta,
    Column('id', Integer, primary_key=True),
    Column('bar', String(50))
)

with op.batch_alter_table("some_table", copy_from=some_table) as batch_op:
    batch_op.add_column(Column('foo', Integer))
    batch_op.drop_column('bar')
```

The above use pattern is pretty tedious and quite far off from Alembic’s preferred style of working; however, if one needs to do SQLite-compatible “move and copy” migrations and need them to generate flat SQL files in “offline” mode, there’s not much alternative.
