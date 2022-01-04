# Writing Migration Scripts to Support Script Generation

The challenge of SQL script generation is that the scripts we generate can’t rely upon any client/server database access. This means a migration script that pulls some rows into memory via a `SELECT` statement will not work in `--sql` mode. It’s also important that the Alembic directives, all of which are designed specifically to work in both “live execution” as well as “offline SQL generation” mode, are used.
