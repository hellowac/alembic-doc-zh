# The Replaceable Object Structure

**可替换对象结构**

[table-metadata-like system]: https://github.com/sqlalchemy/sqlalchemy/wiki/UsageRecipes/Views
[表元数据的系统]: https://github.com/sqlalchemy/sqlalchemy/wiki/UsageRecipes/Views

We first need to devise a simple format that represents the “CREATE XYZ” / “DROP XYZ” aspect of what it is we’re building. We will work with an object that represents a textual definition; while a SQL view is an object that we can define using a **[table-metadata-like system]**, this is not so much the case for things like stored procedures, where we pretty much need to have a full string definition written down somewhere. We’ll use a simple value object called `ReplaceableObject` that can represent any named set of SQL text to send to a “CREATE” statement of some kind:

> 我们首先需要设计一个简单的格式来代表我们正在构建的“CREATE XYZ”/“DROP XYZ”表达式。 我们将使用一个表示文本定义的对象； 虽然 SQL 视图是我们可以使用类似 **[表元数据的系统]** 来定义的对象，但对于像存储过程这样的东西来说，情况并非如此，我们几乎需要在某处写下完整的字符串定义。 我们将使用一个名为 `ReplaceableObject` 的简单值对象，它可以表示任何命名的 SQL 文本集，以发送到某种“CREATE”语句：

```python
class ReplaceableObject:
    def __init__(self, name, sqltext):
        self.name = name
        self.sqltext = sqltext
```

Using this object in a migration script, assuming a Postgresql-style syntax, looks like:

> 在迁移脚本中使用此对象，假设使用 Postgresql 样式的语法，如下所示：

```python
customer_view = ReplaceableObject(
    "customer_view",
    "SELECT name, order_count FROM customer WHERE order_count > 0"
)

add_customer_sp = ReplaceableObject(
    "add_customer_sp(name varchar, order_count integer)",
    """
    RETURNS integer AS $$
    BEGIN
        insert into customer (name, order_count)
        VALUES (in_name, in_order_count);
    END;
    $$ LANGUAGE plpgsql;
    """
)
```

The `ReplaceableObject` class is only one very simplistic way to do this. The structure of how we represent our schema objects is not too important for the purposes of this example; we can just as well put strings inside of tuples or dictionaries, as well as that we could define any kind of series of fields and class structures we want. The only important part is that below we will illustrate how organize the code that can consume the structure we create here.

> `ReplaceableObject` 类只是执行此操作的一种非常简单的方法。 对于这个例子来说，我们如何表示我们的模式对象的结构并不是很重要； 我们也可以将字符串放在元组或字典中，也可以定义我们想要的任何类型的字段序列和类结构。 唯一重要的部分是，下面我们将说明如何组织可以使用我们在这里创建的结构的代码。
