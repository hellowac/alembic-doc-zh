# Replaceable Objects

**可替换对象**

[Alembic Utils]: https://github.com/olirice/alembic_utils
[Operation Plugins]: ../zh/08_05_01_operation_plugins.md
[操作插件]: ../zh/08_05_01_operation_plugins.md

This recipe proposes a hypothetical way of dealing with what we might call a replaceable schema object. A replaceable object is a schema object that needs to be created and dropped all at once. Examples of such objects include views, stored procedures, and triggers.

> 本文章提出了一种假设的方法来处理我们可能称之为可替换模式对象的东西。 可替换对象是需要一次性创建和删除的模式对象。 此类对象的示例包括视图、存储过程和触发器。

> **See also:** The Replaceable Object concept has been integrated by the **[Alembic Utils]** project, which provides autogenerate and migration support for PostgreSQL functions and views. See **[Alembic Utils]** at **<https://github.com/olirice/alembic_utils>** .

> **同样参考**: 可替换对象概念已被 **[Alembic Utils]** 项目集成，该项目为 PostgreSQL 函数和视图提供自动生成和迁移支持。 请参阅 <https://github.com/olirice/alembic_utils> 上的 **[Alembic Utils]**。

Replaceable objects present a problem in that in order to make incremental changes to them, we have to refer to the whole definition at once. If we need to add a new column to a view, for example, we have to drop it entirely and recreate it fresh with the extra column added, referring to the whole structure; but to make it even tougher, if we wish to support downgrade operarations in our migration scripts, we need to refer to the previous version of that construct fully, and we’d much rather not have to type out the whole definition in multiple places.

> 可替换对象存在一个问题，即为了对它们进行增量更改，我们必须立即引用整个定义。 例如，如果我们需要向视图添加一个新列，我们必须完全删除它并重新创建它并添加额外的列，以引用整个结构； 但更难的是，如果我们希望在我们的迁移脚本中支持降级操作，我们需要完全引用该结构的先前版本，我们宁愿不必在多个地方输入整个定义。

This recipe proposes that we may refer to the older version of a replaceable construct by directly naming the migration version in which it was created, and having a migration refer to that previous file as migrations run. We will also demonstrate how to integrate this logic within the **[Operation Plugins]** feature introduced in Alembic 0.8. It may be very helpful to review this section first to get an overview of this API.

> 这篇文章建议我们可以通过直接命名创建它的迁移版本来引用可替换构造的旧版本，并在迁移运行时让迁移引用之前的文件。 我们还将演示如何将此逻辑集成到 Alembic 0.8 中引入的 **[操作插件]** 功能中。 首先查看此部分以了解此 API 的概述可能会非常有帮助。
