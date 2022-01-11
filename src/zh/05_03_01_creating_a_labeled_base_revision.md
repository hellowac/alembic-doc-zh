# Creating a Labeled Base Revision

**创建带标注的基本修订**

We also want our new branch to have its own name, and for that we want to apply a branch label to the base. In order to achieve this using the `alembic revision` command without editing, we need to ensure our `script.py.mako` file, used for generating new revision files, has the appropriate substitutions present. If Alembic version 0.7.0 or greater was used to generate the original migration environment, this is already done. However when working with an older environment, `script.py.mako` needs to have this directive added, typically underneath the `down_revision` directive:

> 我们还希望我们的新分支有自己的名称，为此我们希望将分支标签应用于基础。 为了在不编辑的情况下使用 `alembic revision` 命令实现这一点，我们需要确保用于生成新修订文件的 `script.py.mako` 文件具有适当的替换。 如果使用 Alembic 0.7.0 或更高版本来生成原始迁移环境，这已经完成。 但是，在使用旧环境时，`script.py.mako` 需要添加此指令，通常在 `down_revision` 指令下方：

```bash
# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}

# add this here in order to use revision with branch_label
branch_labels = ${repr(branch_labels)}
```

With this in place, we can create a new revision file, starting up a branch that will deal with database tables involving networking; we specify the `--head` version of `base`, a `--branch-label` of `networking`, and the directory we want this first revision file to be placed in with `--version-path`:

> 有了这个，我们可以创建一个新的修订文件，启动一个处理涉及网络的数据库表的分支； 我们指定 `base` 的 `--head` 版本，`networking` 的 `--branch-label`，以及我们希望使用 `--version-path` 放置第一个修订文件的目录：

```bash
$ alembic revision -m "create networking branch" --head=base --branch-label=networking --version-path=model/networking
  Creating directory /path/to/foo/model/networking ... done
  Generating /path/to/foo/model/networking/3cac04ae8714_create_networking_branch.py ... done
```

If we ran the above command and we didn’t have the newer `script.py.mako` directive, we’d get this error:

> 如果我们运行上面的命令并且我们没有更新的 `script.py.mako` 指令，我们会得到这个错误：

```bash
FAILED: Version 3cac04ae8714 specified branch_labels networking, however
the migration file foo/model/networking/3cac04ae8714_create_networking_branch.py
does not have them; have you upgraded your script.py.mako to include the 'branch_labels'
section?
```

When we receive the above error, and we would like to try again, we need to either **delete** the incorrectly generated file in order to run `revision` again, or we can edit the `3cac04ae8714_create_networking_branch.py` directly to add the `branch_labels` in of our choosing.

> 当我们收到上述错误，我们想重试时，我们需要**删除**错误生成的文件才能再次运行`revision`，或者我们可以直接编辑`3cac04ae8714_create_networking_branch.py`添加我们选择的`branch_labels`。
