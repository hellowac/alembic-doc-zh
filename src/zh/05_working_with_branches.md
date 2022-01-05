# Working with Branches

**工作分支**

[Create a Migration Script]: ../en/tutorial.html#create-migration

A **branch** describes a point in a migration stream when two or more versions refer to the same parent migration as their anscestor. Branches occur naturally when two divergent source trees, both containing Alembic revision files created independently within those source trees, are merged together into one. When this occurs, the challenge of a branch is to **merge** the branches into a single series of changes, so that databases established from either source tree individually can be upgraded to reference the merged result equally. Another scenario where branches are present are when we create them directly; either at some point in the migration stream we’d like different series of migrations to be managed independently (e.g. we create a tree), or we’d like separate migration streams for different features starting at the root (e.g. a forest). We’ll illustrate all of these cases, starting with the most common which is a source-merge-originated branch that we’ll merge.

Starting with the “account table” example we began in **[Create a Migration Script]**, assume we have our basemost version `1975ea83b712`, which leads into the second revision `ae1027a6acf`, and the migration files for these two revisions are checked into our source repository. Consider if we merged into our source repository another code branch which contained a revision for another table called `shopping_cart`. This revision was made against our first Alembic revision, the one that generated `account`. After loading the second source tree in, a new file `27c6a30d7c24_add_shopping_cart_table.py` exists within our `versions` directory. Both it, as well as `ae1027a6acf_add_a_column.py`, reference `1975ea83b712_add_account_table.py` as the “downgrade” revision. To illustrate:

```bash
# main source tree:
1975ea83b712 (create account table) -> ae1027a6acf (add a column)

# branched source tree
1975ea83b712 (create account table) -> 27c6a30d7c24 (add shopping cart table)
```

Above, we can see `1975ea83b712` is our **branch point**; two distinct versions both refer to it as its parent. The Alembic command `branches` illustrates this fact:

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

```bash
$ alembic history
1975ea83b712 -> 27c6a30d7c24 (head), add shopping cart table
1975ea83b712 -> ae1027a6acf (head), add a column
<base> -> 1975ea83b712 (branchpoint), create account table
```

We can get a view of just the current heads using `alembic heads`:

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

```bash
$ alembic upgrade head
  FAILED: Multiple head revisions are present for given argument 'head'; please specify a specific
  target revision, '<branchname>@head' to narrow to a specific head, or 'heads' for all heads
```

The `upgrade` command gives us quite a few options in which we can proceed with our `upgrade`, either giving it information on which head we’d like to `upgrade` towards, or alternatively stating that we’d like all heads to be upgraded towards at once. However, in the typical case of two source trees being merged, we will want to pursue a third option, which is that we can **merge** these branches.
