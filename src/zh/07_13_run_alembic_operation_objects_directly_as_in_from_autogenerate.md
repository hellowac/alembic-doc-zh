# Run Alembic Operation Objects Directly (as in from autogenerate)

[Operations]: ../en/ops.html#alembic.operations.Operations
[Operations.invoke()]: ../en/ops.html#alembic.operations.Operations.invoke
[autogenerate.produce_migrations()]: ../en/api/autogenerate.html#alembic.autogenerate.produce_migrations
[ops.MigrationScript]: ../en/api/operations.html#alembic.operations.ops.MigrationScript
[ModifyTableOps]: ../en/api/operations.html#alembic.operations.ops.ModifyTableOps
[autogenerate.compare_metadata()]: ../en/api/autogenerate.html#alembic.autogenerate.compare_metadata

The **[Operations]** object has a method known as **[Operations]**.invoke() that will generically invoke a particular operation object. We can therefore use the **[autogenerate.produce_migrations()]** function to run an autogenerate comparison, get back a **[ops.MigrationScript]** structure representing the changes, and with a little bit of insider information we can invoke them directly.

The traversal through the **[ops.MigrationScript]** structure is as follows:

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

A full example follows. The overall setup here is copied from the example at **[autogenerate.compare_metadata()]**:

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
