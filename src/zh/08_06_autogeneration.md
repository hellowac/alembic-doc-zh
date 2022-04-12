# Autogeneration

[Auto Generating Migrations]: ../en/autogenerate.html
[自动生成迁移]: ./01_auto_generating_migrations.md
[MetaData]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.MetaData
[MigrateOperation]: ../en/operations.html#alembic.operations.ops.MigrateOperation

> **Note:** this section discusses the **internal API of Alembic** as regards the autogeneration feature of the `alembic revision` command. This section is only useful for developers who wish to extend the capabilities of Alembic. For general documentation on the autogenerate feature, please see **[Auto Generating Migrations]**.

The autogeneration system has a wide degree of public API, including the following areas:

1. The ability to do a “diff” of a **[MetaData]** object against a database, and receive a data structure back. This structure is available either as a rudimentary list of changes, or as a **[MigrateOperation]** structure.
2. The ability to alter how the `alembic revision` command generates revision scripts, including support for multiple revision scripts generated in one pass.
3. The ability to add new operation directives to autogeneration, including custom schema/model comparison functions and revision script rendering.

> **注意**： 本节讨论 Alembic 的内部 API 关于 alembic 修订命令的自动生成功能。 本节仅对希望扩展 Alembic 功能的开发人员有用。 有关自动生成功能的一般文档，请参阅[自动生成迁移]。

自动生成系统具有广泛的公共API，包括以下领域：

1. 能够根据数据库对 [MetaData] 对象进行“比较”，并接收返回的数据结构。 此结构可用作基本更改列表或 [MigrateOperation] 结构。
2. 更改 `alembic revision` 命令生成修订脚本的方式的能力，包括支持一次生成的多个修订脚本。
3. 向自动生成添加新操作指令的能力，包括自定义模式/模型比较功能和修订脚本渲染。
