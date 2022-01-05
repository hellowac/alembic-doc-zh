# inline_literal

**inline_literal**(*value*:  Union\[[str], [int]\], *type_*:  [None] = [None]) → _literal_bindparam

[str]: https://docs.python.org/3/library/stdtypes.html#str
[int]: https://docs.python.org/3/library/functions.html#int
[None]: https://docs.python.org/3/library/constants.html#None
[execute()]: ../zh/06_01_18_execute.md
[inline_literal()]: ../zh/06_01_23_inline_literal.md
[EnvironmentContext.configure.literal_binds]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.literal_binds
[sqlalchemy.types.TypeEngine]: https://docs.sqlalchemy.org/en/14/core/type_api.html#sqlalchemy.types.TypeEngine

Produce an ‘inline literal’ expression, suitable for using in an INSERT, UPDATE, or DELETE statement.

When using Alembic in “offline” mode, CRUD operations aren’t compatible with SQLAlchemy’s default behavior surrounding literal values, which is that they are converted into bound values and passed separately into the `execute()` method of the DBAPI cursor. An offline SQL script needs to have these rendered inline. While it should always be noted that inline literal values are an **enormous** security hole in an application that handles untrusted input, a schema migration is not run in this context, so literals are safe to render inline, with the caveat that advanced types like dates may not be supported directly by SQLAlchemy.

See **[execute()]** for an example usage of **[inline_literal()]**.

The environment can also be configured to attempt to render “literal” values inline automatically, for those simple types that are supported by the dialect; see **[EnvironmentContext.configure.literal_binds]** for this more recently added feature.

**Parameters:**

* ***value*** – The **value** to render. Strings, integers, and simple numerics should be supported. Other types like boolean, dates, etc. may or may not be supported yet by various backends.

* ***type_*** – optional - a **[sqlalchemy.types.TypeEngine]** subclass stating the type of this value. In SQLAlchemy expressions, this is usually derived automatically from the Python type of the value itself, as well as based on the context in which the value is used.

**See also:**

* **[EnvironmentContext.configure.literal_binds]**
