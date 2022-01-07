# Writing Migration Scripts to Support Script Generation

**编写支持生成脚本的迁移脚本**

The challenge of SQL script generation is that the scripts we generate can’t rely upon any client/server database access. This means a migration script that pulls some rows into memory via a `SELECT` statement will not work in `--sql` mode. It’s also important that the Alembic directives, all of which are designed specifically to work in both “live execution” as well as “offline SQL generation” mode, are used.

> SQL 脚本生成的挑战在于我们生成的脚本不能依赖于任何客户端/服务器数据库访问。 这意味着通过 `SELECT` 语句将一些行拉入内存的迁移脚本将无法在 `--sql` 模式下工作。 同时 Alembic 指令也很重要，所有这些指令都是专门为在 “live execution”(实时执行)和 “offline SQL generation”(离线SQL生成) 模式下工作而设计的。
