# downgrade

alembic.command.**downgrade**(*config*:  Config, *revision*:  [str], *sql*:  [bool] = False, *tag*:  Optional\[[str]\] = None) → None

[str]: https://docs.python.org/3/library/stdtypes.html#str
[bool]: https://docs.python.org/3/library/functions.html#bool
[Config]: ../en/config.html#alembic.config.Config
[EnvironmentContext.get_tag_argument()]: ../en/runtime.html#alembic.runtime.environment.EnvironmentContext.get_tag_argument

Revert to a previous version.

**Parameters:**

* ***config*** – a **[Config]** instance.

* ***revision*** – string **revision** target or range for –sql mode

* ***sql*** – if True, use `--sql` mode

* ***tag*** – an arbitrary “tag” that can be intercepted by custom `env.py` scripts via the **[EnvironmentContext.get_tag_argument()]** method.
