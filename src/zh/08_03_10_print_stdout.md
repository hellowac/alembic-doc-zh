# print_stdout

**print_stdout**(*text*:  [str], *arg) → None

[str]: https://docs.python.org/3/library/stdtypes.html#str
[Config.print_stdout()]: #alembic.config.Config.print_stdout

Render a message to standard out.

When **[Config.print_stdout()]** is called with additional args those arguments will formatted against the provided text, otherwise we simply output the provided text verbatim.

e.g.:

```python
>>> config.print_stdout('Some text %s', 'arg')
Some Text arg
```
