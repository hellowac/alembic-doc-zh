# upgrade

alembic.command.**upgrade**(*config*:  Config, *revision*:  [str], *sql*:  [bool] = False, *tag*:  Optional\[[str]\] = None) → None

[str]: https://docs.python.org/3/library/stdtypes.html#str
[bool]: https://docs.python.org/3/library/functions.html#bool
[Config]: ../zh/08_03_configuration.md
[EnvironmentContext.get_tag_argument()]: ../zh/08_02_01_10_get_tag_argument.md

Upgrade to a later version.

**Parameters:**

* ***config*** – a **[Config]** instance.
* ***revision*** – string **revision** target or range for –sql mode
* ***sql*** – if True, use `--sql` mode
* ***tag*** – an arbitrary “tag” that can be intercepted by custom `env.py` scripts via the **[EnvironmentContext.get_tag_argument()]** method.

> 参数:
>
> * ***config*** – 一个 **[Config]** 实例.
> * ***revision*** – `–sql` 模式的字符串 **修订** 目标或范围
> * ***sql*** – 如果为 `True` , 使用 `--sql` 模式
> * ***tag*** – 一个任意"标签", 可以通过 `env.py` 文件中的 **[EnvironmentContext.get_tag_argument]** 方法定义。
