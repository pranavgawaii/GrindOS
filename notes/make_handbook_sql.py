import base64
import os

# Load logo
with open("../logo.png", "rb") as img_file:
    LOGO_BASE64 = base64.b64encode(img_file.read()).decode('utf-8')

# ─────────────────────────────────────────
# 40 SQL INTERVIEW TOPICS
# ─────────────────────────────────────────
topics = [
    {
        "id": "sql-01-select",
        "num": "01",
        "chapter": "SQL Fundamentals",
        "title": "SELECT Statement",
        "subtitle": "Projection mechanics and relational query basis.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>The <code>SELECT</code> statement is the foundational command of relational algebra's projection (&pi;) operation, specifying which columns to retrieve from a table. Instead of selecting all columns (<code>*</code>), best practice mandates selecting explicit columns to minimize network payload, disk I/O, and optimize query caches.</p>
</div>
<div class="concept-visual">
  <div class="flow-container">
    <div style="font-size: 8pt; font-weight: 800; color: #EA763F; margin-bottom: 4px;">Projection Flow</div>
    <div style="font-size: 7.5pt; font-family: monospace; background: #FFF5F0; border: 1px solid #EA763F; padding: 4px; border-radius: 4px; width: 100%; text-align: center;">Table [A, B, C, D] (Disk Scan)</div>
    <div style="font-size: 8pt; color: #A0AEC0; margin: 2px 0;">↓ SELECT A, C</div>
    <div style="font-size: 7.5pt; font-family: monospace; background: #F0FFF4; border: 1px solid #38A169; padding: 4px; border-radius: 4px; width: 100%; text-align: center;">Result [A, C] (Memory Projection)</div>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why is using <code>SELECT *</code> considered an anti-pattern in production environments?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Schema Binding</span>
    <span class="buzz-tag">Network Payload</span>
    <span class="buzz-tag">Covering Index</span>
    <span class="buzz-tag">Disk I/O</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Using <code>SELECT *</code> pulls unnecessary columns, increasing memory and network transit times. It also prevents the query optimizer from leveraging covering indexes (where all requested columns reside in the index). Furthermore, schema changes (e.g., adding or reordering columns) can break application integrations that rely on explicit ordinal column bindings."</p>
</div>
""",
        "trap": "Claiming SELECT * has the exact same performance as explicit projection. It requires an extra dictionary metadata lookup to expand * to all columns.",
        "trick": "Always explicitly map columns to save bandwidth and prevent schema drift errors."
    },
    {
        "id": "sql-02-where",
        "num": "02",
        "chapter": "SQL Fundamentals",
        "title": "WHERE Clause",
        "subtitle": "Row-level filtering and sargable predicates.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>The <code>WHERE</code> clause implements relational selection (&sigma;), filtering rows dynamically *before* any grouping or aggregation takes place. To execute efficiently, filter predicates should be 'SARGable' (Search Argument Able), enabling the query optimizer to utilize index seeks rather than full table scans.</p>
</div>
<div class="concept-visual">
  <table class="visual-table">
    <thead>
      <tr><th>Predicate</th><th>SARGable?</th><th>Action</th></tr>
    </thead>
    <tbody>
      <tr><td><code>age = 30</code></td><td style="color:#276749; font-weight:bold;">Yes</td><td>Index Seek</td></tr>
      <tr><td><code>YEAR(date) = 2026</code></td><td style="color:#C53030; font-weight:bold;">No</td><td>Full Table Scan</td></tr>
      <tr><td><code>date >= '2026-01-01'</code></td><td style="color:#276749; font-weight:bold;">Yes</td><td>Index Range Seek</td></tr>
    </tbody>
  </table>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is a SARGable predicate, and why does wrapping a indexed column in a function like <code>LOWER(email) = 'abc'</code> degrade performance?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">SARGable</span>
    <span class="buzz-tag">Index Seek</span>
    <span class="buzz-tag">Table Scan</span>
    <span class="buzz-tag">Function Wrap</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A SARGable predicate allows the database engine to perform an index seek. Wrapping an indexed column in a function (like <code>LOWER()</code> or <code>YEAR()</code>) prevents the optimizer from using the index tree directly, as it must calculate the function's output for every single row, forcing a full table scan."</p>
</div>
""",
        "trap": "Assuming logical operators (AND/OR) have no evaluation order. OR can cause performance drops if columns on both sides are not indexed.",
        "trick": "Keep your filter columns clean and bare—never wrap them in functions inside the WHERE clause."
    },
    {
        "id": "sql-03-orderby",
        "num": "03",
        "chapter": "SQL Fundamentals",
        "title": "ORDER BY Clause",
        "subtitle": "Sorting mechanics and database sort buffers.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>The <code>ORDER BY</code> clause sorts result sets logically. Relational databases do not guarantee any order by default (data is returned as an unordered bag of rows). Sorting requires processing power; it either reads records directly from an ordered index or uses database Sort Buffers (filesort) in memory.</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8pt; line-height: 1.4; background: white; border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 10px;">
    <strong>Sort Execution Paths:</strong><br>
    • <strong>Index Scan:</strong> O(N) reading directly from sorted index leaf nodes.<br>
    • <strong>File Sort:</strong> O(N log N) using sorting algorithms in memory/temp files.
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How does the database execute an <code>ORDER BY</code> query when no index is present, and what is a filesort?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Filesort</span>
    <span class="buzz-tag">Sort Buffer</span>
    <span class="buzz-tag">Temporary Table</span>
    <span class="buzz-tag">Index Scan</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"When no sorted index is available, the engine performs a 'filesort'. It copies matching records to a memory buffer (Sort Buffer) and applies quicksort. If the data size exceeds the sort buffer capacity, it splits the data into temporary disk files, creating high I/O latency."</p>
</div>
""",
        "trap": "Believing ORDER BY is free if output size is small. If sorting millions of rows to output 5, the sort executes on all millions first.",
        "trick": "Create indexes on your ORDER BY columns to eliminate filesorts completely."
    },
    {
        "id": "sql-04-distinct",
        "num": "04",
        "chapter": "SQL Fundamentals",
        "title": "DISTINCT Clause",
        "subtitle": "Deduplication and grouping execution paths.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>The <code>DISTINCT</code> clause filters out duplicate rows, returning only unique values or combinations. Under the hood, databases implement deduplication using either an **Index Scan** (fastest), a **Hash Table aggregation** (hash aggregate), or by **sorting and merging** the result set.</p>
</div>
<div class="concept-visual">
  <div style="text-align: center; padding: 6px; background: white; border: 1px solid #E2E8F0; border-radius: 6px;">
    <div style="font-size: 8pt; font-weight: bold; color: #EA763F;">Deduplication Logic</div>
    <div style="font-size: 7.5pt; font-family: monospace; margin-top: 4px;">Rows [1, 2, 2, 3] → Hash Table Lookup → Unique [1, 2, 3]</div>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is the physical execution difference between <code>SELECT DISTINCT col</code> and <code>SELECT col ... GROUP BY col</code>?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Hash Aggregate</span>
    <span class="buzz-tag">Group Deduplication</span>
    <span class="buzz-tag">Sort Merge</span>
    <span class="buzz-tag">Execution Plan</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"For simple deduplication, modern query optimizers translate both <code>DISTINCT</code> and <code>GROUP BY</code> into the same physical operators (usually Hash Aggregates). However, <code>DISTINCT</code> is logically used to remove duplicates from columns, while <code>GROUP BY</code> is intended to partition rows for aggregate functions."</p>
</div>
""",
        "trap": "Using DISTINCT as a mask to cover duplicate joins. This hides underlying data anomalies and kills query efficiency.",
        "trick": "Ensure Joins are correct rather than throwing DISTINCT on top to mask duplicate issues."
    },
    {
        "id": "sql-05-limit",
        "num": "05",
        "chapter": "SQL Fundamentals",
        "title": "LIMIT & OFFSET",
        "subtitle": "Paging strategies and pagination limits.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>The <code>LIMIT</code> (or <code>TOP</code> / <code>FETCH FIRST</code>) clause limits the number of rows returned. <code>OFFSET</code> skips a specified number of rows. While ideal for frontend paging, high <code>OFFSET</code> queries degrade performance since the database must scan and discard all skipped rows.</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8pt; line-height: 1.4; background: white; border: 1px solid #CBD5E0; border-radius: 6px; padding: 8px 10px;">
    <strong>Offsets Performance Cost:</strong><br>
    • <code>OFFSET 10 LIMIT 10</code>: Scans 20 rows (Fast)<br>
    • <code>OFFSET 10000 LIMIT 10</code>: Scans 10,010 rows, discards 10,000 (Slow)
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why does database performance degrade as OFFSET values increase, and what is Keyset Pagination?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Keyset Pagination</span>
    <span class="buzz-tag">Row Discard</span>
    <span class="buzz-tag">Offset Paging</span>
    <span class="buzz-tag">Seek Method</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"With high offsets, the engine must read all skipped rows from disk and discard them. Keyset Pagination (or cursor paging) avoids this by filtering on the last-seen identifier (e.g., <code>WHERE id > last_seen_id LIMIT 10</code>), performing a direct index seek instead."</p>
</div>
""",
        "trap": "Thinking LIMIT without ORDER BY is deterministic. Without sorting, the rows returned depend on physical page positions, which can change.",
        "trick": "Always use LIMIT in conjunction with an ORDER BY clause for stable, predictable paging."
    },
    {
        "id": "sql-06-groupby",
        "num": "06",
        "chapter": "Filtering & Aggregation",
        "title": "GROUP BY Clause",
        "subtitle": "Aggregation boundaries and hashing execution.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>The <code>GROUP BY</code> clause partitions a result set into groups. The database groups rows using either a **Hash Aggregate** (building an in-memory hash table of unique group keys) or a **Sort Aggregate** (sorting data by keys and summarizing consecutive matching records).</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8.5pt; font-family: monospace; background: white; border: 1px solid #CBD5E0; padding: 6px; border-radius: 6px; text-align: center;">
    <strong>Hash Aggregation Path:</strong><br>
    Key "A" → Hash Index [0] (Sum = 12)<br>
    Key "B" → Hash Index [1] (Sum = 45)
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why can't you select non-aggregated columns in a query that utilizes the <code>GROUP BY</code> clause?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Functional Dependency</span>
    <span class="buzz-tag">SQL Standard</span>
    <span class="buzz-tag">Hash Table Key</span>
    <span class="buzz-tag">Indeterminacy</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Selecting non-aggregated columns that are not part of the <code>GROUP BY</code> clause violates relational logic. Because multiple rows are collapsed into a single row, the database cannot determine which value of the ungrouped column to display, leading to syntax errors."</p>
</div>
""",
        "trap": "Believing GROUP BY automatically sorts results. In older MySQL versions it did, but modern SQL engines require explicit ORDER BY for sorting.",
        "trick": "Ensure all non-aggregate SELECT columns are explicitly defined in the GROUP BY clause."
    },
    {
        "id": "sql-07-having",
        "num": "07",
        "chapter": "Filtering & Aggregation",
        "title": "HAVING Clause",
        "subtitle": "Group-level filters vs row-level filters.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>The <code>HAVING</code> clause filters aggregated groups. Unlike the <code>WHERE</code> clause (which filters rows prior to group generation), <code>HAVING</code> acts on grouped results after aggregation. Mixing their logic can severely degrade performance by delaying filter operations.</p>
</div>
<div class="concept-visual">
  <div class="flow-container">
    <div style="font-size: 7.5pt; background:#FFF5F0; padding:4px; border:1px solid #EA763F; border-radius:4px; width:100%; text-align:center;">Raw Rows</div>
    <div style="font-size:7pt; color:#666; margin: 1px 0;">↓ WHERE (Filters raw rows)</div>
    <div style="font-size:7.5pt; background:#EBF2F9; padding:4px; border:1px solid #2B6CB0; border-radius:4px; width:100%; text-align:center;">GROUP BY (Aggregates)</div>
    <div style="font-size:7pt; color:#666; margin: 1px 0;">↓ HAVING (Filters aggregated keys)</div>
    <div style="font-size:7.5pt; background:#F0FFF4; padding:4px; border:1px solid #38A169; border-radius:4px; width:100%; text-align:center;">Final Groups</div>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is the core difference between <code>WHERE</code> and <code>HAVING</code>, and which runs first?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Logical Execution</span>
    <span class="buzz-tag">Post-Aggregation</span>
    <span class="buzz-tag">Pre-Aggregation</span>
    <span class="buzz-tag">Performance Optimization</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"<code>WHERE</code> filters individual records before groups are formed, whereas <code>HAVING</code> filters group results after aggregation. <code>WHERE</code> is executed first. Filtering records in the <code>WHERE</code> clause is always preferred because it reduces the volume of rows that must be aggregated."</p>
</div>
""",
        "trap": "Placing non-aggregated conditions in HAVING (e.g. HAVING age > 30). This forces the database to aggregate rows that could have been skipped in WHERE.",
        "trick": "Use WHERE for row filtering, and HAVING exclusively for aggregate metrics."
    },
    {
        "id": "sql-08-aggregates",
        "num": "08",
        "chapter": "Filtering & Aggregation",
        "title": "Aggregate Functions",
        "subtitle": "SUM, AVG, COUNT, MIN, MAX and NULL behaviors.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>Aggregate functions collapse columns of values into single scalar metrics. A critical aspect of interview evaluations is understanding how these functions handle `NULL` values. Standard mathematical aggregates discard `NULLs`, whereas `COUNT(*)` counts complete row occurrences.</p>
</div>
<div class="concept-visual">
  <table class="visual-table">
    <thead>
      <tr><th>Salary Col</th><th>COUNT(*)</th><th>COUNT(Salary)</th><th>AVG(Salary)</th></tr>
    </thead>
    <tbody>
      <tr><td>1000<br>NULL<br>2000</td><td style="font-weight:bold;">3</td><td style="font-weight:bold;">2</td><td style="font-weight:bold;">1500 (3000/2)</td></tr>
    </tbody>
  </table>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How do <code>COUNT(*)</code>, <code>COUNT(col)</code>, and <code>AVG(col)</code> differ in handling <code>NULL</code> values?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Null Elimination</span>
    <span class="buzz-tag">Row Count</span>
    <span class="buzz-tag">Aggregate Denominator</span>
    <span class="buzz-tag">COALESCE</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"<code>COUNT(*)</code> counts every row regardless of column content (including NULL rows). <code>COUNT(col)</code> counts only rows where the specified column is not NULL. <code>AVG(col)</code> calculates the sum of non-NULL values divided by the count of non-NULL values. To treat NULL as zero in averages, wrap the column in <code>COALESCE(col, 0)</code>."</p>
</div>
""",
        "trap": "Believing AVG(col) automatically includes NULLs as 0. It completely ignores NULL columns, shifting the mathematical mean higher.",
        "trick": "Always use COALESCE to force database aggregates to treat nulls as zero."
    },
    {
        "id": "sql-09-innerjoin",
        "num": "09",
        "chapter": "Joins",
        "title": "INNER JOIN",
        "subtitle": "Intersection operations and physical join algorithms.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>An <code>INNER JOIN</code> returns rows that match join conditions on both tables, representing a mathematical intersection. Physically, database engines use three core join algorithms: **Nested Loop** (best for small tables), **Hash Join** (best for large unsorted tables), and **Merge Join** (best for sorted indexed relations).</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8pt; line-height: 1.4; background: white; border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 10px;">
    <strong>Physical Join Algorithms:</strong><br>
    • <strong>Nested Loop:</strong> Outer row scans inner table index.<br>
    • <strong>Hash Join:</strong> Build hash table for Table A, probe with B.<br>
    • <strong>Merge Join:</strong> Line up and scan two pre-sorted index lists.
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Explain how a Hash Join works and under what conditions the engine prefers it over a Nested Loop Join."</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Hash Join</span>
    <span class="buzz-tag">Probe Phase</span>
    <span class="buzz-tag">Nested Loop</span>
    <span class="buzz-tag">Build Phase</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A Hash Join operates in two phases: **Build Phase** (reads the smaller table and constructs a hash table of join keys in memory) and **Probe Phase** (scans the larger table, hashing its join keys to look for matches). The engine prefers it over Nested Loop for large, unsorted datasets where indexing is absent."</p>
</div>
""",
        "trap": "Believing join order does not matter. Though logically the same, query optimizers physically swap tables to construct the build phase hash table from the smaller relation.",
        "trick": "Make sure your join keys have identical data types to avoid performance-killing implicit conversions."
    },
    {
        "id": "sql-10-leftjoin",
        "num": "10",
        "chapter": "Joins",
        "title": "LEFT OUTER JOIN",
        "subtitle": "Preserving left relation records with null extensions.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>A <code>LEFT OUTER JOIN</code> preserves all rows of the left-hand table. If a row has a matching record in the right-hand table, columns are combined; otherwise, the right-hand columns are padded with `NULL`. This is primary for identifying unmatched records (anti-patterns).</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8pt; font-family: monospace; background: white; border: 1px solid #CBD5E0; padding: 6px 10px; border-radius: 6px; text-align: center;">
    Left Table [A, B] LEFT JOIN Right Table [B, C]<br>
    → Output: A (Right = NULL), B (Right = B)
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How can you use a <code>LEFT JOIN</code> to find records in Table A that have no matching records in Table B, and what is this pattern called?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Anti-Join</span>
    <span class="buzz-tag">Null Filtering</span>
    <span class="buzz-tag">Outer Join Exclusion</span>
    <span class="buzz-tag">Execution Scan</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"This is called an **Anti-Join**. It is implemented by left-joining Table A with Table B and filtering for non-matches in the <code>WHERE</code> clause: <code>SELECT A.* FROM A LEFT JOIN B ON A.id = B.id WHERE B.id IS NULL</code>. The optimizer filters rows where B's columns resolve to NULL."</p>
</div>
""",
        "trap": "Placing right-table filters in the WHERE clause instead of ON. E.g. WHERE B.status = 'Active' implicitly turns a LEFT JOIN into an INNER JOIN because NULL status fails the filter.",
        "trick": "Always place right-table filter predicates inside the ON clause of a LEFT JOIN."
    },
    {
        "id": "sql-11-rightjoin",
        "num": "11",
        "chapter": "Joins",
        "title": "RIGHT OUTER JOIN",
        "subtitle": "Preserving right relation records and query compiler transformations.",
        "yield_stars": "★★★☆☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>A <code>RIGHT OUTER JOIN</code> functions exactly like a <code>LEFT JOIN</code>, but preserves all records of the right-hand table instead. In practice, query compilers instantly convert all `RIGHT JOIN` structures into equivalent `LEFT JOIN` syntax under the hood to standardize execution planning.</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8pt; line-height: 1.4; background: white; border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 10px;">
    <strong>Compiler Rewrite:</strong><br>
    <code>SELECT * FROM A RIGHT JOIN B ON A.id = B.id</code><br>
    Is compiled as:<br>
    <code>SELECT * FROM B LEFT JOIN A ON B.id = A.id</code>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why are <code>RIGHT OUTER JOIN</code> statements rarely written in production-grade SQL code?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Readability</span>
    <span class="buzz-tag">Left-to-Right Flow</span>
    <span class="buzz-tag">Optimizer Rewrite</span>
    <span class="buzz-tag">Equivalence</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Because humans read text left-to-right, writing <code>LEFT JOIN</code> queries matches standard logical processing workflows. <code>RIGHT JOIN</code> queries make complex multi-join trees hard to read, and because the optimizer compiles them to <code>LEFT JOIN</code> anyway, they provide zero performance advantage."</p>
</div>
""",
        "trap": "Stating that RIGHT JOIN is faster or slower than LEFT JOIN. They are physically compiled to the exact same execution plan.",
        "trick": "Standardize on LEFT JOIN to maintain code readability and simple join hierarchies."
    },
    {
        "id": "sql-12-fulljoin",
        "num": "12",
        "chapter": "Joins",
        "title": "FULL OUTER JOIN",
        "subtitle": "Union joins and matching null padding.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>A <code>FULL OUTER JOIN</code> (or <code>FULL JOIN</code>) returns all records from both tables. When a match exists, rows are combined; when no match exists, columns of the unmatched table are populated with `NULL`. It represents the mathematical union of two datasets.</p>
</div>
<div class="concept-visual">
  <div style="text-align: center; padding: 6px; background: white; border: 1px solid #E2E8F0; border-radius: 6px;">
    <div style="font-size: 8pt; font-weight: bold; color: #EA763F;">Full Join Logic</div>
    <div style="font-size: 7.5pt; font-family: monospace; margin-top: 4px;">Table A [1, 2] FULL JOIN Table B [2, 3] → Results [1 (Null), 2 (2), Null (3)]</div>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How do you emulate a <code>FULL OUTER JOIN</code> in database engines (like MySQL) that do not support it natively?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">UNION Operator</span>
    <span class="buzz-tag">LEFT JOIN</span>
    <span class="buzz-tag">RIGHT JOIN</span>
    <span class="buzz-tag">Deduplication</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"In MySQL, you emulate a <code>FULL OUTER JOIN</code> by executing a <code>LEFT JOIN</code> and a <code>RIGHT JOIN</code> on the tables, and merging the two result sets using the <code>UNION</code> operator. <code>UNION</code> automatically filters out the duplicate matching records generated by both joins."</p>
</div>
""",
        "trap": "Using UNION ALL instead of UNION when emulating FULL OUTER JOIN. UNION ALL will retain duplicate rows for matching records.",
        "trick": "Always use UNION (not UNION ALL) to combine LEFT and RIGHT joins for a correct full join emulation."
    },
    {
        "id": "sql-13-selfjoin",
        "num": "13",
        "chapter": "Joins",
        "title": "SELF JOIN",
        "subtitle": "Recursive mappings and alias resolution.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>A <code>SELF JOIN</code> is a standard join query that joins a table to itself. This is not a separate relational operator; rather, it is a technique used to map hierarchical or recursive relationships (like Manager-Employee or Parent-Child nodes) within a single table.</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8pt; line-height: 1.4; background: white; border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 10px;">
    <strong>Hierarchical Schema Mapping:</strong><br>
    Employee Table (emp_id, name, manager_id)<br>
    • Join: <code>emp E JOIN emp M ON E.manager_id = M.emp_id</code>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why are table aliases mandatory when performing a <code>SELF JOIN</code>, and what happens if you omit them?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Table Alias</span>
    <span class="buzz-tag">Ambiguity</span>
    <span class="buzz-tag">Namespace Conflict</span>
    <span class="buzz-tag">Self-Reference</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Table aliases are mandatory to resolve column name ambiguity. Without aliases, the database engine cannot distinguish which copy of the table a column belongs to, resulting in namespace conflicts and parsing errors."</p>
</div>
""",
        "trap": "Believing a SELF JOIN requires a unique join keyword. It uses standard INNER or LEFT JOIN syntax with the same table name listed twice.",
        "trick": "Differentiate references by using clear alias names like 'E' (employee) and 'M' (manager)."
    },
    {
        "id": "sql-14-crossjoin",
        "num": "14",
        "chapter": "Joins",
        "title": "CROSS JOIN",
        "subtitle": "Cartesian products and multi-dimension matrix setups.",
        "yield_stars": "★★★☆☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>A <code>CROSS JOIN</code> returns the Cartesian product of the joined tables, pairing every row of the first table with every row of the second. The size of the resulting set is multiplicative (Table A rows &times; Table B rows). It is used to generate permutations or test matrices.</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8pt; font-family: monospace; background: white; border: 1px solid #CBD5E0; padding: 6px 10px; border-radius: 6px; text-align: center;">
    Table A (3 rows) CROSS JOIN Table B (5 rows)<br>
    → Output size: 3 &times; 5 = 15 rows
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is the danger of executing an unintended <code>CROSS JOIN</code> on large production databases, and how does it happen?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Cartesian Explosion</span>
    <span class="buzz-tag">Missing Join Criteria</span>
    <span class="buzz-tag">Memory Thrashing</span>
    <span class="buzz-tag">Temp Space Exhaustion</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Unintended Cartesian products occur when join criteria (the <code>ON</code> clause) are omitted. Joining a 10,000-row table with a 100,000-row table produces 1,000,000,000 rows. This 'Cartesian explosion' triggers out-of-memory errors and exhausts temp tablespace storage."</p>
</div>
""",
        "trap": "Assuming CROSS JOIN is useless in production. It is highly useful for generating master calendars, timezone grid matrices, or inventory item combinations.",
        "trick": "Always double check that your INNER JOINs have valid ON conditions to prevent accidental CROSS JOINs."
    },
    {
        "id": "sql-15-subqueries",
        "num": "15",
        "chapter": "Subqueries",
        "title": "Subqueries (Nested Queries)",
        "subtitle": "Nested expressions and logical evaluation zones.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>A subquery is a nested <code>SELECT</code> statement. Subqueries can be: **Scalar** (returns one value), **Row** (returns one record), or **Table** (returns multiple rows). They can be nested in <code>SELECT</code>, <code>FROM</code>, <code>WHERE</code>, or <code>HAVING</code> clauses.</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8pt; line-height: 1.4; background: white; border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 10px;">
    <strong>Subquery Classifications:</strong><br>
    • <strong>Scalar:</strong> <code>SELECT (SELECT MAX(price) FROM P) FROM T</code><br>
    • <strong>Filter Table:</strong> <code>WHERE id IN (SELECT id FROM Active)</code>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is the difference between a subquery nested in the <code>FROM</code> clause vs one in the <code>WHERE</code> clause?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Derived Table</span>
    <span class="buzz-tag">Inline View</span>
    <span class="buzz-tag">Predicate Filter</span>
    <span class="buzz-tag">Optimizer Scope</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A subquery in the <code>FROM</code> clause acts as a **Derived Table** (or inline view). It must be assigned an alias and is treated as a temporary relation. A subquery in the <code>WHERE</code> clause acts as a **Predicate Filter** (evaluating conditions row-by-row to filter outer table rows)."</p>
</div>
""",
        "trap": "Believing subqueries are always evaluated before the outer query. While true for basic subqueries, correlated subqueries behave differently.",
        "trick": "Always assign aliases to subqueries placed in the FROM clause to prevent parser errors."
    },
    {
        "id": "sql-16-correlated",
        "num": "16",
        "chapter": "Subqueries",
        "title": "Correlated Subqueries",
        "subtitle": "Row-by-row dependency loops and performance issues.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>A correlated subquery is a nested query that references one or more columns from the outer query. Unlike independent subqueries (which execute once), a correlated subquery must theoretically execute once for every single candidate row processed by the outer query.</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8pt; line-height: 1.4; background: white; border: 1px solid #CBD5E0; border-radius: 6px; padding: 8px 10px;">
    <strong>Correlated Loop Mechanism:</strong><br>
    For each Outer Row (R):<br>
    &nbsp;&nbsp;Evaluate Inner Query using R.col<br>
    &nbsp;&nbsp;If True → Retain R; else Discard R.<br>
    • Complexity: <strong>O(Outer_Rows &times; Inner_Rows)</strong>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why are correlated subqueries generally avoided in high-performance production databases, and what is the alternative?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Row-by-Row Loop</span>
    <span class="buzz-tag">O(N^2) Complexity</span>
    <span class="buzz-tag">Query Decorrelation</span>
    <span class="buzz-tag">JOIN / CTE Rewrite</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Correlated subqueries create O(N&times;M) execution paths due to row-by-row outer dependencies. Query optimizers attempt to 'decorrelate' them, but complex queries fail to optimize. Re-writing them using Joins, CTEs, or window functions allows the engine to perform set-based index scans."</p>
</div>
""",
        "trap": "Believing EXISTS queries are always slow correlated queries. EXISTS correlates by design but short-circuits upon the first match, making them highly efficient.",
        "trick": "Rewrite correlated queries to INNER JOINs with aggregated subqueries to compute statistics in bulk."
    },
    {
        "id": "sql-17-cte",
        "num": "17",
        "chapter": "Advanced SQL",
        "title": "CTEs (Common Table Expressions)",
        "subtitle": "Logical query modularity and recursive CTE execution.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>A Common Table Expression (CTE) is a temporary result set defined using the <code>WITH</code> clause. CTEs improve readability by breaking complex logic into modular blocks. Special **Recursive CTEs** referencing themselves are used to traverse trees and graphs.</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8pt; line-height: 1.4; background: white; border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 10px;">
    <strong>Recursive CTE Anchor/Recursive Union:</strong><br>
    <code>WITH RECURSIVE Hierarchy AS (</code><br>
    &nbsp;&nbsp;<code>SELECT Anchor_Row (Base Case)</code><br>
    &nbsp;&nbsp;<code>UNION ALL</code><br>
    &nbsp;&nbsp;<code>SELECT Recursive_Rows JOIN Hierarchy</code><br>
    <code>)</code>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is the execution plan difference between a CTE and a Temp Table, and are CTEs physically materialized?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Inline Optimization</span>
    <span class="buzz-tag">Materialization</span>
    <span class="buzz-tag">Temp Table</span>
    <span class="buzz-tag">Query Scope</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"CTEs exist only during query compilation and are optimized inline by modern query planners (treated like virtual views, usually not materialized). Temporary Tables physically write data to disk/temp tablespaces, support indexing, and are optimal for massive datasets that require repeated queries."</p>
</div>
""",
        "trap": "Believing CTEs act as physical performance boosters. They are logical formatting aids; rewriting a slow subquery to a standard CTE does not automatically speed it up.",
        "trick": "Use recursive CTEs to easily generate lists of dates, numbers, or hierarchies without procedural loops."
    },
    {
        "id": "sql-18-window",
        "num": "18",
        "chapter": "Advanced SQL",
        "title": "Window Functions",
        "subtitle": "Calculations over table partitions and the OVER clause.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>Window functions perform calculations across a set of table rows that are logically related to the current row. Unlike `GROUP BY` (which collapses rows), window functions preserve the identity of each row while returning aggregate or ranking results in new columns.</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8pt; line-height: 1.4; background: white; border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 10px;">
    <strong>Window Syntax Breakdown:</strong><br>
    <code>SUM(val) OVER (PARTITION BY dept ORDER BY date)</code><br>
    • <strong>PARTITION BY:</strong> Group boundary lines.<br>
    • <strong>ORDER BY:</strong> Running frame calculation order.
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Explain the physical difference between grouping data with <code>GROUP BY</code> and executing a window function with the <code>OVER</code> clause."</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Row Identity</span>
    <span class="buzz-tag">Partitioning</span>
    <span class="buzz-tag">Reduction</span>
    <span class="buzz-tag">Window Frame</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"<code>GROUP BY</code> collapses multiple rows into a single summary row, discarding detail fields. A window function processes groups of rows ('windows') but leaves row identities intact, outputting the aggregate calculation on every single row."</p>
</div>
""",
        "trap": "Attempting to filter window outputs inside WHERE (e.g. WHERE ROW_NUMBER() = 1). Window functions execute after WHERE, requiring a CTE to filter results.",
        "trick": "Wrap queries containing window functions in a CTE or outer SELECT to filter on their outputs."
    },
    {
        "id": "sql-19-rownumber",
        "num": "19",
        "chapter": "Advanced SQL",
        "title": "ROW_NUMBER()",
        "subtitle": "Sequential row numbering without ties.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p><code>ROW_NUMBER()</code> assigns a unique, sequential integer to each row within a partition. If multiple rows have identical values in the <code>ORDER BY</code> column, <code>ROW_NUMBER()</code> still assigns distinct sequential numbers arbitrarily (non-deterministic tie resolution).</p>
</div>
<div class="concept-visual">
  <table class="visual-table">
    <thead>
      <tr><th>Value</th><th>ROW_NUMBER()</th></tr>
    </thead>
    <tbody>
      <tr><td>100</td><td style="font-weight:bold;">1</td></tr>
      <tr><td>100 (Tie)</td><td style="font-weight:bold;">2</td></tr>
      <tr><td>200</td><td style="font-weight:bold;">3</td></tr>
    </tbody>
  </table>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How does <code>ROW_NUMBER()</code> resolve duplicate values in its sorting criteria, and how do you make it deterministic?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Determinism</span>
    <span class="buzz-tag">Tie Resolution</span>
    <span class="buzz-tag">Sequential Order</span>
    <span class="buzz-tag">Unique Sort Key</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"<code>ROW_NUMBER()</code> is non-deterministic for tie values—the engine assigns sequence numbers based on physical read orders. To make it deterministic, you must add a tie-breaking column to the sorting clause (e.g., <code>ORDER BY score DESC, unique_id ASC</code>)."</p>
</div>
""",
        "trap": "Expecting ROW_NUMBER() to skip values when ties occur. It always increments by exactly 1.",
        "trick": "Use ROW_NUMBER() to isolate the single latest entry by sorting by timestamp descending."
    },
    {
        "id": "sql-20-rank",
        "num": "20",
        "chapter": "Advanced SQL",
        "title": "RANK()",
        "subtitle": "Ranking with ties and sequence gaps.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p><code>RANK()</code> calculates the rank of each row within a partition. When identical sort values (ties) are encountered, they receive the same rank. However, the function leaves gaps in the sequential ranking values, reflecting the count of duplicated ties.</p>
</div>
<div class="concept-visual">
  <table class="visual-table">
    <thead>
      <tr><th>Score</th><th>RANK() Rank</th></tr>
    </thead>
    <tbody>
      <tr><td>100</td><td style="font-weight:bold;">1</td></tr>
      <tr><td>100 (Tie)</td><td style="font-weight:bold;">1</td></tr>
      <tr><td>90</td><td style="font-weight:bold; color:#C53030;">3 (Gap left)</td></tr>
    </tbody>
  </table>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why does the <code>RANK()</code> function leave gaps in its sequence when ties are found, and how is the gap calculated?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Tie Gaps</span>
    <span class="buzz-tag">Non-Continuous</span>
    <span class="buzz-tag">Ordinal Rank</span>
    <span class="buzz-tag">Window Ordering</span>
  </div>
</div>
<div class="box box-answer">
  <p>"<code>RANK()</code> leaves gaps to preserve the cardinal position of rows. The rank of a row is calculated as <code>1 + (number of rows preceding it that rank higher)</code>. If two rows share rank 1, the third row has 2 rows preceding it, resulting in rank 3."</p>
</div>
""",
        "trap": "Confusing RANK() with DENSE_RANK() in interview questions requesting standard ranking outputs.",
        "trick": "Remember: RANK() leaves gaps (1, 1, 3); DENSE_RANK() keeps it tight (1, 1, 2)."
    },
    {
        "id": "sql-21-denserank",
        "num": "21",
        "chapter": "Advanced SQL",
        "title": "DENSE_RANK()",
        "subtitle": "Continuous ranking without sequence gaps.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p><code>DENSE_RANK()</code> assigns a rank value to each row within a partition. Like <code>RANK()</code>, ties receive the same rank value. However, the sequence is contiguous—no ranks are skipped, and the rank increments by exactly 1 for the next distinct value.</p>
</div>
<div class="concept-visual">
  <table class="visual-table">
    <thead>
      <tr><th>Score</th><th>DENSE_RANK()</th></tr>
    </thead>
    <tbody>
      <tr><td>100</td><td style="font-weight:bold;">1</td></tr>
      <tr><td>100 (Tie)</td><td style="font-weight:bold;">1</td></tr>
      <tr><td>90</td><td style="font-weight:bold; color:#276749;">2 (No gap)</td></tr>
    </tbody>
  </table>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Explain the behavioral difference between <code>ROW_NUMBER()</code>, <code>RANK()</code>, and <code>DENSE_RANK()</code> when sorting data with duplicate values."</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">DENSE_RANK</span>
    <span class="buzz-tag">Contiguous Rank</span>
    <span class="buzz-tag">Duplicate Sorting</span>
    <span class="buzz-tag">Tie Behaviors</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Given three rows with identical sorting values: <code>ROW_NUMBER()</code> outputs unique sequential values: 1, 2, 3. <code>RANK()</code> assigns identical ranks and leaves gaps: 1, 1, 3. <code>DENSE_RANK()</code> assigns identical ranks without gaps: 1, 1, 2."</p>
</div>
""",
        "trap": "Believing DENSE_RANK() is slower than RANK(). Under the hood, they utilize similar window sorting paths and have identical performance costs.",
        "trick": "Always use DENSE_RANK() when calculating Nth highest values (like top salaries) to prevent duplicate value bugs."
    },
    {
        "id": "sql-22-lead",
        "num": "22",
        "chapter": "Advanced SQL",
        "title": "LEAD()",
        "subtitle": "Accessing forward row values and offset offsets.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>The <code>LEAD()</code> window function allows queries to access data from subsequent rows without performing expensive self-joins. You can specify a forward offset distance (default is 1) and define default fallback values for boundary nulls.</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8.5pt; font-family: monospace; background: white; border: 1px solid #CBD5E0; padding: 6px; border-radius: 6px; text-align: center;">
    <strong>LEAD(salary, 1, 0) Flow:</strong><br>
    Row 1 ($1000) → Lead Value = $2000 (Row 2)<br>
    Row 2 ($2000) → Lead Value = $0 (Fallback)
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What does the third argument in the <code>LEAD(col, offset, default)</code> function do, and why is it useful?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Fallback Value</span>
    <span class="buzz-tag">Offset Distance</span>
    <span class="buzz-tag">Null Prevention</span>
    <span class="buzz-tag">Window Boundary</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"The third argument defines a fallback value returned when the window calculation reaches the boundary (i.e. when the forward offset points beyond the end of the partition). This prevents database outputs from returning NULLs, simplifying delta calculations."</p>
</div>
""",
        "trap": "Omitting ORDER BY in LEAD(). Window functions require sorting to logically compute 'forward' rows; omitting it causes syntax or ordering errors.",
        "trick": "Use LEAD() to compare current values with next rows, avoiding self-joins."
    },
    {
        "id": "sql-23-lag",
        "num": "23",
        "chapter": "Advanced SQL",
        "title": "LAG()",
        "subtitle": "Accessing backward row values and time-series deltas.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>The <code>LAG()</code> window function enables access to preceding row values relative to the current row. This is optimal for time-series analysis (e.g. comparing month-over-month sales or daily server metric fluctuations) at O(N) cost.</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8.5pt; font-family: monospace; background: white; border: 1px solid #CBD5E0; padding: 6px; border-radius: 6px; text-align: center;">
    <strong>LAG(sales, 1) Flow:</strong><br>
    Jan ($5k) → Lag Value = NULL<br>
    Feb ($8k) → Lag Value = $5k (Jan)
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How would you write a query to find the percentage increase in sales month-over-month using the <code>LAG()</code> function?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Delta Calculation</span>
    <span class="buzz-tag">Time-Series Analysis</span>
    <span class="buzz-tag">Offset Lag</span>
    <span class="buzz-tag">Preceding Row</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"To calculate sales deltas: <code>SELECT month, sales, LAG(sales) OVER (ORDER BY month) AS prev_sales, ((sales - LAG(sales) OVER (ORDER BY month)) / LAG(sales) OVER (ORDER BY month)) * 100 AS pct_increase FROM monthly_sales</code>."</p>
</div>
""",
        "trap": "Believing LAG() is restricted to offset 1. You can pass any integer offset distance (e.g., LAG(salary, 12) for year-over-year deltas).",
        "trick": "Always define window ordering explicitly inside the OVER() clause when using LAG()."
    },
    {
        "id": "sql-24-indexing",
        "num": "24",
        "chapter": "Indexing & Performance",
        "title": "Database Indexing",
        "subtitle": "B-Tree node storage and index seeks.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>An Index is an auxiliary disk structure that speeds up database record retrieval. Most relational indexes utilize **B-Trees** (specifically B+ Trees), maintaining sorted values in a tree hierarchy (Root -> Internal Nodes -> Leaf Nodes) to reduce lookup complexity to **O(log N)**.</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8pt; line-height: 1.4; background: white; border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 10px;">
    <strong>Index Search Types:</strong><br>
    • <strong>Index Seek:</strong> Traverse the B-Tree directly to locate the match (Fast).<br>
    • <strong>Index Scan:</strong> Traverse the entire sorted index leaf list (Moderate).<br>
    • <strong>Table Scan:</strong> Scan the unordered table on disk (Slow).
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is the physical difference between an Index Seek and an Index Scan in database execution plan outputs?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">B+ Tree</span>
    <span class="buzz-tag">Leaf Node</span>
    <span class="buzz-tag">Index Seek</span>
    <span class="buzz-tag">Index Scan</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"An **Index Seek** traverses the B-Tree from the root node to locate specific matching record leaf keys directly. An **Index Scan** reads all keys sequentially along the index leaf node linked-list, which happens when filter predicates are not matching key orders."</p>
</div>
""",
        "trap": "Assuming indexes make all queries faster. Indexes speed up reads but degrade writes (INSERT/UPDATE/DELETE) because index trees must be modified.",
        "trick": "Always construct index filters to match column ordering in compound indexes."
    },
    {
        "id": "sql-25-clustered",
        "num": "25",
        "chapter": "Indexing & Performance",
        "title": "Clustered Index",
        "subtitle": "Physical sorting and primary key tables.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>A Clustered Index dictates the physical sorting order of table rows on disk. In a clustered index, the leaf nodes of the B+ Tree contain the **actual data pages** of the table. Because physical data can only be sorted one way, a table can only have **one** clustered index.</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8.5pt; font-family: monospace; background: white; border: 1px solid #CBD5E0; padding: 6px; border-radius: 6px; text-align: center;">
    Root Node → Branch Nodes<br>
    → Leaf Nodes (Contain Actual Data Rows 101, 102, 103)
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Does creating a Primary Key constraint automatically create a clustered index, and why can you only have one clustered index?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Physical Sorting</span>
    <span class="buzz-tag">Primary Key</span>
    <span class="buzz-tag">Leaf Data Page</span>
    <span class="buzz-tag">Index Default</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Creating a Primary Key automatically builds a clustered index by default (can be overridden). Because table data pages can only be sorted physically in one physical order (e.g. sorted by ID or sorted by Date), a table can only support one clustered index."</p>
</div>
""",
        "trap": "Believing clustered indexes use extra storage for data duplication. The index is the table itself—data pages are the leaf nodes.",
        "trick": "Use auto-incrementing integers as clustered index keys to prevent page splitting and index fragmentation."
    },
    {
        "id": "sql-26-nonclustered",
        "num": "26",
        "chapter": "Indexing & Performance",
        "title": "Non-Clustered Index",
        "subtitle": "Logical pointers and key lookup overhead.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>A Non-Clustered Index is a logical structure separated from data pages. Leaf nodes of non-clustered B+ Trees do not contain data rows; they store index key values and **pointers** (Row IDs or Clustered Index Keys) pointing to the physical data rows.</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8.5pt; font-family: monospace; background: white; border: 1px solid #CBD5E0; padding: 6px; border-radius: 6px; text-align: center;">
    Leaf Node [Key = "Active"]<br>
    → Pointer → Row ID 412 (Heap Table)<br>
    → Pointer → PK Key 102 (Clustered Table)
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is a Key Lookup (or RID Lookup) operation in execution plans, and how can it be avoided?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Key Lookup</span>
    <span class="buzz-tag">Row Identifier</span>
    <span class="buzz-tag">Covering Index</span>
    <span class="buzz-tag">INCLUDE Clause</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A Key Lookup occurs when a query uses a non-clustered index, but requests columns not stored in the index. The database must traverse the clustered index to fetch those columns. It can be avoided by creating a **Covering Index** that contains those columns using the <code>INCLUDE</code> clause."</p>
</div>
""",
        "trap": "Believing you should index every column. Every index adds write overhead (I/O) to keep index trees in sync during updates.",
        "trick": "Add commonly selected columns to the index INCLUDE clause to cover queries and avoid key lookups."
    },
    {
        "id": "sql-27-optimization",
        "num": "27",
        "chapter": "Indexing & Performance",
        "title": "Query Optimization",
        "subtitle": "SARGable filtering and optimizing execution paths.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>Query Optimization is the process of improving SQL query performance. The optimizer evaluates potential execution plans (Join orderings, index usage, access paths) and selects the lowest-cost path. Avoiding table scans and sargable filters are key optimizations.</p>
</div>
<div class="concept-visual">
  <table class="visual-table">
    <thead>
      <tr><th>Pattern</th><th>Status</th><th>Alternative</th></tr>
    </thead>
    <tbody>
      <tr><td><code>col LIKE '%abc'</code></td><td style="color:#C53030; font-weight:bold;">Bad Scan</td><td>Full Text Search</td></tr>
      <tr><td><code>col LIKE 'abc%'</code></td><td style="color:#276749; font-weight:bold;">Good Seek</td><td>Index Seek (prefix)</td></tr>
      <tr><td><code>OR checks</code></td><td style="color:#C53030; font-weight:bold;">Bad Scan</td><td><code>UNION ALL</code></td></tr>
    </tbody>
  </table>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why does a query filtering with <code>LIKE '%value%'</code> fail to use an index, and what alternatives exist?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Wildcard Prefix</span>
    <span class="buzz-tag">Left-to-Right Sort</span>
    <span class="buzz-tag">Full Table Scan</span>
    <span class="buzz-tag">Full-Text Index</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Indexes are sorted left-to-right. A wildcard prefix (<code>%value</code>) prevents the engine from utilizing sorting sequence, forcing a full table scan. The alternatives are removing the leading wildcard (using prefix matches <code>value%</code>) or using Full-Text Indexes."</p>
</div>
""",
        "trap": "Believing the query optimizer is infallible. Outdated table statistics can cause the optimizer to select bad plans.",
        "trick": "Keep your table statistics updated to help the optimizer select the most efficient execution plans."
    },
    {
        "id": "sql-28-execplan",
        "num": "28",
        "chapter": "Indexing & Performance",
        "title": "Execution Plan Basics",
        "subtitle": "Logical vs physical plan parsing and database costs.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>An Execution Plan is the database engine's step-by-step roadmap for executing a query. In SQL, you review the plan using the <code>EXPLAIN</code> statement, which lists operators (Nested Loops, Hash Joins, Scans, Seeks) and estimated card costs.</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8pt; line-height: 1.4; background: white; border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 10px;">
    <strong>Logical Execution Phases:</strong><br>
    Parser (Syntax Check) → Optimizer (Cost Estimate) → Execution Engine (Physical CPU/IO Read)
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How do you extract the execution plan of a SQL query, and what is estimated cost?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">EXPLAIN Statement</span>
    <span class="buzz-tag">Cost Model</span>
    <span class="buzz-tag">I/O Units</span>
    <span class="buzz-tag">Cardinality Estimate</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"You extract execution plans using <code>EXPLAIN SELECT ...</code> (or <code>EXPLAIN ANALYZE</code> to run and trace execution). The 'cost' represents estimated CPU cycles and disk page I/O reads calculated using table statistics. Planners compare costs to select the cheapest plan."</p>
</div>
""",
        "trap": "Relying on EXPLAIN without ANALYZE. Plain EXPLAIN only shows database planner estimates; EXPLAIN ANALYZE shows actual runtime execution statistics.",
        "trick": "Always use EXPLAIN ANALYZE to compare actual vs estimated rows to detect outdated stats."
    },
    {
        "id": "sql-29-acid",
        "num": "29",
        "chapter": "Transactions",
        "title": "ACID Properties",
        "subtitle": "Transaction guarantees and reliability foundations.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>ACID represents the core guarantees of transactions: **Atomicity** (All-or-Nothing execution), **Consistency** (Transition from valid state to valid state), **Isolation** (Concurrence control segregation), and **Durability** (Committed data survives system crashes).</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8pt; line-height: 1.4; background: white; border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 10px;">
    <strong>ACID Mechanisms:</strong><br>
    • <strong>Atomicity/Durability:</strong> Managed by WAL and Undo/Redo Logs.<br>
    • <strong>Isolation:</strong> Enforced using Locks or Multi-Version Concurrency (MVCC).
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How does the database guarantee Atomicity and Durability during sudden hardware power failures?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Write-Ahead Logging</span>
    <span class="buzz-tag">Redo Log</span>
    <span class="buzz-tag">Undo Segment</span>
    <span class="buzz-tag">Crash Recovery</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"The engine guarantees Atomicity and Durability using Write-Ahead Logging (WAL) and Undo/Redo logs. Prior to table modification, transaction steps are written to disk logs. On reboot, the engine scans the logs: committed steps are re-applied (Redo) and uncommitted steps are reversed (Undo)."</p>
</div>
""",
        "trap": "Believing Consistency is maintained by the DB alone. Consistency requires both database constraints (types, FKs) and correct application logic.",
        "trick": "Wrap multi-table updates in explicit transaction blocks to guarantee data consistency."
    },
    {
        "id": "sql-30-transactions",
        "num": "30",
        "chapter": "Transactions",
        "title": "Transactions",
        "subtitle": "Isolation levels and concurrency anomalies.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>A Transaction is a single logical unit of database work. Managing transaction isolation levels controls concurrency anomalies (Dirty Reads, Non-Repeatable Reads, Phantom Reads) at the cost of processing speed.</p>
</div>
<div class="concept-visual">
  <table class="visual-table" style="font-size: 7pt;">
    <thead>
      <tr><th>Isolation Level</th><th>Dirty Read</th><th>Non-Rep Read</th><th>Phantom Read</th></tr>
    </thead>
    <tbody>
      <tr><td>Read Uncomm.</td><td style="color:#C53030;">Yes</td><td style="color:#C53030;">Yes</td><td style="color:#C53030;">Yes</td></tr>
      <tr><td>Read Comm.</td><td style="color:#276749;">No</td><td style="color:#C53030;">Yes</td><td style="color:#C53030;">Yes</td></tr>
      <tr><td>Repeatable Read</td><td style="color:#276749;">No</td><td style="color:#276749;">No</td><td style="color:#C53030;">Yes (MySQL No)</td></tr>
      <tr><td>Serializable</td><td style="color:#276749;">No</td><td style="color:#276749;">No</td><td style="color:#276749;">No</td></tr>
    </tbody>
  </table>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is the difference between a Non-Repeatable Read and a Phantom Read, and how are they prevented?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Dirty Read</span>
    <span class="buzz-tag">Repeatable Read</span>
    <span class="buzz-tag">Range Lock</span>
    <span class="buzz-tag">MVCC Snapshots</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A **Non-Repeatable Read** occurs when Transaction A reads a row, Transaction B updates it, and Transaction A reads the same row again to find updated values. A **Phantom Read** occurs when Transaction A reads a range of rows, Transaction B inserts new rows in that range, and Transaction A re-reads the range to find new rows. They are prevented using MVCC or Range Locks."</p>
</div>
""",
        "trap": "Assuming Serializable is the best level for all use-cases. It causes heavy lock contention, timeouts, and low concurrency.",
        "trick": "Use Read Committed for general web apps, and Repeatable Read or Serializable exclusively for financial transfers."
    },
    {
        "id": "sql-31-locks",
        "num": "31",
        "chapter": "Transactions",
        "title": "Locks & Concurrency",
        "subtitle": "Shared vs exclusive locks and deadlocks.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>Locks manage concurrent access to database data. The core lock types are **Shared (S) Locks** (read locks) and **Exclusive (X) Locks** (write locks). Conflict matrices dictate that multiple sessions can read, but only one can write.</p>
</div>
<div class="concept-visual">
  <table class="visual-table">
    <thead>
      <tr><th>Lock Matrix</th><th>Shared (S)</th><th>Exclusive (X)</th></tr>
    </thead>
    <tbody>
      <tr><td>Shared (S)</td><td style="color:#276749; font-weight:bold;">Granted</td><td style="color:#C53030; font-weight:bold;">Blocked</td></tr>
      <tr><td>Exclusive (X)</td><td style="color:#C53030; font-weight:bold;">Blocked</td><td style="color:#C53030; font-weight:bold;">Blocked</td></tr>
    </tbody>
  </table>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is a Deadlock, and how does the database engine detect and resolve it?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Deadlock Cycle</span>
    <span class="buzz-tag">Lock Wait Timeout</span>
    <span class="buzz-tag">Transaction Rollback</span>
    <span class="buzz-tag">Dependency Graph</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A Deadlock occurs when Transaction A holds Lock 1 and requests Lock 2, while Transaction B holds Lock 2 and requests Lock 1. The engine detects this cycle using dependency graphs. It resolves it by terminating one transaction (the victim), rolling back its steps, and releasing its locks."</p>
</div>
""",
        "trap": "Believing locks are only column or table level. Databases use Row-level, Page-level, and Table-level locks, upgrading them dynamically (lock escalation).",
        "trick": "Always acquire locks in the same order across different transactions to prevent deadlocks."
    },
    {
        "id": "sql-32-nthsalary",
        "num": "32",
        "chapter": "Interview SQL",
        "title": "Nth Highest Salary",
        "subtitle": "Correlated subqueries vs window functions.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>Finding the Nth highest salary is a classic interview query. It checks the candidate's understanding of subqueries, window functions, and tie-handling. The two standard methods are correlated subqueries and `DENSE_RANK()` functions.</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8pt; font-family: monospace; background: white; border: 1px solid #CBD5E0; padding: 6px 10px; border-radius: 6px; text-align: left;">
    <strong>Method 1: Correlated Subquery</strong><br>
    <code>SELECT DISTINCT salary FROM Employee E1</code><br>
    <code>WHERE N-1 = (</code><br>
    &nbsp;&nbsp;<code>SELECT COUNT(DISTINCT salary)</code><br>
    &nbsp;&nbsp;<code>FROM Employee E2 WHERE E2.salary > E1.salary</code><br>
    <code>)</code>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Write a query to find the Nth highest salary using <code>DENSE_RANK()</code>, and explain why <code>DENSE_RANK()</code> is preferred over <code>RANK()</code>."</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">DENSE_RANK</span>
    <span class="buzz-tag">Window Filtering</span>
    <span class="buzz-tag">Duplicate Salary</span>
    <span class="buzz-tag">Rank Ties</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Query:<br>
  <code>WITH RankedSalary AS (SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rk FROM Employee) SELECT salary FROM RankedSalary WHERE rk = N LIMIT 1;</code><br>
  <code>DENSE_RANK()</code> is preferred because if salaries are tied (e.g. $10k, $10k, $8k), <code>DENSE_RANK()</code> assigns (1, 1, 2) finding $8k as the 2nd highest, whereas <code>RANK()</code> assigns (1, 1, 3), skipping rank 2."</p>
</div>
""",
        "trap": "Using LIMIT offset method (LIMIT 1 OFFSET N-1) without ORDER BY. This returns random rows because data ordering is not guaranteed.",
        "trick": "Always use DENSE_RANK() rather than ROW_NUMBER() when querying top values to handle duplicates correctly."
    },
    {
        "id": "sql-33-duplicates",
        "num": "33",
        "chapter": "Interview SQL",
        "title": "Duplicate Records",
        "subtitle": "Identifying and cleaning database records.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>Duplicate records are matching values in key columns. Identifying duplicates uses `GROUP BY` and `HAVING COUNT(*) > 1`. Removing duplicates requires deleting duplicate row rows while keeping the unique primary key record.</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8pt; font-family: monospace; background: white; border: 1px solid #CBD5E0; padding: 6px 10px; border-radius: 6px; text-align: left;">
    <strong>Delete Duplicate Rows:</strong><br>
    <code>DELETE FROM Users WHERE id NOT IN (</code><br>
    &nbsp;&nbsp;<code>SELECT MIN(id) FROM Users</code><br>
    &nbsp;&nbsp;<code>GROUP BY email</code><br>
    <code>)</code>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How would you delete all duplicate records based on email, keeping only the record with the lowest unique ID?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">GROUP BY</span>
    <span class="buzz-tag">Subquery Exclusion</span>
    <span class="buzz-tag">ROW_NUMBER() Deletion</span>
    <span class="buzz-tag">Deduplication</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Using CTE:<br>
  <code>WITH CTE AS (SELECT id, ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) as rn FROM Users) DELETE FROM Users WHERE id IN (SELECT id FROM CTE WHERE rn > 1);</code><br>
  This partitions records by email and numbers them. Any row with a row number greater than 1 represents a duplicate and is deleted."</p>
</div>
""",
        "trap": "Believing COUNT(*) is identical to COUNT(col) when checking for duplicates with null values. Nulls can group together or get dropped.",
        "trick": "Always use unique fields (IDs) to anchor your deduplication deletes."
    },
    {
        "id": "sql-34-consecutive",
        "num": "34",
        "chapter": "Interview SQL",
        "title": "Consecutive Numbers",
        "subtitle": "Sequence isolation and row number differences.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>Finding consecutive repeating numbers is an advanced query pattern. The standard interview problem asks to identify numbers that appear at least three times consecutively. This can be resolved using multiple self-joins or `LEAD`/`LAG` window functions.</p>
</div>
<div class="concept-visual">
  <table class="visual-table" style="font-size: 7.5pt;">
    <thead>
      <tr><th>Id</th><th>Num</th><th>Prev (LAG 1)</th><th>Prev2 (LAG 2)</th></tr>
    </thead>
    <tbody>
      <tr><td>1</td><td>10</td><td>NULL</td><td>NULL</td></tr>
      <tr><td>2</td><td>10</td><td>10</td><td>NULL</td></tr>
      <tr><td style="color:#C53030;">3</td><td style="color:#C53030; font-weight:bold;">10</td><td style="color:#C53030; font-weight:bold;">10</td><td style="color:#C53030; font-weight:bold;">10 (Consecutive!)</td></tr>
    </tbody>
  </table>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Write a query to find all numbers that appear at least three times consecutively."</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Consecutive Sequences</span>
    <span class="buzz-tag">LAG Window</span>
    <span class="buzz-tag">Gaps and Islands</span>
    <span class="buzz-tag">Conditional Joins</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Query using LAG:<br>
  <code>WITH SeqCheck AS (SELECT Num, LAG(Num, 1) OVER (ORDER BY id) as prev1, LAG(Num, 2) OVER (ORDER BY id) as prev2 FROM Logs) SELECT DISTINCT Num FROM SeqCheck WHERE Num = prev1 AND Num = prev2;</code><br>
  This fetches the preceding two rows for each row and verifies if they have the same value."</p>
</div>
""",
        "trap": "Assuming sequence IDs are contiguous integers (1, 2, 3) without gaps. Using raw self-joins on `id = id + 1` fails if a record is deleted.",
        "trick": "Always use window functions (LEAD/LAG) or ROW_NUMBER() grouping keys rather than hardcoding ID offsets."
    },
    {
        "id": "sql-35-depthsalary",
        "num": "35",
        "chapter": "Interview SQL",
        "title": "Department Top Earners",
        "subtitle": "Group partitioning and top rank extraction.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>Finding the department's highest salary requires partitioning rows. An inner subquery calculates ranks per department using the `DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC)` window function, and the outer query filters rank 1.</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8pt; line-height: 1.4; background: white; border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 10px;">
    <strong>Partition Windowing:</strong><br>
    • Dept A: Emp 1 ($50k) → Rank 1<br>
    • Dept A: Emp 2 ($45k) → Rank 2<br>
    • Dept B: Emp 3 ($60k) → Rank 1
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Write a query to find employees who have the highest salary in each of their departments."</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">PARTITION BY</span>
    <span class="buzz-tag">DENSE_RANK</span>
    <span class="buzz-tag">Partition Boundary</span>
    <span class="buzz-tag">Filter Subquery</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Query:<br>
  <code>WITH RankedSalary AS (SELECT name, salary, dept_id, DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) as rk FROM Employee) SELECT name, salary, dept_id FROM RankedSalary WHERE rk = 1;</code><br>
  This partitions records by department, ranks salaries descending, and extracts all rows with rank 1 (handling tied top salaries)."</p>
