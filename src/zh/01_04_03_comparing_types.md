# Comparing Types

[EnvironmentContext.configure.compare_type]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.compare_type
[sqlalchemy.engine.reflection.Inspector.reflect_table()]: https://docs.sqlalchemy.org/en/14/core/reflection.html#sqlalchemy.engine.reflection.Inspector.reflect_table
[EnvironmentContext.configure.compare_type]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.compare_type

The default type comparison logic will work for SQLAlchemy built in types as well as basic user defined types. This logic is only enabled if the **[EnvironmentContext.configure.compare_type]** parameter is set to `True`:

```python
context.configure(
    # ...
    compare_type = True
)
```

> **Note**: The default type comparison logic (which is end-user extensible) currently (as of Alembic version 1.4.0) works by comparing the generated SQL for a column. It does this in two steps-
>
> * First, it compares the outer type of each column such as VARCHAR or TEXT. Dialect implementations can have synonyms that are considered equivalent- this is because some databases support types by converting them to another type. For example, NUMERIC and DECIMAL are considered equivalent on all backends, while on the Oracle backend the additional synonyms BIGINT, INTEGER, NUMBER, SMALLINT are added to this list of equivalents
> * Next, the arguments within the type, such as the lengths of strings, precision values for numerics, the elements inside of an enumeration are compared. If BOTH columns have arguments AND they are different, a change will be detected. If one column is just set to the default and the other has arguments, Alembic will pass on attempting to compare these. The rationale is that it is difficult to detect what a database backend sets as a default value without generating false positives.

> *Changed in version 1.4.0*: Added the text and keyword comparison for column types

Alternatively, the **[EnvironmentContext.configure.compare_type]** parameter accepts a callable function which may be used to implement custom type comparison logic, for cases such as where special user defined types are being used:

```python
def my_compare_type(context, inspected_column,
            metadata_column, inspected_type, metadata_type):
    # return False if the metadata_type is the same as the inspected_type
    # or None to allow the default implementation to compare these
    # types. a return value of True means the two types do not
    # match and should result in a type change operation.
    return None

context.configure(
    # ...
    compare_type = my_compare_type
)
```

Above, `inspected_column` is a **[sqlalchemy.schema.Column]** as returned by **[sqlalchemy.engine.reflection.Inspector.reflect_table()]**, whereas metadata_column is a **[sqlalchemy.schema.Column]** from the local model environment. A return value of `None` indicates that default type comparison to proceed.

Additionally, custom types that are part of imported or third party packages which have special behaviors such as per-dialect behavior should implement a method called `compare_against_backend()` on their SQLAlchemy type. If this method is present, it will be called where it can also return True or False to specify the types compare as equivalent or not; if it returns None, default type comparison logic will proceed:

```python
class MySpecialType(TypeDecorator):

    # ...

    def compare_against_backend(self, dialect, conn_type):
        # return True if this type is the same as the given database type,
        # or None to allow the default implementation to compare these
        # types. a return value of False means the given type does not
        # match this type.

        if dialect.name == 'postgresql':
            return isinstance(conn_type, postgresql.UUID)
        else:
            return isinstance(conn_type, String)
```

> **Warning**: The boolean return values for the above `compare_against_backend` method, which is part of SQLAlchemy and not Alembic,are **the opposite** of that of the **[EnvironmentContext.configure.compare_type]** callable, returning `True` for types that are the same vs. `False` for types that are different.The **[EnvironmentContext.configure.compare_type]** callable on the other hand should return `True` for types that are **different**.

The order of precedence regarding the **[EnvironmentContext.configure.compare_type]** callable vs. the type itself implementing `compare_against_backend` is that the **[EnvironmentContext.configure.compare_type]** callable is favored first; if it returns `None`, then the `compare_against_backend` method will be used, if present on the metadata type. If that returns `None`, then a basic check for type equivalence is run.

> *New in version 1.4.0*: - added column keyword comparisons and the type_synonyms property.
