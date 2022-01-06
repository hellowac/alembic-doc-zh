# attributes

**attributes**

[sqlalchemy.engine.base.Connection]: https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Connection
[alembic.command]: ../en/commands.html#module-alembic.command
[Sharing a Connection with a Series of Migration Commands and Environments]: ../en/../cookbook.html#connection-sharing
[Config.attributes]: #alembic.config.Config.params.attributes

A Python dictionary for storage of additional state.

This is a utility dictionary which can include not just strings but engines, connections, schema objects, or anything else. Use this to pass objects into an env.py script, such as passing a **[sqlalchemy.engine.base.Connection]** when calling commands from **[alembic.command]** programmatically.

**See also:** **[Sharing a Connection with a Series of Migration Commands and Environments]**

* **[Config.attributes]**
