
[SQLAlchemy]: https://www.sqlalchemy.org/
[Pylons]: http://www.pylonsproject.org/
[Openstack]: http://www.openstack.org/
[sqlalchemy-alembic]: https://groups.google.com/group/sqlalchemy-alembic
[Mike Bayer]: http://techspot.zzzeek.org/
[virtualenv activate]: https://virtualenv.pypa.io/en/latest/userguide/#activate-script
[editable mode]: https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs
[可编辑的模式]: https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs
[Python virtualenv]: https://pypi.org/project/virtualenv/
[virtual environment]: https://docs.python.org/3/tutorial/venv.html
[虚拟环境]: https://docs.python.org/3/tutorial/venv.html
[GitHub issue tracker]: https://github.com/sqlalchemy/alembic/issues/

# Front Matter (指南)

Information about the Alembic project.

有关 Alembic 项目的信息。

## Project Homepage (项目主页)

Alembic is hosted on GitHub at <https://github.com/sqlalchemy/alembic> under the SQLAlchemy organization.

Alembic 托管在 GitHub 上，网址为 <https://github.com/sqlalchemy/alembic>，隶属于 SQLAlchemy 组织。

Releases and project status are available on Pypi at <https://pypi.python.org/pypi/alembic>.

发布和项目状态可在 Pypi 上获取，网址为 <https://pypi.python.org/pypi/alembic>。

The most recent published version of this documentation should be at <https://alembic.sqlalchemy.org>.

本文档的最新发布版本位于 <https://alembic.sqlalchemy.org>。

## Installation （安装）

While Alembic can be installed system wide, it’s more common that it’s installed local to a [virtual environment] , as it also uses libraries such as SQLAlchemy and database drivers that are more appropriate for local installations.

虽然 Alembic 可以在系统范围内安装，但更常见的是将其安装在本地[虚拟环境]中，因为它还使用更适合本地安装的 SQLAlchemy 和数据库驱动程序等库。

The documentation below is only one kind of approach to installing Alembic for a project; there are many such approaches. The documentation below is provided only for those users who otherwise have no specific project setup chosen.

下面的文档只是为项目安装 Alembic 的一种方法； 有很多这样的方法。 下面的文档仅提供给那些没有选择特定项目设置的用户。

To build a virtual environment for a specific project, first we assume that [Python virtualenv] is installed systemwide. Then:

要为特定项目构建虚拟环境，首先我们假设 [Python virtualenv] 已安装在系统范围内。 然后：

```bash
cd /path/to/your/project
virtualenv .venv
```

There is now a Python interpreter that you can access in `/path/to/your/project/.venv/bin/python`, as well as the pip installer tool in `/path/to/your/project/.venv/bin/pip`.

现在有一个 Python 解释器，您可以在 `/path/to/your/project/.venv/bin/python` 中访问，以及 `/path/to/your/project/.venv/bin/pip` 中的 pip 安装程序工具.

We now install Alembic as follows:

我们现在按如下方式安装 Alembic：

```bash
/path/to/your/project/.venv/bin/pip install alembic
```

The install will add the alembic command to the virtual environment. All operations with Alembic in terms of this specific virtual environment will then proceed through the usage of this command, as in:

安装会将 alembic 命令添加到虚拟环境中。 然后，在此特定虚拟环境中使用 Alembic 的所有操作都将通过使用此命令进行，如下所示：

```bash
/path/to/your/project/.venv/bin/alembic init .
```

The next step is optional. If our project itself has a setup.py file, we can also install it in the local virtual environment in [editable mode]:

下一步是可选的。 如果我们的项目本身有setup.py文件，我们也可以在本地虚拟环境中以[可编辑的模式]安装：

```bash
/path/to/your/project/.venv/bin/pip install -e .
```

If we don’t “install” the project locally, that’s fine as well; the default alembic.ini file includes a directive `prepend_sys_path = .` so that the local path is also in sys.path. This allows us to run the alembic command line tool from this directory without our project being “installed” in that environment.

如果我们不在本地“安装”项目，那也没关系； 默认的 alembic.ini 文件包含一个指令 `prepend_sys_path = .` 这样本地路径也在 `sys.path` 中。 这允许我们从该目录运行 alembic 命令行工具，而无需在该环境中“安装”我们的项目。

> *Changed in version 1.5.5: Fixed a long-standing issue where the `alembic` command-line tool would not preserve the default `sys.path` of `.` by implementing `prepend_sys_path` option.*

> 1.5.5版本更新: 修复了一个长期存在的问题，即 alembic 命令行工具不会通过实现 `prepend_sys_path` 选项来保留当前目录(`.`)在`sys.path`中。

As a final step, the [virtualenv activate] tool can be used so that the `alembic` command is available without any path information, within the context of the current shell:

作为最后一步，可以使用 [virtualenv activate] 工具，以便在当前 shell 的上下文中无需任何路径信息即可使用 `alembic` 命令：

```bash
source /path/to/your/project/.venv/bin/activate
```

### Dependencies (依赖)

Alembic’s install process will ensure that [SQLAlchemy] is installed, in addition to other dependencies. Alembic will work with SQLAlchemy as of version 1.3.0.

除了其他依赖项外，[Alembic] 安装过程将确保安装 [SQLAlchemy]。 从 1.3.0 版本开始，[Alembic] 将与 [SQLAlchemy] 一起使用。

> Changed in version 1.5.0: Support for SQLAlchemy older than 1.3.0 was dropped.

> 版本1.5.0更新: 不再支持 1.3.0 版本之前的 SQLAlchemy。

Alembic supports Python versions 3.6 and above

Alembic 支持 Python 3.6 及以上版本

> Changed in version 1.7: Alembic now supports Python 3.6 and newer; support for Python 2.7 has been dropped.

> 版本1.7更新: Alembic 现在支持 Python 3.6 及更新的版本； 已取消对 Python 2.7 的支持。

## Community (社区)

Alembic is developed by [Mike Bayer], and is loosely associated with the [SQLAlchemy], [Pylons], and [Openstack] projects.

Alembic 由 [Mike Bayer] 开发，与 [SQLAlchemy]、[Pylons] 和 [Openstack] 项目松散关联。

User issues, discussion of potential bugs and features should be posted to the Alembic Google Group at [sqlalchemy-alembic].

用户问题、潜在错误和功能的讨论应发布到 Alembic 在 Google Group群组上的 [sqlalchemy-alembic]。

## Bugs (问题)

Bugs and feature enhancements to Alembic should be reported on the [GitHub issue tracker].

应在 [GitHub issue tracker] 上报告 Alembic 的错误和功能加强。
