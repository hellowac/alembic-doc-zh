# Getting Diffs

[MetaData]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.MetaData
[compare_metadata()]: #alembic.autogenerate.compare_metadata
[produce_migrations()]: #alembic.autogenerate.produce_migrations
[Operation Directives]: ../en/operations.html#alembic-operations-toplevel
[MigrationContext]: ../en/runtime.html#alembic.runtime.migration.MigrationContext
[EnvironmentContext.configure()]: ../en/runtime.html#alembic.runtime.environment.EnvironmentContext.configure
[MigrationScript]: ../en/operations.html#alembic.operations.ops.MigrationScript
[Customizing Revision Generation]: #customizing-revision

The simplest API autogenerate provides is the “schema comparison” API; these are simple functions that will run all registered “comparison” functions between a **[MetaData]** object and a database backend to produce a structure showing how they differ. The two functions provided are **[compare_metadata()]**, which is more of the “legacy” function that produces diff tuples, and **[produce_migrations()]**, which produces a structure consisting of operation directives detailed in **[Operation Directives]**.

* *class* alembic.autogenerate.**compare_metadata**(*context*:  MigrationContext, *metadata*:  MetaData) → Any

    Compare a database schema to that given in a **[MetaData]** instance.

    The database connection is presented in the context of a **[MigrationContext]** object, which provides database connectivity as well as optional comparison functions to use for datatypes and server defaults - see the “autogenerate” arguments at **[EnvironmentContext.configure()]** for details on these.

    The return format is a list of “diff” directives, each representing individual differences:

    ```python
    from alembic.migration import MigrationContext
    from alembic.autogenerate import compare_metadata
    from sqlalchemy.schema import SchemaItem
    from sqlalchemy.types import TypeEngine
    from sqlalchemy import (create_engine, MetaData, Column,
            Integer, String, Table, text)
    import pprint

    engine = create_engine("sqlite://")

    with engine.begin() as conn:
        conn.execute(text('''
            create table foo (
                id integer not null primary key,
                old_data varchar,
                x integer
            )'''))

        conn.execute(text('''
            create table bar (
                data varchar
            )'''))

    metadata = MetaData()
    Table('foo', metadata,
        Column('id', Integer, primary_key=True),
        Column('data', Integer),
        Column('x', Integer, nullable=False)
    )
    Table('bat', metadata,
        Column('info', String)
    )

    mc = MigrationContext.configure(engine.connect())

    diff = compare_metadata(mc, metadata)
    pprint.pprint(diff, indent=2, width=20)
    ```

    Output:

    ```python
    [ ( 'add_table',
        Table('bat', MetaData(bind=None),
            Column('info', String(), table=<bat>), schema=None)),
    ( 'remove_table',
        Table(u'bar', MetaData(bind=None),
            Column(u'data', VARCHAR(), table=<bar>), schema=None)),
    ( 'add_column',
        None,
        'foo',
        Column('data', Integer(), table=<foo>)),
    ( 'remove_column',
        None,
        'foo',
        Column(u'old_data', VARCHAR(), table=None)),
    [ ( 'modify_nullable',
        None,
        'foo',
        u'x',
        { 'existing_server_default': None,
            'existing_type': INTEGER()},
        True,
        False)]]
    ```

  **Parameters:**

  * ***context*** – a **[MigrationContext]** instance.
  * ***metadata*** – a **[MetaData]** instance.

    > **See also:** **[produce_migrations()]** - produces a **[MigrationScript]** structure based on metadata comparison.
    >
    > * ***context*** – a **[MigrationContext]** instance.
    > * ***metadata*** – a **[MetaData]** instance.

* *class* alembic.autogenerate.**produce_migrations**(*context*:  MigrationContext, *metadata*:  MetaData) → MigrationScript

    Produce a **[MigrationScript]** structure based on schema comparison.

    This function does essentially what **[compare_metadata()]** does, but then runs the resulting list of diffs to produce the full **[MigrationScript]** object. For an example of what this looks like, see the example in **[Customizing Revision Generation]**.

    **See also:** **[compare_metadata()]** - returns more fundamental “diff” data from comparing a schema.
