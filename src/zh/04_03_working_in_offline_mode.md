# Working in Offline Mode

**在离线模式下工作**

[Operations.batch_alter_table()]: ../zh/06_01_03_batch_alter_table.md
[copy_from]: ../zh/06_01_03_batch_alter_table.md#copy_from

In the preceding sections, we’ve seen how much of an emphasis the “move and copy” process has on using reflection in order to know the structure of the table that is to be copied. This means that in the typical case, “online” mode, where a live database connection is present so that **[Operations.batch_alter_table()]** can reflect the table from the database, is required; the `--sql` flag **cannot** be used without extra steps.

> 在前面的部分中，我们已经看到 “移动和复制” 过程对于使用反射来了解要复制的表的结构有多么重要。 这意味着在典型情况下，需要“在线”模式，其中存在实时数据库连接，以便 **[Operations.batch_alter_table()]** 可以反映数据库中的表； 如果没有额外的步骤，就不能使用 `--sql` 标志。

To support offline mode, the system must work without table reflection present, which means the full table as it intends to be created must be passed to **[Operations.batch_alter_table()]** using **[copy_from]**:

> 为了支持离线模式，系统必须在没有表反射的情况下工作，这意味着必须使用 **[copy_from]** 将要创建的完整表传递给 **[Operations.batch_alter_table()]**：

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

> 上述使用模式相当乏味，与 Alembic 喜欢的工作方式相去甚远； 但是，如果需要进行与 SQLite 兼容的“移动和复制”迁移，并需要它们在“离线”模式下生成平面 SQL 文件，则别无选择。
