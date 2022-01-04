#

**再次运行迁移**

Let’s do another one so we have some things to play with. We again create a revision file:

> 让我们再做一个，这样我们就有一些东西可以玩了。 我们再次创建一个修订文件：

```bash
$ alembic revision -m "Add a column"
Generating /path/to/yourapp/alembic/versions/ae1027a6acf_add_a_column.py...
done
```

Let’s edit this file and add a new column to the `account` table:

> 让我们编辑这个文件并向 `account` 表中添加一个新列：

```python
"""Add a column

Revision ID: ae1027a6acf
Revises: 1975ea83b712
Create Date: 2011-11-08 12:37:36.714947

"""

# revision identifiers, used by Alembic.
revision = 'ae1027a6acf'
down_revision = '1975ea83b712'

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))

def downgrade():
    op.drop_column('account', 'last_transaction_date')
```

Running again to `head`:

> 再次运行到`head`：

```bash
$ alembic upgrade head
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
INFO  [alembic.context] Running upgrade 1975ea83b712 -> ae1027a6acf
```

We’ve now added the `last_transaction_date` column to the database.

> 我们现在已将 `last_transaction_date` 列添加到数据库中。
