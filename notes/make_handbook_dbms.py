import base64
import os

# Load logo
with open("../logo.png", "rb") as img_file:
    LOGO_BASE64 = base64.b64encode(img_file.read()).decode('utf-8')

# ─────────────────────────────────────────
# 24 DBMS TOPICS + 6 SQL PRACTICE PAGES (30 total)
# ─────────────────────────────────────────
topics = [
    {
        "id": "db-3tier",
        "num": "01",
        "chapter": "DBMS Architecture & Fundamentals",
        "title": "3-Tier Architecture",
        "subtitle": "The industry standard design structure for web applications.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p><strong>1-Tier:</strong> Direct user access to database (local dev).<br>
  <strong>2-Tier:</strong> Client-Server model. Client contacts DB directly (JDBC/ODBC). Limited scalability.<br>
  <strong>3-Tier:</strong> Adds an Application Server between client and database for business logic, safety, and caching.</p>
</div>
<div class="concept-visual">
  <div class="flow-container">
    <div class="flow-block block-orange">Presentation Tier (UI)<br><span class="desc">Browser / Mobile App</span></div>
    <div class="flow-arrow">↓↑ APIs / REST</div>
    <div class="flow-block block-blue">Application Tier (Server)<br><span class="desc">Node.js / Python / Spring</span></div>
    <div class="flow-arrow">↓↑ Connection Pooling</div>
    <div class="flow-block block-green">Data Tier (Database)<br><span class="desc">PostgreSQL / MySQL</span></div>
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">Connection Pooling</div>
  <p>Rather than opening a new DB connection for every client request, the Application Server maintains a pool of active connections, recycling them to handle 10,000 clients with just 100 DB links.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why is a 3-Tier architecture preferred over 2-Tier in enterprise web services?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Data Abstraction</span>
    <span class="buzz-tag">Connection Pooling</span>
    <span class="buzz-tag">Security Firewalls</span>
    <span class="buzz-tag">Independent Scaling</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A 3-Tier architecture provides data abstraction, preventing client devices from directly querying database engines. This shields credentials, mitigates SQL injections, allows connection pooling to conserve DB resources, and enables scaling server nodes independently of storage nodes."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"Where does database caching typically live?"</p>
  <p class="followup-a">In the Application Tier (using in-memory stores like Redis) to serve read queries without hitting the database disk.</p>
</div>
""",
        "trap": "Don't say 2-Tier is extinct. Many internal desktop software configurations and administrative shell tools still use direct 2-Tier database credentials.",
        "trick": "3-Tier inserts an Application Server as a bouncer between the guest (client) and the VIP lounge (database)."
    },
    {
        "id": "db-indep",
        "num": "02",
        "chapter": "DBMS Architecture & Fundamentals",
        "title": "Data Independence",
        "subtitle": "Modifying schema layers without cascading changes to higher levels.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Schema Architecture</div>
  <p><strong>Physical Independence:</strong> Changing physical storage organization (SSD migration, file pathing) without altering conceptual schemas.</p>
  <p><strong>Logical Independence:</strong> Changing conceptual table structures (adding columns/tables) without breaking external views or user queries.</p>
</div>
<div class="concept-visual">
  <div style="font-family:monospace; font-size:7.5pt; text-align:center; border:1px solid #CBD5E0; padding:6px; background:white; width:100%;">
    [External Views] (Logical Independence)<br>
    ↓ mapping layer<br>
    [Conceptual Schema] (Physical Independence)<br>
    ↓ mapping layer<br>
    [Physical Storage Schema]
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"If I create an index on a table, which type of data independence is demonstrated?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Schema Mapping</span>
    <span class="buzz-tag">Physical Files</span>
    <span class="buzz-tag">Query Abstraction</span>
    <span class="buzz-tag">Logical Views</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Physical Data Independence. Adding an index changes how data is physically searched and stored on disk, but it does not change the logical tables, columns, or the SELECT queries used by the application code."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"Why is Logical Data Independence harder to achieve than Physical?"</p>
  <p class="followup-a">Because changes to tables (like splitting one table into two) require complex view rewrites to present the original structure to applications.</p>
</div>
""",
        "trap": "Don't confuse the two. If columns change, it is Logical. If disk file indexing changes, it is Physical.",
        "trick": "Logical = Logic (tables/relations). Physical = Plastic/Metal (disks, file structures)."
    },
    {
        "id": "db-keys",
        "num": "03",
        "chapter": "Relational Model Core",
        "title": "Database Keys",
        "subtitle": "Constraint identifiers to establish integrity and unique records.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Key Classifications</div>
  <p><strong>Super Key:</strong> Set of attributes that uniquely identifies a row. May contain redundant columns.</p>
  <p><strong>Candidate Key:</strong> A minimal Super Key. Removing any column destroys uniqueness.</p>
  <p><strong>Primary Key:</strong> The chosen candidate key. Cannot be NULL.</p>
  <p><strong>Foreign Key:</strong> References the Primary Key of another table, ensuring referential integrity.</p>
</div>
<div class="concept-visual">
  <div style="padding:8px; border:1px solid #CBD5E0; border-radius:6px; background:white; font-size:7.5pt; text-align:center;">
    [Super Keys (Broadest)]<br>
    ↓ minimal subsets<br>
    [Candidate Keys]<br>
    ↓ chosen one<br>
    <strong>[Primary Key]</strong>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Can a Foreign Key contain NULL values? Can a Primary Key contain NULLs?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Entity Integrity</span>
    <span class="buzz-tag">Referential Integrity</span>
    <span class="buzz-tag">Candidate Key</span>
    <span class="buzz-tag">Null Value Support</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A Primary Key can never be NULL due to Entity Integrity, as it uniquely identifies the row. A Foreign Key, however, CAN be NULL if the relationship is optional (e.g. an employee without an assigned department)."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a surrogate key?"</p>
  <p class="followup-a">A system-generated key (like an auto-incrementing integer or UUID) with no business meaning, used to uniquely identify rows when natural keys are missing.</p>
</div>
""",
        "trap": "Don't say a table can have multiple Primary Keys. It can only have ONE Primary Key, although that PK can be a composite of multiple columns.",
        "trick": "Super = anything unique. Candidate = minimalist unique. Primary = the chosen candidate."
    },
    {
        "id": "db-normalization",
        "num": "04",
        "chapter": "Relational Model Core",
        "title": "Normal Forms (1NF → BCNF)",
        "subtitle": "Structuring tables to eliminate redundancy and data anomalies.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Normalization Rules</div>
  <p><strong>1NF:</strong> Atomic values only (no lists/arrays in a cell).</p>
  <p><strong>2NF:</strong> In 1NF + No Partial Dependencies (non-key columns must depend on the entire candidate key).</p>
  <p><strong>3NF:</strong> In 2NF + No Transitive Dependencies (non-key columns cannot depend on other non-key columns).</p>
  <p><strong>BCNF:</strong> For every dependency X → Y, X must be a super key.</p>
</div>
<div class="concept-visual">
  <table class="visual-table contrast-table" style="font-size:7.5pt;">
    <thead>
      <tr>
        <th>Normal Form</th>
        <th>Main Requirement</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>1NF</td><td>Atomic Columns</td></tr>
      <tr><td>2NF</td><td>No Partial Dependencies</td></tr>
      <tr><td>3NF</td><td>No Transitive Dependencies</td></tr>
      <tr><td>BCNF</td><td>X → Y (X must be Super Key)</td></tr>
    </tbody>
  </table>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Explain the difference between 3NF and BCNF. When does a table satisfy 3NF but fail BCNF?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Overlapping Keys</span>
    <span class="buzz-tag">Determinant Check</span>
    <span class="buzz-tag">Transitive Loss</span>
    <span class="buzz-tag">Super Key Rule</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A table is in 3NF if for X → Y, either X is a super key or Y is a prime attribute. BCNF removes the 'prime attribute' loophole. A table fails BCNF if it has overlapping candidate keys where a prime attribute transitively determines part of another key."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"Why do we intentionally denormalize database tables?"</p>
  <p class="followup-a">To improve read performance in data warehouses or reporting services by avoiding expensive multi-table JOIN operations.</p>
</div>
""",
        "trap": "Don't say BCNF is always preferred. BCNF can lose functional dependencies during decomposition, which is why 3NF is sometimes chosen.",
        "trick": "The key, the whole key, and nothing but the key (so help me Codd)."
    },
    {
        "id": "db-advanced-nf",
        "num": "05",
        "chapter": "Relational Model Core",
        "title": "4NF & 5NF Normalization",
        "subtitle": "Handling multi-valued dependencies and join dependency structures.",
        "yield_stars": "★★★☆☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Higher Normal Forms</div>
  <p><strong>4NF:</strong> In BCNF + No Multi-Valued Dependencies (MVD). If A determines a set of values for B and C independently, B and C must not be stored in the same table.</p>
  <p><strong>5NF (PJNF):</strong> In 4NF + No Join Dependencies. A table cannot be reconstructed from several smaller tables without losing information.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is a Multi-Valued Dependency (MVD), and how does 4NF resolve it?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Multi-Valued Dep</span>
    <span class="buzz-tag">Independent Attributes</span>
    <span class="buzz-tag">Table Decomposition</span>
    <span class="buzz-tag">Trivial Dependency</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"An MVD occurs when an attribute determines multiple independent values (e.g. a teacher teaches multiple subjects AND speaks multiple languages). 4NF resolves this by decomposing the table into separate tables: (Teacher, Subject) and (Teacher, Language)."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a Join Dependency in 5NF?"</p>
  <p class="followup-a">A join dependency exists if a table can be decomposed into N smaller tables, which when joined back, recreate the exact original table without spurious rows.</p>
</div>
""",
        "trap": "Don't worry about 5NF for simple business app interviews; it is extremely rare in real-world database design and mostly theoretical.",
        "trick": "4NF splits unrelated checklists that get awkwardly crammed into a single table."
    },
    {
        "id": "db-er-mapping",
        "num": "06",
        "chapter": "Database Design & Models",
        "title": "ER Model to Relational",
        "subtitle": "Mapping Entity-Relationship diagrams to logical database tables.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Mapping Paradigms</div>
  <p><strong>Strong Entity:</strong> Becomes a table with its key as the Primary Key.</p>
  <p><strong>Weak Entity:</strong> Becomes a table including its owner entity's PK as a Foreign Key, combined as a composite PK.</p>
  <p><strong>1-to-Many Relationship:</strong> Place the PK of the '1' side as a Foreign Key in the 'Many' side table.</p>
</div>
<div class="concept-visual">
  <div style="border:1px solid #CBD5E0; border-radius:6px; padding:10px; background:white; font-size:7.5pt; text-align:center;">
    <strong>Many-to-Many Mapping</strong><br>
    Create a new <strong>Junction Table</strong> containing:<br>
    Composite PK: (FK_EntityA, FK_EntityB)
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How do you map a Weak Entity set to a relational table structure?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Identifying Relationship</span>
    <span class="buzz-tag">Composite Primary Key</span>
    <span class="buzz-tag">Discriminator Column</span>
    <span class="buzz-tag">Cascade Delete</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A weak entity cannot be identified by its own attributes alone. To map it: create a table, import the primary key of the identifying strong entity as a foreign key, and combine it with the weak entity's discriminator column as a composite primary key."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a recursive relationship in ER diagrams?"</p>
  <p class="followup-a">A relationship where an entity relates to itself (e.g. an Employee table has a Foreign Key pointing back to the Employee table's Manager ID).</p>
</div>
""",
        "trap": "Don't forget to implement CASCADE deletes for weak entity tables, as they cannot exist without their parent strong entities.",
        "trick": "Many-to-Many = Marriage table. You need a third paper (junction table) linking the two spouses."
    },
    {
        "id": "db-acid-wal",
        "num": "07",
        "chapter": "Transaction Management",
        "title": "ACID Properties & WAL",
        "subtitle": "Guarantees for reliable database transaction execution.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">ACID Guarantees</div>
  <p><strong>Atomicity:</strong> All or nothing transaction execution.<br>
  <strong>Consistency:</strong> Moves DB from one valid state to another (violating constraints rolls back).<br>
  <strong>Isolation:</strong> Concurrent transactions run as if sequential.<br>
  <strong>Durability:</strong> Committed data survives system crashes.</p>
</div>
<div class="concept-visual">
  <div style="border:1px solid #E2E8F0; padding:10px; background:white; border-radius:6px; font-size:7.5pt; text-align:center;">
    <strong>Write-Ahead Logging (WAL)</strong><br>
    Transaction changes written to <strong>WAL on Disk</strong> first<br>
    ↓ then<br>
    Data modified in buffer cache &amp; flushed to DB disk
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How does a database guarantee Atomicity and Durability during a sudden server crash?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Write-Ahead Log (WAL)</span>
    <span class="buzz-tag">Transaction Rollback</span>
    <span class="buzz-tag">REDO / UNDO Log</span>
    <span class="buzz-tag">Flush to Disk</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Through Write-Ahead Logging (WAL). Every database modification is written to an append-only log on disk before changes are applied to data files. On crash recovery, the engine replays the WAL to REDO committed transactions (Durability) and UNDOs uncommitted ones (Atomicity)."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a checkpoint in database logging?"</p>
  <p class="followup-a">A marker in the log indicating that all dirty data buffers have been flushed to disk. During recovery, the DB only scans logs recorded after the last checkpoint.</p>
</div>
""",
        "trap": "Don't confuse ACID Consistency with CAP Theorem Consistency. ACID is constraint validation. CAP is distributed node synchronization.",
        "trick": "WAL is like writing your will on paper before distributing the physical money."
    },
    {
        "id": "db-tx-states",
        "num": "08",
        "chapter": "Transaction Management",
        "title": "Transaction States",
        "subtitle": "The lifecycle stages of active database transactions.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">State Transitions</div>
  <p>Transactions traverse distinct states during execution: <strong>Active</strong> (running queries) → <strong>Partially Committed</strong> (checks complete, but writing logs) → <strong>Committed</strong> (permanent) or <strong>Failed/Aborted</strong> (rollback).</p>
</div>
<div class="concept-visual">
  <div style="font-family:monospace; font-size:7pt; line-height:1.25; background:#FAFAFA; border:1px solid #CBD5E0; padding:8px; text-align:center;">
    &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [Active]<br>
    &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; / &nbsp; &nbsp; \\<br>
    [Partially Committed] &nbsp; [Failed]<br>
    &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;|<br>
    &nbsp; &nbsp; &nbsp; [Committed] &nbsp; &nbsp; [Aborted]
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is the difference between a Partially Committed state and a Committed state?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Buffer Cache</span>
    <span class="buzz-tag">Flush to Disk</span>
    <span class="buzz-tag">Commit Command</span>
    <span class="buzz-tag">Permanent Save</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A transaction is partially committed when its final statement has run, but changes are still held in volatile RAM buffers. It transitions to the Committed state only after the commit records are written to the transaction log on disk."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a cascading rollback?"</p>
  <p class="followup-a">If Transaction A reads dirty data from uncommitted Transaction B, and Transaction B aborts, Transaction A must also be rolled back, potentially triggering a chain reaction.</p>
</div>
""",
        "trap": "Don't assume a transaction is safe once the code completes. If the database crashes before the log is flushed, the transaction reverts to Aborted.",
        "trick": "Partially Committed = checkout screen. Committed = receiving your payment receipt."
    },
    {
        "id": "db-concurrency",
        "num": "09",
        "chapter": "Concurrency & Isolation",
        "title": "Concurrency Anomalies",
        "subtitle": "Analyzing dirty reads, non-repeatable reads, and phantom reads.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Anomaly Definitions</div>
  <p><strong>Dirty Read:</strong> Reading uncommitted data from another transaction that later aborts.</p>
  <p><strong>Non-Repeatable Read:</strong> Reading the same row twice within a transaction and getting different values because another transaction updated it.</p>
  <p><strong>Phantom Read:</strong> Re-executing a query with a range search and discovering new 'phantom' rows inserted by another transaction.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is a Phantom Read, and how does it differ from a Non-Repeatable Read?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Range Query</span>
    <span class="buzz-tag">Row Modification</span>
    <span class="buzz-tag">Insert / Delete</span>
    <span class="buzz-tag">Predicate Locking</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A non-repeatable read occurs when an existing row's data is updated (a modification anomaly). A phantom read occurs when new rows are inserted or deleted within a queried range (a structural anomaly), violating range-query consistency."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a lost update anomaly?"</p>
  <p class="followup-a">When two transactions read the same value, modify it concurrently, and write back, with the second write overwriting the first change without incorporating it.</p>
</div>
""",
        "trap": "Don't assume all databases run in Serializable mode by default. Most default to Read Committed to prevent slow transactions.",
        "trick": "Dirty = reading garbage. Non-Repeatable = values change under you. Phantom = new ghost rows appear."
    },
    {
        "id": "db-serial",
        "num": "10",
        "chapter": "Concurrency & Isolation",
        "title": "Conflict & View Serializability",
        "subtitle": "Evaluating if concurrent execution schedules match sequential execution.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Conflict Criteria</div>
  <p>Two operations conflict if they belong to different transactions, target the same item, and at least one is a Write.</p>
  <p><strong>Conflict Serializability:</strong> A schedule is conflict serializable if it can be transformed into a serial schedule by swapping non-conflicting operations.</p>
  <p><strong>View Serializability:</strong> Stricter, focuses on final state and initial reads. All conflict serializable schedules are view serializable, but not vice versa.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How do you test a database schedule for Conflict Serializability?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Precedence Graph</span>
    <span class="buzz-tag">Cycle Detection</span>
    <span class="buzz-tag">Topological Sort</span>
    <span class="buzz-tag">Active Read/Write</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Create a Precedence Graph where transactions are nodes. Draw a directed edge from Ti to Tj if Ti performs an operation that conflicts with Tj's later operation. If the graph contains no cycles, the schedule is conflict serializable."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a blind write?"</p>
  <p class="followup-a">A write operation performed by a transaction on an item without reading it first. Blind writes allow a schedule to be view serializable without being conflict serializable.</p>
</div>
""",
        "trap": "Don't confuse scheduling with execution speed. Serializability ensures safety, not speed; serial schedules are highly inefficient in production.",
        "trick": "Draw nodes for transactions. Connect conflicts. If a cycle forms, you have a collision."
    },
    {
        "id": "db-isolation-levels",
        "num": "11",
        "chapter": "Concurrency & Isolation",
        "title": "Transaction Isolation Levels",
        "subtitle": "Tuning safety vs performance inside ACID database engines.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Isolation Options</div>
  <p>Defines how changes made by one transaction are visible to others. Enforces SQL-92 standards.</p>
</div>
<div class="concept-visual">
  <table class="visual-table contrast-table" style="font-size:7pt;">
    <thead>
      <tr>
        <th>Level</th>
        <th>Dirty Read</th>
        <th>Non-Rep.</th>
        <th>Phantom</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Read Uncomm.</td><td>Allowed</td><td>Allowed</td><td>Allowed</td></tr>
      <tr><td>Read Comm.</td><td>Prevented</td><td>Allowed</td><td>Allowed</td></tr>
      <tr><td>Repeatable</td><td>Prevented</td><td>Prevented</td><td>Allowed</td></tr>
      <tr><td>Serializable</td><td>Prevented</td><td>Prevented</td><td>Prevented</td></tr>
    </tbody>
  </table>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Explain the trade-offs of the 'Serializable' isolation level compared to 'Read Committed'."</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Locking Overhead</span>
    <span class="buzz-tag">Query Throughput</span>
    <span class="buzz-tag">Concurrency Control</span>
    <span class="buzz-tag">Optimistic Locking</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Read Committed prevents dirty reads but allows non-repeatable reads, maximizing speed with minimal locks. Serializable guarantees complete isolation (preventing all anomalies) but introduces massive locking overhead, increasing transaction aborts and bottlenecks."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"How is Repeatable Read implemented?"</p>
  <p class="followup-a">Typically using MVCC (Multi-Version Concurrency Control), where read queries access a static snapshot of the database taken when the transaction started.</p>
</div>
""",
        "trap": "Don't say Serializable runs transactions strictly one after the other. Modern databases run queries concurrently, aborting transactions only if conflict tests fail.",
        "trick": "Higher isolation = more locks, slower throughput, maximum consistency safety."
    },
    {
        "id": "db-2pl",
        "num": "12",
        "chapter": "Concurrency & Isolation",
        "title": "2-Phase Locking (2PL)",
        "subtitle": "A lock acquisition protocol ensuring conflict serializability.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Locking Phases</div>
  <p><strong>Growing Phase:</strong> Transaction acquires locks but cannot release any.</p>
  <p><strong>Shrinking Phase:</strong> Transaction releases locks but cannot acquire new ones.</p>
  <p><strong>Strict 2PL:</strong> Releasing exclusive (write) locks is delayed until the transaction commits or aborts, preventing cascading rollbacks.</p>
</div>
<div class="concept-visual">
  <div style="font-family:monospace; font-size:7.5pt; border:1px solid #CBD5E0; padding:10px; background:white; text-align:center;">
    Lock Count<br>
    ▲ &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;[Lock Point]<br>
    │ &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; / &nbsp; &nbsp; \\<br>
    │ &nbsp; &nbsp;Growing &nbsp;/ &nbsp; &nbsp; &nbsp; \\ &nbsp;Shrinking<br>
    └─────────────────────────────► Time
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How does 2PL guarantee Conflict Serializability, and why is Strict 2PL preferred?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Lock Point</span>
    <span class="buzz-tag">Cascading Rollback</span>
    <span class="buzz-tag">Exclusive Lock</span>
    <span class="buzz-tag">Growing/Shrinking</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"2PL ensures conflict serializability by preventing transactions from releasing a lock and acquiring a new one later, serializing transactions based on their Lock Point. Strict 2PL goes further by holding write locks until commit, preventing dirty reads and cascading rollbacks."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"Does 2PL prevent deadlocks?"</p>
  <p class="followup-a">No. 2PL can easily lead to deadlocks if two transactions acquire locks in opposing order (e.g., T1 locks A, waits for B; T2 locks B, waits for A).</p>
</div>
""",
        "trap": "Don't say 2PL is used in every relational database. Many modern engines use MVCC to avoid read locks entirely, using 2PL only for write operations.",
        "trick": "Once you release a lock, you cannot ask for another. Acquire all keys first, then unlock."
    },
    {
        "id": "db-deadlock",
        "num": "13",
        "chapter": "Concurrency & Isolation",
        "title": "DBMS Deadlocks",
        "subtitle": "Handling circular lock dependencies inside transaction loops.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Deadlock Management</div>
  <p><strong>Prevention:</strong> Use lock ordering or timestamps (Wait-Die, Wound-Wait).</p>
  <p><strong>Detection:</strong> Maintain a Wait-For Graph (WFG) and scan for cycles periodically.</p>
  <p><strong>Recovery:</strong> Select a victim transaction (based on cost, age, or changes), abort it, and rollback its modifications.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Compare the 'Wait-Die' and 'Wound-Wait' deadlock prevention schemes."</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Transaction Timestamp</span>
    <span class="buzz-tag">Preemption</span>
    <span class="buzz-tag">Wound (Abort)</span>
    <span class="buzz-tag">Die (Revert)</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Both schemes use transaction timestamps (older = higher priority). In **Wait-Die** (non-preemptive): if an older transaction needs a resource held by a younger one, it waits; if a younger needs from older, it dies. In **Wound-Wait** (preemptive): older wounds/aborts the younger; younger waits for older."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"Which is better: Wound-Wait or Wait-Die?"</p>
  <p class="followup-a">Wound-Wait is generally more efficient because older transactions preemptively abort younger ones, minimizing idle waiting times.</p>
</div>
""",
        "trap": "Don't say you can avoid deadlocks entirely in high-concurrency systems. Deadlocks are normal; databases are designed to catch and retry aborted transactions.",
        "trick": "Wait-Die = Older waits, younger dies. Wound-Wait = Older wounds, younger waits."
    },
    {
        "id": "db-indexing",
        "num": "14",
        "chapter": "Storage & Indexing",
        "title": "B-Tree vs B+ Tree",
        "subtitle": "Balanced search trees optimized for secondary storage blocks.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Structure Rules</div>
  <p><strong>B-Tree:</strong> Stores keys, data pointers, and child pointers in both internal and leaf nodes.</p>
  <p><strong>B+ Tree:</strong> Stores keys and data pointers **only in leaf nodes**; internal nodes only store routing keys. Leaf nodes are linked sequentially.</p>
</div>
<div class="concept-visual">
  <div style="border:1px solid #CBD5E0; border-radius:6px; padding:10px; background:white; font-size:7.5pt; width:100%; text-align:center;">
    <strong>B+ Tree Leaf Node Chain</strong><br>
    [Leaf 1] ──&gt; [Leaf 2] ──&gt; [Leaf 3]<br>
    (Enables O(1) range scans along leaf links)
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why are B+ Trees preferred over B-Trees for database indexing?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Internal Node Capacity</span>
    <span class="buzz-tag">Fan-out Factor</span>
    <span class="buzz-tag">Sequential Scan</span>
    <span class="buzz-tag">Disk I/O Count</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"B+ Trees store data pointers only in leaf nodes. This makes internal nodes smaller, allowing them to fit more keys per disk block (a higher Fan-out Factor) and reducing tree height (fewer disk reads). Additionally, linked leaf nodes enable fast O(N) range queries."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a clustered index?"</p>
  <p class="followup-a">An index that dictates the physical storage order of rows on disk. A table can have only one clustered index (typically on the Primary Key).</p>
</div>
""",
        "trap": "Don't suggest binary search trees for database indexing. Disk lookups are slow; B+ trees use broad child pointers to minimize tree depth and disk I/O.",
        "trick": "B+ Tree has the '+' sign for the linked leaf chain at the bottom."
    },
    {
        "id": "db-hashing",
        "num": "15",
        "chapter": "Storage & Indexing",
        "title": "Static vs Dynamic Hashing",
        "subtitle": "Handling bucket overflow in database hash index files.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Hashing Mechanics</div>
  <p><strong>Static Hashing:</strong> Maps keys to a fixed number of buckets. Overflow is handled using overflow chains (linked lists). Performance degrades over time.</p>
  <p><strong>Extendible (Dynamic) Hashing:</strong> Uses a directory of bucket pointers. Buckets split dynamically, adjusting directory depth as data grows.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How does Extendible Hashing handle bucket overflow without rehashing all keys?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Global Depth</span>
    <span class="buzz-tag">Local Depth</span>
    <span class="buzz-tag">Directory Doubling</span>
    <span class="buzz-tag">Bucket Split</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Extendible hashing uses a directory of bucket pointers. Each bucket has a Local Depth, and the directory has a Global Depth. When a bucket overflows, only that bucket splits. If its local depth equals the global depth, the directory doubles in size, keeping other buckets untouched."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"When is hash indexing preferred over B+ Tree indexing?"</p>
  <p class="followup-a">For point lookups (e.g. `WHERE ID = 5`), which hash indexes resolve in O(1) time. However, they do not support range queries.</p>
</div>
""",
        "trap": "Don't use hash indexes if your application performs range queries (e.g. `WHERE age > 21`), as hash lookups are unordered.",
        "trick": "Static = fixed slots (overflows crawl). Dynamic = directory doubles to fit new entries."
    },
    {
        "id": "db-relational-algebra",
        "num": "16",
        "chapter": "Query Languages & Algebra",
        "title": "Relational Algebra",
        "subtitle": "The formal procedural language defining relational operations.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Formal Operators</div>
  <p><strong>Selection (σ):</strong> Filters rows based on a predicate condition (maps to SQL WHERE).</p>
  <p><strong>Projection (π):</strong> Selects specific columns, removing duplicates (maps to SQL SELECT).</p>
  <p><strong>Join (⋈):</strong> Combines tables based on a matching attribute condition.</p>
</div>
<div class="concept-visual" style="font-family:monospace; font-size:7.5pt; padding:8px; background:white; border:1px solid #CBD5E0; border-radius:6px; text-align:center;">
  σ_age &gt; 21 (π_name, age (Users))<br>
  (Filters rows after projecting columns)
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is the difference between Relational Algebra and Relational Calculus?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Procedural Language</span>
    <span class="buzz-tag">Non-Procedural / Decl.</span>
    <span class="buzz-tag">Tuple Calculus</span>
    <span class="buzz-tag">Operator Flow</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Relational Algebra is procedural: it defines the step-by-step operators (Selection, Projection) used to retrieve data. Relational Calculus is non-procedural (declarative): it describes WHAT data to retrieve without specifying how to fetch it, similar to user-level SQL queries."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is the Cartesian Product (x) operator?"</p>
  <p class="followup-a">An operator combining all rows of Table A with all rows of Table B, producing A × B total rows. Forms the mathematical basis for JOIN operations.</p>
</div>
""",
        "trap": "Don't forget that projection (π) in relational algebra removes duplicates by default, unlike SQL SELECT which requires SELECT DISTINCT.",
        "trick": "σ (sigma) = Selection (rows). π (pi) = Projection (columns)."
    },
    {
        "id": "db-joins",
        "num": "17",
        "chapter": "Query Languages & Algebra",
        "title": "SQL Joins",
        "subtitle": "Combining rows from two or more tables based on matching columns.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Join Taxonomy</div>
  <p><strong>INNER:</strong> Returns matching rows from both tables.<br>
  <strong>LEFT:</strong> Returns all rows from the left table + matched rows from the right.<br>
  <strong>FULL:</strong> Returns all rows from both tables, filling mismatches with NULLs.</p>
</div>
<div class="concept-visual">
  <div style="display:flex; justify-content:space-between; font-size:7.5pt; gap:10px; width:100%;">
    <div style="flex:1; border:1px solid #3182CE; padding:6px; background:#EBF8FF; border-radius:4px; text-align:center;">
      <strong>INNER</strong><br>
      A ∩ B<br>
      Only matches
    </div>
    <div style="flex:1; border:1px solid #38A169; padding:6px; background:#F0FFF4; border-radius:4px; text-align:center;">
      <strong>LEFT</strong><br>
      A + (A ∩ B)<br>
      Keep Left
    </div>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What happens when you run an INNER JOIN on columns containing NULL values?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Three-Valued Logic</span>
    <span class="buzz-tag">NULL Evaluation</span>
    <span class="buzz-tag">Unknown Match</span>
    <span class="buzz-tag">Row Exclusion</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"In SQL, NULL is evaluated as Unknown rather than a value. The comparison `NULL = NULL` evaluates to Unknown, not True. Therefore, an INNER JOIN excludes rows with NULL values in the join columns because they fail the predicate comparison."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a Self Join?"</p>
  <p class="followup-a">A join where a table is joined with itself by using alias names (e.g. matching employees to their managers in the same Employee table).</p>
</div>
""",
        "trap": "Don't confuse FULL OUTER JOIN with CROSS JOIN. FULL OUTER matches rows and fills gaps with NULLs. CROSS JOIN is a Cartesian product (A × B rows) with no matching condition.",
        "trick": "Inner = matches only. Left = keep left side anyway. Full = keep both sides anyway."
    },
    {
        "id": "db-subqueries",
        "num": "18",
        "chapter": "SQL Operations",
        "title": "Subqueries & Correlated",
        "subtitle": "Nested subqueries vs loops evaluated per outer row.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Nested Queries</div>
  <p><strong>Subquery:</strong> A nested query executed once, with its output used by the outer query.</p>
  <p><strong>Correlated Subquery:</strong> A nested query referencing columns from the outer query. It is evaluated once for every row processed by the outer query, acting like a nested loop.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why are Correlated Subqueries slow, and how can they be optimized?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Row-by-row Loop</span>
    <span class="buzz-tag">Query Planner</span>
    <span class="buzz-tag">JOIN Conversion</span>
    <span class="buzz-tag">EXISTS vs IN</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Correlated subqueries execute row-by-row, running the inner query once for each row in the outer query (O(N^2) complexity). They can be optimized by rewriting them using JOINs or subqueries in the FROM clause, allowing the optimizer to process them as a single bulk operation."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"When is EXISTS preferred over IN?"</p>
  <p class="followup-a">`EXISTS` stops scanning as soon as it finds a single match, making it faster than `IN` for large tables where the subquery returns many rows.</p>
</div>
""",
        "trap": "Don't assume subqueries are always slow. Modern query optimizers often rewrite simple subqueries as JOINs automatically.",
        "trick": "Simple = run once, reuse result. Correlated = run for every row in the outer table."
    },
    {
        "id": "db-views",
        "num": "19",
        "chapter": "SQL Operations",
        "title": "Views vs Materialized Views",
        "subtitle": "Virtual queries vs physically cached query tables.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Virtualization Layers</div>
  <p><strong>Standard View:</strong> A saved SQL query. Virtual only; it stores no physical data and runs the query each time it is accessed.</p>
  <p><strong>Materialized View:</strong> A physical table storing the query results on disk. Must be refreshed when underlying data changes.</p>
</div>
<div class="concept-visual">
  <table class="visual-table contrast-table" style="font-size:7.5pt;">
    <thead>
      <tr>
        <th>Metric</th>
        <th>Standard View</th>
        <th>Materialized View</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Storage</td><td>None (Saved Query)</td><td>Disk Storage</td></tr>
      <tr><td>Execution</td><td>Runs on every access</td><td>Reads cached disk data</td></tr>
      <tr><td>Latency</td><td>High (computed live)</td><td>Low (read direct)</td></tr>
      <tr><td>Data Freshness</td><td>Real-time</td><td>Requires Refresh</td></tr>
    </tbody>
  </table>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"When would you choose a Materialized View over a Standard View?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Analytical Cache</span>
    <span class="buzz-tag">Complex JOIN Query</span>
    <span class="buzz-tag">Refresh Policy</span>
    <span class="buzz-tag">Read Performance</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Materialized views are preferred for expensive aggregation or JOIN queries on large datasets where real-time accuracy is not required (e.g. daily dashboards). Reading the pre-computed disk cache is much faster than running the query live."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is incremental refresh in materialized views?"</p>
  <p class="followup-a">A refresh strategy that applies only the changes (inserts/updates) made since the last refresh, avoiding rebuilding the view from scratch.</p>
</div>
""",
        "trap": "Don't use materialized views for write-heavy tables with real-time read requirements; the refresh overhead will degrade performance.",
        "trick": "Standard View = a shortcut link. Materialized View = downloading the file to your desktop."
    },
    {
        "id": "db-triggers",
        "num": "20",
        "chapter": "SQL Operations",
        "title": "Triggers & Stored Procs",
        "subtitle": "Automating database events and encapsulating business logic.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Active Database Objects</div>
  <p><strong>Trigger:</strong> An automated block executed in response to a database event (INSERT, UPDATE, DELETE).</p>
  <p><strong>Stored Procedure:</strong> Pre-compiled SQL code saved in the database, called explicitly to execute business logic.</p>
</div>
<div class="concept-visual" style="font-size:7pt; font-family:monospace; background:#FAFAFA; border:1px solid #CBD5E0; padding:10px;">
  <strong>Trigger Event hook example:</strong><br>
  CREATE TRIGGER check_inventory<br>
  BEFORE UPDATE ON orders<br>
  FOR EACH ROW EXECUTE FUNCTION verify();
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What are the disadvantages of relying heavily on database Triggers for business logic?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Hidden Execution</span>
    <span class="buzz-tag">Debugging Complexity</span>
    <span class="buzz-tag">Performance Overhead</span>
    <span class="buzz-tag">Cascade Execution</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Heavy use of triggers hides execution logic from developers, making debugging difficult. Additionally, cascading triggers (where one trigger fires another) increase write latency and can lead to infinite loops or connection pool exhaustion."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is the difference between a Stored Procedure and a Function?"</p>
  <p class="followup-a">Procedures cannot be called within SELECT queries and support transaction control (COMMIT/ROLLBACK). Functions must return a value and cannot manage transactions.</p>
</div>
""",
        "trap": "Don't state that triggers are fast. While they run inside the database, they add overhead to every write operation.",
        "trick": "Trigger = smoke detector (alarm goes off automatically). Procedure = calling the fire department manually."
    },
    {
        "id": "db-recovery",
        "num": "21",
        "chapter": "Transaction Management",
        "title": "Database Recovery",
        "subtitle": "Restoring databases to a consistent state after system failures.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Recovery Paradigms</div>
  <p><strong>Log-Based Recovery:</strong> Replays logs (WAL) bottom-up, executing REDO and UNDO passes. Assures Durability.</p>
  <p><strong>Shadow Paging:</strong> Maintaining two page tables (active and shadow). Writing changes to new pages on disk, updating the active table pointer on commit.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Explain the difference between Shadow Paging and Log-Based Recovery."</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Shadow Page Table</span>
    <span class="buzz-tag">Log File Overhead</span>
    <span class="buzz-tag">Pointer Swap Commit</span>
    <span class="buzz-tag">No REDO / UNDO log</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Log-based recovery uses append-only logs on disk, requiring REDO/UNDO passes on restart. Shadow paging writes changes to new disk blocks and swaps a pointer to commit. It needs no logs or recovery passes, but causes disk fragmentation."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is the ARIES recovery algorithm?"</p>
  <p class="followup-a">A popular log-based recovery algorithm with three phases: Analysis (finding active transactions), Redo (replaying all changes), and Undo (rolling back uncommitted changes).</p>
</div>
""",
        "trap": "Don't say shadow paging is standard. Modern relational databases (PostgreSQL, Oracle) use log-based WAL recovery due to better write performance.",
        "trick": "Log-based = replaying history. Shadow Paging = editing a copy of a file and swapping the filenames on commit."
    },
    {
        "id": "db-constraints",
        "num": "22",
        "chapter": "Relational Model Core",
        "title": "SQL Constraints",
        "subtitle": "Enforcing data integrity rules at the schema level.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Constraint Types</div>
  <p>Constraints restrict the data values that can be inserted into tables, enforcing business logic at the database level.</p>
  <p><strong>UNIQUE:</strong> Enforces distinct values across rows (creates a B+ tree index automatically).</p>
  <p><strong>CHECK:</strong> Validates row values against a Boolean expression (e.g. `CHECK (age >= 18)`).</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How does a UNIQUE constraint differ from a Primary Key constraint?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Multiple Unique Keys</span>
    <span class="buzz-tag">NULL Support</span>
    <span class="buzz-tag">Clustered Index PK</span>
    <span class="buzz-tag">Non-Clustered Unique</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A table can have only one Primary Key, which cannot contain NULLs and typically creates a clustered index. UNIQUE constraints allow multiple columns to be marked unique, support NULL values, and create non-clustered indexes."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a composite check constraint?"</p>
  <p class="followup-a">A CHECK constraint referencing multiple columns (e.g. `CHECK (sale_price < original_price)`), validating relationships between fields in the same row.</p>
</div>
""",
        "trap": "Don't assume a UNIQUE column cannot contain NULLs. In most databases, UNIQUE columns can contain multiple NULL values, as NULL is not equal to itself.",
        "trick": "Constraints are the structural walls of your database, preventing bad data from entering."
    },
    {
        "id": "db-nosql-cap",
        "num": "23",
        "chapter": "Advanced DBMS Concepts",
        "title": "NoSQL vs SQL & CAP",
        "subtitle": "Relational storage vs horizontal scale-out architectures.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">CAP Theorem</div>
  <p>In a distributed data store, you can guarantee at most two of: <strong>Consistency</strong> (all nodes see same data), <strong>Availability</strong> (every read succeeds), and <strong>Partition Tolerance</strong> (survives node drops).</p>
</div>
<div class="concept-visual">
  <table class="visual-table contrast-table" style="font-size:7.5pt;">
    <thead>
      <tr>
        <th>Metric</th>
        <th>SQL Databases</th>
        <th>NoSQL Databases</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Schema</td><td>Strict, Structured</td><td>Dynamic Schema</td></tr>
      <tr><td>Scale</td><td>Vertical (bigger server)</td><td>Horizontal (more nodes)</td></tr>
      <tr><td>Transaction</td><td>ACID compliant</td><td>BASE (Eventually consistent)</td></tr>
      <tr><td>CAP Model</td><td>Typically CA</td><td>Typically AP or CP</td></tr>
    </tbody>
  </table>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why does the CAP Theorem force distributed databases to choose between Consistency and Availability?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Network Partition</span>
    <span class="buzz-tag">Sync Replication</span>
    <span class="buzz-tag">Stale Read Reject</span>
    <span class="buzz-tag">Eventually Consistent</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Network partitions (lost connections between nodes) are inevitable. If a partition occurs, the database must choose: either reject writes on isolated nodes to maintain Consistency (CP), or accept writes on all nodes, sacrificing Consistency for Availability (AP)."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What are BASE properties in NoSQL?"</p>
  <p class="followup-a">Basic Availability, Soft-state, and Eventual consistency. Replaces strict ACID guarantees to support horizontal scale.</p>
</div>
""",
        "trap": "Don't say SQL databases cannot scale. They can, but scaling horizontally requires complex replication and sharding setups.",
        "trick": "SQL is a single bank vault (perfect consistency). NoSQL is distributed cash drawers (fast transactions, audited later)."
    },
    {
        "id": "db-sharding",
        "num": "24",
        "chapter": "Advanced DBMS Concepts",
        "title": "Sharding & Replication",
        "subtitle": "Distributing database workloads across multiple servers.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Scale-Out Strategies</div>
  <p><strong>Replication:</strong> Copying the database across multiple servers. Master handles writes; replicas handle read queries (improves read capacity).</p>
  <p><strong>Sharding:</strong> Horizontal partitioning. Splitting a single table's rows across different database nodes based on a Shard Key (improves write capacity).</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How does Sharding differ from Replication, and when is each chosen?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Read Heavy Replication</span>
    <span class="buzz-tag">Write Bottleneck Shard</span>
    <span class="buzz-tag">Partitioning Key</span>
    <span class="buzz-tag">Shared Nothing</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Replication copies the entire database to multiple servers, optimizing read performance but keeping write bottlenecks on the master node. Sharding splits table rows across separate servers based on a shard key, dividing both read and write workloads across nodes."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a hot shard?"</p>
  <p class="followup-a">A shard receiving disproportionately high traffic due to a poor shard key choice (e.g. sharding by date, causing all recent writes to hit the same node).</p>
</div>
""",
        "trap": "Don't suggest sharding unless database writes exceed a single server's hardware limits; it adds massive application complexity.",
        "trick": "Replication = copying a book for multiple readers. Sharding = splitting a massive directory into letters A-M and N-Z."
    },
    
    # ─────────────────────────────────────────
    # 6 SQL PRACTICE PAGES (25 to 30)
    # ─────────────────────────────────────────
    {
        "id": "sql-prac-nth-salary",
        "num": "25",
        "chapter": "SQL Practice Pages",
        "title": "SQL: Nth Highest Salary",
        "subtitle": "Finding the Nth highest salary in an Employee table.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">SQL Query Code</div>
  <div style="background:#1A202C; color:#E2E8F0; padding:10px; border-radius:6px; font-family:monospace; font-size:7.5pt; line-height:1.35;">
SELECT DISTINCT Salary <br>
FROM Employee <br>
ORDER BY Salary DESC <br>
LIMIT 1 OFFSET N-1;
  </div>
</div>
<div class="box box-industry" style="margin-top:10px;">
  <div class="box-title">Alternative CTE Method (DENSE_RANK)</div>
  <div style="background:#1A202C; color:#E2E8F0; padding:8px; border-radius:6px; font-family:monospace; font-size:7pt; line-height:1.3;">
WITH RankedSalaries AS (<br>
&nbsp;&nbsp;SELECT Salary, DENSE_RANK() <br>
&nbsp;&nbsp;OVER (ORDER BY Salary DESC) as rk<br>
&nbsp;&nbsp;FROM Employee<br>
)<br>
SELECT Salary FROM RankedSalaries WHERE rk = N LIMIT 1;
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why is DENSE_RANK() preferred over ROW_NUMBER() for the Nth highest salary query?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Duplicate Salaries</span>
    <span class="buzz-tag">Dense vs Gap</span>
    <span class="buzz-tag">Ranking Window</span>
    <span class="buzz-tag">Analytical Query</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"ROW_NUMBER() assigns sequential integers to rows without handling duplicates, meaning duplicate highest salaries will take up ranks 1 and 2. DENSE_RANK() assigns the same rank to identical salaries without leaving gaps in the ranking order, ensuring accurate results."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is the difference between RANK() and DENSE_RANK()?"</p>
  <p class="followup-a">`RANK()` leaves gaps after duplicate values (e.g. 1, 2, 2, 4). `DENSE_RANK()` does not leave gaps (e.g. 1, 2, 2, 3).</p>
</div>
""",
        "trap": "Don't use `LIMIT 1 OFFSET N` without subtracting 1; OFFSET is 0-indexed, so the 2nd highest salary requires `OFFSET 1`.",
        "trick": "DENSE_RANK doesn't skip ranks; it keeps the numbering dense."
    },
    {
        "id": "sql-prac-duplicate-emails",
        "num": "26",
        "chapter": "SQL Practice Pages",
        "title": "SQL: Duplicate Emails",
        "subtitle": "Finding duplicate email records inside a Person table.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">SQL Query Code</div>
  <div style="background:#1A202C; color:#E2E8F0; padding:10px; border-radius:6px; font-family:monospace; font-size:8pt; line-height:1.4;">
SELECT Email<br>
FROM Person<br>
GROUP BY Email<br>
HAVING COUNT(Email) &gt; 1;
  </div>
</div>
<div class="box box-industry" style="margin-top:10px;">
  <div class="box-title">Self-Join Deletion Method</div>
  <div style="background:#1A202C; color:#E2E8F0; padding:8px; border-radius:6px; font-family:monospace; font-size:7pt; line-height:1.3;">
DELETE p1 FROM Person p1, Person p2<br>
WHERE p1.Email = p2.Email AND p1.Id &gt; p2.Id;<br>
(Deletes duplicate rows, keeping the smallest ID)
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Explain the difference between WHERE and HAVING clauses. Can we use aggregate functions in WHERE?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Row Filter (WHERE)</span>
    <span class="buzz-tag">Group Filter (HAVING)</span>
    <span class="buzz-tag">Aggregate Condition</span>
    <span class="buzz-tag">Execution Order</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"The WHERE clause filters rows before they are grouped (GROUP BY). The HAVING clause filters grouped rows after aggregation. Aggregate functions (like `COUNT()`) cannot be used in WHERE because it runs before grouping occurs."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is the query execution order in SQL?"</p>
  <p class="followup-a">FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT.</p>
</div>
""",
        "trap": "Don't use HAVING without a GROUP BY clause, as it will evaluate the entire table as a single group, which is often not what you want.",
        "trick": "WHERE filters individual rows. HAVING filters grouped blocks."
    },
    {
        "id": "sql-prac-consec-nums",
        "num": "27",
        "chapter": "SQL Practice Pages",
        "title": "SQL: Consecutive Numbers",
        "subtitle": "Finding numbers that appear at least three times consecutively.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">SQL Query Code</div>
  <div style="background:#1A202C; color:#E2E8F0; padding:10px; border-radius:6px; font-family:monospace; font-size:7.5pt; line-height:1.35;">
SELECT DISTINCT l1.Num as ConsecutiveNums<br>
FROM Logs l1, Logs l2, Logs l3<br>
WHERE l1.Id = l2.Id - 1 <br>
&nbsp;&nbsp;AND l2.Id = l3.Id - 1<br>
&nbsp;&nbsp;AND l1.Num = l2.Num <br>
&nbsp;&nbsp;AND l2.Num = l3.Num;
  </div>
</div>
<div class="box box-industry" style="margin-top:10px;">
  <div class="box-title">Optimization: LEAD / LAG window functions</div>
  <div style="background:#1A202C; color:#E2E8F0; padding:8px; border-radius:6px; font-family:monospace; font-size:7.0pt; line-height:1.25;">
SELECT DISTINCT Num FROM (<br>
&nbsp;&nbsp;SELECT Num, <br>
&nbsp;&nbsp;LEAD(Num, 1) OVER (ORDER BY Id) as next1,<br>
&nbsp;&nbsp;LEAD(Num, 2) OVER (ORDER BY Id) as next2<br>
&nbsp;&nbsp;FROM Logs<br>
) t WHERE Num = next1 AND next1 = next2;
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why are window functions (LEAD/LAG) preferred over self-joins for consecutive number queries?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Self-Join Overhead</span>
    <span class="buzz-tag">Index Scan Loop</span>
    <span class="buzz-tag">Window Frame Partition</span>
    <span class="buzz-tag">Single Pass Scan</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Self-joins force the database to scan and join the logs table three times (O(N^3) complexity without indexes). Window functions (LEAD/LAG) run in a single sequential pass over the sorted rows (O(N log N)), reducing disk reads."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is the difference between LEAD and LAG?"</p>
  <p class="followup-a">`LEAD` accesses data from subsequent rows. `LAG` accesses data from preceding rows within the same window frame.</p>
</div>
""",
        "trap": "Don't assume ID values are sequential without gaps. If IDs have gaps, use `ROW_NUMBER() OVER (ORDER BY Id)` to establish sequential row indexing first.",
        "trick": "LEAD peeks forward. LAG peeks backward."
    },
    {
        "id": "sql-prac-dep-top-sal",
        "num": "28",
        "chapter": "SQL Practice Pages",
        "title": "SQL: Department Top Salaries",
        "subtitle": "Finding employees with the highest salaries in each department.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">SQL Query Code</div>
  <div style="background:#1A202C; color:#E2E8F0; padding:10px; border-radius:6px; font-family:monospace; font-size:7.5pt; line-height:1.35;">
SELECT d.Name as Department, <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;e1.Name as Employee, <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;e1.Salary<br>
FROM Employee e1<br>
JOIN Department d ON e1.DepartmentId = d.Id<br>
WHERE e1.Salary = (<br>
&nbsp;&nbsp;SELECT MAX(Salary) FROM Employee e2<br>
&nbsp;&nbsp;WHERE e2.DepartmentId = e1.DepartmentId<br>
);
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is the difference between DENSE_RANK() and MAX() subqueries for department top salaries?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Window Partitioning</span>
    <span class="buzz-tag">Correlated Subquery</span>
    <span class="buzz-tag">Dense Rank Tie</span>
    <span class="buzz-tag">Execution Speed</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A MAX() correlated subquery runs row-by-row, which is slow. Using `DENSE_RANK() OVER (PARTITION BY DepartmentId ORDER BY Salary DESC)` partitions the data and ranks salaries in a single pass. Both handle ties correctly by returning all top-paid employees."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is the PARTITION BY clause?"</p>
  <p class="followup-a">A window clause that groups rows into partitions before applying the window function (e.g. ranking salaries independently within each department).</p>
</div>
""",
        "trap": "Don't use `ROW_NUMBER()` if multiple employees share the top salary; it will randomly choose only one instead of returning all of them.",
        "trick": "PARTITION BY is like GROUP BY, but it does not collapse rows."
    },
    {
        "id": "sql-prac-exchange-seats",
        "num": "29",
        "chapter": "SQL Practice Pages",
        "title": "SQL: Exchange Seats",
        "subtitle": "Swapping adjacent seat IDs for consecutive students.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">SQL Query Code</div>
  <div style="background:#1A202C; color:#E2E8F0; padding:10px; border-radius:6px; font-family:monospace; font-size:7.2pt; line-height:1.35;">
SELECT <br>
&nbsp;&nbsp;CASE <br>
&nbsp;&nbsp;&nbsp;&nbsp;WHEN id % 2 = 1 AND id = (SELECT MAX(id) FROM Seat) <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;THEN id<br>
&nbsp;&nbsp;&nbsp;&nbsp;WHEN id % 2 = 1 <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;THEN id + 1<br>
&nbsp;&nbsp;&nbsp;&nbsp;ELSE id - 1<br>
&nbsp;&nbsp;END as id, student<br>
FROM Seat<br>
ORDER BY id;
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Explain how the CASE statement handles the final odd seat ID in this query."</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Max boundary Check</span>
    <span class="buzz-tag">Modulo Odd Check</span>
    <span class="buzz-tag">Sequence Order</span>
    <span class="buzz-tag">Case Evaluation</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"The first WHEN condition checks if the seat ID is odd and matches the maximum ID in the table. If true, the ID is left unchanged to prevent it from swapping to a non-existent higher seat. Other odd IDs are incremented, and even IDs are decremented."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a COALESCE function?"</p>
  <p class="followup-a">A function returning the first non-NULL value in its argument list. Used to handle empty or fallback values in queries.</p>
</div>
""",
        "trap": "Don't forget to include the final `ORDER BY id` clause; swapping IDs without sorting the output will return rows in incorrect order.",
        "trick": "Even becomes odd (subtract 1). Odd becomes even (add 1). Leave the final odd seat alone."
    },
    {
        "id": "sql-prac-cancel-rate",
        "num": "30",
        "chapter": "SQL Practice Pages",
        "title": "SQL: Cancellation Rate",
        "subtitle": "Calculating trip cancellation rates for unbanned users.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">SQL Query Code</div>
  <div style="background:#1A202C; color:#E2E8F0; padding:8px; border-radius:6px; font-family:monospace; font-size:7pt; line-height:1.3;">
SELECT Request_at as Day, <br>
&nbsp;&nbsp;ROUND(SUM(CASE WHEN Status != 'completed' THEN 1 ELSE 0 END) <br>
&nbsp;&nbsp;/ COUNT(*), 2) as "Cancellation Rate"<br>
FROM Trips t<br>
WHERE Client_Id NOT IN (SELECT Users_Id FROM Users WHERE Banned = 'Yes')<br>
&nbsp;&nbsp;AND Driver_Id NOT IN (SELECT Users_Id FROM Users WHERE Banned = 'Yes')<br>
&nbsp;&nbsp;AND Request_at BETWEEN '2013-10-01' AND '2013-10-03'<br>
GROUP BY Request_at;
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How does the SUM(CASE) construction calculate the cancellation rate in a single scan?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Conditional Aggregation</span>
    <span class="buzz-tag">Subquery Filtering</span>
    <span class="buzz-tag">Ratio Rounding</span>
    <span class="buzz-tag">Single Pass Scan</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"The `CASE` statement returns 1 if the trip status is cancelled (by client or driver) and 0 if completed. `SUM()` totals these 1s to get the count of cancelled trips. Dividing this by `COUNT(*)` (total trips) yields the cancellation rate in a single scan."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"Why are NOT IN subqueries dangerous here?"</p>
  <p class="followup-a">If the subquery returns even a single NULL value, the `NOT IN` condition will evaluate to Unknown, and the query will return zero rows. Using `NOT EXISTS` is safer.</p>
</div>
""",
        "trap": "Don't count banned users. Always filter out banned clients and drivers in the WHERE clause first.",
        "trick": "SUM(CASE WHEN cancelled THEN 1 ELSE 0 END) / COUNT(*) = Cancellation Rate."
    }
]

