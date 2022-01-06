# set_section_option

**set_section_option**(*section*:  [str], *name*:  [str], *value*:  [str]) → [None]

[str]: https://docs.python.org/3/library/stdtypes.html#str
[None]: https://docs.python.org/3/library/constants.html#None

Set an option programmatically within the given section.

The section is created if it doesn’t exist already. The value here will override whatever was in the .ini file.

**Parameters:**

* ***section*** – name of the section
* ***name*** – **name** of the value
* ***value*** – the value. Note that this **value** is passed to `ConfigParser.set`, which supports variable interpolation using pyformat (e.g. %(some_value)s). A raw percent sign not part of an interpolation symbol must therefore be escaped, e.g. `%%`. The given **value** may refer to another **value** already in the file using the interpolation format.
