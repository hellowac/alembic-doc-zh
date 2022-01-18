[ScriptDirectory]: #alembic.script.ScriptDirectory
[str]: https://docs.python.org/3/library/stdtypes.html#str
[Script]: #alembic.script.Script
[ScriptDirectory.iterate_revisions()]: #alembic.script.ScriptDirectory.iterate_revisions
[module]: #alembic.script.Script.module
[int]: https://docs.python.org/3/library/functions.html#int
[bool]: https://docs.python.org/3/library/functions.html#bool
[Config]: config.html#alembic.config.Config
[alembic.script.base.Script]: #alembic.script.Script
[ScriptDirectory.get_bases()]: #alembic.script.ScriptDirectory.get_bases
[ScriptDirectory.get_heads()]: #alembic.script.ScriptDirectory.get_heads
[ScriptDirectory.get_current_head()]: #alembic.script.ScriptDirectory.get_current_head
[None]: https://docs.python.org/3/library/constants.html#None
[alembic.command]: commands.html#module-alembic.command
[RevisionMap]: #alembic.script.revision.RevisionMap
[Revision]: #alembic.script.revision.Revision
[alembic.script.revision.Revision]: #alembic.script.revision.Revision
[Â¶]: #alembic.script.revision.RevisionMap.get_current_head.params.branch_label
[MultipleHeads]: #alembic.script.revision.MultipleHeads

# Script Directory

The  **[ScriptDirectory]**  object provides programmatic accessto the Alembic version files present in the filesystem.

* *class* alembic.script. **Script** (*module:* *module*, *rev_id:* ***[str]***, *path:* ***[str]***)

    Represent a single revision file in a  directory.

    The  **[Script]**  instance is returned by methodssuch as  **[ScriptDirectory.iterate_revisions()]** .

  * **property***doc***:**[str]***

    Return the docstring given in the script.

  * *property*  **longdoc**  *: **[str]***

    Return the docstring given in the script.

  * **module**  *: **[module]***  *= None*

    The Python module representing the actual script itself.

  * **path**  *: **[str]***  *= None*

    Filesystem path of the script.

* *class* alembic.script. **ScriptDirectory** (*dir:* ***[str]***, *file_template:* ***[str]** = '%(rev)s_%(slug)s'*, *truncate_slug_length:* *Optional\[**[int]**\] = 40*, *version_locations:* *Optional\[List\[**[str]**\]\] = None*, *sourceless:* ***[bool]** = False*, *output_encoding:* ***[str]** = 'utf-8'*, *timezone:* *Optional\[**[str]**\] = None*, *hook_config:* *Optional\[Dict\[**[str]**, **[str]**\]\] = None*)

    Provides operations upon an Alembic script directory.

    This object is useful to get information as to current revisions, most notably being able to get at the “head” revision, for schemes that want to test if the current revision in the database is the most recent:

    ```python
    from alembic.script import ScriptDirectory
    from alembic.config import Config
    config = Config()
    config.set_main_option("script_location", "myapp:migrations")
    script = ScriptDirectory.from_config(config)

    head_revision = script.get_current_head()
    ```
  * *classmethod*  **from_config** (*config:* *Config*) → **[ScriptDirectory]**

    Produce a new  **[ScriptDirectory]**  given a  **[Config]** instance.

    The   **[Config]**   need only have the   `script_location`   key present.
  * **generate_revision** (*revid:* ***[str]***, *message:* *Optional\[**[str]**\]*, *head:* *Optional\[**[str]**\] = None*, *refresh:* ***[bool]** = False*, *splice:* *Optional\[**[bool]**\] = False*, *branch_labels:* *Optional\[**[str]**\] = None*, *version_path:* *Optional\[**[str]**\] = None*, *depends_on:* *Optional\[Union\[**[str]**, Sequence\[**[str]**\]\]\] = None*, *\*\*kw:* *Any*) → Optional\[**[alembic.script.base.Script]**\]

    Generate a new revision file.

    This runs the  template, giventemplate arguments, and creates a new file.

    Parameters

    * **[revid]**   - String revision id.  Typically thiscomes from   `alembic.util.rev_id()`  .
    * **[message]**   - the revision message, the one passedby the -m argument to the   `revision`   command.
    * **[head]**   - the head revision to generate against.  Defaultsto the current âheadâ if True, allow the âheadâ deprecated.

  * **get_base** () → Optional\[**[str]**\]

    Return the âbaseâbaseâversioned headâll get nothing back.

    The iterator yields   **[Script]**   objects.

  * **run_env** () → **[None]**

    Run the script environment.

    This basically runs the   `env.py`   script presentin the migration environment.   It is called exclusivelyby the command functions in   **[alembic.command]**  .

  * **walk_revisions** (*base:* ***[str]** = 'base'*, *head:* ***[str]** = 'heads'*) → Iterator\[**[alembic.script.base.Script]**\]

    Iterate through all revisions.

    Parameters

    * **[base]**   - the base revision, or âbaseâ the head revision; defaults to âheadsâheadâs branch
    * **[head]**   â the head revision; defaults to “heads” to indicateall head revisions.  May also be “heads” to indicate a singlehead revision.