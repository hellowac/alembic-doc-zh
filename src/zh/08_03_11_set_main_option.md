# set_main_option

**set_main_option**(*name*:  [str], *value*:  [str]) → [None]

[str]: https://docs.python.org/3/library/stdtypes.html#str
[None]: https://docs.python.org/3/library/constants.html#None

Set an option programmatically within the ‘main’ section.

This overrides whatever was in the .ini file.

**Parameters:**

* ***name*** – **name** of the value
* ***value*** – the value. Note that this **value** is passed to `ConfigParser.set`, which supports variable interpolation using pyformat (e.g. %(some_value)s). A raw percent sign not part of an interpolation symbol must therefore be escaped, e.g. `%%`. The given **value** may refer to another **value** already in the file using the interpolation format.
