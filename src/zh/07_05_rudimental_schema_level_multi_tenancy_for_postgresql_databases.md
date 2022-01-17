# Rudimental Schema-Level Multi Tenancy for PostgreSQL Databases

PostgreSQL 数据库的基础架构级多租户

[schema_translate_map]: https://docs.sqlalchemy.org/core/connections.html#translation-of-schema-names
[EnvironmentContext.configure.include_schemas]: ../zh/08_02_01_02_configure.md#include_schemas
[EnvironmentContext.get_x_argument()]: ../zh/08_02_01_11_get_x_argument.md

**Multi tenancy** refers to an application that accommodates for many clients simultaneously. Within the scope of a database migrations tool, multi-tenancy typically refers to the practice of maintaining multiple, identical databases where each database is assigned to one client.

> 多租户是指同时容纳多个客户端的应用程序。 在数据库迁移工具的范围内，多租户通常是指维护多个相同数据库的做法，其中每个数据库都分配给一个客户端。

Alembic does not currently have explicit multi-tenant support; typically, the approach must involve running Alembic multiple times against different database URLs.

> Alembic 目前没有明确的多租户支持； 通常，该方法必须涉及针对不同的数据库 URL 多次运行 Alembic。

One common approach to multi-tenancy, particularly on the PostgreSQL database, is to install tenants within individual PostgreSQL schemas. When using PostgreSQL’s schemas, a special variable `search_path` is offered that is intended to assist with targeting of different schemas.

> 多租户的一种常见方法，特别是在 PostgreSQL 数据库上，是在单个 PostgreSQL 模式中安装租户。 使用 PostgreSQL 的模式时，提供了一个特殊的变量 `search_path`，旨在帮助定位不同的模式。

> **Note:** SQLAlchemy includes a system of directing a common set of `Table` metadata to many schemas called **[schema_translate_map]**. Alembic at the time of this writing lacks adequate support for this feature. The recipe below should be considered **interim** until Alembic has more first-class support for schema-level multi-tenancy.

> **注意:** SQLAlchemy 包含一个系统，该系统将一组通用的表元数据定向到许多称为 **[schema_translate_map]** 的模式。 在撰写本文时，Alembic 对此功能缺乏足够的支持。 在 Alembic 对模式级多租户提供更多一流的支持之前，应将以下解决方法视为临时方案。

The recipe below can be altered for flexibility. The primary purpose of this recipe is to illustrate how to point the Alembic process towards one PostgreSQL schema or another.

> 可以更改以下配方以提高灵活性。 这个秘籍的主要目的是说明如何将 Alembic 进程指向一个或另一个 PostgreSQL 模式。

1. The model metadata used as the target for autogenerate must not include any schema name for tables; the schema must be non-present or set to `None`. Otherwise, Alembic autogenerate will still attempt to compare and render tables in terms of this schema:
    ```python
    class A(Base):
        __tablename__ = 'a'

        id = Column(Integer, primary_key=True)
        data = Column(UnicodeText())
        foo = Column(Integer)

        __table_args__ = {
            "schema": None
        }

    ```
2. The **[EnvironmentContext.configure.include_schemas]** flag must also be False or not included.
3. The “tenant” will be a schema name passed to Alembic using the “-x” flag. In `env.py` an approach like the following allows `-xtenant=some_schema` to be supported by making use of **[EnvironmentContext.get_x_argument()]**:

    ```python
    def run_migrations_online():
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        current_tenant = context.get_x_argument(as_dictionary=True).get("tenant")
        with connectable.connect() as connection:

            # set search path on the connection, which ensures that
            # PostgreSQL will emit all CREATE / ALTER / DROP statements
            # in terms of this schema by default
            connection.execute("set search_path to %s" % current_tenant)

            # make use of non-supported SQLAlchemy attribute to ensure
            # the dialect reflects tables in terms of the current tenant name
            connection.dialect.default_schema_name = current_tenant

            context.configure(
                connection=connection,
                target_metadata=target_metadata,
            )

            with context.begin_transaction():
                context.run_migrations()
    ```

    The current tenant is set using the PostgreSQL `search_path` variable on the connection. Note above we must employ a **non-supported SQLAlchemy workaround** at the moment which is to hardcode the SQLAlchemy dialect’s default schema name to our target schema.

    It is also important to note that the above changes remain on the connection permanently unless reversed explicitly. If the alembic application simply exits above, there is no issue. However if the application attempts to continue using the above connection for other purposes, it may be necessary to reset these variables back to the default, which for PostgreSQL is usually the name “public” however may be different based on configuration.
4. Alembic operations will now proceed in terms of whichever schema we pass on the command line. All logged SQL will show no schema, except for reflection operations which will make use of the `default_schema_name` attribute:

    ```bash
    []$ alembic -x tenant=some_schema revision -m "rev1" --autogenerate
    ```
5. Since **all** schemas are to be maintained in sync, autogenerate should be run against only **one** schema, generating new Alembic migration files. Autogenerate migratin operations are then run against **all** schemas.

----

1. 用作自动生成目标的模型元数据不得包含表的任何`schema`名称； `schema` 必须不存在或设置为`None`。 否则，Alembic 自动生成仍将尝试根据此模式比较和呈现表：
    ```python
    class A(Base):
        __tablename__ = 'a'

        id = Column(Integer, primary_key=True)
        data = Column(UnicodeText())
        foo = Column(Integer)

        __table_args__ = {
            "schema": None
        }

    ```
2. **[EnvironmentContext.configure.include_schemas]** 标志也必须为 `False` 或不包括在内。
3. “租户”将是使用`“-x”`选项传递给 Alembic 的模式名称。 在 `env.py` 中，类似以下的方法允许通过使用 **[EnvironmentContext.get_x_argument()]** 来支持 `-xtenant=some_schema`：

    ```python
    def run_migrations_online():
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        current_tenant = context.get_x_argument(as_dictionary=True).get("tenant")
        with connectable.connect() as connection:

            # set search path on the connection, which ensures that
            # PostgreSQL will emit all CREATE / ALTER / DROP statements
            # in terms of this schema by default
            connection.execute("set search_path to %s" % current_tenant)

            # make use of non-supported SQLAlchemy attribute to ensure
            # the dialect reflects tables in terms of the current tenant name
            connection.dialect.default_schema_name = current_tenant

            context.configure(
                connection=connection,
                target_metadata=target_metadata,
            )

            with context.begin_transaction():
                context.run_migrations()
    ```

    当前租户是使用连接上的 PostgreSQL `search_path` 变量设置的。 请注意，我们目前必须采用 **不受支持的 SQLAlchemy 解决方法**，即将 SQLAlchemy 方言的默认模式名称硬编码到我们的目标模式。

    同样重要的是要注意，除非明确撤销，否则上述更改将永久保留在连接上。 如果 alembic 应用程序只是在上面退出，则没有问题。 但是，如果应用程序尝试继续使用上述连接用于其他目的，则可能需要将这些变量重置为默认值，对于 PostgreSQL，默认值通常是名称 “public”，但根据配置可能会有所不同。

4. Alembic 操作现在将根据我们在命令行上传递的任何模式进行。 除了使用 `default_schema_name` 属性的反射操作外，所有记录的 SQL 都不会显示任何模式：

    ```bash
    []$ alembic -x tenant=some_schema revision -m "rev1" --autogenerate
    ```
5. 由于 **所有schema** 都将保持同步，因此自动生成应该只针对 **一个schema** 运行，生成新的 Alembic 迁移文件。 然后针对 **所有schema** 运行自动生成迁移操作。