</div>
""",
        "trap": "Using MAX(salary) inside GROUP BY and joining back. This is slow and fails to handle cases where two employees share the top salary.",
        "trick": "Always use PARTITION BY inside DENSE_RANK() to calculate top ranks per group."
    },
    {
        "id": "sql-36-runningtotal",
        "num": "36",
        "chapter": "Interview SQL",
        "title": "Running Total",
        "subtitle": "Cumulative aggregations and window frame clauses.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>Calculating running totals or cumulative sums computes progress over time. In SQL, this is achieved using window aggregation: <code>SUM(val) OVER (ORDER BY date)</code>. Understanding window frame clauses is critical for performance.</p>
</div>
<div class="concept-visual">
  <table class="visual-table" style="font-size: 7.5pt;">
    <thead>
      <tr><th>Date</th><th>Amount</th><th>Running Total</th></tr>
    </thead>
    <tbody>
      <tr><td>Jan 1</td><td>100</td><td>100</td></tr>
      <tr><td>Jan 2</td><td>150</td><td>250 (100+150)</td></tr>
      <tr><td>Jan 3</td><td>200</td><td>450 (250+200)</td></tr>
    </tbody>
  </table>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Explain what the frame clause <code>ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW</code> does and why it is useful."</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Window Frame</span>
    <span class="buzz-tag">Running Total</span>
    <span class="buzz-tag">UNBOUNDED</span>
    <span class="buzz-tag">Cumulative Sum</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"The frame clause defines the boundaries of rows included in the current aggregate. <code>ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW</code> instructs the engine to sum values from the first row of the partition up to the current row, calculating a running total."</p>
</div>
""",
        "trap": "Omitting ORDER BY in running sums. Without ORDER BY, the window aggregate defaults to summing the entire partition at once.",
        "trick": "Always define ORDER BY on your time or ID column to force sequential running total updates."
    },
    {
        "id": "sql-37-topngroup",
        "num": "37",
        "chapter": "Interview SQL",
        "title": "Top N Per Group",
        "subtitle": "Filtering window rankings in subqueries.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>Extracting the top N records per group (e.g. top 3 customers per region) builds upon partitioning. It is resolved by assigning ranks using `ROW_NUMBER()` or `DENSE_RANK()`, and filtering for rank `&le; N` in the outer query block.</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8pt; line-height: 1.4; background: white; border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 10px;">
    <strong>Top 2 Per Group Flow:</strong><br>
    Region A: Cust 1 (Rank 1) → Retained<br>
    Region A: Cust 2 (Rank 2) → Retained<br>
    Region A: Cust 3 (Rank 3) → Discarded
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Write a query to extract the top 3 highest-spending customers for each country."</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Top N Filter</span>
    <span class="buzz-tag">ROW_NUMBER</span>
    <span class="buzz-tag">CTE Selection</span>
    <span class="buzz-tag">Group Rankings</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Query:<br>
  <code>WITH RankedCustomers AS (SELECT customer_id, country, spending, ROW_NUMBER() OVER (PARTITION BY country ORDER BY spending DESC) as rn FROM CustomerSpend) SELECT customer_id, country, spending FROM RankedCustomers WHERE rn <= 3;</code><br>
  This numbers rows per country descending by spending, and returns rows numbered 1, 2, or 3."</p>
</div>
""",
        "trap": "Believing you can filter window values directly (e.g., WHERE ROW_NUMBER() <= 3). You must wrap it in a CTE or subquery.",
        "trick": "Use ROW_NUMBER() to guarantee exactly N records; use DENSE_RANK() to include all ties."
    },
    {
        "id": "sql-38-retention",
        "num": "38",
        "chapter": "Interview SQL",
        "title": "Customer Retention",
        "subtitle": "Cohort analysis and active user retention.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>Customer retention measures repeat user logins. A standard query tracks Month-over-Month (MoM) active user retention. This is solved by self-joining user activity logs on user identifiers with matching month offsets.</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8.5pt; font-family: monospace; background: white; border: 1px solid #CBD5E0; padding: 6px; border-radius: 6px; text-align: center;">
    Active Users Month 1 (Join on UserID)<br>
    → Active Users Month 2<br>
    • Formula: Retained / Total Month 1 &times; 100
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Write a query to find the percentage of active users in Month 1 who logged in again in Month 2."</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Cohort</span>
    <span class="buzz-tag">Self-Join</span>
    <span class="buzz-tag">Active User</span>
    <span class="buzz-tag">Monthly Active Users</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Query:<br>
  <code>SELECT COUNT(DISTINCT M2.user_id) * 100.0 / COUNT(DISTINCT M1.user_id) AS retention_rate FROM Logins M1 LEFT JOIN Logins M2 ON M1.user_id = M2.user_id AND M2.month = M1.month + 1 WHERE M1.month = 1;</code><br>
  This left-joins Month 1 logins to Month 2 logins on user ID, calculating the percentage that returned."</p>
</div>
""",
        "trap": "Using INNER JOIN instead of LEFT JOIN. An INNER JOIN drops users who did not return, preventing calculation of the retention rate.",
        "trick": "Always use LEFT JOIN to preserve the initial cohort size in retention queries."
    },
    {
        "id": "sql-39-rankingqueries",
        "num": "39",
        "chapter": "Interview SQL",
        "title": "Ranking Queries",
        "subtitle": "Complex custom ranking constraints and ties.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>Complex ranking problems require sorting data based on secondary conditional columns when ties occur. This is implemented by supplying multiple columns to the window `ORDER BY` clause (e.g. sort by score DESC, then by date ASC).</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8pt; line-height: 1.4; background: white; border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 10px;">
    <strong>Compound Order Priority:</strong><br>
    1. Score DESC (Primary)<br>
    2. Errors ASC (Tie Breaker)<br>
    3. Timestamp ASC (Secondary Tie Breaker)
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Write a query to rank students by score descending. If scores are equal, rank them by exam completion time ascending."</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">DENSE_RANK</span>
    <span class="buzz-tag">Secondary Sort</span>
    <span class="buzz-tag">Tie Breaking</span>
    <span class="buzz-tag">Sort Order</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Query:<br>
  <code>SELECT student_id, score, completion_time, DENSE_RANK() OVER (ORDER BY score DESC, completion_time ASC) as rk FROM ExamResults;</code><br>
  By specifying multiple columns in ORDER BY, ties in score are resolved by completion time before rank assignment."</p>
</div>
""",
        "trap": "Mixing ASC and DESC without explicit keywords. e.g. ORDER BY score, time ASC defaults both to ASC.",
        "trick": "Always write DESC or ASC explicitly after each column in compound sorting lists."
    },
    {
        "id": "sql-40-datequeries",
        "num": "40",
        "chapter": "Interview SQL",
        "title": "Date Queries",
        "subtitle": "DATEDIFF, DATEADD, and date truncation.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>Date metrics require handling temporal functions. The most tested operations are DATEDIFF (calculating days between dates), DATEADD (moving dates forward), and DATE_TRUNC (rounding timestamps to boundaries).</p>
</div>
<div class="concept-visual">
  <div style="font-size: 8.5pt; font-family: monospace; background: white; border: 1px solid #CBD5E0; padding: 6px; border-radius: 6px; text-align: center;">
    <strong>DATE_TRUNC('month', '2026-05-30')</strong><br>
    → Output: '2026-05-01 00:00:00'<br>
    • Useful for group aggregation by month.
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Write a query to count the number of users registered per month, truncating creation timestamps."</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">DATE_TRUNC</span>
    <span class="buzz-tag">Temporal Aggregation</span>
    <span class="buzz-tag">Date Math</span>
    <span class="buzz-tag">Time Period Grouping</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Query:<br>
  <code>SELECT DATE_TRUNC('month', created_at) AS reg_month, COUNT(*) AS count FROM Users GROUP BY reg_month ORDER BY reg_month;</code><br>
  Using <code>DATE_TRUNC</code> collapses all daily timestamps to their respective monthly boundaries for clean grouping."</p>
</div>
""",
        "trap": "Subtracting dates using raw math (date1 - date2). This is non-portable and returns incorrect data depending on timezone settings.",
        "trick": "Always use DATEDIFF or database-specific date difference functions to calculate intervals."
    }
]