# ─────────────────────────────────────────
# PLACEMENT BOOSTERS DICTIONARY
# ─────────────────────────────────────────
DBMS_BOOSTERS = {
    "db-3tier": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Explain that the 3-tier architecture separates physical storage, logical business rules, and application UI. This ensures data isolation so that changing database software doesn't break the frontend client."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Confusing 3-schema abstraction with 3-tier system architecture. <strong>Depth:</strong> Know the physical, conceptual, and external schema mappings.</p>
</div>
""",
    "db-indep": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Define data independence as changing schema at one level without modifying the next. Logical independence (changing conceptual schemas without changing external views) is much harder than physical independence."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking physical schema changes require rewriting SQL queries. <strong>Depth:</strong> Know how view definitions shield external user queries.</p>
</div>
""",
    "db-keys": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Explain that a candidate key is a minimal super key. Every primary key is chosen from candidate keys. Relate this directly to database integrity and index creation."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking a table can have multiple primary keys. Only one primary key is allowed, but it can be composite. <strong>Depth:</strong> Differentiate Candidate, Super, Primary, and Foreign keys.</p>
</div>
""",
    "db-normalization": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Describe normalization as a systematic design technique to eliminate redundancy and update/insert/delete anomalies by splitting tables into smaller, well-structured relations."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Believing full normalization is always best. It causes multiple table joins, which degrades read performance. <strong>Depth:</strong> Know 1NF, 2NF, and 3NF definitions.</p>
</div>
""",
    "db-advanced-nf": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Explain BCNF as a stricter version of 3NF. In BCNF, for every functional dependency X → Y, the determinant X must be a super key. BCNF does not guarantee dependency preservation."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking all 3NF tables are in BCNF. BCNF is violated when a non-key attribute determines a part of a composite key. <strong>Depth:</strong> Deconstruct composite keys.</p>
</div>
""",
    "db-er-mapping": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"ER-to-Relational mapping translates entity sets to tables. Weak entities map to tables with composite primary keys formed by their partial key and the identifying entity key."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Creating separate tables for 1:N relations instead of adding a foreign key to the 'Many' side table. <strong>Depth:</strong> Map cardinality constraints (1:1, 1:N, M:N).</p>
</div>
""",
    "db-acid-wal": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"ACID guarantees transaction integrity. Atomicity (all or nothing) and Durability (permanent write) are enforced via Write-Ahead Logging (WAL) and rollback journals."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Believing consistency is solely the database engine's job. It requires correct schema rules and user code logic. <strong>Depth:</strong> Explain shadow paging and WAL.</p>
</div>
""",
    "db-tx-states": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Trace a transaction's lifecycle: Active → Partially Committed (after the last statement executes) → Committed (after flush to log), or Failed → Aborted."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Believing 'Partially Committed' means data is saved. It just means statements finished running, but log buffer hasn't flushed. <strong>Depth:</strong> Explain states.</p>
</div>
""",
    "db-concurrency": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Concurrent execution maximizes CPU utilization. Without concurrency controls, read/write inter-leavings cause Dirty Reads, Non-Repeatable Reads, and Lost Updates."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking concurrency anomalies can only occur if the database crashes. They are scheduling order problems. <strong>Depth:</strong> Contrast reading anomalies.</p>
</div>
""",
    "db-serial": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Conflict serializability checks if a schedule is equivalent to a serial schedule by drawing a precedence graph. A cycle-free graph guarantees conflict serializability."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking view serializability is easy to compute. It is NP-complete. Conflict serializability is O(V+E) via cycle check. <strong>Depth:</strong> Draw graphs.</p>
</div>
""",
    "db-isolation-levels": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"SQL isolation levels trade speed for safety: Read Uncommitted (dirty reads allowed) → Read Committed → Repeatable Read → Serializable (full row/range locks)."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Assuming default isolation is always Serializable. Most RDBMS use Read Committed or Repeatable Read. <strong>Depth:</strong> Compare anomalies prevented at each level.</p>
</div>
""",
    "db-2pl": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Two-Phase Locking (2PL) has a growing phase (acquiring locks) and a shrinking phase (releasing locks). Strict 2PL holds write locks until commit to prevent cascading rollbacks."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Assuming basic 2PL prevents deadlocks. It only guarantees serializability. Deadlocks are still possible. <strong>Depth:</strong> Compare Basic 2PL, Strict 2PL, Rigorous 2PL.</p>
</div>
""",
    "db-deadlock": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Deadlocks occur when transactions wait in a loop. Mitigate using prevention (Wait-Die, Wound-Wait) or detection (periodically traversing the Wait-For Graph)."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Confusing Wait-Die (non-preemptive) vs Wound-Wait (preemptive). Wound-Wait is generally more efficient. <strong>Depth:</strong> Detail rollback selection strategies.</p>
</div>
""",
    "db-indexing": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Explain that B+ Trees are preferred over B-Trees for database indexes because B+ Trees store data pointers only in leaf nodes, leaving branch nodes dense and quick to scan."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Believing indexing speeds up write queries (INSERT/UPDATE). It slows writes due to index structure updates. <strong>Depth:</strong> Contrast Clustered vs Non-Clustered.</p>
</div>
""",
    "db-hashing": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Hashing maps search keys to bucket addresses, offering O(1) time complexity for point queries. Extendible hashing handles dynamic table growth using directory resizing."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Saying hashing is good for range queries. Hash indexes don't support sort order, rendering range searches useless. <strong>Depth:</strong> Differentiate Static vs Dynamic.</p>
</div>
""",
    "db-relational-algebra": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Relational algebra is a procedural query language. Describe key operations: Projection (select columns), Selection (filter rows), and Joins (cross-match datasets)."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Confusing Selection (sigma σ) with SQL SELECT. σ filters rows (SQL WHERE). SQL SELECT matches Projection (pi π). <strong>Depth:</strong> Relate operators to SQL.</p>
</div>
""",
    "db-joins": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Explain Joins as merging table rows. Inner Join returns matches. Left/Right Outer Joins retain unmatched records from one side, inserting NULLs on the other."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking Cross Join uses conditional matches. It evaluates the Cartesian Product (all row pairs). <strong>Depth:</strong> Nested loop vs Hash join vs Merge join execution.</p>
</div>
""",
    "db-subqueries": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Differentiate standard subqueries (run once, return static output) from correlated subqueries (reference the outer table, running once for every outer loop row)."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Using correlated subqueries in large tables without indexes. It causes performance bottlenecks (O(N^2)). <strong>Depth:</strong> Explain EXISTS vs IN optimizing.</p>
</div>
""",
    "db-views": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"A View is a virtual table containing a saved query definition. Materialized Views physically store query results on disk, updating via schedules to speed up reads."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Modifying views expecting free writes. Only simple views with 1-to-1 table relations are writeable. <strong>Depth:</strong> View security advantages.</p>
</div>
""",
    "db-triggers": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Triggers are event-driven procedures executed automatically after actions (INSERT, UPDATE, DELETE). Use them to log operations or enforce custom business rules."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Writing recursive trigger loops that lock database threads. <strong>Depth:</strong> Row-level triggers (FOR EACH ROW) vs Statement-level triggers.</p>
</div>
""",
    "db-recovery": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Database recovery uses log files to reconstruct states after a crash. Mention checkpoints: they limit log analysis time by ensuring all dirty pages are flushed."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking database recovery undoes every change. Commits are replayed (REDO), while uncommitted crashes are discarded (UNDO). <strong>Depth:</strong> Explain ARIES.</p>
</div>
""",
    "db-constraints": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Integrity constraints secure database structure: Entity Integrity (no null primary keys), Referential Integrity (valid foreign key targets), and Domain rules."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Forgetting ON DELETE CASCADE effects. Deleting a parent row will delete child rows automatically, which can cause mass data loss. <strong>Depth:</strong> Restrict rules.</p>
</div>
""",
    "db-nosql-cap": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"CAP theorem states a distributed system can choose only 2 of 3: Consistency, Availability, and Partition Tolerance. Real-world systems choose CP or AP."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Saying you can drop Partition Tolerance. Partitions are inevitable hardware errors. The real choice is Consistency vs Availability. <strong>Depth:</strong> BASE vs ACID.</p>
</div>
""",
    "db-sharding": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Sharding is horizontal partitioning, distributing database rows across distinct server hardware nodes. Contrast this with vertical sharding (splitting columns)."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Sharding too early. Try read-replicas, caching, and vertical hardware scaling first, since sharding complicates joins. <strong>Depth:</strong> Hash sharding vs Range sharding.</p>
</div>
""",
    "sql-prac-nth-salary": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"State that `LIMIT 1 OFFSET N-1` extracts the single row at index N-1 from descending sorted salaries. In product companies, write the `DENSE_RANK()` CTE instead."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Writing `OFFSET N` instead of `OFFSET N-1`. OFFSET is 0-indexed. <strong>Depth:</strong> Know how to handle duplicate salaries correctly in your query.</p>
</div>
""",
    "sql-prac-duplicate-emails": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Use `GROUP BY` and `HAVING COUNT(*) > 1` to find duplicates. For deletion, explain a self-join where you compare email matches and delete rows with the higher ID."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Using `WHERE` for aggregate counts. WHERE runs before rows are grouped, so you must use HAVING. <strong>Depth:</strong> Detail duplicate self-join syntax.</p>
</div>
""",
    "sql-prac-consec-nums": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Propose a self-join using consecutive ID conditions (id, id-1, id-2) for simple RDBMS, but mention `LEAD()` window functions for highly optimized execution plans."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Assuming ID sequences have no gaps. Always recommend creating row index sequences using ROW_NUMBER if gaps exist. <strong>Depth:</strong> Window partition syntax.</p>
</div>
""",
    "sql-prac-dep-top-sal": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Use a correlated MAX subquery or a `DENSE_RANK() OVER (PARTITION BY DepartmentId ORDER BY Salary DESC)` window rank to handle department-level ties."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Using `ROW_NUMBER()`, which returns only one employee if there is a top-salary tie, violating department top list rules. <strong>Depth:</strong> Draw partition blocks.</p>
</div>
""",
    "sql-prac-exchange-seats": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Use a `CASE` expression: if ID is odd and matches MAX(ID), keep it. Otherwise, add 1 to odd IDs and subtract 1 from even IDs to swap them."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Forgetting the `ORDER BY id` clause at the end of the query, resulting in random output row sequences. <strong>Depth:</strong> Modulo calculation math.</p>
</div>
""",
    "sql-prac-cancel-rate": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Explain that `SUM(CASE WHEN Status != 'completed' THEN 1 ELSE 0 END) / COUNT(*)` yields the cancellation rate in a single scan. Filter out banned clients/drivers first."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Counting banned users because of missing filters in the WHERE block. <strong>Depth:</strong> Explain why subquery indexes help here.</p>
</div>
"""
}

