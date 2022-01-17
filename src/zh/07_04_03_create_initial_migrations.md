# Create Initial Migrations

**创建初始迁移**

We can now illustrate how these objects look during use. For the first step, we’ll create a new migration to create a “customer” table:

> 我们现在可以说明这些对象在使用过程中的外观。 第一步，我们将创建一个新的迁移来创建一个 “customer” 表：

```bash
alembic revision -m "create table"
```

We build the first revision as follows:

> 我们构建第一个修订版如下：

```python
"""create table

Revision ID: 3ab8b2dfb055
Revises:
Create Date: 2015-07-27 16:22:44.918507

"""

# revision identifiers, used by Alembic.
revision = '3ab8b2dfb055'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        "customer",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('order_count', sa.Integer),
    )


def downgrade():
    op.drop_table('customer')
```

For the second migration, we will create a view and a stored procedure which act upon this table:

> 对于第二次迁移，我们将创建一个视图和一个作用于该表的存储过程：

```bash
alembic revision -m "create views/sp"
```

This migration will use the new directives:

> 此迁移将使用新指令：

```python
"""create views/sp

Revision ID: 28af9800143f
Revises: 3ab8b2dfb055
Create Date: 2015-07-27 16:24:03.589867

"""

# revision identifiers, used by Alembic.
revision = '28af9800143f'
down_revision = '3ab8b2dfb055'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

from foo import ReplaceableObject

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


def upgrade():
    op.create_view(customer_view)
    op.create_sp(add_customer_sp)


def downgrade():
    op.drop_view(customer_view)
    op.drop_sp(add_customer_sp)
```

We see the use of our new `create_view()`, `create_sp()`, `drop_view()`, and `drop_sp()` directives. Running these to “head” we get the following (this includes an edited view of SQL emitted):

> 我们看到了我们新的 `create_view()`、`create_sp()`、`drop_view()` 和 `drop_sp()` 指令的使用。 将这些运行到“head”，我们得到以下信息（这包括发出的 SQL 的编辑视图）：

```bash
$ alembic upgrade 28af9800143
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [sqlalchemy.engine.base.Engine] BEGIN (implicit)
INFO  [sqlalchemy.engine.base.Engine] select relname from pg_class c join pg_namespace n on n.oid=c.relnamespace where pg_catalog.pg_table_is_visible(c.oid) and relname=%(name)s
INFO  [sqlalchemy.engine.base.Engine] {'name': u'alembic_version'}
INFO  [sqlalchemy.engine.base.Engine] SELECT alembic_version.version_num
FROM alembic_version
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] select relname from pg_class c join pg_namespace n on n.oid=c.relnamespace where pg_catalog.pg_table_is_visible(c.oid) and relname=%(name)s
INFO  [sqlalchemy.engine.base.Engine] {'name': u'alembic_version'}
INFO  [alembic.runtime.migration] Running upgrade  -> 3ab8b2dfb055, create table
INFO  [sqlalchemy.engine.base.Engine]
CREATE TABLE customer (
    id SERIAL NOT NULL,
    name VARCHAR,
    order_count INTEGER,
    PRIMARY KEY (id)
)


INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] INSERT INTO alembic_version (version_num) VALUES ('3ab8b2dfb055')
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [alembic.runtime.migration] Running upgrade 3ab8b2dfb055 -> 28af9800143f, create views/sp
INFO  [sqlalchemy.engine.base.Engine] CREATE VIEW customer_view AS SELECT name, order_count FROM customer WHERE order_count > 0
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] CREATE FUNCTION add_customer_sp(name varchar, order_count integer)
    RETURNS integer AS $$
    BEGIN
        insert into customer (name, order_count)
        VALUES (in_name, in_order_count);
    END;
    $$ LANGUAGE plpgsql;

INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] UPDATE alembic_version SET version_num='28af9800143f' WHERE alembic_version.version_num = '3ab8b2dfb055'
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] COMMIT
```

We see that our CREATE TABLE proceeded as well as the CREATE VIEW and CREATE FUNCTION operations produced by our new directives.

> 我们看到我们的 CREATE TABLE 以及由我们的新指令产生的 CREATE VIEW 和 CREATE FUNCTION 操作正常进行。
