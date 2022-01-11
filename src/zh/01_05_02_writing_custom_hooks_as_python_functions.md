# Writing Custom Hooks as Python Functions

[write_hooks.register()]: http://localhost:3002/en/api/script.html#alembic.script.write_hooks.register

The previous section illustrated how to run command-line code formatters, through the use of a post write hook provided by Alembic known as `console_scripts`. This hook is in fact a Python function that is registered under that name using a registration function that may be used to register other types of hooks as well.

> 上一节说明了如何通过使用 Alembic 提供的称为`“console_scripts”`的写后挂钩来运行命令行代码格式化程序。 这个钩子实际上是一个 Python 函数，它使用一个注册函数以该名称注册，该注册函数也可用于注册其他类型的钩子。

To illustrate, we will use the example of a short Python function that wants to rewrite the generated code to use tabs instead of four spaces. For simplicity, we will illustrate how this function can be present directly in the `env.py` file. The function is declared and registered using the [write_hooks.register()] decorator:

> 为了说明，我们将使用一个简短的 Python 函数示例，该函数希望重写生成的代码以使用制表符而不是四个空格。 为简单起见，我们将说明如何将此函数直接存在于 `env.py` 文件中。 该函数使用 [write_hooks.register()] 装饰器声明和注册：

```python
from alembic.script import write_hooks
import re

@write_hooks.register("spaces_to_tabs")
def convert_spaces_to_tabs(filename, options):
    lines = []
    with open(filename) as file_:
        for line in file_:
            lines.append(
                re.sub(
                    r"^(    )+",
                    lambda m: "\t" * (len(m.group(1)) // 4),
                    line
                )
            )
    with open(filename, "w") as to_write:
        to_write.write("".join(lines))
```

Our new `"spaces_to_tabs"` hook can be configured in `alembic.ini` as follows:

> 我们新的 `"spaces_to_tabs"` 钩子可以在 `alembic.ini` 中配置如下：

```ini
[alembic]

# ...

# ensure the revision command loads env.py
revision_environment = true

[post_write_hooks]

hooks = spaces_to_tabs

spaces_to_tabs.type = spaces_to_tabs
```

When `alembic revision` is run, the `env.py` file will be loaded in all cases, the custom `“spaces_to_tabs”` function will be registered and it will then be run against the newly generated file path:

> 当 `alembic revision` 运行时，`env.py` 文件将在所有情况下被加载，自定义的 `“spaces_to_tabs”` 函数将被注册，然后它将针对新生成的文件路径运行：

```bash
$ alembic revision -m "rev1"
  Generating /path/to/project/versions/481b13bc369a_rev1.py ... done
  Running post write hook "spaces_to_tabs" ...
  done
```
