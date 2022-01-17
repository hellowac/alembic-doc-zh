# Tutorial

**指南**

[Installation]: ../zh/_front_matter.md#installation-安装
[安装]: ../zh/_front_matter.md#installation-安装
[Python virtual environment]: https://docs.python.org/3/tutorial/venv.html
[Python 虚拟环境]: https://docs.python.org/3/tutorial/venv.html

Alembic provides for the creation, management, and invocation of change management scripts for a relational database, using SQLAlchemy as the underlying engine. This tutorial will provide a full introduction to the theory and usage of this tool.

> Alembic 使用 SQLAlchemy 作为底层引擎，为关系数据库提供变更管理脚本的创建、管理和调用。 本教程将全面介绍该工具的理论和用法。

To begin, make sure Alembic is installed as described at [Installation]. As stated in the linked document, it is usually preferable that Alembic is installed in the **same module / Python path as that of the target project**, usually using a [Python virtual environment], so that when the `alembic` command is run, the Python script which is invoked by `alembic`, namely your project’s `env.py` script, will have access to your application’s models. This is not strictly necessary in all cases, however in the vast majority of cases is usually preferred.

> 首先，请确保按照 [安装] 中的说明安装 `Alembic` 。 如文档中所述，通常最好将 `Alembic` 安装在与目标项目相同的 / Python 路径的模块中，通常使用[Python 虚拟环境]，以便在运行 alembic 命令时，Python 脚本 由 alembic 调用，即你项目的 `env.py` 脚本，将可以访问您的应用程序模型。 这并非在所有情况下都严格必要，但在绝大多数情况下通常是首选。

The tutorial below assumes the `alembic` command line utility is present in the local path and when invoked, will have access to the same Python module environment as that of the target project.

> 下面的教程假设 `alembic` 命令行实用程序存在于本地路径中，并且在调用时，将可以访问与目标项目相同的 Python 模块环境。