HIGH_YIELD_TOPICS = ["db-acid-wal", "db-keys", "db-normalization", "db-isolation-levels", "db-indexing", "db-joins"]

# ─────────────────────────────────────────
# HELPERS FOR FOLLOW-UPS AND SPACE FILLERS
# ─────────────────────────────────────────
def get_topic_followups(tid):
    followups_dict = {
        "db-3tier": "• What is physical data independence?<br>• What is conceptual schema?",
        "db-indep": "• Differentiate logical and physical independence.<br>• How are mappings maintained?",
        "db-keys": "• What is referential integrity?<br>• Can a primary key be null?",
        "db-normalization": "• What is insertion anomaly?<br>• What is a prime attribute?",
        "db-advanced-nf": "• What is multi-valued dependency?<br>• Explain 4NF and 5NF.",
        "db-er-mapping": "• Differentiate strong vs weak entities.<br>• What is participation constraint?",
        "db-acid-wal": "• What is isolation level?<br>• How is durability achieved?",
        "db-tx-states": "• What is partially committed state?<br>• What triggers rollback?",
        "db-concurrency": "• What is dirty read?<br>• Explain phantom read.",
        "db-serial": "• What is precedence graph?<br>• Explain view serializability.",
        "db-isolation-levels": "• What is MVCC?<br>• What is snapshot isolation?",
        "db-2pl": "• Explain strict 2PL vs rigorous 2PL.<br>• What is lock conversion?",
        "db-deadlock": "• Explain deadlock detection.<br>• What is wait-die scheme?",
        "db-indexing": "• Why B+ Tree over B Tree?<br>• What is clustered index?",
        "db-hashing": "• What is dynamic hashing directory?<br>• Differentiate static vs dynamic hashing.",
        "db-relational-algebra": "• Explain projection operator.<br>• What is natural join?",
        "db-joins": "• What is self join?<br>• Explain cross join.",
        "db-subqueries": "• Explain correlated subquery.<br>• Differentiate IN vs EXISTS.",
        "db-views": "• What is materialized view?<br>• Can views be updated?",
        "db-triggers": "• Explain stored procedure vs trigger.<br>• Differentiate BEFORE vs AFTER trigger.",
        "db-recovery": "• What is deferred update?<br>• Explain checkpoint in recovery.",
        "db-constraints": "• What is domain constraint?<br>• What is check constraint?",
        "db-nosql-cap": "• Explain eventual consistency.<br>• Differentiate BASE vs ACID.",
        "db-sharding": "• Explain sharding key choice.<br>• Differentiate vertical vs horizontal partitioning.",
        "sql-prac-nth-salary": "• Explain DENSE_RANK() vs RANK().<br>• How to get 2nd highest salary?",
        "sql-prac-duplicate-emails": "• How to delete duplicate rows?<br>• Explain self join deletion.",
        "sql-prac-consec-nums": "• Explain LEAD() and LAG() functions.<br>• How to find 3 consecutive rows?",
        "sql-prac-dep-top-sal": "• Explain PARTITION BY clause.<br>• How to handle salary ties?",
        "sql-prac-exchange-seats": "• How to swap adjacent seats?<br>• Explain CASE WHEN syntax.",
        "sql-prac-cancel-rate": "• How to calculate cancel rate?<br>• Explain date filtering."
    }
    return followups_dict.get(tid, "• List related SQL command examples.<br>• What are the indexing implications?")

