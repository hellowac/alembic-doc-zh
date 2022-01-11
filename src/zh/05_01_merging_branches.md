# Merging Branches

**合并分支**

[Operations]: ../zh/06_01_operations.md

An Alembic merge is a migration file that joins two or more “head” files together. If the two branches we have right now can be said to be a “tree” structure, introducing this merge file will turn it into a “diamond” structure:

> Alembic 合并是将两个或多个 “head” 文件连接在一起的迁移文件。 如果我们现在的两个分支可以说是一个 “tree” 结构，那么引入这个合并文件就会变成一个 “diamond”（菱形）结构：

```text
                            -- ae1027a6acf -->
                           /                   \
<base> --> 1975ea83b712 -->                      --> mergepoint
                           \                   /
                            -- 27c6a30d7c24 -->
```

We create the merge file using `alembic merge`; with this command, we can pass to it an argument such as `heads`, meaning we’d like to merge all `heads`. Or, we can pass it individual revision numbers sequentally:

> 我们使用 `alembic merge` 创建合并文件； 使用这个命令，我们可以向它传递一个参数，例如 `heads`，这意味着我们想要合并所有的 `heads`。 或者，我们可以依次传递单独的修订号：

```bash
$ alembic merge -m "merge ae1 and 27c" ae1027 27c6a
  Generating /path/to/foo/versions/53fffde5ad5_merge_ae1_and_27c.py ... done
```

Looking inside the new file, we see it as a regular migration file, with the only new twist is that `down_revision` points to both revisions:

> 查看新文件，我们将其视为常规迁移文件，唯一的新变化是 `down_revision` 指向两个修订版：

```python
"""merge ae1 and 27c

Revision ID: 53fffde5ad5
Revises: ae1027a6acf, 27c6a30d7c24
Create Date: 2014-11-20 13:31:50.811663

"""

# revision identifiers, used by Alembic.
revision = '53fffde5ad5'
down_revision = ('ae1027a6acf', '27c6a30d7c24')
branch_labels = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    pass


def downgrade():
    pass
```

This file is a regular migration file, and if we wish to, we may place **[Operations]** directives into the `upgrade()` and `downgrade()` functions like any other migration file. Though it is probably best to limit the instructions placed here only to those that deal with any kind of reconciliation that is needed between the two merged branches, if any.

> 这个文件是一个常规的迁移文件，如果我们愿意，我们可以像任何其他迁移文件一样将操作指令放入 `upgrade()` 和 `downgrade()` 函数中。 尽管最好将此处的说明限制为仅处理两个合并分支之间所需的任何类型的协调（如果有）的说明。

The `heads` command now illustrates that the multiple `heads` in our `versions/` directory have been resolved into our new head:

> 现在，`heads` 命令说明我们的 `versions/` 目录中的多个`heads` 已被解析为我们的新 `head`：

```bash
$ alembic heads --verbose
Rev: 53fffde5ad5 (head) (mergepoint)
Merges: ae1027a6acf, 27c6a30d7c24
Path: foo/versions/53fffde5ad5_merge_ae1_and_27c.py

    merge ae1 and 27c

    Revision ID: 53fffde5ad5
    Revises: ae1027a6acf, 27c6a30d7c24
    Create Date: 2014-11-20 13:31:50.811663
```

History shows a similar result, as the mergepoint becomes our head:

> 历史显示了类似的结果，因为合并点成为我们的 `head` ：

```bash
$ alembic history
ae1027a6acf, 27c6a30d7c24 -> 53fffde5ad5 (head) (mergepoint), merge ae1 and 27c
1975ea83b712 -> ae1027a6acf, add a column
1975ea83b712 -> 27c6a30d7c24, add shopping cart table
<base> -> 1975ea83b712 (branchpoint), create account table
```

With a single `head` target, a generic `upgrade` can proceed:

> 使用单个`head`目标，可以进行通用 `upgrade`：

```bash
$ alembic upgrade head
INFO  [alembic.migration] Context impl PostgresqlImpl.
INFO  [alembic.migration] Will assume transactional DDL.
INFO  [alembic.migration] Running upgrade  -> 1975ea83b712, create account table
INFO  [alembic.migration] Running upgrade 1975ea83b712 -> 27c6a30d7c24, add shopping cart table
INFO  [alembic.migration] Running upgrade 1975ea83b712 -> ae1027a6acf, add a column
INFO  [alembic.migration] Running upgrade ae1027a6acf, 27c6a30d7c24 -> 53fffde5ad5, merge ae1 and 27c
```
----

