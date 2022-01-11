# Setting up Multiple Version Directories

**设置多版本目录**

While optional, it is often the case that when working with multiple bases, we’d like different sets of version files to exist within their own directories; typically, if an application is organized into several sub-modules, each one would have a version directory containing migrations pertinent to that module. So to start out, we can edit `alembic.ini` to refer to multiple directories; we’ll also state the current `versions` directory as one of them:

> 虽然是可选的，但通常情况下，在使用多个基础时，我们希望不同的版本文件集存在于它们自己的目录中； 通常，如果一个应用程序被组织成几个子模块，每个子模块都会有一个版本目录，其中包含与该模块相关的迁移。 因此，首先，我们可以编辑 `alembic.ini` 来引用多个目录； 我们还将当前的 `versions` 目录声明为其中之一：

```python
# A separator for the location paths must be defined first.
version_path_separator = os  # Use os.pathsep.
# version location specification; this defaults
# to foo/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path
version_locations = %(here)s/model/networking:%(here)s/alembic/versions
```

The new directory `%(here)s/model/networking` is in terms of where the `alembic.ini` file is, as we are using the symbol `%(here)s` which resolves to this location. When we create our first new revision targeted at this directory, `model/networking` will be created automatically if it does not exist yet. Once we’ve created a revision here, the path is used automatically when generating subsequent revision files that refer to this revision tree.

> 新目录 `%(here)s/model/networking` 与 `alembic.ini` 文件的位置有关，因为我们使用符号 `%(here)s` 来解析该位置。 当我们针对这个目录创建第一个新版本时，如果 `model/networking` 尚不存在，它将自动创建。 一旦我们在此处创建了修订，在生成引用此修订树的后续修订文件时，将自动使用该路径。
