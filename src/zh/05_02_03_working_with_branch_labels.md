# Working with Branch Labels

**使用分支标注**

To satisfy the use case where an environment has long-lived branches, especially independent branches as will be discussed in the next section, Alembic supports the concept of branch labels. These are string values that are present within the migration file, using the new identifier `branch_labels`. For example, if we want to refer to the “shopping cart” branch using the name “shoppingcart”, we can add that name to our file `27c6a30d7c24_add_shopping_cart_table.py`:

> 为了满足环境具有长期存在的分支的用例，尤其是下一节将讨论的独立分支，Alembic 支持分支标签的概念。 这些是迁移文件中存在的字符串值，使用新的标识符 `branch_labels`。 例如，如果我们想使用名称“shopping cart”来引用“购物车”分支，我们可以将该名称添加到我们的文件 `27c6a30d7c24_add_shopping_cart_table.py` 中：

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

> `branch_labels` 属性指的是字符串名称或名称元组，现在将应用于此修订版、此修订版的所有后代，以及此修订版的所有祖先，直到前一个分支点，在本例中为 `1975ea83b712`。 我们可以看到应用于此修订版的 `shoppingcart` 标签：

```bash
$ alembic history
1975ea83b712 -> 27c6a30d7c24 (shoppingcart) (head), add shopping cart table
1975ea83b712 -> ae1027a6acf (head), add a column
<base> -> 1975ea83b712 (branchpoint), create account table
```

With the label applied, the name `shoppingcart` now serves as an alias for the `27c6a30d7c24` revision specifically. We can illustrate this by showing it with `alembic show`:

> 应用标签后，名称 `shoppingcart` 现在专门用作 `27c6a30d7c24` 修订版的别名。 我们可以通过 `alembic show` 展示它来说明这一点：

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

> 但是，在使用分支标签时，我们通常希望使用一种称为 “branch at” 的语法来使用它们； 这种语法允许我们声明我们想要使用一个特定的修订，比如说一个 “head” 修订，就特定的分支而言。 虽然通常情况下，当有多个 `head` 时，我们不能引用 `alembic upgrade head`，但我们可以使用 `shoppingcart@head` 语法专门引用这个 `head` ：

```bash
$ alembic upgrade shoppingcart@head
INFO  [alembic.migration] Running upgrade 1975ea83b712 -> 27c6a30d7c24, add shopping cart table
```

The `shoppingcart@head` syntax becomes important to us if we wish to add new migration files to our versions directory while maintaining multiple branches. Just like the `upgrade` command, if we attempted to add a new revision file to our multiple-heads layout without a specific parent revision, we’d get a familiar error:

> 如果我们希望在维护多个分支的同时将新的迁移文件添加到版本目录中，`shoppingcart@head` 语法对我们来说变得很重要。 就像 `upgrade` 命令一样，如果我们试图在没有特定父版本的情况下向多头布局添加新的版本文件，我们会得到一个熟悉的错误：

```bash
$ alembic revision -m "add a shopping cart column"
  FAILED: Multiple heads are present; please specify the head revision on
  which the new revision should be based, or perform a merge.
```

The `alembic revision` command is pretty clear in what we need to do; to add our new revision specifically to the `shoppingcart` branch, we use the `--head` argument, either with the specific revision identifier `27c6a30d7c24`, or more generically using our branchname `shoppingcart@head`:

> `alembic revision` 命令非常清楚我们需要做什么； 为了将我们的新版本专门添加到 `shoppingcart` 分支，我们使用 `--head` 参数，或者使用特定的版本标识符 `27c6a30d7c24`，或者更一般地使用我们的分支名称 `shoppingcart@head`：

```bash
$ alembic revision -m "add a shopping cart column"  --head shoppingcart@head
  Generating /path/to/foo/versions/d747a8a8879_add_a_shopping_cart_column.py ... done
```

`alembic history` shows both files now part of the `shoppingcart` branch:

> `alembic history` 显示两个文件现在都属于 `shoppingcart` 分支：

```bash
$ alembic history
1975ea83b712 -> ae1027a6acf (head), add a column
27c6a30d7c24 -> d747a8a8879 (shoppingcart) (head), add a shopping cart column
1975ea83b712 -> 27c6a30d7c24 (shoppingcart), add shopping cart table
<base> -> 1975ea83b712 (branchpoint), create account table
```

We can limit our history operation just to this branch as well:

> 我们也可以将历史操作限制在这个分支上：

```bash
$ alembic history -r shoppingcart:
27c6a30d7c24 -> d747a8a8879 (shoppingcart) (head), add a shopping cart column
1975ea83b712 -> 27c6a30d7c24 (shoppingcart), add shopping cart table
```

If we want to illustrate the path of `shoppingcart` all the way from the base, we can do that as follows:

> 如果我们想说明 `shoppingcart` 从 base 开始的路径，我们可以这样做：

```bash
$ alembic history -r :shoppingcart@head
27c6a30d7c24 -> d747a8a8879 (shoppingcart) (head), add a shopping cart column
1975ea83b712 -> 27c6a30d7c24 (shoppingcart), add shopping cart table
<base> -> 1975ea83b712 (branchpoint), create account table
```

We can run this operation from the “base” side as well, but we get a different result:

> 我们也可以从“base”端运行这个操作，但是我们得到了不同的结果：

```bash$ alembic history -r shoppingcart@base:
1975ea83b712 -> ae1027a6acf (head), add a column
27c6a30d7c24 -> d747a8a8879 (shoppingcart) (head), add a shopping cart column
1975ea83b712 -> 27c6a30d7c24 (shoppingcart), add shopping cart table
<base> -> 1975ea83b712 (branchpoint), create account table
```

When we list from `shoppingcart@base` without an endpoint, it’s really shorthand for -r `shoppingcart@base`:heads, e.g. all heads, and since `shoppingcart@base` is the same “base” shared by the `ae1027a6acf` revision, we get that revision in our listing as well. The `<branchname>@base` syntax can be useful when we are dealing with individual bases, as we’ll see in the next section.

> 当我们从 `shoppingcart@base` 列出没有端点时，它实际上是 -r `shoppingcart@base`:heads 的简写，例如 所有的head，因为 `shoppingcart@base` 是 `ae1027a6acf` 修订版共享的同一个“基础”，我们也可以在我们的清单中获得该修订版。 `<branchname>@base` 语法在我们处理单个碱基时很有用，我们将在下一节中看到。

The `<branchname>@head` format can also be used with revision numbers instead of branch names, though this is less convenient. If we wanted to add a new revision to our branch that includes the un-labeled `ae1027a6acf`, if this weren’t a head already, we could ask for the “head of the branch that includes ae1027a6acf” as follows:

> `<branchname>@head` 格式也可以与修订号一起使用，而不是分支名称，尽管这样不太方便。 如果我们想向我们的分支添加一个包含未标记的 `ae1027a6acf` 的新修订，如果这还不是一个head，我们可以要求“包含 ae1027a6acf 的分支的head”，如下所示：

```bash
$ alembic revision -m "add another account column" --head ae10@head
  Generating /path/to/foo/versions/55af2cb1c267_add_another_account_column.py ... done
```
