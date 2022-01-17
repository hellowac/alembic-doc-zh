# Conditional Migration Elements

**条件迁移元素**

[EnvironmentContext.get_x_argument()]: ../zh/08_02_01_11_get_x_argument.md

This example features the basic idea of a common need, that of affecting how a migration runs based on command line switches.

> 此示例具有共同需求的基本思想，即基于命令行开关影响迁移的运行方式。

The technique to use here is simple; within a migration script, inspect the **[EnvironmentContext.get_x_argument()]** collection for any additional, user-defined parameters. Then take action based on the presence of those arguments.

> 这里使用的技术很简单； 在迁移脚本中，检查 **[EnvironmentContext.get_x_argument()]** 集合中是否有任何其他用户定义的参数。 然后根据这些参数的存在采取行动。

To make it such that the logic to inspect these flags is easy to use and modify, we modify our `script.py.mako` template to make this feature available in all new revision files:

> 为了使检查这些标志的逻辑易于使用和修改，我们修改了我们的 `script.py.mako` 模板，以使该功能在所有新修订文件中都可用：

```python
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision}
Create Date: ${create_date}

"""

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

from alembic import context


def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_upgrades()

def downgrade():
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_downgrades()
    schema_downgrades()

def schema_upgrades():
    """schema upgrade migrations go here."""
    ${upgrades if upgrades else "pass"}

def schema_downgrades():
    """schema downgrade migrations go here."""
    ${downgrades if downgrades else "pass"}

def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
```

Now, when we create a new migration file, the `data_upgrades()` and `data_downgrades()` placeholders will be available, where we can add optional data migrations:

> 现在，当我们创建一个新的迁移文件时， `data_upgrades()` 和 `data_downgrades()` 新增的函数将可用，我们可以在其中添加可选的数据迁移：

```python
"""rev one

Revision ID: 3ba2b522d10d
Revises: None
Create Date: 2014-03-04 18:05:36.992867

"""

# revision identifiers, used by Alembic.
revision = '3ba2b522d10d'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy import String, Column
from sqlalchemy.sql import table, column

from alembic import context

def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_upgrades()

def downgrade():
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_downgrades()
    schema_downgrades()

def schema_upgrades():
    """schema upgrade migrations go here."""
    op.create_table("my_table", Column('data', String))

def schema_downgrades():
    """schema downgrade migrations go here."""
    op.drop_table("my_table")

def data_upgrades():
    """Add any optional data upgrade migrations here!"""

    my_table = table('my_table',
        column('data', String),
    )

    op.bulk_insert(my_table,
        [
            {'data': 'data 1'},
            {'data': 'data 2'},
            {'data': 'data 3'},
        ]
    )

def data_downgrades():
    """Add any optional data downgrade migrations here!"""

    op.execute("delete from my_table")
```

To invoke our migrations with data included, we use the `-x` flag:

> 要调用包含数据的迁移，我们使用 `-x` 标志：

```bash
alembic -x data=true upgrade head
```

The **[EnvironmentContext.get_x_argument()]** is an easy way to support new commandline options within environment and migration scripts.

> **[EnvironmentContext.get_x_argument()]** 是一种在环境和迁移脚本中支持新命令行选项的简单方法。
