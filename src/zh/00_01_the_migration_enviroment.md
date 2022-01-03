# 迁移环境

[Mako]: http://www.makotemplates.org/

Usage of Alembic starts with creation of the *Migration Environment*. This is a directory of scripts that is specific to a particular application. The migration environment is created just once, and is then maintained along with the application’s source code itself. The environment is created using the *init* command of Alembic, and is then customizable to suit the specific needs of the application.

使用 Alembic 从创建***迁移环境***开始。这是独立于应用程序的特别脚本目录。迁移环境只创建一次，然后与应用程序的源代码本身一起维护。该环境是使用 Alembic 的 `init` 命令创建的，然后可以自定义以满足应用程序的特别需求。

The structure of this environment, including some generated migration scripts, looks like:

这个环境的结构，包括一些生成的迁移脚本，看起来像：

```text
yourproject/
    alembic/
        env.py
        README
        script.py.mako
        versions/
            3512b954651e_add_account.py
            2b1ae634e5cd_add_order_id.py
            3adcc9a56557_rename_username_field.py
```

The directory includes these directories/files:

该目录包括以下目录/文件：

* **yourproject** - this is the root of your application’s source code, or some directory within it.
* **yourproject** - 这是应用程序源代码的根目录，或其中的某个目录。
* **alembic** - this directory lives within your application’s source tree and is the home of the migration environment. It can be named anything, and a project that uses multiple databases may even have more than one.
* **alembic** - 该目录位于应用程序的源代码树中，是迁移环境的主目录。 它可以命名为任何名称，一个使用多个数据库的项目甚至可能有多个。
* **env.py** - This is a Python script that is run whenever the alembic migration tool is invoked. At the very least, it contains instructions to configure and generate a SQLAlchemy engine, procure a connection from that engine along with a transaction, and then invoke the migration engine, using the connection as a source of database connectivity.
* **env.py** - 这是一个 Python 脚本，只要调用 alembic 迁移工具就会运行。至少，它包含配置和生成 SQLAlchemy 引擎的指令，从该引擎获取连接以及事务，然后调用迁移引擎，使用该连接作为数据库连接的来源。

    The `env.py` script is part of the generated environment so that the way migrations run is entirely customizable. The exact specifics of how to connect are here, as well as the specifics of how the migration environment are invoked. The script can be modified so that multiple engines can be operated upon, custom arguments can be passed into the migration environment, application-specific libraries and models can be loaded in and made available.

    `env.py` 脚本是生成环境的一部分，因此迁移运行的方式是完全可定制的。 如何连接的确切细节在这里，以及如何调用迁移环境的细节。 可以修改脚本以便可以操作多个引擎，可以将自定义参数传递到迁移环境中，可以加载特定于应用程序的库和模型并使其可用。

    Alembic includes a set of initialization templates which feature different varieties of `env.py` for different use cases.

    Alembic 包含一组初始化模板，其中包含针对不同用例的不同类型的 `env.py`。

* **README** - included with the various environment templates, should have something informative.
* **README** - 包含在各种环境模板中，应该有的一些说明信息。
* **script.py.mako** - This is a [Mako] template file which is used to generate new migration scripts. Whatever is here is used to generate new files within `versions/`. This is scriptable so that the structure of each migration file can be controlled, including standard imports to be within each, as well as changes to the structure of the `upgrade()` and `downgrade()` functions. For example, the `multidb` environment allows for multiple functions to be generated using a naming scheme `upgrade_engine1()`, `upgrade_engine2()`.
* **script.py.mako** - 这是一个 [Mako] 模板文件，用于生成新的迁移脚本。 这里的任何内容都用于在 `versions/` 中生成新文件。 这是可编的写脚本，因此可以控制每个迁移文件的结构，包括每个迁移文件中的标准导入，以及对 `upgrade()` 和 `downgrade()` 函数结构的更改。 例如，多数据库(multidb)环境允许使用命名方案`upgrade_engine1()`、`upgrade_engine2()`生成多个函数。
* **versions/** - This directory holds the individual version scripts. Users of other migration tools may notice that the files here don’t use ascending integers, and instead use a partial GUID approach. In Alembic, the ordering of version scripts is relative to directives within the scripts themselves, and it is theoretically possible to “splice” version files in between others, allowing migration sequences from different branches to be merged, albeit carefully by hand.
* **versions/** 该目录包含各个版本的脚本。 其他迁移工具的用户可能会注意到这里的文件不使用升序整数，而是使用部分 GUID 方法。 在 Alembic 中，版本脚本的排序与脚本本身内的指令相关，理论上可以在其他版本文件之间“拼接”版本文件，允许合并来自不同分支的迁移序列，尽管需要小心的手动合并。
