# Autogenerating Custom Operation Directives

[Operation Plugins]: ../en/operations.html#operation-plugins
[MigrateOperation]: ../en/operations.html#alembic.operations.ops.MigrateOperation
[Customizing Revision Generation]: #customizing-revision
[Sequence]: https://docs.sqlalchemy.org/en/14/core/defaults.html#sqlalchemy.schema.Sequence
[Table]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table
[MetaData]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.MetaData
[AutogenContext]: #alembic.autogenerate.api.AutogenContext
[UpgradeOps]: ../en/operations.html#alembic.operations.ops.UpgradeOps
[ModifyTableOps]: ../en/operations.html#alembic.operations.ops.ModifyTableOps
[AlterColumnOp]: ../en/operations.html#alembic.operations.ops.AlterColumnOp
[Column]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column
[Connection]: https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Connection
[MigrationContext.bind]: ../en/runtime.html#alembic.runtime.migration.MigrationContext.bind
[Dialect]: https://docs.sqlalchemy.org/en/14/core/internals.html#sqlalchemy.engine.Dialect
[EnvironmentContext.configure.render_item]: ../en/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.render_item
[Affecting the Rendering of Types Themselves]: ../en/../autogenerate.html#autogen-render-types
[EnvironmentContext.configure.target_metadata]: ../en/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.target_metadata
[MigrationContext]: ../en/runtime.html#alembic.runtime.migration.MigrationContext
[EnvironmentContext.configure.include_object]: ../en/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.include_object
[EnvironmentContext.configure.include_name]: ../en/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.include_name

In the section **[Operation Plugins]**, we talked about adding new subclasses of **[MigrateOperation]** in order to add new `op.` directives. In the preceding section **[Customizing Revision Generation]**, we also learned that these same **[MigrateOperation]** structures are at the base of how the autogenerate system knows what Python code to render. Using this knowledge, we can create additional functions that plug into the autogenerate system so that our new operations can be generated into migration scripts when `alembic revision --autogenerate` is run.

The following sections will detail an example of this using the the `CreateSequenceOp` and `DropSequenceOp` directives we created in **[Operation Plugins]**, which correspond to the SQLAlchemy **[Sequence]** construct.

## Tracking our Object with the Model

The basic job of an autogenerate comparison function is to inspect a series of objects in the database and compare them against a series of objects defined in our model. By “in our model”, we mean anything defined in Python code that we want to track, however most commonly we’re talking about a series of **[Table]** objects present in a **[MetaData]** collection.

Let’s propose a simple way of seeing what **[Sequence]** objects we want to ensure exist in the database when autogenerate runs. While these objects do have some integrations with **[Table]** and **[MetaData]** already, let’s assume they don’t, as the example here intends to illustrate how we would do this for most any kind of custom construct. We associate the object with the `info` collection of **[MetaData]**, which is a dictionary we can use for anything, which we also know will be passed to the autogenerate process:

```python
from sqlalchemy.schema import Sequence

def add_sequence_to_model(sequence, metadata):
    metadata.info.setdefault("sequences", set()).add(
        (sequence.schema, sequence.name)
    )

my_seq = Sequence("my_sequence")
add_sequence_to_model(my_seq, model_metadata)
```

The `info` dictionary is a good place to put things that we want our autogeneration routines to be able to locate, which can include any object such as custom DDL objects representing views, triggers, special constraints, or anything else we want to support.

## Registering a Comparison Function

We now need to register a comparison hook, which will be used to compare the database to our model and produce `CreateSequenceOp` and `DropSequenceOp` directives to be included in our migration script. Note that we are assuming a Postgresql backend:

