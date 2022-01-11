# Comparing Types

[EnvironmentContext.configure.compare_type]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.compare_type
[sqlalchemy.engine.reflection.Inspector.reflect_table()]: https://docs.sqlalchemy.org/en/14/core/reflection.html#sqlalchemy.engine.reflection.Inspector.reflect_table
[EnvironmentContext.configure.compare_type]: ../en/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.compare_type

The default type comparison logic will work for SQLAlchemy built in types as well as basic user defined types. This logic is only enabled if the **[EnvironmentContext.configure.compare_type]** parameter is set to `True`:

> 默认类型比较逻辑适用于 SQLAlchemy 内置类型以及基本用户定义类型。 此逻辑仅在 **[EnvironmentContext.configure.compare_type]** 参数设置为 `True` 时启用：

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

> **注意**: 当前（从 Alembic 版本 1.4.0 开始）默认类型比较逻辑（最终用户可扩展）通过比较为列生成的 SQL 来工作。 它分两步完成 -
>
> * 首先，它比较每列的外部类型，例如 VARCHAR 或 TEXT。 方言实现可以具有被视为等效的同义词——这是因为某些数据库通过将类型转换为另一种类型来支持类型。 例如，NUMERIC 和 DECIMAL 在所有后端都被认为是等效的，而在 Oracle 后端，其他同义词 BIGINT、INTEGER、NUMBER、SMALLINT 被添加到此等效列表中
> * 接下来，比较类型中的参数，例如字符串的长度、数字的精度值、枚举中的元素。 如果两列都有参数并且它们不同，则将检测到更改。 如果一列只是设置为默认值，而另一列有参数，Alembic 将继续尝试比较这些。 基本原理是很难检测数据库后端设置的默认值而不产生误报。

> *Changed in version 1.4.0*: Added the text and keyword comparison for column types

> *版本1.4.0更新*：添加了列类型的文本和关键字比较

Alternatively, the **[EnvironmentContext.configure.compare_type]** parameter accepts a callable function which may be used to implement custom type comparison logic, for cases such as where special user defined types are being used:

> 或者，**[EnvironmentContext.configure.compare_type]** 参数接受可用于实现自定义类型比较逻辑的可调用函数，例如使用特殊用户定义类型的情况：

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

> 上面，`inspected_column` 是由 **[sqlalchemy.engine.reflection.Inspector.reflect_table()]** 返回的 **[sqlalchemy.schema.Column]**，而 metadata_column 是 **[sqlalchemy.schema.Column]** 来自本地模型环境。 `None` 的返回值表示要进行默认类型比较。

Additionally, custom types that are part of imported or third party packages which have special behaviors such as per-dialect behavior should implement a method called `compare_against_backend()` on their SQLAlchemy type. If this method is present, it will be called where it can also return True or False to specify the types compare as equivalent or not; if it returns None, default type comparison logic will proceed:

> 此外，作为具有特殊行为（例如每种方言行为）的导入包或第三方包的一部分的自定义类型应在其 SQLAlchemy 类型上实现名为`“compare_against_backend()”`的方法。 如果此方法存在，它将被调用，它还可以返回 `True` 或 `False` 以指定类型比较是否等效； 如果它返回 `None` ，默认类型比较逻辑将继续：

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

> **警告**：上述 `compare_against_backend` 方法的布尔返回值，它是 SQLAlchemy 的一部分，而不是 Alembic，与 **[EnvironmentContext.configure.compare_type]** 可调用的方法相反，对于相同的类型返回  `True` ，对于不相同的类型返回 `False`。另一方面，**[EnvironmentContext.configure.compare_type]** 可调用应该为不同的类型返回 `True` 。

The order of precedence regarding the **[EnvironmentContext.configure.compare_type]** callable vs. the type itself implementing `compare_against_backend` is that the **[EnvironmentContext.configure.compare_type]** callable is favored first; if it returns `None`, then the `compare_against_backend` method will be used, if present on the metadata type. If that returns `None`, then a basic check for type equivalence is run.

> 关于 **[EnvironmentContext.configure.compare_type]**  可调用对象与实现 `compare_against_backend` 的类型本身的优先顺序是 **[EnvironmentContext.configure.compare_type]** 可调用对象优先； 如果它返回 `None` ，则将使用 `compare_against_backend` 方法（如果存在于元数据类型上）。 如果返回 `None` ，则运行类型等价的基本检查。

> *New in version 1.4.0*: - added column keyword comparisons and the type_synonyms property.

> *版本1.4.0新功能*: 添加了列关键字比较和 type_synonyms 属性。
