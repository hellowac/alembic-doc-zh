# Branch Dependencies

When working with multiple roots, it is expected that these different revision streams will need to refer to one another. For example, a new revision in `networking` which needs to refer to the `account` table will want to establish 55af2cb1c267, add another `account` column, the last revision that works with the `account` table, as a dependency. From a graph perspective, this means nothing more that the new file will feature both 55af2cb1c267, add another `account` column and `29f859a13ea, add DNS table` as “down” revisions, and looks just as though we had merged these two branches together. However, we don’t want to consider these as “merged”; we want the two revision streams to remain independent, even though a version in `networking` is going to reach over into the other stream. To support this use case, Alembic provides a directive known as `depends_on`, which allows a revision file to refer to another as a “dependency”, very similar to an entry in `down_revision` from a graph perspective, but different from a semantic perspective.

To use `depends_on`, we can specify it as part of our `alembic revision` command:

```bash
$ alembic revision -m "add ip account table" --head=networking@head  --depends-on=55af2cb1c267
  Generating /path/to/foo/model/networking/2a95102259be_add_ip_account_table.py ... done
```

Within our migration file, we’ll see this new directive present:

```python
# revision identifiers, used by Alembic.
revision = '2a95102259be'
down_revision = '29f859a13ea'
branch_labels = None
depends_on='55af2cb1c267'
```

`depends_on` may be either a real revision number or a branch name. When specified at the command line, a resolution from a partial revision number will work as well. It can refer to any number of dependent revisions as well; for example, if we were to run the command:

```bash
$ alembic revision -m "add ip account table" \\
    --head=networking@head  \\
    --depends-on=55af2cb1c267 --depends-on=d747a --depends-on=fa445
  Generating /path/to/foo/model/networking/2a95102259be_add_ip_account_table.py ... done
```

We’d see inside the file:

```python
# revision identifiers, used by Alembic.
revision = '2a95102259be'
down_revision = '29f859a13ea'
branch_labels = None
depends_on = ('55af2cb1c267', 'd747a8a8879', 'fa4456a9201')
```

We also can of course add or alter this value within the file manually after it is generated, rather than using the `--depends-on` argument.

We can see the effect this directive has when we view the history of the `networking` branch in terms of “heads”, e.g., all the revisions that are descendants:

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

```bash
$ alembic history -r networking@base:
29f859a13ea (55af2cb1c267) -> 2a95102259be (networking) (head), add ip account table
109ec7d132bf -> 29f859a13ea (networking), add DNS table
3cac04ae8714 -> 109ec7d132bf (networking), add ip number table
<base> -> 3cac04ae8714 (networking), create networking branch
```

The reason for the discrepancy is that displaying history from the base shows us what would occur if we ran a downgrade operation, instead of an upgrade. If we downgraded all the files in `networking` using `networking@base`, the dependencies aren’t affected, they’re left in place.

We also see something odd if we view `heads` at the moment:

```bash
$ alembic heads
2a95102259be (networking) (head)
27c6a30d7c24 (shoppingcart) (head)
55af2cb1c267 (effective head)
```

The head file that we used as a “dependency”, `55af2cb1c267`, is displayed as an “effective” head, which we can see also in the history display earlier. What this means is that at the moment, if we were to upgrade all versions to the top, the `55af2cb1c267` revision number would not actually be present in the `alembic_version` table; this is because it does not have a branch of its own subsequent to the `2a95102259be` revision which depends on it:

```bash
$ alembic upgrade heads
INFO  [alembic.migration] Running upgrade 29f859a13ea, 55af2cb1c267 -> 2a95102259be, add ip account table

$ alembic current
2a95102259be (head)
27c6a30d7c24 (head)
```

The entry is still displayed in `alembic heads` because Alembic knows that even though this revision isn’t a “real” head, it’s still something that we developers consider semantically to be a head, so it’s displayed, noting its special status so that we don’t get quite as confused when we don’t see it within `alembic current`.

If we add a new revision onto `55af2cb1c267`, the branch again becomes a “real” branch which can have its own entry in the database:

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