```python
from alembic.autogenerate import comparators

@comparators.dispatch_for("schema")
def compare_sequences(autogen_context, upgrade_ops, schemas):
    all_conn_sequences = set()

    for sch in schemas:

        all_conn_sequences.update([
            (sch, row[0]) for row in
            autogen_context.connection.execute(
                "SELECT relname FROM pg_class c join "
                "pg_namespace n on n.oid=c.relnamespace where "
                "relkind='S' and n.nspname=%(nspname)s",

                # note that we consider a schema of 'None' in our
                # model to be the "default" name in the PG database;
                # this usually is the name 'public'
                nspname=autogen_context.dialect.default_schema_name
                if sch is None else sch
            )
        ])

    # get the collection of Sequence objects we're storing with
    # our MetaData
    metadata_sequences = autogen_context.metadata.info.setdefault(
        "sequences", set())

    # for new names, produce CreateSequenceOp directives
    for sch, name in metadata_sequences.difference(all_conn_sequences):
        upgrade_ops.ops.append(
            CreateSequenceOp(name, schema=sch)
        )

    # for names that are going away, produce DropSequenceOp
    # directives
    for sch, name in all_conn_sequences.difference(metadata_sequences):
        upgrade_ops.ops.append(
            DropSequenceOp(name, schema=sch)
        )
```

Above, we’ve built a new function `compare_sequences()` and registered it as a “schema” level comparison function with autogenerate. The job that it performs is that it compares the list of sequence names present in each database schema with that of a list of sequence names that we are maintaining in our **[MetaData]** object.

When autogenerate completes, it will have a series of `CreateSequenceOp` and `DropSequenceOp` directives in the list of “upgrade” operations; the list of “downgrade” operations is generated directly from these using the `CreateSequenceOp`.reverse() and `DropSequenceOp`.reverse() methods that we’ve implemented on these objects.

The registration of our function at the scope of “schema” means our autogenerate comparison function is called outside of the context of any specific table or column. The three available scopes are “schema”, “table”, and “column”, summarized as follows:

1. **Schema level** - these hooks are passed a **[AutogenContext]**, an **[UpgradeOps]** collection, and a collection of string schema names to be operated upon. If the **[UpgradeOps]** collection contains changes after all hooks are run, it is included in the migration script:

    ```python
    @comparators.dispatch_for("schema")
    def compare_schema_level(autogen_context, upgrade_ops, schemas):
        pass
    ```

2. **Table level** - these hooks are passed a **[AutogenContext]**, a **[ModifyTableOps]** collection, a schema name, table name, a **[Table]** reflected from the database if any or `None`, and a **[Table]** present in the local **[MetaData]**. If the **[ModifyTableOps]** collection contains changes after all hooks are run, it is included in the migration script:

    ```python
    @comparators.dispatch_for("table")
    def compare_table_level(autogen_context, modify_ops,
        schemaname, tablename, conn_table, metadata_table):
        pass
    ```

3. **Column level** - these hooks are passed a **[AutogenContext]**, an **[AlterColumnOp]** object, a schema name, table name, column name, a **[Column]** reflected from the database and a **[Column]** present in the local table. If the **[AlterColumnOp]** contains changes after all hooks are run, it is included in the migration script; a “change” is considered to be present if any of the `modify_` attributes are set to a non-default value, or there are any keys in the `.kw` collection with the prefix `"modify_"`:

    ```python
    @comparators.dispatch_for("column")
    def compare_column_level(autogen_context, alter_column_op,
        schemaname, tname, cname, conn_col, metadata_col):
        pass
    ```

The **[AutogenContext]** passed to these hooks is documented below.

