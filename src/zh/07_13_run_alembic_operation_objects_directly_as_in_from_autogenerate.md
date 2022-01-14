# Run Alembic Operation Objects Directly (as in from autogenerate)

[Operations]: ../zh/06_operation_reference.md
[Operations.invoke()]: ../zh/06_01_24_invoke.md
[autogenerate.produce_migrations()]: ../zh/08_06_01_getting_diffs.md#produce_migrations
[ops.MigrationScript]: ../zh/08_05_02_built_in_operation_objects.md#MigrationScript
[ModifyTableOps]: ../zh/08_05_02_built_in_operation_objects.md#ModifyTableOps
[autogenerate.compare_metadata()]: ../zh/08_06_01_getting_diffs.md#compare_metadata

The **[Operations]** object has a method known as **[Operations.invoke()]** that will generically invoke a particular operation object. We can therefore use the **[autogenerate.produce_migrations()]** function to run an autogenerate comparison, get back a **[ops.MigrationScript]** structure representing the changes, and with a little bit of insider information we can invoke them directly.

> **[Operations]** 对象有一个称为 **[Operations.invoke()]** 的方法，它通常会调用特定的操作对象。 因此，我们可以使用 **[autogenerate.produce_migrations()]** 函数来运行自动生成比较，返回一个表示更改的 **[ops.MigrationScript]** 结构，并且通过一些内部信息，我们可以直接调用它们。

The traversal through the **[ops.MigrationScript]** structure is as follows:

> 通过 **[ops.MigrationScript]** 结构的遍历如下：

```python
use_batch = engine.name == "sqlite"

stack = [migrations.upgrade_ops]
while stack:
    elem = stack.pop(0)

    if use_batch and isinstance(elem, ModifyTableOps):
        with operations.batch_alter_table(
            elem.table_name, schema=elem.schema
        ) as batch_ops:
            for table_elem in elem.ops:
                # work around Alembic issue #753 (fixed in 1.5.0)
                if hasattr(table_elem, "column"):
                    table_elem.column = table_elem.column.copy()
                batch_ops.invoke(table_elem)

    elif hasattr(elem, "ops"):
        stack.extend(elem.ops)
    else:
        # work around Alembic issue #753 (fixed in 1.5.0)
        if hasattr(elem, "column"):
            elem.column = elem.column.copy()
        operations.invoke(elem)
```

Above, we detect elements that have a collection of operations by looking for the `.ops` attribute. A check for **[ModifyTableOps]** allows us to use a batch context if we are supporting that. Finally there’s a workaround for an Alembic issue that exists for SQLAlchemy 1.3.20 and greater combined with Alembic older than 1.5.

> 上面，我们通过查找 `.ops` 属性来检测具有操作集合的元素。 如果我们支持，对 **[ModifyTableOps]** 的检查允许我们使用批处理上下文。 最后，对于 SQLAlchemy 1.3.20 和更高版本以及早于 1.5 的 Alembic 存在的 Alembic 问题，有一个解决方法。

A full example follows. The overall setup here is copied from the example at **[autogenerate.compare_metadata()]**:

> 下面是一个完整的例子。 这里的整体设置是从 **[autogenerate.compare_metadata()]** 的示例复制而来的：

```python
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table

from alembic.autogenerate import produce_migrations
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.operations.ops import ModifyTableOps


engine = create_engine("sqlite://", echo=True)

with engine.connect() as conn:
    conn.execute(
        """
        create table foo (
            id integer not null primary key,
            old_data varchar(50),
            x integer
        )"""
    )

    conn.execute(
        """
        create table bar (
            data varchar(50)
        )"""
    )

metadata = MetaData()
Table(
    "foo",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("data", Integer),
    Column("x", Integer, nullable=False),
)
Table("bat", metadata, Column("info", String(100)))

mc = MigrationContext.configure(engine.connect())

migrations = produce_migrations(mc, metadata)

operations = Operations(mc)

use_batch = engine.name == "sqlite"

stack = [migrations.upgrade_ops]
while stack:
    elem = stack.pop(0)

    if use_batch and isinstance(elem, ModifyTableOps):
        with operations.batch_alter_table(
            elem.table_name, schema=elem.schema
        ) as batch_ops:
            for table_elem in elem.ops:
                # work around Alembic issue #753 (fixed in 1.5.0)
                if hasattr(table_elem, "column"):
                    table_elem.column = table_elem.column.copy()
                batch_ops.invoke(table_elem)

    elif hasattr(elem, "ops"):
        stack.extend(elem.ops)
    else:
        # work around Alembic issue #753 (fixed in 1.5.0)
        if hasattr(elem, "column"):
            elem.column = elem.column.copy()
        operations.invoke(elem)
```
