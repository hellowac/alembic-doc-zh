# revision

alembic.command.**revision**(*config*:  Config, *message*:  Optional\[[str]\] = None, *autogenerate*:  [bool] = False, *sql*:  [bool] = False, *head*:  [str] = 'head', *splice*:  [bool] = False, *branch_label*:  Optional\[[str]\] = None, *version_path*:  Optional\[[str]\] = None, *rev_id*:  Optional\[[str]\] = None, *depends_on*:  Optional\[[str]\] = None, *process_revision_directives*:  Callable = None) → Union\[Script, None, List\[Optional\[Script\]\]\]

[str]: https://docs.python.org/3/library/stdtypes.html#str
[bool]: https://docs.python.org/3/library/functions.html#bool
[Config]: ../en/config.html#alembic.config.Config
[EnvironmentContext.configure.process_revision_directives]: ../en/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.process_revision_directives
[command.revision()]: #alembic.command.revision

Create a new revision file.

**Parameters:**

* ***config*** – a **[Config]** object.
* ***message*** – string **message** to apply to the revision; this is the `-m` option to `alembic revision`.
* ***autogenerate*** – whether or not to **autogenerate** the script from the database; this is the `--autogenerate` option to `alembic revision`.
* ***sql*** – whether to dump the script out as a SQL string; when specified, the script is dumped to stdout. This is the `--sql` option to `alembic revision`.
* ***head*** – **head** revision to build the new revision upon as a parent; this is the `--head` option to `alembic revision`.
* ***splice*** – whether or not the new revision should be made into a new `head` of its own; is required when the given `head` is not itself a `head`. This is the `--splice` option to `alembic revision`.
* ***branch_label*** – string label to apply to the branch; this is the `--branch-label` option to `alembic revision`.
* ***version_path*** – string symbol identifying a specific version path from the configuration; this is the `--version-path` option to `alembic revision`.
* ***rev_id*** – optional revision identifier to use instead of having one generated; this is the `--rev-id` option to `alembic revision`.
* ***depends_on*** – optional list of “depends on” identifiers; this is the `--depends-on` option to `alembic revision`.
* ***process_revision_directives*** – this is a callable that takes the same form as the callable described at EnvironmentContext.configure.process_revision_directives; will be applied to the structure generated by the revision process where it can be altered programmatically. Note that unlike all the other parameters, this option is only available via programmatic use of command.revision()