# ensure_version

alembic.command.**ensure_version**(*config*:  Config, *sql*:  [bool] = False) → None

[bool]: https://docs.python.org/3/library/functions.html#bool
[Config]: ../zh/08_03_configuration.md

Create the alembic version table if it doesn’t exist already .

> 如果 alembic 版本表不存在，则创建它。

**Parameters:**

* ***config*** – a **[Config]** instance.
* ***sql*** – use `--sql` mode

    New in version 1.7.6.

> 参数:
>
> * ***config*** – 一个 **[Config]** 实例.
> * ***sql*** – 使用 `--sql` 模式
>
>   1.7.6版本中新增
