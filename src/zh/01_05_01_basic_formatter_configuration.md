# Basic Formatter Configuration

[setuptools entrypoint]: https://setuptools.readthedocs.io/en/latest/pkg_resources.html#entry-points
[zimports]: https://pypi.org/project/zimports/

The `alembic.ini` samples now include commented-out configuration illustrating how to configure code-formatting tools to run against the newly generated file path. Example:

> `alembic.ini` 示例现在包含注释掉的配置，说明如何配置代码格式化工具以针对新生成的文件路径运行。 例子：

```ini
[post_write_hooks]

# format using "black"
hooks=black

black.type = console_scripts
black.entrypoint = black
black.options = -l 79
```

Above, we configure `hooks` to be a single post write hook labeled `"black"`. Note that this label is arbitrary. We then define the configuration for the `"black"` post write hook, which includes:

> 上面，我们将 `hooks` 配置为标记为 `"black"` 的单个 post write hook。 请注意，此标签是任意的。 然后我们定义了`"black"` post write hook的配置，包括：

* `type` - this is the type of hook we are running. Alembic includes a hook runner called `"console_scripts"`, which is specifically a Python function that uses `subprocess.run()` to invoke a separate Python script against the revision file. For a custom-written hook function, this configuration variable would refer to the name under which the custom hook was registered; see the next section for an example.

> * `type` - 这是我们正在运行的钩子类型。 Alembic 包含一个名为 `"console_scripts"` 的钩子运行器，它专门是一个 Python 函数，它使用 `subprocess.run()` 针对修订文件调用单独的 Python 脚本。 对于自定义编写的钩子函数，此配置变量将引用注册自定义钩子的名称； 有关示例，请参见下一节。

The following configuration options are specific to the `"console_scripts"` hook runner:

> 以下配置选项特定于 `"console_scripts"` 钩子运行：

* `entrypoint` - the name of the [setuptools entrypoint] that is used to define the console script. Within the scope of standard Python console scripts, this name will match the name of the shell command that is usually run for the code formatting tool, in this case `black`.
* `options` - a line of command-line options that will be passed to the code formatting tool. In this case, we want to run the command `black /path/to/revision.py -l 79`. By default, the revision path is positioned as the first argument. In order specify a different position, we can use the `REVISION_SCRIPT_FILENAME` token as illustrated by the subsequent examples.

    **Note**: Make sure options for the script are provided such that it will rewrite the input file **in place**. For example, when running autopep8, the `--in-place` option should be provided:

    ```ini
    [post_write_hooks]
    hooks = autopep8
    autopep8.type = console_scripts
    autopep8.entrypoint = autopep8
    autopep8.options = --in-place REVISION_SCRIPT_FILENAME
    ```
* `cwd` - optional working directory from which the console script is run.

> * `entrypoint` - 用于定义控制台脚本的 [setuptools entrypoint] 的名称。 在标准 Python 控制台脚本的范围内，此名称将匹配通常为代码格式化工具运行的 shell 命令的名称，在本例中为`“black”`。
> * `options` - 将传递给代码格式化工具的命令行选项。 在这种情况下，我们要运行命令“black /path/to/revision.py -l 79”。 默认情况下，修订路径定位为第一个参数。 为了指定不同的位置，我们可以使用 `REVISION_SCRIPT_FILENAME` 标记，如后续示例所示。
>
>   **注意:** 确保提供了脚本选项，以便它会在 **原地** 重写输入文件。 例如，在运行 `autopep8` 时，应提供 `--in-place` 选项：
>
>   ```ini
>   [post_write_hooks]
>   hooks = autopep8
>   autopep8.type = console_scripts
>   autopep8.entrypoint = autopep8
>   autopep8.options = --in-place REVISION_SCRIPT_FILENAME
>   ```
>
> * `cwd` - 运行控制台脚本的可选工作目录。

When running `alembic revision -m "rev1"`, we will now see the `black` tool’s output as well:

> 当运行 `alembic revision -m "rev1"` 时，我们现在也会看到 `black` 工具的输出：

```bash
$ alembic revision -m "rev1"
  Generating /path/to/project/versions/481b13bc369a_rev1.py ... done
  Running post write hook "black" ...
reformatted /path/to/project/versions/481b13bc369a_rev1.py
All done! ✨ 🍰 ✨
1 file reformatted.
  done
```

Hooks may also be specified as a list of names, which correspond to hook runners that will run sequentially. As an example, we can also run the [zimports] import rewriting tool (written by Alembic’s author) subsequent to running the `black` tool, using a configuration as follows:

> 钩子也可以指定为名称列表，这些名称对应于将按顺序运行的挂钩运行器。 例如，我们还可以在运行 `black` 工具之后运行 [zimports] 导入重写工具（由 Alembic 的作者编写），使用如下配置：

```ini
[post_write_hooks]

# format using "black", then "zimports"
hooks=black, zimports

black.type = console_scripts
black.entrypoint = black
black.options = -l 79 REVISION_SCRIPT_FILENAME

zimports.type = console_scripts
zimports.entrypoint = zimports
zimports.options = --style google REVISION_SCRIPT_FILENAME
```

When using the above configuration, a newly generated revision file will be processed first by the “black” tool, then by the “zimports” tool.

> 使用上述配置时，新生成的修订文件将首先由“black”工具处理，然后由“zimports”工具处理。

Alternatively, one can run pre-commit itself as follows:

> 或者，可以按如下方式运行预提交本身：

```ini
[post_write_hooks]

hooks = pre-commit

pre-commit.type = console_scripts
pre-commit.entrypoint = pre-commit
pre-commit.options = run --files REVISION_SCRIPT_FILENAME
pre-commit.cwd = %(here)s
```

(The last line helps to ensure that the `.pre-commit-config.yaml` file will always be found, regardless of from where the hook was called.)

> (最后一行有助于确保始终可以找到 `.pre-commit-config.yaml` 文件，无论从何处调用钩子。)
