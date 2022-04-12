# Getting Diffs

[MetaData]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.MetaData
[compare_metadata()]: #alembic.autogenerate.compare_metadata
[produce_migrations()]: #alembic.autogenerate.produce_migrations
[Operation Directives]: ./08_05_operation_directives.md
[操作指令]: ./08_05_operation_directives.md
[MigrationContext]: ./08_02_02_the_migration_context.md
[EnvironmentContext.configure()]: ./08_02_01_02_configure.md
[MigrationScript]: ./08_05_02_built_in_operation_objects.md#MigrationScript
[Customizing Revision Generation]: ./08_06_02_customizing_revision_generation.md
[自定义修订生成]: ./08_06_02_customizing_revision_generation.md

The simplest API autogenerate provides is the “schema comparison” API; these are simple functions that will run all registered “comparison” functions between a **[MetaData]** object and a database backend to produce a structure showing how they differ. The two functions provided are **[compare_metadata()]**, which is more of the “legacy” function that produces diff tuples, and **[produce_migrations()]**, which produces a structure consisting of operation directives detailed in **[Operation Directives]**.

自动生成提供的最简单的 API 是“模式比较”API； 这些是简单的函数，它们将在 [MetaData] 对象和数据库后端之间运行所有已注册的“比较”函数，以生成显示它们之间差异的结构。 提供的两个函数是 [compare_metadata()]，它更像是产生差异元组的“遗留”函数，以及产生由 **[操作指令]** 中详述的操作指令组成的结构的 [produce_migrations()]。

* *class* alembic.autogenerate.**compare_metadata**(*context*:  MigrationContext, *metadata*:  MetaData) → Any <a name="compare_metadata"></a>

    Compare a database schema to that given in a **[MetaData]** instance.

    将 数据库schema 与 **[MetaData]** 实例中给出的 schema 进行比较。

    The database connection is presented in the context of a **[MigrationContext]** object, which provides database connectivity as well as optional comparison functions to use for datatypes and server defaults - see the “autogenerate” arguments at **[EnvironmentContext.configure()]** for details on these.

    数据库连接在 [MigrationContext] 对象的上下文中呈现，该对象提供数据库连接以及用于数据类型和服务器默认值的可选比较函数 - 有关这些详细信息，请参阅 **[EnvironmentContext.configure()]** 中的 “autogenerate” 参数。

    The return format is a list of “diff” directives, each representing individual differences:

    返回格式是 “diff” 指令列表，每个指令代表个体差异：

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

  * ***context*** – 一个 **[MigrationContext]** 实例.
  * ***metadata*** – 一个 **[MetaData]** 实例.

    > **同样参考:** **[produce_migrations()]** - 生成基于 **metadata** (元数据) 比较的 **[MigrationScript]** 结构。

* *class* alembic.autogenerate.**produce_migrations**(*context*:  MigrationContext, *metadata*:  MetaData) → MigrationScript <a name="produce_migrations"></a>

    根据 schema 比较生成 **[MigrationScript]** 的结构。

    这个函数本质上是 **[compare_metadata()]** 所做的，但随后会运行结果列表来生成完整的 **[MigrationScript]** 对象。 有关其外观的示例，请参阅[自定义修订生成]中的示例。

    **同样参考:** **[compare_metadata()]** - 通过比较 `schema` 返回更基本的 “diff” 数据。
