# Creating a Labeled Base Revision

**创建带标注的基本修订**

We also want our new branch to have its own name, and for that we want to apply a branch label to the base. In order to achieve this using the `alembic revision` command without editing, we need to ensure our `script.py.mako` file, used for generating new revision files, has the appropriate substitutions present. If Alembic version 0.7.0 or greater was used to generate the original migration environment, this is already done. However when working with an older environment, `script.py.mako` needs to have this directive added, typically underneath the `down_revision` directive:

```bash
# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}

# add this here in order to use revision with branch_label
branch_labels = ${repr(branch_labels)}
```

With this in place, we can create a new revision file, starting up a branch that will deal with database tables involving networking; we specify the `--head` version of `base`, a `--branch-label` of `networking`, and the directory we want this first revision file to be placed in with `--version-path`:

```bash
$ alembic revision -m "create networking branch" --head=base --branch-label=networking --version-path=model/networking
  Creating directory /path/to/foo/model/networking ... done
  Generating /path/to/foo/model/networking/3cac04ae8714_create_networking_branch.py ... done
```

If we ran the above command and we didn’t have the newer `script.py.mako` directive, we’d get this error:

```bash
FAILED: Version 3cac04ae8714 specified branch_labels networking, however
the migration file foo/model/networking/3cac04ae8714_create_networking_branch.py
does not have them; have you upgraded your script.py.mako to include the 'branch_labels'
section?
```

When we receive the above error, and we would like to try again, we need to either **delete** the incorrectly generated file in order to run `revision` again, or we can edit the `3cac04ae8714_create_networking_branch.py` directly to add the `branch_labels` in of our choosing.
