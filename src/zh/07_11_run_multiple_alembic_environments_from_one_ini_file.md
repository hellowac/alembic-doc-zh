# Run Multiple Alembic Environments from one .ini file

[Working with Multiple Bases]: ../en/branches.html#multiple-bases

Long before Alembic had the “multiple bases” feature described in **[Working with Multiple Bases]**, projects had a need to maintain more than one Alembic version history in a single project, where these version histories are completely independent of each other and each refer to their own alembic_version table, either across multiple databases, schemas, or namespaces. A simple approach was added to support this, the `--name` flag on the commandline.

First, one would create an alembic.ini file of this form:

```ini
[DEFAULT]
# all defaults shared between environments go here

sqlalchemy.url = postgresql://scott:tiger@hostname/mydatabase


[schema1]
# path to env.py and migration scripts for schema1
script_location = myproject/revisions/schema1

[schema2]
# path to env.py and migration scripts for schema2
script_location = myproject/revisions/schema2

[schema3]
# path to env.py and migration scripts for schema3
script_location = myproject/revisions/db2

# this schema uses a different database URL as well
sqlalchemy.url = postgresql://scott:tiger@hostname/myotherdatabase
```

Above, in the `[DEFAULT]` section we set up a default database URL. Then we create three sections corresponding to different revision lineages in our project. Each of these directories would have its own `env.py` and set of versioning files. Then when we run the `alembic` command, we simply give it the name of the configuration we want to use:

```bash
alembic --name schema2 revision -m "new rev for schema 2" --autogenerate
```

Above, the `alembic` command makes use of the configuration in `[schema2]`, populated with defaults from the `[DEFAULT]` section.

The above approach can be automated by creating a custom front-end to the Alembic commandline as well.