# ─────────────────────────────────────────
# ROADMAP PAGE
# ─────────────────────────────────────────
roadmap_page = f"""
  <div class="page roadmap-page" id="sql-roadmap">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="header-badge" style="background: rgba(255,255,255,0.25);">SQL ROADMAP</div>
      </div>
    </div>
    
    <div style="padding: 30px 40px; flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
      <div>
        <div style="font-size: 26pt; font-weight: 800; color: #111; margin-bottom: 8px;">SQL Preparation Roadmap</div>
        <div style="font-size: 11pt; color: #EA763F; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px;">Placement Preparation Guide</div>
        
        <div style="background: #FFF5F0; border-left: 5px solid #EA763F; padding: 14px 20px; border-radius: 6px; margin-bottom: 25px;">
          <strong style="color: #EA763F; font-size: 11pt; display: block; margin-bottom: 6px;">How to use this Handbook:</strong>
          <p style="font-size: 9.5pt; color: #4A5568; line-height: 1.5;">SQL questions are highly standardized in coding interviews. Master the <strong>Logical Execution Order</strong> of queries first. Focus heavily on <strong>Window Functions</strong> (ROW_NUMBER vs DENSE_RANK), **Joins** (handling nulls in outer joins), **Indexing** structures (seek vs scan), and **Transaction Isolation** anomaly models.</p>
        </div>

        <div style="margin-top: 15px;">
          <div style="font-size: 12pt; font-weight: 800; color: #1A202C; margin-bottom: 12px; border-bottom: 2px solid #E2E8F0; padding-bottom: 6px;">🎯 Three-Phase Learning Plan</div>
          
          <div style="display: flex; gap: 15px; margin-bottom: 15px;">
            <div style="background: #EBF8FF; border: 1px solid #BEE3F8; border-radius: 8px; padding: 12px; flex: 1;">
              <span style="background: #3182CE; color: white; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 7.5pt; text-transform: uppercase;">Phase 1</span>
              <strong style="display: block; font-size: 9.5pt; margin-top: 6px; color: #2B6CB0;">Fundamentals &amp; Joins</strong>
              <p style="font-size: 8pt; color: #4A5568; margin-top: 4px;">Learn projection filtering (WHERE vs HAVING), aggregate null behaviors, and physical join mechanics (Nested Loop, Hash, Merge Joins). (Topics 1 - 14)</p>
            </div>
            
            <div style="background: #F0FFF4; border: 1px solid #C6F6D5; border-radius: 8px; padding: 12px; flex: 1;">
              <span style="background: #38A169; color: white; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 7.5pt; text-transform: uppercase;">Phase 2</span>
              <strong style="display: block; font-size: 9.5pt; margin-top: 6px; color: #276749;">Advanced SQL</strong>
              <p style="font-size: 8pt; color: #4A5568; margin-top: 4px;">Study correlated subqueries, recursive CTEs, and window partition frames (LEAD, LAG, DENSE_RANK). (Topics 15 - 23)</p>
            </div>
            
            <div style="background: #FFFFF0; border: 1px solid #FEFCBF; border-radius: 8px; padding: 12px; flex: 1;">
              <span style="background: #D69E2E; color: white; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 7.5pt; text-transform: uppercase;">Phase 3</span>
              <strong style="display: block; font-size: 9.5pt; margin-top: 6px; color: #B7791F;">Indexing, ACID &amp; Practice</strong>
              <p style="font-size: 8pt; color: #4A5568; margin-top: 4px;">Understand B+ Trees, clustered/non-clustered indexes, transaction isolation levels, and solve classic interview queries. (Topics 24 - 40)</p>
            </div>
          </div>
        </div>
      </div>

      <div style="border-top: 1.5px dashed #E2E8F0; padding-top: 15px; display: flex; justify-content: space-between; align-items: center; font-size: 9pt; color: #718096;">
        <div>GrindOS Placement Handbooks</div>
        <div>Page 02 / 55</div>
      </div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# INDEX (TOC) GENERATION
# ─────────────────────────────────────────
toc_cols = []
chunk_size = 14
for c_idx in range(0, len(topics), chunk_size):
    chunk = topics[c_idx:c_idx+chunk_size]
    col_html = '<div style="flex: 1; display: flex; flex-direction: column; gap: 4px;">'
    for t in chunk:
        col_html += f"""
        <div style="display: flex; justify-content: space-between; font-size: 8pt; border-bottom: 1px dotted #EDE5D8; padding-bottom: 2px;">
          <span style="color: #EA763F; font-weight: 800; margin-right: 4px;">{t['num']}</span>
          <span style="flex: 1; font-weight: 700; color: #333;">{t['title']}</span>
          <span style="color: #888; font-family: monospace;">p.{str(int(t['num'])+3).zfill(2)}</span>
        </div>
        """
    col_html += "</div>"
    toc_cols.append(col_html)

# Append extra reference pages
extra_toc_col = f"""
<div style="flex: 1; display: flex; flex-direction: column; gap: 4px;">
  <div style="display: flex; justify-content: space-between; font-size: 8pt; border-bottom: 1px dotted #EDE5D8; padding-bottom: 2px;">
    <span style="color: #EA763F; font-weight: 800; margin-right: 4px;">41</span>
    <span style="flex: 1; font-weight: 700; color: #333;">Cram Sheet</span>
    <span style="color: #888; font-family: monospace;">p.44</span>
  </div>
  <div style="display: flex; justify-content: space-between; font-size: 8pt; border-bottom: 1px dotted #EDE5D8; padding-bottom: 2px;">
    <span style="color: #EA763F; font-weight: 800; margin-right: 4px;">42</span>
    <span style="flex: 1; font-weight: 700; color: #333;">Comparison Table</span>
    <span style="color: #888; font-family: monospace;">p.45</span>
  </div>
  <div style="display: flex; justify-content: space-between; font-size: 8pt; border-bottom: 1px dotted #EDE5D8; padding-bottom: 2px;">
    <span style="color: #EA763F; font-weight: 800; margin-right: 4px;">43</span>
    <span style="flex: 1; font-weight: 700; color: #333;">Expected Q&amp;A (P1)</span>
    <span style="color: #888; font-family: monospace;">p.46</span>
  </div>
  <div style="display: flex; justify-content: space-between; font-size: 8pt; border-bottom: 1px dotted #EDE5D8; padding-bottom: 2px;">
    <span style="color: #EA763F; font-weight: 800; margin-right: 4px;">44</span>
    <span style="flex: 1; font-weight: 700; color: #333;">Expected Q&amp;A (P2)</span>
    <span style="color: #888; font-family: monospace;">p.47</span>
  </div>
  <div style="display: flex; justify-content: space-between; font-size: 8pt; border-bottom: 1px dotted #EDE5D8; padding-bottom: 2px;">
    <span style="color: #EA763F; font-weight: 800; margin-right: 4px;">45</span>
    <span style="flex: 1; font-weight: 700; color: #333;">Expected Q&amp;A (P3)</span>
    <span style="color: #888; font-family: monospace;">p.48</span>
  </div>
  <div style="display: flex; justify-content: space-between; font-size: 8pt; border-bottom: 1px dotted #EDE5D8; padding-bottom: 2px;">
    <span style="color: #EA763F; font-weight: 800; margin-right: 4px;">46</span>
    <span style="flex: 1; font-weight: 700; color: #333;">Expected Q&amp;A (P4)</span>
    <span style="color: #888; font-family: monospace;">p.49</span>
  </div>
  <div style="display: flex; justify-content: space-between; font-size: 8pt; border-bottom: 1px dotted #EDE5D8; padding-bottom: 2px;">
    <span style="color: #EA763F; font-weight: 800; margin-right: 4px;">47</span>
    <span style="flex: 1; font-weight: 700; color: #333;">Expected Q&amp;A (P5)</span>
    <span style="color: #888; font-family: monospace;">p.50</span>
  </div>
  <div style="display: flex; justify-content: space-between; font-size: 8pt; border-bottom: 1px dotted #EDE5D8; padding-bottom: 2px;">
    <span style="color: #EA763F; font-weight: 800; margin-right: 4px;">48</span>
    <span style="flex: 1; font-weight: 700; color: #333;">Rapid Fire (P1)</span>
    <span style="color: #888; font-family: monospace;">p.51</span>
  </div>
  <div style="display: flex; justify-content: space-between; font-size: 8pt; border-bottom: 1px dotted #EDE5D8; padding-bottom: 2px;">
    <span style="color: #EA763F; font-weight: 800; margin-right: 4px;">49</span>
    <span style="flex: 1; font-weight: 700; color: #333;">Rapid Fire (P2)</span>
    <span style="color: #888; font-family: monospace;">p.52</span>
  </div>
  <div style="display: flex; justify-content: space-between; font-size: 8pt; border-bottom: 1px dotted #EDE5D8; padding-bottom: 2px;">
    <span style="color: #EA763F; font-weight: 800; margin-right: 4px;">50</span>
    <span style="flex: 1; font-weight: 700; color: #333;">Interview Traps (P1)</span>
    <span style="color: #888; font-family: monospace;">p.53</span>
  </div>
  <div style="display: flex; justify-content: space-between; font-size: 8pt; border-bottom: 1px dotted #EDE5D8; padding-bottom: 2px;">
    <span style="color: #EA763F; font-weight: 800; margin-right: 4px;">51</span>
    <span style="flex: 1; font-weight: 700; color: #333;">Interview Traps (P2)</span>
    <span style="color: #888; font-family: monospace;">p.54</span>
  </div>
  <div style="display: flex; justify-content: space-between; font-size: 8pt; border-bottom: 1px dotted #EDE5D8; padding-bottom: 2px;">
    <span style="color: #EA763F; font-weight: 800; margin-right: 4px;">52</span>
    <span style="flex: 1; font-weight: 700; color: #333;">Notes Pages</span>
    <span style="color: #888; font-family: monospace;">p.55</span>
  </div>
