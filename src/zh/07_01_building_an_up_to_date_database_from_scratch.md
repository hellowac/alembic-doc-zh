# Building an Up to Date Database from Scratch

**从头开始构建最新的数据库**

[create_all()]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.MetaData.create_all

There’s a theory of database migrations that says that the revisions in existence for a database should be able to go from an entirely blank schema to the finished product, and back again. Alembic can roll this way. Though we think it’s kind of overkill, considering that SQLAlchemy itself can emit the full CREATE statements for any given model using **[create_all()]**. If you check out a copy of an application, running this will give you the entire database in one shot, without the need to run through all those migration files, which are instead tailored towards applying incremental changes to an existing database.

> 有一种数据库迁移理论认为，数据库的现有修订应该能够从完全空白的模式转移到成品，然后再返回。 Alembic 可以这样滚动。 尽管我们认为这有点矫枉过正，但考虑到 SQLAlchemy 本身可以使用 **[create_all()]** 为任何给定模型发出完整的 CREATE 语句。 如果您检查一个应用程序的副本，运行它将一次性为您提供整个数据库，而无需运行所有这些迁移文件，这些迁移文件是针对对现有数据库应用增量更改而量身定制的。

Alembic can integrate with a **[create_all()]** script quite easily. After running the create operation, tell Alembic to create a new version table, and to stamp it with the most recent revision (i.e. `head`):

> Alembic 可以很容易地与 **[create_all()]** 脚本集成。 运行 `create` 操作后，告诉 `Alembic` 创建一个新的版本表，并用最新的修订（即 `head`）标记它：

```python
# inside of a "create the database" script, first create
# tables:
# 在“创建数据库”脚本中，首先创建表
my_metadata.create_all(engine)

# then, load the Alembic configuration and generate the
# version table, "stamping" it with the most recent rev:
# 然后，加载 Alembic 配置并生成版本表，用最新版本“标记”它：
from alembic.config import Config
from alembic import command
alembic_cfg = Config("/path/to/yourapp/alembic.ini")
command.stamp(alembic_cfg, "head")
```

When this approach is used, the application can generate the database using normal SQLAlchemy techniques instead of iterating through hundreds of migration scripts. Now, the purpose of the migration scripts is relegated just to movement between versions on out-of-date databases, not new databases. You can now remove old migration files that are no longer represented on any existing environments.

> 当使用这种方法时，应用程序可以使用普通的 SQLAlchemy 技术生成数据库，而不是遍历数百个迁移脚本。 现在，迁移脚本的目的仅是在过期数据库上的版本之间移动，而不是在新数据库上移动。 您现在可以删除不再存在于任何现有环境中的旧迁移文件。

To prune old migration files, simply delete the files. Then, in the earliest, still-remaining migration file, set `down_revision` to `None`:

> 要修剪旧的迁移文件，只需删除这些文件。 然后，在最早的、仍然存在的迁移文件中，将 `down_revision` 设置为 `None`：

```python
# replace this:
#down_revision = '290696571ad2'

# with this:
down_revision = None
```

That file now becomes the “base” of the migration series.

> 该文件现在成为迁移系列的 **“base”**。
