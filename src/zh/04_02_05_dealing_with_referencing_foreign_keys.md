# Dealing with Referencing Foreign Keys

**处理引用外键**

It is important to note that batch table operations **do not work** with foreign keys that enforce referential integrity. This because the target table is dropped; if foreign keys refer to it, this will raise an error. On SQLite, whether or not foreign keys actually enforce is controlled by the `PRAGMA FOREIGN KEYS` pragma; this pragma, if in use, must be disabled when the workflow mode proceeds. When the operation is complete, the batch-migrated table will have the same name that it started with, so those referring foreign keys will again refer to this table.

> 需要注意的是，批处理表操作 **不适用于** 强制参照完整性的外键。 这是因为目标表被删除了； 如果外键引用它，这将引发错误。 在 SQLite 上，是否实际执行外键由 `PRAGMA FOREIGN KEYS` 语法控制； 如果正在使用此编译指示，则必须在工作流模式继续时禁用。 操作完成后，批量迁移的表将与开始时的名称相同，因此引用外键的人将再次引用该表。

A special case is dealing with self-referring foreign keys. Here, Alembic takes a special step of recreating the self-referring foreign key as referring to the original table name, rather than at the “temp” table, so that like in the case of other foreign key constraints, when the table is renamed to its original name, the foreign key again references the correct table. This operation only works when referential integrity is disabled, consistent with the same requirement for referring foreign keys from other tables.

> 一种特殊情况是处理自引用外键。 在这里，Alembic 采取了一个特殊的步骤，将自引用外键重新创建为引用原始表名，而不是在“临时”表中，这样就像在其他外键约束的情况下一样，当表被重命名为它的原始名称，外键再次引用正确的表。 此操作仅在禁用引用完整性时有效，与从其他表引用外键的相同要求一致。

When SQLite’s `PRAGMA FOREIGN KEYS` mode is turned on, it does provide the service that foreign key constraints, including self-referential, will automatically be modified to point to their table across table renames, however this mode prevents the target table from being dropped as is required by a batch migration. Therefore it may be necessary to manipulate the `PRAGMA FOREIGN KEYS` setting if a migration seeks to rename a table vs. batch migrate it.

> 当 SQLite 的 `PRAGMA FOREIGN KEYS` 模式开启时，它确实提供了外键约束的服务，包括自引用, 将自动修改为跨表重命名指向其表，但是此模式可防止目标表按照批量迁移的要求被删除。 因此，如果迁移试图重命名表而不是批量迁移，则可能需要操作 `PRAGMA FOREIGN KEYS` 设置。
