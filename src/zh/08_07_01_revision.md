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
[MultipleHeads]: #alembic.script.revision.MultipleHeads

# Revision

The   **[RevisionMap]**   object serves as the basis for revisionmanagement, used exclusively by   **[ScriptDirectory]**  .

* *exception* alembic.script.revision. **CycleDetected** (*revisions:* *Sequence\[**[str]**\]*)
* *exception* alembic.script.revision. **DependencyCycleDetected** (*revisions:* *Sequence\[**[str]**\]*)
* *exception* alembic.script.revision. **DependencyLoopDetected** (*revision:* *Sequence\[**[str]**\]*)
* *exception* alembic.script.revision. **LoopDetected** (*revision:* ***[str]***)
* *exception* alembic.script.revision. **MultipleHeads** (*heads:* *Sequence\[**[str]**\]*, *argument:* *Optional\[**[str]**\]*)
* *exception* alembic.script.revision. **RangeNotAncestorError** (*lower:* *Optional\[Union\[**[str]**, Tuple\[**[str]**, ...\]\]\]*, *upper:* *Optional\[Union\[**[str]**, Tuple\[**[str]**, ...\]\]\]*)
* *exception* alembic.script.revision. **ResolutionError** (*message:* ***[str]***, *argument:* ***[str]***)
* *class* alembic.script.revision. **Revision** (*revision:* ***[str]***, *down_revision:* *Optional\[Union\[**[str]**, Tuple\[**[str]**, ...\]\]\]*, *dependencies:* *Optional\[Tuple\[**[str]**, ...\]\] = None*, *branch_labels:* *Optional\[Tuple\[**[str]**, ...\]\] = None*)

    Base class for revisioned objects.

    The   **[Revision]**   class is the base of the more public-facing  **[Script]**   object, which represents a migration script.The mechanics of revision management and traversal are encapsulatedwithin   **[Revision]**  , while   **[Script]**   applies this logicto Python files in a version directory.

  * **branch_labels**  *: Set\[**[str]**\]*  *= None*

    Optional string/tuple of symbolic names to apply to thisrevision"s branch

  * **dependencies**  *: Optional\[Union\[**[str]**, Sequence\[**[str]**\]\]\]*  *= None*

    Additional revisions which this revision is dependent on.

    From a migration standpoint, these dependencies are added to thedown_revision to form the full iteration.  However, the separationof down_revision from “dependencies” is to assist in navigatinga history that contains many branches, typically a multi-root scenario.

  * **down_revision**  *: Optional\[Union\[**[str]**, Sequence\[**[str]**\]\]\]*  *= None*

    The   `down_revision`   identifier(s) within the migration script.

    Note that the total set of "down" revisions isdown_revision + dependencies.

  * *property*  **is_base**  *: **[bool]***

    Return True if this   **[Revision]**   is a "base" revision.

  * *property*  **is_branch_point**  *: **[bool]***

    Return True if this   **[Script]**   is a branch point.

    A branchpoint is defined as a   **[Script]**   which is referredto by more than one succeeding   **[Script]**  , that is morethan one   **[Script]**   has a   identifier pointinghere.

  * *property*  **is_head**  *: **[bool]***

    Return True if this   **[Revision]**   is a "head" revision.

    This is determined based on whether any other   **[Script]**  within the   **[ScriptDirectory]**   refers to this  **[Script]**  .   Multiple heads can be present.

  * *property*  **is_merge_point**  *: **[bool]***

    Return True if this   **[Script]**   is a merge point.

  * **nextrev**  *: FrozenSet\[**[str]**\]*  *= frozenset({})*

    following revisions, based on down_revision only.

  * **revision**  *: **[str]***  *= None*

    The string revision number.

* *exception* alembic.script.revision. **RevisionError**

* *class* alembic.script.revision. **RevisionMap** (*generator:* *Callable\[\[\], Iterator\[**[alembic.script.revision.Revision]**\]\]*)

    Maintains a map of   **[Revision]**   objects.

    **[RevisionMap]**   is used by   **[ScriptDirectory]**   to maintainand traverse the collection of   **[Script]**   objects, which arethemselves instances of   **[Revision]** .

    Construct a new   **[RevisionMap]**  .

    > **Parameters:**
    >
    > * **generator**   " a zero-arg callable that will generate an iterableof   **[Revision]**   instances to be used.   These are typically  **[Script]**   subclasses within regular Alembic use.

  * **add_revision** (*revision:* ***[alembic.script.revision.Revision]***, *_replace:* ***[bool]** = False*) → **[None]**

    add a single revision to an existing map.

    This method is for single-revision use cases, it"s notappropriate for fully populating an entire revision map.

  * **bases**

    All ”base“ revisions as strings.

    These are revisions that have a   `down_revision`   of None,or empty tuple.

    > **Returns：**
    >
    > * a tuple of string revision numbers.

  * **get_current_head** (*branch_label:* *Optional\[**[str]**\] = None*) → Optional\[**[str]**\]

    Return the current head revision.

    If the script directory has multiple headsdue to branching, an error is raised;  **[ScriptDirectory.get_heads()]**   should bepreferred.

    > **Parameters:**
    >
    > * **branch_label**   " optional branch name which will limit theheads considered to those which include that branch_label.

    > **Returns:** a string revision number.

    > **See also:** **[ScriptDirectory.get_heads()]**

  * **get_revision** (*id_:* *Optional\[**[str]**\]*) → **[alembic.script.revision.Revision]**

    Return the   **[Revision]**   instance with the given rev id.

    If a symbolic name such as "head" or "base" is given, resolvesthe identifier into the current head or base revision.  If the symbolicname refers to multiples,   **[MultipleHeads]**   is raised.

    Supports partial identifiers, where the given identifieris matched against all identifiers that start with the givencharacters; if there is exactly one match, that determines thefull revision.

  * **get_revisions** (*id_:* *Optional\[Union\[**[str]**, Collection\[**[str]**\]\]\]*) → Tuple\[**[alembic.script.revision.Revision]**, ...\]

    Return the   **[Revision]**   instances with the given rev idor identifiers.

    May be given a single identifier, a sequence of identifiers, or thespecial symbols "head" or "base".  The result is a tuple of oneor more identifiers, or an empty tuple in the case of "base".

    In the cases where "head", "heads" is requested and therevision map is empty, returns an empty tuple.

    Supports partial identifiers, where the given identifieris matched against all identifiers that start with the givencharacters; if there is exactly one match, that determines thefull revision.

  * **heads**

    All "head" revisions as strings.

    This is normally a tuple of length one,unless unmerged branches are present.

    > **Returns:** a tuple of string revision numbers.

  * **iterate_revisions** (*upper:* *Optional\[Union\[**[str]**, Tuple\[**[str]**, ...\]\]\]*, *lower:* *Optional\[Union\[**[str]**, Tuple\[**[str]**, ...\]\]\]*, *implicit_base:* ***[bool]** = False*, *inclusive:* ***[bool]** = False*, *assert_relative_length:* ***[bool]** = True*, *select_for_downgrade:* ***[bool]** = False*) → Iterator\[**[alembic.script.revision.Revision]**\]

    Iterate through script revisions, starting at the givenupper revision identifier and ending at the lower.

    The traversal uses strictly the  marker inside each migration script, soit is a requirement that upper >= lower,else you"ll get nothing back.

    The iterator yields   **[Revision]**   objects.
