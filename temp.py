
import json
from pyquery import PyQuery


def main():

    html2 = """
    <li class="toctree-l1"><a class="reference internal" href="changelog.html">Changelog</a><ul>
    <li class="toctree-l2"><a class="reference internal" href="changelog.html#change-1.7.6">1.7.6</a><ul>
    <li class="toctree-l3"><a class="reference internal" href="changelog.html#change-1.7.6-usecase">usecase</a></li>
    <li class="toctree-l3"><a class="reference internal" href="changelog.html#change-1.7.6-bug">bug</a></li>
    """

    query = PyQuery(html2)

    prefix_temp = './zh/08_08_{index:0>2d}'  # 07_

    for index, line in enumerate(query('a').items(), start=1):

        prefix = prefix_temp.format(index=index)

        title = line.text()

        link = title.lower()
        link = link.replace("'", '')
        link = link.replace(".", '')
        link = link.replace("(", '')
        link = link.replace(")", '')
        link = link.replace("’", '')
        link = link.replace("-", '')
        link = link.replace(" ", '_')

        print(f"- [{title}]({prefix}_{link}.md)")


def parse_section():

    html2 = """
        <section id="create-revision-migrations">
<h3>Create Revision Migrations<a class="headerlink" href="#create-revision-migrations" title="Permalink to this headline">¶</a></h3>
<p>Finally, we can illustrate how we would “revise” these objects.
Let’s consider we added a new column <code class="docutils literal notranslate"><span class="pre">email</span></code> to our <code class="docutils literal notranslate"><span class="pre">customer</span></code> table:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ alembic revision -m "add email col"
</pre></div>
</div>
<p>The migration is:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>

<span class="c1"># revision identifiers, used by Alembic.</span>
<span class="n">revision</span> <span class="o">=</span> <span class="s1">'191a2d20b025'</span>
<span class="n">down_revision</span> <span class="o">=</span> <span class="s1">'28af9800143f'</span>
<span class="n">branch_labels</span> <span class="o">=</span> <span class="kc">None</span>
<span class="n">depends_on</span> <span class="o">=</span> <span class="kc">None</span>

<span class="kn">from</span> <span class="nn">alembic</span> <span class="kn">import</span> <span class="n">op</span>
<span class="kn">import</span> <span class="nn">sqlalchemy</span> <span class="k">as</span> <span class="nn">sa</span>


<span class="k">def</span> <span class="nf">upgrade</span><span class="p">():</span>
    <span class="n">op</span><span class="o">.</span><span class="n">add_column</span><span class="p">(</span><span class="s2">"customer"</span><span class="p">,</span> <span class="n">sa</span><span class="o">.</span><span class="n">Column</span><span class="p">(</span><span class="s2">"email"</span><span class="p">,</span> <span class="n">sa</span><span class="o">.</span><span class="n">String</span><span class="p">()))</span>


<span class="k">def</span> <span class="nf">downgrade</span><span class="p">():</span>
    <span class="n">op</span><span class="o">.</span><span class="n">drop_column</span><span class="p">(</span><span class="s2">"customer"</span><span class="p">,</span> <span class="s2">"email"</span><span class="p">)</span>
</pre></div>
</div>
<p>We now need to recreate the <code class="docutils literal notranslate"><span class="pre">customer_view</span></code> view and the
<code class="docutils literal notranslate"><span class="pre">add_customer_sp</span></code> function.   To include downgrade capability, we will
need to refer to the <strong>previous</strong> version of the construct; the
<code class="docutils literal notranslate"><span class="pre">replace_view()</span></code> and <code class="docutils literal notranslate"><span class="pre">replace_sp()</span></code> operations we’ve created make
this possible, by allowing us to refer to a specific, previous revision.
the <code class="docutils literal notranslate"><span class="pre">replaces</span></code> and <code class="docutils literal notranslate"><span class="pre">replace_with</span></code> arguments accept a dot-separated
string, which refers to a revision number and an object name, such
as <code class="docutils literal notranslate"><span class="pre">"28af9800143f.customer_view"</span></code>.  The <code class="docutils literal notranslate"><span class="pre">ReversibleOp</span></code> class makes use
of the <a class="reference internal" href="ops.html#alembic.operations.Operations.get_context" title="alembic.operations.Operations.get_context"><code class="xref py py-meth docutils literal notranslate"><span class="pre">Operations.get_context()</span></code></a> method to locate the version file
we refer to:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ alembic revision -m "update views/sp"
</pre></div>
</div>
<p>The migration:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>

<span class="c1"># revision identifiers, used by Alembic.</span>
<span class="n">revision</span> <span class="o">=</span> <span class="s1">'199028bf9856'</span>
<span class="n">down_revision</span> <span class="o">=</span> <span class="s1">'191a2d20b025'</span>
<span class="n">branch_labels</span> <span class="o">=</span> <span class="kc">None</span>
<span class="n">depends_on</span> <span class="o">=</span> <span class="kc">None</span>

<span class="kn">from</span> <span class="nn">alembic</span> <span class="kn">import</span> <span class="n">op</span>
<span class="kn">import</span> <span class="nn">sqlalchemy</span> <span class="k">as</span> <span class="nn">sa</span>

<span class="kn">from</span> <span class="nn">foo</span> <span class="kn">import</span> <span class="n">ReplaceableObject</span>

<span class="n">customer_view</span> <span class="o">=</span> <span class="n">ReplaceableObject</span><span class="p">(</span>
    <span class="s2">"customer_view"</span><span class="p">,</span>
    <span class="s2">"SELECT name, order_count, email "</span>
    <span class="s2">"FROM customer WHERE order_count &gt; 0"</span>
<span class="p">)</span>

<span class="n">add_customer_sp</span> <span class="o">=</span> <span class="n">ReplaceableObject</span><span class="p">(</span>
    <span class="s2">"add_customer_sp(name varchar, order_count integer, email varchar)"</span><span class="p">,</span>
    
<span class="p">)</span>


<span class="k">def</span> <span class="nf">upgrade</span><span class="p">():</span>
    <span class="n">op</span><span class="o">.</span><span class="n">replace_view</span><span class="p">(</span><span class="n">customer_view</span><span class="p">,</span> <span class="n">replaces</span><span class="o">=</span><span class="s2">"28af9800143f.customer_view"</span><span class="p">)</span>
    <span class="n">op</span><span class="o">.</span><span class="n">replace_sp</span><span class="p">(</span><span class="n">add_customer_sp</span><span class="p">,</span> <span class="n">replaces</span><span class="o">=</span><span class="s2">"28af9800143f.add_customer_sp"</span><span class="p">)</span>


<span class="k">def</span> <span class="nf">downgrade</span><span class="p">():</span>
    <span class="n">op</span><span class="o">.</span><span class="n">replace_view</span><span class="p">(</span><span class="n">customer_view</span><span class="p">,</span> <span class="n">replace_with</span><span class="o">=</span><span class="s2">"28af9800143f.customer_view"</span><span class="p">)</span>
    <span class="n">op</span><span class="o">.</span><span class="n">replace_sp</span><span class="p">(</span><span class="n">add_customer_sp</span><span class="p">,</span> <span class="n">replace_with</span><span class="o">=</span><span class="s2">"28af9800143f.add_customer_sp"</span><span class="p">)</span>
</pre></div>
</div>
<p>Above, instead of using <code class="docutils literal notranslate"><span class="pre">create_view()</span></code>, <code class="docutils literal notranslate"><span class="pre">create_sp()</span></code>,
<code class="docutils literal notranslate"><span class="pre">drop_view()</span></code>, and <code class="docutils literal notranslate"><span class="pre">drop_sp()</span></code> methods, we now use <code class="docutils literal notranslate"><span class="pre">replace_view()</span></code> and
<code class="docutils literal notranslate"><span class="pre">replace_sp()</span></code>.  The replace operation we’ve built always runs a DROP <em>and</em>
a CREATE.  Running an upgrade to head we see:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [sqlalchemy.engine.base.Engine] BEGIN (implicit)
INFO  [sqlalchemy.engine.base.Engine] select relname from pg_class c join pg_namespace n on n.oid=c.relnamespace where pg_catalog.pg_table_is_visible(c.oid) and relname=%(name)s
INFO  [sqlalchemy.engine.base.Engine] {'name': u'alembic_version'}
INFO  [sqlalchemy.engine.base.Engine] SELECT alembic_version.version_num
FROM alembic_version
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [alembic.runtime.migration] Running upgrade 28af9800143f -&gt; 191a2d20b025, add email col
INFO  [sqlalchemy.engine.base.Engine] ALTER TABLE customer ADD COLUMN email VARCHAR
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] UPDATE alembic_version SET version_num='191a2d20b025' WHERE alembic_version.version_num = '28af9800143f'
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [alembic.runtime.migration] Running upgrade 191a2d20b025 -&gt; 199028bf9856, update views/sp
INFO  [sqlalchemy.engine.base.Engine] DROP VIEW customer_view
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] CREATE VIEW customer_view AS SELECT name, order_count, email FROM customer WHERE order_count &gt; 0
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] DROP FUNCTION add_customer_sp(name varchar, order_count integer)
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] CREATE FUNCTION add_customer_sp(name varchar, order_count integer, email varchar)
    RETURNS integer AS $$
    BEGIN
        insert into customer (name, order_count, email)
        VALUES (in_name, in_order_count, email);
    END;
    $$ LANGUAGE plpgsql;

INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] UPDATE alembic_version SET version_num='199028bf9856' WHERE alembic_version.version_num = '191a2d20b025'
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] COMMIT
</pre></div>
</div>
<p>After adding our new <code class="docutils literal notranslate"><span class="pre">email</span></code> column, we see that both <code class="docutils literal notranslate"><span class="pre">customer_view</span></code>
and <code class="docutils literal notranslate"><span class="pre">add_customer_sp()</span></code> are dropped before the new version is created.
If we downgrade back to the old version, we see the old version of these
recreated again within the downgrade for this migration:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span></span>$ alembic downgrade 28af9800143
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [sqlalchemy.engine.base.Engine] BEGIN (implicit)
INFO  [sqlalchemy.engine.base.Engine] select relname from pg_class c join pg_namespace n on n.oid=c.relnamespace where pg_catalog.pg_table_is_visible(c.oid) and relname=%(name)s
INFO  [sqlalchemy.engine.base.Engine] {'name': u'alembic_version'}
INFO  [sqlalchemy.engine.base.Engine] SELECT alembic_version.version_num
FROM alembic_version
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [alembic.runtime.migration] Running downgrade 199028bf9856 -&gt; 191a2d20b025, update views/sp
INFO  [sqlalchemy.engine.base.Engine] DROP VIEW customer_view
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] CREATE VIEW customer_view AS SELECT name, order_count FROM customer WHERE order_count &gt; 0
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] DROP FUNCTION add_customer_sp(name varchar, order_count integer, email varchar)
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] CREATE FUNCTION add_customer_sp(name varchar, order_count integer)
    RETURNS integer AS $$
    BEGIN
        insert into customer (name, order_count)
        VALUES (in_name, in_order_count);
    END;
    $$ LANGUAGE plpgsql;

INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] UPDATE alembic_version SET version_num='191a2d20b025' WHERE alembic_version.version_num = '199028bf9856'
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [alembic.runtime.migration] Running downgrade 191a2d20b025 -&gt; 28af9800143f, add email col
INFO  [sqlalchemy.engine.base.Engine] ALTER TABLE customer DROP COLUMN email
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] UPDATE alembic_version SET version_num='28af9800143f' WHERE alembic_version.version_num = '191a2d20b025'
INFO  [sqlalchemy.engine.base.Engine] {}
INFO  [sqlalchemy.engine.base.Engine] COMMIT
</pre></div>
</div>
</section>
    """

    query = PyQuery(html2)

    batch_op_md_file_dict = {
        "#alembic.operations.BatchOperations": "../zh/06_02_batch_operations.md",
        "#alembic.operations.BatchOperations.add_column": "../zh/06_02_01_add_column.md",
        "#alembic.operations.BatchOperations.alter_column": "../zh/06_02_02_alter_column.md",
        "#alembic.operations.BatchOperations.create_check_constraint": "../zh/06_02_03_create_check_constraint.md",
        "#alembic.operations.BatchOperations.create_exclude_constraint": "../zh/06_02_04_create_exclude_constraint.md",
        "#alembic.operations.BatchOperations.create_foreign_key": "../zh/06_02_05_create_foreign_key.md",
        "#alembic.operations.BatchOperations.create_index": "../zh/06_02_06_create_index.md",
        "#alembic.operations.BatchOperations.create_primary_key": "../zh/06_02_07_create_primary_key.md",
        "#alembic.operations.BatchOperations.create_table_comment": "../zh/06_02_08_create_table_comment.md",
        "#alembic.operations.BatchOperations.create_unique_constraint": "../zh/06_02_09_create_unique_constraint.md",
        "#alembic.operations.BatchOperations.drop_column": "../zh/06_02_10_drop_column.md",
        "#alembic.operations.BatchOperations.drop_constraint": "../zh/06_02_11_drop_constraint.md",
        "#alembic.operations.BatchOperations.drop_index": "../zh/06_02_12_drop_index.md",
        "#alembic.operations.BatchOperations.drop_table_comment": "../zh/06_02_13_drop_table_comment.md"
    }
    op_md_file_dict = {
        "#alembic.operations.Operations": "../zh/06_01_operations.md",
        "#alembic.operations.Operations.add_column": "../zh/06_01_01_add_column.md",
        "#alembic.operations.Operations.alter_column": "../zh/06_01_02_alter_column.md",
        "#alembic.operations.Operations.alter_column.params.comment": "../zh/06_01_02_alter_column.md#params.comment",
        "#alembic.operations.Operations.batch_alter_table": "../zh/06_01_03_batch_alter_table.md",
        "#alembic.operations.Operations.bulk_insert": "../zh/06_01_04_bulk_insert.md",
        "#alembic.operations.Operations.create_check_constraint": "../zh/06_01_05_create_check_constraint.md",
        "#alembic.operations.Operations.create_exclude_constraint": "../zh/06_01_06_create_exclude_constraint.md",
        "#alembic.operations.Operations.create_foreign_key": "../zh/06_01_07_create_foreign_key.md",
        "#alembic.operations.Operations.create_index": "../zh/06_01_08_create_index.md",
        "#alembic.operations.Operations.create_primary_key": "../zh/06_01_09_create_primary_key.md",
        "#alembic.operations.Operations.create_table": "../zh/06_01_10_create_table.md",
        "#alembic.operations.Operations.create_table_comment": "../zh/06_01_11_create_table_comment.md",
        "#alembic.operations.Operations.create_unique_constraint": "../zh/06_01_12_create_unique_constraint.md",
        "#alembic.operations.Operations.drop_column": "../zh/06_01_13_drop_column.md",
        "#alembic.operations.Operations.drop_constraint": "../zh/06_01_14_drop_constraint.md",
        "#alembic.operations.Operations.drop_index": "../zh/06_01_15_drop_index.md",
        "#alembic.operations.Operations.drop_table": "../zh/06_01_16_drop_table.md",
        "#alembic.operations.Operations.drop_table_comment": "../zh/06_01_17_drop_table_comment.md",
        "#alembic.operations.Operations.execute": "../zh/06_01_18_execute.md",
        "#alembic.operations.Operations.f": "../zh/06_01_19_f.md",
        "#alembic.operations.Operations.get_bind": "../zh/06_01_20_get_bind.md",
        "#alembic.operations.Operations.get_context": "../zh/06_01_21_get_context.md",
        "#alembic.operations.Operations.implementation_for": "../zh/06_01_22_implementation_for.md",
        "#alembic.operations.Operations.inline_literal": "../zh/06_01_23_inline_literal.md",
        "#alembic.operations.Operations.invoke": "../zh/06_01_24_invoke.md",
        "#alembic.operations.Operations.register_operation": "../zh/06_01_25_register_operation.md",
        "#alembic.operations.Operations.rename_table": "../zh/06_01_26_rename_table.md"
    }

    links = {}
    texts = []


    title = query.children('h2').text() or query.children('h3').text()
    title = title.replace('¶', '')

    print(f'# {title}')

    for p in query('p').items():

        _a_tags = {a.text(): a.attr('href') for a in p('a').items() }
        code_tags = [code.text() for code in p('code').items() ]
        strong_tags = [strong.text() for strong in p('strong').items() ]

        # 替换成本地文件路径
        a_tags = {}
        for a, link in _a_tags.items():
            if link in op_md_file_dict:
                a_tags[a] = op_md_file_dict[link]
            elif link in batch_op_md_file_dict:
                a_tags[a] = batch_op_md_file_dict[link]
            elif a == '¶':
                continue
            else:
                a_tags[a] = link

        text = p.text()

        # 处理每个P标签里面的特殊字符
        words = []
        
        for index, word in enumerate(text.split(' ')):
            if index == 0 and word.startswith('Note'):  # Note 
                word = f'> **{word}:**'
            
            if index == 0 and word.startswith('See also'):  # See also 
                word = f'> **{word}:**'
            
            if word.endswith('¶'):  # 参数 斜体
                word = f'* ***{word[:-1]}***'

                # 新增参数flag
                if parameter_flag:
                    texts.append('**Parameters:**')
                    parameter_flag = False
            
            words.append(word)

        text = ' '.join(words)

        if text == 'See also':  # See also 
            text = f'**{text}:**'

        # 单行代码
        for code in code_tags:
            if code not in a_tags:
                text = text.replace(f" {code} ", f' `{code}` ')
                text = text.replace(f" {code},", f' `{code}`,')
                text = text.replace(f" {code}:", f' `{code}`:')
                text = text.replace(f" {code}.", f' `{code}`.')
                text = text.replace(f" {code})", f' `{code}`)')

        # 加粗
        for strong in strong_tags:
            if strong not in a_tags:
                text = text.replace(f" {strong} ", f' **{strong}** ')
                text = text.replace(f" {strong},", f' **{strong}**,')
                text = text.replace(f" {strong}:", f' **{strong}**:')
                text = text.replace(f" {strong};", f' **{strong}**;')

        # 链接
        for a, href in a_tags.items():
            text = text.replace(f" {a} ", f' **[{a}]** ')
            text = text.replace(f" {a},", f' **[{a}]**,')
            text = text.replace(f" {a}.", f' **[{a}]**.')
            text = text.replace(f" {a}:", f' **[{a}]**:')

            if a == text:
                text = text.replace(f"{a}", f'* **[{a}]** ')
        
        links.update(a_tags)
        texts.append(text)

        if text.endswith(':'):
            texts.append('```python')
            texts.append('```')

        # print(a_tags)
        # print(code_tags)
    
    links_text = []

    for a_text, href in links.items():
        _href = href
        if not (href.startswith('http') or href.startswith('#') or href.startswith('../zh')):
            _href = f'../en/{href}'

        links_text.append(f'[{a_text}]: {_href}')

    print('\n')
    print('\n'.join(links_text))
    print('\n')
    print('\n\n'.join(texts))