def get_dbms_space_filler(tid):
    fillers = {
        "db-3tier": """
<div class="box box-depth">
  <div class="box-title">📈 Architecture Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Basic):</strong> Name Physical, Conceptual, and External layers.<br>
    <strong>Level 2 (PDU):</strong> Map user views to conceptual logical tables.<br>
    <strong>Level 3 (Access):</strong> Explain how the storage engine stores records.<br>
    <strong>Level 4 (Cluster):</strong> Detail distributed multi-node shard coordination layers.
  </div>
</div>
""",
        "db-indep": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "How does logical data independence save dev time?"<br>
    <strong>Candidate:</strong> "It allows changing the conceptual schema (like splitting tables or adding fields) without having to rewrite user-mode application views or client SQL queries."
  </div>
</div>
""",
        "db-keys": """
<div class="box box-depth">
  <div class="box-title">📈 Constraints Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Identify):</strong> Define primary keys and candidate keys.<br>
    <strong>Level 2 (Refer):</strong> Differentiate foreign key referential cascades vs restrictions.<br>
    <strong>Level 3 (Alternate):</strong> Identify alternate keys and unique constraints.<br>
    <strong>Level 4 (Surrogate):</strong> Explain compound natural vs single auto-increment surrogate keys.
  </div>
</div>
""",
        "db-normalization": """
