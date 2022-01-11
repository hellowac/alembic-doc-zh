# Branch Dependencies

When working with multiple roots, it is expected that these different revision streams will need to refer to one another. For example, a new revision in `networking` which needs to refer to the `account` table will want to establish 55af2cb1c267, add another `account` column, the last revision that works with the `account` table, as a dependency. From a graph perspective, this means nothing more that the new file will feature both 55af2cb1c267, add another `account` column and `29f859a13ea, add DNS table` as “down” revisions, and looks just as though we had merged these two branches together. However, we don’t want to consider these as “merged”; we want the two revision streams to remain independent, even though a version in `networking` is going to reach over into the other stream. To support this use case, Alembic provides a directive known as `depends_on`, which allows a revision file to refer to another as a “dependency”, very similar to an entry in `down_revision` from a graph perspective, but different from a semantic perspective.

> 当使用多个根时，预计这些不同的修订流将需要相互引用。例如，需要引用 `account` 表的 `networking` 中的新修订版将要建立 `55af2cb1c267`，添加另一个 `account` 列，即与 `account` 表一起使用的最后一个修订版，作为依赖项。从图表的角度来看，这仅意味着新文件将同时包含 `55af2cb1c267`，添加另一个“account”列和`29f859a13ea，添加 DNS 表`作为 “down” 修订，看起来就像我们将这两个分支合并在一起.但是，我们不想将这些视为“merge”；我们希望两个修订流保持独立，即使 `networking` 中的一个版本将延伸到另一个流。为了支持这个用例，Alembic 提供了一个名为 `depends_on` 的指令，它允许修订文件将另一个文件称为“依赖项”，从图形的角度来看，这与 `down_revision` 中的条目非常相似，但不同于语义看法。

To use `depends_on`, we can specify it as part of our `alembic revision` command:

> 要使用 `depends_on`，我们可以将其指定为 `alembic revision` 命令的一部分：

```bash
$ alembic revision -m "add ip account table" --head=networking@head  --depends-on=55af2cb1c267
  Generating /path/to/foo/model/networking/2a95102259be_add_ip_account_table.py ... done
```

Within our migration file, we’ll see this new directive present:

> 在我们的迁移文件中，我们将看到这个新指令：

```python
# revision identifiers, used by Alembic.
revision = '2a95102259be'
down_revision = '29f859a13ea'
branch_labels = None
depends_on='55af2cb1c267'
```

`depends_on` may be either a real revision number or a branch name. When specified at the command line, a resolution from a partial revision number will work as well. It can refer to any number of dependent revisions as well; for example, if we were to run the command:

> `depends_on` 可以是真实的修订号或分支名称。 当在命令行中指定时，部分修订号的解析也将起作用。 它也可以引用任意数量的相关修订； 例如，如果我们要运行命令：

```bash
$ alembic revision -m "add ip account table" \\
    --head=networking@head  \\
    --depends-on=55af2cb1c267 --depends-on=d747a --depends-on=fa445
  Generating /path/to/foo/model/networking/2a95102259be_add_ip_account_table.py ... done
```

We’d see inside the file:

> 我们会在文件中看到：

```python
# revision identifiers, used by Alembic.
revision = '2a95102259be'
down_revision = '29f859a13ea'
branch_labels = None
depends_on = ('55af2cb1c267', 'd747a8a8879', 'fa4456a9201')
```

We also can of course add or alter this value within the file manually after it is generated, rather than using the `--depends-on` argument.

> 我们当然也可以在文件生成后手动添加或更改此值，而不是使用 `--depends-on` 参数。

We can see the effect this directive has when we view the history of the `networking` branch in terms of “heads”, e.g., all the revisions that are descendants:

> 当我们以“heads”的形式查看“networking”分支的历史时，我们可以看到该指令的效果，例如，所有作为后代的修订：

```bash
$ alembic history -r :networking@head
29f859a13ea (55af2cb1c267) -> 2a95102259be (networking) (head), add ip account table
109ec7d132bf -> 29f859a13ea (networking), add DNS table
3cac04ae8714 -> 109ec7d132bf (networking), add ip number table
<base> -> 3cac04ae8714 (networking), create networking branch
ae1027a6acf -> 55af2cb1c267 (effective head), add another account column
1975ea83b712 -> ae1027a6acf, Add a column
<base> -> 1975ea83b712 (branchpoint), create account table
```

What we see is that the full history of the `networking` branch, in terms of an “upgrade” to the “head”, will include that the tree building up `55af2cb1c267, add another account column` will be pulled in first. Interstingly, we don’t see this displayed when we display history in the other direction, e.g. from `networking@base`:

> 我们看到的是，`networking` 分支的完整历史记录，就“upgrade”到“head”而言，将包括构建 `55af2cb1c267, add another account column` 的树将首先被拉入。 有趣的是，当我们在另一个方向显示历史记录时，我们看不到这一点，例如 来自`networking@base`：

