# batch_alter_table

**batch_alter_table**(table_name, schema=None, recreate='auto', partial_reordering=None, copy_from=None, table_args=(), table_kwargs={}, reflect_args=(), reflect_kwargs={}, naming_convention=None)

[BatchOperations]: ../zh/06_02_batch_operations.md
[Operations]: ../zh/06_01_operations.md
[batch_alter_table()]: ../zh/06_01_03_batch_alter_table.md
[Dealing with Constraints]: ../en/batch.html#sqlite-batch-constraints
[Table]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table
[Working in Offline Mode]: ../zh/04_03_working_in_offline_mode.html
[copy_from]: #alembic.operations.Operations.batch_alter_table.params.copy_from
[Integration of Naming Conventions into Operations, Autogenerate]: ../en/naming.html#autogen-naming-conventions
[MetaData]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.MetaData
[Dropping Unnamed or Named Foreign Key Constraints]: ../en/batch.html#dropping-sqlite-foreign-keys
[batch_alter_table.recreate]: #alembic.operations.Operations.batch_alter_table.params.recreate
[Running “Batch” Migrations for SQLite and Other Databases]: ../en/batch.html#batch-migrations

Invoke a series of per-table migrations in batch.

Batch mode allows a series of operations specific to a table to be syntactically grouped together, and allows for alternate modes of table migration, in particular the “recreate” style of migration required by SQLite.

“recreate” style is as follows:

1. A new table is created with the new specification, based on the migration directives within the batch, using a temporary name.
2. the data copied from the existing table to the new table.
3. the existing table is dropped.
4. the new table is renamed to the existing table name.

The directive by default will only use “recreate” style on the SQLite backend, and only if directives are present which require this form, e.g. anything other than `add_column()`. The batch operation on other backends will proceed using standard ALTER TABLE operations.

The method is used as a context manager, which returns an instance of BatchOperations; this object is the same as **[Operations]** except that table names and schema names are omitted. E.g.:

```python
with op.batch_alter_table("some_table") as batch_op:
    batch_op.add_column(Column('foo', Integer))
    batch_op.drop_column('bar')
```

The operations within the context manager are invoked at once when the context is ended. When run against SQLite, if the migrations include operations not supported by SQLite’s ALTER TABLE, the entire table will be copied to a new one with the new specification, moving all data across as well.

The copy operation by default uses reflection to retrieve the current structure of the table, and therefore **[batch_alter_table()]** in this mode requires that the migration is run in “online” mode. The `copy_from` parameter may be passed which refers to an existing `Table` object, which will bypass this reflection step.

> **Note** The table copy operation will currently not copy CHECK constraints, and may not copy UNIQUE constraints that are unnamed, as is possible on SQLite. See the section **[Dealing with Constraints]** for workarounds.

**Parameters:**

* ***table_name*** – name of table
* ***schema*** – optional **schema** name.
* ***recreate*** – under what circumstances the table should be recreated. At its default of `"auto"`, the SQLite dialect will **recreate** the table if any operations other than `add_column()`, `create_index()`, or `drop_index()` are present. Other options include `"always"` and `"never"`.
* *copy_from* – optional **[Table]** object that will act as the structure of the table being copied. If omitted, table reflection is used to retrieve the structure of the table.
  
  **See also** *[Working in Offline Mode]*
  
  ***reflect_args***
  
  ***reflect_kwargs***
* ***reflect_args*** – a sequence of additional positional arguments that will be applied to the table structure being reflected / copied; this may be used to pass column and constraint overrides to the table that will be reflected, in lieu of passing the whole **[Table]** using **[copy_from]**.
* ***reflect_kwargs*** – a dictionary of additional keyword arguments that will be applied to the table structure being copied; this may be used to pass additional table and reflection options to the table that will be reflected, in lieu of passing the whole **[Table]** using **[copy_from]**.
* ***table_args*** – a sequence of additional positional arguments that will be applied to the new **[Table]** when created, in addition to those copied from the source table. This may be used to provide additional constraints such as CHECK constraints that may not be reflected.
* ***table_args*** – a sequence of additional positional arguments that will be applied to the new **[Table]** when created, in addition to those copied from the source table. This may be used to provide additional constraints such as CHECK constraints that may not be reflected.
* ***table_kwargs*** – a dictionary of additional keyword arguments that will be applied to the new **[Table]** when created, in addition to those copied from the source table. This may be used to provide for additional table options that may not be reflected.
* ***naming_convention*** – a naming convention dictionary of the form described at **[Integration of Naming Conventions into Operations, Autogenerate]** which will be applied to the **[MetaData]** during the reflection process. This is typically required if one wants to drop SQLite constraints, as these constraints will not have names when reflected on this backend. Requires SQLAlchemy **0.9.4** or greater.
    > See also
    >
    > [Dropping Unnamed or Named Foreign Key Constraints]
* ***partial_reordering*** – a list of tuples, each suggesting a desired ordering of two or more columns in the newly created table. Requires that **[batch_alter_table.recreate]** is set to `"always"`. Examples, given a table with columns “a”, “b”, “c”, and “d”:

    Specify the order of all columns:
    ```python
    with op.batch_alter_table(
            "some_table", recreate="always",
            partial_reordering=[("c", "d", "a", "b")]
    ) as batch_op:
        pass
    ```
    Ensure “d” appears before “c”, and “b”, appears before “a”:
    ```python
    with op.batch_alter_table(
            "some_table", recreate="always",
            partial_reordering=[("d", "c"), ("b", "a")]
    ) as batch_op:
        pass
    ```

    The ordering of columns not included in the partial_reordering set is undefined. Therefore it is best to specify the complete ordering of all columns for best results.

    *New in version 1.4.0.*

> **Note:** batch mode requires SQLAlchemy 0.8 or above.

> **See also** [Running “Batch” Migrations for SQLite and Other Databases]
