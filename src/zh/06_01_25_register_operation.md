# register_operation

*classmethod* **register_operation**(*name*:  [str], *sourcename*:  Optional\[[str]\] = None) → Callable

[str]: https://docs.python.org/3/library/stdtypes.html#str
[Operations]: ../zh/06_01_operations.md
[BatchOperations]: ../zh/06_02_batch_operations.md
[Operation Plugins]: ../en/api/operations.html#operation-plugins

Register a new operation for this class.

This method is normally used to add new operations to the **[Operations]** class, and possibly the **[BatchOperations]** class as well. All Alembic migration operations are implemented via this system, however the system is also available as a public API to facilitate adding custom operations.

**See also:**

* **[Operation Plugins]**