```bash
$ alembic history -r networking@base:
29f859a13ea (55af2cb1c267) -> 2a95102259be (networking) (head), add ip account table
109ec7d132bf -> 29f859a13ea (networking), add DNS table
3cac04ae8714 -> 109ec7d132bf (networking), add ip number table
<base> -> 3cac04ae8714 (networking), create networking branch
```

The reason for the discrepancy is that displaying history from the base shows us what would occur if we ran a downgrade operation, instead of an upgrade. If we downgraded all the files in `networking` using `networking@base`, the dependencies aren’t affected, they’re left in place.

> 出现差异的原因是，显示基础的历史记录向我们展示了如果我们运行降级操作而不是升级会发生什么。 如果我们使用 `networking@base` 降级 `networking` 中的所有文件，则依赖关系不会受到影响，它们会保留在原处。

We also see something odd if we view `heads` at the moment:

> 如果我们现在查看 `heads`，我们也会看到一些奇怪的东西：

```bash
$ alembic heads
2a95102259be (networking) (head)
27c6a30d7c24 (shoppingcart) (head)
55af2cb1c267 (effective head)
```

The head file that we used as a “dependency”, `55af2cb1c267`, is displayed as an “effective” head, which we can see also in the history display earlier. What this means is that at the moment, if we were to upgrade all versions to the top, the `55af2cb1c267` revision number would not actually be present in the `alembic_version` table; this is because it does not have a branch of its own subsequent to the `2a95102259be` revision which depends on it:

> 我们用作“依赖”的head文件“55af2cb1c267”显示为 “effective” head，我们也可以在前面的历史显示中看到。 这意味着目前，如果我们将所有版本升级到顶部，则 `55af2cb1c267` 修订号实际上不会出现在 `alembic_version` 表中； 这是因为它在依赖于它的 `2a95102259be` 修订版之后没有自己的分支：

```bash
$ alembic upgrade heads
INFO  [alembic.migration] Running upgrade 29f859a13ea, 55af2cb1c267 -> 2a95102259be, add ip account table

$ alembic current
2a95102259be (head)
27c6a30d7c24 (head)
```

The entry is still displayed in `alembic heads` because Alembic knows that even though this revision isn’t a “real” head, it’s still something that we developers consider semantically to be a head, so it’s displayed, noting its special status so that we don’t get quite as confused when we don’t see it within `alembic current`.

> 该条目仍然显示在`alembic heads`中，因为 Alembic 知道即使此修订版不是“真正的”head，它仍然是我们开发人员在语义上认为是head的东西，所以它被显示，并指出它的特殊状态，以便当我们在“alembic current”中看不到它时，我们不会那么困惑。

If we add a new revision onto `55af2cb1c267`, the branch again becomes a “real” branch which can have its own entry in the database:

> 如果我们在 `55af2cb1c267` 上添加一个新版本，该分支再次成为一个“真正的”分支，它可以在数据库中拥有自己的条目：

```bash
$ alembic revision -m "more account changes" --head=55af2cb@head
  Generating /path/to/foo/versions/34e094ad6ef1_more_account_changes.py ... done

$ alembic upgrade heads
INFO  [alembic.migration] Running upgrade 55af2cb1c267 -> 34e094ad6ef1, more account changes

$ alembic current
2a95102259be (head)
27c6a30d7c24 (head)
34e094ad6ef1 (head)
```

For posterity, the revision tree now looks like:

> 对于后代，修订树现在看起来像：

```bash
$ alembic history
29f859a13ea (55af2cb1c267) -> 2a95102259be (networking) (head), add ip account table
109ec7d132bf -> 29f859a13ea (networking), add DNS table
3cac04ae8714 -> 109ec7d132bf (networking), add ip number table
<base> -> 3cac04ae8714 (networking), create networking branch
1975ea83b712 -> 27c6a30d7c24 (shoppingcart) (head), add shopping cart table
55af2cb1c267 -> 34e094ad6ef1 (head), more account changes
ae1027a6acf -> 55af2cb1c267, add another account column
1975ea83b712 -> ae1027a6acf, Add a column
<base> -> 1975ea83b712 (branchpoint), create account table


                    --- 27c6 --> d747 --> <head>
                   /   (shoppingcart)
<base> --> 1975 -->
                   \
                     --- ae10 --> 55af --> <head>
                                    ^
                                    +--------+ (dependency)
                                             |
                                             |
<base> --> 3782 -----> 109e ----> 29f8 ---> 2a95 --> <head>
         (networking)
```

If there’s any point to be made here, it’s if you are too freely branching, merging and labeling, things can get pretty crazy! Hence the branching system should be used carefully and thoughtfully for best results.

> 如果这里有什么要说的，那就是如果你过于自由地分支、合并和标记，事情会变得非常疯狂！ 因此，应谨慎使用分支系统以获得最佳结果。
