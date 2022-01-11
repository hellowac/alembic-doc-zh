# Running with Multiple Bases

**基于多个base运行**

Once we have a new, permanent (for as long as we desire it to be) base in our system, we’ll always have multiple heads present:

> 一旦我们在我们的系统中有一个新的、永久的（只要我们希望它是）base，我们就会一直有多个head：

```bash
$ alembic heads
3cac04ae8714 (networking) (head)
27c6a30d7c24 (shoppingcart) (head)
ae1027a6acf (head)

```

When we want to add a new revision file to `networking`, we specify `networking@head` as the `--head`. The appropriate version directory is now selected automatically based on the head we choose:

> 当我们想向 `networking` 添加一个新的修订文件时，我们将 `networking@head` 指定为 `--head`。 现在根据我们选择的头自动选择适当的版本目录：

```bash
$ alembic revision -m "add ip number table" --head=networking@head
  Generating /path/to/foo/model/networking/109ec7d132bf_add_ip_number_table.py ... done
```

It’s important that we refer to the head using networking@head; if we only refer to `networking`, that refers to only `3cac04ae8714` specifically; if we specify this and it’s not a head, `alembic revision` will make sure we didn’t mean to specify the head:

> 重要的是我们使用 networking@head 来引用 head ； 如果我们只指 `networking`，那具体指的是 `3cac04ae8714`； 如果我们指定这个并且它不是一个头，`alembic revision` 将确保我们不是要指定头：

```bash
$ alembic revision -m "add DNS table" --head=networking
  FAILED: Revision 3cac04ae8714 is not a head revision; please
  specify --splice to create a new branch from this revision
```

As mentioned earlier, as this base is independent, we can view its history from the base using `history -r networking@base:`:

> 如前所述，由于这个base是独立的，我们可以使用`history -r networking@base:`从base查看它的历史：

```bash
$ alembic history -r networking@base:
109ec7d132bf -> 29f859a13ea (networking) (head), add DNS table
3cac04ae8714 -> 109ec7d132bf (networking), add ip number table
<base> -> 3cac04ae8714 (networking), create networking branch
```

At the moment, this is the same output we’d get at this point if we used `-r :networking@head`. However, that will change later on as we use additional directives.

> 目前，如果我们使用 `-r :networking@head`，这与我们此时得到的输出相同。 然而，随着我们使用额外的指令，这将在稍后改变。

We may now run upgrades or downgrades freely, among individual branches (let’s assume a clean database again):

> 我们现在可以在各个分支之间自由地运行 upgrades 或 downgrades （让我们再次假设一个干净的数据库）：

```bash
$ alembic upgrade networking@head
INFO  [alembic.migration] Running upgrade  -> 3cac04ae8714, create networking branch
INFO  [alembic.migration] Running upgrade 3cac04ae8714 -> 109ec7d132bf, add ip number table
INFO  [alembic.migration] Running upgrade 109ec7d132bf -> 29f859a13ea, add DNS table
```

or against the whole thing using `heads`:

> 或使用 `heads` 替换全部事情：

```bash
$ alembic upgrade heads
INFO  [alembic.migration] Running upgrade  -> 1975ea83b712, create account table
INFO  [alembic.migration] Running upgrade 1975ea83b712 -> 27c6a30d7c24, add shopping cart table
INFO  [alembic.migration] Running upgrade 27c6a30d7c24 -> d747a8a8879, add a shopping cart column
INFO  [alembic.migration] Running upgrade 1975ea83b712 -> ae1027a6acf, add a column
INFO  [alembic.migration] Running upgrade ae1027a6acf -> 55af2cb1c267, add another account column
```
