# The Replaceable Object Structure

**可替换对象结构**

[table-metadata-like system]: https://github.com/sqlalchemy/sqlalchemy/wiki/UsageRecipes/Views

We first need to devise a simple format that represents the “CREATE XYZ” / “DROP XYZ” aspect of what it is we’re building. We will work with an object that represents a textual definition; while a SQL view is an object that we can define using a **[table-metadata-like system]**, this is not so much the case for things like stored procedures, where we pretty much need to have a full string definition written down somewhere. We’ll use a simple value object called `ReplaceableObject` that can represent any named set of SQL text to send to a “CREATE” statement of some kind:

```python
class ReplaceableObject:
    def __init__(self, name, sqltext):
        self.name = name
        self.sqltext = sqltext
```

Using this object in a migration script, assuming a Postgresql-style syntax, looks like:

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
