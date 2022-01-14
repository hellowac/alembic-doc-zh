# Create a Migration Script

[create_table()]: ../zh/06_01_10_create_table.md
[drop_table()]: ../zh/06_01_16_drop_table.md
[Operation Reference]: ../zh/06_operation_reference.md
[操作参考]: ../zh/06_operation_reference.md
[Building an Up to Date Database from Scratch]: ../zh/07_01_building_an_up_to_date_database_from_scratch.md
[从头开始构建最新数据库部分]: ../zh/07_01_building_an_up_to_date_database_from_scratch.md

**创建迁移脚本**

With the environment in place we can create a new revision, using `alembic revision`:

> 环境准备好后，我们可以使用 `alembic revision` 创建一个新修订：

```bash
$ alembic revision -m "create account table"
Generating /path/to/yourproject/alembic/versions/1975ea83b712_create_accoun
t_table.py...done
```

A new file `1975ea83b712_create_account_table.py` is generated. Looking inside the file:

> 生成了一个新文件`1975ea83b712_create_account_table.py`。 文件内容如下:

```python
"""create account table

Revision ID: 1975ea83b712
Revises:
Create Date: 2011-11-08 11:40:27.089406

"""

# revision identifiers, used by Alembic.
revision = '1975ea83b712'
down_revision = None
branch_labels = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    pass

def downgrade():
    pass
```

The file contains some header information, identifiers for the current revision and a “downgrade” revision, an import of basic Alembic directives, and empty `upgrade()` and `downgrade()` functions. Our job here is to populate the `upgrade()` and `downgrade()` functions with directives that will apply a set of changes to our database. Typically, `upgrade()` is required while `downgrade()` is only needed if down-revision capability is desired, though it’s probably a good idea.

> 该文件包含一些标题信息、当前修订和“downgrade”修订的标识符、Alembic 基本的导入指令以及空的 `upgrade()` 和 `downgrade()` 函数。我们在这里的工作是使用指令填充 `upgrade()` 和 `downgrade()` 函数，这些指令将对我们的数据库应用一组更改。通常，`upgrade()` 是必需的，而 `downgrade()` 仅在向下修订功能需要时才使用，尽管这可能是一个好主意。

Another thing to notice is the `down_revision` variable. This is how Alembic knows the correct order in which to apply migrations. When we create the next revision, the new file’s `down_revision` identifier would point to this one:

> 另一件需要注意的是 `down_revision` 变量。 这就是 Alembic 知道应用迁移的正确顺序的方式。 当我们创建下一个修订版时，新文件的 `down_revision` 标识符将指向这个：

```python
# revision identifiers, used by Alembic.
revision = 'ae1027a6acf'
down_revision = '1975ea83b712'
```

Every time Alembic runs an operation against the `versions/` directory, it reads all the files in, and composes a list based on how the `down_revision` identifiers link together, with the `down_revision` of `None` representing the first file. In theory, if a migration environment had thousands of migrations, this could begin to add some latency to startup, but in practice a project should probably prune old migrations anyway (see the section [Building an Up to Date Database from Scratch](/en/cookbook.html#building-uptodate) for a description on how to do this, while maintaining the ability to build the current database fully).

> 每次 Alembic 对 `versions/` 目录运行操作时，它都会读取所有文件，并根据 `down_revision` 标识符链接在一起的方式组成一个列表，其中`down_revision` 变量为 `None` 的文件代表第一个迁移文件。 理论上，如果迁移环境有数千次迁移，这在开始迁移时增加一些延迟，但在项目实践中，无论如何都应该精简旧的迁移(有关如何执行此操作的说明，请参阅[从头开始构建最新数据库部分]，同时保持完全构建当前数据库的能力).

We can then add some directives to our script, suppose adding a new table `account`:

> 然后我们可以向我们的脚本添加一些指令，假设添加一个新表 `account`：

```python
def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )

def downgrade():
    op.drop_table('account')
```

[create_table()] and [drop_table()] are Alembic directives. Alembic provides all the basic database migration operations via these directives, which are designed to be as simple and minimalistic as possible; there’s no reliance upon existing table metadata for most of these directives. They draw upon a global “context” that indicates how to get at a database connection (if any; migrations can dump SQL/DDL directives to files as well) in order to invoke the command. This global context is set up, like everything else, in the `env.py` script.

> [create_table()] 和 [drop_table()] 是 Alembic 指令。 Alembic 通过这些指令提供了所有基本的数据库迁移操作，这些指令设计得尽可能简单和简约； 大多数这些指令不依赖现有的表元数据。 它们利用一个全局“上下文”来指示如何获得数据库连接（如果有的话；迁移也可以将 SQL/DDL 指令转储到文件）以调用命令。 与其他所有内容一样，此全局上下文在 `env.py` 脚本中设置。

An overview of all Alembic directives is at [Operation Reference].

> 所有 Alembic 指令的概述位于 [操作参考]。