</div>
"""
toc_cols.append(extra_toc_col)

toc_rows = f"""
<div style="display: flex; gap: 24px; margin-top: 15px;">
  {toc_cols[0]}
  {toc_cols[1]}
  {toc_cols[2]}
</div>
"""

toc_page = f"""
  <div class="page toc-page" id="sql-toc">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="header-badge" style="background: rgba(255,255,255,0.25);">INDEX</div>
      </div>
    </div>
    
    <div class="toc-inner" style="padding: 24px 40px; flex:1; display:flex; flex-direction:column; justify-content:space-between;">
      <div>
        <div style="font-size: 24pt; font-weight: 800; color: #111; border-bottom: 4px solid #EA763F; display: inline-block; padding-bottom: 6px; margin-bottom: 8px; letter-spacing: -0.5px;">Table of Contents</div>
        <div style="font-size: 9pt; color: #A0AEC0; font-weight: 600; margin-bottom: 12px;">SQL Fundamentals &amp; Advanced Systems · Placement Preparation Handbook</div>
        {toc_rows}
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> SQL <span>›</span> <span>Index</span></div>
      </div>
      <div class="page-number-premium">PAGE 03 / 55</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# HELPER FUNCTIONS (Industry & Depth & Space)
# ─────────────────────────────────────────
def get_sql_industry_box(tid):
    industry_usage = {
        "sql-01-select": "Data warehouse layers (e.g. Snowflake, BigQuery) charge queries by volume of scanned bytes; selecting explicit columns is critical to contain cloud bills.",
        "sql-02-where": "Payment backends index checking transaction states. SARGable range indexes filter active transactions in microseconds during checkout operations.",
        "sql-03-orderby": "E-commerce product grids sorted by price rely on indexed fields to retrieve items instantly, bypassing memory sorting limits.",
        "sql-04-distinct": "User analytics aggregates identify unique customer IDs accessing platform APIs monthly to calculate billing cohorts.",
        "sql-05-limit": "Mobile app dashboards leverage keyset seeking (cursor paging) to fetch activity updates, skipping slow offsets under high traffic.",
        "sql-06-groupby": "Reporting engines group server telemetry data by hour and region to visualize operational trends on Grafana dashboards.",
        "sql-07-having": "SaaS analytics modules filter user groups that averaged more than 50 API errors daily to alert developer integration teams.",
        "sql-08-aggregates": "Risk valuation modules average portfolio returns, utilizing COALESCE checks to map missing stock entries to default values.",
        "sql-09-innerjoin": "Order processing modules query orders joined with client emails to dispatch tracking status emails during warehouse releases.",
        "sql-10-leftjoin": "Marketing directories audit active users, executing LEFT JOINs to isolate accounts that have never completed a registration checkout.",
        "sql-11-rightjoin": "Data ingestion pipes utilize equivalent LEFT JOIN rewrites to verify raw supplier records match corporate database formats.",
        "sql-12-fulljoin": "Inventory audits combine store stock lists with online catalog systems, identifying discrepancies on both physical and digital sides.",
        "sql-13-selfjoin": "Identity management databases join employees with managers to map supervisor chains inside unified LDAP directories.",
        "sql-14-crossjoin": "Testing utilities execute CROSS JOINs to pair every test category with every browser environment to build verification grids.",
        "sql-15-subqueries": "Content portals filter active publications, pulling only articles whose category matches current dashboard layout arrays.",
        "sql-16-correlated": "Audit systems check for suspicious ledger updates. Optimizers attempt to rewrite these to Joins to prevent looping query delays.",
        "sql-17-cte": "Financial reporting queries divide multi-table ledger parsing stages into modular CTE blocks to keep query code readable and audit-safe.",
        "sql-18-window": "Stock tracking dashboards execute window functions over partitions to compare current pricing ticks with historical daily records.",
        "sql-19-rownumber": "Message streaming logs use ROW_NUMBER() grouping by ID to isolate and delete duplicate message instances from queue tables.",
        "sql-20-rank": "University grading systems assign percentile rankings to scores, leaving sequence gaps where students share tied results.",
        "sql-21-denserank": "Global gaming leaderboards calculate continuous player ranks. If scores tie, subsequent ranks increment by exactly one.",
        "sql-22-lead": "Industrial IoT sensors compare consecutive temperature telemetry points, checking forward rows to flag sudden sensor overheating.",
        "sql-23-lag": "SaaS subscription logs compute month-over-month recurring revenue deltas by comparing current logs with preceding month values.",
        "sql-24-indexing": "Relational storage backends write indexes to disk structures to query keys in microseconds instead of scanning tables.",
        "sql-25-clustered": "Relational databases physically sort tables by their primary key, resolving record lookups at the root index nodes.",
        "sql-26-nonclustered": "High-throughput catalogs map secondary indexes (like product SKU) back to primary key records to query items fast.",
        "sql-27-optimization": "DBAs inspect slow query logs, rewriting wildcard filters to ensure execution plans use indexed ranges.",
        "sql-28-execplan": "Performance engineers review EXPLAIN output operators to identify hash join bottlenecks on non-indexed columns.",
        "sql-29-acid": "Banking ledgers write deposits to disk log buffers before modifying schemas, guaranteeing transactions survive host crashes.",
        "sql-30-transactions": "Flight reservation engines set transaction isolation levels to prevent double-booking seats during concurrent checkout requests.",
        "sql-31-locks": "Inventory catalogs execute write locks on stock keys during flash sales to prevent purchasing items that have sold out.",
        "sql-32-nthsalary": "HR compliance platforms calculate gender-pay metrics, querying salary values at specific partition index points.",
        "sql-33-duplicates": "CRM platforms clean contact lists, running row-number deduplication scripts to delete duplicate profile registrations.",
        "sql-34-consecutive": "Security systems analyze user logs, querying for accounts with three consecutive failed login attempts to trigger security lockouts.",
        "sql-35-depthsalary": "Payroll dashboards calculate department top earners, reporting employees who receive the maximum salary in each team.",
        "sql-36-runningtotal": "SaaS sales dashboards track running totals to display year-to-date cumulative revenue figures over monthly intervals.",
        "sql-37-topngroup": "E-commerce frontends display the top 3 highest-rated products in each product category using window partition rankings.",
        "sql-38-retention": "Growth metrics systems calculate user retention percentages by tracking user login cohorts month-over-month.",
        "sql-39-rankingqueries": "Trading engines rank transactions by amount descending and time ascending to resolve order execution sequence.",
        "sql-40-datequeries": "Compliance systems query user creation dates, truncating timestamps to aggregate logs by month for tax audits."
    }
    desc = industry_usage.get(tid, "Relational database platforms use query engines and indexing layers to serve high-throughput client queries at scale.")
    return f"""
<div class="box box-industry" style="padding: 10px; margin-bottom: 0; border: 1px solid #F5E6B3; background: #FDF6E3;">
  <div class="box-title" style="font-size: 8pt; color: #B7791F; margin-bottom: 4px;">🏭 Where Used in Industry</div>
  <p style="font-size: 7.5pt; line-height: 1.35; color: #5C5438; margin: 0;">{desc}</p>
</div>
"""