def parse_method_define(dt: PyQuery):
    """ 解析定义的方法 """

    method_name = dt('span.sig-name.descname').text()

    paramters = []
    links = {}

    for parameter in dt('em.sig-param').items():
        p_text = parameter.text()

        if p_text.startswith('*'):
            paramters.append(p_text)
            continue
            
        if ':' not in p_text:
            paramters.append(p_text)
            continue

        p_name, p_type = p_text.split(":", 1)

        p_name = f'*{p_name}*'  # 斜体
        p_type = p_type.replace('[', '\[')  # 转义
        p_type = p_type.replace(']', '\]')  # 转义

        a_tags = {a.text(): a.attr('href') for a in parameter('a').items() }
        links.update(a_tags)

        for a_name in a_tags.keys():
            p_type = p_type.replace(a_name, f'[{a_name}]')

        paramters.append(f'{p_name}: {p_type}')
    
    _return_type_text = dt('.sig-return-typehint').text()
    _return_type_text = _return_type_text.replace('[', '\[')  # 转义
    _return_type_text = _return_type_text.replace(']', '\]')  # 转义
    
    paramters_str = ', '.join(paramters)
    method_name = f"**{method_name}**({paramters_str})"

    if _return_type_text:
        method_name = f"{method_name} → {_return_type_text}"
    
    return method_name, links


def main2():
    html = """
        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.BatchOperations.drop_table_comment">
        <span class="sig-name descname"><span class="pre">drop_table_comment</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">existing_comment</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#alembic.operations.BatchOperations.drop_table_comment" title="Permalink to this definition">¶</a></dt>
        <dd><p>Issue a “drop table comment” operation to
        remove an existing comment set on a table using the current
        batch operations context.</p>
        <div class="versionadded">
        <p><span class="versionmodified added">New in version 1.6.0.</span></p>
        </div>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><p><span class="target" id="alembic.operations.BatchOperations.drop_table_comment.params.existing_comment"></span><strong>existing_comment</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.BatchOperations.drop_table_comment.params.existing_comment">¶</a> – An optional string value of a comment already
        registered on the specified table.</p>
        </dd>
        </dl>
        </dd></dl>
    """

    query = PyQuery(html)

    method_name = query('dt').text()
    method_name = method_name.replace('¶', '')

    method_name, links = parse_method_define(query('dt'))

    print(f"{method_name}")

    batch_op_md_file_dict = {
        "#alembic.operations.BatchOperations": "../zh/06_02_batch_operations.md",
        "#alembic.operations.BatchOperations.add_column": "../zh/06_02_01_add_column.md",
        "#alembic.operations.BatchOperations.alter_column": "../zh/06_02_02_alter_column.md",
        "#alembic.operations.BatchOperations.create_check_constraint": "../zh/06_02_03_create_check_constraint.md",
        "#alembic.operations.BatchOperations.create_exclude_constraint": "../zh/06_02_04_create_exclude_constraint.md",
        "#alembic.operations.BatchOperations.create_foreign_key": "../zh/06_02_05_create_foreign_key.md",
        "#alembic.operations.BatchOperations.create_index": "../zh/06_02_06_create_index.md",
        "#alembic.operations.BatchOperations.create_primary_key": "../zh/06_02_07_create_primary_key.md",
        "#alembic.operations.BatchOperations.create_table_comment": "../zh/06_02_08_create_table_comment.md",
        "#alembic.operations.BatchOperations.create_unique_constraint": "../zh/06_02_09_create_unique_constraint.md",
        "#alembic.operations.BatchOperations.drop_column": "../zh/06_02_10_drop_column.md",
        "#alembic.operations.BatchOperations.drop_constraint": "../zh/06_02_11_drop_constraint.md",
        "#alembic.operations.BatchOperations.drop_index": "../zh/06_02_12_drop_index.md",
        "#alembic.operations.BatchOperations.drop_table_comment": "../zh/06_02_13_drop_table_comment.md"
    }
    op_md_file_dict = {
        "#alembic.operations.Operations": "../zh/06_01_operations.md",
        "#alembic.operations.Operations.add_column": "../zh/06_01_01_add_column.md",
        "#alembic.operations.Operations.alter_column": "../zh/06_01_02_alter_column.md",
        "#alembic.operations.Operations.alter_column.params.comment": "../zh/06_01_02_alter_column.md#params.comment",
        "#alembic.operations.Operations.batch_alter_table": "../zh/06_01_03_batch_alter_table.md",
        "#alembic.operations.Operations.bulk_insert": "../zh/06_01_04_bulk_insert.md",
        "#alembic.operations.Operations.create_check_constraint": "../zh/06_01_05_create_check_constraint.md",
        "#alembic.operations.Operations.create_exclude_constraint": "../zh/06_01_06_create_exclude_constraint.md",
        "#alembic.operations.Operations.create_foreign_key": "../zh/06_01_07_create_foreign_key.md",
        "#alembic.operations.Operations.create_index": "../zh/06_01_08_create_index.md",
        "#alembic.operations.Operations.create_primary_key": "../zh/06_01_09_create_primary_key.md",
        "#alembic.operations.Operations.create_table": "../zh/06_01_10_create_table.md",
        "#alembic.operations.Operations.create_table_comment": "../zh/06_01_11_create_table_comment.md",
        "#alembic.operations.Operations.create_unique_constraint": "../zh/06_01_12_create_unique_constraint.md",
        "#alembic.operations.Operations.drop_column": "../zh/06_01_13_drop_column.md",
        "#alembic.operations.Operations.drop_constraint": "../zh/06_01_14_drop_constraint.md",
        "#alembic.operations.Operations.drop_index": "../zh/06_01_15_drop_index.md",
        "#alembic.operations.Operations.drop_table": "../zh/06_01_16_drop_table.md",
        "#alembic.operations.Operations.drop_table_comment": "../zh/06_01_17_drop_table_comment.md",
        "#alembic.operations.Operations.execute": "../zh/06_01_18_execute.md",
        "#alembic.operations.Operations.f": "../zh/06_01_19_f.md",
        "#alembic.operations.Operations.get_bind": "../zh/06_01_20_get_bind.md",
        "#alembic.operations.Operations.get_context": "../zh/06_01_21_get_context.md",
        "#alembic.operations.Operations.implementation_for": "../zh/06_01_22_implementation_for.md",
        "#alembic.operations.Operations.inline_literal": "../zh/06_01_23_inline_literal.md",
        "#alembic.operations.Operations.invoke": "../zh/06_01_24_invoke.md",
        "#alembic.operations.Operations.register_operation": "../zh/06_01_25_register_operation.md",
        "#alembic.operations.Operations.rename_table": "../zh/06_01_26_rename_table.md"
    }

    parameter_flag = True
    texts = []

    for p in query('p').items():
        
        _a_tags = {a.text(): a.attr('href') for a in p('a').items() }
        code_tags = [code.text() for code in p('code').items() ]
        strong_tags = [strong.text() for strong in p('strong').items() ]

        # 替换成本地文件路径
        a_tags = {}
        for a, link in _a_tags.items():
            if link in op_md_file_dict:
                a_tags[a] = op_md_file_dict[link]
            elif link in batch_op_md_file_dict:
                a_tags[a] = batch_op_md_file_dict[link]
            elif a == '¶':
                continue
            else:
                a_tags[a] = link

        text = p.text()

        # 处理每个P标签里面的特殊字符
        words = []
        
        for index, word in enumerate(text.split(' ')):
            if index == 0 and word.startswith('Note'):  # Note 
                word = f'> **{word}:**'
            
            if index == 0 and word.startswith('See also'):  # See also 
                word = f'> **{word}:**'
            
            if word.endswith('¶'):  # 参数 斜体
                word = f'* ***{word[:-1]}***'

                # 新增参数flag
                if parameter_flag:
                    texts.append('**Parameters:**')
                    parameter_flag = False
            
            words.append(word)

        text = ' '.join(words)

        if text == 'See also':  # See also 
            text = f'**{text}:**'

        # 单行代码
        for code in code_tags:
            if code not in a_tags:
                text = text.replace(f" {code} ", f' `{code}` ')
                text = text.replace(f" {code},", f' `{code}`,')
                text = text.replace(f" {code}:", f' `{code}`:')
                text = text.replace(f" {code}.", f' `{code}`.')

        # 加粗
        for strong in strong_tags:
            if strong not in a_tags:
                text = text.replace(f" {strong} ", f' **{strong}** ')
                text = text.replace(f" {strong},", f' **{strong}**,')
                text = text.replace(f" {strong}:", f' **{strong}**:')
                text = text.replace(f" {strong};", f' **{strong}**;')

        # 链接
        for a, href in a_tags.items():
            text = text.replace(f" {a} ", f' **[{a}]** ')
            text = text.replace(f" {a},", f' **[{a}]**,')
            text = text.replace(f" {a}.", f' **[{a}]**.')
            text = text.replace(f" {a}:", f' **[{a}]**:')

            if a == text:
                text = text.replace(f"{a}", f'* **[{a}]** ')
        
        links.update(a_tags)
        texts.append(text)

        # print(a_tags)
        # print(code_tags)
    
    links_text = []

    for a_text, href in links.items():
        _href = href
        if not (href.startswith('http') or href.startswith('#') or href.startswith('../zh')):
            _href = f'../en/{href}'

        links_text.append(f'[{a_text}]: {_href}')

    print('\n')
    print('\n'.join(links_text))
    print('\n')
    print('\n\n'.join(texts))


