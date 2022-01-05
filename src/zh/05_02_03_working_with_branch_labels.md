# Working with Branch Labels

**使用分支标注**

To satisfy the use case where an environment has long-lived branches, especially independent branches as will be discussed in the next section, Alembic supports the concept of branch labels. These are string values that are present within the migration file, using the new identifier `branch_labels`. For example, if we want to refer to the “shopping cart” branch using the name “shoppingcart”, we can add that name to our file `27c6a30d7c24_add_shopping_cart_table.py`:

```python
"""add shopping cart table

"""

# revision identifiers, used by Alembic.
revision = '27c6a30d7c24'
down_revision = '1975ea83b712'
branch_labels = ('shoppingcart',)

# ...
```

The `branch_labels` attribute refers to a string name, or a tuple of names, which will now apply to this revision, all descendants of this revision, as well as all ancestors of this revision up until the preceding branch point, in this case `1975ea83b712`. We can see the `shoppingcart` label applied to this revision:

```bash
$ alembic history
1975ea83b712 -> 27c6a30d7c24 (shoppingcart) (head), add shopping cart table
1975ea83b712 -> ae1027a6acf (head), add a column
<base> -> 1975ea83b712 (branchpoint), create account table
```

With the label applied, the name `shoppingcart` now serves as an alias for the `27c6a30d7c24` revision specifically. We can illustrate this by showing it with `alembic show`:

```bash
$ alembic show shoppingcart
Rev: 27c6a30d7c24 (head)
Parent: 1975ea83b712
Branch names: shoppingcart
Path: foo/versions/27c6a30d7c24_add_shopping_cart_table.py

    add shopping cart table

    Revision ID: 27c6a30d7c24
    Revises: 1975ea83b712
    Create Date: 2014-11-20 13:03:11.436407
```

However, when using branch labels, we usually want to use them using a syntax known as “branch at” syntax; this syntax allows us to state that we want to use a specific revision, let’s say a “head” revision, in terms of a specific branch. While normally, we can’t refer to `alembic upgrade head` when there’s multiple heads, we can refer to this head specifcally using `shoppingcart@head` syntax:

```bash
$ alembic upgrade shoppingcart@head
INFO  [alembic.migration] Running upgrade 1975ea83b712 -> 27c6a30d7c24, add shopping cart table
```

The `shoppingcart@head` syntax becomes important to us if we wish to add new migration files to our versions directory while maintaining multiple branches. Just like the `upgrade` command, if we attempted to add a new revision file to our multiple-heads layout without a specific parent revision, we’d get a familiar error:

```bash
$ alembic revision -m "add a shopping cart column"
  FAILED: Multiple heads are present; please specify the head revision on
  which the new revision should be based, or perform a merge.
```

The `alembic revision` command is pretty clear in what we need to do; to add our new revision specifically to the `shoppingcart` branch, we use the `--head` argument, either with the specific revision identifier `27c6a30d7c24`, or more generically using our branchname `shoppingcart@head`:

```bash
$ alembic revision -m "add a shopping cart column"  --head shoppingcart@head
  Generating /path/to/foo/versions/d747a8a8879_add_a_shopping_cart_column.py ... done
```

alembic history shows both files now part of the `shoppingcart` branch:

```bash
$ alembic history
1975ea83b712 -> ae1027a6acf (head), add a column
27c6a30d7c24 -> d747a8a8879 (shoppingcart) (head), add a shopping cart column
1975ea83b712 -> 27c6a30d7c24 (shoppingcart), add shopping cart table
<base> -> 1975ea83b712 (branchpoint), create account table
```

We can limit our history operation just to this branch as well:

```bash
$ alembic history -r shoppingcart:
27c6a30d7c24 -> d747a8a8879 (shoppingcart) (head), add a shopping cart column
1975ea83b712 -> 27c6a30d7c24 (shoppingcart), add shopping cart table
```

If we want to illustrate the path of `shoppingcart` all the way from the base, we can do that as follows:

```bash
$ alembic history -r :shoppingcart@head
27c6a30d7c24 -> d747a8a8879 (shoppingcart) (head), add a shopping cart column
1975ea83b712 -> 27c6a30d7c24 (shoppingcart), add shopping cart table
<base> -> 1975ea83b712 (branchpoint), create account table
```

We can run this operation from the “base” side as well, but we get a different result:

```bash$ alembic history -r shoppingcart@base:
1975ea83b712 -> ae1027a6acf (head), add a column
27c6a30d7c24 -> d747a8a8879 (shoppingcart) (head), add a shopping cart column
1975ea83b712 -> 27c6a30d7c24 (shoppingcart), add shopping cart table
<base> -> 1975ea83b712 (branchpoint), create account table
```

When we list from `shoppingcart@base` without an endpoint, it’s really shorthand for -r `shoppingcart@base`:heads, e.g. all heads, and since `shoppingcart@base` is the same “base” shared by the `ae1027a6acf` revision, we get that revision in our listing as well. The `<branchname>@base` syntax can be useful when we are dealing with individual bases, as we’ll see in the next section.

The `<branchname>@head` format can also be used with revision numbers instead of branch names, though this is less convenient. If we wanted to add a new revision to our branch that includes the un-labeled `ae1027a6acf`, if this weren’t a head already, we could ask for the “head of the branch that includes ae1027a6acf” as follows:

```bash
$ alembic revision -m "add another account column" --head ae10@head
  Generating /path/to/foo/versions/55af2cb1c267_add_another_account_column.py ... done
```