def get_sql_depth_box(tid):
    depth_levels = {
        "sql-01-select": [
            "Logical projection vs physical page scanning steps.",
            "Covering indexes and column pruning optimization.",
            "Impact of SELECT * on network payload and packet latency.",
            "Metadata catalog lock contention during query parsing.",
            "Memory buffer allocation adjustments based on row width."
        ],
        "sql-02-where": [
            "Selection operations on relational tables.",
            "SARGable predicates and index scan/seek selections.",
            "Implicit type conversions and indexing degradation.",
            "Logical operator precedence (AND before OR evaluation).",
            "Index range scan operations on compound indexes."
        ],
        "sql-03-orderby": [
            "Implicit sorting behaviors on relational schemas.",
            "Index-based sorting vs filesort (Sort Buffers).",
            "Quicksort algorithms in memory vs external merge sorts.",
            "Sort buffer size configuration and temp file degradation.",
            "Ordering NULL values: NULLS FIRST vs NULLS LAST."
        ],
        "sql-04-distinct": [
            "Deduplication basics and unique row values.",
            "Deduplication mechanisms: Sort vs Hash Aggregates.",
            "DISTINCT vs GROUP BY compiler translation structures.",
            "Distinct scans using index prefix trees.",
            "Memory footprint of distinct checks on huge datasets."
        ],
        "sql-05-limit": [
            "Limiting row outputs and page offset queries.",
            "Offset scan-and-discard overheads on high pages.",
            "Keyset pagination seeking (Direct Index Seek).",
            "Non-deterministic LIMIT queries without ORDER BY.",
            "Optimizer early termination paths during limit matching."
        ],
        "sql-06-groupby": [
            "Collapsing duplicate columns into group keys.",
            "Hash Aggregation vs Sort Aggregation physical paths.",
            "Single-column vs multi-column grouping structures.",
            "Indeterminacy and the functional dependency validation.",
            "Buffer pool optimizations during heavy grouping operations."
        ],
        "sql-07-having": [
            "Filtering aggregated group outcomes.",
            "WHERE execution order vs HAVING execution order.",
            "Delaying evaluations: Non-aggregate filters in HAVING.",
            "Optimizer push-down of HAVING filters to WHERE.",
            "Complex aggregates inside HAVING condition expressions."
        ],
        "sql-08-aggregates": [
            "SUM, AVG, COUNT, MIN, MAX definitions.",
            "COUNT(*) row count vs COUNT(col) value count.",
            "Aggregate behaviors with NULL (Zero vs Null exclusion).",
            "Using COALESCE to force default numerical aggregates.",
            "Custom aggregate functions using procedural database scripts."
        ],
        "sql-09-innerjoin": [
            "Mathematical intersection of two relation schemas.",
            "Physical join algorithms: Nested Loop vs Hash vs Merge.",
            "Build vs Probe phases in Hash Join execution.",
            "Logical join reordering by cost optimizers.",
            "Hash table bucket collisions during join calculations."
        ],
        "sql-10-leftjoin": [
            "Preserving left-side relations with null extensions.",
            "Anti-Join pattern implementations to find missing links.",
            "Placing filters: ON clause vs WHERE clause.",
            "Implicit conversion of LEFT JOIN to INNER JOIN.",
            "Optimizing left joins over partitioned partition keys."
        ],
        "sql-11-rightjoin": [
            "Preserving right-side relations with null extensions.",
            "Logical equivalence of RIGHT JOIN to LEFT JOIN.",
            "Query parser rewrite of right joins to left joins.",
            "Readability constraints in complex query joins.",
            "Compiler parsing trees for multi-table outer joins."
        ],
        "sql-12-fulljoin": [
            "Union joins and complete null padding structures.",
            "Emulating full joins using LEFT/RIGHT JOIN and UNION.",
            "Performance difference: UNION vs UNION ALL emulation.",
            "Full join hash execution plans and memory allocation.",
            "Distributed full join operations in clustered databases."
        ],
        "sql-13-selfjoin": [
            "Joining a table schema to its own records.",
            "Namespace separation using clear table aliases.",
            "Hierarchical mappings (Parent-Child relationships).",
            "Performance overhead of scanning the same table twice.",
            "Converting self-joins to window functions or CTE paths."
        ],
        "sql-14-crossjoin": [
            "Cartesian product computations and grid arrays.",
            "Accidental cross joins due to missing ON conditions.",
            "Permutation generation logic for combinatorics.",
            "Memory footprint of massive Cartesian result sets.",
            "Optimizer short-circuit checks for empty table pairs."
        ],
        "sql-15-subqueries": [
            "Scalar, row, and table nested query paths.",
            "IN vs EXISTS query processing and optimizations.",
            "Derived tables and inline query parser definitions.",
            "Scope visibility rules in nested SELECT statements.",
            "Optimizer flattening of basic nested subqueries."
        ],
        "sql-16-correlated": [
            "Outer table references within nested queries.",
            "Row-by-row correlation loops (O(N&times;M) complexity).",
            "Optimizer decorrelation paths and join conversions.",
            "EXISTS short-circuiting mechanics (first match escape).",
            "Comparing correlated subqueries vs partitioned window views."
        ],
        "sql-17-cte": [
            "Temporary result sets using WITH statements.",
            "CTE optimization: Inline view optimization vs Materialization.",
            "Recursive CTEs (Anchor vs Recursive union steps).",
            "Traversal limits (MAXRECURSION configurations).",
            "CTE scoping limits in complex transaction blocks."
        ],
        "sql-18-window": [
            "Window functions and the OVER clause mechanics.",
            "PARTITION BY vs GROUP BY (preserve vs collapse rows).",
            "Window frame clauses (ROWS vs RANGE specifications).",
            "Sorting cost overheads inside window execution plans.",
            "Index utilization in partition-ranking queries."
        ],
        "sql-19-rownumber": [
            "Sequential row numbering inside group partitions.",
            "Non-deterministic tie handling in ROW_NUMBER().",
            "Creating deterministic sequences with secondary sort keys.",
            "Duplicate record isolation using ROW_NUMBER() filters.",
            "Performance difference: ROW_NUMBER() vs RANK() execution."
        ],
        "sql-20-rank": [
            "Ranking values within partition boundaries.",
            "Ties handling: identical ranks and sequence gaps.",
            "Ranking calculation: 1 + preceding higher rows.",
            "Index scan paths during multi-row ranking.",
            "Using RANK() to identify top-tier entities."
        ],
        "sql-21-denserank": [
            "Contiguous ranking inside partition boundaries.",
            "DENSE_RANK() vs RANK() gap comparison.",
            "Handling duplicates without skipping ranking steps.",
            "DENSE_RANK() OVER (PARTITION BY ... ORDER BY ...) syntax.",
            "Memory allocation during dense ranking of values."
        ],
        "sql-22-lead": [
            "Accessing subsequent records without self-joins.",
            "Passable arguments (offset and default fallbacks).",
            "Null prevention on partition boundary limits.",
            "Execution tree for forward row offset reads.",
            "Lead lookups over time-series logs."
        ],
        "sql-23-lag": [
            "Accessing preceding records without self-joins.",
            "Lag offset steps and boundary default constants.",
            "Calculating percentages and deltas over intervals.",
            "Time-series lag seek operations on sorted indexes.",
            "Comparing lag utility vs self-join complexity."
        ],
        "sql-24-indexing": [
            "Disk storage paths and lookup optimization.",
            "B+ Tree node traversal mechanics (O(log N) seeking).",
            "Index scans vs index seeks in execution plans.",
            "Write degradation: indexing overhead during writes.",
            "Updating index statistics to keep plans cost-accurate."
        ],
        "sql-25-clustered": [
            "Physical disk page sorting by index key.",
            "Leaf node contents: Actual data pages (Clustered).",
            "Single clustered index limit per database relation.",
            "Auto-increment PK design vs UUID index fragmentation.",
            "Page split events during non-sequential index insertions."
        ],
        "sql-26-nonclustered": [
            "Logical index structures separated from data.",
            "Leaf node contents: Key values and data pointers.",
            "Key Lookup (or RID Lookup) overheads in queries.",
            "Covering indexes: using INCLUDE to avoid lookups.",
            "Updating pointer tables during clustered index page splits."
        ],
        "sql-27-optimization": [
            "Identifying query execution path bottlenecks.",
            "Non-SARGable wildcard prefixes (LIKE '%value').",
            "Rewrite paths: OR statements to UNION ALL splits.",
            "Implicit conversions: string comparing to integers.",
            "Optimizer cost modeling under outdated statistics."
        ],
        "sql-28-execplan": [
            "Extracting execution roadmaps using EXPLAIN.",
            "Cost estimations based on CPU and disk page access.",
            "Estimated vs Actual rows (EXPLAIN ANALYZE comparison).",
            "Logical parser, compiler, and physical execution engine.",
            "Graph analysis of physical database operations."
        ],
        "sql-29-acid": [
            "ACID guarantees for transactional stability.",
            "Write-Ahead Logging (WAL) for durability execution.",
            "Undo/Redo segments and logging page checkpoints.",
            "Consistency checks using DB constraints vs app logic.",
            "Doublewrite buffer safety to prevent page splits."
        ],
        "sql-30-transactions": [
            "Atomic execution blocks: BEGIN, COMMIT, ROLLBACK.",
            "Dirty Reads, Non-Repeatable Reads, and Phantom Reads.",
            "Database Isolation Levels and concurrency anomalies.",
            "Multi-Version Concurrency Control (MVCC) snapshot reads.",
            "Range locks and gap locking to prevent phantom rows."
        ],
        "sql-31-locks": [
            "Shared (S) locks vs Exclusive (X) locks.",
            "Deadlock cycles and dependency graph resolution.",
            "Lock escalation (Row -> Page -> Table lock swaps).",
            "Two-Phase Locking (2PL) protocols and serializability.",
            "Shared vs Exclusive lock collision resolution."
        ],
        "sql-32-nthsalary": [
            "Subqueries to locate top N salary metrics.",
            "DENSE_RANK() OVER (ORDER BY salary DESC) queries.",
            "Rank tie differences (RANK vs DENSE_RANK gaps).",
            "Correlated subquery complexity (O(N^2) evaluation).",
            "Index-based seeks on ordered salary fields."
        ],
        "sql-33-duplicates": [
            "Finding duplicates with GROUP BY and HAVING COUNT.",
            "ROW_NUMBER() window partitioning for record isolation.",
            "Bulk deletion of duplicate rows keeping minimum ID.",
            "Unique indexes to prevent duplicate insert attempts.",
            "Locking concerns during bulk duplicate cleaning operations."
        ],
        "sql-34-consecutive": [
            "Identifying repeating values over sequences.",
            "LEAD() and LAG() offset comparisons (offset 1 and 2).",
            "Row number difference techniques (Gaps and Islands).",
            "Handling gaps in ID columns during self-joins.",
            "Optimizing sequential range scans on logs."
        ],
        "sql-35-depthsalary": [
            "Group partitioning window calculations.",
            "DENSE_RANK() PARTITION BY department ORDER BY salary.",
            "Handling duplicate maximum value occurrences.",
            "Index strategies for partition sorting.",
            "CTE vs nested subquery performance paths."
        ],
        "sql-36-runningtotal": [
            "Running aggregates over sorting indexes.",
            "Window frame clauses: ROWS BETWEEN UNBOUNDED and CURRENT.",
            "O(N) execution plans using aggregate window buffers.",
            "Omitting ORDER BY: partition-level summary defaults.",
            "Range-based vs Row-based window frame evaluations."
        ],
        "sql-37-topngroup": [
            "Partition rankings and top list extractions.",
            "ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...) logic.",
            "Filtering window values inside outer query wrappers.",
            "DENSE_RANK tie resolution in group limits.",
            "Performance analysis of partition seeks."
        ],
        "sql-38-retention": [
            "Cohort metrics and active user mappings.",
            "Self-joins on user IDs with matching month offsets.",
            "LEFT JOIN preservation to compute retention percentages.",
            "Cohort boundaries and active client classifications.",
            "Optimizing massive user login self-joins."
        ],
        "sql-39-rankingqueries": [
            "Sorting data with multiple tie-breaking criteria.",
            "Compound ORDER BY lists inside OVER() partition blocks.",
            "Ascending vs Descending order priority limits.",
            "Deterministic rank values using unique identifiers.",
            "Index sorting paths for compound ordering keys."
        ],
        "sql-40-datequeries": [
            "Temporal data manipulation and parsing paths.",
            "DATEDIFF, DATEADD, and DATE_TRUNC operations.",
            "Collapsing timestamps to monthly intervals for grouping.",
            "Timezone offsets and date math complications.",
            "Range queries on index date columns."
        ]
    }
    levels = depth_levels.get(tid, [
        "Core syntax and basic database logic.",
        "SQL Query structures, filters, and standard aggregate mappings.",
        "Window calculations, index seeks, and execution plan parsing.",
        "Transaction isolation levels, locks, and B+ Tree structures.",
        "Distributed database consistency and horizontal sharding coordinates."
    ])
    return f"""
<div class="box box-depth" style="padding: 10px; margin-bottom: 0; border-left-color: #3182CE; background: #EBF8FF;">
  <div class="box-title" style="font-size: 8pt; color: #3182CE; margin-bottom: 4px;">📊 Interview Depth</div>
  <div style="font-size: 7.2pt; line-height: 1.35; color: #2D3748;">
    <strong>L1:</strong> {levels[0]}<br>
    <strong>L2:</strong> {levels[1]}<br>
    <strong>L3:</strong> {levels[2]}<br>
    <strong>L4:</strong> {levels[3]}<br>
    <strong>L5:</strong> {levels[4]}
  </div>
</div>
"""

