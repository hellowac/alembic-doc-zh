# Creating an Environment

**创建环境**

With a basic understanding of what the environment is, we can create one using `alembic init`. This will create an environment using the “generic” template:

对环境是什么有了基本的了解后，我们可以使用 `alembic init` 创建一个。 这将使用“通用（generic）”模板创建一个环境：

```bash
cd /path/to/yourproject
source /path/to/yourproject/.venv/bin/activate   # assuming a local virtualenv (激活一个本地环境)
alembic init alembic
```

Where above, the init command was called to generate a migrations directory called alembic:

在上面的地方，调用了 `init` 命令来生成一个名为 alembic 的迁移目录：

```bash
Creating directory /path/to/yourproject/alembic...done
Creating directory /path/to/yourproject/alembic/versions...done
Generating /path/to/yourproject/alembic.ini...done
Generating /path/to/yourproject/alembic/env.py...done
Generating /path/to/yourproject/alembic/README...done
Generating /path/to/yourproject/alembic/script.py.mako...done
Please edit configuration/connection/logging settings in '/path/to/yourproject/alembic.ini' before proceeding.
```

Alembic also includes other environment templates. These can be listed out using the `list_templates` command:

Alembic 还包括其他环境模板。 这些可以使用 `list_templates` 命令列出：

```bash
$ alembic list_templates
Available templates:

generic - Generic single-database configuration.
async - Generic single-database configuration with an async dbapi.
multidb - Rudimentary multi-database configuration.
pylons - Configuration that reads from a Pylons project environment.

Templates are used via the 'init' command, e.g.:

  alembic init --template pylons ./scripts
```
