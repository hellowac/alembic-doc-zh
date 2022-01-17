# Run Multiple Alembic Environments from one .ini file

[Working with Multiple Bases]: ../zh/05_03_working_with_multiple_bases.md
[使用多个base]: ../zh/05_03_working_with_multiple_bases.md

Long before Alembic had the “multiple bases” feature described in **[Working with Multiple Bases]**, projects had a need to maintain more than one Alembic version history in a single project, where these version histories are completely independent of each other and each refer to their own alembic_version table, either across multiple databases, schemas, or namespaces. A simple approach was added to support this, the `--name` flag on the commandline.

> 早在 Alembic 拥有[使用多个base]中描述的“多base”功能之前，项目需要在单个项目中维护多个 Alembic 版本历史，其中这些版本历史完全相互独立，并且每个都引用自己的 `alembic_version` 表，可以跨多个数据库、模式或命名空间。 添加了一种简单的方法来支持这一点，即命令行上的 `--name` 标志。

First, one would create an alembic.ini file of this form:

> 首先，创建一个这种形式的 `alembic.ini` 文件：

```ini
[DEFAULT]
# all defaults shared between environments go here

sqlalchemy.url = postgresql://scott:tiger@hostname/mydatabase


[schema1]
# path to env.py and migration scripts for schema1
script_location = myproject/revisions/schema1

[schema2]
# path to env.py and migration scripts for schema2
script_location = myproject/revisions/schema2

[schema3]
# path to env.py and migration scripts for schema3
script_location = myproject/revisions/db2

# this schema uses a different database URL as well
sqlalchemy.url = postgresql://scott:tiger@hostname/myotherdatabase
```

Above, in the `[DEFAULT]` section we set up a default database URL. Then we create three sections corresponding to different revision lineages in our project. Each of these directories would have its own `env.py` and set of versioning files. Then when we run the `alembic` command, we simply give it the name of the configuration we want to use:

> 如上所示，在 `[DEFAULT]` 部分中，我们设置了默认的 数据库URL。 然后我们在我们的项目中创建三个对应于不同修订沿袭的部分。 这些目录中的每一个都有自己的 `env.py` 和一组版本控制文件。 然后当我们运行 `alembic` 命令时，我们只需给它指定我们要使用的配置的名称：

```bash
alembic --name schema2 revision -m "new rev for schema 2" --autogenerate
```

Above, the `alembic` command makes use of the configuration in `[schema2]`, populated with defaults from the `[DEFAULT]` section.

> 上面， `alembic` 命令使用 `[schema2]` 中的配置，填充了 `[DEFAULT]` 部分的默认值。

The above approach can be automated by creating a custom front-end to the Alembic commandline as well.

> 上述方法也可以通过为 Alembic 命令行创建自定义前端来实现自动化。
