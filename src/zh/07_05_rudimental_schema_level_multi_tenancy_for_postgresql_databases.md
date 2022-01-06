# Rudimental Schema-Level Multi Tenancy for PostgreSQL Databases

PostgreSQL 数据库的基础架构级多租户

[schema_translate_map]: https://docs.sqlalchemy.org/core/connections.html#translation-of-schema-names
[EnvironmentContext.configure.include_schemas]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.include_schemas
[EnvironmentContext.get_x_argument()]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.get_x_argument

Multi tenancy refers to an application that accommodates for many clients simultaneously. Within the scope of a database migrations tool, multi-tenancy typically refers to the practice of maintaining multiple, identical databases where each database is assigned to one client.

Alembic does not currently have explicit multi-tenant support; typically, the approach must involve running Alembic multiple times against different database URLs.

One common approach to multi-tenancy, particularly on the PostgreSQL database, is to install tenants within individual PostgreSQL schemas. When using PostgreSQL’s schemas, a special variable `search_path` is offered that is intended to assist with targeting of different schemas.

> **Note:** SQLAlchemy includes a system of directing a common set of `Table` metadata to many schemas called **[schema_translate_map]**. Alembic at the time of this writing lacks adequate support for this feature. The recipe below should be considered **interim** until Alembic has more first-class support for schema-level multi-tenancy.

The recipe below can be altered for flexibility. The primary purpose of this recipe is to illustrate how to point the Alembic process towards one PostgreSQL schema or another.

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
