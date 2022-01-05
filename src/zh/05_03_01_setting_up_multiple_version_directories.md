# Setting up Multiple Version Directories

**设置多版本目录**

While optional, it is often the case that when working with multiple bases, we’d like different sets of version files to exist within their own directories; typically, if an application is organized into several sub-modules, each one would have a version directory containing migrations pertinent to that module. So to start out, we can edit `alembic.ini` to refer to multiple directories; we’ll also state the current `versions` directory as one of them:

```python
# A separator for the location paths must be defined first.
version_path_separator = os  # Use os.pathsep.
# version location specification; this defaults
# to foo/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path
version_locations = %(here)s/model/networking:%(here)s/alembic/versions
```

The new directory `%(here)s/model/networking` is in terms of where the `alembic.ini` file is, as we are using the symbol `%(here)s` which resolves to this location. When we create our first new revision targeted at this directory, `model/networking` will be created automatically if it does not exist yet. Once we’ve created a revision here, the path is used automatically when generating subsequent revision files that refer to this revision tree.