* *class* alembic.autogenerate.api.**AutogenContext**(migration_context: MigrationContext, metadata: Optional[MetaData] = None, opts: Optional[dict] = None, autogenerate: bool = True)

    Maintains configuration and state that’s specific to an autogenerate operation.

  * **connection**: *Optional*\[Connection\] = None

    The **[Connection]** object currently connected to the database backend being compared.

    This is obtained from the **[MigrationContext.bind]** and is ultimately set up in the `env.py` script.

  * **dialect**: *Optional*\[Dialect\] = None

    The **[Dialect]** object currently in use.

    This is normally obtained from the `dialect` attribute.

  * **imports**: *Set*\[[str]\] = None

    A `set()` which contains string Python import directives.

    The directives are to be rendered into the `${imports}` section of a script template. The set is normally empty and can be modified within hooks such as the **[EnvironmentContext.configure.render_item]** hook.

    **See also:** **[Affecting the Rendering of Types Themselves]**

  * **metadata**: *Optional*\[MetaData\] = None

    The **[MetaData]** object representing the destination.

    This object is the one that is passed within `env.py` to the **[EnvironmentContext.configure.target_metadata]** parameter. It represents the structure of `Table` and other objects as stated in the current database model, and represents the destination structure for the database being examined.

    While the **[MetaData]** object is primarily known as a collection of **[Table]** objects, it also has an `info` dictionary that may be used by end-user schemes to store additional schema-level objects that are to be compared in custom autogeneration schemes.

  * **migration_context**: *MigrationContext* = None

    The **[MigrationContext]** established by the `env.py` script.

  * **run_filters**(object_: Union\[Table, Index, Column, UniqueConstraint, ForeignKeyConstraint\], name: Optional\[[str]\], type_: [str], reflected: [bool], compare_to: Optional\[Union\[Table, Index, Column, UniqueConstraint\]\]) → [bool]

    Run the context’s object filters and return True if the targets should be part of the autogenerate operation.

    This method should be run for every kind of object encountered within an autogenerate operation, giving the environment the chance to filter what objects should be included in the comparison. The filters here are produced directly via the **[EnvironmentContext.configure.include_object]** parameter.

  * **run_name_filters**(name: Optional\[[str]\], type_: [str], parent_names: Dict\[str, Optional\[[str]\]\]) → [bool]

    Run the context’s name filters and return True if the targets should be part of the autogenerate operation.

    This method should be run for every kind of name encountered within the reflection side of an autogenerate operation, giving the environment the chance to filter what names should be reflected as database objects. The filters here are produced directly via the **[EnvironmentContext.configure.include_name]** parameter.

  * **run_object_filters**(object_: Union\[Table, Index, Column, UniqueConstraint, ForeignKeyConstraint\], name: Optional\[**str**\], type_: [str], reflected: [bool], compare_to: Optional\[Union\[Table, Index, Column, UniqueConstraint\]\]) → [bool]

    Run the context’s object filters and return True if the targets should be part of the autogenerate operation.

    This method should be run for every kind of object encountered within an autogenerate operation, giving the environment the chance to filter what objects should be included in the comparison. The filters here are produced directly via the **[EnvironmentContext.configure.include_object]** parameter.

  * **sorted_tables**

    Return an aggregate of the `MetaData.sorted_tables` collection(s).

    For a sequence of `MetaData` objects, this concatenates the `MetaData`.sorted_tables collection for each individual `MetaData` in the order of the sequence. It does **not** collate the sorted tables collections.

  * **table_key_to_table**

    Return an aggregate of the `MetaData.tables` dictionaries.

    The `MetaData.tables` collection is a dictionary of table key to Table; this method aggregates the dictionary across multiple `MetaData` objects into one dictionary.

    Duplicate table keys are **not** supported; if two `MetaData` objects contain the same table key, an exception is raised.

## Creating a Render Function

The second autogenerate integration hook is to provide a “render” function; since the autogenerate system renders Python code, we need to build a function that renders the correct “op” instructions for our directive:

```python
from alembic.autogenerate import renderers

@renderers.dispatch_for(CreateSequenceOp)
def render_create_sequence(autogen_context, op):
    return "op.create_sequence(%r, **%r)" % (
        op.sequence_name,
        {"schema": op.schema}
    )


@renderers.dispatch_for(DropSequenceOp)
def render_drop_sequence(autogen_context, op):
    return "op.drop_sequence(%r, **%r)" % (
        op.sequence_name,
        {"schema": op.schema}
    )
```

The above functions will render Python code corresponding to the presence of `CreateSequenceOp` and `DropSequenceOp` instructions in the list that our comparison function generates.

## Running It

All the above code can be organized however the developer sees fit; the only thing that needs to make it work is that when the Alembic environment `env.py` is invoked, it either imports modules which contain all the above routines, or they are locally present, or some combination thereof.

If we then have code in our model (which of course also needs to be invoked when `env.py` runs!) like this:

```python
from sqlalchemy.schema import Sequence

my_seq_1 = Sequence("my_sequence_1")
add_sequence_to_model(my_seq_1, target_metadata)
```

When we first run `alembic revision --autogenerate`, we’ll see this in our migration file:

```python
def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_sequence('my_sequence_1', **{'schema': None})
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_sequence('my_sequence_1', **{'schema': None})
    ### end Alembic commands ###
```

These are our custom directives that will invoke when `alembic upgrade` or `alembic downgrade` is run.
