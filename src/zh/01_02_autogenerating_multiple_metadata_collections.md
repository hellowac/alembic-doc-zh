# Autogenerating Multiple MetaData collections

[MetaData]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.MetaData

The `target_metadata` collection may also be defined as a sequence if an application has multiple **[MetaData]** collections involved:

```python
from myapp.mymodel1 import Model1Base
from myapp.mymodel2 import Model2Base
target_metadata = [Model1Base.metadata, Model2Base.metadata]
```

The sequence of **[MetaData]** collections will be consulted in order during the autogenerate process. Note that each **[MetaData]** must contain **unique** table keys (e.g. the “key” is the combination of the table’s name and schema); if two **[MetaData]** objects contain a table with the same schema/name combination, an error is raised.
