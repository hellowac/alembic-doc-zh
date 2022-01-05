# Working with Multiple Bases

**基于多个base工作**

[Run Multiple Alembic Environments from one .ini file]: ../en/cookbook.html#multiple-environments

> **Note**: The multiple base feature is intended to allow for multiple Alembic versioning lineages which share the same alembic_version table. This is so that individual revisions within the lineages can have cross-dependencies on each other. For the simpler case where one project has multiple, **completely independent** revision lineages that refer to **separate** alembic_version tables, see the example in **[Run Multiple Alembic Environments from one .ini file]**.

We’ve seen in the previous section that `alembic upgrade` is fine if we have multiple heads, `alembic revision` allows us to tell it which “head” we’d like to associate our new revision file with, and branch labels allow us to assign names to branches that we can use in subsequent commands. Let’s put all these together and refer to a new “base”, that is, a whole new tree of revision files that will be semi-independent of the account/shopping cart revisions we’ve been working with. This new tree will deal with database tables involving “networking”.
