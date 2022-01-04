# Writing Custom Hooks as Python Functions

[write_hooks.register()]: http://localhost:3002/en/api/script.html#alembic.script.write_hooks.register

The previous section illustrated how to run command-line code formatters, through the use of a post write hook provided by Alembic known as `console_scripts`. This hook is in fact a Python function that is registered under that name using a registration function that may be used to register other types of hooks as well.

To illustrate, we will use the example of a short Python function that wants to rewrite the generated code to use tabs instead of four spaces. For simplicity, we will illustrate how this function can be present directly in the `env.py` file. The function is declared and registered using the [write_hooks.register()] decorator:

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

```bash
$ alembic revision -m "rev1"
  Generating /path/to/project/versions/481b13bc369a_rev1.py ... done
  Running post write hook "spaces_to_tabs" ...
  done
```
