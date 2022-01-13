# Editing the .ini File

[Working with Multiple Bases]: ../zh/05_03_working_with_multiple_bases.md
[Run Multiple Alembic Environments from one .ini]: /zh/07_11_run_multiple_alembic_environments_from_one_ini_file.md
[从一个 .ini 文件运行多个 Alembic 环境]: /zh/07_11_run_multiple_alembic_environments_from_one_ini_file.md
[Configuration File Format]: <http://docs.python.org/library/logging.config.html#configuration-file-format>

**编辑.ini文件**

Alembic placed a file `alembic.ini` into the current directory. This is a file that the `alembic` script looks for when invoked. This file can exist in a different directory, with the location to it specified by either the `--config` option for the `alembic` runner or the `ALEMBIC_CONFIG` environment variable (the former takes precedence).

> Alembic 将文件 `alembic.ini` 放入当前目录。 这是 `alembic` 脚本在调用时查找的文件。 该文件可以存在于不同的目录中，其位置由 alembic runner 的 `--config` 选项或 `ALEMBIC_CONFIG` 环境变量（前者优先）指定。

The file generated with the “generic” configuration looks like:

> 使用“通用(generic)”配置生成的文件如下所示：

```ini
# A generic, single database configuration.
# 通用的单一数据库配置。

[alembic]
# path to migration scripts
# 迁移脚本的路径
script_location = alembic

# template used to generate migration files
# 用于生成迁移文件的模板
# file_template = %%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
# (new in 1.5.5)

# sys.path 路径，如果存在，将被添加到 sys.path 之前。
# 默认为当前工作目录。
# 版本1.5.5中新增
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python-dateutil library that can be
# installed by adding `alembic[tz]` to the pip requirements
# string value is passed to dateutil.tz.gettz()
# leave blank for localtime

# 在迁移文件中呈现日期以及文件名时要使用的时区。
# 如果指定，则需要可以通过将 `alembic[tz]` 添加到 pip 要求来安装的 python-dateutil 库
# 字符串值将传递给 dateutil.tz.gettz() 
# 本地时间留空
# timezone =

# max length of characters to apply to the
# "slug" field

# 应用于“slug”字段的最大字符长度
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate

# 设置为 'true' 以在 'revision' 命令期间运行环境，而无论是否自动生成
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory

# 设置为“true”以允许将没有源 .py 文件的 .pyc 和 .pyo 文件检测为 `versions/` 目录中的版本文件
# sourceless = false

# version location specification; This defaults
# to ${script_location}/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path.
# The path separator used here should be the separator specified by "version_path_separator" below.

# 版本位置规范； 这默认为`${script_location}/versions`。 使用多个版本目录时，必须使用 --version-path 指定初始版本。
# 这里使用的路径分隔符应该是下面“version_path_separator”指定的分隔符。
# version_locations = %(here)s/bar:%(here)s/bat:${script_location}/versions

# version path separator; As mentioned above, this is the character used to split
# version_locations. The default within new alembic.ini files is "os", which uses os.pathsep.
# If this key is omitted entirely, it falls back to the legacy behavior of splitting on spaces and/or commas.
# Valid values for version_path_separator are:
#
# 版本路径分隔符； 如上所述，这是用于拆分 version_locations 的字符。 新 alembic.ini 文件中的默认值是“os”，它使用 os.pathsep。
# 如果这个键被完全省略，它会退回到在空格和/或逗号上分割的传统行为。
# version_path_separator 的有效值为：
# 
# version_path_separator = :
# version_path_separator = ;
# version_path_separator = space
version_path_separator = os  # Use os.pathsep. Default configuration used for new projects. (使用 os.pathsep。 用于新项目的默认配置。)

# the output encoding used when revision files
# are written from script.py.mako
# 从 script.py.mako 写入修订文件时使用的输出编码
# output_encoding = utf-8

; sqlalchemy.url = driver://user:pass@localhost/dbname
sqlalchemy.url = postgresql://wangchao:@localhost/test

# [post_write_hooks]
# This section defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples
# 本节定义在新生成的修订脚本上运行的脚本或 Python 函数。 有关更多详细信息和示例，请参阅文档

# format using "black" - use the console_scripts runner,
# against the "black" entrypoint
# 使用“black”格式 - 使用 console_scripts runner，针对“black”入口点
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

# Logging configuration
# 日志记录配置
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

The file is read using **Python’s ConfigParser.SafeConfigParser** object. The `%(here)s` variable is provided as a substitution variable, which can be used to produce absolute pathnames to directories and files, as we do above with the path to the Alembic script location.

> 该文件是使用 Python 的 **ConfigParser.SafeConfigParser** 对象读取的。 **%(here)s** 变量作为替代变量提供，可用于生成目录和文件的绝对路径名，就像我们上面对 Alembic 脚本位置的路径所做的那样。

This file contains the following features:

> 该文件包含以下功能：

* [alembic] - this is the section read by Alembic to determine configuration. Alembic itself does not directly read any other areas of the file. The name “alembic” can be customized using the **--name** commandline flag; see [Run Multiple Alembic Environments from one .ini] file for a basic example of this.
* > [alembic] - 这是 Alembic 读取的用于确定配置的部分。 Alembic 本身不直接读取文件的任何其他区域。 可以使用 **--name** 命令行标志自定义名称“alembic”； 有关此操作的基本示例，请参阅[从一个 .ini 文件运行多个 Alembic 环境]。
* **script_location** - this is the location of the Alembic environment. It is normally specified as a filesystem location, either relative or absolute. If the location is a relative path, it’s interpreted as relative to the current directory.
* > **script_location** - 这是 Alembic 环境的位置。 它通常被指定为相对或绝对的文件系统位置。 如果位置是相对路径，则将其解释为相对于当前目录。

    This is the only key required by Alembic in all cases. The generation of the .ini file by the command `alembic init alembic` automatically placed the directory name `alembic` here. The special variable `%(here)s` can also be used, as in `%(here)s/alembic`.

    > 这是 Alembic 在所有情况下都需要的唯一密钥。 通过命令 `alembic init alembic` 生成的 `.ini` 文件会自动将目录名 `alembic` 放置在这里。 也可以使用特殊变量 `%(here)s`，如 `%(here)s/alembic`。

    For support of applications that package themselves into .egg files, the value can also be specified as a [package resource](https://setuptools.readthedocs.io/en/latest/pkg_resources.html), in which case **resource_filename()** is used to find the file (new in 0.2.2). Any non-absolute URI which contains colons is interpreted here as a resource name, rather than a straight filename.

    > 为了支持将自身打包成 .egg 文件的应用程序，该值也可以指定为[包资源](https://setuptools.readthedocs.io/en/latest/pkg_resources.html)，在这种情况下，**resource_filename()** 用于查找文件（版本0.2.2 中的新功能）。 任何包含冒号的非绝对 URI 在这里都被解释为资源名称，而不是直接的文件名。

* **file_template** - this is the naming scheme used to generate new migration files. The value present is the default, so is commented out. Tokens available include:
* > **file_template** - 这是用于生成新迁移文件的命名方案。 存在的值是默认值，因此被注释掉。 可用的token包括：
  * **%%(rev)s** - revision id (修订号)
  * **%%(slug)s** - a truncated string derived from the revision message (从修订消息派生的截断字符串)
  * **%%(year)d**, **%%(month).2d**, **%%(day).2d**, **%%(hour).2d**, **%%(minute).2d**, **%%(second).2d** - components of the create date, by default **datetime.datetime.now()** unless the **timezone** configuration option is also used. （创建日期的组成部分，默认为 **datetime.datetime.now()** 除非还使用了 **timezone** 配置选项。）
* **timezone** - an optional timezone name (e.g. UTC, EST5EDT, etc.) that will be applied to the timestamp which renders inside the migration file’s comment as well as within the filename. This option requires installing the **python-dateutil** library. If **timezone** is specified, the create date object is no longer derived from **datetime.datetime.now()** and is instead generated as:
* > **timezone** - 一个可选的时区名称（例如 UTC、EST5EDT 等），它将应用于在迁移文件的注释以及文件名中呈现的时间戳。 此选项需要安装 **python-dateutil** 库。 如果指定了时区，则创建日期对象不再从 **datetime.datetime.now()** 派生，而是生成为：

    ```python
    datetime.datetime.utcnow().replace(
        tzinfo=dateutil.tz.tzutc()
    ).astimezone(
        dateutil.tz.gettz(<timezone>)
    )
    ```

* **truncate_slug_length** - defaults to 40, the max number of characters to include in the “slug” field.
* > **truncate_slug_length** - 默认为 40，即“slug”字段中包含的最大字符数。
* **sqlalchemy.url** - A URL to connect to the database via SQLAlchemy. This configuration value is only used if the **env.py** file calls upon them; in the “generic” template, the call to **config.get_main_option("sqlalchemy.url")** in the **run_migrations_offline()** function and the call to **engine_from_config(prefix="sqlalchemy.")** in the **run_migrations_online()** function are where this key is referenced. If the SQLAlchemy URL should come from some other source, such as from environment variables or a global registry, or if the migration environment makes use of multiple database URLs, the developer is encouraged to alter the **env.py** file to use whatever methods are appropriate in order to acquire the database URL or URLs.
* > **sqlalchemy.url** - 通过 SQLAlchemy 连接到数据库的 URL。 此配置值仅在 **env.py** 文件调用它们时使用； 在“通用”模板中，**run_migrations_offline()** 函数中对 **config.get_main_option("sqlalchemy.url")** 的调用和 **run_migrations_online()** 函数中对 **engine_from_config(prefix="sqlalchemy.")** 的调用是该键所在的位置参考。 如果 SQLAlchemy URL 应该来自某些其他源，例如来自环境变量或全局注册表，或者如果迁移环境使用多个数据库 URL，则鼓励开发人员更改 **env.py** 文件以使用任何合适的方法以获取数据库 URL 或 其他URL。
* **revision_environment** - this is a flag which when set to the value ‘true’, will indicate that the migration environment script **env.py** should be run unconditionally when generating new revision files, as well as when running the **alembic history** command.
* > **revision_environment** - 这是一个标志，当设置为值“true”时，将指示在生成新修订文件以及运行 alembic 历史命令时应无条件运行迁移环境脚本 **env.py**。
* **sourceless** - when set to ‘true’, revision files that only exist as .pyc or .pyo files in the versions directory will be used as versions, allowing “sourceless” versioning folders. When left at the default of ‘false’, only .py files are consumed as version files.
* > **sourceless** - 当设置为“true”时，版本目录中仅作为 .pyc 或 .pyo 文件存在的修订文件将用作版本，允许“无源”版本控制文件夹。 当保留默认值“false”时，只有 .py 文件被用作版本文件。
* **version_locations** - an optional list of revision file locations, to allow revisions to exist in multiple directories simultaneously. See [Working with Multiple Bases] for examples.
* > **version_locations** - 一个可选的修订文件位置列表，允许修订同时存在于多个目录中。 有关示例，请参阅 [Working with Multiple Bases]。
* **version_path_separator** - a separator of **version_locations** paths. It should be defined if multiple version_locations is used. See [Working with Multiple Bases] for examples.
* > **version_path_separator** - version_locations 路径的分隔符。 如果使用多个 **version_locations**，则应定义它。 有关示例，请参阅[Working with Multiple Bases]。
* **output_encoding** - the encoding to use when Alembic writes the **script.py.mako** file into a new migration file. Defaults to `'utf-8'`.
* > **output_encoding** - 当 Alembic 将 **script.py.mako** 文件写入新的迁移文件时使用的编码。 默认为“utf-8”。
* [loggers], [handlers], [formatters], [logger_*], [handler_*], [formatter_*] - these sections are all part of Python’s standard logging configuration, the mechanics of which are documented at [Configuration File Format]. As is the case with the database connection, these directives are used directly as the result of the **logging.config.fileConfig()** call present in the **env.py** script, which you’re free to modify.
* > [loggers], [handlers], [formatters], [logger_*], [handler_*], [formatter_*] - 这些部分都是 Python 标准日志配置的一部分，其机制记录在配置文件格式中。 与数据库连接的情况一样，这些指令直接作为 **env.py** 脚本中存在的 **logging.config.fileConfig()** 调用的结果使用，您可以自由修改。

For starting up with just a single database and the generic configuration, setting up the SQLAlchemy URL is all that’s needed:

> 对于只使用单个数据库和通用配置的启动，只需要设置 SQLAlchemy URL：

```python
sqlalchemy.url = postgresql://scott:tiger@localhost/test
```
