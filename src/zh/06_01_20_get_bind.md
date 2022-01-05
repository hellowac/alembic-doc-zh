# get_bind

**get_bind**() → Connection

[Connection]: https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Connection

Return the current ‘bind’.

Under normal circumstances, this is the **[Connection]** currently being used to emit SQL to the database.

In a SQL script context, this value is `None`. [TODO: verify this]
