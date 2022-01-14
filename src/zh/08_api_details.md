# API Details

**API详细**

[Operations]: ../zh/06_operation_reference.md
[EnvironmentContext.configure()]: ../en/runtime.html#alembic.runtime.environment.EnvironmentContext.configure
[Commands]: ../en/commands.html

Alembic’s internal API has many public integration points that can be used to extend Alembic’s functionality as well as to re-use its functionality in new ways. As the project has grown, more APIs are created and exposed for this purpose.

Direct use of the vast majority of API details discussed here is not needed for rudimentary use of Alembic; the only API that is used normally by end users is the methods provided by the **[Operations]** class, which is discussed outside of this subsection, and the parameters that can be passed to the **[EnvironmentContext.configure()]** method, used when configuring one’s `env.py` environment. However, real-world applications will usually end up using more of the internal API, in particular being able to run commands programmatically, as discussed in the section **[Commands]**.