def get_sql_space_filler(tid):
    fillers = {
        "sql-01-select": """
<div class="box box-say">
  <div class="box-title">💬 How to Explain in Interview</div>
  <p><strong>"Always projection first:</strong> Using <code>SELECT *</code> pulls all fields from the page tables. In production systems, we use explicit column selection to minimize database disk page loads and cache pollution, allowing covering index scans."</p>
</div>
""",
        "sql-02-where": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "Why did my index seek break when I filtered with <code>WHERE SUBSTRING(phone, 1, 3) = '+1'</code>?"<br>
    <strong>Candidate:</strong> "Because wrapping <code>phone</code> in a function makes it non-SARGable. The database must scan every record's phone number to calculate the substring. Use <code>WHERE phone LIKE '+1%'</code> instead."
  </div>
</div>
""",
        "sql-03-orderby": """
<div class="box box-say">
  <div class="box-title">💬 How to Explain in Interview</div>
  <p><strong>"Sorting isn't free:</strong> Relational tables are unordered. Sorting uses temporary disk files (filesort) if the sort buffer runs out of space. Creating an index on the sorting column lets the database read records in order at O(1) sort cost."</p>
</div>
""",
        "sql-04-distinct": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "Is <code>DISTINCT</code> always slow?"<br>
    <strong>Candidate:</strong> "No. If columns are indexed, the database uses a fast Index Scan. If not, it uses a Hash Aggregate in memory. It only slows down when memory limits force a Sort Merge to disk."
  </div>
</div>
""",
        "sql-05-limit": """
<div class="box box-say">
  <div class="box-title">💬 How to Explain in Interview</div>
  <p><strong>"Cursor Paging:</strong> Instead of <code>LIMIT 10 OFFSET 10000</code>, filter with <code>WHERE id > last_seen_id LIMIT 10</code>. This avoids scanning and discarding the first 10,000 records, executing in microseconds."</p>
</div>
""",
        "sql-06-groupby": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "Why did this fail: <code>SELECT department, AVG(salary) FROM emp GROUP BY office</code>?"<br>
    <strong>Candidate:</strong> "Because <code>department</code> is not in the <code>GROUP BY</code>. Multiple department values exist inside each office group; the database cannot collapse them without an aggregate function."
  </div>
</div>
""",
        "sql-07-having": """
<div class="box box-say">
  <div class="box-title">💬 How to Explain in Interview</div>
  <p><strong>"Filter Early:</strong> Never filter raw row conditions in <code>HAVING</code>. Write row filters in <code>WHERE</code> first to reduce the rows that must be aggregated, saving CPU and sort buffers."</p>
</div>
""",
        "sql-08-aggregates": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "What is the average of [10, NULL, 20]?"<br>
    <strong>Candidate:</strong> "In SQL, <code>AVG()</code> ignores NULL, yielding 15 (30/2). To count NULL as 0, write <code>AVG(COALESCE(col, 0))</code>, which yields 10 (30/3)."
  </div>
</div>
""",
        "sql-09-innerjoin": """
<div class="box box-say">
  <div class="box-title">💬 How to Explain in Interview</div>
  <p><strong>"Join Algorithms:</strong> Databases use Hash Joins for large tables, Merge Joins for pre-sorted indexed lists, and Nested Loops for small lookups. The optimizer calculates data volumes to pick the best physical path."</p>
</div>
""",
        "sql-10-leftjoin": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "Why did my <code>LEFT JOIN</code> act as an <code>INNER JOIN</code>?"<br>
    <strong>Candidate:</strong> "You placed a filter on the right table inside the <code>WHERE</code> clause (e.g. <code>WHERE R.status = 'A'</code>). Unmatched rows with NULLs fail this check, filtering them out. Place the filter in the <code>ON</code> clause."
  </div>
</div>
""",
        "sql-11-rightjoin": """
<div class="box box-say">
  <div class="box-title">💬 How to Explain in Interview</div>
  <p><strong>"Left Preference:</strong> Standardize on <code>LEFT JOIN</code> to read queries consistently. Planners automatically swap tables to put the smaller table in the build phase of a Hash Join anyway."</p>
</div>
""",
        "sql-12-fulljoin": """
<div class="box box-scenario">
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Full Join Emulation Syntax:</strong><br>
    <code>SELECT * FROM A LEFT JOIN B ON A.id = B.id</code><br>
    <code>UNION</code><br>
    <code>SELECT * FROM A RIGHT JOIN B ON A.id = B.id;</code>
  </div>
</div>
""",
        "sql-13-selfjoin": """
<div class="box box-say">
  <div class="box-title">💬 How to Explain in Interview</div>
  <p><strong>"Scoping Aliases:</strong> When joining a table to itself, you are creating two logical views in memory. You must assign distinct alias names to each to let the SQL compiler resolve column namespaces."</p>
</div>
""",
        "sql-14-crossjoin": """
<div class="box box-scenario">
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Permutation Matrix Example:</strong><br>
    <code>SELECT Color, Size</code><br>
    <code>FROM Colors CROSS JOIN Sizes;</code><br>
    Returns all possible variations of colors and sizes.
  </div>
</div>
""",
        "sql-15-subqueries": """
<div class="box box-say">
  <div class="box-title">💬 How to Explain in Interview</div>
  <p><strong>"Subquery Scopes:</strong> Scalar subqueries return a single cell value; table subqueries return a list for <code>IN</code> checks. Derived tables in the <code>FROM</code> clause require aliases because they function as virtual tables."</p>
</div>
""",
        "sql-16-correlated": """
<div class="box box-scenario">
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Correlated Subquery Example:</strong><br>
    <code>SELECT * FROM Emp E</code><br>
    <code>WHERE salary > (SELECT AVG(salary)</code><br>
    <code>FROM Emp WHERE dept = E.dept);</code><br>
    Evaluates average salaries per department for each employee.
  </div>
</div>
""",
        "sql-17-cte": """
<div class="box box-say">
  <div class="box-title">💬 How to Explain in Interview</div>
  <p><strong>"CTE Scoping:</strong> CTEs act as logical documentation within complex queries. In recursive CTEs, the recursive step executes until it returns an empty result set (base case exit)."</p>
</div>
""",
        "sql-18-window": """
<div class="box box-scenario">
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Window Aggregation Example:</strong><br>
    <code>SELECT val,</code><br>
    &nbsp;&nbsp;<code>SUM(val) OVER (ORDER BY id) AS running_tot</code><br>
    <code>FROM Ledger;</code><br>
    Preserves row detail lines while computing cumulative summaries.
  </div>
</div>
""",
        "sql-24-indexing": """
<div class="box box-say">
  <div class="box-title">💬 How to Explain in Interview</div>
  <p><strong>"Index Traversals:</strong> B+ Trees store keys in sorted order. Index seeks traverse paths in O(log N) operations. Scans occur when predicates are non-SARGable, requiring sequential scans of leaf nodes."</p>
</div>
""",
        "sql-29-acid": """
<div class="box box-scenario">
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>ACID Commit Checkpoint Flow:</strong><br>
    Transaction SQL → Log Buffer → Flush to WAL Disk Log (Durability) → Table Space Pages Modified.
  </div>
</div>
"""
    }
    fallback = fillers.get(tid, f"""
<div class="box box-say">
  <div class="box-title">💬 How to Explain in Interview</div>
  <p><strong>"Set-Based Logic:</strong> SQL is a declarative language. Explain that you define 'what' data to fetch, leaving the database engine's optimizer to determine the most efficient physical path (joins, seeks, and indexes)."</p>
</div>
""")
    return fallback

# ─────────────────────────────────────────
# PAGE COMPILING LOGIC
# ─────────────────────────────────────────
def generate_page(topic, current_page, total_pages):
    chapter = topic['chapter']
    num = topic['num']
    title = topic['title']
    subtitle = topic['subtitle']
    stars = topic['yield_stars']
    tid = topic['id']
    left_col = topic['left_col']
    right_col = topic['right_col']
    trap = topic['trap']
    trick = topic['trick']
    
    page_indicator = f"PAGE {str(current_page).zfill(2)} / {str(total_pages).zfill(2)}"
    
    # Conditional badge
    header_right_content = """
        <div class="badge-yield">🔥 HIGH YIELD</div>
        <div class="header-badge">Placement Handbook</div>
    """ if "★" in stars and stars.count("★") >= 5 else """
        <div class="header-badge">Core SQL Notes</div>
    """
    
    industry_box = get_sql_industry_box(tid)
    depth_box = get_sql_depth_box(tid)
    space_filler = get_sql_space_filler(tid)
    
    left_col_updated = left_col + "\n" + industry_box + "\n" + depth_box
    
    return f"""
  <div class="page" id="{tid}">
    <!-- Header (L1) -->
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        {header_right_content}
      </div>
    </div>

    <!-- Topic Bar (L2) -->
    <div class="topic-bar">
      <div class="topic-bar-top">
        <div class="topic-eyebrow">{chapter}</div>
        <div class="yield-rating">Yield: <span class="stars-gold">{stars}</span></div>
      </div>
      <div class="topic-title">{num} - {title}</div>
      <div class="topic-subtitle">{subtitle}</div>
    </div>

    <!-- Body Container (L3) -->
    <div class="body-container">
      <!-- Left Column -->
      <div class="col-left">
        {left_col_updated}
      </div>
      
      <!-- Right Column -->
      <div class="col-right">
        {right_col}
        {space_filler}
      </div>
    </div>

    <!-- Bottom Placement Grid (L4) -->
    <div class="bottom-placement-grid">
      <div class="placement-block block-mistake">
        <div class="placement-block-title">⚠️ Common Mistake</div>
        <div>Believing databases store data sequentially by default. Relational data is an unordered bag unless sorted or indexed.</div>
      </div>
      <div class="placement-block block-trap">
        <div class="placement-block-title">🛑 Interviewer Trap</div>
        <div>Claiming SELECT * has the exact same performance as explicit projection. It requires an extra dictionary metadata lookup to expand * to all columns.</div>
      </div>
      <div class="placement-block block-followups">
        <div class="placement-block-title">🔄 Top Follow-Up</div>
        <div>Claiming SELECT * has the exact same performance as explicit projection. It requires an extra dictionary metadata lookup to expand * to all columns.</div>
      </div>
      <div class="placement-block block-trick">
        <div class="placement-block-title">💡 Memory Trick</div>
        <div>Alance sunlinith mar handividth and neaunnt</div>
      </div>
    </div>
    
    <!-- Footer (L5) -->
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> SQL <span>›</span> <span>{title}</span></div>
      </div>
      <div class="page-number-premium">
        {page_indicator}
      </div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# CRAM SHEET PAGE (Page 44)
# ─────────────────────────────────────────
cram_sheet_page = f"""
  <div class="page final-rev-page" id="sql-cram">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="badge-yield" style="background:#FFF5F0; color:#EA763F;">⚡ CRAM SHEET</div>
        <div class="header-badge">SQL Last Minute</div>
      </div>
    </div>
    
    <div style="padding: 24px 30px; display: flex; flex-direction: column; gap: 12px; flex: 1;">
      <div style="text-align: center;">
        <div style="font-size: 20pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">SQL Cram &amp; Execution Guide</div>
        <div style="font-size: 9.5pt; color: #EA763F; font-weight: 700; margin-top: 4px;">Logical Processing Steps &amp; Transaction Anomalies</div>
      </div>
      
      <div style="display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 12px;">
        <div style="border: 1px solid #CBD5E0; border-radius: 8px; padding: 12px; background: white;">
          <strong style="color: #EA763F; font-size: 9pt; display: block; margin-bottom: 6px; border-bottom: 1.5px solid #EA763F; padding-bottom: 2px;">⚙️ LOGICAL QUERY PROCESSING ORDER</strong>
          <ol style="font-size: 8pt; line-height: 1.45; color: #333; padding-left: 15px;">
            <li><strong>FROM:</strong> Identifies source tables and builds Cartesian product grid.</li>
            <li><strong>ON:</strong> Filters join rows based on join conditional keys.</li>
            <li><strong>JOIN:</strong> Joins target relations (INNER, LEFT, RIGHT).</li>
            <li><strong>WHERE:</strong> Filters individual row records (pre-aggregation).</li>
            <li><strong>GROUP BY:</strong> Groups rows by specified unique columns.</li>
            <li><strong>HAVING:</strong> Filters aggregated group results (post-aggregation).</li>
            <li><strong>SELECT:</strong> Projects column selections and window calculations.</li>
            <li><strong>DISTINCT:</strong> Deduplicates identical rows.</li>
            <li><strong>ORDER BY:</strong> Sorts rows logically (filesort vs index scan).</li>
            <li><strong>LIMIT / OFFSET:</strong> Constrains output row limits.</li>
          </ol>
        </div>
        
        <div style="border: 1px solid #CBD5E0; border-radius: 8px; padding: 12px; background: white;">
          <strong style="color: #2B6CB0; font-size: 9pt; display: block; margin-bottom: 6px; border-bottom: 1.5px solid #2B6CB0; padding-bottom: 2px;">⚡ ACID CONCURRENCY</strong>
          <table style="width: 100%; font-size: 7.5pt; border-collapse: collapse; line-height:1.4;">
            <tr style="border-bottom:1px solid #EEE;"><td style="font-weight:bold;">Dirty Read</td><td>Read uncommitted transactions.</td></tr>
            <tr style="border-bottom:1px solid #EEE;"><td style="font-weight:bold;">Non-Rep</td><td>Values modify mid-transaction.</td></tr>
            <tr style="border-bottom:1px solid #EEE;"><td style="font-weight:bold;">Phantom</td><td>Rows inserted in selected ranges.</td></tr>
            <tr style="border-bottom:1px solid #EEE;"><td style="font-weight:bold;">S-Lock</td><td>Shared read locks (compatible).</td></tr>
            <tr style="border-bottom:1px solid #EEE;"><td style="font-weight:bold;">X-Lock</td><td>Exclusive write locks (blocking).</td></tr>
          </table>
        </div>
      </div>
      
      <div style="border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px; background: #FEF8F4;">
        <strong style="color: #276749; font-size: 9.5pt; display: block; margin-bottom: 4px;">💡 SARGABLE PREDICATE OPTIMIZATIONS</strong>
        <div style="font-size: 8pt; color: #2D3748; line-height: 1.45;">
          • <strong>Non-SARGable:</strong> <code>WHERE DATE_ADD(created, INTERVAL 7 DAY) > NOW()</code> (Forces table scan)<br>
          • <strong>SARGable Rewrite:</strong> <code>WHERE created > DATE_SUB(NOW(), INTERVAL 7 DAY)</code> (Leverages index seek)<br>
          • <strong>Wildcard Scan:</strong> <code>WHERE name LIKE '%xyz%'</code> (Index Scan)<br>
          • <strong>Prefix Seek:</strong> <code>WHERE name LIKE 'xyz%'</code> (Index Range Seek)
        </div>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> SQL <span>›</span> <span>Cram Sheet</span></div>
      </div>
      <div class="page-number-premium">PAGE 44 / 55</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# COMPARISON SHEET PAGE (Page 45)
# ─────────────────────────────────────────
comparison_sheet_page = f"""
  <div class="page" id="sql-comparison">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="badge-yield" style="background:#EBF8FF; color:#3182CE;">📊 COMPARISON</div>
        <div class="header-badge">SQL Cheat Sheet</div>
      </div>
    </div>
    
    <div style="padding: 24px 30px; display: flex; flex-direction: column; gap: 14px; flex: 1;">
      <div style="text-align: center;">
        <div style="font-size: 20pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">Most Asked SQL Comparisons</div>
        <div style="font-size: 9.5pt; color: #3182CE; font-weight: 700; margin-top: 4px;">Key Architectural Differences Summarized for Placement Interviews</div>
      </div>
      
      <div style="display: flex; flex-direction: column; gap: 10px;">
        <table class="visual-table contrast-table" style="font-size: 7.5pt; border: 1px solid #E2E8F0; width:100%;">
          <thead>
            <tr style="background:#EDF2F7;">
              <th style="padding:6px;">Topic</th>
              <th style="padding:6px;">Option A</th>
              <th style="padding:6px;">Option B</th>
              <th style="padding:6px;">Key Difference</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Filter</strong></td>
              <td><strong>WHERE:</strong> Filters rows prior to grouping.</td>
              <td><strong>HAVING:</strong> Filters aggregated groups.</td>
              <td>WHERE cannot filter aggregate functions (e.g. SUM); HAVING operates post-aggregation.</td>
            </tr>
            <tr>
              <td><strong>Deduplicate</strong></td>
              <td><strong>DISTINCT:</strong> Evaluates row values for deduplication.</td>
              <td><strong>GROUP BY:</strong> Groups rows by unique key sets.</td>
              <td>DISTINCT is for data projection uniqueness; GROUP BY splits rows for aggregate operations.</td>
            </tr>
            <tr>
              <td><strong>Index</strong></td>
              <td><strong>Clustered Index:</strong> Data physically sorted on disk.</td>
              <td><strong>Non-Clustered:</strong> Separated logical lookup pointers.</td>
              <td>One clustered index per table (keys contain actual data); multiple non-clustered allowed.</td>
            </tr>
            <tr>
              <td><strong>Remove</strong></td>
              <td><strong>DELETE:</strong> DML, filters rows, writes WAL logs.</td>
              <td><strong>TRUNCATE:</strong> DDL, drops and reallocates pages.</td>
              <td>DELETE supports WHERE and triggers; TRUNCATE is faster and releases data pages directly.</td>
            </tr>
            <tr>
              <td><strong>Rank</strong></td>
              <td><strong>RANK():</strong> Assigns identical rank with gaps.</td>
              <td><strong>DENSE_RANK():</strong> Continuous ranking values.</td>
              <td>RANK() skips ranking steps on ties (1, 1, 3); DENSE_RANK() leaves no gaps (1, 1, 2).</td>
            </tr>
            <tr>
              <td><strong>Subquery</strong></td>
              <td><strong>Subquery:</strong> Executed once independently.</td>
              <td><strong>Correlated:</strong> References outer query columns.</td>
              <td>Subqueries evaluate once; correlated subqueries loop row-by-row for the outer set.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> SQL <span>›</span> <span>Comparisons</span></div>
      </div>
      <div class="page-number-premium">PAGE 45 / 55</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# EXPECTED Q&A PAGES (Pages 46 - 50, 10 Questions)
# ─────────────────────────────────────────
def generate_expected_qa_pages(LOGO_BASE64):
    qas = [
        {
            "q": "Q1: Explain the functional differences between DELETE, TRUNCATE, and DROP commands in SQL.",
            "a": "DELETE is a Data Manipulation Language (DML) command that deletes specific rows using a WHERE clause. It writes individual row deletes to the Write-Ahead Log (WAL), triggers database triggers, and retains index space. TRUNCATE is a Data Definition Language (DDL) command that drops the table pages and reallocates storage pages directly. It writes minimal page-deallocation steps to the logs, bypasses delete triggers, and resets auto-increment primary keys. DROP is also a DDL command that removes the entire table structure, indexes, permissions, and definition from the database catalog entirely.",
            "kw": ["DML vs DDL", "Page Reallocation", "Triggers Bypass", "WAL Logging Log"],
            "depth": "DELETE acquires Row-Exclusive locks. TRUNCATE locks the entire table page allocation units (Exclusive schema lock)."
        },
        {
            "q": "Q2: Compare ROW_NUMBER(), RANK(), and DENSE_RANK() window functions. Show their outputs for tied scores [100, 100, 90].",
            "a": "ROW_NUMBER() assigns a unique, sequential row index. For ties, it resolves numbers arbitrarily: [1, 2, 3]. RANK() assigns identical rankings to tied values, but leaves gaps in sequential values: [1, 1, 3] (rank 2 is skipped because 2 rows share rank 1). DENSE_RANK() assigns identical rankings to tied values, but keeps the sequence contiguous: [1, 1, 2]. All three require the OVER() clause specifying ordering columns.",
            "kw": ["Contiguous Rank", "Sequence Gaps", "Arbitrary Sequence", "Tied Scores"],
            "depth": "Explain sorting costs in execution plan sorting steps (Sort operator overhead)."
        },
        {
            "q": "Q3: Write a SQL query to find the Nth highest salary in the Employee table using both CTE and subqueries.",
            "a": "Subquery Method:<br><code>SELECT DISTINCT salary FROM Employee E1 WHERE N-1 = (SELECT COUNT(DISTINCT salary) FROM Employee E2 WHERE E2.salary > E1.salary);</code><br>DENSE_RANK CTE Method:<br><code>WITH RankedSalary AS (SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rk FROM Employee) SELECT salary FROM RankedSalary WHERE rk = N LIMIT 1;</code>",
            "kw": ["DENSE_RANK()", "Correlated Check", "CTE Filter", "Offset Seek"],
            "depth": "The CTE Dense Rank method is generally faster due to set-based sorting optimizations instead of the nested O(N^2) loops of correlated queries."
        },
        {
            "q": "Q4: How do you identify and delete duplicate user rows based on email, keeping only the record with the lowest primary key ID?",
            "a": "To locate duplicates: <code>SELECT email, COUNT(*) FROM Users GROUP BY email HAVING COUNT(*) > 1;</code>. To delete duplicates: <code>WITH DuplicateRows AS (SELECT id, ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) AS rn FROM Users) DELETE FROM Users WHERE id IN (SELECT id FROM DuplicateRows WHERE rn > 1);</code>. This numbers duplicate emails sequentially by ID and deletes any duplicate row indexed higher than 1.",
            "kw": ["ROW_NUMBER() Deletion", "PARTITION BY", "HAVING COUNT > 1", "Subquery filter"],
            "depth": "In massive tables, batch duplicate deletions in intervals (e.g., LIMIT 5000) to prevent transaction log expansion."
        },
        {
            "q": "Q5: What is a covering index, and how does the INCLUDE clause improve query performance?",
            "a": "A covering index is a non-clustered index that contains all columns requested by a query (both filters and projections). When a index covers a query, the database resolves the request using the index leaf nodes directly. The INCLUDE clause appends non-key columns to the index leaf nodes without sorting them, avoiding the physical clustered index traversal known as Key/RID lookup.",
            "kw": ["Key Lookup", "RID Lookup", "INCLUDE Key", "Leaf Node Content"],
            "depth": "Adding columns to the INCLUDE clause avoids index sorting overhead because columns are stored raw at the leaf node level."
        },
        {
            "q": "Q6: Explain transaction isolation levels and how they prevent dirty reads, non-repeatable reads, and phantom reads.",
            "a": "Read Uncommitted permits dirty reads (reading uncommitted write buffers). Read Committed prevents dirty reads by reading only committed data. Repeatable Read prevents non-repeatable reads (row values modified mid-transaction) using read locks or snapshot views. Serializable prevents phantom reads (new rows inserted in selected ranges) by using range/gap locking. Each level trades concurrency for safety.",
            "kw": ["MVCC Snapshots", "Gap Locking", "Read Locks", "Anomaly Isolation"],
            "depth": "Engines like PostgreSQL/MySQL implement Repeatable Read using MVCC, which handles phantom reads without using lock ranges."
        },
        {
            "q": "Q7: Write a query to find all users who logged in for 3 consecutive days, explaining the gap-and-island technique.",
            "a": "Using row number difference:<br><code>WITH GroupedLogins AS (SELECT user_id, login_date, login_date - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) * INTERVAL '1 day' AS grp FROM Logins) SELECT DISTINCT user_id FROM GroupedLogins GROUP BY user_id, grp HAVING COUNT(*) >= 3;</code>. Subtracting the sequential row index from dates yields identical anchor dates for consecutive login series.",
            "kw": ["Gaps and Islands", "Row Number Offset", "Date Interval Math", "Consecutive Days"],
            "depth": "This partitions dates into groups without procedural loops. The CTE evaluates in O(N log N) sorting time."
        },
        {
            "q": "Q8: How do you optimize a query with the filter WHERE LOWER(username) = 'john' and why does it run slow?",
            "a": "Wrapping columns in functions like <code>LOWER()</code> makes predicates non-SARGable, forcing a full table scan because the engine must compute LOWER() for every row. Optimize it by: 1. Making the search case-insensitive at the database schema collation level. 2. Creating a Function-Based Index (or expression index): <code>CREATE INDEX idx_lower_user ON Users (LOWER(username));</code>.",
            "kw": ["Non-SARGable Predicate", "Function-Based Index", "Expression Index", "Collation Setup"],
            "depth": "Function-based indexes compute and store values during write operations, restoring O(log N) seeking paths."
        },
        {
            "q": "Q9: Write a query to calculate a running total of transactions per account over time.",
            "a": "Running total is computed using window SUM:<br><code>SELECT account_id, trans_date, amount, SUM(amount) OVER (PARTITION BY account_id ORDER BY trans_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total FROM Transactions;</code>. The frame clause instructs the engine to sum values from the start of the account partition up to the current row date.",
            "kw": ["Window Aggregate", "Running Total", "Frame Bounds", "ROWS BETWEEN"],
            "depth": "Omitting the ROWS frame clause defaults the frame boundary to RANGE, which is slower because it evaluates duplicate dates together."
        },
        {
            "q": "Q10: Explain theCAP Theorem and PACELC extension for distributed database designs.",
            "a": "CAP Theorem states that a distributed data system can simultaneously guarantee only two of: Consistency, Availability, and Partition Tolerance. PACELC extends this: If there is a Partition (P), choose Availability (A) or Consistency (C); Else (E), trade Latency (L) or Consistency (C). This models real-world database choices like MongoDB (CP) or Cassandra (AP).",
            "kw": ["CAP Theorem", "PACELC Extension", "Eventual Consistency", "Latency vs Consistency"],
            "depth": "Distributed setups like Spanner utilize atomic clocks (TrueTime API) to achieve both consistency and partition tolerance."
        }
    ]
    
    pages_html = ""
    for p_idx in range(5):
        q1 = qas[p_idx * 2]
        q2 = qas[p_idx * 2 + 1]
        page_num = 46 + p_idx
        
        pages_html += f"""
  <div class="page" id="sql-expectedqa-p{p_idx+1}">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="header-badge" style="background: rgba(255,255,255,0.25);">EXPECTED Q&amp;A</div>
      </div>
    </div>
    
    <div style="padding: 20px 24px; flex: 1; display: flex; flex-direction: column; overflow: hidden;">
      <div style="text-align: center; margin-bottom: 10px;">
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">SQL Top Expected Interview Questions</div>
        <div style="font-size: 9pt; color: #EA763F; font-weight: 700; margin-top: 2px;">Placement Q&amp;As · Created by Pranav Gawai (Part {p_idx+1})</div>
      </div>
      
      <div style="display: flex; flex-direction: column; gap: 8px;">
        <!-- Question block 1 -->
        <div style="border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px; background: white;">
          <div style="font-weight: 800; font-size: 8.5pt; color: #EA763F; margin-bottom: 3px;">{q1['q']}</div>
          <div style="font-size: 7.5pt; color: #333; line-height: 1.35; margin-bottom: 4px;">{q1['a']}</div>
          <div style="font-size: 7pt; color: #718096; margin-bottom: 4px;">
            <strong>Keywords:</strong> {" · ".join([f"<span>{k}</span>" for k in q1['kw']])}
          </div>
          <div style="font-size: 7pt; color: #2B6CB0; background: #EBF8FF; padding: 4px 6px; border-radius: 4px; border-left: 2px solid #3182CE;">
            <strong>Senior Depth:</strong> {q1['depth']}
          </div>
        </div>
        
        <!-- Question block 2 -->
        <div style="border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px; background: white;">
          <div style="font-weight: 800; font-size: 8.5pt; color: #EA763F; margin-bottom: 3px;">{q2['q']}</div>
          <div style="font-size: 7.5pt; color: #333; line-height: 1.35; margin-bottom: 4px;">{q2['a']}</div>
          <div style="font-size: 7pt; color: #718096; margin-bottom: 4px;">
            <strong>Keywords:</strong> {" · ".join([f"<span>{k}</span>" for k in q2['kw']])}
          </div>
          <div style="font-size: 7pt; color: #2B6CB0; background: #EBF8FF; padding: 4px 6px; border-radius: 4px; border-left: 2px solid #3182CE;">
            <strong>Senior Depth:</strong> {q2['depth']}
          </div>
        </div>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> SQL <span>›</span> <span>Expected Q&amp;A</span></div>
      </div>
      <div class="page-number-premium">PAGE {page_num} / 55</div>
    </div>
  </div>
        """
    return pages_html

# ─────────────────────────────────────────
# RAPID FIRE QUESTIONS PAGES (Pages 51 - 52, 32 Questions)
# ─────────────────────────────────────────
def generate_rapid_fire_page(LOGO_BASE64):
    qas = [
        ("What does SELECT 1 FROM table do?", "Returns integer 1 for each matching row; used in EXISTS checks."),
        ("What is the default sort order of ORDER BY?", "Ascending (ASC)."),
        ("How does DISTINCT eliminate duplicates?", "Uses hash aggregation or sorting algorithms to collapse rows."),
        ("What is the danger of high LIMIT offsets?", "Scans and discards skipped rows, creating database I/O latency."),
        ("Can we select columns not in GROUP BY?", "No, unless they are wrapped in aggregate functions."),
        ("Difference between COUNT(*) and COUNT(col)?", "COUNT(*) counts all rows; COUNT(col) counts only non-null values."),
        ("What join produces a Cartesian Product?", "CROSS JOIN."),
        ("Does a LEFT JOIN preserve right-side rows?", "No, it preserves left-side rows with null padding for right rows."),
        ("When is a SELF JOIN useful?", "Mapping parent-child, supervisor-employee, or recursive structures."),
        ("What is a correlated subquery?", "A subquery that references outer columns, running row-by-row."),
        ("What is the benefit of EXISTS over IN?", "EXISTS short-circuits on the first match, bypassing complete scans."),
        ("What does a CTE stand for?", "Common Table Expression (WITH clause result sets)."),
        ("Can a CTE be recursive?", "Yes, referencing itself to traverse tree schemas."),
        ("What clause is mandatory for window functions?", "The OVER clause."),
        ("What does LEAD(col, 2) do?", "Accesses values located 2 rows forward in the window partition."),
        ("What is the output of DENSE_RANK() for ties?", "Assigns identical ranks, incrementing by 1 for the next distinct rank."),
        ("What index structure is used by default?", "B-Tree (specifically B+ Tree node structures)."),
        ("How many clustered indexes can a table have?", "One, because data rows can only be physically sorted one way."),
        ("What is a covering index?", "An index containing all columns selected, filtered, and projected by a query."),
        ("What is a SARGable predicate?", "A search argument that allows the query engine to perform an index seek."),
        ("What is an execution plan?", "The query compiler's step-by-step roadmap for executing SQL."),
        ("What does the 'I' in ACID stand for?", "Isolation (preventing concurrent transaction interference)."),
        ("What are the 4 database isolation levels?", "Read Uncommitted, Read Committed, Repeatable Read, Serializable."),
        ("What is a dirty read?", "Reading uncommitted writes from parallel transactions."),
        ("What is a phantom read?", "New rows inserted in a selected range mid-transaction."),
        ("What does a COMMIT statement do?", "Permanently writes transactional modifications to tablespace files."),
        ("What is a deadlock?", "A circular lock block between two transactions."),
        ("How does a DB resolve deadlocks?", "Kills and rolls back the transaction with the lowest cost victim."),
        ("What is a Shared Lock (S-Lock)?", "Read lock allowing concurrent reads but blocking modifications."),
        ("What is an Exclusive Lock (X-Lock)?", "Write lock blocking all parallel access to target rows."),
        ("What is the SQL standard date format?", "YYYY-MM-DD."),
        ("What does DATE_TRUNC('month', date) do?", "Rounds a date timestamp to the first day of that month.")
    ]
    
    def render_rapid_card(q, a):
        return f"""
        <div style="border: 1px solid #E2E8F0; border-radius: 6px; padding: 6px 8px; background: white;">
          <div style="font-weight: 800; font-size: 8pt; color: #EA763F; margin-bottom: 2px;">Q: {q}</div>
          <div style="font-size: 7.5pt; color: #4A5568; line-height: 1.35;">A: {a}</div>
        </div>
        """
        
    p1_left = "".join([render_rapid_card(q, a) for q, a in qas[:8]])
    p1_right = "".join([render_rapid_card(q, a) for q, a in qas[8:16]])
    
    p2_left = "".join([render_rapid_card(q, a) for q, a in qas[16:24]])
    p2_right = "".join([render_rapid_card(q, a) for q, a in qas[24:]])
    
    p1_html = f"""
  <div class="page" id="sql-rapidfire-p1">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="badge-yield" style="background:#FFF5F0; color:#EA763F;">⚡ RAPID FIRE</div>
        <div class="header-badge">Placement Recall</div>
      </div>
    </div>
    
    <div style="padding: 20px 24px; display: flex; flex-direction: column; gap: 10px; flex: 1; overflow: hidden;">
      <div style="text-align: center; margin-bottom: 4px;">
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">SQL Rapid Fire Questions (Part 1)</div>
        <div style="font-size: 9pt; color: #EA763F; font-weight: 700;">Fast-Recall Flashcards for Last-Minute Self-Testing</div>
      </div>
      
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; flex: 1;">
        <div style="display: flex; flex-direction: column; gap: 8px;">
          {p1_left}
        </div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
          {p1_right}
        </div>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> SQL <span>›</span> <span>Rapid Fire</span></div>
      </div>
      <div class="page-number-premium">PAGE 51 / 55</div>
    </div>
  </div>
    """
    
    p2_html = f"""
  <div class="page" id="sql-rapidfire-p2">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="badge-yield" style="background:#FFF5F0; color:#EA763F;">⚡ RAPID FIRE</div>
        <div class="header-badge">Placement Recall</div>
      </div>
    </div>
    
    <div style="padding: 20px 24px; display: flex; flex-direction: column; gap: 10px; flex: 1; overflow: hidden;">
      <div style="text-align: center; margin-bottom: 4px;">
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">SQL Rapid Fire Questions (Part 2)</div>
        <div style="font-size: 9pt; color: #EA763F; font-weight: 700;">Fast-Recall Flashcards for Last-Minute Self-Testing</div>
      </div>
      
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; flex: 1;">
        <div style="display: flex; flex-direction: column; gap: 8px;">
          {p2_left}
        </div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
          {p2_right}
        </div>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> SQL <span>›</span> <span>Rapid Fire</span></div>
      </div>
      <div class="page-number-premium">PAGE 52 / 55</div>
    </div>
  </div>
    """
    return p1_html + p2_html

# ─────────────────────────────────────────
# COMMON TRAPS PAGES (Pages 53 - 54, 10 Traps)
# ─────────────────────────────────────────
def generate_common_traps_page(LOGO_BASE64):
    traps = [
        {
            "t": "Trap 1: The Null Arithmetic Trap",
            "q": "\"What is the result of executing SELECT 10 + NULL in SQL?\"",
            "i": "State clearly that NULL represents an unknown value. Therefore, any standard arithmetic calculation or comparison containing NULL yields NULL. Always use COALESCE(col, 0) to prevent NULL propagation."
        },
        {
            "t": "Trap 2: The WHERE Aggregate Trap",
            "q": "\"Can you filter grouped aggregate values directly inside the WHERE clause?\"",
            "i": "No. The WHERE clause executes before grouping takes place. Aggregated values do not exist yet in the database execution pipeline. You must use HAVING to filter aggregated metrics."
        },
        {
            "t": "Trap 3: The Cartesian Explosion Join Trap",
            "q": "\"What happens if you run an INNER JOIN on a massive table and omit the ON condition?\"",
            "i": "It degenerates into a CROSS JOIN, generating the Cartesian product (Table A rows &times; Table B rows). A 10k-row table paired with a 100k-row table generates 1 billion rows, causing out-of-memory crashes."
        },
        {
            "t": "Trap 4: The IN vs EXISTS subquery execution",
            "q": "\"Is the EXISTS operator always faster than the IN operator for subquery filters?\"",
            "i": "EXISTS is typically faster for subqueries because it short-circuits (returns TRUE upon finding the first match). IN evaluates all subquery results first. However, modern planners optimize both to similar plans."
        },
        {
            "t": "Trap 5: The Primary Key vs Clustered Index myth",
            "q": "\"Does creating a Primary Key always create a Clustered Index?\"",
            "i": "Usually yes by default, but they are conceptually separate. A primary key is a logical unique constraint; a clustered index is a physical layout organization. You can specify a non-clustered primary key."
        },
        {
            "t": "Trap 6: The CTE Materialization Trap",
            "q": "\"Are Common Table Expressions (CTEs) always written to disk memory?\"",
            "i": "No. CTEs are logical wrappers compiled inline by query optimizers (like virtual views). Only temporary tables physically write data to disk structures."
        },
        {
            "t": "Trap 7: Indexing all columns to speed queries",
            "q": "\"Why don't we index every single column in our database tables?\"",
            "i": "Because indexes add write overhead. Every write operation (INSERT/UPDATE/DELETE) must physically update B-Tree structures, degrading write performance and increasing disk storage footprint."
        },
        {
            "t": "Trap 8: The Serializable isolation overhead",
            "q": "\"Is Serializable always the best isolation level because it guarantees correctness?\"",
            "i": "While safest for consistency, it is the worst for performance. It places extensive lock ranges, causing concurrency bottlenecks, transaction timeouts, and deadlock aborts under high web traffic."
        },
        {
            "t": "Trap 9: COUNT(col) NULL evaluation",
            "q": "\"Does COUNT(column_name) count records that contain NULL?\"",
            "i": "No. COUNT(column_name) completely excludes NULL values, counting only populated rows. Only COUNT(*) counts all rows including NULL records."
        },
        {
            "t": "Trap 10: SELECT alias filtering inside WHERE",
            "q": "\"Why can you sort by a column alias in ORDER BY, but you cannot filter by it in WHERE?\"",
            "i": "Because WHERE executes *before* SELECT in the database logical processing sequence, so aliases are not defined yet. ORDER BY executes *after* SELECT, recognizing the aliases."
        }
    ]
    
    def render_trap_block(item):
        return f"""
        <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 8px; background: white; margin-bottom: 4px;">
          <div style="font-weight: 800; font-size: 8pt; color: #C53030; margin-bottom: 2px;">{item['t']}</div>
          <div style="font-size: 7.5pt; font-style: italic; color: #4A5568; margin-bottom: 2px;">Interviewer: {item['q']}</div>
          <div style="font-size: 7.5pt; color: #2D3748; line-height: 1.35; border-left: 2px solid #E53E3E; padding-left: 6px;">
            <strong>Deflection:</strong> {item['i']}
          </div>
        </div>
        """
        
    p1_rows = "".join([render_trap_block(t) for t in traps[:5]])
    p2_rows = "".join([render_trap_block(t) for t in traps[5:]])
    
    p1_html = f"""
  <div class="page" id="sql-commontraps-p1">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="badge-yield" style="background:#FFF5F5; color:#E53E3E;">🛑 INTERVIEW TRAPS</div>
        <div class="header-badge">Placement Tactics</div>
      </div>
    </div>
    
    <div style="padding: 20px 24px; display: flex; flex-direction: column; gap: 10px; flex: 1; overflow: hidden;">
      <div style="text-align: center; margin-bottom: 4px;">
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">SQL Common Traps (Part 1)</div>
        <div style="font-size: 9pt; color: #C53030; font-weight: 700;">Tactics to Evade Trick Interview Questions with Confident Answers</div>
      </div>
      
      <div style="display: flex; flex-direction: column; gap: 2px;">
        {p1_rows}
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> SQL <span>›</span> <span>Traps</span></div>
      </div>
      <div class="page-number-premium">PAGE 53 / 55</div>
    </div>
  </div>
    """
    
    p2_html = f"""
  <div class="page" id="sql-commontraps-p2">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="badge-yield" style="background:#FFF5F5; color:#E53E3E;">🛑 INTERVIEW TRAPS</div>
        <div class="header-badge">Placement Tactics</div>
      </div>
    </div>
    
    <div style="padding: 20px 24px; display: flex; flex-direction: column; gap: 10px; flex: 1; overflow: hidden;">
      <div style="text-align: center; margin-bottom: 4px;">
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">SQL Common Traps (Part 2)</div>
        <div style="font-size: 9pt; color: #C53030; font-weight: 700;">Tactics to Evade Trick Interview Questions with Confident Answers</div>
      </div>
      
      <div style="display: flex; flex-direction: column; gap: 2px;">
        {p2_rows}
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> SQL <span>›</span> <span>Traps</span></div>
      </div>
      <div class="page-number-premium">PAGE 54 / 55</div>
    </div>
  </div>
    """
    return p1_html + p2_html

# ─────────────────────────────────────────
# BLANK NOTES PAGES (Page 55)
# ─────────────────────────────────────────
blank_notes_pages = f"""
  <div class="page" id="sql-notes-1">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="header-badge" style="background: rgba(255,255,255,0.25);">NOTES</div>
      </div>
    </div>
    
    <div style="padding: 24px 30px; flex: 1; display: flex; flex-direction: column;">
      <div style="font-size: 16pt; font-weight: 800; color: #111; border-bottom: 2px solid #EA763F; padding-bottom: 6px; margin-bottom: 12px;">Personal Notes &amp; SQL Queries</div>
      <div class="notes-lines" style="flex: 1; background-image: linear-gradient(#E2E8F0 1px, transparent 1px); background-size: 100% 24px; line-height: 24px; margin-top: 10px;"></div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> SQL <span>›</span> <span>Notes</span> <span style="font-size:7.5pt; color:#A0AEC0; font-weight:normal; margin-left:10px;">grindos.pranavx.in</span></div>
      </div>
      <div class="page-number-premium">PAGE 55 / 55</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# COMPILING HTML PAGES
# ─────────────────────────────────────────
content_pages_html = "".join([generate_page(t, i+4, 55) for i, t in enumerate(topics)])
expected_qa_html = generate_expected_qa_pages(LOGO_BASE64)
rapid_fire_html = generate_rapid_fire_page(LOGO_BASE64)
common_traps_html = generate_common_traps_page(LOGO_BASE64)

# ─────────────────────────────────────────
# CSS DESIGN SYSTEMS
# ─────────────────────────────────────────
css = f"""
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
  @page {{ size: A4 portrait; margin: 0; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ font-family: 'DM Sans', sans-serif; background: #E5E7EB; color: #333; }}
  
  /* A4 PORTRAIT CONTAINER */
  .page {{
    width: 210mm;
    height: 297mm;
    background: #FFFFFF;
    position: relative;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    page-break-after: always;
    break-after: page;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
    margin: 10px auto;
  }}
  
  @media print {{
    body {{ background: white; }}
    .page {{ margin: 0; box-shadow: none; page-break-after: always; break-after: page; }}
  }}
  
  /* BORDER LINE PATTERN ON ALL PAGES */
  .page::before {{
    content: "";
    position: absolute;
    top: 5mm;
    bottom: 5mm;
    left: 5mm;
    right: 5mm;
    border: 1px solid rgba(234, 118, 63, 0.15);
    pointer-events: none;
    border-radius: 4px;
    z-index: 10;
  }}
  
  /* COVER PAGE */
  .cover-page {{ justify-content: center; align-items: center; text-align: center; padding: 40px; border: 8px solid #EA763F; }}
  .cover-page::before {{ display: none; }}
  .cover-logo-container {{ width: 120px; height: 120px; margin-bottom: 40px; display: flex; justify-content: center; align-items: center; }}
  .cover-logo-container img {{ width: 100px; object-fit: contain; }}
  .cover-eyebrow {{ font-size: 14pt; font-weight: 800; color: #EA763F; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 20px; }}
  .cover-title {{ font-size: 40pt; font-weight: 800; color: #111; line-height: 1.1; margin-bottom: 30px; letter-spacing: -1.5px; }}
  .cover-subtitle {{ font-size: 18pt; color: #666; font-weight: 600; margin-bottom: 60px; }}
  .cover-footer {{ position: absolute; bottom: 60px; font-size: 12pt; font-weight: 800; color: #888; letter-spacing: 1px; display: flex; align-items: center; gap: 12px; }}
  .cover-footer img {{ height: 24px; }}
  .cover-footer a {{ text-decoration: none; color: inherit; }}

  /* TOC PAGE */
  .toc-page {{ justify-content: flex-start; }}
  .toc-inner {{ padding: 30px 40px; width: 100%; }}

  /* HEADER */
  .header {{ background: #EA763F; height: 11mm; display: flex; justify-content: space-between; align-items: center; padding: 0 24px; color: white; flex-shrink: 0; margin-top: 5mm; margin-left: 5mm; margin-right: 5mm; }}
  .header-left {{ display: flex; align-items: center; gap: 12px; }}
  .header-logo {{ height: 7mm; filter: brightness(0) invert(1); }}
  .header-wordmark {{ font-size: 16pt; font-weight: 800; letter-spacing: -0.5px; }}
  .header-right {{ display: flex; align-items: center; gap: 8px; }}
  .badge-yield {{ background: #FFF; color: #E53E3E; padding: 4px 10px; border-radius: 20px; font-weight: 800; font-size: 8.5pt; display: flex; align-items: center; gap: 4px; }}
  .header-badge {{ background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 4px; font-weight: 700; font-size: 10pt; }}

  /* TOPIC BAR */
  .topic-bar {{ padding: 10px 24px; border-bottom: 2px solid #EBE5DB; background: white; flex-shrink: 0; margin-left: 5mm; margin-right: 5mm; }}
  .topic-bar-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }}
  .topic-eyebrow {{ font-size: 9pt; color: #EA763F; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px; }}
  .yield-rating {{ font-size: 9pt; font-weight: 800; color: #4A5568; }}
  .stars-gold {{ color: #D69E2E; font-size: 10pt; letter-spacing: 1px; }}
  .topic-title {{ font-size: 18pt; font-weight: 800; color: #111; margin-bottom: 2px; letter-spacing: -0.5px; }}
  .topic-subtitle {{ font-size: 9pt; color: #666; font-weight: 600; line-height: 1.3; }}

  /* BODY COLUMNS */
  .body-container {{ display: flex; flex: 1; overflow: hidden; margin-left: 5mm; margin-right: 5mm; }}
  .col-left {{ width: 50%; background: #FEF8F4; padding: 12px 16px; border-right: 1px solid #F0E6DD; overflow: hidden; display: flex; flex-direction: column; gap: 10px; }}
  .col-right {{ width: 50%; background: #FFFFFF; padding: 12px 16px; display: flex; flex-direction: column; gap: 10px; overflow: hidden; }}
  
  /* BOXES */
  .box {{ border-radius: 8px; padding: 10px 12px; font-size: 8.5pt; line-height: 1.45; }}
  .box-title {{ font-size: 8pt; font-weight: 800; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.8px; display: flex; align-items: center; gap: 6px; }}
  .box-theory {{ border-left: 4px solid #EA763F; background: #FFF5F0; }}
  .box-theory .box-title {{ color: #EA763F; }}
  .box-industry {{ background: #FDF6E3; border: 1px solid #F5E6B3; }}
  .box-industry .box-title {{ color: #B7791F; }}
  .box-question {{ background: #EBF2F9; border: 1px solid #C5D9ED; }}
  .box-question .box-title {{ color: #2B6CB0; }}
  .box-question p {{ font-weight: 700; color: #1A365D; font-size: 9.5pt; line-height: 1.35; }}
  .box-buzzwords {{ background: #FDF2F8; border: 1px dashed #FCC2D7; }}
  .box-buzzwords .box-title {{ color: #D53F8C; margin-bottom: 4px; }}
  .buzzword-tags {{ display: flex; gap: 4px; flex-wrap: wrap; }}
  .buzz-tag {{ background: white; border: 1px solid #FCC2D7; color: #B83280; padding: 3px 6px; border-radius: 4px; font-weight: 800; font-size: 7pt; text-transform: uppercase; letter-spacing: 0.5px; }}
  .box-answer {{ background: #FFFFFF; border: 1px solid #E2E8F0; box-shadow: 0 4px 10px rgba(0,0,0,0.03); }}
  .box-answer .box-title {{ color: #4A5568; }}
  
  /* NEW PLACEMENT BOOSTER BOXES */
  .box-say {{ border-left: 4px solid #38A169; background: #F0FFF4; }}
  .box-say .box-title {{ color: #38A169; }}
  .box-mistake {{ border-left: 4px solid #E53E3E; background: #FFF5F5; }}
  .box-mistake .box-title {{ color: #E53E3E; }}
  .box-depth {{ border-left: 4px solid #3182CE; background: #EBF8FF; }}
  .box-depth .box-title {{ color: #3182CE; }}
  .box-scenario {{ border-left: 4px solid #805AD5; background: #F5EBFE; }}
  .box-scenario .box-title {{ color: #805AD5; }}
  .box-comparison {{ border-left: 4px solid #319795; background: #E6FFFA; }}
  .box-comparison .box-title {{ color: #319795; }}
  
  /* FOLLOW-UP SUBSECTION */
  .followup-box {{ background: #F5EBFE; border: 1px solid #E9D8FD; }}
  .followup-title {{ color: #6B46C1; }}
  .followup-q {{ font-weight: 800; color: #44337A; font-size: 8.5pt; margin-bottom: 2px; }}
  .followup-q::before {{ content: "→ "; color: #805AD5; }}
  .followup-a {{ color: #553C9A; font-size: 8pt; line-height: 1.35; }}

  /* CONCEPT DIAGRAMS */
  .concept-visual {{ background: white; border-radius: 8px; padding: 10px; border: 1px solid #EBE5DB; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
  .visual-table {{ width: 100%; border-collapse: collapse; font-size: 7.5pt; text-align: center; }}
  .visual-table th {{ background: #EDF2F7; color: #4A5568; padding: 4px; border-bottom: 1.5px solid #CBD5E0; font-weight: 800; }}
  .visual-table td {{ padding: 4px; border-bottom: 1px solid #E2E8F0; }}
  
  .row-app {{ background: #FFF5F5; font-weight: bold; color: #C53030; }}
  .row-trans {{ background: #FFFFF0; font-weight: bold; color: #B7791F; }}
  .row-net {{ background: #EBF8FF; font-weight: bold; color: #2B6CB0; }}
  .row-link {{ background: #F0FFF4; font-weight: bold; color: #276749; }}
  .row-phy {{ background: #F7FAFC; font-weight: bold; color: #4A5568; }}
  
  .contrast-table td {{ font-weight: bold; }}
  .contrast-table tr:nth-child(even) {{ background: #F7FAFC; }}
  
  .flow-container {{ display: flex; flex-direction: column; width: 100%; align-items: center; justify-content: center; gap: 2px; }}
  .flow-block {{ width: 90%; text-align: center; padding: 6px; border-radius: 6px; font-size: 8pt; font-weight: 800; border: 1.5px solid; }}
  .block-orange {{ background: #FFF5F0; border-color: #EA763F; color: #EA763F; }}
  .block-blue {{ background: #EBF8FF; border-color: #3182CE; color: #3182CE; }}
  .block-green {{ background: #F0FFF4; border-color: #38A169; color: #38A169; }}
  .block-grey {{ background: #F7FAFC; border-color: #CBD5E0; color: #4A5568; }}
  .flow-arrow {{ font-size: 7pt; font-weight: bold; color: #A0AEC0; margin: 1px 0; }}
  
  .diagram-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; width: 100%; }}
  .grid-item {{ border: 1px solid #E2E8F0; padding: 6px; border-radius: 6px; font-size: 8pt; text-align: center; background: white; }}

  /* NOTES LINES FOR BLANK PAGES */
  .notes-lines {{
    flex: 1;
    background-image: linear-gradient(#E2E8F0 1px, transparent 1px);
    background-size: 100% 24px;
    margin-top: 10px;
  }}

  /* BOTTOM PLACEMENT GRID (L4) */
  .bottom-placement-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 6px;
    padding: 6px 12px;
    background: #FDFBF7;
    border-top: 2px solid #EBE5DB;
    flex-shrink: 0;
    min-height: 110px;
    max-height: 125px;
    margin-left: 5mm;
    margin-right: 5mm;
  }}
  .placement-block {{
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 7pt;
    line-height: 1.25;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .placement-block-title {{
    font-size: 7pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 1px;
    display: flex;
    align-items: center;
    gap: 4px;
  }}
  .block-mistake {{ background: #FFF5F5; border-left: 3px solid #E53E3E; color: #742A2A; }}
  .block-mistake .placement-block-title {{ color: #C53030; }}
  .block-trap {{ background: #FFF5F0; border-left: 3px solid #EA763F; color: #7B341E; }}
  .block-trap .placement-block-title {{ color: #DD6B20; }}
  .block-followups {{ background: #F5EBFE; border-left: 3px solid #805AD5; color: #553C9A; }}
  .block-followups .placement-block-title {{ color: #6B46C1; }}
  .block-trick {{ background: #F0FFF4; border-left: 3px solid #38A169; color: #276749; }}
  .block-trick .placement-block-title {{ color: #2F855A; }}

  /* FOOTER WITH PREMIUM PAGE NUMBERS */
  .footer {{ height: 30px; background: white; border-top: 1px solid #EDE5D8; display: flex; justify-content: space-between; align-items: center; padding: 0 24px; font-size: 8pt; color: #718096; flex-shrink: 0; font-weight: 700; margin-bottom: 4mm; margin-left: 5mm; margin-right: 5mm; }}
  .footer-left {{ display: flex; align-items: center; gap: 8px; }}
  .footer-logo {{ height: 12px; }}
  .breadcrumb {{ color: #A0AEC0; }}
  .breadcrumb span {{ color: #4A5568; font-weight: 800; margin: 0 4px; }}
  .page-number-premium {{ font-size: 8pt; font-weight: 800; color: #EA763F; letter-spacing: 1px; background: #FFF5F0; padding: 2px 8px; border-radius: 4px; border: 1px solid #FBD38D; }}
"""

# Compile final template
html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SQL Placement Handbook</title>
<style>{css}</style>
</head>
<body>
  <!-- COVER PAGE -->
  <div class="page cover-page" id="sql-cover">
    <div class="cover-logo-container">
      <img src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS">
    </div>
    <div class="cover-eyebrow">Core Computer Science</div>
    <div class="cover-title">Structured<br>Query Language</div>
    <div class="cover-subtitle">Placement Preparation Handbook</div>
    <div style="font-size: 11pt; color: #718096; font-weight: 700; margin-top: -30px; margin-bottom: 50px;">Created by Pranav Gawai</div>
    <div class="cover-footer">
      <img src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
      <a href="https://grindos.pranavx.in">grindos.pranavx.in</a>
    </div>
  </div>

  <!-- ROADMAP PAGE -->
  {roadmap_page}

  <!-- TOC PAGE -->
  {toc_page}

  <!-- CONTENT PAGES -->
  {content_pages_html}

  <!-- CRAM SHEET -->
  {cram_sheet_page}

  <!-- COMPARISON SHEET -->
  {comparison_sheet_page}

  <!-- EXPECTED Q&A PAGES -->
  {expected_qa_html}

  <!-- RAPID FIRE PAGES -->
  {rapid_fire_html}

  <!-- COMMON TRAPS PAGES -->
  {common_traps_html}

  <!-- BLANK NOTES PAGES -->
  {blank_notes_pages}
</body>
</html>
"""

# Write to file
os.makedirs("subjects/sql", exist_ok=True)
output_path = "subjects/sql/01_sql_notes.html"
with open(output_path, "w") as f:
    f.write(html_out)

print(f"Generated complete SQL Handbook with {len(topics)} topics.")
