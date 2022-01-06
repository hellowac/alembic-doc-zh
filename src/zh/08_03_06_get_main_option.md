# get_main_option

**get_main_option**(*name*:  [str], *default*:  [str]) → [str]

**get_main_option**(*name*:  [str], *default*:  Optional\[[str]\] = None) → Optional\[[str]\]

[str]: https://docs.python.org/3/library/stdtypes.html#str

Return an option from the ‘main’ section of the .ini file.

This defaults to being a key from the `[alembic]` section, unless the `-n/--name` flag were used to indicate a different section.
