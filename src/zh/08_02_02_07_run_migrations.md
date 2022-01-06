# run_migrations

**run_migrations**(**kw) → [None]

[MigrationContext]: #alembic.runtime.migration.MigrationContext
[alembic.command]: ../en/commands.html#module-alembic.command
[MigrationContext.run_migrations()]: #alembic.runtime.migration.MigrationContext.run_migrations
[None]: https://docs.python.org/3/library/constants.html#None

Run the migration scripts established for this **[MigrationContext]**, if any.

The commands in **[alembic.command]** will set up a function that is ultimately passed to the **[MigrationContext]** as the `fn` argument. This function represents the “work” that will be done when **[MigrationContext]**.run_migrations() is called, typically from within the `env.py` script of the migration environment. The “work function” then provides an iterable of version callables and other version information which in the case of the `upgrade` or `downgrade` commands are the list of version scripts to invoke. Other commands yield nothing, in the case that a command wants to run some other operation against the database such as the `current` or `stamp` commands.

**Parameters:**

* *****kw*** – keyword arguments here will be passed to each migration callable, that is the `upgrade()` or `downgrade()` method within revision scripts.
