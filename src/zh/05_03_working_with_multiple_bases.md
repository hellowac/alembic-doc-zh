# Working with Multiple Bases

**基于多个base工作**

[Run Multiple Alembic Environments from one .ini file]: ../zh/07_11_run_multiple_alembic_environments_from_one_ini_file.md
[从一个 .ini 文件运行多个 Alembic 环境]: ../zh/07_11_run_multiple_alembic_environments_from_one_ini_file.md

> **Note**: The multiple base feature is intended to allow for multiple Alembic versioning lineages which share the same alembic_version table. This is so that individual revisions within the lineages can have cross-dependencies on each other. For the simpler case where one project has multiple, **completely independent** revision lineages that refer to **separate** alembic_version tables, see the example in **[Run Multiple Alembic Environments from one .ini file]**.

> **注意**：多基础功能旨在允许共享同一个 `alembic_version` 表的多个 Alembic 版本控制沿袭。 这样一来，沿袭中的各个修订可以相互交叉依赖。 对于一个项目具有多个、**完全独立的**修订沿袭的更简单情况，这些修订沿袭引用**单独的** `alembic_version` 表，请参阅 **[从一个 .ini 文件运行多个 Alembic 环境]** 中的示例。

We’ve seen in the previous section that `alembic upgrade` is fine if we have multiple heads, `alembic revision` allows us to tell it which “head” we’d like to associate our new revision file with, and branch labels allow us to assign names to branches that we can use in subsequent commands. Let’s put all these together and refer to a new “base”, that is, a whole new tree of revision files that will be semi-independent of the account/shopping cart revisions we’ve been working with. This new tree will deal with database tables involving “networking”.

> 我们在上一节中已经看到，如果我们有多个头，`alembic upgrade` 很好，`alembic revision` 允许我们告诉它我们想将我们的新修订文件关联到哪个“head”，并且分支标签允许我们为可以在后续命令中使用的分支分配名称。 让我们把所有这些放在一起并指代一个新的“base”，即一个全新的修订文件树，它将半独立于我们一直在使用的帐户/购物车修订。 这棵新树将处理涉及“networking”的数据库表。
