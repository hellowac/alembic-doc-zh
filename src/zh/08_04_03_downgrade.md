# downgrade

alembic.command.**downgrade**(*config*:  Config, *revision*:  [str], *sql*:  [bool] = False, *tag*:  Optional\[[str]\] = None) → None

[str]: https://docs.python.org/3/library/stdtypes.html#str
[bool]: https://docs.python.org/3/library/functions.html#bool
[Config]: ../zh/08_03_configuration.md
[EnvironmentContext.get_tag_argument()]: ../en/runtime.html#alembic.runtime.environment.EnvironmentContext.get_tag_argument

Revert to a previous version.

> 恢复到以前的版本。

**Parameters:**

* ***config*** – a **[Config]** instance.
* ***revision*** – string **revision** target or range for –sql mode
* ***sql*** – if True, use `--sql` mode
* ***tag*** – an arbitrary “tag” that can be intercepted by custom `env.py` scripts via the **[EnvironmentContext.get_tag_argument()]** method.

> 参数:
>
> * ***config*** – 一个 **[Config]** 实例.
> * ***revision*** – `–sql` 模式的字符串 **修订** 目标或范围
> * ***sql*** – 如果为 `True`, 使用 `--sql` 模式
> * ***tag*** – 一个可以通过定义 `env.py` 脚本的 **[EnvironmentContext.get_tag_argument()]** 方法 获取的任意”标签“=
