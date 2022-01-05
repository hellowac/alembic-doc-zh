# Replaceable Objects

**可替换对象**

[Alembic Utils]: https://github.com/olirice/alembic_utils
[Operation Plugins]: ../en/api/operations.html#operation-plugins

This recipe proposes a hypothetical way of dealing with what we might call a replaceable schema object. A replaceable object is a schema object that needs to be created and dropped all at once. Examples of such objects include views, stored procedures, and triggers.

> **See also:** The Replaceable Object concept has been integrated by the **[Alembic Utils]** project, which provides autogenerate and migration support for PostgreSQL functions and views. See **[Alembic Utils]** at **<https://github.com/olirice/alembic_utils>** .

Replaceable objects present a problem in that in order to make incremental changes to them, we have to refer to the whole definition at once. If we need to add a new column to a view, for example, we have to drop it entirely and recreate it fresh with the extra column added, referring to the whole structure; but to make it even tougher, if we wish to support downgrade operarations in our migration scripts, we need to refer to the previous version of that construct fully, and we’d much rather not have to type out the whole definition in multiple places.

This recipe proposes that we may refer to the older version of a replaceable construct by directly naming the migration version in which it was created, and having a migration refer to that previous file as migrations run. We will also demonstrate how to integrate this logic within the **[Operation Plugins]** feature introduced in Alembic 0.8. It may be very helpful to review this section first to get an overview of this API.
