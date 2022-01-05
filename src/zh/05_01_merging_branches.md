# Merging Branches

**合并分支**

[Operations]: ../en/ops.html#alembic.operations.Operations

An Alembic merge is a migration file that joins two or more “head” files together. If the two branches we have right now can be said to be a “tree” structure, introducing this merge file will turn it into a “diamond” structure:

```text
                            -- ae1027a6acf -->
                           /                   \
<base> --> 1975ea83b712 -->                      --> mergepoint
                           \                   /
                            -- 27c6a30d7c24 -->
```

We create the merge file using alembic merge; with this command, we can pass to it an argument such as `heads`, meaning we’d like to merge all `heads`. Or, we can pass it individual revision numbers sequentally:

```bash
$ alembic merge -m "merge ae1 and 27c" ae1027 27c6a
  Generating /path/to/foo/versions/53fffde5ad5_merge_ae1_and_27c.py ... done
```

Looking inside the new file, we see it as a regular migration file, with the only new twist is that `down_revision` points to both revisions:

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

The `heads` command now illustrates that the multiple `heads` in our `versions/` directory have been resolved into our new head:

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

```bash
$ alembic history
ae1027a6acf, 27c6a30d7c24 -> 53fffde5ad5 (head) (mergepoint), merge ae1 and 27c
1975ea83b712 -> ae1027a6acf, add a column
1975ea83b712 -> 27c6a30d7c24, add shopping cart table
<base> -> 1975ea83b712 (branchpoint), create account table
```

With a single `head` target, a generic `upgrade` can proceed:

```bash
$ alembic upgrade head
INFO  [alembic.migration] Context impl PostgresqlImpl.
INFO  [alembic.migration] Will assume transactional DDL.
INFO  [alembic.migration] Running upgrade  -> 1975ea83b712, create account table
INFO  [alembic.migration] Running upgrade 1975ea83b712 -> 27c6a30d7c24, add shopping cart table
INFO  [alembic.migration] Running upgrade 1975ea83b712 -> ae1027a6acf, add a column
INFO  [alembic.migration] Running upgrade ae1027a6acf, 27c6a30d7c24 -> 53fffde5ad5, merge ae1 and 27c
```

**merge mechanics**

The upgrade process traverses through all of our migration files using a **topological sorting** algorithm, treating the list of migration files not as a linked list, but as a directed acyclic graph. The starting points of this traversal are the **current heads** within our database, and the end point is the “head” revision or revisions specified.

When a migration proceeds across a point at which there are multiple heads, the `alembic_version` table will at that point store multiple rows, one for each head. Our migration process above will emit SQL against `alembic_version` along these lines:

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

Prior to Alembic’s support of merge points, the use case of databases sitting on different heads was basically impossible to reconcile; having to manually splice the head files together invariably meant that one migration would occur before the other, thus being incompatible with databases that were present on the other migration.