## merge mechanics

**合并机制**

The upgrade process traverses through all of our migration files using a **topological sorting** algorithm, treating the list of migration files not as a linked list, but as a directed acyclic graph. The starting points of this traversal are the **current heads** within our database, and the end point is the “head” revision or revisions specified.

> 升级过程使用 **拓扑排序** 算法遍历我们所有的迁移文件，将迁移文件列表不作为链表，而是作为有向无环图。 此遍历的起点是我们数据库中的 **current heads**，终点是“head”修订版或指定的修订版。

When a migration proceeds across a point at which there are multiple heads, the `alembic_version` table will at that point store multiple rows, one for each head. Our migration process above will emit SQL against `alembic_version` along these lines:

> 当迁移跨越一个有多个`head`的点时，`alembic_version` 表将在该点存储多行，每个 `head` 一个。 我们上面的迁移过程将按照以下几行针对 `alembic_version` 发出 SQL：

```bash
-- Running upgrade  -> 1975ea83b712, create account table
INSERT INTO alembic_version (version_num) VALUES ('1975ea83b712')

-- Running upgrade 1975ea83b712 -> 27c6a30d7c24, add shopping cart table
UPDATE alembic_version SET version_num='27c6a30d7c24' WHERE alembic_version.version_num = '1975ea83b712'

-- Running upgrade 1975ea83b712 -> ae1027a6acf, add a column
INSERT INTO alembic_version (version_num) VALUES ('ae1027a6acf')

-- Running upgrade ae1027a6acf, 27c6a30d7c24 -> 53fffde5ad5, merge ae1 and 27c
DELETE FROM alembic_version WHERE alembic_version.version_num = 'ae1027a6acf'
UPDATE alembic_version SET version_num='53fffde5ad5' WHERE alembic_version.version_num = '27c6a30d7c24'
```

At the point at which both `27c6a30d7c24` and `ae1027a6acf` exist within our database, both values are present in `alembic_version`, which now has two rows. If we upgrade to these two versions alone, then stop and run `alembic current`, we will see this:

> 在我们的数据库中同时存在 `27c6a30d7c24` 和 `ae1027a6acf` 时，这两个值都存在于 `alembic_version` 中，现在它有两行。 如果我们单独升级到这两个版本，然后停止并运行 `alembic current`，我们将看到：

```bash
$ alembic current --verbose
Current revision(s) for postgresql://scott:XXXXX@localhost/test:
Rev: ae1027a6acf
Parent: 1975ea83b712
Path: foo/versions/ae1027a6acf_add_a_column.py

    add a column

    Revision ID: ae1027a6acf
    Revises: 1975ea83b712
    Create Date: 2014-11-20 13:02:54.849677

Rev: 27c6a30d7c24
Parent: 1975ea83b712
Path: foo/versions/27c6a30d7c24_add_shopping_cart_table.py

    add shopping cart table

    Revision ID: 27c6a30d7c24
    Revises: 1975ea83b712
    Create Date: 2014-11-20 13:03:11.436407
```

A key advantage to the `merge` process is that it will run equally well on databases that were present on version `ae1027a6acf` alone, versus databases that were present on version `27c6a30d7c24` alone; whichever version was not yet applied, will be applied before the `merge` point can be crossed. This brings forth a way of thinking about a `merge` file, as well as about any Alembic revision file. As they are considered to be “nodes” within a set that is subject to topological sorting, each “node” is a point that cannot be crossed until all of its dependencies are satisfied.

> **合并**过程的一个关键优势是，它在单独存在于 `ae1027a6acf` 版本上的数据库上与单独存在于版本 `27c6a30d7c24` 上的数据库上运行同样好； 无论哪个版本尚未应用，都将在可以跨越合并点之前应用。 这带来了一种考虑合并文件以及任何 Alembic 修订文件的方式。 由于它们被认为是受拓扑排序的集合中的“节点”，因此每个“节点”都是一个点，在满足其所有依赖关系之前无法跨越。

Prior to Alembic’s support of merge points, the use case of databases sitting on different heads was basically impossible to reconcile; having to manually splice the head files together invariably meant that one migration would occur before the other, thus being incompatible with databases that were present on the other migration.

> 在 Alembic 支持合并点之前，数据库位于不同头部的用例基本上是无法协调的； 必须手动将头文件拼接在一起, 意味着一个迁移将在另一个迁移之前发生，因此与另一个迁移中存在的数据库不兼容。