def main3():
    html = """
        <dd><p>Define high level migration operations.</p>
        <p>Each operation corresponds to some schema migration operation,
        executed against a particular <a class="reference internal" href="api/runtime.html#alembic.runtime.migration.MigrationContext" title="alembic.runtime.migration.MigrationContext"><code class="xref py py-class docutils literal notranslate"><span class="pre">MigrationContext</span></code></a>
        which in turn represents connectivity to a database,
        or a file output stream.</p>
        <p>While <a class="reference internal" href="#alembic.operations.Operations" title="alembic.operations.Operations"><code class="xref py py-class docutils literal notranslate"><span class="pre">Operations</span></code></a> is normally configured as
        part of the <a class="reference internal" href="api/runtime.html#alembic.runtime.environment.EnvironmentContext.run_migrations" title="alembic.runtime.environment.EnvironmentContext.run_migrations"><code class="xref py py-meth docutils literal notranslate"><span class="pre">EnvironmentContext.run_migrations()</span></code></a>
        method called from an <code class="docutils literal notranslate"><span class="pre">env.py</span></code> script, a standalone
        <a class="reference internal" href="#alembic.operations.Operations" title="alembic.operations.Operations"><code class="xref py py-class docutils literal notranslate"><span class="pre">Operations</span></code></a> instance can be
        made for use cases external to regular Alembic
        migrations by passing in a <a class="reference internal" href="api/runtime.html#alembic.runtime.migration.MigrationContext" title="alembic.runtime.migration.MigrationContext"><code class="xref py py-class docutils literal notranslate"><span class="pre">MigrationContext</span></code></a>:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">alembic.migration</span> <span class="kn">import</span> <span class="n">MigrationContext</span>
        <span class="kn">from</span> <span class="nn">alembic.operations</span> <span class="kn">import</span> <span class="n">Operations</span>

        <span class="n">conn</span> <span class="o">=</span> <span class="n">myengine</span><span class="o">.</span><span class="n">connect</span><span class="p">()</span>
        <span class="n">ctx</span> <span class="o">=</span> <span class="n">MigrationContext</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="n">conn</span><span class="p">)</span>
        <span class="n">op</span> <span class="o">=</span> <span class="n">Operations</span><span class="p">(</span><span class="n">ctx</span><span class="p">)</span>

        <span class="n">op</span><span class="o">.</span><span class="n">alter_column</span><span class="p">(</span><span class="s2">"t"</span><span class="p">,</span> <span class="s2">"c"</span><span class="p">,</span> <span class="n">nullable</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
        </pre></div>
        </div>
        <p>Note that as of 0.8, most of the methods on this class are produced
        dynamically using the <a class="reference internal" href="#alembic.operations.Operations.register_operation" title="alembic.operations.Operations.register_operation"><code class="xref py py-meth docutils literal notranslate"><span class="pre">Operations.register_operation()</span></code></a>
        method.</p>
        <p>Construct a new <a class="reference internal" href="#alembic.operations.Operations" title="alembic.operations.Operations"><code class="xref py py-class docutils literal notranslate"><span class="pre">Operations</span></code></a></p>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><p><span class="target" id="alembic.operations.Operations.params.migration_context"></span><strong>migration_context</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.params.migration_context">¶</a> – a <a class="reference internal" href="api/runtime.html#alembic.runtime.migration.MigrationContext" title="alembic.runtime.migration.MigrationContext"><code class="xref py py-class docutils literal notranslate"><span class="pre">MigrationContext</span></code></a>
        instance.</p>
        </dd>
        </dl>
        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.add_column">
        <span class="sig-name descname"><span class="pre">add_column</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Column</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">schema</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">Table</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#alembic.operations.Operations.add_column" title="Permalink to this definition">¶</a></dt>
        <dd><p>Issue an “add column” instruction using the current
        migration context.</p>
        <p>e.g.:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">alembic</span> <span class="kn">import</span> <span class="n">op</span>
        <span class="kn">from</span> <span class="nn">sqlalchemy</span> <span class="kn">import</span> <span class="n">Column</span><span class="p">,</span> <span class="n">String</span>

        <span class="n">op</span><span class="o">.</span><span class="n">add_column</span><span class="p">(</span><span class="s1">'organization'</span><span class="p">,</span>
            <span class="n">Column</span><span class="p">(</span><span class="s1">'name'</span><span class="p">,</span> <span class="n">String</span><span class="p">())</span>
        <span class="p">)</span>
        </pre></div>
        </div>
        <p>The provided <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Column</span></code></a> object can also
        specify a <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/constraints.html#sqlalchemy.schema.ForeignKey" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">ForeignKey</span></code></a>, referencing
        a remote table name.  Alembic will automatically generate a stub
        “referenced” table and emit a second ALTER statement in order
        to add the constraint separately:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">alembic</span> <span class="kn">import</span> <span class="n">op</span>
        <span class="kn">from</span> <span class="nn">sqlalchemy</span> <span class="kn">import</span> <span class="n">Column</span><span class="p">,</span> <span class="n">INTEGER</span><span class="p">,</span> <span class="n">ForeignKey</span>

        <span class="n">op</span><span class="o">.</span><span class="n">add_column</span><span class="p">(</span><span class="s1">'organization'</span><span class="p">,</span>
            <span class="n">Column</span><span class="p">(</span><span class="s1">'account_id'</span><span class="p">,</span> <span class="n">INTEGER</span><span class="p">,</span> <span class="n">ForeignKey</span><span class="p">(</span><span class="s1">'accounts.id'</span><span class="p">))</span>
        <span class="p">)</span>
        </pre></div>
        </div>
        <p>Note that this statement uses the <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Column</span></code></a>
        construct as is from the SQLAlchemy library.  In particular,
        default values to be created on the database side are
        specified using the <code class="docutils literal notranslate"><span class="pre">server_default</span></code> parameter, and not
        <code class="docutils literal notranslate"><span class="pre">default</span></code> which only specifies Python-side defaults:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">alembic</span> <span class="kn">import</span> <span class="n">op</span>
        <span class="kn">from</span> <span class="nn">sqlalchemy</span> <span class="kn">import</span> <span class="n">Column</span><span class="p">,</span> <span class="n">TIMESTAMP</span><span class="p">,</span> <span class="n">func</span>

        <span class="c1"># specify "DEFAULT NOW" along with the column add</span>
        <span class="n">op</span><span class="o">.</span><span class="n">add_column</span><span class="p">(</span><span class="s1">'account'</span><span class="p">,</span>
            <span class="n">Column</span><span class="p">(</span><span class="s1">'timestamp'</span><span class="p">,</span> <span class="n">TIMESTAMP</span><span class="p">,</span> <span class="n">server_default</span><span class="o">=</span><span class="n">func</span><span class="o">.</span><span class="n">now</span><span class="p">())</span>
        <span class="p">)</span>
        </pre></div>
        </div>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><ul class="simple">
        <li><p><span class="target" id="alembic.operations.Operations.add_column.params.table_name"></span><strong>table_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.add_column.params.table_name">¶</a> – String name of the parent table.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.add_column.params.column"></span><strong>column</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.add_column.params.column">¶</a> – a <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">sqlalchemy.schema.Column</span></code></a> object
        representing the new column.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.add_column.params.schema"></span><strong>schema</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.add_column.params.schema">¶</a> – Optional schema name to operate within.  To control
        quoting of the schema outside of the default behavior, use
        the SQLAlchemy construct
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">quoted_name</span></code></a>.</p></li>
        </ul>
        </dd>
        </dl>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.alter_column">
        <span class="sig-name descname"><span class="pre">alter_column</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">nullable</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">comment</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">Union</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">,</span> </span><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">server_default</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Any</span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">new_column_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">type_</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">Union</span><span class="p"><span class="pre">[</span></span><span class="pre">TypeEngine</span><span class="p"><span class="pre">,</span> </span><span class="pre">Type</span><span class="p"><span class="pre">[</span></span><span class="pre">TypeEngine</span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">existing_type</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">Union</span><span class="p"><span class="pre">[</span></span><span class="pre">TypeEngine</span><span class="p"><span class="pre">,</span> </span><span class="pre">Type</span><span class="p"><span class="pre">[</span></span><span class="pre">TypeEngine</span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">existing_server_default</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">Union</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">,</span> </span><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a><span class="p"><span class="pre">,</span> </span><span class="pre">Identity</span><span class="p"><span class="pre">,</span> </span><span class="pre">Computed</span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">existing_nullable</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">existing_comment</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">schema</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kw</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">Table</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#alembic.operations.Operations.alter_column" title="Permalink to this definition">¶</a></dt>
        <dd><p>Issue an “alter column” instruction using the
        current migration context.</p>
        <p>Generally, only that aspect of the column which
        is being changed, i.e. name, type, nullability,
        default, needs to be specified.  Multiple changes
        can also be specified at once and the backend should
        “do the right thing”, emitting each change either
        separately or together as the backend allows.</p>
        <p>MySQL has special requirements here, since MySQL
        cannot ALTER a column without a full specification.
        When producing MySQL-compatible migration files,
        it is recommended that the <code class="docutils literal notranslate"><span class="pre">existing_type</span></code>,
        <code class="docutils literal notranslate"><span class="pre">existing_server_default</span></code>, and <code class="docutils literal notranslate"><span class="pre">existing_nullable</span></code>
        parameters be present, if not being altered.</p>
        <p>Type changes which are against the SQLAlchemy
        “schema” types <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Boolean" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Boolean</span></code></a>
        and  <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Enum" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Enum</span></code></a> may also
        add or drop constraints which accompany those
        types on backends that don’t support them natively.
        The <code class="docutils literal notranslate"><span class="pre">existing_type</span></code> argument is
        used in this case to identify and remove a previous
        constraint that was bound to the type object.</p>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><ul class="simple">
        <li><p><span class="target" id="alembic.operations.Operations.alter_column.params.table_name"></span><strong>table_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.alter_column.params.table_name">¶</a> – string name of the target table.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.alter_column.params.column_name"></span><strong>column_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.alter_column.params.column_name">¶</a> – string name of the target column,
        as it exists before the operation begins.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.alter_column.params.nullable"></span><strong>nullable</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.alter_column.params.nullable">¶</a> – Optional; specify <code class="docutils literal notranslate"><span class="pre">True</span></code> or <code class="docutils literal notranslate"><span class="pre">False</span></code>
        to alter the column’s nullability.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.alter_column.params.server_default"></span><strong>server_default</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.alter_column.params.server_default">¶</a> – Optional; specify a string
        SQL expression, <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.text" title="(in SQLAlchemy v1.4)"><code class="xref py py-func docutils literal notranslate"><span class="pre">text()</span></code></a>,
        or <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/defaults.html#sqlalchemy.schema.DefaultClause" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">DefaultClause</span></code></a> to indicate
        an alteration to the column’s default value.
        Set to <code class="docutils literal notranslate"><span class="pre">None</span></code> to have the default removed.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.alter_column.params.comment"></span><strong>comment</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.alter_column.params.comment">¶</a> – </p><p>optional string text of a new comment to add to the
        column.</p>
        <div class="versionadded">
        <p><span class="versionmodified added">New in version 1.0.6.</span></p>
        </div>
        <p></p></li>
        <li><p><span class="target" id="alembic.operations.Operations.alter_column.params.new_column_name"></span><strong>new_column_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.alter_column.params.new_column_name">¶</a> – Optional; specify a string name here to
        indicate the new name within a column rename operation.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.alter_column.params.type_"></span><strong>type_</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.alter_column.params.type_">¶</a> – Optional; a <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/type_api.html#sqlalchemy.types.TypeEngine" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">TypeEngine</span></code></a>
        type object to specify a change to the column’s type.
        For SQLAlchemy types that also indicate a constraint (i.e.
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Boolean" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Boolean</span></code></a>, <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Enum" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Enum</span></code></a>),
        the constraint is also generated.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.alter_column.params.autoincrement"></span><strong>autoincrement</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.alter_column.params.autoincrement">¶</a> – set the <code class="docutils literal notranslate"><span class="pre">AUTO_INCREMENT</span></code> flag of the column;
        currently understood by the MySQL dialect.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.alter_column.params.existing_type"></span><strong>existing_type</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.alter_column.params.existing_type">¶</a> – Optional; a
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/type_api.html#sqlalchemy.types.TypeEngine" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">TypeEngine</span></code></a>
        type object to specify the previous type.   This
        is required for all MySQL column alter operations that
        don’t otherwise specify a new type, as well as for
        when nullability is being changed on a SQL Server
        column.  It is also used if the type is a so-called
        SQLlchemy “schema” type which may define a constraint (i.e.
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Boolean" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Boolean</span></code></a>,
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Enum" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Enum</span></code></a>),
        so that the constraint can be dropped.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.alter_column.params.existing_server_default"></span><strong>existing_server_default</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.alter_column.params.existing_server_default">¶</a> – Optional; The existing
        default value of the column.   Required on MySQL if
        an existing default is not being changed; else MySQL
        removes the default.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.alter_column.params.existing_nullable"></span><strong>existing_nullable</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.alter_column.params.existing_nullable">¶</a> – Optional; the existing nullability
        of the column.  Required on MySQL if the existing nullability
        is not being changed; else MySQL sets this to NULL.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.alter_column.params.existing_autoincrement"></span><strong>existing_autoincrement</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.alter_column.params.existing_autoincrement">¶</a> – Optional; the existing autoincrement
        of the column.  Used for MySQL’s system of altering a column
        that specifies <code class="docutils literal notranslate"><span class="pre">AUTO_INCREMENT</span></code>.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.alter_column.params.existing_comment"></span><strong>existing_comment</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.alter_column.params.existing_comment">¶</a> – </p><p>string text of the existing comment on the
        column to be maintained.  Required on MySQL if the existing comment
        on the column is not being changed.</p>
        <div class="versionadded">
        <p><span class="versionmodified added">New in version 1.0.6.</span></p>
        </div>
        <p></p></li>
        <li><p><span class="target" id="alembic.operations.Operations.alter_column.params.schema"></span><strong>schema</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.alter_column.params.schema">¶</a> – Optional schema name to operate within.  To control
        quoting of the schema outside of the default behavior, use
        the SQLAlchemy construct
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">quoted_name</span></code></a>.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.alter_column.params.postgresql_using"></span><strong>postgresql_using</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.alter_column.params.postgresql_using">¶</a> – String argument which will indicate a
        SQL expression to render within the Postgresql-specific USING clause
        within ALTER COLUMN.    This string is taken directly as raw SQL which
        must explicitly include any necessary quoting or escaping of tokens
        within the expression.</p></li>
        </ul>
        </dd>
        </dl>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.batch_alter_table">
        <span class="sig-name descname"><span class="pre">batch_alter_table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">table_name</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">schema</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">recreate</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'auto'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">partial_reordering</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">copy_from</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_args</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_kwargs</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">{}</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">reflect_args</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">reflect_kwargs</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">{}</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">naming_convention</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#alembic.operations.Operations.batch_alter_table" title="Permalink to this definition">¶</a></dt>
        <dd><p>Invoke a series of per-table migrations in batch.</p>
        <p>Batch mode allows a series of operations specific to a table
        to be syntactically grouped together, and allows for alternate
        modes of table migration, in particular the “recreate” style of
        migration required by SQLite.</p>
        <p>“recreate” style is as follows:</p>
        <ol class="arabic simple">
        <li><p>A new table is created with the new specification, based on the
        migration directives within the batch, using a temporary name.</p></li>
        <li><p>the data copied from the existing table to the new table.</p></li>
        <li><p>the existing table is dropped.</p></li>
        <li><p>the new table is renamed to the existing table name.</p></li>
        </ol>
        <p>The directive by default will only use “recreate” style on the
        SQLite backend, and only if directives are present which require
        this form, e.g. anything other than <code class="docutils literal notranslate"><span class="pre">add_column()</span></code>.   The batch
        operation on other backends will proceed using standard ALTER TABLE
        operations.</p>
        <p>The method is used as a context manager, which returns an instance
        of <a class="reference internal" href="#alembic.operations.BatchOperations" title="alembic.operations.BatchOperations"><code class="xref py py-class docutils literal notranslate"><span class="pre">BatchOperations</span></code></a>; this object is the same as
        <a class="reference internal" href="#alembic.operations.Operations" title="alembic.operations.Operations"><code class="xref py py-class docutils literal notranslate"><span class="pre">Operations</span></code></a> except that table names and schema names
        are omitted.  E.g.:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="k">with</span> <span class="n">op</span><span class="o">.</span><span class="n">batch_alter_table</span><span class="p">(</span><span class="s2">"some_table"</span><span class="p">)</span> <span class="k">as</span> <span class="n">batch_op</span><span class="p">:</span>
            <span class="n">batch_op</span><span class="o">.</span><span class="n">add_column</span><span class="p">(</span><span class="n">Column</span><span class="p">(</span><span class="s1">'foo'</span><span class="p">,</span> <span class="n">Integer</span><span class="p">))</span>
            <span class="n">batch_op</span><span class="o">.</span><span class="n">drop_column</span><span class="p">(</span><span class="s1">'bar'</span><span class="p">)</span>
        </pre></div>
        </div>
        <p>The operations within the context manager are invoked at once
        when the context is ended.   When run against SQLite, if the
        migrations include operations not supported by SQLite’s ALTER TABLE,
        the entire table will be copied to a new one with the new
        specification, moving all data across as well.</p>
        <p>The copy operation by default uses reflection to retrieve the current
        structure of the table, and therefore <a class="reference internal" href="#alembic.operations.Operations.batch_alter_table" title="alembic.operations.Operations.batch_alter_table"><code class="xref py py-meth docutils literal notranslate"><span class="pre">batch_alter_table()</span></code></a>
        in this mode requires that the migration is run in “online” mode.
        The <code class="docutils literal notranslate"><span class="pre">copy_from</span></code> parameter may be passed which refers to an existing
        <code class="xref py py-class docutils literal notranslate"><span class="pre">Table</span></code> object, which will bypass this reflection step.</p>
        <div class="admonition note">
        <p class="admonition-title">Note</p>
        <p>The table copy operation will currently not copy
        CHECK constraints, and may not copy UNIQUE constraints that are
        unnamed, as is possible on SQLite.   See the section
        <a class="reference internal" href="batch.html#sqlite-batch-constraints"><span class="std std-ref">Dealing with Constraints</span></a> for workarounds.</p>
        </div>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><ul class="simple">
        <li><p><span class="target" id="alembic.operations.Operations.batch_alter_table.params.table_name"></span><strong>table_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.batch_alter_table.params.table_name">¶</a> – name of table</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.batch_alter_table.params.schema"></span><strong>schema</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.batch_alter_table.params.schema">¶</a> – optional schema name.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.batch_alter_table.params.recreate"></span><strong>recreate</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.batch_alter_table.params.recreate">¶</a> – under what circumstances the table should be
        recreated. At its default of <code class="docutils literal notranslate"><span class="pre">"auto"</span></code>, the SQLite dialect will
        recreate the table if any operations other than <code class="docutils literal notranslate"><span class="pre">add_column()</span></code>,
        <code class="docutils literal notranslate"><span class="pre">create_index()</span></code>, or <code class="docutils literal notranslate"><span class="pre">drop_index()</span></code> are
        present. Other options include <code class="docutils literal notranslate"><span class="pre">"always"</span></code> and <code class="docutils literal notranslate"><span class="pre">"never"</span></code>.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.batch_alter_table.params.copy_from"></span><strong>copy_from</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.batch_alter_table.params.copy_from">¶</a> – </p><p>optional <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Table</span></code></a> object
        that will act as the structure of the table being copied.  If omitted,
        table reflection is used to retrieve the structure of the table.</p>
        <div class="admonition seealso">
        <p class="admonition-title">See also</p>
        <p><a class="reference internal" href="batch.html#batch-offline-mode"><span class="std std-ref">Working in Offline Mode</span></a></p>
        <p><a class="reference internal" href="#alembic.operations.Operations.batch_alter_table.params.reflect_args" title="alembic.operations.Operations.batch_alter_table"><code class="xref py py-paramref docutils literal notranslate"><span class="pre">reflect_args</span></code></a></p>
        <p><a class="reference internal" href="#alembic.operations.Operations.batch_alter_table.params.reflect_kwargs" title="alembic.operations.Operations.batch_alter_table"><code class="xref py py-paramref docutils literal notranslate"><span class="pre">reflect_kwargs</span></code></a></p>
        </div>
        <p></p></li>
        <li><p><span class="target" id="alembic.operations.Operations.batch_alter_table.params.reflect_args"></span><strong>reflect_args</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.batch_alter_table.params.reflect_args">¶</a> – a sequence of additional positional arguments that
        will be applied to the table structure being reflected / copied;
        this may be used to pass column and constraint overrides to the
        table that will be reflected, in lieu of passing the whole
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Table</span></code></a> using
        <a class="reference internal" href="#alembic.operations.Operations.batch_alter_table.params.copy_from" title="alembic.operations.Operations.batch_alter_table"><code class="xref py py-paramref docutils literal notranslate"><span class="pre">copy_from</span></code></a>.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.batch_alter_table.params.reflect_kwargs"></span><strong>reflect_kwargs</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.batch_alter_table.params.reflect_kwargs">¶</a> – a dictionary of additional keyword arguments
        that will be applied to the table structure being copied; this may be
        used to pass additional table and reflection options to the table that
        will be reflected, in lieu of passing the whole
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Table</span></code></a> using
        <a class="reference internal" href="#alembic.operations.Operations.batch_alter_table.params.copy_from" title="alembic.operations.Operations.batch_alter_table"><code class="xref py py-paramref docutils literal notranslate"><span class="pre">copy_from</span></code></a>.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.batch_alter_table.params.table_args"></span><strong>table_args</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.batch_alter_table.params.table_args">¶</a> – a sequence of additional positional arguments that
        will be applied to the new <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Table</span></code></a> when
        created, in addition to those copied from the source table.
        This may be used to provide additional constraints such as CHECK
        constraints that may not be reflected.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.batch_alter_table.params.table_kwargs"></span><strong>table_kwargs</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.batch_alter_table.params.table_kwargs">¶</a> – a dictionary of additional keyword arguments
        that will be applied to the new <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Table</span></code></a>
        when created, in addition to those copied from the source table.
        This may be used to provide for additional table options that may
        not be reflected.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.batch_alter_table.params.naming_convention"></span><strong>naming_convention</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.batch_alter_table.params.naming_convention">¶</a> – </p><p>a naming convention dictionary of the form
        described at <a class="reference internal" href="naming.html#autogen-naming-conventions"><span class="std std-ref">Integration of Naming Conventions into Operations, Autogenerate</span></a> which will be applied
        to the <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.MetaData" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">MetaData</span></code></a> during the reflection
        process.  This is typically required if one wants to drop SQLite
        constraints, as these constraints will not have names when
        reflected on this backend.  Requires SQLAlchemy <strong>0.9.4</strong> or greater.</p>
        <div class="admonition seealso">
        <p class="admonition-title">See also</p>
        <p><a class="reference internal" href="batch.html#dropping-sqlite-foreign-keys"><span class="std std-ref">Dropping Unnamed or Named Foreign Key Constraints</span></a></p>
        </div>
        <p></p></li>
        <li><p><span class="target" id="alembic.operations.Operations.batch_alter_table.params.partial_reordering"></span><strong>partial_reordering</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.batch_alter_table.params.partial_reordering">¶</a> – </p><p>a list of tuples, each suggesting a desired
        ordering of two or more columns in the newly created table.  Requires
        that <a class="reference internal" href="#alembic.operations.Operations.batch_alter_table.params.recreate" title="alembic.operations.Operations.batch_alter_table"><code class="xref py py-paramref docutils literal notranslate"><span class="pre">batch_alter_table.recreate</span></code></a> is set to <code class="docutils literal notranslate"><span class="pre">"always"</span></code>.
        Examples, given a table with columns “a”, “b”, “c”, and “d”:</p>
        <p>Specify the order of all columns:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="k">with</span> <span class="n">op</span><span class="o">.</span><span class="n">batch_alter_table</span><span class="p">(</span>
                <span class="s2">"some_table"</span><span class="p">,</span> <span class="n">recreate</span><span class="o">=</span><span class="s2">"always"</span><span class="p">,</span>
                <span class="n">partial_reordering</span><span class="o">=</span><span class="p">[(</span><span class="s2">"c"</span><span class="p">,</span> <span class="s2">"d"</span><span class="p">,</span> <span class="s2">"a"</span><span class="p">,</span> <span class="s2">"b"</span><span class="p">)]</span>
        <span class="p">)</span> <span class="k">as</span> <span class="n">batch_op</span><span class="p">:</span>
            <span class="k">pass</span>
        </pre></div>
        </div>
        <p>Ensure “d” appears before “c”, and “b”, appears before “a”:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="k">with</span> <span class="n">op</span><span class="o">.</span><span class="n">batch_alter_table</span><span class="p">(</span>
                <span class="s2">"some_table"</span><span class="p">,</span> <span class="n">recreate</span><span class="o">=</span><span class="s2">"always"</span><span class="p">,</span>
                <span class="n">partial_reordering</span><span class="o">=</span><span class="p">[(</span><span class="s2">"d"</span><span class="p">,</span> <span class="s2">"c"</span><span class="p">),</span> <span class="p">(</span><span class="s2">"b"</span><span class="p">,</span> <span class="s2">"a"</span><span class="p">)]</span>
        <span class="p">)</span> <span class="k">as</span> <span class="n">batch_op</span><span class="p">:</span>
            <span class="k">pass</span>
        </pre></div>
        </div>
        <p>The ordering of columns not included in the partial_reordering
        set is undefined.   Therefore it is best to specify the complete
        ordering of all columns for best results.</p>
        <div class="versionadded">
        <p><span class="versionmodified added">New in version 1.4.0.</span></p>
        </div>
        <p></p></li>
        </ul>
        </dd>
        </dl>
        <div class="admonition note">
        <p class="admonition-title">Note</p>
        <p>batch mode requires SQLAlchemy 0.8 or above.</p>
        </div>
        <div class="admonition seealso">
        <p class="admonition-title">See also</p>
        <p><a class="reference internal" href="batch.html#batch-migrations"><span class="std std-ref">Running “Batch” Migrations for SQLite and Other Databases</span></a></p>
        </div>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.bulk_insert">
        <span class="sig-name descname"><span class="pre">bulk_insert</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">table</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Union</span><span class="p"><span class="pre">[</span></span><span class="pre">Table</span><span class="p"><span class="pre">,</span> </span><span class="pre">TableClause</span><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="n"><span class="pre">rows</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">List</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#dict" title="(in Python v3.10)"><span class="pre">dict</span></a><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="n"><span class="pre">multiinsert</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">True</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/constants.html#None" title="(in Python v3.10)"><span class="pre">None</span></a></span></span><a class="headerlink" href="#alembic.operations.Operations.bulk_insert" title="Permalink to this definition">¶</a></dt>
        <dd><p>Issue a “bulk insert” operation using the current
        migration context.</p>
        <p>This provides a means of representing an INSERT of multiple rows
        which works equally well in the context of executing on a live
        connection as well as that of generating a SQL script.   In the
        case of a SQL script, the values are rendered inline into the
        statement.</p>
        <p>e.g.:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">alembic</span> <span class="kn">import</span> <span class="n">op</span>
        <span class="kn">from</span> <span class="nn">datetime</span> <span class="kn">import</span> <span class="n">date</span>
        <span class="kn">from</span> <span class="nn">sqlalchemy.sql</span> <span class="kn">import</span> <span class="n">table</span><span class="p">,</span> <span class="n">column</span>
        <span class="kn">from</span> <span class="nn">sqlalchemy</span> <span class="kn">import</span> <span class="n">String</span><span class="p">,</span> <span class="n">Integer</span><span class="p">,</span> <span class="n">Date</span>

        <span class="c1"># Create an ad-hoc table to use for the insert statement.</span>
        <span class="n">accounts_table</span> <span class="o">=</span> <span class="n">table</span><span class="p">(</span><span class="s1">'account'</span><span class="p">,</span>
            <span class="n">column</span><span class="p">(</span><span class="s1">'id'</span><span class="p">,</span> <span class="n">Integer</span><span class="p">),</span>
            <span class="n">column</span><span class="p">(</span><span class="s1">'name'</span><span class="p">,</span> <span class="n">String</span><span class="p">),</span>
            <span class="n">column</span><span class="p">(</span><span class="s1">'create_date'</span><span class="p">,</span> <span class="n">Date</span><span class="p">)</span>
        <span class="p">)</span>

        <span class="n">op</span><span class="o">.</span><span class="n">bulk_insert</span><span class="p">(</span><span class="n">accounts_table</span><span class="p">,</span>
            <span class="p">[</span>
                <span class="p">{</span><span class="s1">'id'</span><span class="p">:</span><span class="mi">1</span><span class="p">,</span> <span class="s1">'name'</span><span class="p">:</span><span class="s1">'John Smith'</span><span class="p">,</span>
                        <span class="s1">'create_date'</span><span class="p">:</span><span class="n">date</span><span class="p">(</span><span class="mi">2010</span><span class="p">,</span> <span class="mi">10</span><span class="p">,</span> <span class="mi">5</span><span class="p">)},</span>
                <span class="p">{</span><span class="s1">'id'</span><span class="p">:</span><span class="mi">2</span><span class="p">,</span> <span class="s1">'name'</span><span class="p">:</span><span class="s1">'Ed Williams'</span><span class="p">,</span>
                        <span class="s1">'create_date'</span><span class="p">:</span><span class="n">date</span><span class="p">(</span><span class="mi">2007</span><span class="p">,</span> <span class="mi">5</span><span class="p">,</span> <span class="mi">27</span><span class="p">)},</span>
                <span class="p">{</span><span class="s1">'id'</span><span class="p">:</span><span class="mi">3</span><span class="p">,</span> <span class="s1">'name'</span><span class="p">:</span><span class="s1">'Wendy Jones'</span><span class="p">,</span>
                        <span class="s1">'create_date'</span><span class="p">:</span><span class="n">date</span><span class="p">(</span><span class="mi">2008</span><span class="p">,</span> <span class="mi">8</span><span class="p">,</span> <span class="mi">15</span><span class="p">)},</span>
            <span class="p">]</span>
        <span class="p">)</span>
        </pre></div>
        </div>
        <p>When using –sql mode, some datatypes may not render inline
        automatically, such as dates and other special types.   When this
        issue is present, <a class="reference internal" href="#alembic.operations.Operations.inline_literal" title="alembic.operations.Operations.inline_literal"><code class="xref py py-meth docutils literal notranslate"><span class="pre">Operations.inline_literal()</span></code></a> may be used:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="n">op</span><span class="o">.</span><span class="n">bulk_insert</span><span class="p">(</span><span class="n">accounts_table</span><span class="p">,</span>
            <span class="p">[</span>
                <span class="p">{</span><span class="s1">'id'</span><span class="p">:</span><span class="mi">1</span><span class="p">,</span> <span class="s1">'name'</span><span class="p">:</span><span class="s1">'John Smith'</span><span class="p">,</span>
                        <span class="s1">'create_date'</span><span class="p">:</span><span class="n">op</span><span class="o">.</span><span class="n">inline_literal</span><span class="p">(</span><span class="s2">"2010-10-05"</span><span class="p">)},</span>
                <span class="p">{</span><span class="s1">'id'</span><span class="p">:</span><span class="mi">2</span><span class="p">,</span> <span class="s1">'name'</span><span class="p">:</span><span class="s1">'Ed Williams'</span><span class="p">,</span>
                        <span class="s1">'create_date'</span><span class="p">:</span><span class="n">op</span><span class="o">.</span><span class="n">inline_literal</span><span class="p">(</span><span class="s2">"2007-05-27"</span><span class="p">)},</span>
                <span class="p">{</span><span class="s1">'id'</span><span class="p">:</span><span class="mi">3</span><span class="p">,</span> <span class="s1">'name'</span><span class="p">:</span><span class="s1">'Wendy Jones'</span><span class="p">,</span>
                        <span class="s1">'create_date'</span><span class="p">:</span><span class="n">op</span><span class="o">.</span><span class="n">inline_literal</span><span class="p">(</span><span class="s2">"2008-08-15"</span><span class="p">)},</span>
            <span class="p">],</span>
            <span class="n">multiinsert</span><span class="o">=</span><span class="kc">False</span>
        <span class="p">)</span>
        </pre></div>
        </div>
        <p>When using <a class="reference internal" href="#alembic.operations.Operations.inline_literal" title="alembic.operations.Operations.inline_literal"><code class="xref py py-meth docutils literal notranslate"><span class="pre">Operations.inline_literal()</span></code></a> in conjunction with
        <a class="reference internal" href="#alembic.operations.Operations.bulk_insert" title="alembic.operations.Operations.bulk_insert"><code class="xref py py-meth docutils literal notranslate"><span class="pre">Operations.bulk_insert()</span></code></a>, in order for the statement to work
        in “online” (e.g. non –sql) mode, the
        <a class="reference internal" href="#alembic.operations.Operations.bulk_insert.params.multiinsert" title="alembic.operations.Operations.bulk_insert"><code class="xref py py-paramref docutils literal notranslate"><span class="pre">multiinsert</span></code></a>
        flag should be set to <code class="docutils literal notranslate"><span class="pre">False</span></code>, which will have the effect of
        individual INSERT statements being emitted to the database, each
        with a distinct VALUES clause, so that the “inline” values can
        still be rendered, rather than attempting to pass the values
        as bound parameters.</p>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><ul class="simple">
        <li><p><span class="target" id="alembic.operations.Operations.bulk_insert.params.table"></span><strong>table</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.bulk_insert.params.table">¶</a> – a table object which represents the target of the INSERT.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.bulk_insert.params.rows"></span><strong>rows</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.bulk_insert.params.rows">¶</a> – a list of dictionaries indicating rows.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.bulk_insert.params.multiinsert"></span><strong>multiinsert</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.bulk_insert.params.multiinsert">¶</a> – when at its default of True and –sql mode is not
        enabled, the INSERT statement will be executed using
        “executemany()” style, where all elements in the list of
        dictionaries are passed as bound parameters in a single
        list.   Setting this to False results in individual INSERT
        statements being emitted per parameter set, and is needed
        in those cases where non-literal values are present in the
        parameter sets.</p></li>
        </ul>
        </dd>
        </dl>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.create_check_constraint">
        <span class="sig-name descname"><span class="pre">create_check_constraint</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">constraint_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">condition</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Union</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">,</span> </span><span class="pre">BinaryExpression</span><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="n"><span class="pre">schema</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kw</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">Table</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#alembic.operations.Operations.create_check_constraint" title="Permalink to this definition">¶</a></dt>
        <dd><p>Issue a “create check constraint” instruction using the
        current migration context.</p>
        <p>e.g.:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">alembic</span> <span class="kn">import</span> <span class="n">op</span>
        <span class="kn">from</span> <span class="nn">sqlalchemy.sql</span> <span class="kn">import</span> <span class="n">column</span><span class="p">,</span> <span class="n">func</span>

        <span class="n">op</span><span class="o">.</span><span class="n">create_check_constraint</span><span class="p">(</span>
            <span class="s2">"ck_user_name_len"</span><span class="p">,</span>
            <span class="s2">"user"</span><span class="p">,</span>
            <span class="n">func</span><span class="o">.</span><span class="n">len</span><span class="p">(</span><span class="n">column</span><span class="p">(</span><span class="s1">'name'</span><span class="p">))</span> <span class="o">&gt;</span> <span class="mi">5</span>
        <span class="p">)</span>
        </pre></div>
        </div>
        <p>CHECK constraints are usually against a SQL expression, so ad-hoc
        table metadata is usually needed.   The function will convert the given
        arguments into a <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/constraints.html#sqlalchemy.schema.CheckConstraint" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">sqlalchemy.schema.CheckConstraint</span></code></a> bound
        to an anonymous table in order to emit the CREATE statement.</p>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><ul class="simple">
        <li><p><span class="target" id="alembic.operations.Operations.create_check_constraint.params.name"></span><strong>name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_check_constraint.params.name">¶</a> – Name of the check constraint.  The name is necessary
        so that an ALTER statement can be emitted.  For setups that
        use an automated naming scheme such as that described at
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/constraints.html#constraint-naming-conventions" title="(in SQLAlchemy v1.4)"><span>Configuring Constraint Naming Conventions</span></a>,
        <code class="docutils literal notranslate"><span class="pre">name</span></code> here can be <code class="docutils literal notranslate"><span class="pre">None</span></code>, as the event listener will
        apply the name to the constraint object when it is associated
        with the table.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_check_constraint.params.table_name"></span><strong>table_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_check_constraint.params.table_name">¶</a> – String name of the source table.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_check_constraint.params.condition"></span><strong>condition</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_check_constraint.params.condition">¶</a> – SQL expression that’s the condition of the
        constraint. Can be a string or SQLAlchemy expression language
        structure.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_check_constraint.params.deferrable"></span><strong>deferrable</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_check_constraint.params.deferrable">¶</a> – optional bool. If set, emit DEFERRABLE or
        NOT DEFERRABLE when issuing DDL for this constraint.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_check_constraint.params.initially"></span><strong>initially</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_check_constraint.params.initially">¶</a> – optional string. If set, emit INITIALLY &lt;value&gt;
        when issuing DDL for this constraint.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_check_constraint.params.schema"></span><strong>schema</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_check_constraint.params.schema">¶</a> – Optional schema name to operate within.  To control
        quoting of the schema outside of the default behavior, use
        the SQLAlchemy construct
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">quoted_name</span></code></a>.</p></li>
        </ul>
        </dd>
        </dl>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.create_exclude_constraint">
        <span class="sig-name descname"><span class="pre">create_exclude_constraint</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">constraint_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">elements</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Any</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kw</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">Table</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#alembic.operations.Operations.create_exclude_constraint" title="Permalink to this definition">¶</a></dt>
        <dd><p>Issue an alter to create an EXCLUDE constraint using the
        current migration context.</p>
        <div class="admonition note">
        <p class="admonition-title">Note</p>
        <p>This method is Postgresql specific, and additionally
        requires at least SQLAlchemy 1.0.</p>
        </div>
        <p>e.g.:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">alembic</span> <span class="kn">import</span> <span class="n">op</span>

        <span class="n">op</span><span class="o">.</span><span class="n">create_exclude_constraint</span><span class="p">(</span>
            <span class="s2">"user_excl"</span><span class="p">,</span>
            <span class="s2">"user"</span><span class="p">,</span>

            <span class="p">(</span><span class="s2">"period"</span><span class="p">,</span> <span class="s1">'&amp;&amp;'</span><span class="p">),</span>
            <span class="p">(</span><span class="s2">"group"</span><span class="p">,</span> <span class="s1">'='</span><span class="p">),</span>
            <span class="n">where</span><span class="o">=</span><span class="p">(</span><span class="s2">"group != 'some group'"</span><span class="p">)</span>

        <span class="p">)</span>
        </pre></div>
        </div>
        <p>Note that the expressions work the same way as that of
        the <code class="docutils literal notranslate"><span class="pre">ExcludeConstraint</span></code> object itself; if plain strings are
        passed, quoting rules must be applied manually.</p>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><ul class="simple">
        <li><p><span class="target" id="alembic.operations.Operations.create_exclude_constraint.params.name"></span><strong>name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_exclude_constraint.params.name">¶</a> – Name of the constraint.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_exclude_constraint.params.table_name"></span><strong>table_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_exclude_constraint.params.table_name">¶</a> – String name of the source table.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_exclude_constraint.params.elements"></span><strong>elements</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_exclude_constraint.params.elements">¶</a> – exclude conditions.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_exclude_constraint.params.where"></span><strong>where</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_exclude_constraint.params.where">¶</a> – SQL expression or SQL string with optional WHERE
        clause.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_exclude_constraint.params.deferrable"></span><strong>deferrable</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_exclude_constraint.params.deferrable">¶</a> – optional bool. If set, emit DEFERRABLE or
        NOT DEFERRABLE when issuing DDL for this constraint.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_exclude_constraint.params.initially"></span><strong>initially</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_exclude_constraint.params.initially">¶</a> – optional string. If set, emit INITIALLY &lt;value&gt;
        when issuing DDL for this constraint.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_exclude_constraint.params.schema"></span><strong>schema</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_exclude_constraint.params.schema">¶</a> – Optional schema name to operate within.</p></li>
        </ul>
        </dd>
        </dl>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.create_foreign_key">
        <span class="sig-name descname"><span class="pre">create_foreign_key</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">constraint_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="n"><span class="pre">source_table</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">referent_table</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">local_cols</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">List</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="n"><span class="pre">remote_cols</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">List</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="n"><span class="pre">onupdate</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">ondelete</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">deferrable</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">initially</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">match</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">source_schema</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">referent_schema</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">dialect_kw</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">Table</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#alembic.operations.Operations.create_foreign_key" title="Permalink to this definition">¶</a></dt>
        <dd><p>Issue a “create foreign key” instruction using the
        current migration context.</p>
        <p>e.g.:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">alembic</span> <span class="kn">import</span> <span class="n">op</span>
        <span class="n">op</span><span class="o">.</span><span class="n">create_foreign_key</span><span class="p">(</span>
                    <span class="s2">"fk_user_address"</span><span class="p">,</span> <span class="s2">"address"</span><span class="p">,</span>
                    <span class="s2">"user"</span><span class="p">,</span> <span class="p">[</span><span class="s2">"user_id"</span><span class="p">],</span> <span class="p">[</span><span class="s2">"id"</span><span class="p">])</span>
        </pre></div>
        </div>
        <p>This internally generates a <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Table</span></code></a> object
        containing the necessary columns, then generates a new
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">ForeignKeyConstraint</span></code></a>
        object which it then associates with the
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Table</span></code></a>.
        Any event listeners associated with this action will be fired
        off normally.   The <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/ddl.html#sqlalchemy.schema.AddConstraint" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">AddConstraint</span></code></a>
        construct is ultimately used to generate the ALTER statement.</p>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><ul class="simple">
        <li><p><span class="target" id="alembic.operations.Operations.create_foreign_key.params.constraint_name"></span><strong>constraint_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_foreign_key.params.constraint_name">¶</a> – Name of the foreign key constraint.  The name
        is necessary so that an ALTER statement can be emitted.  For setups
        that use an automated naming scheme such as that described at
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/constraints.html#constraint-naming-conventions" title="(in SQLAlchemy v1.4)"><span>Configuring Constraint Naming Conventions</span></a>,
        <code class="docutils literal notranslate"><span class="pre">name</span></code> here can be <code class="docutils literal notranslate"><span class="pre">None</span></code>, as the event listener will
        apply the name to the constraint object when it is associated
        with the table.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_foreign_key.params.source_table"></span><strong>source_table</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_foreign_key.params.source_table">¶</a> – String name of the source table.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_foreign_key.params.referent_table"></span><strong>referent_table</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_foreign_key.params.referent_table">¶</a> – String name of the destination table.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_foreign_key.params.local_cols"></span><strong>local_cols</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_foreign_key.params.local_cols">¶</a> – a list of string column names in the
        source table.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_foreign_key.params.remote_cols"></span><strong>remote_cols</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_foreign_key.params.remote_cols">¶</a> – a list of string column names in the
        remote table.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_foreign_key.params.onupdate"></span><strong>onupdate</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_foreign_key.params.onupdate">¶</a> – Optional string. If set, emit ON UPDATE &lt;value&gt; when
        issuing DDL for this constraint. Typical values include CASCADE,
        DELETE and RESTRICT.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_foreign_key.params.ondelete"></span><strong>ondelete</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_foreign_key.params.ondelete">¶</a> – Optional string. If set, emit ON DELETE &lt;value&gt; when
        issuing DDL for this constraint. Typical values include CASCADE,
        DELETE and RESTRICT.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_foreign_key.params.deferrable"></span><strong>deferrable</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_foreign_key.params.deferrable">¶</a> – optional bool. If set, emit DEFERRABLE or NOT
        DEFERRABLE when issuing DDL for this constraint.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_foreign_key.params.source_schema"></span><strong>source_schema</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_foreign_key.params.source_schema">¶</a> – Optional schema name of the source table.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_foreign_key.params.referent_schema"></span><strong>referent_schema</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_foreign_key.params.referent_schema">¶</a> – Optional schema name of the destination table.</p></li>
        </ul>
        </dd>
        </dl>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.create_index">
        <span class="sig-name descname"><span class="pre">create_index</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">index_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">columns</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Sequence</span><span class="p"><span class="pre">[</span></span><span class="pre">Union</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">,</span> </span><span class="pre">TextClause</span><span class="p"><span class="pre">,</span> </span><span class="pre">Function</span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="n"><span class="pre">schema</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">unique</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/functions.html#bool" title="(in Python v3.10)"><span class="pre">bool</span></a></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kw</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">Table</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#alembic.operations.Operations.create_index" title="Permalink to this definition">¶</a></dt>
        <dd><p>Issue a “create index” instruction using the current
        migration context.</p>
        <p>e.g.:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">alembic</span> <span class="kn">import</span> <span class="n">op</span>
        <span class="n">op</span><span class="o">.</span><span class="n">create_index</span><span class="p">(</span><span class="s1">'ik_test'</span><span class="p">,</span> <span class="s1">'t1'</span><span class="p">,</span> <span class="p">[</span><span class="s1">'foo'</span><span class="p">,</span> <span class="s1">'bar'</span><span class="p">])</span>
        </pre></div>
        </div>
        <p>Functional indexes can be produced by using the
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.text" title="(in SQLAlchemy v1.4)"><code class="xref py py-func docutils literal notranslate"><span class="pre">sqlalchemy.sql.expression.text()</span></code></a> construct:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">alembic</span> <span class="kn">import</span> <span class="n">op</span>
        <span class="kn">from</span> <span class="nn">sqlalchemy</span> <span class="kn">import</span> <span class="n">text</span>
        <span class="n">op</span><span class="o">.</span><span class="n">create_index</span><span class="p">(</span><span class="s1">'ik_test'</span><span class="p">,</span> <span class="s1">'t1'</span><span class="p">,</span> <span class="p">[</span><span class="n">text</span><span class="p">(</span><span class="s1">'lower(foo)'</span><span class="p">)])</span>
        </pre></div>
        </div>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><ul class="simple">
        <li><p><span class="target" id="alembic.operations.Operations.create_index.params.index_name"></span><strong>index_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_index.params.index_name">¶</a> – name of the index.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_index.params.table_name"></span><strong>table_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_index.params.table_name">¶</a> – name of the owning table.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_index.params.columns"></span><strong>columns</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_index.params.columns">¶</a> – a list consisting of string column names and/or
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.text" title="(in SQLAlchemy v1.4)"><code class="xref py py-func docutils literal notranslate"><span class="pre">text()</span></code></a> constructs.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_index.params.schema"></span><strong>schema</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_index.params.schema">¶</a> – Optional schema name to operate within.  To control
        quoting of the schema outside of the default behavior, use
        the SQLAlchemy construct
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">quoted_name</span></code></a>.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_index.params.unique"></span><strong>unique</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_index.params.unique">¶</a> – If True, create a unique index.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_index.params.quote"></span><strong>quote</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_index.params.quote">¶</a> – Force quoting of this column’s name on or off, corresponding
        to <code class="docutils literal notranslate"><span class="pre">True</span></code> or <code class="docutils literal notranslate"><span class="pre">False</span></code>. When left at its default
        of <code class="docutils literal notranslate"><span class="pre">None</span></code>, the column identifier will be quoted according to
        whether the name is case sensitive (identifiers with at least one
        upper case character are treated as case sensitive), or if it’s a
        reserved word. This flag is only needed to force quoting of a
        reserved word which is not known by the SQLAlchemy dialect.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_index.params.**kw"></span><strong>**kw</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_index.params.**kw">¶</a> – Additional keyword arguments not mentioned above are
        dialect specific, and passed in the form
        <code class="docutils literal notranslate"><span class="pre">&lt;dialectname&gt;_&lt;argname&gt;</span></code>.
        See the documentation regarding an individual dialect at
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/dialects/index.html#dialect-toplevel" title="(in SQLAlchemy v1.4)"><span>Dialects</span></a> for detail on documented arguments.</p></li>
        </ul>
        </dd>
        </dl>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.create_primary_key">
        <span class="sig-name descname"><span class="pre">create_primary_key</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">constraint_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">columns</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">List</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="n"><span class="pre">schema</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">Table</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#alembic.operations.Operations.create_primary_key" title="Permalink to this definition">¶</a></dt>
        <dd><p>Issue a “create primary key” instruction using the current
        migration context.</p>
        <p>e.g.:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">alembic</span> <span class="kn">import</span> <span class="n">op</span>
        <span class="n">op</span><span class="o">.</span><span class="n">create_primary_key</span><span class="p">(</span>
                    <span class="s2">"pk_my_table"</span><span class="p">,</span> <span class="s2">"my_table"</span><span class="p">,</span>
                    <span class="p">[</span><span class="s2">"id"</span><span class="p">,</span> <span class="s2">"version"</span><span class="p">]</span>
                <span class="p">)</span>
        </pre></div>
        </div>
        <p>This internally generates a <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Table</span></code></a> object
        containing the necessary columns, then generates a new
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">PrimaryKeyConstraint</span></code></a>
        object which it then associates with the
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Table</span></code></a>.
        Any event listeners associated with this action will be fired
        off normally.   The <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/ddl.html#sqlalchemy.schema.AddConstraint" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">AddConstraint</span></code></a>
        construct is ultimately used to generate the ALTER statement.</p>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><ul class="simple">
        <li><p><span class="target" id="alembic.operations.Operations.create_primary_key.params.constraint_name"></span><strong>constraint_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_primary_key.params.constraint_name">¶</a> – Name of the primary key constraint.  The name
        is necessary so that an ALTER statement can be emitted.  For setups
        that use an automated naming scheme such as that described at
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/constraints.html#constraint-naming-conventions" title="(in SQLAlchemy v1.4)"><span>Configuring Constraint Naming Conventions</span></a>
        <code class="docutils literal notranslate"><span class="pre">name</span></code> here can be <code class="docutils literal notranslate"><span class="pre">None</span></code>, as the event listener will
        apply the name to the constraint object when it is associated
        with the table.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_primary_key.params.table_name"></span><strong>table_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_primary_key.params.table_name">¶</a> – String name of the target table.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_primary_key.params.columns"></span><strong>columns</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_primary_key.params.columns">¶</a> – a list of string column names to be applied to the
        primary key constraint.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_primary_key.params.schema"></span><strong>schema</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_primary_key.params.schema">¶</a> – Optional schema name to operate within.  To control
        quoting of the schema outside of the default behavior, use
        the SQLAlchemy construct
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">quoted_name</span></code></a>.</p></li>
        </ul>
        </dd>
        </dl>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.create_table">
        <span class="sig-name descname"><span class="pre">create_table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">columns</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kw</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">Table</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#alembic.operations.Operations.create_table" title="Permalink to this definition">¶</a></dt>
        <dd><p>Issue a “create table” instruction using the current migration
        context.</p>
        <p>This directive receives an argument list similar to that of the
        traditional <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">sqlalchemy.schema.Table</span></code></a> construct, but without the
        metadata:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">sqlalchemy</span> <span class="kn">import</span> <span class="n">INTEGER</span><span class="p">,</span> <span class="n">VARCHAR</span><span class="p">,</span> <span class="n">NVARCHAR</span><span class="p">,</span> <span class="n">Column</span>
        <span class="kn">from</span> <span class="nn">alembic</span> <span class="kn">import</span> <span class="n">op</span>

        <span class="n">op</span><span class="o">.</span><span class="n">create_table</span><span class="p">(</span>
            <span class="s1">'account'</span><span class="p">,</span>
            <span class="n">Column</span><span class="p">(</span><span class="s1">'id'</span><span class="p">,</span> <span class="n">INTEGER</span><span class="p">,</span> <span class="n">primary_key</span><span class="o">=</span><span class="kc">True</span><span class="p">),</span>
            <span class="n">Column</span><span class="p">(</span><span class="s1">'name'</span><span class="p">,</span> <span class="n">VARCHAR</span><span class="p">(</span><span class="mi">50</span><span class="p">),</span> <span class="n">nullable</span><span class="o">=</span><span class="kc">False</span><span class="p">),</span>
            <span class="n">Column</span><span class="p">(</span><span class="s1">'description'</span><span class="p">,</span> <span class="n">NVARCHAR</span><span class="p">(</span><span class="mi">200</span><span class="p">)),</span>
            <span class="n">Column</span><span class="p">(</span><span class="s1">'timestamp'</span><span class="p">,</span> <span class="n">TIMESTAMP</span><span class="p">,</span> <span class="n">server_default</span><span class="o">=</span><span class="n">func</span><span class="o">.</span><span class="n">now</span><span class="p">())</span>
        <span class="p">)</span>
        </pre></div>
        </div>
        <p>Note that <a class="reference internal" href="#alembic.operations.Operations.create_table" title="alembic.operations.Operations.create_table"><code class="xref py py-meth docutils literal notranslate"><span class="pre">create_table()</span></code></a> accepts
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Column</span></code></a>
        constructs directly from the SQLAlchemy library.  In particular,
        default values to be created on the database side are
        specified using the <code class="docutils literal notranslate"><span class="pre">server_default</span></code> parameter, and not
        <code class="docutils literal notranslate"><span class="pre">default</span></code> which only specifies Python-side defaults:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">alembic</span> <span class="kn">import</span> <span class="n">op</span>
        <span class="kn">from</span> <span class="nn">sqlalchemy</span> <span class="kn">import</span> <span class="n">Column</span><span class="p">,</span> <span class="n">TIMESTAMP</span><span class="p">,</span> <span class="n">func</span>

        <span class="c1"># specify "DEFAULT NOW" along with the "timestamp" column</span>
        <span class="n">op</span><span class="o">.</span><span class="n">create_table</span><span class="p">(</span><span class="s1">'account'</span><span class="p">,</span>
            <span class="n">Column</span><span class="p">(</span><span class="s1">'id'</span><span class="p">,</span> <span class="n">INTEGER</span><span class="p">,</span> <span class="n">primary_key</span><span class="o">=</span><span class="kc">True</span><span class="p">),</span>
            <span class="n">Column</span><span class="p">(</span><span class="s1">'timestamp'</span><span class="p">,</span> <span class="n">TIMESTAMP</span><span class="p">,</span> <span class="n">server_default</span><span class="o">=</span><span class="n">func</span><span class="o">.</span><span class="n">now</span><span class="p">())</span>
        <span class="p">)</span>
        </pre></div>
        </div>
        <p>The function also returns a newly created
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Table</span></code></a> object, corresponding to the table
        specification given, which is suitable for
        immediate SQL operations, in particular
        <a class="reference internal" href="#alembic.operations.Operations.bulk_insert" title="alembic.operations.Operations.bulk_insert"><code class="xref py py-meth docutils literal notranslate"><span class="pre">Operations.bulk_insert()</span></code></a>:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">sqlalchemy</span> <span class="kn">import</span> <span class="n">INTEGER</span><span class="p">,</span> <span class="n">VARCHAR</span><span class="p">,</span> <span class="n">NVARCHAR</span><span class="p">,</span> <span class="n">Column</span>
        <span class="kn">from</span> <span class="nn">alembic</span> <span class="kn">import</span> <span class="n">op</span>

        <span class="n">account_table</span> <span class="o">=</span> <span class="n">op</span><span class="o">.</span><span class="n">create_table</span><span class="p">(</span>
            <span class="s1">'account'</span><span class="p">,</span>
            <span class="n">Column</span><span class="p">(</span><span class="s1">'id'</span><span class="p">,</span> <span class="n">INTEGER</span><span class="p">,</span> <span class="n">primary_key</span><span class="o">=</span><span class="kc">True</span><span class="p">),</span>
            <span class="n">Column</span><span class="p">(</span><span class="s1">'name'</span><span class="p">,</span> <span class="n">VARCHAR</span><span class="p">(</span><span class="mi">50</span><span class="p">),</span> <span class="n">nullable</span><span class="o">=</span><span class="kc">False</span><span class="p">),</span>
            <span class="n">Column</span><span class="p">(</span><span class="s1">'description'</span><span class="p">,</span> <span class="n">NVARCHAR</span><span class="p">(</span><span class="mi">200</span><span class="p">)),</span>
            <span class="n">Column</span><span class="p">(</span><span class="s1">'timestamp'</span><span class="p">,</span> <span class="n">TIMESTAMP</span><span class="p">,</span> <span class="n">server_default</span><span class="o">=</span><span class="n">func</span><span class="o">.</span><span class="n">now</span><span class="p">())</span>
        <span class="p">)</span>

        <span class="n">op</span><span class="o">.</span><span class="n">bulk_insert</span><span class="p">(</span>
            <span class="n">account_table</span><span class="p">,</span>
            <span class="p">[</span>
                <span class="p">{</span><span class="s2">"name"</span><span class="p">:</span> <span class="s2">"A1"</span><span class="p">,</span> <span class="s2">"description"</span><span class="p">:</span> <span class="s2">"account 1"</span><span class="p">},</span>
                <span class="p">{</span><span class="s2">"name"</span><span class="p">:</span> <span class="s2">"A2"</span><span class="p">,</span> <span class="s2">"description"</span><span class="p">:</span> <span class="s2">"account 2"</span><span class="p">},</span>
            <span class="p">]</span>
        <span class="p">)</span>
        </pre></div>
        </div>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><ul class="simple">
        <li><p><span class="target" id="alembic.operations.Operations.create_table.params.table_name"></span><strong>table_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_table.params.table_name">¶</a> – Name of the table</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_table.params.*columns"></span><strong>*columns</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_table.params.*columns">¶</a> – collection of <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Column</span></code></a>
        objects within
        the table, as well as optional <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/constraints.html#sqlalchemy.schema.Constraint" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Constraint</span></code></a>
        objects
        and <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/constraints.html#sqlalchemy.schema.Index" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Index</span></code></a> objects.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_table.params.schema"></span><strong>schema</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_table.params.schema">¶</a> – Optional schema name to operate within.  To control
        quoting of the schema outside of the default behavior, use
        the SQLAlchemy construct
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">quoted_name</span></code></a>.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_table.params.**kw"></span><strong>**kw</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_table.params.**kw">¶</a> – Other keyword arguments are passed to the underlying
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">sqlalchemy.schema.Table</span></code></a> object created for the command.</p></li>
        </ul>
        </dd>
        <dt class="field-even">Returns</dt>
        <dd class="field-even"><p>the <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Table</span></code></a> object corresponding
        to the parameters given.</p>
        </dd>
        </dl>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.create_table_comment">
        <span class="sig-name descname"><span class="pre">create_table_comment</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">comment</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="n"><span class="pre">existing_comment</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/constants.html#None" title="(in Python v3.10)"><span class="pre">None</span></a></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">schema</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">Table</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#alembic.operations.Operations.create_table_comment" title="Permalink to this definition">¶</a></dt>
        <dd><p>Emit a COMMENT ON operation to set the comment for a table.</p>
        <div class="versionadded">
        <p><span class="versionmodified added">New in version 1.0.6.</span></p>
        </div>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><ul class="simple">
        <li><p><span class="target" id="alembic.operations.Operations.create_table_comment.params.table_name"></span><strong>table_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_table_comment.params.table_name">¶</a> – string name of the target table.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_table_comment.params.comment"></span><strong>comment</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_table_comment.params.comment">¶</a> – string value of the comment being registered against
        the specified table.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_table_comment.params.existing_comment"></span><strong>existing_comment</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_table_comment.params.existing_comment">¶</a> – String value of a comment
        already registered on the specified table, used within autogenerate
        so that the operation is reversible, but not required for direct
        use.</p></li>
        </ul>
        </dd>
        </dl>
        <div class="admonition seealso">
        <p class="admonition-title">See also</p>
        <p><a class="reference internal" href="#alembic.operations.Operations.drop_table_comment" title="alembic.operations.Operations.drop_table_comment"><code class="xref py py-meth docutils literal notranslate"><span class="pre">Operations.drop_table_comment()</span></code></a></p>
        <p><a class="reference internal" href="#alembic.operations.Operations.alter_column.params.comment" title="alembic.operations.Operations.alter_column"><code class="xref py py-paramref docutils literal notranslate"><span class="pre">Operations.alter_column.comment</span></code></a></p>
        </div>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.create_unique_constraint">
        <span class="sig-name descname"><span class="pre">create_unique_constraint</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">constraint_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">columns</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Sequence</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="n"><span class="pre">schema</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kw</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Any</span></span></span><a class="headerlink" href="#alembic.operations.Operations.create_unique_constraint" title="Permalink to this definition">¶</a></dt>
        <dd><p>Issue a “create unique constraint” instruction using the
        current migration context.</p>
        <p>e.g.:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">alembic</span> <span class="kn">import</span> <span class="n">op</span>
        <span class="n">op</span><span class="o">.</span><span class="n">create_unique_constraint</span><span class="p">(</span><span class="s2">"uq_user_name"</span><span class="p">,</span> <span class="s2">"user"</span><span class="p">,</span> <span class="p">[</span><span class="s2">"name"</span><span class="p">])</span>
        </pre></div>
        </div>
        <p>This internally generates a <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Table</span></code></a> object
        containing the necessary columns, then generates a new
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/constraints.html#sqlalchemy.schema.UniqueConstraint" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">UniqueConstraint</span></code></a>
        object which it then associates with the
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Table</span></code></a>.
        Any event listeners associated with this action will be fired
        off normally.   The <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/ddl.html#sqlalchemy.schema.AddConstraint" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">AddConstraint</span></code></a>
        construct is ultimately used to generate the ALTER statement.</p>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><ul class="simple">
        <li><p><span class="target" id="alembic.operations.Operations.create_unique_constraint.params.name"></span><strong>name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_unique_constraint.params.name">¶</a> – Name of the unique constraint.  The name is necessary
        so that an ALTER statement can be emitted.  For setups that
        use an automated naming scheme such as that described at
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/constraints.html#constraint-naming-conventions" title="(in SQLAlchemy v1.4)"><span>Configuring Constraint Naming Conventions</span></a>,
        <code class="docutils literal notranslate"><span class="pre">name</span></code> here can be <code class="docutils literal notranslate"><span class="pre">None</span></code>, as the event listener will
        apply the name to the constraint object when it is associated
        with the table.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_unique_constraint.params.table_name"></span><strong>table_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_unique_constraint.params.table_name">¶</a> – String name of the source table.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_unique_constraint.params.columns"></span><strong>columns</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_unique_constraint.params.columns">¶</a> – a list of string column names in the
        source table.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_unique_constraint.params.deferrable"></span><strong>deferrable</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_unique_constraint.params.deferrable">¶</a> – optional bool. If set, emit DEFERRABLE or
        NOT DEFERRABLE when issuing DDL for this constraint.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_unique_constraint.params.initially"></span><strong>initially</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_unique_constraint.params.initially">¶</a> – optional string. If set, emit INITIALLY &lt;value&gt;
        when issuing DDL for this constraint.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.create_unique_constraint.params.schema"></span><strong>schema</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.create_unique_constraint.params.schema">¶</a> – Optional schema name to operate within.  To control
        quoting of the schema outside of the default behavior, use
        the SQLAlchemy construct
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">quoted_name</span></code></a>.</p></li>
        </ul>
        </dd>
        </dl>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.drop_column">
        <span class="sig-name descname"><span class="pre">drop_column</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">schema</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kw</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">Table</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#alembic.operations.Operations.drop_column" title="Permalink to this definition">¶</a></dt>
        <dd><p>Issue a “drop column” instruction using the current
        migration context.</p>
        <p>e.g.:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="n">drop_column</span><span class="p">(</span><span class="s1">'organization'</span><span class="p">,</span> <span class="s1">'account_id'</span><span class="p">)</span>
        </pre></div>
        </div>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><ul class="simple">
        <li><p><span class="target" id="alembic.operations.Operations.drop_column.params.table_name"></span><strong>table_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.drop_column.params.table_name">¶</a> – name of table</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.drop_column.params.column_name"></span><strong>column_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.drop_column.params.column_name">¶</a> – name of column</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.drop_column.params.schema"></span><strong>schema</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.drop_column.params.schema">¶</a> – Optional schema name to operate within.  To control
        quoting of the schema outside of the default behavior, use
        the SQLAlchemy construct
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">quoted_name</span></code></a>.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.drop_column.params.mssql_drop_check"></span><strong>mssql_drop_check</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.drop_column.params.mssql_drop_check">¶</a> – Optional boolean.  When <code class="docutils literal notranslate"><span class="pre">True</span></code>, on
        Microsoft SQL Server only, first
        drop the CHECK constraint on the column using a
        SQL-script-compatible
        block that selects into a @variable from sys.check_constraints,
        then exec’s a separate DROP CONSTRAINT for that constraint.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.drop_column.params.mssql_drop_default"></span><strong>mssql_drop_default</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.drop_column.params.mssql_drop_default">¶</a> – Optional boolean.  When <code class="docutils literal notranslate"><span class="pre">True</span></code>, on
        Microsoft SQL Server only, first
        drop the DEFAULT constraint on the column using a
        SQL-script-compatible
        block that selects into a @variable from sys.default_constraints,
        then exec’s a separate DROP CONSTRAINT for that default.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.drop_column.params.mssql_drop_foreign_key"></span><strong>mssql_drop_foreign_key</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.drop_column.params.mssql_drop_foreign_key">¶</a> – Optional boolean.  When <code class="docutils literal notranslate"><span class="pre">True</span></code>, on
        Microsoft SQL Server only, first
        drop a single FOREIGN KEY constraint on the column using a
        SQL-script-compatible
        block that selects into a @variable from
        sys.foreign_keys/sys.foreign_key_columns,
        then exec’s a separate DROP CONSTRAINT for that default.  Only
        works if the column has exactly one FK constraint which refers to
        it, at the moment.</p></li>
        </ul>
        </dd>
        </dl>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.drop_constraint">
        <span class="sig-name descname"><span class="pre">drop_constraint</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">constraint_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">type_</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">schema</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">Table</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#alembic.operations.Operations.drop_constraint" title="Permalink to this definition">¶</a></dt>
        <dd><p>Drop a constraint of the given name, typically via DROP CONSTRAINT.</p>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><ul class="simple">
        <li><p><span class="target" id="alembic.operations.Operations.drop_constraint.params.constraint_name"></span><strong>constraint_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.drop_constraint.params.constraint_name">¶</a> – name of the constraint.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.drop_constraint.params.table_name"></span><strong>table_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.drop_constraint.params.table_name">¶</a> – table name.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.drop_constraint.params.type_"></span><strong>type_</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.drop_constraint.params.type_">¶</a> – optional, required on MySQL.  can be
        ‘foreignkey’, ‘primary’, ‘unique’, or ‘check’.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.drop_constraint.params.schema"></span><strong>schema</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.drop_constraint.params.schema">¶</a> – Optional schema name to operate within.  To control
        quoting of the schema outside of the default behavior, use
        the SQLAlchemy construct
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">quoted_name</span></code></a>.</p></li>
        </ul>
        </dd>
        </dl>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.drop_index">
        <span class="sig-name descname"><span class="pre">drop_index</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">index_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">schema</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kw</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">Table</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#alembic.operations.Operations.drop_index" title="Permalink to this definition">¶</a></dt>
        <dd><p>Issue a “drop index” instruction using the current
        migration context.</p>
        <p>e.g.:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="n">drop_index</span><span class="p">(</span><span class="s2">"accounts"</span><span class="p">)</span>
        </pre></div>
        </div>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><ul class="simple">
        <li><p><span class="target" id="alembic.operations.Operations.drop_index.params.index_name"></span><strong>index_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.drop_index.params.index_name">¶</a> – name of the index.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.drop_index.params.table_name"></span><strong>table_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.drop_index.params.table_name">¶</a> – name of the owning table.  Some
        backends such as Microsoft SQL Server require this.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.drop_index.params.schema"></span><strong>schema</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.drop_index.params.schema">¶</a> – Optional schema name to operate within.  To control
        quoting of the schema outside of the default behavior, use
        the SQLAlchemy construct
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">quoted_name</span></code></a>.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.drop_index.params.**kw"></span><strong>**kw</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.drop_index.params.**kw">¶</a> – Additional keyword arguments not mentioned above are
        dialect specific, and passed in the form
        <code class="docutils literal notranslate"><span class="pre">&lt;dialectname&gt;_&lt;argname&gt;</span></code>.
        See the documentation regarding an individual dialect at
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/dialects/index.html#dialect-toplevel" title="(in SQLAlchemy v1.4)"><span>Dialects</span></a> for detail on documented arguments.</p></li>
        </ul>
        </dd>
        </dl>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.drop_table">
        <span class="sig-name descname"><span class="pre">drop_table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">schema</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kw</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><a class="reference external" href="https://docs.python.org/3/library/constants.html#None" title="(in Python v3.10)"><span class="pre">None</span></a></span></span><a class="headerlink" href="#alembic.operations.Operations.drop_table" title="Permalink to this definition">¶</a></dt>
        <dd><p>Issue a “drop table” instruction using the current
        migration context.</p>
        <p>e.g.:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="n">drop_table</span><span class="p">(</span><span class="s2">"accounts"</span><span class="p">)</span>
        </pre></div>
        </div>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><ul class="simple">
        <li><p><span class="target" id="alembic.operations.Operations.drop_table.params.table_name"></span><strong>table_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.drop_table.params.table_name">¶</a> – Name of the table</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.drop_table.params.schema"></span><strong>schema</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.drop_table.params.schema">¶</a> – Optional schema name to operate within.  To control
        quoting of the schema outside of the default behavior, use
        the SQLAlchemy construct
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">quoted_name</span></code></a>.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.drop_table.params.**kw"></span><strong>**kw</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.drop_table.params.**kw">¶</a> – Other keyword arguments are passed to the underlying
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">sqlalchemy.schema.Table</span></code></a> object created for the command.</p></li>
        </ul>
        </dd>
        </dl>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.drop_table_comment">
        <span class="sig-name descname"><span class="pre">drop_table_comment</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">existing_comment</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">schema</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">Table</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#alembic.operations.Operations.drop_table_comment" title="Permalink to this definition">¶</a></dt>
        <dd><p>Issue a “drop table comment” operation to
        remove an existing comment set on a table.</p>
        <div class="versionadded">
        <p><span class="versionmodified added">New in version 1.0.6.</span></p>
        </div>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><ul class="simple">
        <li><p><span class="target" id="alembic.operations.Operations.drop_table_comment.params.table_name"></span><strong>table_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.drop_table_comment.params.table_name">¶</a> – string name of the target table.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.drop_table_comment.params.existing_comment"></span><strong>existing_comment</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.drop_table_comment.params.existing_comment">¶</a> – An optional string value of a comment already
        registered on the specified table.</p></li>
        </ul>
        </dd>
        </dl>
        <div class="admonition seealso">
        <p class="admonition-title">See also</p>
        <p><a class="reference internal" href="#alembic.operations.Operations.create_table_comment" title="alembic.operations.Operations.create_table_comment"><code class="xref py py-meth docutils literal notranslate"><span class="pre">Operations.create_table_comment()</span></code></a></p>
        <p><a class="reference internal" href="#alembic.operations.Operations.alter_column.params.comment" title="alembic.operations.Operations.alter_column"><code class="xref py py-paramref docutils literal notranslate"><span class="pre">Operations.alter_column.comment</span></code></a></p>
        </div>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.execute">
        <span class="sig-name descname"><span class="pre">execute</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">sqltext</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Union</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">,</span> </span><span class="pre">TextClause</span><span class="p"><span class="pre">,</span> </span><span class="pre">Update</span><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="n"><span class="pre">execution_options</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/constants.html#None" title="(in Python v3.10)"><span class="pre">None</span></a></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">Table</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#alembic.operations.Operations.execute" title="Permalink to this definition">¶</a></dt>
        <dd><p>Execute the given SQL using the current migration context.</p>
        <p>The given SQL can be a plain string, e.g.:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="n">op</span><span class="o">.</span><span class="n">execute</span><span class="p">(</span><span class="s2">"INSERT INTO table (foo) VALUES ('some value')"</span><span class="p">)</span>
        </pre></div>
        </div>
        <p>Or it can be any kind of Core SQL Expression construct, such as
        below where we use an update construct:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">sqlalchemy.sql</span> <span class="kn">import</span> <span class="n">table</span><span class="p">,</span> <span class="n">column</span>
        <span class="kn">from</span> <span class="nn">sqlalchemy</span> <span class="kn">import</span> <span class="n">String</span>
        <span class="kn">from</span> <span class="nn">alembic</span> <span class="kn">import</span> <span class="n">op</span>

        <span class="n">account</span> <span class="o">=</span> <span class="n">table</span><span class="p">(</span><span class="s1">'account'</span><span class="p">,</span>
            <span class="n">column</span><span class="p">(</span><span class="s1">'name'</span><span class="p">,</span> <span class="n">String</span><span class="p">)</span>
        <span class="p">)</span>
        <span class="n">op</span><span class="o">.</span><span class="n">execute</span><span class="p">(</span>
            <span class="n">account</span><span class="o">.</span><span class="n">update</span><span class="p">()</span><span class="o">.</span>\\
                <span class="n">where</span><span class="p">(</span><span class="n">account</span><span class="o">.</span><span class="n">c</span><span class="o">.</span><span class="n">name</span><span class="o">==</span><span class="n">op</span><span class="o">.</span><span class="n">inline_literal</span><span class="p">(</span><span class="s1">'account 1'</span><span class="p">))</span><span class="o">.</span>\\
                <span class="n">values</span><span class="p">({</span><span class="s1">'name'</span><span class="p">:</span><span class="n">op</span><span class="o">.</span><span class="n">inline_literal</span><span class="p">(</span><span class="s1">'account 2'</span><span class="p">)})</span>
                <span class="p">)</span>
        </pre></div>
        </div>
        <p>Above, we made use of the SQLAlchemy
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/selectable.html#sqlalchemy.sql.expression.table" title="(in SQLAlchemy v1.4)"><code class="xref py py-func docutils literal notranslate"><span class="pre">sqlalchemy.sql.expression.table()</span></code></a> and
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.column" title="(in SQLAlchemy v1.4)"><code class="xref py py-func docutils literal notranslate"><span class="pre">sqlalchemy.sql.expression.column()</span></code></a> constructs to make a brief,
        ad-hoc table construct just for our UPDATE statement.  A full
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Table" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Table</span></code></a> construct of course works perfectly
        fine as well, though note it’s a recommended practice to at least
        ensure the definition of a table is self-contained within the migration
        script, rather than imported from a module that may break compatibility
        with older migrations.</p>
        <p>In a SQL script context, the statement is emitted directly to the
        output stream.   There is <em>no</em> return result, however, as this
        function is oriented towards generating a change script
        that can run in “offline” mode.     Additionally, parameterized
        statements are discouraged here, as they <em>will not work</em> in offline
        mode.  Above, we use <a class="reference internal" href="#alembic.operations.Operations.inline_literal" title="alembic.operations.Operations.inline_literal"><code class="xref py py-meth docutils literal notranslate"><span class="pre">inline_literal()</span></code></a> where parameters are
        to be used.</p>
        <p>For full interaction with a connected database where parameters can
        also be used normally, use the “bind” available from the context:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">alembic</span> <span class="kn">import</span> <span class="n">op</span>
        <span class="n">connection</span> <span class="o">=</span> <span class="n">op</span><span class="o">.</span><span class="n">get_bind</span><span class="p">()</span>

        <span class="n">connection</span><span class="o">.</span><span class="n">execute</span><span class="p">(</span>
            <span class="n">account</span><span class="o">.</span><span class="n">update</span><span class="p">()</span><span class="o">.</span><span class="n">where</span><span class="p">(</span><span class="n">account</span><span class="o">.</span><span class="n">c</span><span class="o">.</span><span class="n">name</span><span class="o">==</span><span class="s1">'account 1'</span><span class="p">)</span><span class="o">.</span>
            <span class="n">values</span><span class="p">({</span><span class="s2">"name"</span><span class="p">:</span> <span class="s2">"account 2"</span><span class="p">})</span>
        <span class="p">)</span>
        </pre></div>
        </div>
        <p>Additionally, when passing the statement as a plain string, it is first
        coerceed into a <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.text" title="(in SQLAlchemy v1.4)"><code class="xref py py-func docutils literal notranslate"><span class="pre">sqlalchemy.sql.expression.text()</span></code></a> construct
        before being passed along.  In the less likely case that the
        literal SQL string contains a colon, it must be escaped with a
        backslash, as:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="n">op</span><span class="o">.</span><span class="n">execute</span><span class="p">(</span><span class="s2">"INSERT INTO table (foo) VALUES ('\:colon_value')"</span><span class="p">)</span>
        </pre></div>
        </div>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><p><span class="target" id="alembic.operations.Operations.execute.params.sqltext"></span><strong>sqltext</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.execute.params.sqltext">¶</a> – Any legal SQLAlchemy expression, including:</p>
        </dd>
        </dl>
        <ul class="simple">
        <li><p>a string</p></li>
        <li><p>a <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.text" title="(in SQLAlchemy v1.4)"><code class="xref py py-func docutils literal notranslate"><span class="pre">sqlalchemy.sql.expression.text()</span></code></a> construct.</p></li>
        <li><p>a <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/dml.html#sqlalchemy.sql.expression.insert" title="(in SQLAlchemy v1.4)"><code class="xref py py-func docutils literal notranslate"><span class="pre">sqlalchemy.sql.expression.insert()</span></code></a> construct.</p></li>
        <li><p>a <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/dml.html#sqlalchemy.sql.expression.update" title="(in SQLAlchemy v1.4)"><code class="xref py py-func docutils literal notranslate"><span class="pre">sqlalchemy.sql.expression.update()</span></code></a>,
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/dml.html#sqlalchemy.sql.expression.insert" title="(in SQLAlchemy v1.4)"><code class="xref py py-func docutils literal notranslate"><span class="pre">sqlalchemy.sql.expression.insert()</span></code></a>,
        or <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/dml.html#sqlalchemy.sql.expression.delete" title="(in SQLAlchemy v1.4)"><code class="xref py py-func docutils literal notranslate"><span class="pre">sqlalchemy.sql.expression.delete()</span></code></a>  construct.</p></li>
        <li><p>Pretty much anything that’s “executable” as described
        in <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/tutorial.html#sqlexpression-toplevel" title="(in SQLAlchemy v1.4)"><span>SQL Expression Language Tutorial (1.x API)</span></a>.</p></li>
        </ul>
        <div class="admonition note">
        <p class="admonition-title">Note</p>
        <p>when passing a plain string, the statement is coerced into
        a <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.text" title="(in SQLAlchemy v1.4)"><code class="xref py py-func docutils literal notranslate"><span class="pre">sqlalchemy.sql.expression.text()</span></code></a> construct. This construct
        considers symbols with colons, e.g. <code class="docutils literal notranslate"><span class="pre">:foo</span></code> to be bound parameters.
        To avoid this, ensure that colon symbols are escaped, e.g.
        <code class="docutils literal notranslate"><span class="pre">\:foo</span></code>.</p>
        </div>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><p><span class="target" id="alembic.operations.Operations.execute.params.execution_options"></span><strong>execution_options</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.execute.params.execution_options">¶</a> – Optional dictionary of
        execution options, will be passed to
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Connection.execution_options" title="(in SQLAlchemy v1.4)"><code class="xref py py-meth docutils literal notranslate"><span class="pre">sqlalchemy.engine.Connection.execution_options()</span></code></a>.</p>
        </dd>
        </dl>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.f">
        <span class="sig-name descname"><span class="pre">f</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">sqlalchemy.sql.elements.conv</span></span></span><a class="headerlink" href="#alembic.operations.Operations.f" title="Permalink to this definition">¶</a></dt>
        <dd><p>Indicate a string name that has already had a naming convention
        applied to it.</p>
        <p>This feature combines with the SQLAlchemy <code class="docutils literal notranslate"><span class="pre">naming_convention</span></code> feature
        to disambiguate constraint names that have already had naming
        conventions applied to them, versus those that have not.  This is
        necessary in the case that the <code class="docutils literal notranslate"><span class="pre">"%(constraint_name)s"</span></code> token
        is used within a naming convention, so that it can be identified
        that this particular name should remain fixed.</p>
        <p>If the <a class="reference internal" href="#alembic.operations.Operations.f" title="alembic.operations.Operations.f"><code class="xref py py-meth docutils literal notranslate"><span class="pre">Operations.f()</span></code></a> is used on a constraint, the naming
        convention will not take effect:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="n">op</span><span class="o">.</span><span class="n">add_column</span><span class="p">(</span><span class="s1">'t'</span><span class="p">,</span> <span class="s1">'x'</span><span class="p">,</span> <span class="n">Boolean</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="n">op</span><span class="o">.</span><span class="n">f</span><span class="p">(</span><span class="s1">'ck_bool_t_x'</span><span class="p">)))</span>
        </pre></div>
        </div>
        <p>Above, the CHECK constraint generated will have the name
        <code class="docutils literal notranslate"><span class="pre">ck_bool_t_x</span></code> regardless of whether or not a naming convention is
        in use.</p>
        <p>Alternatively, if a naming convention is in use, and ‘f’ is not used,
        names will be converted along conventions.  If the <code class="docutils literal notranslate"><span class="pre">target_metadata</span></code>
        contains the naming convention
        <code class="docutils literal notranslate"><span class="pre">{"ck":</span> <span class="pre">"ck_bool_%(table_name)s_%(constraint_name)s"}</span></code>, then the
        output of the following:</p>
        <blockquote>
        <div><p>op.add_column(‘t’, ‘x’, Boolean(name=’x’))</p>
        </div></blockquote>
        <p>will be:</p>
        <div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="n">CONSTRAINT</span> <span class="n">ck_bool_t_x</span> <span class="n">CHECK</span> <span class="p">(</span><span class="n">x</span> <span class="ow">in</span> <span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="mi">0</span><span class="p">)))</span>
        </pre></div>
        </div>
        <p>The function is rendered in the output of autogenerate when
        a particular constraint name is already converted.</p>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.get_bind">
        <span class="sig-name descname"><span class="pre">get_bind</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Connection</span></span></span><a class="headerlink" href="#alembic.operations.Operations.get_bind" title="Permalink to this definition">¶</a></dt>
        <dd><p>Return the current ‘bind’.</p>
        <p>Under normal circumstances, this is the
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Connection" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">Connection</span></code></a> currently being used
        to emit SQL to the database.</p>
        <p>In a SQL script context, this value is <code class="docutils literal notranslate"><span class="pre">None</span></code>. [TODO: verify this]</p>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.get_context">
        <span class="sig-name descname"><span class="pre">get_context</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#alembic.operations.Operations.get_context" title="Permalink to this definition">¶</a></dt>
        <dd><p>Return the <a class="reference internal" href="api/runtime.html#alembic.runtime.migration.MigrationContext" title="alembic.runtime.migration.MigrationContext"><code class="xref py py-class docutils literal notranslate"><span class="pre">MigrationContext</span></code></a> object that’s
        currently in use.</p>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.implementation_for">
        <em class="property"><span class="pre">classmethod</span> </em><span class="sig-name descname"><span class="pre">implementation_for</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">op_cls</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Callable</span></span></span><a class="headerlink" href="#alembic.operations.Operations.implementation_for" title="Permalink to this definition">¶</a></dt>
        <dd><p>Register an implementation for a given <a class="reference internal" href="api/operations.html#alembic.operations.ops.MigrateOperation" title="alembic.operations.ops.MigrateOperation"><code class="xref py py-class docutils literal notranslate"><span class="pre">MigrateOperation</span></code></a>.</p>
        <p>This is part of the operation extensibility API.</p>
        <div class="admonition seealso">
        <p class="admonition-title">See also</p>
        <p><a class="reference internal" href="api/operations.html#operation-plugins"><span class="std std-ref">Operation Plugins</span></a> - example of use</p>
        </div>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.inline_literal">
        <span class="sig-name descname"><span class="pre">inline_literal</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Union</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">,</span> </span><a class="reference external" href="https://docs.python.org/3/library/functions.html#int" title="(in Python v3.10)"><span class="pre">int</span></a><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="n"><span class="pre">type_</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/constants.html#None" title="(in Python v3.10)"><span class="pre">None</span></a></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">_literal_bindparam</span></span></span><a class="headerlink" href="#alembic.operations.Operations.inline_literal" title="Permalink to this definition">¶</a></dt>
        <dd><p>Produce an ‘inline literal’ expression, suitable for
        using in an INSERT, UPDATE, or DELETE statement.</p>
        <p>When using Alembic in “offline” mode, CRUD operations
        aren’t compatible with SQLAlchemy’s default behavior surrounding
        literal values,
        which is that they are converted into bound values and passed
        separately into the <code class="docutils literal notranslate"><span class="pre">execute()</span></code> method of the DBAPI cursor.
        An offline SQL
        script needs to have these rendered inline.  While it should
        always be noted that inline literal values are an <strong>enormous</strong>
        security hole in an application that handles untrusted input,
        a schema migration is not run in this context, so
        literals are safe to render inline, with the caveat that
        advanced types like dates may not be supported directly
        by SQLAlchemy.</p>
        <p>See <a class="reference internal" href="#alembic.operations.Operations.execute" title="alembic.operations.Operations.execute"><code class="xref py py-meth docutils literal notranslate"><span class="pre">execute()</span></code></a> for an example usage of
        <a class="reference internal" href="#alembic.operations.Operations.inline_literal" title="alembic.operations.Operations.inline_literal"><code class="xref py py-meth docutils literal notranslate"><span class="pre">inline_literal()</span></code></a>.</p>
        <p>The environment can also be configured to attempt to render
        “literal” values inline automatically, for those simple types
        that are supported by the dialect; see
        <a class="reference internal" href="api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.literal_binds" title="alembic.runtime.environment.EnvironmentContext.configure"><code class="xref py py-paramref docutils literal notranslate"><span class="pre">EnvironmentContext.configure.literal_binds</span></code></a> for this
        more recently added feature.</p>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><ul class="simple">
        <li><p><span class="target" id="alembic.operations.Operations.inline_literal.params.value"></span><strong>value</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.inline_literal.params.value">¶</a> – The value to render.  Strings, integers, and simple
        numerics should be supported.   Other types like boolean,
        dates, etc. may or may not be supported yet by various
        backends.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.inline_literal.params.type_"></span><strong>type_</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.inline_literal.params.type_">¶</a> – optional - a <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/type_api.html#sqlalchemy.types.TypeEngine" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">sqlalchemy.types.TypeEngine</span></code></a>
        subclass stating the type of this value.  In SQLAlchemy
        expressions, this is usually derived automatically
        from the Python type of the value itself, as well as
        based on the context in which the value is used.</p></li>
        </ul>
        </dd>
        </dl>
        <div class="admonition seealso">
        <p class="admonition-title">See also</p>
        <p><a class="reference internal" href="api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.literal_binds" title="alembic.runtime.environment.EnvironmentContext.configure"><code class="xref py py-paramref docutils literal notranslate"><span class="pre">EnvironmentContext.configure.literal_binds</span></code></a></p>
        </div>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.invoke">
        <span class="sig-name descname"><span class="pre">invoke</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">operation</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">MigrateOperation</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Any</span></span></span><a class="headerlink" href="#alembic.operations.Operations.invoke" title="Permalink to this definition">¶</a></dt>
        <dd><p>Given a <a class="reference internal" href="api/operations.html#alembic.operations.ops.MigrateOperation" title="alembic.operations.ops.MigrateOperation"><code class="xref py py-class docutils literal notranslate"><span class="pre">MigrateOperation</span></code></a>, invoke it in terms of
        this <a class="reference internal" href="#alembic.operations.Operations" title="alembic.operations.Operations"><code class="xref py py-class docutils literal notranslate"><span class="pre">Operations</span></code></a> instance.</p>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.register_operation">
        <em class="property"><span class="pre">classmethod</span> </em><span class="sig-name descname"><span class="pre">register_operation</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">sourcename</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Callable</span></span></span><a class="headerlink" href="#alembic.operations.Operations.register_operation" title="Permalink to this definition">¶</a></dt>
        <dd><p>Register a new operation for this class.</p>
        <p>This method is normally used to add new operations
        to the <a class="reference internal" href="#alembic.operations.Operations" title="alembic.operations.Operations"><code class="xref py py-class docutils literal notranslate"><span class="pre">Operations</span></code></a> class, and possibly the
        <a class="reference internal" href="#alembic.operations.BatchOperations" title="alembic.operations.BatchOperations"><code class="xref py py-class docutils literal notranslate"><span class="pre">BatchOperations</span></code></a> class as well.   All Alembic migration
        operations are implemented via this system, however the system
        is also available as a public API to facilitate adding custom
        operations.</p>
        <div class="admonition seealso">
        <p class="admonition-title">See also</p>
        <p><a class="reference internal" href="api/operations.html#operation-plugins"><span class="std std-ref">Operation Plugins</span></a></p>
        </div>
        </dd></dl>

        <dl class="py method">
        <dt class="sig sig-object py" id="alembic.operations.Operations.rename_table">
        <span class="sig-name descname"><span class="pre">rename_table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">old_table_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">new_table_name</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">schema</span></span><span class="p"><span class="pre">:</span></span> <span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><a class="reference external" href="https://docs.python.org/3/library/stdtypes.html#str" title="(in Python v3.10)"><span class="pre">str</span></a><span class="p"><span class="pre">]</span></span></span> <span class="o"><span class="pre">=</span></span> <span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">→</span> <span class="sig-return-typehint"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">Table</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#alembic.operations.Operations.rename_table" title="Permalink to this definition">¶</a></dt>
        <dd><p>Emit an ALTER TABLE to rename a table.</p>
        <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-odd"><ul class="simple">
        <li><p><span class="target" id="alembic.operations.Operations.rename_table.params.old_table_name"></span><strong>old_table_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.rename_table.params.old_table_name">¶</a> – old name.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.rename_table.params.new_table_name"></span><strong>new_table_name</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.rename_table.params.new_table_name">¶</a> – new name.</p></li>
        <li><p><span class="target" id="alembic.operations.Operations.rename_table.params.schema"></span><strong>schema</strong><a class="paramlink headerlink reference internal" href="#alembic.operations.Operations.rename_table.params.schema">¶</a> – Optional schema name to operate within.  To control
        quoting of the schema outside of the default behavior, use
        the SQLAlchemy construct
        <a class="reference external" href="https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name" title="(in SQLAlchemy v1.4)"><code class="xref py py-class docutils literal notranslate"><span class="pre">quoted_name</span></code></a>.</p></li>
        </ul>
        </dd>
        </dl>
        </dd></dl>

        </dd>
    """

    query = PyQuery(html)

    prefix_temp = '../zh/06_01_{index:0>2d}'

    md_dict = {}

    for index, method in enumerate(query('dl.method>dt').items(), start=1):
        method_name = method.text()

        method_name = method_name.replace('¶', '')

        first_word = method_name.split('(', 1)[0]
        first_word = first_word.replace('classmethod ', '')

        prefix = prefix_temp.format(index=index)

        md_file = f'{prefix}_{first_word}.md'
        md_key = f'#alembic.operations.Operations.{first_word}'

        md_dict[md_key] = md_file
    
    print(json.dumps(md_dict, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parse_section()