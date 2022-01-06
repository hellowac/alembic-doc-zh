# Autogeneration

[Auto Generating Migrations]: ../en/../autogenerate.html
[MetaData]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.MetaData
[MigrateOperation]: ../en/operations.html#alembic.operations.ops.MigrateOperation

> **Note:** this section discusses the **internal API of Alembic** as regards the autogeneration feature of the `alembic revision` command. This section is only useful for developers who wish to extend the capabilities of Alembic. For general documentation on the autogenerate feature, please see **[Auto Generating Migrations]**.

The autogeneration system has a wide degree of public API, including the following areas:

1. The ability to do a “diff” of a **[MetaData]** object against a database, and receive a data structure back. This structure is available either as a rudimentary list of changes, or as a **[MigrateOperation]** structure.
2. The ability to alter how the `alembic revision` command generates revision scripts, including support for multiple revision scripts generated in one pass.
3. The ability to add new operation directives to autogeneration, including custom schema/model comparison functions and revision script rendering.
