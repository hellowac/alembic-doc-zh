# Working with Branches

**工作分支**

[Create a Migration Script]: ../zh/00_04_create_a_migration_script.md
[创建迁移脚本]:../zh/00_04_create_a_migration_script.md

A **branch** describes a point in a migration stream when two or more versions refer to the same parent migration as their anscestor. Branches occur naturally when two divergent source trees, both containing Alembic revision files created independently within those source trees, are merged together into one. When this occurs, the challenge of a branch is to **merge** the branches into a single series of changes, so that databases established from either source tree individually can be upgraded to reference the merged result equally. Another scenario where branches are present are when we create them directly; either at some point in the migration stream we’d like different series of migrations to be managed independently (e.g. we create a tree), or we’d like separate migration streams for different features starting at the root (e.g. a forest). We’ll illustrate all of these cases, starting with the most common which is a source-merge-originated branch that we’ll merge.

> 当两个或多个版本将相同的父迁移作为其祖先时，分支描述了迁移流中的一个点。当两个不同的源代码树（都包含在这些源代码树中独立创建的 Alembic 修订文件）合并为一个时，分支自然会出现。发生这种情况时，分支的挑战是将分支合并为一系列更改，以便从任一源树单独建立的数据库可以升级以平等地引用合并的结果。存在分支的另一种情况是我们直接创建它们时；要么在迁移流中的某个时刻，我们希望独立管理不同系列的迁移（例如，我们创建一棵树），要么我们希望从根开始（例如，森林）为不同的特征提供单独的迁移流。我们将说明所有这些情况，从最常见的开始，即我们将合并的源合并起源分支。

Starting with the “account table” example we began in **[Create a Migration Script]**, assume we have our basemost version `1975ea83b712`, which leads into the second revision `ae1027a6acf`, and the migration files for these two revisions are checked into our source repository. Consider if we merged into our source repository another code branch which contained a revision for another table called `shopping_cart`. This revision was made against our first Alembic revision, the one that generated `account`. After loading the second source tree in, a new file `27c6a30d7c24_add_shopping_cart_table.py` exists within our `versions` directory. Both it, as well as `ae1027a6acf_add_a_column.py`, reference `1975ea83b712_add_account_table.py` as the “downgrade” revision. To illustrate:

> 从我们在 **[创建迁移脚本]** 中开始的“帐户表”示例开始，假设我们有最基本的版本 `1975ea83b712`，它导致第二个修订版 `ae1027a6acf`，并且这两个修订版的迁移文件被签入我们的源存储库。 考虑如果我们将另一个代码分支合并到我们的源存储库中，其中包含另一个名为 `shopping_cart` 的表的修订。 此修订是针对我们的第一个 Alembic 修订进行的，即生成帐户的修订。 加载第二个源代码树后，我们的`版本目录`中存在一个新文件 `27c6a30d7c24_add_shopping_cart_table.py`。 它以及 `ae1027a6acf_add_a_column.py` 都将 `1975ea83b712_add_account_table.py` 引用为“降级”修订版。 为了显示：

```bash
# main source tree:
1975ea83b712 (create account table) -> ae1027a6acf (add a column)

# branched source tree
1975ea83b712 (create account table) -> 27c6a30d7c24 (add shopping cart table)
```

Above, we can see `1975ea83b712` is our **branch point**; two distinct versions both refer to it as its parent. The Alembic command `branches` illustrates this fact:

> 上面，我们可以看到 `1975ea83b712` 是我们的分支点； 两个不同的版本都将其称为其父级。 Alembic 命令 `branches` 说明了这一事实：

```bash
$ alembic branches --verbose
Rev: 1975ea83b712 (branchpoint)
Parent: <base>
Branches into: 27c6a30d7c24, ae1027a6acf
Path: foo/versions/1975ea83b712_add_account_table.py

    create account table

    Revision ID: 1975ea83b712
    Revises:
    Create Date: 2014-11-20 13:02:46.257104

             -> 27c6a30d7c24 (head), add shopping cart table
             -> ae1027a6acf (head), add a column
```

History shows it too, illustrating two `head` entries as well as a `branchpoint`:

> 历史也显示了这一点，说明了两个头条 `head` 和一个 `branchpoint`(分支点)：

```bash
$ alembic history
1975ea83b712 -> 27c6a30d7c24 (head), add shopping cart table
1975ea83b712 -> ae1027a6acf (head), add a column
<base> -> 1975ea83b712 (branchpoint), create account table
```

We can get a view of just the current heads using `alembic heads`:

> 我们可以使用 `alembic heads` 来查看当前的 heads：

```bash
$ alembic heads --verbose
Rev: 27c6a30d7c24 (head)
Parent: 1975ea83b712
Path: foo/versions/27c6a30d7c24_add_shopping_cart_table.py

    add shopping cart table

    Revision ID: 27c6a30d7c24
    Revises: 1975ea83b712
    Create Date: 2014-11-20 13:03:11.436407

Rev: ae1027a6acf (head)
Parent: 1975ea83b712
Path: foo/versions/ae1027a6acf_add_a_column.py

    add a column

    Revision ID: ae1027a6acf
    Revises: 1975ea83b712
    Create Date: 2014-11-20 13:02:54.849677
```

If we try to run an `upgrade` to the usual end target of `head`, Alembic no longer considers this to be an unambiguous command. As we have more than one `head`, the `upgrade` command wants us to provide more information:

> 如果我们尝试 `upgrade` 到通常的最终目标 `head` ，Alembic 不再认为这是一个明确的命令。 由于我们有多个`head`，`upgrade` 命令希望我们提供更多信息：

```bash
$ alembic upgrade head
  FAILED: Multiple head revisions are present for given argument 'head'; please specify a specific
  target revision, '<branchname>@head' to narrow to a specific head, or 'heads' for all heads
```

The `upgrade` command gives us quite a few options in which we can proceed with our `upgrade`, either giving it information on which head we’d like to `upgrade` towards, or alternatively stating that we’d like all heads to be upgraded towards at once. However, in the typical case of two source trees being merged, we will want to pursue a third option, which is that we can **merge** these branches.

> `upgrade` 命令为我们提供了很多选项，我们可以在其中继续进行`upgrade`，或者提供有关我们想要`upgrade`到哪个`head`的信息，或者说明我们希望同时升级所有`head`。 然而，在两个源代码树被合并的典型情况下，我们将要追求第三种选择，即我们可以合并这些分支。
