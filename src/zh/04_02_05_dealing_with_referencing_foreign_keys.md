# Dealing with Referencing Foreign Keys

**处理引用外键**

It is important to note that batch table operations **do not work** with foreign keys that enforce referential integrity. This because the target table is dropped; if foreign keys refer to it, this will raise an error. On SQLite, whether or not foreign keys actually enforce is controlled by the `PRAGMA FOREIGN KEYS` pragma; this pragma, if in use, must be disabled when the workflow mode proceeds. When the operation is complete, the batch-migrated table will have the same name that it started with, so those referring foreign keys will again refer to this table.

A special case is dealing with self-referring foreign keys. Here, Alembic takes a special step of recreating the self-referring foreign key as referring to the original table name, rather than at the “temp” table, so that like in the case of other foreign key constraints, when the table is renamed to its original name, the foreign key again references the correct table. This operation only works when referential integrity is disabled, consistent with the same requirement for referring foreign keys from other tables.

When SQLite’s `PRAGMA FOREIGN KEYS` mode is turned on, it does provide the service that foreign key constraints, including self-referential, will automatically be modified to point to their table across table renames, however this mode prevents the target table from being dropped as is required by a batch migration. Therefore it may be necessary to manipulate the `PRAGMA FOREIGN KEYS` setting if a migration seeks to rename a table vs. batch migrate it.
