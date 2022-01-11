# Controlling Table Reflection

**控制表反射**

[Table]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table
 [表]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table
[reflect_args]: ../zh/06_01_03_batch_alter_table.md#reflect_args
[reflect_kwargs]: ../zh/06_01_03_batch_alter_table.md#reflect_kwargs
[Column]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column
[Boolean]: https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Boolean
[column_reflect()]: https://docs.sqlalchemy.org/en/14/core/events.html#sqlalchemy.events.DDLEvents.column_reflect
[Working in Offline Mode]: ../zh/04_03_working_in_offline_mode.md
[在脱机模式下工作]: ../zh/04_03_working_in_offline_mode.md

The **[Table]** object that is reflected when “move and copy” proceeds is performed using the standard `autoload=True` approach. This call can be affected using the **[reflect_args]** and **[reflect_kwargs]** arguments. For example, to override a **[Column]** within the reflection process such that a **[Boolean]** object is reflected with the `create_constraint` flag set to `False`:

> 使用标准 `autoload=True` 方法执行 **“移动和复制”** 时反射的 **[Table]** 对象。 使用 **[reflect_args]** 和 **[reflect_kwargs]** 参数可以影响此调用。 例如，要在反射过程中覆盖 **[Column]**，以便在将 `create_constraint` 标志设置为 `False` 的情况下反射布尔对象：

```python
with self.op.batch_alter_table(
    "bar",
    reflect_args=[Column('flag', Boolean(create_constraint=False))]
) as batch_op:
    batch_op.alter_column(
        'flag', new_column_name='bflag', existing_type=Boolean)
```

Another use case, add a listener to the **[Table]** as it is reflected so that special logic can be applied to columns or types, using the **[column_reflect()]** event:

> 另一个用例，使用 **[column_reflect()]** 事件在 **[表]** 反射时向 **[表]** 添加一个侦听器，以便可以将特殊逻辑应用于列或类型：

```python
def listen_for_reflect(inspector, table, column_info):
    "correct an ENUM type"
    if column_info['name'] == 'my_enum':
        column_info['type'] = Enum('a', 'b', 'c')

with self.op.batch_alter_table(
    "bar",
    reflect_kwargs=dict(
        listeners=[
            ('column_reflect', listen_for_reflect)
        ]
    )
) as batch_op:
    batch_op.alter_column(
        'flag', new_column_name='bflag', existing_type=Boolean)
```

The reflection process may also be bypassed entirely by sending a pre-fabricated **[Table]** object; see **[Working in Offline Mode]** for an example.

> 反射过程也可以通过发送一个预制的 **[Table]** 对象来完全绕过； 有关示例，请参阅[在脱机模式下工作]。
