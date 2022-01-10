# Autogenerating Multiple MetaData collections

**自动生成多个元数据集合**

[MetaData]: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.MetaData

The `target_metadata` collection may also be defined as a sequence if an application has multiple **[MetaData]** collections involved:

> 如果应用程序涉及多个 **MetaData** 集合，则 `target_metadata` 集合也可以定义为一个序列：

```python
from myapp.mymodel1 import Model1Base
from myapp.mymodel2 import Model2Base
target_metadata = [Model1Base.metadata, Model2Base.metadata]
```

The sequence of **[MetaData]** collections will be consulted in order during the autogenerate process. Note that each **[MetaData]** must contain **unique** table keys (e.g. the “key” is the combination of the table’s name and schema); if two **[MetaData]** objects contain a table with the same schema/name combination, an error is raised.

> 在自动生成过程中，将按顺序查询 **[MetaData]** 集合的顺序。 请注意，每个 **[MetaData]** 必须包含唯一的表键（例如，“键”是表名和模式的组合）； 如果两个 MetaData 对象包含一个具有相同模式/名称组合的表，则会引发错误。