<div class="box box-depth">
  <div class="box-title">📈 Normalization Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Goal):</strong> Prevent anomalies (insert, update, delete).<br>
    <strong>Level 2 (1NF/2NF):</strong> Atomize values; remove partial dependencies.<br>
    <strong>Level 3 (3NF):</strong> Remove transitive dependencies (non-key transitive rules).<br>
    <strong>Level 4 (Decompose):</strong> Validate lossless join and dependency preservation attributes.
  </div>
</div>
""",
        "db-advanced-nf": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "Why is a relation decomposed to BCNF instead of just 3NF?"<br>
    <strong>Candidate:</strong> "When there are multiple overlapping candidate keys. BCNF ensures that for every dependency X -> Y, X must be a super key, removing redundant insert anomalies that 3NF tolerates."
  </div>
</div>
""",
        "db-er-mapping": """
<div class="box box-depth">
  <div class="box-title">📈 ER Schema Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Symbol):</strong> Map entities, attributes, and relationships.<br>
    <strong>Level 2 (Key):</strong> Map weak entities relying on identifying relationships.<br>
    <strong>Level 3 (Relation):</strong> Resolve many-to-many relationships into bridge tables.<br>
    <strong>Level 4 (Inherit):</strong> Map ISA specialization hierarchies (table-per-class vs table-per-hierarchy).
  </div>
</div>
""",
        "db-acid-wal": """
<div class="box box-depth">
  <div class="box-title">📈 Recovery Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (ACID):</strong> Define Atomicity, Consistency, Isolation, and Durability.<br>
    <strong>Level 2 (WAL):</strong> Log edits on disk before dirtying cache pages.<br>
    <strong>Level 3 (Undo):</strong> Undo log allows rolling back incomplete transactions.<br>
    <strong>Level 4 (Redo):</strong> Redo log allows recovering committed data from crash states.
  </div>
</div>
""",
        "db-tx-states": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "What happens if a database crashes during a Partially Committed state?"<br>
    <strong>Candidate:</strong> "The state means execution finished but changes aren't flushed to disk. On reboot, the recovery manager reads WAL and rolls back the transaction because it never reached Committed."
  </div>
</div>
""",
        "db-concurrency": """
<div class="box box-depth">
  <div class="box-title">📈 Anomalies Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Conflict):</strong> Understand read-write and write-write conflicts.<br>
    <strong>Level 2 (Dirty):</strong> Dirty Read (reading uncommitted transaction data).<br>
    <strong>Level 3 (Repeat):</strong> Non-repeatable Read (rereading rows yields altered values).<br>
    <strong>Level 4 (Phantom):</strong> Phantom Read (rereading queries yields inserted records).
  </div>
</div>
""",
        "db-serial": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "How do you test if a schedule is conflict serializable?"<br>
    <strong>Candidate:</strong> "We build a precedence graph where transactions are nodes, and directed edges represent conflicting actions. If the precedence graph has no cycles, it is conflict serializable."
  </div>
</div>
""",
        "db-isolation-levels": """
<div class="box box-depth">
  <div class="box-title">⚖️ SQL Isolation Levels</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Read Uncommitted:</strong> Allows Dirty, Non-repeatable, and Phantom reads. No read locks.<br>
    <strong>Read Committed:</strong> Prevents Dirty reads. Reads read-committed data (shared locks released fast).<br>
    <strong>Repeatable Read:</strong> Prevents Dirty and Non-repeatable reads. Shared locks held until commit.<br>
    <strong>Serializable:</strong> Prevents all anomalies. Range locks acquired.
  </div>
</div>
""",
        "db-2pl": """
<div class="box box-depth">
  <div class="box-title">📈 2PL Lock Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Phase):</strong> Growing phase acquires locks; shrinking phase releases them.<br>
    <strong>Level 2 (Strict):</strong> Release exclusive locks at the very end (prevents cascading rollbacks).<br>
    <strong>Level 3 (Rigorous):</strong> Release all locks at transaction end.<br>
    <strong>Level 4 (Convert):</strong> Upgrade shared locks to exclusive; downgrade exclusive to shared.
  </div>
</div>
""",
        "db-deadlock": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "How does wait-die differ from wound-wait deadlock prevention?"<br>
    <strong>Candidate:</strong> "Wait-die is non-preemptive: older waits, younger dies. Wound-wait is preemptive: older wounds/kills younger to take resource. Both prevent circular wait using transaction timestamps."
  </div>
</div>
""",
        "db-indexing": """
<div class="box box-depth">
  <div class="box-title">📈 Index structure Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Index):</strong> Speeds searches; B+ Tree has linked leaf nodes for range queries.<br>
    <strong>Level 2 (Cluster):</strong> Define table physical row order (one per table).<br>
    <strong>Level 3 (Non-Clust):</strong> Secondary index containing key values and bookmarked data references.<br>
    <strong>Level 4 (Cover):</strong> SQL select attributes are fully contained inside index nodes.
  </div>
</div>
""",
        "db-hashing": """
<div class="box box-depth">
  <div class="box-title">⚖️ Static vs Dynamic Hashing</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Static Hashing:</strong> Maps keys to fixed bucket counts. Fast but fails (causes overflows) if database size exceeds expectations.<br>
    <strong>Dynamic Hashing:</strong> Directory-based buckets that split/merge. Scales dynamically via directory doublings, preventing bucket overflow search degradation.
  </div>
</div>
""",
        "db-relational-algebra": """
<div class="box box-depth">
  <div class="box-title">📈 Relational Operators</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Selection (&sigma;):</strong> Filters table rows matching a predicate condition.<br>
    <strong>Projection (&pi;):</strong> Filters table columns, discarding duplicates.<br>
    <strong>Cartesian Product (&times;):</strong> Couples all row pairs of both relations.<br>
    <strong>Division (&divide;):</strong> Retrieves rows matching all records of divisor table.
  </div>
</div>
""",
        "db-joins": """
<div class="box box-depth">
  <div class="box-title">⚖️ Joins Contrast</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Inner Join:</strong> Returns rows matching join condition on both sides.<br>
    <strong>Left Join:</strong> Returns all left rows plus matching right rows (nulls if no match).<br>
    <strong>Right Join:</strong> Returns all right rows plus matching left rows (nulls if no match).<br>
    <strong>Full Join:</strong> Returns all rows from both tables, padded with nulls where unmatched.
  </div>
</div>
""",
        "db-subqueries": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "Why are correlated subqueries generally avoided?"<br>
    <strong>Candidate:</strong> "Because they reference outer query fields, meaning they must be re-evaluated once for every single row returned by the outer query, resulting in poor O(N^2) execution."
  </div>
</div>
""",
        "db-views": """
<div class="box box-depth">
  <div class="box-title">📈 View Execution Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Concept):</strong> Virtual view acts as a saved SELECT statement filter wrapper.<br>
    <strong>Level 2 (Updatable):</strong> View updates succeed only if mapped to single base table keys.<br>
    <strong>Level 3 (Materialize):</strong> Cache query outputs physically on disk to speed execution.<br>
    <strong>Level 4 (Refresh):</strong> Incrementally update materialized tables using trigger diffs.
  </div>
</div>
""",
        "db-triggers": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "stored procedure vs database trigger: when to use which?"<br>
    <strong>Candidate:</strong> "Stored procedures are explicit blocks called manually by applications. Triggers are implicit blocks run automatically by the database on row modifications (INSERT/UPDATE/DELETE) for audit logging."
  </div>
</div>
""",
        "db-recovery": """
<div class="box box-depth">
  <div class="box-title">📈 Recovery Logs Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Crash):</strong> Reboot triggers recovery engine to scan active log entries.<br>
    <strong>Level 2 (Check):</strong> Checkpoints write active dirty cache pages to disk, reducing log scan bounds.<br>
    <strong>Level 3 (Redo):</strong> Redo committed transactions to restore completed updates.<br>
    <strong>Level 4 (Undo):</strong> Undo active transactions to remove unfinished modifications.
  </div>
</div>
""",
        "db-constraints": """
<div class="box box-depth">
  <div class="box-title">📈 Constraints Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Type):</strong> Map domains, keys, references, and check rules.<br>
    <strong>Level 2 (Entity):</strong> Primary keys must be unique and cannot contain NULL.<br>
    <strong>Level 3 (Referential):</strong> Foreign keys must match active parent primary keys.<br>
    <strong>Level 4 (Assertion):</strong> Multi-table constraints verified using catalog assertions.
  </div>
</div>
""",
        "db-nosql-cap": """
<div class="box box-depth">
  <div class="box-title">📈 CAP theorem Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Define):</strong> Consistency, Availability, Partition Tolerance.<br>
    <strong>Level 2 (Trade):</strong> Distributed partitions (P) force CP or AP options.<br>
    <strong>Level 3 (Consistency):</strong> CP yields strong consistency; AP yields eventual consistency.<br>
    <strong>Level 4 (NoSQL):</strong> Map Document (MongoDB), Key-value (Redis), Column (Cassandra) stores.
  </div>
</div>
""",
        "db-sharding": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "Why does selecting the wrong shard key degrade performance?"<br>
    <strong>Candidate:</strong> "If we choose a biased key (like date), all inserts hit a single database node, causing hot-spotting. A good shard key distributes reads and writes uniformly across all nodes."
  </div>
</div>
""",
        "sql-prac-nth-salary": """
<div class="box box-depth">
  <div class="box-title">📈 Window Function Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>RANK() OVER:</strong> Assigns ranks with gaps on salary ties (e.g., 1, 2, 2, 4).<br>
    <strong>DENSE_RANK() OVER:</strong> Assigns ranks without gaps on salary ties (e.g., 1, 2, 2, 3).<br>
    <strong>ROW_NUMBER():</strong> Assigns sequential integers to rows (e.g., 1, 2, 3, 4).
  </div>
</div>
""",
        "sql-prac-duplicate-emails": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "How do you delete duplicate emails using a self-join?"<br>
    <strong>Candidate:</strong> "We self-join the table on email and select the row with the larger ID to delete: `DELETE p1 FROM Person p1 JOIN Person p2 ON p1.Email = p2.Email WHERE p1.Id > p2.Id`"
  </div>
</div>
""",
        "sql-prac-consec-nums": """
<div class="box box-depth">
  <div class="box-title">📈 Analytical Window Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>LEAD(col, 1):</strong> Fetches the value of the next row in the partition.<br>
    <strong>LEAD(col, 2):</strong> Fetches the value of the row two steps ahead.<br>
    <strong>LAG(col, 1):</strong> Fetches the value of the previous row. Use these to find consecutive numbers.
  </div>
</div>
""",
        "sql-prac-dep-top-sal": """
<div class="box box-depth">
  <div class="box-title">📈 Partitioning Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>PARTITION BY:</strong> Divides query rows into groups (e.g., by department).<br>
    <strong>DENSE_RANK() OVER:</strong> Ranks salaries within each department partition separately.<br>
    <strong>Subquery filtering:</strong> Wraps rank calculation to filter rows where department rank <= 3.
  </div>
</div>
""",
        "sql-prac-exchange-seats": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "How do you swap adjacent seat IDs in SQL?"<br>
    <strong>Candidate:</strong> "Using a CASE statement on seat ID. If ID is odd and not last, add 1. If ID is even, subtract 1. If odd and last, keep ID: `CASE WHEN id % 2 = 1 AND id = (select max(id) from seat) THEN id ...`"
  </div>
</div>
""",
        "sql-prac-cancel-rate": """
<div class="box box-depth">
  <div class="box-title">📈 Aggregation Math Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Denominator:</strong> Total requests where clients/drivers are not banned.<br>
    <strong>Numerator:</strong> Requests cancelled by client or driver.<br>
    <strong>Division Rate:</strong> Use SUM(CASE WHEN status != 'completed' THEN 1 ELSE 0 END) / COUNT(*).
  </div>
</div>
"""
    }
    return fillers.get(tid, get_default_space_filler())

def get_default_space_filler():
    return """
<div class="box box-depth">
  <div class="box-title">📈 Depth Progression</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Basic):</strong> Understand the main definition and syntax.<br>
    <strong>Level 2 (Intermediate):</strong> Learn execution trace and typical memory states.<br>
    <strong>Level 3 (Advanced):</strong> Analyze corner cases and optimization schemes.<br>
    <strong>Level 4 (Expert):</strong> Handle system integration trade-offs.
  </div>
</div>
"""

def get_dbms_industry_box(tid):
    industry_usage = {
        "db-3tier": "Enterprise platforms (like Salesforce) implement 3-tier architecture to serve millions of clients, scaling app instances independently of core database clusters.",
        "db-indep": "Cloud database migrations (e.g., migrating MySQL to AWS Aurora) rely on physical data independence, ensuring backend apps require zero code changes.",
        "db-keys": "Identity providers (like Okta) enforce strict primary and unique key constraints to ensure user email records never duplicate across login directories.",
        "db-normalization": "Financial ledgers and billing systems are normalized to 3NF or BCNF to prevent transaction anomalies and guarantee audit trail consistency.",
        "db-advanced-nf": "Social network profiles use denormalized structures (4NF/5NF analysis) or NoSQL databases to store multi-valued attributes like user hobbies and friends.",
        "db-er-mapping": "ORM tools (like Hibernate or Prisma) automatically map ER diagrams to SQL tables, generating primary-foreign key relationships from object schemas.",
        "db-acid-wal": "Payment gateways (like Stripe) use Write-Ahead Logging (WAL) to guarantee Durability; transactions are committed to disk logs before updating tables.",
        "db-tx-states": "High-throughput messaging systems (like RabbitMQ) track transaction states to ensure messages are either fully processed or safely rolled back.",
        "db-concurrency": "Inventory systems during flash sales manage concurrent writes using database locks to prevent selling the same item to two buyers.",
        "db-serial": "Banking databases enforce serializability during account transfers to prevent race conditions and ensure double-spend protection.",
        "db-isolation-levels": "E-commerce checkout platforms tune isolation levels (e.g., Read Committed) to balance query performance with absolute data accuracy.",
        "db-2pl": "Distributed database systems (like Google Spanner) use Strict 2-Phase Locking to prevent dirty reads and cascading transaction rollbacks.",
        "db-deadlock": "High-concurrency SaaS backends run automated deadlock detection loops to select and terminate the cheapest transaction, releasing blocked threads.",
        "db-indexing": "Search platforms use B+ Tree indexes to query millions of e-commerce products in milliseconds, bypassing expensive full table scans.",
        "db-hashing": "In-memory key-value databases (like Redis) use hash tables for O(1) lookups, providing ultra-fast session cache retrievals.",
        "db-relational-algebra": "SQL Query Optimizers translate SELECT statements into relational algebra trees to find the most efficient execution path.",
        "db-joins": "Analytics platforms join user activity tables with product catalogs to generate customized dashboard reports.",
        "db-subqueries": "Reporting services write nested subqueries to identify top-performing sales representatives within each geographic region.",
        "db-views": "Security layers use virtual read-only views to expose user names and emails while hiding sensitive hash passwords and credit cards.",
        "db-triggers": "Compliance platforms implement database triggers to automatically write audit trail logs whenever user balance records are updated.",
        "db-recovery": "Cloud storage backends use checkpointing and WAL logs to recover consistent database states after sudden hardware power failures.",
        "db-constraints": "Medical record databases enforce CHECK and NOT NULL constraints to ensure patient vital stats fall within valid biological ranges.",
        "db-nosql-cap": "Global shopping carts (like Amazon DynamoDB) prioritize Availability over Consistency (AP system) during peak traffic to never reject checkouts.",
        "db-sharding": "Social media giants (like Instagram) partition user tables by UserID (sharding) across database clusters to scale horizontally.",
        "sql-prac-nth-salary": "HR payroll audits run dense ranking queries to identify employees with salaries in specific tax brackets.",
        "sql-prac-duplicate-emails": "Marketing automation systems clean mailing lists by running duplicate checks to prevent sending spam emails to the same user.",
        "sql-prac-consec-nums": "IoT monitoring dashboards run window functions to detect sensor failure anomalies when consecutive error signals are received.",
        "sql-prac-dep-top-sal": "Corporate resource planners execute partitioned rankings to calculate departmental salary distributions and budgets.",
        "sql-prac-exchange-seats": "Booking systems swap seat numbers dynamically during reservation changes using CASE statements in SQL.",
        "sql-prac-cancel-rate": "Ride-sharing dispatch services query taxi cancel rates over time intervals to penalize fraudulent driver accounts."
    }
    desc = industry_usage.get(tid, "Relational databases use ACID transactions and indexing engines to store and retrieve enterprise data reliably at scale.")
    return f"""
<div class="box box-industry" style="padding: 10px; margin-bottom: 0; border: 1px solid #F5E6B3; background: #FDF6E3;">
  <div class="box-title" style="font-size: 8pt; color: #B7791F; margin-bottom: 4px;">🏭 Where Used in Industry</div>
  <p style="font-size: 7.5pt; line-height: 1.35; color: #5C5438; margin: 0;">{desc}</p>
</div>
"""

