# Basic Formatter Configuration

[setuptools entrypoint]: https://setuptools.readthedocs.io/en/latest/pkg_resources.html#entry-points
[zimports]: https://pypi.org/project/zimports/

The `alembic.ini` samples now include commented-out configuration illustrating how to configure code-formatting tools to run against the newly generated file path. Example:

```ini
[post_write_hooks]

# format using "black"
hooks=black

black.type = console_scripts
black.entrypoint = black
black.options = -l 79
```

Above, we configure `hooks` to be a single post write hook labeled `"black"`. Note that this label is arbitrary. We then define the configuration for the `"black"` post write hook, which includes:

* `type` - this is the type of hook we are running. Alembic includes a hook runner called `"console_scripts"`, which is specifically a Python function that uses `subprocess.run()` to invoke a separate Python script against the revision file. For a custom-written hook function, this configuration variable would refer to the name under which the custom hook was registered; see the next section for an example.

The following configuration options are specific to the `"console_scripts"` hook runner:

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

When running `alembic revision -m "rev1"`, we will now see the `black` tool’s output as well:

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

Alternatively, one can run pre-commit itself as follows:

```ini
[post_write_hooks]

hooks = pre-commit

pre-commit.type = console_scripts
pre-commit.entrypoint = pre-commit
pre-commit.options = run --files REVISION_SCRIPT_FILENAME
pre-commit.cwd = %(here)s
```

(The last line helps to ensure that the `.pre-commit-config.yaml` file will always be found, regardless of from where the hook was called.)
