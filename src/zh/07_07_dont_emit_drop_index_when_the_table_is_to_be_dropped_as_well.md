# Don’t emit DROP INDEX when the table is to be dropped as well

[DropIndexOp]: ../en/api/operations.html#alembic.operations.ops.DropIndexOp

MySQL may complain when dropping an index that is against a column that also has a foreign key constraint on it. If the table is to be dropped in any case, the DROP INDEX isn’t necessary. This recipe will process the set of autogenerate directives such that all **[DropIndexOp]** directives are removed against tables that themselves are to be dropped:

```python
def run_migrations_online():

    # ...

    from alembic.operations import ops

    def process_revision_directives(context, revision, directives):
        script = directives[0]

        # process both "def upgrade()", "def downgrade()"
        for directive in (script.upgrade_ops, script.downgrade_ops):

            # make a set of tables that are being dropped within
            # the migration function
            tables_dropped = set()
            for op in directive.ops:
                if isinstance(op, ops.DropTableOp):
                    tables_dropped.add((op.table_name, op.schema))

            # now rewrite the list of "ops" such that DropIndexOp
            # is removed for those tables.   Needs a recursive function.
            directive.ops = list(
                _filter_drop_indexes(directive.ops, tables_dropped)
            )

    def _filter_drop_indexes(directives, tables_dropped):
        # given a set of (tablename, schemaname) to be dropped, filter
        # out DropIndexOp from the list of directives and yield the result.

        for directive in directives:
            # ModifyTableOps is a container of ALTER TABLE types of
            # commands.  process those in place recursively.
            if isinstance(directive, ops.ModifyTableOps) and \
                    (directive.table_name, directive.schema) in tables_dropped:
                directive.ops = list(
                    _filter_drop_indexes(directive.ops, tables_dropped)
                )

                # if we emptied out the directives, then skip the
                # container altogether.
                if not directive.ops:
                    continue
            elif isinstance(directive, ops.DropIndexOp) and \
                    (directive.table_name, directive.schema) in tables_dropped:
                # we found a target DropIndexOp.   keep looping
                continue

            # otherwise if not filtered, yield out the directive
            yield directive

    # connectable = ...

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives
        )

        with context.begin_transaction():
            context.run_migrations()
```

Whereas autogenerate, when dropping two tables with a foreign key and an index, would previously generate something like:

```python
def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_b_aid'), table_name='b')
    op.drop_table('b')
    op.drop_table('a')
    # ### end Alembic commands ###
```

With the above rewriter, it generates as:

```python
def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('b')
    op.drop_table('a')
    # ### end Alembic commands ###
```