def get_dbms_depth_box(tid):
    depth_levels = {
        "db-3tier": [
            "Client direct queries vs middleware orchestrations.",
            "Connection pool limits and socket recycling.",
            "Load balancing client sessions across application tiers.",
            "Security zoning and database firewall rules.",
            "Distributed caching strategies (Redis/Memcached) at application layer."
        ],
        "db-indep": [
            "Conceptual, logical, and physical schema mappings.",
            "Physical independence (file layout changes).",
            "Logical independence (view abstraction layers).",
            "Query translation through schema mapping engines.",
            "Managing schema migrations in blue-green deployments."
        ],
        "db-keys": [
            "Super keys, candidate keys, and primary keys.",
            "Referential integrity constraints and foreign keys.",
            "Composite keys vs auto-incrementing surrogate keys.",
            "Cascade operations (ON DELETE CASCADE) internals.",
            "UUID v4 vs sequential integer PK index fragmentation."
        ],
        "db-normalization": [
            "Redundancy anomalies: insert, update, delete.",
            "1NF atomic fields, 2NF partial dependencies.",
            "3NF transitive dependencies, BCNF super key rules.",
            "Functional dependency closure and attribute sets.",
            "Lossless-join and dependency-preserving decompositions."
        ],
        "db-advanced-nf": [
            "Multivalued dependencies and 4NF rules.",
            "Join dependencies and 5NF (Project-Join Normal Form).",
            "Domain-Key Normal Form (DKNF) constraints.",
            "Denormalization trade-offs for read-heavy systems.",
            "Designing hybrid SQL-NoSQL schema layers."
        ],
        "db-er-mapping": [
            "Entity sets, attributes, and relationships.",
            "Mapping strong vs weak entities to tables.",
            "Mapping 1:1, 1:N, and N:M relationships.",
            "Representing inheritance (Single Table vs Joined Table).",
            "Converting complex ER constraints into SQL assertions."
        ],
        "db-acid-wal": [
            "Atomicity, Consistency, Isolation, and Durability.",
            "Write-Ahead Logging (WAL) and commit protocols.",
            "Buffer pool management and dirty page flushing.",
            "Force/No-Force and Steal/No-Steal buffer policies.",
            "Doublewrite buffers to prevent partial page write crashes."
        ],
        "db-tx-states": [
            "Active, partially committed, and committed states.",
            "Failed and aborted transaction states.",
            "Transaction rollback using rollback segments.",
            "Savepoints and partial rollback implementations.",
            "Distributed transaction state tracking (Two-Phase Commit)."
        ],
        "db-concurrency": [
            "Concurrency issues: dirty reads, non-repeatable reads, phantoms.",
            "Shared (S) vs Exclusive (X) lock request queues.",
            "Intention locks (IS/IX) in multiple granularity locking.",
            "Optimistic Concurrency Control (OCC) validation stages.",
            "Multi-Version Concurrency Control (MVCC) snapshot isolation."
        ],
        "db-serial": [
            "Conflict serializability vs view serializability.",
            "Conflict equivalence and precedence graphs.",
            "Serialization order and topological sorting.",
            "Recoverable and cascade-less schedules.",
            "Formal mathematical proof of serializability."
        ],
        "db-isolation-levels": [
            "ANSI SQL isolation levels: Read Uncommitted to Serializable.",
            "Read phenomena: Dirty Read, Non-repeatable Read, Phantom Read.",
            "Snapshot isolation internals and MVCC row versions.",
            "Write skew anomaly under snapshot isolation.",
            "Performance vs safety trade-offs in high-concurrency."
        ],
        "db-2pl": [
            "Growing phase, shrinking phase, and lock point.",
            "Basic 2PL vs Conservative 2PL lock requirements.",
            "Strict 2PL and Rigorous 2PL lock releases.",
            "Cascading rollbacks prevention under Strict 2PL.",
            "Mathematical proof of serializability under 2PL."
        ],
        "db-deadlock": [
            "Deadlock conditions: mutual exclusion, hold-wait, no-preemption, circular wait.",
            "Deadlock prevention using wait-die and wound-wait schemes.",
            "Deadlock detection using Wait-For Graphs (WFG).",
            "Victim selection criteria (rollback cost, lock hold duration).",
            "Distributed deadlock detection protocols."
        ],
        "db-indexing": [
            "Clustered vs non-clustered index storage formats.",
            "B+ Tree index node splits and height balancing.",
            "Index scan, index seek, and covering index queries.",
            "Composite index prefix rules (leftmost column rule).",
            "Index fragmentation and rebuild/reorganize metrics."
        ],
        "db-hashing": [
            "Static hashing vs dynamic hashing.",
            "Collision resolution: overflow chaining vs open addressing.",
            "Extendible hashing directories and bucket splits.",
            "Linear hashing load factors and split pointers.",
            "Hash index performance for range queries vs equality search."
        ],
        "db-relational-algebra": [
            "Select, project, and rename unary operators.",
            "Union, intersection, set difference binary operators.",
            "Cartesian product and join types (Theta, Natural, Outer).",
            "Query tree parsing and relational equivalences.",
            "Cost-based query optimization plans."
        ],
        "db-joins": [
            "Inner join, left/right outer joins, full outer joins.",
            "Cross joins and self joins.",
            "Nested loop join, block nested loop join engines.",
            "Sort-merge join and partition-hash join algorithms.",
            "Join order optimizations in multi-table queries."
        ],
        "db-subqueries": [
            "Correlated vs non-correlated subqueries.",
            "Subquery execution in SELECT, FROM, and WHERE clauses.",
            "Set comparison operators (IN, ANY, ALL, EXISTS).",
            "Query rewriting (subquery flattening to joins) by optimizer.",
            "Performance traps of correlated subqueries on large datasets."
        ],
        "db-views": [
            "Virtual views vs materialized views.",
            "View query rewriting and inline execution.",
            "Updatable view rules (WITH CHECK OPTION).",
            "Materialized view refresh strategies (incremental vs full).",
            "Using views for column-level and row-level security."
        ],
        "db-triggers": [
            "Row-level vs statement-level trigger executions.",
            "BEFORE vs AFTER trigger event firing sequences.",
            "NEW and OLD pseudo-tables memory allocations.",
            "Trigger cascading, recursion limits, and side-effects.",
            "Trigger auditing performance costs on bulk updates."
        ],
        "db-recovery": [
            "Transaction log undo and redo pass execution.",
            "Log-based recovery algorithms (ARIES framework).",
            "Fuzzy checkpointing logs and dirty page tables.",
            "Compensation Log Records (CLRs) during undo loops.",
            "Recovering data consistency after media failure."
        ],
        "db-constraints": [
            "Domain constraints, entity integrity, and referential integrity.",
            "CHECK, NOT NULL, and UNIQUE constraint checks.",
            "Deferred vs immediate constraint validation during commits.",
            "Enforcing cross-table assertions and complex constraints.",
            "System catalog metadata storage for constraints."
        ],
        "db-nosql-cap": [
            "NoSQL categories: Key-Value, Document, Column-Family, Graph.",
            "CAP Theorem: Consistency, Availability, Partition Tolerance.",
            "BASE properties: Basically Available, Soft state, Eventual consistency.",
            "Vector clocks and conflict-free replicated data types (CRDTs).",
            "PACELC theorem extensions to CAP trade-offs."
        ],
        "db-sharding": [
            "Vertical partitioning vs horizontal partitioning (sharding).",
            "Shard keys selection (range, hash, list sharding).",
            "Cross-shard queries and scatter-gather operations.",
            "Consistent hashing and shard rebalancing algorithms.",
            "Distributed transaction coordinations over shards."
        ],
        "sql-prac-nth-salary": [
            "Using subqueries to find top N records.",
            "DENSE_RANK() vs RANK() vs ROW_NUMBER() window functions.",
            "Correlated subquery complexity (O(N^2) search cost).",
            "Index utilization in partition-ranking queries.",
            "Performance comparison of offset queries vs subqueries."
        ],
        "sql-prac-duplicate-emails": [
            "Finding duplicates using GROUP BY and HAVING clauses.",
            "Deleting duplicates using SELF JOIN or CTID/ROWID.",
            "Window functions (ROW_NUMBER) for duplicate isolation.",
            "Database unique constraints to prevent duplicates.",
            "Performance analysis of bulk duplicate deletes."
        ],
        "sql-prac-consec-nums": [
            "Tracking consecutive sequences using SELF JOINs.",
            "Using LEAD() and LAG() window functions.",
            "Row number difference technique (Gaps and Islands).",
            "Time-series sequence tracking in SQL.",
            "Optimizing sequential range scans."
        ],
        "sql-prac-dep-top-sal": [
            "Using window functions over partition groups.",
            "DENSE_RANK() OVER (PARTITION BY ... ORDER BY ...).",
            "Handling duplicate ranking boundary conditions.",
            "Index design for partition window calculations.",
            "Performance of CTEs vs nested rank subqueries."
        ],
        "sql-prac-exchange-seats": [
            "Using CASE statements for dynamic value shifts.",
            "Swapping rows using arithmetic index offset logic.",
            "Handling odd-numbered row boundaries.",
            "LAG() and LEAD() window operations for seat changes.",
            "Transaction safety during dynamic updates."
        ],
        "sql-prac-cancel-rate": [
            "Calculating percentages using filtered aggregate counts.",
            "SUM(CASE WHEN ... THEN 1 ELSE 0 END) syntax patterns.",
            "Handling division-by-zero boundary conditions.",
            "Optimizing join-filter operations on massive transaction logs.",
            "Time-series window filtering partitions."
        ]
    }
    levels = depth_levels.get(tid, [
        "Core syntax and basic conceptual definitions.",
        "SQL Query structures, database keys, or normal forms.",
        "Transaction scheduling, lock queues, or B+ Tree operations.",
        "Query optimizer paths and storage engine caching.",
        "Horizontally partitioned shards and distributed coordination."
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

# ─────────────────────────────────────────
# GENERATE_PAGE: 14-Section Template with Bottom Grid
# ─────────────────────────────────────────
def generate_page(topic, current_page, total_pages):
    num = topic['num']
    title = topic['title']
    subtitle = topic['subtitle']
    chapter = topic['chapter']
    left_col = topic['left_col']
    right_col = topic['right_col']
    trap = topic['trap']
    trick = topic['trick']
    tid = topic['id']
    stars = topic['yield_stars']
    
    page_indicator = f"PAGE {str(current_page).zfill(2)} / {str(total_pages).zfill(2)}"
    
    # Conditional High Yield Badge (Top 20%)
    header_right_content = """
        <div class="badge-yield">🔥 HIGH YIELD</div>
        <div class="header-badge">Placement Handbook</div>
    """ if tid in HIGH_YIELD_TOPICS else """
        <div class="header-badge">Core CS Notes</div>
    """
    
    # Space Filler Content
    space_filler = get_dbms_space_filler(tid)
    industry_box = get_dbms_industry_box(tid)
    depth_box = get_dbms_depth_box(tid)
    left_col_updated = left_col + "\n" + industry_box + "\n" + depth_box
    
    # Extract Mistake from booster HTML using re
    import re
    booster_html = DBMS_BOOSTERS.get(tid, "")
    mistake_text = "Believing that textbook definitions are sufficient; always lead with real-world trade-offs."
    
    mistake_match = re.search(r"Mistake:</strong>\s*(.*?)\s*<strong>", booster_html)
    if not mistake_match:
        mistake_match = re.search(r"Mistake:</strong>\s*(.*?)\s*$", booster_html)
    if mistake_match:
        mistake_text = mistake_match.group(1).replace("</p>", "").strip()
        
    followups_text = get_topic_followups(tid)
    
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
        <!-- Space Filler replacing the old What to Say booster -->
        {space_filler}
      </div>
    </div>

    <!-- Bottom Placement Grid (L4) - 4-part placement section above the footer -->
    <div class="bottom-placement-grid">
      <div class="placement-block block-mistake">
        <div class="placement-block-title">⚠️ Common Mistake</div>
        <div>{mistake_text}</div>
      </div>
      <div class="placement-block block-trap">
        <div class="placement-block-title">🛑 Interviewer Trap</div>
        <div>{trap}</div>
      </div>
      <div class="placement-block block-followups">
        <div class="placement-block-title">🔄 Top Follow-Ups</div>
        <div>{followups_text}</div>
      </div>
      <div class="placement-block block-trick">
        <div class="placement-block-title">💡 Memory Trick</div>
        <div>{trick}</div>
      </div>
    </div>
    
    <!-- Footer (L5) -->
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> DBMS <span>›</span> <span>{title}</span></div>
      </div>
      <div class="page-number-premium">
        {page_indicator}
      </div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# ROADMAP PAGE (Page 2)
# ─────────────────────────────────────────
roadmap_page = f"""
  <div class="page roadmap-page" id="db-roadmap">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="header-badge" style="background: rgba(255,255,255,0.25);">DBMS ROADMAP</div>
      </div>
    </div>
    
    <div style="padding: 30px 40px; flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
      <div>
        <div style="font-size: 26pt; font-weight: 800; color: #111; margin-bottom: 8px;">Database Systems Roadmap</div>
        <div style="font-size: 11pt; color: #EA763F; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px;">Placement Preparation Guide</div>
        
        <div style="background: #FFF5F0; border-left: 5px solid #EA763F; padding: 14px 20px; border-radius: 6px; margin-bottom: 25px;">
          <strong style="color: #EA763F; font-size: 11pt; display: block; margin-bottom: 6px;">How to use this Handbook:</strong>
          <p style="font-size: 9.5pt; color: #4A5568; line-height: 1.5;">Database Management Systems are tested heavily using transactional integrity questions (ACID, 2PL, Isolation Levels) and normalization mechanics (1NF to BCNF). Focus on index page structures, join optimization algorithms, and sharding vs replication scales.</p>
        </div>

        <div style="margin-top: 15px;">
          <div style="font-size: 12pt; font-weight: 800; color: #1A202C; margin-bottom: 12px; border-bottom: 2px solid #E2E8F0; padding-bottom: 6px;">🎯 Three-Phase Learning Plan</div>
          
          <div style="display: flex; gap: 15px; margin-bottom: 15px;">
            <div style="background: #EBF8FF; border: 1px solid #BEE3F8; border-radius: 8px; padding: 12px; flex: 1;">
              <span style="background: #3182CE; color: white; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 7.5pt; text-transform: uppercase;">Phase 1</span>
              <strong style="display: block; font-size: 9.5pt; margin-top: 6px; color: #2B6CB0;">Schema &amp; Normalization</strong>
              <p style="font-size: 8pt; color: #4A5568; margin-top: 4px;">Master 3-tier architecture, functional dependencies, 1NF/2NF/3NF/BCNF normalization rules, and ER mappings. (Topics 1 - 6)</p>
            </div>
            
            <div style="background: #F0FFF4; border: 1px solid #C6F6D5; border-radius: 8px; padding: 12px; flex: 1;">
              <span style="background: #38A169; color: white; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 7.5pt; text-transform: uppercase;">Phase 2</span>
              <strong style="display: block; font-size: 9.5pt; margin-top: 6px; color: #276749;">Transactions &amp; Locking</strong>
              <p style="font-size: 8pt; color: #4A5568; margin-top: 4px;">Study ACID properties, isolation levels (Dirty/Phantom reads), 2PL lock protocols, and deadlock avoidance models. (Topics 7 - 13)</p>
            </div>
            
            <div style="background: #FFFFF0; border: 1px solid #FEFCBF; border-radius: 8px; padding: 12px; flex: 1;">
              <span style="background: #D69E2E; color: white; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 7.5pt; text-transform: uppercase;">Phase 3</span>
              <strong style="display: block; font-size: 9.5pt; margin-top: 6px; color: #B7791F;">Queries, Indexing &amp; SQL</strong>
              <p style="font-size: 8pt; color: #4A5568; margin-top: 4px;">Understand B+ Trees, relational algebra, joins, subqueries, materialized views, triggers, CAP theorem, and SQL exercises. (Topics 14 - 30)</p>
            </div>
          </div>
        </div>
      </div>

      <div style="border-top: 2px solid #E2E8F0; padding-top: 20px; display: flex; justify-content: space-between; align-items: center;">
        <div style="font-size: 8.5pt; color: #718096;">
          <strong>Target Completion:</strong> 2.5 Hours Core Study &amp; 30 Mins Self-Recall
        </div>
        <div style="font-size: 8.5pt; color: #EA763F; font-weight: 800; text-align: right; line-height: 1.3;">
          Created by Pranav Gawai<br>
          <span style="font-size: 7.5pt; color: #718096; font-weight: 500;">grindos.pranavx.in</span>
        </div>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> DBMS <span>›</span> <span>Roadmap</span></div>
      </div>
      <div class="page-number-premium">PAGE 02 / 40</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# DYNAMIC TABLE OF CONTENTS (Page 3)
# ─────────────────────────────────────────
toc_rows = ""
chapters_seen = {}
for t in topics:
    ch = t['chapter']
    if ch not in chapters_seen:
        chapters_seen[ch] = []
    chapters_seen[ch].append(t)

# Page indices: Cover = 1, Roadmap = 2, TOC = 3, content starts at 4
for ch_name, ch_topics in chapters_seen.items():
    toc_rows += f"""
    <div style="font-size: 9pt; font-weight: 800; color: #EA763F; text-transform: uppercase; letter-spacing: 1px; margin-top: 10px; margin-bottom: 4px;">{ch_name}</div>
    """
    for t in ch_topics:
        idx = int(t['num']) + 3
        page_str = str(idx).zfill(2)
        toc_rows += f"""
        <div style="display: flex; align-items: flex-end; margin-bottom: 4px; font-size: 8.5pt; font-weight: 700; color: #2D3748;">
          <a href="#{t['id']}" style="display: flex; width: 100%; align-items: flex-end; text-decoration: none; color: inherit;">
            <span style="color: #EA763F; width: 24px; font-weight: 800;">{t['num']}</span>
            <span style="background: white; padding-right: 6px;">{t['title']}</span>
            <span style="flex: 1; border-bottom: 2px dotted #CBD5E0; position: relative; top: -3px; margin: 0 4px;"></span>
            <span style="color: #718096; font-weight: 800; padding-left: 4px;">p.{page_str}</span>
          </a>
        </div>
        """

toc_page = f"""
  <div class="page toc-page" id="dbms-toc">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="header-badge" style="background: rgba(255,255,255,0.25);">INDEX</div>
      </div>
    </div>
    
    <div class="toc-inner" style="padding: 20px 40px; flex:1; display:flex; flex-direction:column; justify-content:space-between; overflow:hidden;">
      <div>
        <div style="font-size: 20pt; font-weight: 800; color: #111; border-bottom: 4px solid #EA763F; display: inline-block; padding-bottom: 4px; margin-bottom: 6px; letter-spacing: -0.5px;">Table of Contents</div>
        <div style="font-size: 8.5pt; color: #A0AEC0; font-weight: 600; margin-bottom: 6px;">Database Management Systems · Placement Preparation Handbook</div>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
          <div>
            {"".join(toc_rows.splitlines()[:len(toc_rows.splitlines())//2])}
          </div>
          <div>
            {"".join(toc_rows.splitlines()[len(toc_rows.splitlines())//2:])}
          </div>
        </div>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> DBMS <span>›</span> <span>Index</span></div>
      </div>
      <div class="page-number-premium">PAGE 03 / 40</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# FINAL REVISION PAGE (Page 34)
# ─────────────────────────────────────────
final_revision_page = f"""
  <div class="page final-rev-page" id="dbms-finalrev">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="badge-yield" style="background:#FFF5F0; color:#EA763F;">⚡ CRAM SHEET</div>
        <div class="header-badge">DBMS Final Revision</div>
      </div>
    </div>
    
    <div style="padding: 24px 30px; display: flex; flex-direction: column; gap: 14px; flex: 1;">
      <div style="text-align: center;">
        <div style="font-size: 20pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">DBMS Last-Minute Revision Sheet</div>
        <div style="font-size: 9.5pt; color: #EA763F; font-weight: 700; margin-top: 4px;">Top Integrity Laws, Locking Schemes, and Normalization Guides</div>
      </div>
      
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
        <div style="border: 1px solid #CBD5E0; border-radius: 8px; padding: 12px; background: white;">
          <strong style="color: #EA763F; font-size: 9pt; display: block; margin-bottom: 6px; border-bottom: 1.5px solid #EA763F; padding-bottom: 2px;">⚡ LOCKS &amp; TX SUMMARY</strong>
          <table style="width: 100%; font-size: 8pt; border-collapse: collapse;">
            <tr style="border-bottom: 1px solid #E2E8F0;"><td style="font-weight:bold; padding:3px 0;">ACID</td><td>Atomicity, Consistency, Isolation, Durability.</td></tr>
            <tr style="border-bottom: 1px solid #E2E8F0;"><td style="font-weight:bold; padding:3px 0;">2-Phase Lock</td><td>Growing (locking) and shrinking (unlocking) stages.</td></tr>
            <tr style="border-bottom: 1px solid #E2E8F0;"><td style="font-weight:bold; padding:3px 0;">Strict 2PL</td><td>No exclusive locks released until commit.</td></tr>
            <tr style="border-bottom: 1px solid #E2E8F0;"><td style="font-weight:bold; padding:3px 0;">B+ Tree</td><td>Range queries supported; data stored in leaf nodes.</td></tr>
            <tr style="border-bottom: 1px solid #E2E8F0;"><td style="font-weight:bold; padding:3px 0;">CAP Theorem</td><td>Consistency vs Availability under partitions.</td></tr>
          </table>
        </div>
        
        <div style="border: 1px solid #CBD5E0; border-radius: 8px; padding: 12px; background: white;">
          <strong style="color: #2B6CB0; font-size: 9pt; display: block; margin-bottom: 6px; border-bottom: 1.5px solid #2B6CB0; padding-bottom: 2px;">📏 NORMALIZATION LAWS</strong>
          <ul style="font-size: 8pt; list-style-type: square; padding-left: 14px; line-height: 1.4; color: #4A5568;">
            <li><strong>1NF:</strong> Eliminate duplicate columns; enforce atomic values.</li>
            <li><strong>2NF:</strong> Remove partial dependencies on candidate keys.</li>
            <li><strong>3NF:</strong> Remove transitive dependencies of non-prime attributes.</li>
            <li><strong>BCNF:</strong> For X -> Y, X must be a super key.</li>
            <li><strong>WAL:</strong> Disk log write before memory DB page flush.</li>
          </ul>
        </div>
      </div>
      
      <div style="border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px; background: #FEF8F4;">
        <strong style="color: #276749; font-size: 9.5pt; display: block; margin-bottom: 6px;">💡 TOP 5 INTERVIEW CONCEPTS TO RECALL</strong>
        <ol style="font-size: 8.5pt; padding-left: 18px; line-height: 1.5; color: #2D3748;">
          <li><strong>Dirty vs Phantom reads:</strong> Dirty = reading uncommitted data. Phantom = reading new rows added since.</li>
          <li><strong>MVCC:</strong> Multi-Version Concurrency Control prevents readers from blocking writers.</li>
          <li><strong>Clustered vs Non-Clustered:</strong> Clustered determines physical row storage order on disk (one per table).</li>
          <li><strong>Wait-die vs Wound-wait:</strong> Wait-die (older waits, younger dies). Wound-wait (older preempts younger).</li>
          <li><strong>View vs Materialized:</strong> View is query rewrite. Materialized view is query results cached on disk.</li>
        </ol>
      </div>

      <div style="border: 1px dashed #EA763F; border-radius: 8px; padding: 12px; background: white; text-align: center;">
        <span style="font-size: 9pt; font-weight: 800; color: #EA763F; display: block; margin-bottom: 4px;">🎯 QUICK SELF-TEST CHECKLIST</span>
        <div style="display: flex; justify-content: center; gap: 20px; font-size: 8pt; color: #718096; font-weight: bold;">
          <span>[ ] Differentiate 3NF and BCNF</span>
          <span>[ ] State isolation level anomalies</span>
          <span>[ ] Draw B+ Tree leaf link</span>
        </div>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> DBMS <span>›</span> <span>Cheatsheet</span></div>
      </div>
      <div class="page-number-premium">PAGE 34 / 40</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# COMPARISON CHEAT SHEET PAGE (Page 35)
# ─────────────────────────────────────────
def generate_comparison_cheat_sheet(LOGO_BASE64):
    return f"""
  <div class="page" id="dbms-cheatsheet-comparison">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="badge-yield" style="background:#FFF5F0; color:#EA763F;">⚖️ COMPARISON</div>
        <div class="header-badge">Cheat Sheet</div>
      </div>
    </div>
    
    <div style="padding: 20px 24px; display: flex; flex-direction: column; gap: 8px; flex: 1; overflow: hidden;">
      <div style="text-align: center; margin-bottom: 2px;">
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">DBMS Comparison Cheat Sheet</div>
        <div style="font-size: 9pt; color: #EA763F; font-weight: 700;">Quick Reference Contrast Tables for Fresher Interviews</div>
      </div>
      
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; flex: 1;">
        <!-- Left Column -->
        <div style="display: flex; flex-direction: column; gap: 8px;">
          <!-- Primary Key vs Foreign Key -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 8px; background: white;">
            <div style="font-size: 8pt; font-weight: 800; color: #EA763F; border-bottom: 1.5px solid #EA763F; padding-bottom: 2px; margin-bottom: 4px; text-transform: uppercase;">Primary Key vs Foreign Key</div>
            <table style="width: 100%; font-size: 7.2pt; border-collapse: collapse; text-align: left;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Primary Key</th><th>Foreign Key</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Uniqueness</td><td>Must be unique</td><td>Duplicates allowed</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Null Values</td><td>Strictly NOT NULL</td><td>NULL allowed</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Table Limit</td><td>Max 1 per table</td><td>Multiple allowed</td></tr>
              <tr><td>Purpose</td><td>Identify table records</td><td>Link related tables</td></tr>
            </table>
          </div>
          
          <!-- 3NF vs BCNF -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 8px; background: white;">
            <div style="font-size: 8pt; font-weight: 800; color: #2B6CB0; border-bottom: 1.5px solid #2B6CB0; padding-bottom: 2px; margin-bottom: 4px; text-transform: uppercase;">3NF vs BCNF</div>
            <table style="width: 100%; font-size: 7.2pt; border-collapse: collapse; text-align: left;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>3NF</th><th>BCNF</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Dependency Rule</td><td>X -> Y, Y is prime ok</td><td>X -> Y, X must be super key</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Strength</td><td>Weaker normalization</td><td>Stronger normalization</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Overlapping Keys</td><td>Tolerated</td><td>Strictly normalized</td></tr>
              <tr><td>Decomposition</td><td>Always preserves deps</td><td>May lose dependencies</td></tr>
            </table>
          </div>

          <!-- SQL vs NoSQL -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 8px; background: white;">
            <div style="font-size: 8pt; font-weight: 800; color: #276749; border-bottom: 1.5px solid #276749; padding-bottom: 2px; margin-bottom: 4px; text-transform: uppercase;">SQL vs NoSQL</div>
            <table style="width: 100%; font-size: 7.2pt; border-collapse: collapse; text-align: left;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>SQL</th><th>NoSQL</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Data Model</td><td>Relational Tables</td><td>Document, Key-value</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Schema</td><td>Strict, static</td><td>Flexible, dynamic</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Scaling</td><td>Vertical (bigger VM)</td><td>Horizontal (shards)</td></tr>
              <tr><td>Transactions</td><td>Strong ACID</td><td>BASE / Eventual</td></tr>
            </table>
          </div>
        </div>
        
        <!-- Right Column -->
        <div style="display: flex; flex-direction: column; gap: 8px;">
          <!-- Clustered vs Non-Clustered Index -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 8px; background: white;">
            <div style="font-size: 8pt; font-weight: 800; color: #7B341E; border-bottom: 1.5px solid #7B341E; padding-bottom: 2px; margin-bottom: 4px; text-transform: uppercase;">Clustered vs Non-Clustered</div>
            <table style="width: 100%; font-size: 7.2pt; border-collapse: collapse; text-align: left;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Clustered</th><th>Non-Clustered</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Physical Storage</td><td>Defines physical row order</td><td>Stored in separate structure</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Leaf Nodes</td><td>Contain actual data rows</td><td>Contain pointers/keys</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Table Limit</td><td>Max 1 per table</td><td>Multiple (e.g., 249+)</td></tr>
              <tr><td>Lookup Steps</td><td>Direct retrieval</td><td>Bookmark lookup needed</td></tr>
            </table>
          </div>

          <!-- View vs Materialized View -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 8px; background: white;">
            <div style="font-size: 8pt; font-weight: 800; color: #6B46C1; border-bottom: 1.5px solid #6B46C1; padding-bottom: 2px; margin-bottom: 4px; text-transform: uppercase;">View vs Materialized View</div>
            <table style="width: 100%; font-size: 7.2pt; border-collapse: collapse; text-align: left;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Virtual View</th><th>Materialized View</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Storage</td><td>Query only (no disk space)</td><td>Saves query output on disk</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Execution</td><td>Evaluates on every run</td><td>Precomputed; reads cached</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Latency</td><td>Higher (joins evaluated)</td><td>Extremely low (flat read)</td></tr>
              <tr><td>Updates</td><td>Directly reflects schema</td><td>Requires scheduled refresh</td></tr>
            </table>
          </div>

          <!-- Trigger vs Stored Procedure -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 8px; background: white;">
            <div style="font-size: 8pt; font-weight: 800; color: #319795; border-bottom: 1.5px solid #319795; padding-bottom: 2px; margin-bottom: 4px; text-transform: uppercase;">Trigger vs Stored Procedure</div>
            <table style="width: 100%; font-size: 7.2pt; border-collapse: collapse; text-align: left;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Trigger</th><th>Stored Procedure</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Execution</td><td>Implicit on events (DML)</td><td>Explicit manual call</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Parameters</td><td>No parameters supported</td><td>Accepts IN, OUT params</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Return values</td><td>Cannot return values</td><td>Can return datasets</td></tr>
              <tr><td>Typical Use</td><td>Auditing, constraints</td><td>Batch queries, complex business</td></tr>
            </table>
          </div>
        </div>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> DBMS <span>›</span> <span>Comparisons</span> <span style="font-size:7.5pt; color:#A0AEC0; font-weight:normal; margin-left:10px;">Created by Pranav Gawai</span></div>
      </div>
      <div class="page-number-premium">PAGE 35 / 40</div>
    </div>
  </div>
  """

# ─────────────────────────────────────────
# EXPECTED Q&A GENERATION (Pages 36-37)
# ─────────────────────────────────────────
def generate_expected_qa_pages_new(LOGO_BASE64):
    qas = [
        {
            "q": "What is database normalization, and explain the differences between 1NF, 2NF, 3NF, and BCNF?",
            "a": "Normalization is the process of organizing database schemas to minimize data redundancy and prevent insertion, update, and deletion anomalies. In 1NF, we ensure all column values are atomic and each record is unique. In 2NF, we meet 1NF and eliminate partial dependencies, meaning every non-prime attribute must depend on the whole candidate key. In 3NF, we meet 2NF and eliminate transitive dependencies, meaning non-prime attributes cannot depend on other non-prime attributes. BCNF, or Boyce-Codd Normal Form, is a stronger version of 3NF where for every functional dependency X -> Y, X must be a super key. BCNF resolves anomalies that 3NF allows when there are overlapping candidate keys.",
            "keywords": ["Data Redundancy", "Atomic Values", "Partial Dependency", "Transitive Dependency", "Super Key"],
            "followups": "What is BCNF decomposition? Can a relation be in 3NF but not BCNF?",
            "mistake": "Stating that 3NF allows transitive dependencies. It strictly forbids them.",
            "depth": "Detail the dependency preservation trade-offs when decomposing a relation to BCNF."
        },
        {
            "q": "Explain the ACID properties of a database transaction. How does the DBMS guarantee them?",
            "a": "ACID represents Atomicity, Consistency, Isolation, and Durability, which guarantee reliable transaction processing. Atomicity ensures all operations in a transaction succeed, or the entire transaction is rolled back; this is guaranteed by the Undo Log and Write-Ahead Logging. Consistency ensures a transaction transitions the database from one valid state to another, enforcing constraints. Isolation ensures concurrent transactions execute without interfering with each other; this is guaranteed by concurrency control protocols like 2PL and lock-based isolation levels. Durability guarantees that once a transaction commits, its changes survive system crashes; this is achieved by flushing Redo Logs to non-volatile disk storage before acknowledging the commit.",
            "keywords": ["Transaction Rollback", "Write-Ahead Logging", "Lock Isolation", "Redo Logs", "Crash Recovery"],
            "followups": "Differentiate WAL vs Shadow Paging. What is the role of checkpoints in recovery?",
            "mistake": "Believing Isolation is strictly handled by locks. Modern engines use MVCC (Multi-Version Concurrency Control) to avoid read-write blocking.",
            "depth": "Explain the commit protocols and write-amplification differences of log-structured merge trees vs B-trees."
        },
        {
            "q": "What is the difference between a Clustered and a Non-Clustered index? How do they affect read/write performance?",
            "a": "A clustered index defines the physical order in which data rows are stored on disk. Because of this, a table can have only one clustered index, which is typically built on the primary key. Searching via a clustered index is extremely fast because the leaf nodes of the B+ tree contain the actual data rows. A non-clustered index is a separate structure from the table data; its leaf nodes contain the index key values and bookmark pointers, like a row ID or clustered key, pointing to the actual data location. Non-clustered indexes speed up secondary searches but require an extra lookup step to fetch the row data, and every additional index slows down write operations because all index trees must be updated during INSERT or UPDATE queries.",
            "keywords": ["Physical Order", "Leaf Nodes", "Bookmark Lookup", "Primary Key", "B+ Tree Updates"],
            "followups": "What is a covering index? Why do databases use B+ trees instead of binary trees?",
            "mistake": "Believing you can create multiple clustered indexes on a single table. The physical ordering constraint allows only one.",
            "depth": "Explain how B+ tree page splits occur during inserts and how fill-factors mitigate them."
        },
        {
            "q": "Compare SQL databases with NoSQL databases. When would you choose one over the other?",
            "a": "SQL databases are relational, table-based, and enforce a strict, predefined schema with strong ACID properties, making them ideal for structured data and complex joins. NoSQL databases are non-relational, schema-less, and store data in flexible formats like documents, key-values, columns, or graphs. NoSQL databases typically trade strict consistency for high write throughput and horizontal scaling across clusters, often adhering to the CAP theorem's eventual consistency. I would choose SQL for systems requiring absolute data integrity, like transaction banking or inventory systems. I would choose NoSQL for unstructured, high-volume data streams like social feeds, real-time analytics, or rapid-growth application prototypes where schemas evolve hourly.",
            "keywords": ["Relational Schemas", "Predefined Constraints", "Horizontal Scaling", "CAP Theorem", "Eventual Consistency"],
            "followups": "Explain database sharding. Differentiate document stores from key-value stores.",
            "mistake": "Thinking NoSQL databases are always faster. For complex relational queries, SQL databases are much faster and avoid manual application-layer joins.",
            "depth": "Detail CAP theorem proof and why you can only guarantee two out of Consistency, Availability, and Partition Tolerance in distributed systems."
        }
    ]
    
    p1_html = f"""
  <div class="page" id="dbms-expectedqa-new-1">
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
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">Top Expected Interview Questions</div>
        <div style="font-size: 9pt; color: #EA763F; font-weight: 700; margin-top: 2px;">Placement Q&amp;As · Created by Pranav Gawai (Part 1)</div>
      </div>
      
      <div style="display: flex; flex-direction: column; gap: 8px;">
        {render_qa_block(qas[0])}
        {render_qa_block(qas[1])}
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> DBMS <span>›</span> <span>Expected Q&amp;A</span></div>
      </div>
      <div class="page-number-premium">PAGE 36 / 40</div>
    </div>
  </div>
  """
  
    p2_html = f"""
  <div class="page" id="dbms-expectedqa-new-2">
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
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">Top Expected Interview Questions</div>
        <div style="font-size: 9pt; color: #EA763F; font-weight: 700; margin-top: 2px;">Placement Q&amp;As · Created by Pranav Gawai (Part 2)</div>
      </div>
      
      <div style="display: flex; flex-direction: column; gap: 8px;">
        {render_qa_block(qas[2])}
        {render_qa_block(qas[3])}
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> DBMS <span>›</span> <span>Expected Q&amp;A</span></div>
      </div>
      <div class="page-number-premium">PAGE 37 / 40</div>
    </div>
  </div>
  """
    return p1_html + p2_html

def render_qa_block(item):
    kw_tags = "".join([f'<span style="background: #F7FAFC; border: 1px solid #CBD5E0; padding: 1px 6px; border-radius: 4px; font-weight: bold; font-size: 7pt; color: #4A5568; text-transform: uppercase;">{kw}</span>' for kw in item['keywords']])
    return f"""
    <div style="border: 1px solid #CBD5E0; border-radius: 8px; padding: 10px 12px; background: white; display: flex; flex-direction: column; gap: 4px;">
      <div style="font-weight: 800; font-size: 9pt; color: #2B6CB0;">Q: {item['q']}</div>
      <div style="font-size: 8pt; color: #2D3748; line-height: 1.4; border-left: 3px solid #EA763F; padding-left: 8px; margin-bottom: 2px;">
        "{item['a']}"
      </div>
      <div style="display: flex; flex-wrap: wrap; gap: 4px; align-items: center; margin-top: 2px;">
        <span style="font-size: 7.5pt; font-weight: 800; color: #EA763F; text-transform: uppercase; margin-right: 4px;">Keywords:</span>
        {kw_tags}
      </div>
      <div style="font-size: 7.5pt; color: #4A5568; margin-top: 2px;">
        <strong>🔄 Follow-Up:</strong> {item['followups']}
      </div>
      <div style="font-size: 7.5pt; color: #C53030;">
        <strong>⚠️ Common Mistake:</strong> {item['mistake']}
      </div>
      <div style="font-size: 7.5pt; color: #276749;">
        <strong>📈 Expected Depth:</strong> {item['depth']}
      </div>
    </div>
"""

# ─────────────────────────────────────────
# RAPID FIRE QUESTIONS PAGE (Page 38)
# ─────────────────────────────────────────
def generate_rapid_fire_page(LOGO_BASE64):
    qas = [
        ("What is a transaction?", "A logical unit of work executing queries atomically."),
        ("What does DDL stand for?", "Data Definition Language (e.g. CREATE, DROP, ALTER)."),
        ("What does DML stand for?", "Data Manipulation Language (e.g. SELECT, INSERT, UPDATE)."),
        ("What is a candidate key?", "A minimal set of attributes that uniquely identifies a row."),
        ("What is a surrogate key?", "An artificial, system-generated primary key (like auto-increment ID)."),
        ("Difference between CHAR and VARCHAR?", "CHAR is fixed-length (padded with spaces); VARCHAR is variable-length."),
        ("What is a database view?", "A virtual table representing the output of a saved SELECT query."),
        ("What is a database trigger?", "A set of SQL actions that execute automatically on INSERT, UPDATE, or DELETE."),
        ("What is the CAP theorem?", "A distributed database can guarantee at most two of: Consistency, Availability, and Partition Tolerance."),
        ("What is write-ahead logging?", "WAL requires recording changes in a log on disk before modifying the actual DB pages."),
        ("What is database sharding?", "Horizontal partitioning of database rows across multiple server instances."),
        ("What is 2-Phase Locking (2PL)?", "A lock protocol guaranteeing serializability with growing (locking) and shrinking (unlocking) phases.")
    ]
    
    left_col_cards = "".join([render_rapid_card(q, a) for q, a in qas[:6]])
    right_col_cards = "".join([render_rapid_card(q, a) for q, a in qas[6:]])
    
    return f"""
  <div class="page" id="dbms-rapidfire-page">
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
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">DBMS Rapid Fire Questions</div>
        <div style="font-size: 9pt; color: #EA763F; font-weight: 700;">Fast-Recall Flashcards for Last-Minute Self-Testing</div>
      </div>
      
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; flex: 1;">
        <div style="display: flex; flex-direction: column; gap: 8px;">
          {left_col_cards}
        </div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
          {right_col_cards}
        </div>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> DBMS <span>›</span> <span>Rapid Fire</span></div>
      </div>
      <div class="page-number-premium">PAGE 38 / 40</div>
    </div>
  </div>
"""

def render_rapid_card(q, a):
    return f"""
    <div style="border: 1px solid #E2E8F0; border-radius: 6px; padding: 6px 8px; background: white;">
      <div style="font-weight: 800; font-size: 8pt; color: #EA763F; margin-bottom: 2px;">Q: {q}</div>
      <div style="font-size: 7.5pt; color: #4A5568; line-height: 1.3;">A: {a}</div>
    </div>
"""

# ─────────────────────────────────────────
# COMMON TRAPS PAGE (Page 39)
# ─────────────────────────────────────────
def generate_common_traps_page(LOGO_BASE64):
    traps = [
        {
            "title": "Trap 1: The NULL Equality Comparison",
            "question": 'Why does "SELECT * FROM table WHERE col = NULL" return zero records even if NULL values exist?',
            "intercept": "Correct the syntax: In SQL, NULL represents an unknown state, not a value. Standard comparison operators like `=` or `!=` fail on NULL, returning NULL (unknown) rather than TRUE. You must use the `IS NULL` or `IS NOT NULL` operators to check for NULL values."
        },
        {
            "title": "Trap 2: The MVCC Isolation Lock Myth",
            "question": "Does isolation in transactional databases mean that reading a row always locks it?",
            "intercept": "Clarify that modern relational database engines use Multi-Version Concurrency Control (MVCC). Readers do not block writers, and writers do not block readers. The engine creates temporary versioned snapshots of the data, so read transactions query a point-in-time state without acquiring locks."
        },
        {
            "title": "Trap 3: The 3NF vs BCNF Equivalence",
            "question": "If a table is in 3NF and has no overlapping candidate keys, is it automatically in BCNF?",
            "intercept": "Yes. BCNF only differs from 3NF when there are overlapping candidate keys. If a table has only a single candidate key (or completely disjoint candidate keys) and is in 3NF, it is guaranteed to be in BCNF because no non-trivial dependencies on key subsets can exist."
        },
        {
            "title": "Trap 4: Indexing Everything Performance",
            "question": "To optimize database performance, shouldn't we add an index on every single column in the table?",
            "intercept": "Explain the massive drawback: While indexing speeds up read queries, it significantly degrades write performance (INSERT, UPDATE, DELETE) because the database must update the B+ tree index structure for every index on the table. It also consumes excessive disk space."
        },
        {
            "title": "Trap 5: Trigger transactional scope",
            "question": "If a trigger fails during an INSERT operation, does the original INSERT still commit?",
            "intercept": "No. Triggers execute within the same transactional context as the triggering statement. If the trigger raises an error or fails, the database rolls back the entire transaction, meaning the original INSERT is cancelled and not committed."
        }
    ]
    
    rows = ""
    for item in traps:
        rows += f"""
        <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 8px 10px; background: white; margin-bottom: 6px;">
          <div style="font-weight: 800; font-size: 8.5pt; color: #C53030; margin-bottom: 2px;">{item['title']}</div>
          <div style="font-size: 7.5pt; font-style: italic; color: #4A5568; margin-bottom: 4px;">Interviewer: "{item['question']}"</div>
          <div style="font-size: 7.5pt; color: #2D3748; line-height: 1.35; border-left: 2px solid #E53E3E; padding-left: 6px;">
            <strong>Deflection:</strong> {item['intercept']}
          </div>
        </div>
        """
        
    return f"""
  <div class="page" id="dbms-commontraps-page">
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
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">DBMS Common Traps &amp; Deflections</div>
        <div style="font-size: 9pt; color: #E53E3E; font-weight: 700;">Tactical Responses to Deflect Tricky Placement Questions</div>
      </div>
      
      <div style="flex: 1; display: flex; flex-direction: column; justify-content: center;">
        {rows}
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> DBMS <span>›</span> <span>Common Traps</span></div>
      </div>
      <div class="page-number-premium">PAGE 39 / 40</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# BLANK NOTES PAGES (2 Pages)
# ─────────────────────────────────────────
blank_notes_pages = f"""
  <div class="page" id="dbms-notes-1">
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
      <div style="font-size: 16pt; font-weight: 800; color: #111; border-bottom: 2px solid #EA763F; padding-bottom: 6px; margin-bottom: 12px;">Personal Notes &amp; Scribbles</div>
      <div class="notes-lines" style="flex: 1; background-image: linear-gradient(#E2E8F0 1px, transparent 1px); background-size: 100% 24px; line-height: 24px; margin-top: 10px;"></div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> DBMS <span>›</span> <span>Notes</span></div>
      </div>
      <div class="page-number-premium">PAGE 40 / 40</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# COMPILING HTML PAGES
# ─────────────────────────────────────────
total_content_pages = len(topics)
content_pages_html = "".join([generate_page(t, i+4, 40) for i, t in enumerate(topics)])
comparison_cheat_sheet_html = generate_comparison_cheat_sheet(LOGO_BASE64)
expected_qa_html = generate_expected_qa_pages_new(LOGO_BASE64)
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
  .cover-title {{ font-size: 42pt; font-weight: 800; color: #111; line-height: 1.1; margin-bottom: 30px; letter-spacing: -1.5px; }}
  .cover-subtitle {{ font-size: 18pt; color: #666; font-weight: 600; margin-bottom: 60px; }}
  .cover-footer {{ position: absolute; bottom: 60px; font-size: 12pt; font-weight: 800; color: #888; letter-spacing: 1px; display: flex; align-items: center; gap: 12px; }}
  .cover-footer img {{ height: 24px; }}
  .cover-footer a {{ text-decoration: none; color: inherit; }}
 
  /* TOC PAGE */
  .toc-page {{ justify-content: flex-start; }}
  .toc-inner {{ padding: 30px 40px; width: 100%; }}
 
  /* HEADER */
  .header {{ background: #EA763F; height: 14mm; display: flex; justify-content: space-between; align-items: center; padding: 0 24px; color: white; flex-shrink: 0; margin-top: 5mm; margin-left: 5mm; margin-right: 5mm; }}
  .header-left {{ display: flex; align-items: center; gap: 12px; }}
  .header-logo {{ height: 8mm; filter: brightness(0) invert(1); }}
  .header-wordmark {{ font-size: 16pt; font-weight: 800; letter-spacing: -0.5px; }}
  .header-right {{ display: flex; align-items: center; gap: 8px; }}
  .badge-yield {{ background: #FFF; color: #E53E3E; padding: 4px 10px; border-radius: 20px; font-weight: 800; font-size: 8.5pt; display: flex; align-items: center; gap: 4px; }}
  .header-badge {{ background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 4px; font-weight: 700; font-size: 10pt; }}
 
  /* TOPIC BAR */
  .topic-bar {{ padding: 14px 24px; border-bottom: 2px solid #EBE5DB; background: white; flex-shrink: 0; margin-left: 5mm; margin-right: 5mm; }}
  .topic-bar-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }}
  .topic-eyebrow {{ font-size: 9pt; color: #EA763F; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px; }}
  .yield-rating {{ font-size: 9pt; font-weight: 800; color: #4A5568; }}
  .stars-gold {{ color: #D69E2E; font-size: 10pt; letter-spacing: 1px; }}
  .topic-title {{ font-size: 19pt; font-weight: 800; color: #111; margin-bottom: 2px; letter-spacing: -0.5px; }}
  .topic-subtitle {{ font-size: 9.5pt; color: #666; font-weight: 600; line-height: 1.3; }}
 
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
 
  /* FOOTER WITH PREMIUM PAGE NUMBERS */
  .footer {{ height: 36px; background: white; border-top: 1px solid #EDE5D8; display: flex; justify-content: space-between; align-items: center; padding: 0 24px; font-size: 8.5pt; color: #718096; flex-shrink: 0; font-weight: 700; margin-bottom: 5mm; margin-left: 5mm; margin-right: 5mm; }}
  .footer-left {{ display: flex; align-items: center; gap: 8px; }}
  .footer-logo {{ height: 14px; }}
  .breadcrumb {{ color: #A0AEC0; }}
  .breadcrumb span {{ color: #4A5568; font-weight: 800; margin: 0 4px; }}
  .page-number-premium {{ font-size: 8.5pt; font-weight: 800; color: #EA763F; letter-spacing: 1px; background: #FFF5F0; padding: 3px 10px; border-radius: 4px; border: 1px solid #FBD38D; }}
 
  /* BOTTOM PLACEMENT GRID (L4) */
  .bottom-placement-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 8px;
    padding: 10px 16px;
    background: #FDFBF7;
    border-top: 2px solid #EBE5DB;
    flex-shrink: 0;
    min-height: 140px;
    max-height: 155px;
    margin-left: 5mm;
    margin-right: 5mm;
  }}
  .placement-block {{
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 8pt;
    line-height: 1.35;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .placement-block-title {{
    font-size: 7.5pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 2px;
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
"""

# Compile final template
html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>DBMS Placement Handbook</title>
<style>{css}</style>
</head>
<body>
  <!-- COVER PAGE -->
  <div class="page cover-page" id="dbms-cover">
    <div class="cover-logo-container">
      <img src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS">
    </div>
    <div class="cover-eyebrow">Core Computer Science</div>
    <div class="cover-title">Database<br>Management Systems</div>
    <div class="cover-subtitle">Placement Preparation Notes</div>
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

  <!-- FINAL REVISION SHEET -->
  {final_revision_page}

  <!-- COMPARISON CHEAT SHEET -->
  {comparison_cheat_sheet_html}

  <!-- EXPECTED Q&A PAGES -->
  {expected_qa_html}

  <!-- RAPID FIRE PAGE -->
  {rapid_fire_html}

  <!-- COMMON TRAPS PAGE -->
  {common_traps_html}

  <!-- BLANK NOTES PAGES -->
  {blank_notes_pages}
</body>
</html>
"""

# Write to file
os.makedirs("subjects/dbms", exist_ok=True)
output_path = "subjects/dbms/01_dbms_notes.html"
with open(output_path, "w") as f:
    f.write(html_out)

print(f"Generated complete Database Systems Handbook with {len(topics)} topics.")
