# Create Revision Migrations

**创建修订迁移**

[Operations.get_context()]: ../en/ops.html#alembic.operations.Operations.get_context

Finally, we can illustrate how we would “revise” these objects. Let’s consider we added a new column `email` to our `customer` table:

> 最后，我们可以说明我们将如何“修改”这些对象。 假设我们在 `customer` 表中添加了一个新列 `email`：

```bash
alembic revision -m "add email col"
```

The migration is:

> 迁移是：

```python
"""add email col

Revision ID: 191a2d20b025
Revises: 28af9800143f
Create Date: 2015-07-27 16:25:59.277326

"""

# revision identifiers, used by Alembic.
revision = '191a2d20b025'
down_revision = '28af9800143f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column("customer", sa.Column("email", sa.String()))


def downgrade():
    op.drop_column("customer", "email")
```

We now need to recreate the `customer_view` view and the `add_customer_sp` function. To include downgrade capability, we will need to refer to the **previous** version of the construct; the `replace_view()` and `replace_sp()` operations we’ve created make this possible, by allowing us to refer to a specific, **previous** revision. the `replaces` and `replace_with` arguments accept a dot-separated string, which refers to a revision number and an object name, such as `"28af9800143f.customer_view"`. The `ReversibleOp` class makes use of the **[Operations.get_context()]** method to locate the version file we refer to:

> 我们现在需要重新创建 `customer_view` 视图和 `add_customer_sp` 函数。 要包括 `downgrade` 功能，我们需要参考以前版本的构造； 我们创建的 `replace_view()` 和 `replace_sp()` 操作通过允许我们参考特定的先前版本来实现这一点。 `replaces` 和 `replace_with` 参数接受点分隔的字符串，它指的是修订号和对象名称，例如`“28af9800143f.customer_view”`。 `ReversibleOp` 类使用 `Operations.get_context()` 方法来定位我们引用的版本文件：

```bash
alembic revision -m "update views/sp"
```

The migration:

> 迁移是：

```python
"""update views/sp

Revision ID: 199028bf9856
Revises: 191a2d20b025
Create Date: 2015-07-27 16:26:31.344504

"""

# revision identifiers, used by Alembic.
revision = '199028bf9856'
down_revision = '191a2d20b025'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

from foo import ReplaceableObject

customer_view = ReplaceableObject(
    "customer_view",
    "SELECT name, order_count, email "
    "FROM customer WHERE order_count > 0"
)

add_customer_sp = ReplaceableObject(
    "add_customer_sp(name varchar, order_count integer, email varchar)",
    """
    RETURNS integer AS $$
    BEGIN
        insert into customer (name, order_count, email)
        VALUES (in_name, in_order_count, email);
    END;
    $$ LANGUAGE plpgsql;
    """
)


def upgrade():
    op.replace_view(customer_view, replaces="28af9800143f.customer_view")
    op.replace_sp(add_customer_sp, replaces="28af9800143f.add_customer_sp")


def downgrade():
    op.replace_view(customer_view, replace_with="28af9800143f.customer_view")
    op.replace_sp(add_customer_sp, replace_with="28af9800143f.add_customer_sp")
```

Above, instead of using `create_view()`, `create_sp()`, `drop_view()`, and `drop_sp()` methods, we now use `replace_view()` and `replace_sp()`. The replace operation we’ve built always runs a DROP and a CREATE. Running an upgrade to head we see:

> 上面，我们现在使用 `replace_view()` 和 `replace_sp()`，而不是使用 `create_view()`、`create_sp()`、`drop_view()` 和 `drop_sp()` 方法。 我们构建的替换操作总是运行 DROP 和 CREATE。 运行升级到 head 我们看到：

```bash
$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [sqlalchemy.engine.base.Engine] BEGIN (implicit)
INFO  [sqlalchemy.engine.base.Engine] select relname from pg_class c join pg_namespace n on n.oid=c.relnamespace where pg_catalog.pg_table_is_visible(c.oid) and relname=%(name)s
INFO  [sqlalchemy.engine.base.Engine] {'name': u'alembic_version'}
INFO  [sqlalchemy.engine.base.Engine] SELECT alembic_version.version_num
FROM alembic_version
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [alembic.runtime.migration] Running upgrade 28af9800143f -> 191a2d20b025, add email col
INFO  [sqlalchemy.engine.base.Engine] ALTER TABLE customer ADD COLUMN email VARCHAR
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] UPDATE alembic_version SET version_num='191a2d20b025' WHERE alembic_version.version_num = '28af9800143f'
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [alembic.runtime.migration] Running upgrade 191a2d20b025 -> 199028bf9856, update views/sp
INFO  [sqlalchemy.engine.base.Engine] DROP VIEW customer_view
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] CREATE VIEW customer_view AS SELECT name, order_count, email FROM customer WHERE order_count > 0
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] DROP FUNCTION add_customer_sp(name varchar, order_count integer)
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] CREATE FUNCTION add_customer_sp(name varchar, order_count integer, email varchar)
    RETURNS integer AS $$
    BEGIN
        insert into customer (name, order_count, email)
        VALUES (in_name, in_order_count, email);
    END;
    $$ LANGUAGE plpgsql;

INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] UPDATE alembic_version SET version_num='199028bf9856' WHERE alembic_version.version_num = '191a2d20b025'
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] COMMIT
```

After adding our new `email` column, we see that both `customer_view` and `add_customer_sp()` are dropped before the new version is created. If we downgrade back to the old version, we see the old version of these recreated again within the downgrade for this migration:

> 添加新的 `email` 列后，我们看到 `customer_view` 和 `add_customer_sp()` 在创建新版本之前都被删除了。 如果我们降级回旧版本，我们会看到这些旧版本在此迁移的降级中再次重新创建：

```bash
$ alembic downgrade 28af9800143
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [sqlalchemy.engine.base.Engine] BEGIN (implicit)
INFO  [sqlalchemy.engine.base.Engine] select relname from pg_class c join pg_namespace n on n.oid=c.relnamespace where pg_catalog.pg_table_is_visible(c.oid) and relname=%(name)s
INFO  [sqlalchemy.engine.base.Engine] {'name': u'alembic_version'}
INFO  [sqlalchemy.engine.base.Engine] SELECT alembic_version.version_num
FROM alembic_version
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [alembic.runtime.migration] Running downgrade 199028bf9856 -> 191a2d20b025, update views/sp
INFO  [sqlalchemy.engine.base.Engine] DROP VIEW customer_view
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] CREATE VIEW customer_view AS SELECT name, order_count FROM customer WHERE order_count > 0
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] DROP FUNCTION add_customer_sp(name varchar, order_count integer, email varchar)
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] CREATE FUNCTION add_customer_sp(name varchar, order_count integer)
    RETURNS integer AS $$
    BEGIN
        insert into customer (name, order_count)
        VALUES (in_name, in_order_count);
    END;
    $$ LANGUAGE plpgsql;

INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] UPDATE alembic_version SET version_num='191a2d20b025' WHERE alembic_version.version_num = '199028bf9856'
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [alembic.runtime.migration] Running downgrade 191a2d20b025 -> 28af9800143f, add email col
INFO  [sqlalchemy.engine.base.Engine] ALTER TABLE customer DROP COLUMN email
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] UPDATE alembic_version SET version_num='28af9800143f' WHERE alembic_version.version_num = '191a2d20b025'
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] COMMIT
```
