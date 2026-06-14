import base64
import os

# Load logo
with open("../logo.png", "rb") as img_file:
    LOGO_BASE64 = base64.b64encode(img_file.read()).decode('utf-8')

# PROJECTS AND THEIR 18 SECTIONS
projects_data = [
    # ── TIER 1: CRAFTASTUDIO ──
    {
        "name": "CraftaStudio",
        "subtitle": "AI-Powered Structural Code Generation & Topological Graph Engine",
        "tagline": "AI Code Gen",
        "sections": {
            "01": {
                "type": "case-study",
                "title": "Executive Summary",
                "content": """
                <div class="case-study-grid">
                  <div class="cs-card">
                    <div class="cs-card-title">🚨 The Core Problem</div>
                    <p>Standard LLMs output code sequentially, leading to context truncation, lost parameters, and broken interfaces when generating multi-file, full-stack architectures (API, database, and UI layers).</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">👥 Target Users & Value</div>
                    <p>Developers and startup teams building rapid MVPs. It saves hours of boilerplate coding by ensuring generated code compiles immediately with zero-configuration interfaces.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">🎯 Business Goal & Impact</div>
                    <p>Reduce MVP time-to-market by 80%. CraftaStudio guarantees type-safe connections between backend schemas and frontend components, eliminating compilation errors.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">👑 My Role & Ownership</div>
                    <p><strong>Core Architect & Tech Lead</strong>. Designed the in-memory DAG scheduler, the LLM fallback pipeline, and the sandboxed preview compilation container.</p>
                  </div>
                </div>
                """
            },
            "02": {
                "type": "system",
                "title": "Product Vision",
                "content": """
                <div class="system-section">
                  <h3>Why We Built It</h3>
                  <p>Existing tools generate single-file snippets that drop structural context. CraftaStudio was built to treat codebase creation as a graph problem: compiling English requirements into a visual Directed Acyclic Graph (DAG) before generating a single line of code.</p>
                  <h3>Key Alternatives Analyzed</h3>
                  <table class="visual-table">
                    <thead>
                      <tr><th>Alternative</th><th>Drawback</th><th>CraftaStudio Advantage</th></tr>
                    </thead>
                    <tbody>
                      <tr><td>Copilot / Cursor</td><td>Auto-complements single files; lacks global structural coordination.</td><td>Orchestrates complete multi-file migrations.</td></tr>
                      <tr><td>v0 / Bolt.new</td><td>Mainly frontend UI mockups; database layers are mocked.</td><td>Full-stack sync with active database mapping.</td></tr>
                    </tbody>
                  </table>
                  <h3>Core Feature Matrix</h3>
                  <ul>
                    <li><strong>Graphical Editor:</strong> Real-time Node Canvas built using ReactFlow.</li>
                    <li><strong>Context Scaffolder:</strong> Injects parent node types directly into child LLM prompts.</li>
                    <li><strong>Sandboxed Previews:</strong> Executes code inside micro-containers for verification.</li>
                  </ul>
                </div>
                """
            },
            "03": {
                "type": "comparison",
                "title": "Tech Stack Deep Dive",
                "content": """
                <table class="comparison-table">
                  <thead>
                    <tr><th>Layer</th><th>Tech Chosen</th><th>Key Reason / Why</th><th>Trade-offs & Constraints</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>Frontend</strong></td>
                      <td>Next.js / ReactFlow</td>
                      <td>Server-side rendering for speed; ReactFlow handles complex graphical node layouts.</td>
                      <td>Heavier JavaScript bundles; state synchronization overhead.</td>
                    </tr>
                    <tr>
                      <td><strong>Backend</strong></td>
                      <td>Node.js / Express</td>
                      <td>Non-blocking I/O is ideal for real-time WebSocket canvas synchronization.</td>
                      <td>Single-threaded; heavy calculations block the event loop.</td>
                    </tr>
                    <tr>
                      <td><strong>Agent Engine</strong></td>
                      <td>FastAPI / Python</td>
                      <td>Rich ecosystem for parsing dependency graphs and executing agentic tools.</td>
                      <td>Slower cold-starts compared to compiled languages.</td>
                    </tr>
                    <tr>
                      <td><strong>Database</strong></td>
                      <td>PostgreSQL / Prisma</td>
                      <td>Strict relational integrity (foreign keys) to prevent broken edge mappings.</td>
                      <td>Vertical scale limitations; requires replica configurations.</td>
                    </tr>
                    <tr>
                      <td><strong>AI Models</strong></td>
                      <td>Groq Llama-3.1</td>
                      <td>Ultra-low token latency (<30ms time-to-first-token) for fluid canvas changes.</td>
                      <td>Context limit window of 8K tokens; requires aggressive pruning.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            "04": {
                "type": "architecture",
                "title": "High-Level Architecture",
                "content": """
                <div class="arch-diagram">
+--------------------+      HTTP/WS      +--------------------+      Redis      +--------------------+
|  Next.js Canvas    | ----------------> |  Node.js Gateway   | --------------> | Upstash Job Queue  |
| (ReactFlow UI)     |                   |  (Auth & DB Sync)  |                 +--------------------+
+--------------------+                   +--------------------+                            |
          ^                                        | PostgreSQL                            | Task Trigger
          | WebSockets                             v                                       v
+--------------------+                   +--------------------+                 +--------------------+
| Socket.io Server   | <---------------- | Prisma DB Client   | <-------------- | FastAPI Agent      |
| (Realtime Updates) |                   +--------------------+                 | (Graph Execution)  |
+--------------------+                                                          +--------------------+
                                                                                           | LLM API
                                                                                           v
                                                                                +--------------------+
                                                                                | Groq / Llama 3 API |
                                                                                +--------------------+
                </div>
                <div class="arch-description">
                  <p><strong>Canvas Client:</strong> Renders ReactFlow components and streams user mutations over secure WebSockets to the Node.js gateway.</p>
                  <p><strong>Gateway:</strong> Verifies authorization, updates the graph state in PostgreSQL, and queues execution tasks into Upstash Redis.</p>
                  <p><strong>Agent Executor:</strong> Reads from the queue, performs topological graph sorting, and executes context-isolated code generation loops via the Groq API.</p>
                </div>
                """
            },
            "05": {
                "type": "flow",
                "title": "Request & Execution Flow",
                "content": """
                <div class="flow-diagram">
User Canvas               Node.js Gateway               Upstash Queue              FastAPI Agent              Groq API
    |                           |                            |                           |                       |
    |-- 1. Prompt Canvas Edges ->|                            |                           |                       |
    |                           |-- 2. Validate & Store ---->|                           |                       |
    |                           |-- 3. Queue Execution Block --------------------------->|                       |
    |                           |                            |                           |-- 4. Get Context ---->|
    |                           |                            |                           |<-- 5. Send Prompt ----|
    |                           |                            |                           |-- 6. Generate Code -->|
    |                           |                            |                           |<- 7. Raw JSON Code ---|
    |<-- 8. Broadcast Code WS --|                            |                           |                       |
                </div>
                <div class="flow-steps">
                  <ol>
                    <li><strong>Ingestion:</strong> The user inputs prompts into the canvas nodes. Nodes transition to `pending_generation`.</li>
                    <li><strong>Scheduling:</strong> The Node.js gateway validates constraints and pushes tasks to the Upstash execution queue.</li>
                    <li><strong>Context Assembly:</strong> The FastAPI agent reads child nodes and merges parent output signatures into the prompt context.</li>
                    <li><strong>Execution & Broadcast:</strong> The agent receives code from Groq, validates syntax, writes to DB, and triggers a WebSocket broadcast to render code.</li>
                  </ol>
                </div>
                """
            },
            "06": {
                "type": "database",
                "title": "Database Design",
                "content": """
                <table class="db-table">
                  <thead>
                    <tr><th>Table</th><th>Fields</th><th>Types & Constraints</th><th>Indexes & Scaling</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>Project</strong></td>
                      <td>id (PK), userId, name, createdAt</td>
                      <td>UUID, NOT NULL</td>
                      <td>Index on `userId`.</td>
                    </tr>
                    <tr>
                      <td><strong>BlockNode</strong></td>
                      <td>id (PK), projectId (FK), type, name, code, status</td>
                      <td>VARCHAR, TEXT, Enum</td>
                      <td>Composite index on `(projectId, status)`.</td>
                    </tr>
                    <tr>
                      <td><strong>BlockEdge</strong></td>
                      <td>id (PK), projectId (FK), sourceId (FK), targetId (FK)</td>
                      <td>UUID, FOREIGN KEYS</td>
                      <td>Index on `sourceId` for fast traversal.</td>
                    </tr>
                  </tbody>
                </table>
                <div class="db-notes">
                  <p><strong>Relationships:</strong> A `Project` has one-to-many `BlockNode`s and `BlockEdge`s. Deleting a project cascades deletions to all nodes and edges.</p>
                  <p><strong>Optimization Decisions:</strong> We store code outputs in PostgreSQL as `TEXT` rather than nested JSON to leverage native database compression and speed up lookup operations.</p>
                </div>
                """
            },
            "07": {
                "type": "flow",
                "title": "Authentication Architecture",
                "content": """
                <div class="flow-diagram">
Client                    Clerk OAuth                 Node.js Gateway             Prisma (Postgres)
  |                            |                             |                            |
  |-- 1. Login Request ------->|                             |                            |
  |<-- 2. Signed Token JWT ----|                             |                            |
  |-- 3. API Call with JWT --------------------------------->|                            |
  |                            |                             |-- 4. Verify Signature ---->|
  |                            |                             |-- 5. Query Project (RLS) ->|
  |                            |                             |<-- 6. Grant / Deny Access -|
                </div>
                <div class="auth-details">
                  <p><strong>Token Issuance:</strong> Authentication is delegated to Clerk via OAuth 2.0. A JWT is issued to the client with custom claims for user permissions.</p>
                  <p><strong>Row-Level Protection:</strong> Every database query through Prisma includes a global filter: `where: { userId: currentUserId }`. This ensures data isolation at the ORM layer, preventing cross-tenant access bugs.</p>
                </div>
                """
            },
            "08": {
                "type": "system",
                "title": "Core Engineering Systems",
                "content": """
                <div class="system-section">
                  <h3>Topological Dependency Graph Engine</h3>
                  <p>When the user clicks "Build Codebase", we cannot compile nodes in parallel because a database model node must exist before an API endpoint can reference it. The scheduler implements <strong>Kahn's Algorithm</strong> for topological sorting:</p>
                  <pre style="background:#F7FAFC; padding:6px; border-radius:4px; font-family:monospace; font-size:7pt;">
def topological_sort(nodes, edges):
    in_degree = {n.id: 0 for n in nodes}
    for e in edges: in_degree[e.targetId] += 1
    queue = [n for n in nodes if in_degree[n.id] == 0]
    order = []
    while queue:
        curr = queue.pop(0)
        order.append(curr)
        for e in [x for x in edges if x.sourceId == curr.id]:
            in_degree[e.targetId] -= 1
            if in_degree[e.targetId] == 0:
                queue.append(next(n for n in nodes if n.id == e.targetId))
    return order</pre>
                  <h3>Loop Detection (Tarjan's SCC)</h3>
                  <p>To prevent execution deadlocks, Tarjan's Strongly Connected Components (SCC) algorithm runs on graph mutations. If a cycle is detected (e.g., Node A depends on Node B, which depends on Node A), the editor rejects the canvas link.</p>
                </div>
                """
            },
            "09": {
                "type": "comparison",
                "title": "Scalability Design",
                "content": """
                <table class="comparison-table">
                  <thead>
                    <tr><th>Scale</th><th>Bottleneck</th><th>Architectural Solution</th><th>Trade-offs</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>100 Users</strong></td>
                      <td>Concurrency lag in canvas state updates.</td>
                      <td>WebSocket scaling via Node.js memory arrays.</td>
                      <td>Server crashes drop client sessions.</td>
                    </tr>
                    <tr>
                      <td><strong>1,000 Users</strong></td>
                      <td>PostgreSQL pool exhaust on high read cycles.</td>
                      <td>Connection pooling via PgBouncer.</td>
                      <td>Adds network hop latency.</td>
                    </tr>
                    <tr>
                      <td><strong>10,000 Users</strong></td>
                      <td>LLM rate limits (TPM/RPM limits hit).</td>
                      <td>Multi-provider model fallback pipeline (Groq -> Bedrock).</td>
                      <td> Bedrock has higher latency profile.</td>
                    </tr>
                    <tr>
                      <td><strong>100k+ Users</strong></td>
                      <td>High job queues backlog times.</td>
                      <td>Distributed worker nodes running on AWS ECS.</td>
                      <td>Complex container state sync.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            "10": {
                "type": "system",
                "title": "Failure Handling & Recovery",
                "content": """
                <div class="system-section">
                  <h3>Robust Fault Tolerance</h3>
                  <p>Because code generation relies on external LLM inference hosts, the system is designed with multiple fallback fail-safes:</p>
                  <ul>
                    <li><strong>API Failure:</strong> Handled using exponential backoff with jitter. If the Groq endpoint returns HTTP 429, the system waits `2^retry_count + random(100ms)` before retrying.</li>
                    <li><strong>Worker Failure:</strong> Upstash Redis queues use a Dead Letter Queue (DLQ) pattern. If a worker drops a code compilation task three times, it is stored in DLQ and marked as failed on the user UI.</li>
                    <li><strong>JSON Parse Failure:</strong> If the model outputs conversational markdown code block brackets (e.g., ```json ... ```), our parser strips the wrapper. If syntax errors exist, a regex repair engine automatically inserts missing brackets before giving up.</li>
                  </ul>
                </div>
                """
            },
            "11": {
                "type": "system",
                "title": "Monitoring & Observability",
                "content": """
                <div class="system-section">
                  <h3>Metrics & OpenTelemetry Tracing</h3>
                  <p>We trace every request using Prometheus and Grafana dashboards to monitor latency profiles:</p>
                  <ul>
                    <li><strong>Health Checks:</strong> Endpoint `/api/health` polls node dependencies and database connections every 10 seconds.</li>
                    <li><strong>LLM Latency Tracing:</strong> OpenTelemetry tracks Groq's TTFT (Time To First Token) and total output token generation times.</li>
                    <li><strong>Queue Metrics:</strong> Alerts fire in Slack if Upstash queue backlogs exceed 100 pending items.</li>
                  </ul>
                </div>
                """
            },
            "12": {
                "type": "system",
                "title": "Cost Optimization",
                "content": """
                <div class="system-section">
                  <h3>LLM and Infrastructure Savings</h3>
                  <p>In production, API costs can scale quadratically with active users. We apply the following optimizations:</p>
                  <ul>
                    <li><strong>Prompt Caching:</strong> Node prompt templates are static. We set headers to allow LLM endpoint caching of system instructions.</li>
                    <li><strong>Model Routing:</strong> We use Llama 3 8B (extremely cheap) for graph analysis and layout generation, routing only code compilation prompts to Llama 3 70B.</li>
                    <li><strong>Aggressive Caching:</strong> Compiled components are cached in Redis. If a node's requirements and parent schemas have not mutated, we skip LLM generation entirely and load from cache.</li>
                  </ul>
                </div>
                """
            },
            "13": {
                "type": "system",
                "title": "Security Review",
                "content": """
                <div class="system-section">
                  <h3>Security Threat Modeling</h3>
                  <ul>
                    <li><strong>Threat: Code Injection.</strong> Users might craft prompts that force the agent to run dangerous terminal commands.</li>
                    <li><strong>Mitigation:</strong> Generated code is NEVER executed on the host system. It runs inside isolated WebContainers in the browser sandbox.</li>
                    <li><strong>Threat: Secret Leaks.</strong> API keys could leak via repository outputs.</li>
                    <li><strong>Mitigation:</strong> Environment variables are encrypted at rest using AES-256 and injected into compilation runs via Vault.</li>
                  </ul>
                </div>
                """
            },
            "14": {
                "type": "case-study",
                "title": "Engineering Challenges",
                "content": """
                <div class="case-study-grid">
                  <div class="cs-card">
                    <div class="cs-card-title">🔥 Production Incident</div>
                    <p>The "Circular Loop Hang": When a user accidentally connected Node A to B, and B to A, the scheduler went into an infinite memory leak loop, crashing Node.js servers.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">🔎 Root Cause Analysis</div>
                    <p>The original scheduling array lacked cycle detection. It assumed the graph was a strict DAG, so Kahn's algorithm stayed in an infinite while-loop seeking nodes with in-degree 0.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">🛠️ The Fix Patch</div>
                    <p>Implemented a pre-save check that uses Tarjan's SCC algorithm. If a loop is found, the relation is blocked. Also, added a safety iteration limit counter to the while-loop.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">📈 Key Lessons</div>
                    <p>Never trust client-side validation logic. Even if the ReactFlow canvas UI blocks loops, database constraints and API validation logic must independently enforce data integrity.</p>
                  </div>
                </div>
                """
            },
            "15": {
                "type": "system",
                "title": "Future Roadmap",
                "content": """
                <div class="system-section">
                  <h3>Development Timeline</h3>
                  <ul>
                    <li><strong>Version 2: Real-time Multi-User Collaboration.</strong> Integrating Yjs (CRDT) for Google Docs-like canvas editing and remote state synchronization.</li>
                    <li><strong>Version 3: Self-Correction Sandbox.</strong> Implementing an execution loop where the compiler catches syntax/TypeScript errors and feeds them back into the LLM prompt to automatically self-repair.</li>
                  </ul>
                </div>
                """
            },
            "16": {
                "type": "interview",
                "title": "Interview Deep Dive",
                "content": """
                <div class="interview-qa">
                  <div class="qa-block">
                    <div class="question-header">Q: How do you handle LLM context limits when generating a multi-file system?</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> We apply DAG decomposition. Instead of generating the entire codebase in one prompt, we generate code module-by-module. Parent node typescript interfaces are injected as static contexts into child prompts, keeping active token counts under 3K.</p>
                    </div>
                  </div>
                  <div class="qa-block">
                    <div class="question-header">Q: Why choose WebSockets over polling for canvas generation updates?</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> WebSockets reduce DB polling overhead. When the agent completes generation, the Node.js server immediately emits the update to the client. This saves database connection read cycles compared to client HTTP polling.</p>
                    </div>
                  </div>
                </div>
                """
            },
            "17": {
                "type": "interview",
                "title": "Top Project Questions",
                "content": """
                <div class="interview-qa">
                  <div class="qa-block">
                    <div class="question-header">Question: "What is Kahn's algorithm, and how is it used in your graph compilation?"</div>
                    <div class="model-answer">
                      <p><strong>Interview-Ready Answer:</strong> Kahn's algorithm is a topological sorting method that resolves node dependencies. We count the dependencies of each node (in-degrees). Nodes with 0 dependencies are processed first. As they complete, we decrement the count of child nodes and queue them as they hit 0.</p>
                      <div class="buzzword-tags" style="margin-top: 4px;">
                        <span class="buzz-tag">Topological Sort</span>
                        <span class="buzz-tag">In-Degree Queue</span>
                        <span class="buzz-tag">DAG Scheduler</span>
                      </div>
                    </div>
                  </div>
                  <div class="qa-block">
                    <div class="question-header">Question: "What common mistake did you make when scaling WebSockets?"</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> Believing standard WebSockets scale horizontally out-of-the-box. When we spun up a second API container, clients connected to different nodes could not talk to each other. We resolved this by integrating a Redis Adapter for messaging sync.</p>
                    </div>
                  </div>
                </div>
                """
            },
            "18": {
                "type": "revision",
                "title": "One Page Revision",
                "content": """
                <div class="revision-grid">
                  <div class="rev-card">
                    <div class="rev-card-title">Architecture</div>
                    <p>ReactFlow Canvas UI -> Node.js Backend -> Upstash Job Queue -> Python FastAPI Agent -> Llama-3 API -> PostgreSQL DB.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Database</div>
                    <p>Relational SQL tables mapping Project (1) -> Node (N), and Edges. Composite indexes on query paths.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Scaling</div>
                    <p>PgBouncer for connections, Upstash Redis queue for tasks, API fallbacks for rate-limit protection.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Security</div>
                    <p>Zero-trust client access, in-browser WebContainer code sandboxing, environment variable encryption.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Tech Stack</div>
                    <p>Next.js, Node.js, Python, PostgreSQL, Prisma, Redis, Groq Llama-3.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Key Challenge</div>
                    <p>Circular dependency memory leak solved by integrating pre-save loop checks via Tarjan's SCC.</p>
                  </div>
                </div>
                """
            }
        }
    },
    # ── TIER 1: PLACEPRO ──
    {
        "name": "PlacePro",
        "subtitle": "Campus Placement Management System with Real-Time Event Bus & Row-Level Security",
        "tagline": "Placement Portal",
        "sections": {
            "01": {
                "type": "case-study",
                "title": "Executive Summary",
                "content": """
                <div class="case-study-grid">
                  <div class="cs-card">
                    <div class="cs-card-title">🚨 The Core Problem</div>
                    <p>High concurrent load crashes placement portals during short registration windows. Insecure API routing often allows students to manipulate candidate application records.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">👥 Target Users & Value</div>
                    <p>University coordinators and students. Streamlines job applications, eligibility screening, and company recruitment updates in real-time.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">🎯 Business Goal & Impact</div>
                    <p>Support up to 10,000 concurrent registrations without server drops, ensuring zero lost applications and strict data compliance regulations.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">👑 My Role & Ownership</div>
                    <p><strong>System Architect & Backend Engineer</strong>. Implemented Row-Level Security (RLS) policies in PostgreSQL, and designed the real-time notification engine using Redis Pub/Sub.</p>
                  </div>
                </div>
                """
            },
            "02": {
                "type": "system",
                "title": "Product Vision",
                "content": """
                <div class="system-section">
                  <h3>Why We Built It</h3>
                  <p>Traditional university placement portals lack real-time reactivity and fail under peak loads. PlacePro was designed to handle high write-concurrency with atomic transaction states and instant status broadcasts.</p>
                  <h3>Key Alternatives Analyzed</h3>
                  <table class="visual-table">
                    <thead>
                      <tr><th>Alternative</th><th>Drawback</th><th>PlacePro Advantage</th></tr>
                    </thead>
                    <tbody>
                      <tr><td>Google Sheets</td><td>Concurrent locking conflicts; zero access security.</td><td>Real-time concurrency controls with RLS.</td></tr>
                      <tr><td>Legacy ERPs</td><td>Slow UI load times; manual eligibility reviews.</td><td>Automated instant eligibility matching engine.</td></tr>
                    </tbody>
                  </table>
                  <h3>Core Feature Matrix</h3>
                  <ul>
                    <li><strong>Auto-Filter Eligibility:</strong> Disallows applications matching backlog/CGPA caps.</li>
                    <li><strong>Live Status Logs:</strong> SSE updates on company process progress.</li>
                    <li><strong>Secure Isolation:</strong> Role isolation mapping recruiters, students, and admins.</li>
                  </ul>
                </div>
                """
            },
            "03": {
                "type": "comparison",
                "title": "Tech Stack Deep Dive",
                "content": """
                <table class="comparison-table">
                  <thead>
                    <tr><th>Layer</th><th>Tech Chosen</th><th>Key Reason / Why</th><th>Trade-offs & Constraints</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>Frontend</strong></td>
                      <td>Next.js / Tailwind CSS</td>
                      <td>Server-side validation checks; rapid stylesheet styling for clean dashboards.</td>
                      <td>Routing setups can introduce client bundle weight.</td>
                    </tr>
                    <tr>
                      <td><strong>Backend</strong></td>
                      <td>FastAPI</td>
                      <td>High asynchronous execution throughput; automatic API docs generation.</td>
                      <td>Fewer middleware libraries compared to Express.js.</td>
                    </tr>
                    <tr>
                      <td><strong>Database</strong></td>
                      <td>PostgreSQL (Supabase)</td>
                      <td>SQL relational integrity combined with PostgreSQL Row-Level Security.</td>
                      <td>Connection limit bottlenecks on high parallel runs.</td>
                    </tr>
                    <tr>
                      <td><strong>Message Bus</strong></td>
                      <td>Redis Pub/Sub</td>
                      <td>Sub-millisecond pub/sub broadcasting for real-time application updates.</td>
                      <td>In-memory only; does not persist historic notification queues.</td>
                    </tr>
                    <tr>
                      <td><strong>Container</strong></td>
                      <td>Docker / AWS ECS</td>
                      <td>Containerized micro-services for autoscaling during active drives.</td>
                      <td>Requires configuration overhead for task definitions.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            "04": {
                "type": "architecture",
                "title": "High-Level Architecture",
                "content": """
                <div class="arch-diagram">
+--------------------+      HTTPS        +--------------------+      Pub/Sub    +--------------------+
|  Next.js App       | ----------------> | Load Balancer      | --------------> | Redis Server       |
|  (Student/Recruit) |                   | (Nginx Round Robin)|                 | (Live Events Cache)|
+--------------------+                   +--------------------+                 +--------------------+
          ^                                        |                                       |
          | Server Sent Events (SSE)               v                                       |
+--------------------+                   +--------------------+                            | Broadcast
| SSE Notification   | <---------------- | FastAPI Web Nodes  | <--------------------------+
| Gateway            |                   +--------------------+
+--------------------+                             | PostgreSQL Connection
                                                   v
                                         +--------------------+
                                         | Supabase Postgres  |
                                         | (RLS Enforcement)  |
                                         +--------------------+
                </div>
                <div class="arch-description">
                  <p><strong>Nginx Load Balancer:</strong> Distributes user requests across multiple web servers using a round-robin scheduling algorithm.</p>
                  <p><strong>FastAPI Web Nodes:</strong> Stateless app containers that process business logic, queries database, and publishes event notifications to Redis.</p>
                  <p><strong>Row-Level Security PostgreSQL:</strong> Enforces data isolation policies at the query parser level rather than the application code.</p>
                </div>
                """
            },
            "05": {
                "type": "flow",
                "title": "Request & Execution Flow",
                "content": """
                <div class="flow-diagram">
Student                   FastAPI App                 PostgreSQL DB               Redis Engine           Coordinator UI
  |                            |                            |                           |                      |
  |-- 1. Apply to Job Posting ->|                            |                           |                      |
  |                            |-- 2. Verify Eligibility -->|                           |                      |
  |                            |-- 3. Save Application ---->|                           |                      |
  |                            |<-- 4. Confirmed Write -----|                           |                      |
  |                            |-- 5. Publish Event Notification ---------------------->|                      |
  |                            |                            |                           |-- 6. SSE Broadcast ->|
  |<-- 7. Confirmed Application|                            |                           |                      |
                </div>
                <div class="flow-steps">
                  <ol>
                    <li><strong>Application Request:</strong> Student submits job application.</li>
                    <li><strong>Eligibility Check:</strong> FastAPI queries the student's profile (CGPA, active backlogs) against job criteria.</li>
                    <li><strong>DB Transaction:</strong> Writes application row inside a transaction lock to prevent race conditions.</li>
                    <li><strong>Event Dispatch:</strong> On successful write, an event is published to Redis, broadcasting updates to coordinator panels in real-time.</li>
                  </ol>
                </div>
                """
            },
            "06": {
                "type": "database",
                "title": "Database Design",
                "content": """
                <table class="db-table">
                  <thead>
                    <tr><th>Table</th><th>Fields</th><th>Types & Constraints</th><th>Indexes & Scaling</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>Student</strong></td>
                      <td>id (PK), name, cgpa, backlogs, branch</td>
                      <td>UUID, DECIMAL, INT</td>
                      <td>Index on `branch`.</td>
                    </tr>
                    <tr>
                      <td><strong>JobPosting</strong></td>
                      <td>id (PK), company, minCgpa, maxBacklogs</td>
                      <td>UUID, VARCHAR, DECIMAL</td>
                      <td>Index on `company`.</td>
                    </tr>
                    <tr>
                      <td><strong>Application</strong></td>
                      <td>id (PK), studentId (FK), jobId (FK), status</td>
                      <td>UUID, Enum, NOT NULL</td>
                      <td>Unique index on `(studentId, jobId)`.</td>
                    </tr>
                  </tbody>
                </table>
                <div class="db-notes">
                  <p><strong>RLS Policies:</strong> `CREATE POLICY student_isolation ON "Application" FOR ALL USING (auth.uid() = studentId);` ensures students can only read and write their own applications.</p>
                  <p><strong>Indexing Strategy:</strong> A composite index is defined on `(studentId, jobId)` to guarantee that no student can apply to the same job posting more than once.</p>
                </div>
                """
            },
            "07": {
                "type": "flow",
                "title": "Authentication Architecture",
                "content": """
                <div class="flow-diagram">
Client Client             Auth Server (Supabase)       FastAPI Backend             PostgreSQL (RLS)
  |                            |                             |                            |
  |-- 1. Sign In Credentials ->|                             |                            |
  |<-- 2. JWT Access Token ----|                             |                            |
  |-- 3. GET /applications (Token) ------------------------->|                            |
  |                            |                             |-- 4. Parse JWT Claims ---->|
  |                            |                             |-- 5. Execute Select ------->|
  |                            |                             |<-- 6. Filtered Rows (RLS) -|
                </div>
                <div class="auth-details">
                  <p><strong>Role-Based Access Control (RBAC):</strong> JWT tokens contain a claims array mapping roles: `student`, `recruiter`, or `admin`.</p>
                  <p><strong>Postgres RLS Layer:</strong> We configure RLS policies so recruiters can view applications only for jobs matching their `companyId` header check.</p>
                </div>
                """
            },
            "08": {
                "type": "system",
                "title": "Core Engineering Systems",
                "content": """
                <div class="system-section">
                  <h3>Automated Eligibility Engine</h3>
                  <p>During active campus placement drives, thousands of students apply to jobs simultaneously. Evaluating applicant CGPA and backlog criteria in application code causes scaling bottlenecks. PlacePro implements a database-level selection engine:</p>
                  <pre style="background:#F7FAFC; padding:6px; border-radius:4px; font-family:monospace; font-size:7pt;">
-- Postgres Function for Transaction Eligibility Verification
CREATE OR REPLACE FUNCTION apply_to_job(student_uuid UUID, job_uuid UUID)
RETURNS BOOLEAN AS $$
DECLARE
    eligible BOOLEAN;
BEGIN
    SELECT (s.cgpa >= j.minCgpa AND s.backlogs <= j.maxBacklogs) INTO eligible
    FROM "Student" s, "JobPosting" j
    WHERE s.id = student_uuid AND j.id = job_uuid;
    
    IF eligible THEN
        INSERT INTO "Application" (studentId, jobId, status)
        VALUES (student_uuid, job_uuid, 'applied');
        RETURN TRUE;
    ELSE
        RAISE EXCEPTION 'IneligibleCandidate';
    END IF;
END;
$$ LANGUAGE plpgsql;</pre>
                  <h3>Real-Time Event Notification Queue</h3>
                  <p>We push job registration events into a Redis pub/sub channel. Event streams broadcast to coordinators via persistent SSE connections to eliminate dashboard lag.</p>
                </div>
                """
            },
            "09": {
                "type": "comparison",
                "title": "Scalability Design",
                "content": """
                <table class="comparison-table">
                  <thead>
                    <tr><th>Scale</th><th>Bottleneck</th><th>Architectural Solution</th><th>Trade-offs</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>100 Users</strong></td>
                      <td>Connection leaks on Postgres queries.</td>
                      <td>Strict context managers in FastAPI dependencies.</td>
                      <td>None; best practice implementation.</td>
                    </tr>
                    <tr>
                      <td><strong>1,000 Users</strong></td>
                      <td>Lock contention during application surges.</td>
                      <td>Read replicas for job posting search paths.</td>
                      <td>Sub-second replication lag latency.</td>
                    </tr>
                    <tr>
                      <td><strong>10,000 Users</strong></td>
                      <td>Supabase connection pool exhaust.</td>
                      <td>Pooling via PgBouncer on database instance.</td>
                      <td>Slight latency hit on prepared statements.</td>
                    </tr>
                    <tr>
                      <td><strong>100k+ Users</strong></td>
                      <td>Coordinator socket server failures.</td>
                      <td>Redis sentinel setup with load balanced SSE clusters.</td>
                      <td>Increased infrastructure cost footprint.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            "10": {
                "type": "system",
                "title": "Failure Handling & Recovery",
                "content": """
                <div class="system-section">
                  <h3>Disaster Recovery & Failure Modes</h3>
                  <ul>
                    <li><strong>Database Failover:</strong> Postgres runs in a primary-replica hot-standby configuration. If the primary goes offline, AWS Route 53 redirects connections to the replica within 15 seconds.</li>
                    <li><strong>Redis Memory Overflow:</strong> Under extreme notification bursts, Redis could run out of memory. We set eviction policy to `volatile-lru` to drop older ephemeral events while keeping system session states intact.</li>
                    <li><strong>Network Partitions:</strong> The client implements automatic reconnection logic with exponential backoff for Server-Sent Events, ensuring dashboard sync recovers on network drops.</li>
                  </ul>
                </div>
                """
            },
            "11": {
                "type": "system",
                "title": "Monitoring & Observability",
                "content": """
                <div class="system-section">
                  <h3>System Telemetry Dashboard</h3>
                  <p>The system uses Prometheus to gather API metrics and Grafana to track resource usage:</p>
                  <ul>
                    <li><strong>Active Connections:</strong> Monitors database connection pool count to prevent pool exhaustion alerts.</li>
                    <li><strong>Error Rate Alerts:</strong> Fired when the API error rate (HTTP 5xx responses) exceeds 1% of total traffic.</li>
                    <li><strong>HTTP Latency:</strong> Standard dashboard tracking p95 and p99 response times for critical application endpoints.</li>
                  </ul>
                </div>
                """
            },
            "12": {
                "type": "system",
                "title": "Cost Optimization",
                "content": """
                <div class="system-section">
                  <h3>Resource Usage Optimization</h3>
                  <ul>
                    <li><strong>Static Data Caching:</strong> Company profiles and job posting details are cached in Redis for 10 minutes to minimize heavy Postgres relational reads.</li>
                    <li><strong>Payload Minimization:</strong> SSE endpoints push minimal JSON change logs rather than full data models, saving data egress costs.</li>
                    <li><strong>Serverless Scale Down:</strong> Dev and staging instances automatically spin down outside recruitment hours, reducing environment run costs.</li>
                  </ul>
                </div>
                """
            },
            "13": {
                "type": "system",
                "title": "Security Review",
                "content": """
                <div class="system-section">
                  <h3>Placement Portal Security Profile</h3>
                  <ul>
                    <li><strong>Threat: Privilege Escalation.</strong> A student attempts to approve their own application.</li>
                    <li><strong>Mitigation:</strong> Database RLS constraints block student role modifications on the `Application.status` field.</li>
                    <li><strong>Threat: Parameter Tampering.</strong> Manipulating job IDs to apply for postings with expired deadlines.</li>
                    <li><strong>Mitigation:</strong> API validates server-side timestamps against database deadline dates before executing database write transactions.</li>
                  </ul>
                </div>
                """
            },
            "14": {
                "type": "case-study",
                "title": "Engineering Challenges",
                "content": """
                <div class="case-study-grid">
                  <div class="cs-card">
                    <div class="cs-card-title">🔥 Production Incident</div>
                    <p>The Application Lockout: During a major recruitment drive, 3,000 students tried applying to a single job posting, causing PostgreSQL deadlock errors and application failures.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">🔎 Root Cause Analysis</div>
                    <p>Applications locked student rows sequentially. The system used `SELECT FOR UPDATE` on student profiles to verify eligibility, creating massive deadlock queues.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">🛠️ The Fix Patch</div>
                    <p>Removed the `FOR UPDATE` read lock. Replaced it with optimistic concurrency checks and an eligibility lookup against read-replica instances.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">📈 Key Lessons</div>
                    <p>Never lock primary user tables during high-volume transactional updates unless strictly necessary. Use read-only queries or decoupled validation queues to process checks.</p>
                  </div>
                </div>
                """
            },
            "15": {
                "type": "system",
                "title": "Future Roadmap",
                "content": """
                <div class="system-section">
                  <h3>Future Feature Scope</h3>
                  <ul>
                    <li><strong>Version 2: AI resume parsing and keyword matching.</strong> Automatically matching student resumes against job posting descriptions using embeddings.</li>
                    <li><strong>Version 3: Fully integrated WebRTC video rooms.</strong> Hosting interviews directly within the PlacePro dashboard, syncing schedules in real-time.</li>
                  </ul>
                </div>
                """
            },
            "16": {
                "type": "interview",
                "title": "Interview Deep Dive",
                "content": """
                <div class="interview-qa">
                  <div class="qa-block">
                    <div class="question-header">Q: What is Row-Level Security (RLS), and why enforce it at the database layer?</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> RLS enforces security policy constraints directly within the database engine. Even if application code has a bug or exposes an unsafe SQL injection path, PostgreSQL blocks the query if it violates the user's role policies.</p>
                    </div>
                  </div>
                  <div class="qa-block">
                    <div class="question-header">Q: How do you handle race conditions during high-volume applications?</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> We use database-level unique constraints on `(studentId, jobId)` and optimistic concurrency checks. This ensures duplicates are rejected at the storage layer, maintaining transactional consistency.</p>
                    </div>
                  </div>
                </div>
                """
            },
            "17": {
                "type": "interview",
                "title": "Top Project Questions",
                "content": """
                <div class="interview-qa">
                  <div class="qa-block">
                    <div class="question-header">Question: "What is the difference between WebSockets and Server-Sent Events (SSE)?"</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> WebSockets are full-duplex (two-way) connections, while SSE is mono-directional (server-to-client). For dashboards that mainly stream status updates to users, SSE is more lightweight and recovers automatically from network drops.</p>
                      <div class="buzzword-tags" style="margin-top: 4px;">
                        <span class="buzz-tag">Server-Sent Events</span>
                        <span class="buzz-tag">WebSocket Protocol</span>
                        <span class="buzz-tag">Connection Overheads</span>
                      </div>
                    </div>
                  </div>
                  <div class="qa-block">
                    <div class="question-header">Question: "How do you scale notification broadcasts during peak hours?"</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> We route events through Redis Pub/Sub. When a coordinator connects, their SSE server instance subscribes to the channel. Redis handles broadcasting events across SSE nodes, enabling horizontal scaling.</p>
                    </div>
                  </div>
                </div>
                """
            },
            "18": {
                "type": "revision",
                "title": "One Page Revision",
                "content": """
                <div class="revision-grid">
                  <div class="rev-card">
                    <div class="rev-card-title">Architecture</div>
                    <p>Next.js Dashboard -> Load Balancer -> FastAPI Web Nodes -> Redis Pub/Sub Event Bus -> Supabase PostgreSQL DB.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Database</div>
                    <p>PostgreSQL schema with strict composite indexes. Row-Level Security (RLS) policies isolations.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Scaling</div>
                    <p>PgBouncer for connection limits, Redis Pub/Sub for SSE horizontal scaling, Read-replicas for query offloads.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Security</div>
                    <p>JWT-based RBAC roles checks. RLS policies block unauthorized student/recruiter access scopes.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Tech Stack</div>
                    <p>Next.js, FastAPI, PostgreSQL, Supabase RLS, Redis Pub/Sub, Docker.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Key Challenge</div>
                    <p>Application deadlocks resolved by replacing database-level write locks with optimistic checks.</p>
                  </div>
                </div>
                """
            }
        }
    },
    # ── TIER 1: MNEMO ──
    {
        "name": "Mnemo",
        "subtitle": "AI-Powered Long-Term Memory Engine with Spaced Decay & pgvector Hybrid Search",
        "tagline": "Memory Layer",
        "sections": {
            "01": {
                "type": "case-study",
                "title": "Executive Summary",
                "content": """
                <div class="case-study-grid">
                  <div class="cs-card">
                    <div class="cs-card-title">🚨 The Core Problem</div>
                    <p>AI agents lack native persistent context, suffering from "amnesia" on session reboots or context truncation when massive historical logs are fed into prompt contexts.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">👥 Target Users & Value</div>
                    <p>LLM agents and chat interfaces requiring contextual persistence. It reduces token costs by retrieving only relevant memory blocks.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">🎯 Business Goal & Impact</div>
                    <p>Decrease LLM context window token costs by 70% while improving retrieval relevance by ranking memories based on decay scores.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">👑 My Role & Ownership</div>
                    <p><strong>Core Developer & System Designer</strong>. Designed the pgvector vector embedding schema, the Ebbinghaus decay scoring engine, and the hybrid keyword/vector search logic.</p>
                  </div>
                </div>
                """
            },
            "02": {
                "type": "system",
                "title": "Product Vision",
                "content": """
                <div class="system-section">
                  <h3>Why We Built It</h3>
                  <p>Standard vector databases perform flat semantic scans, ignoring temporal relevance. A user interaction from 5 minutes ago is treated with the same weight as a detail from 3 weeks ago. Mnemo uses spaced decay algorithms to match human memory decay patterns.</p>
                  <h3>Key Alternatives Analyzed</h3>
                  <table class="visual-table">
                    <thead>
                      <tr><th>Alternative</th><th>Drawback</th><th>Mnemo Advantage</th></tr>
                    </thead>
                    <tbody>
                      <tr><td>Pinecone</td><td>Requires external database sync; lacks temporal decay functions.</td><td>Integrated Postgres setup with dynamic scoring.</td></tr>
                      <tr><td>Short-Term System Prompts</td><td>Hits token limit barriers quickly; expensive memory.</td><td>Long-term retrieval based on semantic relevance.</td></tr>
                    </tbody>
                  </table>
                  <h3>Core Feature Matrix</h3>
                  <ul>
                    <li><strong>Decay Engine:</strong> Dynamic Ebbinghaus decay calculations.</li>
                    <li><strong>Hybrid Retrieval:</strong> Combines BM25 lexical search with vector cosine distance.</li>
                    <li><strong>Metadata Pruning:</strong> Automatically deletes low-value noise memory blocks.</li>
                  </ul>
                </div>
                """
            },
            "03": {
                "type": "comparison",
                "title": "Tech Stack Deep Dive",
                "content": """
                <table class="comparison-table">
                  <thead>
                    <tr><th>Layer</th><th>Tech Chosen</th><th>Key Reason / Why</th><th>Trade-offs & Constraints</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>API Engine</strong></td>
                      <td>FastAPI</td>
                      <td>Fast JSON serialization; handles parallel async embedding calls.</td>
                      <td>Requires explicit type declarations for custom objects.</td>
                    </tr>
                    <tr>
                      <td><strong>Database</strong></td>
                      <td>PostgreSQL + pgvector</td>
                      <td>Eliminates external database synchronization; keeps transactions ACID-compliant.</td>
                      <td>Higher CPU load during large-scale vector similarity calculations.</td>
                    </tr>
                    <tr>
                      <td><strong>Embeddings</strong></td>
                      <td>OpenAI text-embedding-ada-002</td>
                      <td>Industry standard 1536-dimension embeddings with balanced performance.</td>
                      <td>Dependency on external API latency and rate limits.</td>
                    </tr>
                    <tr>
                      <td><strong>Cache</strong></td>
                      <td>Redis</td>
                      <td>Stores active session memories to prevent redundant DB reads.</td>
                      <td>Cache invalidation complexity on memory mutations.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            "04": {
                "type": "architecture",
                "title": "High-Level Architecture",
                "content": """
                <div class="arch-diagram">
+--------------------+      HTTP POST    +--------------------+                 +--------------------+
|  LLM Agent Node    | ----------------> |  FastAPI Gateway   | --------------> | OpenAI Embeddings  |
|  (Chat Session)    |                   |  (Parser & Route)  |                 | (1536 Vector Gen)  |
+--------------------+                   +--------------------+                 +--------------------+
          ^                                        |                                       |
          | Context Payload                        v PostgreSQL DB Client                  | Return Vector
+--------------------+                   +--------------------+                            |
| Response Composer  | <---------------- | pgvector Extension | <--------------------------+
| (Ranked Memories)  |                   | (Cosine Similarity)|
+--------------------+                   +--------------------+
                </div>
                <div class="arch-description">
                  <p><strong>LLM Agent:</strong> Pushes user conversation logs into the Mnemo API Gateway during active chat sessions.</p>
                  <p><strong>FastAPI Gateway:</strong> Generates semantic vector embeddings for incoming messages using OpenAI's endpoint.</p>
                  <p><strong>pgvector DB:</strong> Matches the new vector against stored history, applying decay weights before returning records.</p>
                </div>
                """
            },
            "05": {
                "type": "flow",
                "title": "Request & Execution Flow",
                "content": """
                <div class="flow-diagram">
Agent Node                FastAPI Gateway             OpenAI API               PostgreSQL (pgvector)
    |                            |                        |                              |
    |-- 1. Query Context ------->|                        |                              |
    |                            |-- 2. Embed Prompt ---->|                              |
    |                            |<-- 3. Return Vector ---|                              |
    |                            |-- 4. Execute Hybrid Search (Cosine + Decay) --------->|
    |                            |<-- 5. Return Ranked Memory Set -----------------------|
    |<-- 6. Injected Context ----|                        |                              |
                </div>
                <div class="flow-steps">
                  <ol>
                    <li><strong>Query:</strong> Agent requests context matching the current user input message.</li>
                    <li><strong>Vector Generation:</strong> The API converts user text into a 1536-dimension float array vector.</li>
                    <li><strong>Similarity Search:</strong> The database calculates cosine distances between stored memory vectors and the input vector.</li>
                    <li><strong>Decay Calculation:</strong> The database engine calculates decay scores and returns context-ranked memories.</li>
                  </ol>
                </div>
                """
            },
            "06": {
                "type": "database",
                "title": "Database Design",
                "content": """
                <table class="db-table">
                  <thead>
                    <tr><th>Table</th><th>Fields</th><th>Types & Constraints</th><th>Indexes & Scaling</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>MemoryBlock</strong></td>
                      <td>id (PK), userId, content, embedding, lastAccessed</td>
                      <td>UUID, TEXT, vector(1536), TIMESTAMP</td>
                      <td>HNSW index on `embedding`.</td>
                    </tr>
                    <tr>
                      <td><strong>AccessLog</strong></td>
                      <td>id (PK), memoryId (FK), accessedAt, weight</td>
                      <td>UUID, TIMESTAMP, FLOAT</td>
                      <td>Index on `memoryId`.</td>
                    </tr>
                  </tbody>
                </table>
                <div class="db-notes">
                  <p><strong>Vector Indexing:</strong> We use an HNSW (Hierarchical Navigable Small World) index: `CREATE INDEX ON "MemoryBlock" USING hnsw (embedding vector_cosine_ops);` for fast sub-5ms lookups.</p>
                  <p><strong>Temporal Updates:</strong> Every access to a memory block updates the `lastAccessed` timestamp, resetting its Ebbinghaus decay curve.</p>
                </div>
                """
            },
            "07": {
                "type": "flow",
                "title": "Authentication Architecture",
                "content": """
                <div class="flow-diagram">
Agent Client              FastAPI Gateway             Prisma (Postgres)           pgvector Engine
  |                             |                            |                           |
  |-- 1. HTTP request + JWT --->|                            |                           |
  |                             |-- 2. Auth user session --->|                           |
  |                             |-- 3. Query User Memories ----------------------------->|
  |                             |                            |                           |-- 4. Match Vectors -->|
  |                             |                            |<-- 5. Filter User Rows ---|
  |<-- 6. Encrypted Context ----|                            |                           |
                </div>
                <div class="auth-details">
                  <p><strong>Agent Authentication:</strong> Agents authenticate using API tokens verified against PostgreSQL session stores.</p>
                  <p><strong>Multi-Tenant Isolation:</strong> A tenant-scoped RLS policy ensures that an agent query can never traverse or retrieve memory blocks belonging to other users.</p>
                </div>
                """
            },
            "08": {
                "type": "system",
                "title": "Core Engineering Systems",
                "content": """
                <div class="system-section">
                  <h3>Ebbinghaus Spaced Decay Engine</h3>
                  <p>Retrieving memories based purely on semantic similarity fails because older, outdated context can pollute the LLM prompt. Mnemo implements a custom decay algorithm: `S = S_0 * e^(-t/hl)`, where `t` is elapsed time and `hl` is the memory's half-life. This is implemented directly in our Postgres retrieval SQL query:</p>
                  <pre style="background:#F7FAFC; padding:6px; border-radius:4px; font-family:monospace; font-size:7pt;">
-- Spaced Decay SQL Query for Hybrid Ranking Retrieval
SELECT id, content,
       (1.0 - (embedding <=> :query_vector)) AS semantic_similarity,
       EXP(-EXTRACT(EPOCH FROM (NOW() - lastAccessed)) / 86400.0) AS decay_factor,
       ((1.0 - (embedding <=> :query_vector)) * 0.7 + 
        EXP(-EXTRACT(EPOCH FROM (NOW() - lastAccessed)) / 86400.0) * 0.3) AS final_rank
FROM "MemoryBlock"
WHERE userId = :user_id
ORDER BY final_rank DESC
LIMIT 5;</pre>
                  <h3>Hybrid Search Execution</h3>
                  <p>We combine semantic matches with lexical queries using BM25. This ensures exact name/keyword matches rank highly even if semantic distances are wide.</p>
                </div>
                """
            },
            "09": {
                "type": "comparison",
                "title": "Scalability Design",
                "content": """
                <table class="comparison-table">
                  <thead>
                    <tr><th>Scale</th><th>Bottleneck</th><th>Architectural Solution</th><th>Trade-offs</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>100 Users</strong></td>
                      <td>FastAPI process blocking on OpenAI calls.</td>
                      <td>Asynchronous API worker setup.</td>
                      <td>Requires tracking task completion.</td>
                    </tr>
                    <tr>
                      <td><strong>1,000 Users</strong></td>
                      <td>Postgres flat scans on large vector pools.</td>
                      <td>HNSW indexing on vector columns.</td>
                      <td>Requires higher RAM allocations.</td>
                    </tr>
                    <tr>
                      <td><strong>10,000 Users</strong></td>
                      <td>High vector distance calculation CPU usage.</td>
                      <td>Redis caching for active user session loops.</td>
                      <td>Memory capacity scaling requirements.</td>
                    </tr>
                    <tr>
                      <td><strong>100k+ Users</strong></td>
                      <td>OpenAI API rate limit ceilings.</td>
                      <td>Self-hosted HuggingFace embedding nodes.</td>
                      <td>Higher infrastructure maintenance.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            "10": {
                "type": "system",
                "title": "Failure Handling & Recovery",
                "content": """
                <div class="system-section">
                  <h3>Reliability Fail-safes</h3>
                  <ul>
                    <li><strong>Embedding API Failure:</strong> If the external embedding service drops, the gateway falls back to a local BM25 keyword query, keeping systems functional.</li>
                    <li><strong>Database Index Drift:</strong> HNSW indexes can drift as new data is inserted. We run a cron task that rebuilds the indexes: `REINDEX INDEX "MemoryBlock_embedding_idx";` during low-traffic periods.</li>
                    <li><strong>Out of Memory (OOM):</strong> High dimension vectors drain RAM. We limit memory block size limits to 1K tokens.</li>
                  </ul>
                </div>
                """
            },
            "11": {
                "type": "system",
                "title": "Monitoring & Observability",
                "content": """
                <div class="system-section">
                  <h3>Telemetry & Observability Setup</h3>
                  <ul>
                    <li><strong>Vector Query Latency:</strong> Tracked via Grafana dashboards, aiming for p95 response times under 15ms.</li>
                    <li><strong>Embedding Failures:</strong> Sentry alerts trigger on OpenAI API connection timeouts.</li>
                    <li><strong>Relevance Auditing:</strong> Logging system prompts and returned ranked lists to analyze drift patterns.</li>
                  </ul>
                </div>
                """
            },
            "12": {
                "type": "system",
                "title": "Cost Optimization",
                "content": """
                <div class="system-section">
                  <h3>Infrastructure Cost Optimization</h3>
                  <ul>
                    <li><strong>Context Packing:</strong> Merging related short memories into larger semantic chunks, reducing API token waste.</li>
                    <li><strong>Ephemeral Pruning:</strong> Automatically deleting memories that decay past a threshold (e.g., score < 0.1), preventing database bloat.</li>
                    <li><strong>Server Cache Offloads:</strong> Active user chats query Redis cache stores, offloading expensive vector scans.</li>
                  </ul>
                </div>
                """
            },
            "13": {
                "type": "system",
                "title": "Security Review",
                "content": """
                <div class="system-section">
                  <h3>Vector Database Security Model</h3>
                  <ul>
                    <li><strong>Threat: Data Leaks.</strong> Cosine calculations could inadvertently leak context across tenant spaces.</li>
                    <li><strong>Mitigation:</strong> Query bounds are strictly restricted by user session keys at the DB driver layer.</li>
                    <li><strong>Threat: Plaintext Memory Leaks.</strong> Unauthorized database access exposes sensitive conversation logs.</li>
                    <li><strong>Mitigation:</strong> Memory text columns are encrypted at rest using AES-256 before storage.</li>
                  </ul>
                </div>
                """
            },
            "14": {
                "type": "case-study",
                "title": "Engineering Challenges",
                "content": """
                <div class="case-study-grid">
                  <div class="cs-card">
                    <div class="cs-card-title">🔥 Production Incident</div>
                    <p>The Memory Hallucination Leak: The LLM agent received conflicting system details, leading to loop patterns and incorrect user responses.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">🔎 Root Cause Analysis</div>
                    <p>Flat semantic similarity searches returned outdated facts. When a user corrected a detail (e.g., "I moved to Paris"), the old fact ("I live in London") was still returned due to high semantic match score.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">🛠️ The Fix Patch</div>
                    <p>Designed and integrated the temporal spaced decay engine. By factoring in time elapsed, the updated Paris fact outranked the older London fact.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">📈 Key Lessons</div>
                    <p>Semantic search is not a complete memory solution. Factors like time elapsed, user approval ratings, and access frequency must be calculated to mirror human memory retrieval.</p>
                  </div>
                </div>
                """
            },
            "15": {
                "type": "system",
                "title": "Future Roadmap",
                "content": """
                <div class="system-section">
                  <h3>Future Development Timeline</h3>
                  <ul>
                    <li><strong>Version 2: Graph-RAG Integration.</strong> Linking isolated semantic memory blocks into a conceptual graph for multi-hop reasoning.</li>
                    <li><strong>Version 3: Cross-Session Consolidation.</strong> Automatically summarizing conversational drift patterns into consolidated user profiles during idle hours.</li>
                  </ul>
                </div>
                """
            },
            "16": {
                "type": "interview",
                "title": "Interview Deep Dive",
                "content": """
                <div class="interview-qa">
                  <div class="qa-block">
                    <div class="question-header">Q: How does HNSW vector indexing differ from flat cosine scanning?</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> Flat scanning calculates similarity against every single row, scaling linearly O(N). HNSW builds a hierarchical navigation graph of vectors, enabling logarithmic lookup speeds O(log N) at the cost of index build memory.</p>
                    </div>
                  </div>
                  <div class="qa-block">
                    <div class="question-header">Q: Why did you choose Postgres + pgvector over a dedicated database like Pinecone?</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> Using pgvector keeps memory records in our primary database. This guarantees ACID transactions, simplifies auth checks, and avoids the infrastructure overhead of syncing databases.</p>
                    </div>
                  </div>
                </div>
                """
            },
            "17": {
                "type": "interview",
                "title": "Top Project Questions",
                "content": """
                <div class="interview-qa">
                  <div class="qa-block">
                    <div class="question-header">Question: "What is the Ebbinghaus forgetting curve, and how is it modeled in database queries?"</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> The forgetting curve models memory retention decline over time. We calculate an exponential decay factor using SQL timestamps, weighting newer interactions higher in final search rankings.</p>
                      <div class="buzzword-tags" style="margin-top: 4px;">
                        <span class="buzz-tag">Forgot Curve</span>
                        <span class="buzz-tag">Spaced Recall</span>
                        <span class="buzz-tag">Cosine Similarity</span>
                      </div>
                    </div>
                  </div>
                  <div class="qa-block">
                    <div class="question-header">Question: "Explain the tradeoff between vector dimensionality and query performance."</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> Higher dimensions (e.g., 1536) offer richer semantic modeling but consume more RAM and compute power. Lower dimensions are faster but can lose semantic nuances.</p>
                    </div>
                  </div>
                </div>
                """
            },
            "18": {
                "type": "revision",
                "title": "One Page Revision",
                "content": """
                <div class="revision-grid">
                  <div class="rev-card">
                    <div class="rev-card-title">Architecture</div>
                    <p>Agent Node -> FastAPI Gateway -> OpenAI Embeddings -> pgvector similarity engine -> Context injection payload.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Database</div>
                    <p>PostgreSQL schema with HNSW index. Spaced decay functions calculated directly inside SQL queries.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Scaling</div>
                    <p>HNSW index limits latency, Redis caches hot sessions, automatic pruning deletes decayed memory blocks.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Security</div>
                    <p>Encrypted memory text columns, API token authentication, tenant-scoped database isolation policies.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Tech Stack</div>
                    <p>FastAPI, PostgreSQL, pgvector, Redis, OpenAI text-embedding-ada-002 model.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Key Challenge</div>
                    <p>Semantic drift resolved by integrating temporal spaced decay math directly into query filters.</p>
                  </div>
                </div>
                """
            }
        }
    },
    # ── TIER 2: ROVN ──
    {
        "name": "ROVN",
        "subtitle": "AI-Powered Lead Ingestion workspace with Intent Scoring & Prioritization",
        "tagline": "AI Lead Co-Pilot",
        "sections": {
            "01": {
                "type": "case-study",
                "title": "Executive Summary",
                "content": """
                <div class="case-study-grid">
                  <div class="cs-card">
                    <div class="cs-card-title">🚨 The Core Problem</div>
                    <p>Startups receive thousands of raw leads from multiple channels (email, web forms, social media). Sales teams waste hours manual sorting spam from high-intent buyers.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">👥 Target Users & Value</div>
                    <p>Sales development representatives (SDRs). It automatically highlights hot buyers, saving hours of manual data entry.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">🎯 Business Goal & Impact</div>
                    <p>Increase sales team lead-to-opportunity conversion rates by 40% using real-time intent analysis and auto-tagging pipelines.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">👑 My Role & Ownership</div>
                    <p><strong>Lead Engineer</strong>. Built the asynchronous webhook ingestion pipeline, the LLM intent scoring logic, and database schemas.</p>
                  </div>
                </div>
                """
            },
            "02": {
                "type": "system",
                "title": "Product Vision",
                "content": """
                <div class="system-section">
                  <h3>Why We Built It</h3>
                  <p>Lead management systems categorize leads based on static inputs (e.g., job titles). ROVN analyzes lead communication intent dynamically using LLMs, scoring purchase urgency instantly.</p>
                  <h3>Key Alternatives Analyzed</h3>
                  <table class="visual-table">
                    <thead>
                      <tr><th>Alternative</th><th>Drawback</th><th>ROVN Advantage</th></tr>
                    </thead>
                    <tbody>
                      <tr><td>Zapier + Hubspot</td><td>Static routing only; does not analyze text intent.</td><td>Dynamic AI-driven scoring on raw input.</td></tr>
                      <tr><td>Manual Review</td><td>SDR response delays; leads go cold.</td><td>Sub-second ingestion and priority ranking.</td></tr>
                    </tbody>
                  </table>
                  <h3>Core Feature Matrix</h3>
                  <ul>
                    <li><strong>Intent Scoring:</strong> Real-time buyer interest analysis.</li>
                    <li><strong>Context Extraction:</strong> Automatically pulls company size, budget, and pain points.</li>
                    <li><strong>Webhook Ingest:</strong> Integrates with existing web forms.</li>
                  </ul>
                </div>
                """
            },
            "03": {
                "type": "comparison",
                "title": "Tech Stack Deep Dive",
                "content": """
                <table class="comparison-table">
                  <thead>
                    <tr><th>Layer</th><th>Tech Chosen</th><th>Key Reason / Why</th><th>Trade-offs & Constraints</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>Frontend</strong></td>
                      <td>React / Next.js</td>
                      <td>Fast client-side rendering for real-time sales dashboards.</td>
                      <td>Requires state sync management across open sessions.</td>
                    </tr>
                    <tr>
                      <td><strong>Backend</strong></td>
                      <td>Node.js / Express</td>
                      <td>Fast asynchronous API gateway for webhook payload ingestion.</td>
                      <td>Relies on external queue workers for heavy analysis.</td>
                    </tr>
                    <tr>
                      <td><strong>Queue</strong></td>
                      <td>BullMQ / Redis</td>
                      <td>Handles high concurrent traffic spikes without dropping webhook payloads.</td>
                      <td>Adds system infrastructure complexity.</td>
                    </tr>
                    <tr>
                      <td><strong>Database</strong></td>
                      <td>PostgreSQL</td>
                      <td>Structured data relational safety for client records.</td>
                      <td>Requires migrations for schema updates.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            "04": {
                "type": "architecture",
                "title": "High-Level Architecture",
                "content": """
                <div class="arch-diagram">
+--------------------+      HTTP POST    +--------------------+      Queue      +--------------------+
|  Webhooks / Forms  | ----------------> |  API Gateway Node  | --------------> | BullMQ (Redis)     |
|  (Raw Ingestion)   |                   |  (Ingest & Ack)    |                 +--------------------+
+--------------------+                   +--------------------+                            |
                                                   |                                       | Task Trigger
                                                   v PostgreSQL DB                         v
                                         +--------------------+                 +--------------------+
                                         | PostgreSQL DB      | <-------------- | Worker Services    |
                                         | (Lead Records)     |                 | (LLM Intent Engine)|
                                         +--------------------+                 +--------------------+
                </div>
                <div class="arch-description">
                  <p><strong>Webhook Gateway:</strong> Ingests external HTTP payloads, validates signatures, and returns HTTP 200 immediately.</p>
                  <p><strong>BullMQ Queue:</strong> Buffers payloads in Redis to protect internal services from resource spikes.</p>
                  <p><strong>Worker Node:</strong> Runs intent scoring prompts on Llama-3, extracts metadata, and updates PostgreSQL.</p>
                </div>
                """
            },
            "05": {
                "type": "flow",
                "title": "Request & Execution Flow",
                "content": """
                <div class="flow-diagram">
Webhook Source            Webhook Gateway             BullMQ (Redis)               Worker Node             Postgres DB
      |                          |                          |                           |                       |
      |-- 1. POST raw payload -->|                          |                           |                       |
      |<-- 2. HTTP 202 Accepted -|                          |                           |                       |
      |                          |-- 3. Push Job ---------->|                           |                       |
      |                          |                          |-- 4. Trigger Worker ----->|                       |
      |                          |                          |                           |-- 5. Score Intent --->|
      |                          |                          |                           |-- 6. Write Result --->|
      |                          |                          |                           |<-- 7. Confirmed ------|
                </div>
                <div class="flow-steps">
                  <ol>
                    <li><strong>Ingestion:</strong> External form submits data to `/api/v1/webhook`.</li>
                    <li><strong>Queuing:</strong> The gateway validates signatures and pushes the payload to BullMQ.</li>
                    <li><strong>Analysis:</strong> Workers extract intent, budget indicators, and contact details via LLM queries.</li>
                    <li><strong>Storage:</strong> The analyzed lead is stored in PostgreSQL and ranked on the SDR dashboard.</li>
                  </ol>
                </div>
                """
            },
            "06": {
                "type": "database",
                "title": "Database Design",
                "content": """
                <table class="db-table">
                  <thead>
                    <tr><th>Table</th><th>Fields</th><th>Types & Constraints</th><th>Indexes & Scaling</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>Lead</strong></td>
                      <td>id (PK), email, company, rawText, score</td>
                      <td>UUID, VARCHAR, TEXT, INT</td>
                      <td>Index on `score` DESC.</td>
                    </tr>
                    <tr>
                      <td><strong>Metadata</strong></td>
                      <td>id (PK), leadId (FK), budget, size, timeline</td>
                      <td>UUID, DECIMAL, INT, VARCHAR</td>
                      <td>Index on `leadId`.</td>
                    </tr>
                  </tbody>
                </table>
                <div class="db-notes">
                  <p><strong>Indexing Strategy:</strong> An index on `score` accelerates dashboard loads, sorting incoming leads by buying urgency.</p>
                  <p><strong>Integrity:</strong> Deleting a lead cascades deletion to its metadata records, keeping tables clean.</p>
                </div>
                """
            },
            "07": {
                "type": "flow",
                "title": "Authentication Architecture",
                "content": """
                <div class="flow-diagram">
External Webhook          Node.js Ingest              Crypto Module               BullMQ Queue
       |                          |                         |                          |
       |-- 1. POST + Signature -> |                         |                          |
       |                          |-- 2. Verify SHA256 ---->|                          |
       |                          |<-- 3. Valid Signature --|                          |
       |                          |-- 4. Push Ingestion Task ------------------------->|
       |<-- 5. HTTP 200 OK -------|                         |                          |
                </div>
                <div class="auth-details">
                  <p><strong>Webhook Verification:</strong> Incoming webhooks include an `X-Hub-Signature-256` header, verified using HMAC SHA256 with a shared secret to block spam.</p>
                  <p><strong>Client API Authentication:</strong> SDR dashboards verify user sessions using JWT checks at the API gateway.</p>
                </div>
                """
            },
            "08": {
                "type": "system",
                "title": "Core Engineering Systems",
                "content": """
                <div class="system-section">
                  <h3>Dynamic Intent Scoring Engine</h3>
                  <p>When raw text hits the webhook, workers run a classification prompt. We parse the LLM's response using structured JSON schemas to extract key metrics:</p>
                  <pre style="background:#F7FAFC; padding:6px; border-radius:4px; font-family:monospace; font-size:7pt;">
# System Prompt snippet for Intent Scoring
SYS_PROMPT = \"\"\"
You are a Lead Scoring AI. Analyze user requests and return JSON:
{
  "intent_score": Integer (1-100),
  "extracted_budget": Decimal or null,
  "timeline_urgency": "immediate" | "mid" | "low"
}
Output ONLY valid JSON.\"\"\"</pre>
                  <h3>Prioritization Queue</h3>
                  <p>High-scoring leads (e.g., > 80) skip the queue, triggering SMS alerts via Twilio to ensure SDRs respond within 5 minutes.</p>
                </div>
                """
            },
            "09": {
                "type": "comparison",
                "title": "Scalability Design",
                "content": """
                <table class="comparison-table">
                  <thead>
                    <tr><th>Scale</th><th>Bottleneck</th><th>Architectural Solution</th><th>Trade-offs</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>100 Users</strong></td>
                      <td>Slow response times during LLM processing.</td>
                      <td>Decoupled API gateway using async workers.</td>
                      <td>Slight delay before lead is analyzed.</td>
                    </tr>
                    <tr>
                      <td><strong>1,000 Users</strong></td>
                      <td>High concurrent database write locks.</td>
                      <td>Connection pooling via PgBouncer.</td>
                      <td>Slight latency overhead.</td>
                    </tr>
                    <tr>
                      <td><strong>10,000 Users</strong></td>
                      <td>LLM rate limit limits.</td>
                      <td>Model fallback channels (Anthropic -> Groq).</td>
                      <td>Varying scoring consistency.</td>
                    </tr>
                    <tr>
                      <td><strong>100k+ Users</strong></td>
                      <td>Redis memory exhaustion on queues.</td>
                      <td>BullMQ auto-cleanup of completed jobs.</td>
                      <td>Lost historical queue logs.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            "10": {
                "type": "system",
                "title": "Failure Handling & Recovery",
                "content": """
                <div class="system-section">
                  <h3>Queue Fail-safes & Fallbacks</h3>
                  <ul>
                    <li><strong>Queue Overflow:</strong> If the worker cluster blocks, BullMQ queues jobs in Redis. Backpressure controls throttle webhooks on memory limits.</li>
                    <li><strong>LLM Failures:</strong> If the classification API fails, the lead score defaults to 50 (neutral), labeling the record for manual triage.</li>
                    <li><strong>Webhook Retries:</strong> External platforms expect HTTP responses within 3 seconds. The gateway acknowledges receipt immediately, processing classification asynchronously.</li>
                  </ul>
                </div>
                """
            },
            "11": {
                "type": "system",
                "title": "Monitoring & Observability",
                "content": """
                <div class="system-section">
                  <h3>Observability System</h3>
                  <ul>
                    <li><strong>Job Processing Times:</strong> BullMQ dashboard monitors active job processing times, alerting if execution times exceed 5 seconds.</li>
                    <li><strong>Accuracy Checks:</strong> SDRs can flag incorrect intent scores, helping trace classifier drift patterns.</li>
                    <li><strong>Ingestion Failures:</strong> Tracks rejected HTTP payloads due to signature validation issues.</li>
                  </ul>
                </div>
                """
            },
            "12": {
                "type": "system",
                "title": "Cost Optimization",
                "content": """
                <div class="system-section">
                  <h3>Operational Savings</h3>
                  <ul>
                    <li><strong>Input Pruning:</strong> Stripping HTML tags and signatures from raw emails before sending prompts to the LLM.</li>
                    <li><strong>Model Routing:</strong> Classification uses cheap models (Llama-3 8B), reserving Claude only for complex RFP documents.</li>
                    <li><strong>Batching:</strong> Bundling low-priority leads for batch classification during off-peak hours.</li>
                  </ul>
                </div>
                """
            },
            "13": {
                "type": "system",
                "title": "Security Review",
                "content": """
                <div class="system-section">
                  <h3>Workspace Security Profile</h3>
                  <ul>
                    <li><strong>Threat: Webhook Spoofing.</strong> Bad actors sending fake leads to drain API credits.</li>
                    <li><strong>Mitigation:</strong> HMAC SHA256 signature verification blocks unauthenticated HTTP requests.</li>
                    <li><strong>Threat: Injection Attacks.</strong> Users placing malicious instructions inside form fields.</li>
                    <li><strong>Mitigation:</strong> Input fields are strictly sanitized, and system prompts explicitly instruct LLMs to ignore inline user instructions.</li>
                  </ul>
                </div>
                """
            },
            "14": {
                "type": "case-study",
                "title": "Engineering Challenges",
                "content": """
                <div class="case-study-grid">
                  <div class="cs-card">
                    <div class="cs-card-title">🔥 Production Incident</div>
                    <p>The Webhook Lockout: A client launched a campaign that sent 5,000 leads in 2 minutes, causing API gateway timeouts and lost webhook records.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">🔎 Root Cause Analysis</div>
                    <p>The API gateway processed LLM calls inline before returning HTTP responses. The client platform timed out after 3 seconds, retrying and compounding load.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">🛠️ The Fix Patch</div>
                    <p>Decoupled the gateway. Ingestion now returns a quick HTTP 202 after writing to the Redis queue, deferring LLM calls to background workers.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">📈 Key Lessons</div>
                    <p>Never run slow, blocking API operations (like LLM inference) inline inside client-facing HTTP response paths. Accept payloads quickly and process asynchronously.</p>
                  </div>
                </div>
                """
            },
            "15": {
                "type": "system",
                "title": "Future Roadmap",
                "content": """
                <div class="system-section">
                  <h3>Development Roadmap</h3>
                  <ul>
                    <li><strong>Version 2: Automatic Email Reply.</strong> Auto-drafting response emails based on lead questions and pain points.</li>
                    <li><strong>Version 3: Cross-Channel Ingestion.</strong> Integrating Slack, LinkedIn, and intercom streams into a single sales dashboard.</li>
                  </ul>
                </div>
                """
            },
            "16": {
                "type": "interview",
                "title": "Interview Deep Dive",
                "content": """
                <div class="interview-qa">
                  <div class="qa-block">
                    <div class="question-header">Q: How do you protect your LLM prompt from prompt injection?</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> We separate system instructions from user inputs, wrap user text in isolated XML blocks, and instruct the model to analyze the text without executing commands.</p>
                    </div>
                  </div>
                  <div class="qa-block">
                    <div class="question-header">Q: Why use Redis-backed queues instead of simple in-memory arrays?</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> In-memory queues lose all jobs on server reboots. Redis-backed systems (BullMQ) persist queue state to disk, surviving server restarts.</p>
                    </div>
                  </div>
                </div>
                """
            },
            "17": {
                "type": "interview",
                "title": "Top Project Questions",
                "content": """
                <div class="interview-qa">
                  <div class="qa-block">
                    <div class="question-header">Question: "What is HMAC, and how does it verify webhook payloads?"</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> HMAC hashes payloads using a shared secret key. We calculate the hash on receipt and compare it with the header signature to verify the source.</p>
                      <div class="buzzword-tags" style="margin-top: 4px;">
                        <span class="buzz-tag">HMAC Verification</span>
                        <span class="buzz-tag">Cryptographic Hash</span>
                        <span class="buzz-tag">Signature Header</span>
                      </div>
                    </div>
                  </div>
                  <div class="qa-block">
                    <div class="question-header">Question: "How do you handle worker crashes mid-task?"</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> BullMQ monitors worker locks. If a worker goes offline, the lock expires, and the job is automatically returned to the queue for retry.</p>
                    </div>
                  </div>
                </div>
                """
            },
            "18": {
                "type": "revision",
                "title": "One Page Revision",
                "content": """
                <div class="revision-grid">
                  <div class="rev-card">
                    <div class="rev-card-title">Architecture</div>
                    <p>Form POST -> Express Gateway -> BullMQ (Redis) -> Worker -> Llama-3 intent analyzer -> Postgres DB.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Database</div>
                    <p>Relational SQL tables storing Lead records and metadata. Index on scoring column for sorting.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Scaling</div>
                    <p>BullMQ buffers spikes, pgvector indexes speed queries, multi-provider model routing manages rate limits.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Security</div>
                    <p>HMAC SHA256 signature verification blocks spam webhooks, system prompts restrict command execution.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Tech Stack</div>
                    <p>Next.js, Node.js, Express, BullMQ, Redis, PostgreSQL, Llama-3 model.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Key Challenge</div>
                    <p>Inline processing timeouts solved by migrating to asynchronous queue-based worker nodes.</p>
                  </div>
                </div>
                """
            }
        }
    },
    # ── TIER 2: TRAVIO ──
    {
        "name": "Travio",
        "subtitle": "Real-time Collaborative Trip Planner with Conflict Resolution & RBAC",
        "tagline": "Trip Planner",
        "sections": {
            "01": {
                "type": "case-study",
                "title": "Executive Summary",
                "content": """
                <div class="case-study-grid">
                  <div class="cs-card">
                    <div class="cs-card-title">🚨 The Core Problem</div>
                    <p>Collaborative trip planning involves multiple users modifying the same itinerary. Without concurrency control, changes overwrite each other, causing data inconsistency.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">👥 Target Users & Value</div>
                    <p>Travelers planning group trips. Allows users to edit itineraries, select hotels, and assign budgets collaboratively in real-time.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">🎯 Business Goal & Impact</div>
                    <p>Deliver an interactive collaborative editor with sync lag under 100ms, ensuring zero data loss and clean conflict resolution.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">👑 My Role & Ownership</div>
                    <p><strong>Full-stack Engineer</strong>. Implemented the WebSocket event synchronization layer and designed the collaborative editor state engine.</p>
                  </div>
                </div>
                """
            },
            "02": {
                "type": "system",
                "title": "Product Vision",
                "content": """
                <div class="system-section">
                  <h3>Why We Built It</h3>
                  <p>Group travel planning is fragmented across multiple spreadsheets and chat rooms. Travio centralizes group planning, giving teams a single source of truth for itineraries.</p>
                  <h3>Key Alternatives Analyzed</h3>
                  <table class="visual-table">
                    <thead>
                      <tr><th>Alternative</th><th>Drawback</th><th>Travio Advantage</th></tr>
                    </thead>
                    <tbody>
                      <tr><td>Google Sheets</td><td>Difficult to format images; lacks map integrations.</td><td>Rich visual editor with integrated routing.</td></tr>
                      <tr><td>Traditional Planners</td><td>Single-user only; requires manual export sharing.</td><td>Real-time synchronization for collaborative planning.</td></tr>
                    </tbody>
                  </table>
                  <h3>Core Feature Matrix</h3>
                  <ul>
                    <li><strong>Collaborative Canvas:</strong> Multi-user editing canvas.</li>
                    <li><strong>Conflict Resolver:</strong> Handles concurrent updates.</li>
                    <li><strong>Interactive Map:</strong> Real-time distance and route calculations.</li>
                  </ul>
                </div>
                """
            },
            "03": {
                "type": "comparison",
                "title": "Tech Stack Deep Dive",
                "content": """
                <table class="comparison-table">
                  <thead>
                    <tr><th>Layer</th><th>Tech Chosen</th><th>Key Reason / Why</th><th>Trade-offs & Constraints</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>Frontend</strong></td>
                      <td>React / Vite</td>
                      <td>Fast development cycles; light client footprint for canvas.</td>
                      <td>State sync overhead across large user groups.</td>
                    </tr>
                    <tr>
                      <td><strong>Backend</strong></td>
                      <td>Node.js / Socket.io</td>
                      <td>Event-driven WebSocket routing is ideal for real-time collaboration.</td>
                      <td>Harder to scale horizontally compared to stateless HTTP servers.</td>
                    </tr>
                    <tr>
                      <td><strong>Database</strong></td>
                      <td>MongoDB</td>
                      <td>Document model maps directly to dynamic itineraries.</td>
                      <td>Lacks strict SQL schema enforcement.</td>
                    </tr>
                    <tr>
                      <td><strong>Sync Bus</strong></td>
                      <td>Redis</td>
                      <td>Synchronizes WebSocket messages across distributed server nodes.</td>
                      <td>Adds extra network hop latency.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            "04": {
                "type": "architecture",
                "title": "High-Level Architecture",
                "content": """
                <div class="arch-diagram">
+--------------------+      WebSockets   +--------------------+      Redis      +--------------------+
|  React Client A    | ----------------> |  Socket.io Server  | --------------> | Redis Adapter      |
|  (Canvas Editor)   |                   |  (Node.js Cluster) |                 | (State Sync Bus)   |
+--------------------+                   +--------------------+                 +--------------------+
          ^                                        |                                       |
          | WebSocket Event                        v MongoDB Connection                    | Broadcast Event
+--------------------+                   +--------------------+                            |
|  React Client B    | <---------------- | MongoDB Instance   | <--------------------------+
|  (Canvas Editor)   |                   | (Document Stores)  |
+--------------------+                   +--------------------+
                </div>
                <div class="arch-description">
                  <p><strong>React Client:</strong> Renders the collaborative workspace and tracks local edit operations.</p>
                  <p><strong>Socket.io Server:</strong> Distributes user edits and coordinates active room states.</p>
                  <p><strong>Redis Adapter:</strong> Coordinates WebSocket messages across multiple backend instances.</p>
                </div>
                """
            },
            "05": {
                "type": "flow",
                "title": "Request & Execution Flow",
                "content": """
                <div class="flow-diagram">
Client A                  WebSocket Server             Redis Adapter            Client B               MongoDB
   |                             |                           |                      |                     |
   |-- 1. Edit Itinerary Event ->|                           |                      |                     |
   |                             |-- 2. Broadcast Event ---->|                      |                     |
   |                             |                           |-- 3. Emit ---------->|                     |
   |                             |                           |                      |-- 4. Apply Edit --->|
   |                             |-- 5. Write to DB ----------------------------------------------------->|
   |                             |<-- 6. Confirmed Write -------------------------------------------------|
   |<-- 7. Confirmed Broadcast --|                           |                      |                     |
                </div>
                <div class="flow-steps">
                  <ol>
                    <li><strong>Edit Event:</strong> Client A edits a node on the itinerary.</li>
                    <li><strong>Relay:</strong> The WebSocket server processes the edit and broadcasts it to the Redis channel.</li>
                    <li><strong>Synchronization:</strong> Client B receives the event and updates their local view.</li>
                    <li><strong>Storage:</strong> The server writes the updated document structure to MongoDB.</li>
                  </ol>
                </div>
                """
            },
            "06": {
                "type": "database",
                "title": "Database Design",
                "content": """
                <table class="db-table">
                  <thead>
                    <tr><th>Collection</th><th>Fields</th><th>Schema Model</th><th>Indexes & Scaling</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>Itinerary</strong></td>
                      <td>_id, title, ownerId, members (Array)</td>
                      <td>Document BSON</td>
                      <td>Index on `ownerId`.</td>
                    </tr>
                    <tr>
                      <td><strong>TripNode</strong></td>
                      <td>_id, itineraryId, day, title, budget, loc</td>
                      <td>Nested Document</td>
                      <td>Composite index on `(itineraryId, day)`.</td>
                    </tr>
                  </tbody>
                </table>
                <div class="db-notes">
                  <p><strong>Design Decision:</strong> Storing daily itinerary nodes as sub-documents in the `Itinerary` collection avoids complex joins and speeds up document reads.</p>
                  <p><strong>Indexing Strategy:</strong> An index on `itineraryId` ensures fast document retrieval when loading the workspace.</p>
                </div>
                """
            },
            "07": {
                "type": "flow",
                "title": "Authentication Architecture",
                "content": """
                <div class="flow-diagram">
Client                    Socket.io Server            Auth Middleware             MongoDB User Store
  |                            |                             |                            |
  |-- 1. WS Connect + JWT ---->|                             |                            |
  |                            |-- 2. Verify Session token ->|                            |
  |                            |                             |-- 3. Lookup user role ---->|
  |                            |                             |<-- 4. Grant access details-|
  |<-- 5. Connection Approved -|                             |                            |
                </div>
                <div class="auth-details">
                  <p><strong>Handshake Security:</strong> Auth tokens are verified during the initial WebSocket handshake. Unauthenticated connection attempts are immediately rejected.</p>
                  <p><strong>Role Enforcement:</strong> Users are assigned `editor` or `viewer` roles, blocking unauthorized edits at the server layer.</p>
                </div>
                """
            },
            "08": {
                "type": "system",
                "title": "Core Engineering Systems",
                "content": """
                <div class="system-section">
                  <h3>Conflict Resolution State Engine</h3>
                  <p>To support real-time collaborative editing, the system must handle conflicting edits. Travio uses Operational Transformation (OT) to coordinate document updates:</p>
                  <pre style="background:#F7FAFC; padding:6px; border-radius:4px; font-family:monospace; font-size:7pt;">
# Operational Transformation (OT) conflict resolution logic
def transform_edits(op_a, op_b):
    # Resolves overlapping updates
    if op_a['type'] == 'insert' and op_b['type'] == 'insert':
        if op_a['position'] < op_b['position']:
            op_b['position'] += len(op_a['text'])
        else:
            op_a['position'] += len(op_b['text'])
    return op_a, op_b</pre>
                  <h3>Real-time Sync Bus</h3>
                  <p>Redis Adapter broadcasts local edits across all websocket instances, maintaining consistent canvas views.</p>
                </div>
                """
            },
            "09": {
                "type": "comparison",
                "title": "Scalability Design",
                "content": """
                <table class="comparison-table">
                  <thead>
                    <tr><th>Scale</th><th>Bottleneck</th><th>Architectural Solution</th><th>Trade-offs</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>100 Users</strong></td>
                      <td>WebSocket connection limits.</td>
                      <td>Increase file descriptor limits on the host server.</td>
                      <td>None; standard configuration.</td>
                    </tr>
                    <tr>
                      <td><strong>1,000 Users</strong></td>
                      <td>Socket.io memory leaks.</td>
                      <td>Decoupled stateless socket servers using Redis.</td>
                      <td>Requires Redis infrastructure.</td>
                    </tr>
                    <tr>
                      <td><strong>10,000 Users</strong></td>
                      <td>MongoDB write load ceiling.</td>
                      <td>Write caching in Redis, batching saves.</td>
                      <td>Slight data loss window on server crashes.</td>
                    </tr>
                    <tr>
                      <td><strong>100k+ Users</strong></td>
                      <td>Global network latency spikes.</td>
                      <td>Geographic server clustering with region pinning.</td>
                      <td>High infrastructure footprint.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            "10": {
                "type": "system",
                "title": "Failure Handling & Recovery",
                "content": """
                <div class="system-section">
                  <h3>Reliability & Fault Tolerance</h3>
                  <ul>
                    <li><strong>WebSocket Drops:</strong> Socket.io automatically attempts to reconnect on drops, buffered edits are resent on successful reconnection.</li>
                    <li><strong>Redis Sync Loss:</strong> If the Redis adapter drops, users connected to the same server remain in sync. The server queues updates until Redis connection recovers.</li>
                    <li><strong>MongoDB Lockups:</strong> Under high database write loads, changes are written to a Redis cache and flushed to MongoDB in batches every 5 seconds.</li>
                  </ul>
                </div>
                """
            },
            "11": {
                "type": "system",
                "title": "Monitoring & Observability",
                "content": """
                <div class="system-section">
                  <h3>System Telemetry Configuration</h3>
                  <ul>
                    <li><strong>Active Connections Count:</strong> Tracks active WebSocket sessions to monitor server capacity.</li>
                    <li><strong>Broadcast Latency:</strong> Measures the transit time of updates across users, alerting if it exceeds 150ms.</li>
                    <li><strong>DB Write Queue:</strong> Monitors MongoDB queue backlogs to ensure batch operations process on time.</li>
                  </ul>
                </div>
                """
            },
            "12": {
                "type": "system",
                "title": "Cost Optimization",
                "content": """
                <div class="system-section">
                  <h3>Infrastructure Cost Controls</h3>
                  <ul>
                    <li><strong>Event Throttle:</strong> Client-side cursor movement updates are throttled to 50ms intervals, reducing network traffic.</li>
                    <li><strong>Payload Compression:</strong> Compressing WebSocket payloads reduces network egress costs.</li>
                    <li><strong>Autoscaling Nodes:</strong> Socket.io containers automatically scale up during peak holiday seasons, scaling down during low-traffic periods.</li>
                  </ul>
                </div>
                """
            },
            "13": {
                "type": "system",
                "title": "Security Review",
                "content": """
                <div class="system-section">
                  <h3>Workspace Security Profile</h3>
                  <ul>
                    <li><strong>Threat: Unauthorized Edits.</strong> Users edit itineraries without write permissions.</li>
                    <li><strong>Mitigation:</strong> WebSocket handlers validate user session permissions before executing edit events.</li>
                    <li><strong>Threat: Cross-Site Scripting (XSS).</strong> Users inject scripts inside collaborative itinerary nodes.</li>
                    <li><strong>Mitigation:</strong> HTML content is sanitized on the client and validated on the backend.</li>
                  </ul>
                </div>
                """
            },
            "14": {
                "type": "case-study",
                "title": "Engineering Challenges",
                "content": """
                <div class="case-study-grid">
                  <div class="cs-card">
                    <div class="cs-card-title">🔥 Production Incident</div>
                    <p>The Collaborative Drift: Users editing the same itinerary node experienced desynced views, leading to incorrect layouts.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">🔎 Root Cause Analysis</div>
                    <p>The server applied updates in order of receipt without conflict resolution logic. Edits from users with higher latency overwritten newer updates.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">🛠️ The Fix Patch</div>
                    <p>Implemented Operational Transformation (OT) conflict resolution logic on the server to merge concurrent changes before broadcasting.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">📈 Key Lessons</div>
                    <p>Real-time collaboration requires robust conflict resolution logic. Simple order-of-arrival strategies inevitably lead to document state drift.</p>
                  </div>
                </div>
                """
            },
            "15": {
                "type": "system",
                "title": "Future Roadmap",
                "content": """
                <div class="system-section">
                  <h3>Development Timeline</h3>
                  <ul>
                    <li><strong>Version 2: Offline Editing.</strong> Support offline editing with CRDT-based synchronization on reconnection.</li>
                    <li><strong>Version 3: AI Travel Assistant.</strong> Dynamic itinerary suggestions based on group preferences.</li>
                  </ul>
                </div>
                """
            },
            "16": {
                "type": "interview",
                "title": "Interview Deep Dive",
                "content": """
                <div class="interview-qa">
                  <div class="qa-block">
                    <div class="question-header">Q: What is Operational Transformation (OT) and how does it prevent desync?</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> OT transforms operations based on concurrent edits. This ensures that concurrent edits are applied in a consistent order across all clients, maintaining identical document states.</p>
                    </div>
                  </div>
                  <div class="qa-block">
                    <div class="question-header">Q: How do you scale WebSocket connections horizontally?</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> We route events through a Redis Pub/Sub backplane. When a server node receives an update, it publishes to Redis, broadcasting changes across all websocket nodes.</p>
                    </div>
                  </div>
                </div>
                """
            },
            "17": {
                "type": "interview",
                "title": "Top Project Questions",
                "content": """
                <div class="interview-qa">
                  <div class="qa-block">
                    <div class="question-header">Question: "What is the difference between OT and CRDT?"</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> OT relies on a central server to coordinate operations. CRDTs are conflict-free data structures that merge updates peer-to-peer without central coordination, but consume more memory.</p>
                      <div class="buzzword-tags" style="margin-top: 4px;">
                        <span class="buzz-tag">Conflict Resolution</span>
                        <span class="buzz-tag">CRDT structures</span>
                        <span class="buzz-tag">Operational Transform</span>
                      </div>
                    </div>
                  </div>
                  <div class="qa-block">
                    <div class="question-header">Question: "Explain the socket connection handshake process."</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> Handshakes initiate over HTTP, upgrading to WebSockets if the client and server agree. This allows passing authentication tokens during the upgrade phase.</p>
                    </div>
                  </div>
                </div>
                """
            },
            "18": {
                "type": "revision",
                "title": "One Page Revision",
                "content": """
                <div class="revision-grid">
                  <div class="rev-card">
                    <div class="rev-card-title">Architecture</div>
                    <p>React Canvas Client -> Load Balancer -> Node.js WebSocket Cluster -> Redis Adapter -> MongoDB Document Store.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Database</div>
                    <p>MongoDB collections map itineraries and daily itinerary nodes, using indexing for lookup speeds.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Scaling</div>
                    <p>Redis Adapter routes events, stateless websocket nodes allow scaling, write caching buffers DB loads.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Security</div>
                    <p>WebSocket handshake JWT authentication checks. Role enforcement blocks edit attempts by unauthorized users.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Tech Stack</div>
                    <p>React, Node.js, Socket.io, Redis, MongoDB database.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Key Challenge</div>
                    <p>Collaborative desync resolved by replacing order-of-arrival logic with OT conflict resolution.</p>
                  </div>
                </div>
                """
            }
        }
    },
    # ── TIER 3: GRINDOS ──
    {
        "name": "GrindOS",
        "subtitle": "Offline-First CS Learning Environment & Desktop Application",
        "tagline": "Learning OS",
        "sections": {
            "01": {
                "type": "case-study",
                "title": "Executive Summary",
                "content": """
                <div class="case-study-grid">
                  <div class="cs-card">
                    <div class="cs-card-title">🚨 The Core Problem</div>
                    <p>Students face connection disruptions when accessing online learning portals, interrupting studies and creating inconsistent sync experiences.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">👥 Target Users & Value</div>
                    <p>CS students studying for placements. Provides access to study materials, practice problems, and tracking tools offline.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">🎯 Business Goal & Impact</div>
                    <p>Enable uninterrupted study sessions with local data replication, synchronizing updates when connection is restored.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">👑 My Role & Ownership</div>
                    <p><strong>Developer & Architect</strong>. Designed the Electron workspace, IndexedDB local storage synchronization engine, and offline asset resolvers.</p>
                  </div>
                </div>
                """
            },
            "02": {
                "type": "system",
                "title": "Product Vision",
                "content": """
                <div class="system-section">
                  <h3>Why We Built It</h3>
                  <p>Web portals require continuous internet connection. GrindOS operates offline-first, package-loading all assets locally to ensure access under poor connection profiles.</p>
                  <h3>Key Alternatives Analyzed</h3>
                  <table class="visual-table">
                    <thead>
                      <tr><th>Alternative</th><th>Drawback</th><th>GrindOS Advantage</th></tr>
                    </thead>
                    <tbody>
                      <tr><td>Web Portals</td><td>Cannot load without active connection; slow UI transitions.</td><td>Electron app running locally with instant loads.</td></tr>
                      <tr><td>PDF Booklets</td><td>Lacks interactive code editors or progress tracking.</td><td>Interactive environment with local progress tracking.</td></tr>
                    </tbody>
                  </table>
                  <h3>Core Feature Matrix</h3>
                  <ul>
                    <li><strong>Offline-First:</strong> Full core app function without internet connection.</li>
                    <li><strong>Local Database:</strong> Local data persistence using IndexedDB.</li>
                    <li><strong>Sync Service:</strong> Syncs local changes when connection is restored.</li>
                  </ul>
                </div>
                """
            },
            "03": {
                "type": "comparison",
                "title": "Tech Stack Deep Dive",
                "content": """
                <table class="comparison-table">
                  <thead>
                    <tr><th>Layer</th><th>Tech Chosen</th><th>Key Reason / Why</th><th>Trade-offs & Constraints</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>App Container</strong></td>
                      <td>Electron</td>
                      <td>Enables multi-platform desktop application builds using web technologies.</td>
                      <td>Higher memory footprint compared to native OS builds.</td>
                    </tr>
                    <tr>
                      <td><strong>Frontend</strong></td>
                      <td>HTML / JavaScript</td>
                      <td>Light UI layer that loads quickly.</td>
                      <td>Requires manual state rendering.</td>
                    </tr>
                    <tr>
                      <td><strong>Local DB</strong></td>
                      <td>IndexedDB / RxDB</td>
                      <td>Browser-native database with fast query performance.</td>
                      <td>Requires complex migration steps.</td>
                    </tr>
                    <tr>
                      <td><strong>Sync Layer</strong></td>
                      <td>PouchDB / CouchDB</td>
                      <td>Built-in database synchronization protocol.</td>
                      <td>Requires running a CouchDB server instance.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            "04": {
                "type": "architecture",
                "title": "High-Level Architecture",
                "content": """
                <div class="arch-diagram">
+--------------------+      Local Sync   +--------------------+      Couch Sync +--------------------+
|  Electron Window   | ----------------> |  IndexedDB (RxDB)  | --------------> | Remote CouchDB     |
|  (Local UI Render) |                   |  (Local Data Store)|                 | (Cloud Database)   |
+--------------------+                   +--------------------+                 +--------------------+
          ^                                        |                                       |
          | IPC Communication                      v Local System                          | User Sync
+--------------------+                   +--------------------+                            |
| Electron Main      | <---------------- | Local Assets       | <--------------------------+
| (Process Router)   |                   | (Bundled Files)    |
+--------------------+                   +--------------------+
                </div>
                <div class="arch-description">
                  <p><strong>Electron Window:</strong> UI window process, displaying app screens and calling IndexedDB.</p>
                  <p><strong>IndexedDB:</strong> Browser storage layer persisting study progress and bookmarks locally.</p>
                  <p><strong>Remote CouchDB:</strong> Syncs database when connection is restored, handling conflicts.</p>
                </div>
                """
            },
            "05": {
                "type": "flow",
                "title": "Request & Execution Flow",
                "content": """
                <div class="flow-diagram">
Render UI                 IndexedDB (Local)           Sync Service             Remote CouchDB
    |                            |                          |                         |
    |-- 1. Complete Topic ------>|                          |                         |
    |                            |-- 2. Store Record ------>|                         |
    |                            |                          |-- 3. Detect Internet -->|
    |                            |                          |-- 4. Replicate Db ----->|
    |                            |                          |<-- 5. Confirm Sync -----|
    |<-- 6. UI Sync Confirm -----|                          |                         |
                </div>
                <div class="flow-steps">
                  <ol>
                    <li><strong>Completion:</strong> Student completes a topic, updating progress in the UI.</li>
                    <li><strong>Write:</strong> The app writes the completion record to the local IndexedDB.</li>
                    <li><strong>Connection Detection:</strong> Sync service detects active internet connection.</li>
                    <li><strong>Sync:</strong> Local changes replicate to Remote CouchDB.</li>
                  </ol>
                </div>
                """
            },
            "06": {
                "type": "database",
                "title": "Database Design",
                "content": """
                <table class="db-table">
                  <thead>
                    <tr><th>Store</th><th>Fields</th><th>Schema Model</th><th>Indexes & Sync</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>TopicProgress</strong></td>
                      <td>_id, topicId, userId, completed, updatedAt</td>
                      <td>Document JSON</td>
                      <td>Index on `topicId`.</td>
                    </tr>
                    <tr>
                      <td><strong>UserNotes</strong></td>
                      <td>_id, topicId, userId, noteText, synced</td>
                      <td>Document JSON</td>
                      <td>Index on `topicId`.</td>
                    </tr>
                  </tbody>
                </table>
                <div class="db-notes">
                  <p><strong>Sync Flag:</strong> Storing a `synced` boolean flag on records tracks local updates awaiting synchronization.</p>
                  <p><strong>Index:</strong> An index on `topicId` accelerates query updates during study navigation.</p>
                </div>
                """
            },
            "07": {
                "type": "flow",
                "title": "Authentication Architecture",
                "content": """
                <div class="flow-diagram">
Electron UI               Local Encrypt               Remote Auth              CouchDB
    |                            |                         |                      |
    |-- 1. Submit Credentials -->|                         |                      |
    |                            |-- 2. Check Local token ->|                      |
    |                            |-- 3. POST Auth request ----------------------->|
    |                            |                         |<-- 4. JWT Approved --|
    |<-- 5. Access Granted ------|                         |                      |
                </div>
                <div class="auth-details">
                  <p><strong>Offline Authentication:</strong> Tokens are verified locally using cached session states when offline, validating credentials remotely on reconnection.</p>
                  <p><strong>Data Encryption:</strong> Local database files are encrypted using SQLCipher/AES-256 to protect user data.</p>
                </div>
                """
            },
            "08": {
                "type": "system",
                "title": "Core Engineering Systems",
                "content": """
                <div class="system-section">
                  <h3>Offline-First Sync Engine</h3>
                  <p>When connection returns, GrindOS replicates local progress records to the database server. Conflicts are resolved using CouchDB's revision keys:</p>
                  <pre style="background:#F7FAFC; padding:6px; border-radius:4px; font-family:monospace; font-size:7pt;">
# CouchDB revision synchronization logic
def sync_local_db(local_db, remote_db):
    try:
        # Replicates local changes to remote database
        local_db.replicate_to(remote_db)
        # Pulls updates from remote database
        remote_db.replicate_to(local_db)
    except ConnectionError:
        # Silently fail, queueing updates for retry on reconnection
        pass</pre>
                  <h3>Asset Resolvers</h3>
                  <p>Intercepts media requests, loading files from local resources to bypass network needs.</p>
                </div>
                """
            },
            "09": {
                "type": "comparison",
                "title": "Scalability Design",
                "content": """
                <table class="comparison-table">
                  <thead>
                    <tr><th>Scale</th><th>Bottleneck</th><th>Architectural Solution</th><th>Trade-offs</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>100 Users</strong></td>
                      <td>Local DB read overhead.</td>
                      <td>IndexedDB indices on query paths.</td>
                      <td>None; standard database management.</td>
                    </tr>
                    <tr>
                      <td><strong>1,000 Users</strong></td>
                      <td>Remote sync concurrency limits.</td>
                      <td>Autoscaling CouchDB clusters.</td>
                      <td>Higher server infrastructure cost.</td>
                    </tr>
                    <tr>
                      <td><strong>10,000 Users</strong></td>
                      <td>High conflict resolution overhead.</td>
                      <td>Deterministic last-write-wins policy.</td>
                      <td>Accidental overwrites on simultaneous edits.</td>
                    </tr>
                    <tr>
                      <td><strong>100k+ Users</strong></td>
                      <td>Static asset delivery limits.</td>
                      <td>Geo-distributed CDN edge caches.</td>
                      <td>CDN traffic cost footprints.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            "10": {
                "type": "system",
                "title": "Failure Handling & Recovery",
                "content": """
                <div class="system-section">
                  <h3>Fail-Safe Configurations</h3>
                  <ul>
                    <li><strong>Sync Failures:</strong> If network connections drop during replication, PouchDB rolls back the transaction, retrying when connectivity is verified.</li>
                    <li><strong>Local Corruptions:</strong> If local IndexedDB files corrupt, the application pulls user data from the remote database on login.</li>
                    <li><strong>Asset Missing:</strong> If a local asset fails to load, the app requests the file from the CDN, caching it locally for future use.</li>
                  </ul>
                </div>
                """
            },
            "11": {
                "type": "system",
                "title": "Monitoring & Observability",
                "content": """
                <div class="system-section">
                  <h3>Telemetry & Metrics Configuration</h3>
                  <ul>
                    <li><strong>Sync Failure Rate:</strong> Monitors replication drops to identify connectivity issues.</li>
                    <li><strong>Local DB Sizes:</strong> Tracks IndexedDB storage footprints to prevent disk usage issues.</li>
                    <li><strong>Asset Cache Hit Rates:</strong> Tracks hit rates to verify local asset delivery performance.</li>
                  </ul>
                </div>
                """
            },
            "12": {
                "type": "system",
                "title": "Cost Optimization",
                "content": """
                <div class="system-section">
                  <h3>Operational Cost Reductions</h3>
                  <ul>
                    <li><strong>Bundle Size Pruning:</strong> Removing unused dependencies reduces application download sizes.</li>
                    <li><strong>Sync Throttle:</strong> Sync replication tasks trigger only on key events, minimizing unnecessary traffic.</li>
                    <li><strong>Static Hosting:</strong> Hosting static files on CDN edges reduces web server compute costs.</li>
                  </ul>
                </div>
                """
            },
            "13": {
                "type": "system",
                "title": "Security Review",
                "content": """
                <div class="system-section">
                  <h3>Application Security Profile</h3>
                  <ul>
                    <li><strong>Threat: Data Tampering.</strong> Users editing local database records to falsify progress.</li>
                    <li><strong>Mitigation:</strong> Server verifies sync logs against validation checks before accepting database writes.</li>
                    <li><strong>Threat: Local Exploit.</strong> Exploits accessing Electron processes.</li>
                    <li><strong>Mitigation:</strong> Restrict IPC process scopes, disabling node integration on renderer threads.</li>
                  </ul>
                </div>
                """
            },
            "14": {
                "type": "case-study",
                "title": "Engineering Challenges",
                "content": """
                <div class="case-study-grid">
                  <div class="cs-card">
                    <div class="cs-card-title">🔥 Production Incident</div>
                    <p>The DB Sync Crash: Users logging in from multiple devices experienced desynced progress records and application crashes.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">🔎 Root Cause Analysis</div>
                    <p>Database synchronization did not calculate conflicts on concurrent edits, resulting in validation crashes.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">🛠️ The Fix Patch</div>
                    <p>Implemented PouchDB's conflict handling logic, resolving conflicts using a deterministic timestamp policy.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">📈 Key Lessons</div>
                    <p>Offline-first systems must implement conflict resolution policies from the start. Unhandled sync conflicts inevitably lead to database consistency issues.</p>
                  </div>
                </div>
                """
            },
            "15": {
                "type": "system",
                "title": "Future Roadmap",
                "content": """
                <div class="system-section">
                  <h3>Product Feature Roadmap</h3>
                  <ul>
                    <li><strong>Version 2: Peer-to-Peer Sync.</strong> Sync progress records between local network peers without cloud database steps.</li>
                    <li><strong>Version 3: Sandboxed Terminal.</strong> In-app code terminal execution without local developer setups.</li>
                  </ul>
                </div>
                """
            },
            "16": {
                "type": "interview",
                "title": "Interview Deep Dive",
                "content": """
                <div class="interview-qa">
                  <div class="qa-block">
                    <div class="question-header">Q: How does PouchDB synchronize data with CouchDB databases?</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> Sync uses CouchDB's replication protocol, checking revision keys to identify changes and applying updates incrementally.</p>
                    </div>
                  </div>
                  <div class="qa-block">
                    <div class="question-header">Q: What is the risk of using nodeIntegration in Electron applications?</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> Enabling nodeIntegration allows the renderer process to run node commands. If XSS occurs, attackers can run shell commands on the host OS.</p>
                    </div>
                  </div>
                </div>
                """
            },
            "17": {
                "type": "interview",
                "title": "Top Project Questions",
                "content": """
                <div class="interview-qa">
                  <div class="qa-block">
                    <div class="question-header">Question: "What is IndexedDB and how does it compare to localStorage?"</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> IndexedDB is a transactional database supporting large structured datasets, indexes, and async execution. localStorage is synchronous, blocking execution threads, and limited to 5MB.</p>
                      <div class="buzzword-tags" style="margin-top: 4px;">
                        <span class="buzz-tag">IndexedDB storage</span>
                        <span class="buzz-tag">localStorage limits</span>
                        <span class="buzz-tag">Async operations</span>
                      </div>
                    </div>
                  </div>
                  <div class="qa-block">
                    <div class="question-header">Question: "Explain how you handle offline sync conflicts."</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> We compare document revision tags. If there are conflicting versions, we apply a last-write-wins timestamp policy to resolve the differences.</p>
                    </div>
                  </div>
                </div>
                """
            },
            "18": {
                "type": "revision",
                "title": "One Page Revision",
                "content": """
                <div class="revision-grid">
                  <div class="rev-card">
                    <div class="rev-card-title">Architecture</div>
                    <p>Electron Window -> IndexedDB Local Store -> PouchDB Sync Manager -> Remote CouchDB Server.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Database</div>
                    <p>IndexedDB collections map topic progress and user notes, using indices for local lookup speeds.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Scaling</div>
                    <p>CouchDB sharding scales write capacities, local database offloads backend read requirements.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Security</div>
                    <p>Restricted Electron IPC bridges, encrypted IndexedDB database files, authenticated API replication steps.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Tech Stack</div>
                    <p>Electron, HTML, JavaScript, IndexedDB, PouchDB, CouchDB.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Key Challenge</div>
                    <p>DB replication conflicts resolved by implementing CouchDB revision-tag sorting policies.</p>
                  </div>
                </div>
                """
            }
        }
    },
    # ── TIER 3: SANKALAN ──
    {
        "name": "Sankalan",
        "subtitle": "Academic Resource Pathfinder & Collaborative Study Hub",
        "tagline": "Resource Hub",
        "sections": {
            "01": {
                "type": "case-study",
                "title": "Executive Summary",
                "content": """
                <div class="case-study-grid">
                  <div class="cs-card">
                    <div class="cs-card-title">🚨 The Core Problem</div>
                    <p>CS students waste time hunting down study notes and past papers, which are scattered across disorganized email threads and messaging channels.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">👥 Target Users & Value</div>
                    <p>Students looking for organized study guides and papers. Centralizes resources with clean search and tag filtering.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">🎯 Business Goal & Impact</div>
                    <p>Organize academic guides and papers in one dashboard, cutting student document search times by 90%.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">👑 My Role & Ownership</div>
                    <p><strong>Core Developer</strong>. Implemented the Postgres storage schema, BM25 indexing search endpoints, and file upload systems.</p>
                  </div>
                </div>
                """
            },
            "02": {
                "type": "system",
                "title": "Product Vision",
                "content": """
                <div class="system-section">
                  <h3>Why We Built It</h3>
                  <p>Study materials are scattered. Sankalan centralizes academic resources in a dashboard with tag filters, text search, and collaborative resource sharing.</p>
                  <h3>Key Alternatives Analyzed</h3>
                  <table class="visual-table">
                    <thead>
                      <tr><th>Alternative</th><th>Drawback</th><th>Sankalan Advantage</th></tr>
                    </thead>
                    <tbody>
                      <tr><td>Google Drive</td><td>Lacks text search within documents; slow file sharing.</td><td>Clean categorizations and fast searches.</td></tr>
                      <tr><td>Messaging Groups</td><td>Resource links get lost in chat histories.</td><td>Persistent, searchable library index.</td></tr>
                    </tbody>
                  </table>
                  <h3>Core Feature Matrix</h3>
                  <ul>
                    <li><strong>Smart Pathfinder:</strong> Recommends guides based on course history.</li>
                    <li><strong>Fast Search:</strong> Full-text indexing across document titles and tags.</li>
                    <li><strong>User Uploads:</strong> Safe file upload pipeline with verification controls.</li>
                  </ul>
                </div>
                """
            },
            "03": {
                "type": "comparison",
                "title": "Tech Stack Deep Dive",
                "content": """
                <table class="comparison-table">
                  <thead>
                    <tr><th>Layer</th><th>Tech Chosen</th><th>Key Reason / Why</th><th>Trade-offs & Constraints</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>Frontend</strong></td>
                      <td>Next.js</td>
                      <td>Server-side rendering speeds up first page loads and index parsing.</td>
                      <td>Increases server compute costs compared to static builds.</td>
                    </tr>
                    <tr>
                      <td><strong>Backend</strong></td>
                      <td>Node.js / Express</td>
                      <td>Handles file upload streams and API routes efficiently.</td>
                      <td>Single-threaded execution limits heavy processing paths.</td>
                    </tr>
                    <tr>
                      <td><strong>Database</strong></td>
                      <td>PostgreSQL</td>
                      <td>Structured SQL tables map courses and resource links.</td>
                      <td>Requires scaling database CPU limits under high search loads.</td>
                    </tr>
                    <tr>
                      <td><strong>Storage</strong></td>
                      <td>AWS S3</td>
                      <td>Scalable cloud storage for files, notes, and past papers.</td>
                      <td>Adds upload traffic transfer costs.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            "04": {
                "type": "architecture",
                "title": "High-Level Architecture",
                "content": """
                <div class="arch-diagram">
+--------------------+      HTTP POST    +--------------------+      Upload     +--------------------+
|  Next.js App       | ----------------> |  Node.js Backend   | --------------> | AWS S3 Bucket      |
|  (User Dashboard)  |                   |  (App API Route)   |                 | (Notes & PDFs Storage)|
+--------------------+                   +--------------------+                 +--------------------+
          ^                                        |                                       |
          | Search Results                         v PostgreSQL Connection                 | File URL
+--------------------+                   +--------------------+                            |
|  Search Engine     | <---------------- | PostgreSQL DB      | <--------------------------+
|  (BM25 fulltext)   |                   | (Metadata Index)   |
+--------------------+                   +--------------------+
                </div>
                <div class="arch-description">
                  <p><strong>Next.js Client:</strong> Renders search inputs, filters, and downloads resource files.</p>
                  <p><strong>Node.js Server:</strong> Validates user uploads, writes metadata to database, and uploads files to AWS S3.</p>
                  <p><strong>PostgreSQL DB:</strong> Indexes file names and tags to power fast user search paths.</p>
                </div>
                """
            },
            "05": {
                "type": "flow",
                "title": "Request & Execution Flow",
                "content": """
                <div class="flow-diagram">
Student                   Node.js Server              PostgreSQL DB            AWS S3 Bucket
   |                             |                          |                        |
   |-- 1. Upload study notes --->|                          |                        |
   |                             |-- 2. Validate payload -> |                        |
   |                             |-- 3. Upload file -------------------------------->|
   |                             |                          |<-- 4. Return URL ------|
   |                             |-- 5. Write metadata ---->|                        |
   |                             |<-- 6. Confirmed write ---|                        |
   |<-- 7. Upload Confirmed -----|                          |                        |
                </div>
                <div class="flow-steps">
                  <ol>
                    <li><strong>Upload:</strong> Student submits a study PDF via the upload dashboard.</li>
                    <li><strong>Validation:</strong> The server verifies the file type and checks the payload size.</li>
                    <li><strong>Cloud Storage:</strong> The server streams the file directly to AWS S3, returning the URL.</li>
                    <li><strong>Metadata Save:</strong> The database saves the file metadata and S3 path URL.</li>
                  </ol>
                </div>
                """
            },
            "06": {
                "type": "database",
                "title": "Database Design",
                "content": """
                <table class="db-table">
                  <thead>
                    <tr><th>Table</th><th>Fields</th><th>Types & Constraints</th><th>Indexes & Search</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>Resource</strong></td>
                      <td>id (PK), title, url, courseId, uploadedBy</td>
                      <td>UUID, VARCHAR, NOT NULL</td>
                      <td>Full-text index on `title`.</td>
                    </tr>
                    <tr>
                      <td><strong>Course</strong></td>
                      <td>id (PK), code, title, department</td>
                      <td>UUID, VARCHAR, NOT NULL</td>
                      <td>Index on `code`.</td>
                    </tr>
                  </tbody>
                </table>
                <div class="db-notes">
                  <p><strong>Relationships:</strong> A `Course` has many `Resource` files. Deleting a course cascades deletion to its file records.</p>
                  <p><strong>Indexing Strategy:</strong> A GIN index on `title` powers fast database-level full-text searches.</p>
                </div>
                """
            },
            "07": {
                "type": "flow",
                "title": "Authentication Architecture",
                "content": """
                <div class="flow-diagram">
Client                    Node.js Server              Auth Provider (Clerk)       PostgreSQL DB
  |                            |                             |                            |
  |-- 1. Get user session ---->|                             |                            |
  |                            |-- 2. Validate session token>|                            |
  |                            |                             |-- 3. Query credentials --->|
  |                            |                             |<-- 4. Access Approved -----|
  |<-- 5. User Authorized -----|                             |                            |
                </div>
                <div class="auth-details">
                  <p><strong>Session Controls:</strong> User session authorization checks run via Clerk API connections.</p>
                  <p><strong>Upload Security:</strong> Only verified users can upload study files, blocking guest upload attempts.</p>
                </div>
                """
            },
            "08": {
                "type": "system",
                "title": "Core Engineering Systems",
                "content": """
                <div class="system-section">
                  <h3>Full-Text Search Engine</h3>
                  <p>Sankalan maps academic study files to database records. To deliver fast query results, search endpoints use full-text indexing queries:</p>
                  <pre style="background:#F7FAFC; padding:6px; border-radius:4px; font-family:monospace; font-size:7pt;">
-- PostgreSQL Full-Text Search Query
SELECT id, title, url,
       ts_rank(to_tsvector('english', title), query) as rank
FROM "Resource", to_tsquery('english', :search_query) query
WHERE to_tsvector('english', title) @@ query
ORDER BY rank DESC
LIMIT 10;</pre>
                  <h3>Upload Sandbox Pipeline</h3>
                  <p>Scans uploaded files for malicious scripts before saving them to S3 storage buckets.</p>
                </div>
                """
            },
            "09": {
                "type": "comparison",
                "title": "Scalability Design",
                "content": """
                <table class="comparison-table">
                  <thead>
                    <tr><th>Scale</th><th>Bottleneck</th><th>Architectural Solution</th><th>Trade-offs</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>100 Users</strong></td>
                      <td>File upload network limits.</td>
                      <td>Stream files directly to S3.</td>
                      <td>None; standard best practice.</td>
                    </tr>
                    <tr>
                      <td><strong>1,000 Users</strong></td>
                      <td>Database search performance drops.</td>
                      <td>Add full-text indices.</td>
                      <td>Higher index storage footprints.</td>
                    </tr>
                    <tr>
                      <td><strong>10,000 Users</strong></td>
                      <td>High server load on file downloads.</td>
                      <td>Deliver S3 files via CloudFront.</td>
                      <td>CloudFront traffic cost overheads.</td>
                    </tr>
                    <tr>
                      <td><strong>100k+ Users</strong></td>
                      <td>Search index sync lag.</td>
                      <td>Migrate to Elasticsearch instances.</td>
                      <td>Higher infrastructure maintenance.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            "10": {
                "type": "system",
                "title": "Failure Handling & Recovery",
                "content": """
                <div class="system-section">
                  <h3>Failure Handling & Recovery</h3>
                  <ul>
                    <li><strong>Upload Drops:</strong> If upload streams break, client connection retry loops resume transfers from interrupted points.</li>
                    <li><strong>Database Outages:</strong> Cache course structures in Redis, ensuring dashboard read paths function on database drops.</li>
                    <li><strong>S3 Outages:</strong> Implement multi-region S3 replication, falling back to redundant buckets on connection failures.</li>
                  </ul>
                </div>
                """
            },
            "11": {
                "type": "system",
                "title": "Monitoring & Observability",
                "content": """
                <div class="system-section">
                  <h3>Telemetry & Metrics Configuration</h3>
                  <ul>
                    <li><strong>Search Latencies:</strong> Monitors full-text query runtimes to identify slow search queries.</li>
                    <li><strong>Upload Failure Rates:</strong> Tracks interrupted uploads to detect network transfer limits.</li>
                    <li><strong>Active Connections:</strong> Tracks database connection pool levels.</li>
                  </ul>
                </div>
                """
            },
            "12": {
                "type": "system",
                "title": "Cost Optimization",
                "content": """
                <div class="system-section">
                  <h3>Operational Cost Reductions</h3>
                  <ul>
                    <li><strong>S3 Lifecycle Rules:</strong> Move historical files to glacier storage, cutting S3 storage expenses.</li>
                    <li><strong>Image Compression:</strong> Automatically compress uploaded user preview images on the server before S3 uploads.</li>
                    <li><strong>CDN Caching:</strong> Cache search results at CDN edge nodes, reducing web server compute costs.</li>
                  </ul>
                </div>
                """
            },
            "13": {
                "type": "system",
                "title": "Security Review",
                "content": """
                <div class="system-section">
                  <h3>Security Threat Modeling</h3>
                  <ul>
                    <li><strong>Threat: Malicious File Uploads.</strong> Attackers upload scripts disguised as PDFs.</li>
                    <li><strong>Mitigation:</strong> Server checks file mime types and runs clamd scan checks before saving uploads.</li>
                    <li><strong>Threat: Hotlinking.</strong> Websites hotlinking directly to S3 download links, inflating egress costs.</li>
                    <li><strong>Mitigation:</strong> Use signed S3 URLs with short (e.g., 10 minute) expiration limits.</li>
                  </ul>
                </div>
                """
            },
            "14": {
                "type": "case-study",
                "title": "Engineering Challenges",
                "content": """
                <div class="case-study-grid">
                  <div class="cs-card">
                    <div class="cs-card-title">🔥 Production Incident</div>
                    <p>The Upload Crash: Node server processes crashed during major exam weeks due to OOM (Out Of Memory) limits.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">🔎 Root Cause Analysis</div>
                    <p>The upload API loaded entire files into server memory arrays before executing S3 saves, crashing processes on large files.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">🛠️ The Fix Patch</div>
                    <p>Replaced memory buffering with node streams (e.g., `multer-s3`), streaming uploads directly to S3.</p>
                  </div>
                  <div class="cs-card">
                    <div class="cs-card-title">📈 Key Lessons</div>
                    <p>Never buffer user uploads in application memory. Stream data directly to storage to prevent OOM server failures.</p>
                  </div>
                </div>
                """
            },
            "15": {
                "type": "system",
                "title": "Future Roadmap",
                "content": """
                <div class="system-section">
                  <h3>Product Feature Roadmap</h3>
                  <ul>
                    <li><strong>Version 2: In-browser PDF Reader.</strong> Render files directly in the dashboard, enabling collaborative highlighting.</li>
                    <li><strong>Version 3: AI Document Summarizer.</strong> Auto-generate key bullet points from uploaded notes files.</li>
                  </ul>
                </div>
                """
            },
            "16": {
                "type": "interview",
                "title": "Interview Deep Dive",
                "content": """
                <div class="interview-qa">
                  <div class="qa-block">
                    <div class="question-header">Q: How do you prevent buffer overflows when handling file uploads?</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> We set limits on incoming payloads (e.g., max 10MB) and stream files directly to disk or S3 without buffering in memory.</p>
                    </div>
                  </div>
                  <div class="qa-block">
                    <div class="question-header">Q: Why use S3 pre-signed URLs instead of public S3 links?</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> Pre-signed URLs authorize access for limited periods, preventing hotlinking and ensuring only authenticated users can download resources.</p>
                    </div>
                  </div>
                </div>
                """
            },
            "17": {
                "type": "interview",
                "title": "Top Project Questions",
                "content": """
                <div class="interview-qa">
                  <div class="qa-block">
                    <div class="question-header">Question: "What is full-text search and how does it compare to LIKE queries?"</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> Full-text search parses text, matches root words (stemming), and scores matches. LIKE performs character scans, which cannot utilize indexes and run slower.</p>
                      <div class="buzzword-tags" style="margin-top: 4px;">
                        <span class="buzz-tag">Full-Text indexing</span>
                        <span class="buzz-tag">Lexical stemming</span>
                        <span class="buzz-tag">GIN Search Index</span>
                      </div>
                    </div>
                  </div>
                  <div class="qa-block">
                    <div class="question-header">Question: "How do you scale static asset delivery?"</div>
                    <div class="model-answer">
                      <p><strong>Answer:</strong> We route files through a CDN (CloudFront), caching resources at edge nodes near users to offload the origin server.</p>
                    </div>
                  </div>
                </div>
                """
            },
            "18": {
                "type": "revision",
                "title": "One Page Revision",
                "content": """
                <div class="revision-grid">
                  <div class="rev-card">
                    <div class="rev-card-title">Architecture</div>
                    <p>Next.js UI -> Express Server -> S3 file storage / PostgreSQL database index search.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Database</div>
                    <p>PostgreSQL tables map course and resource rows, with full-text search indexings on titles.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Scaling</div>
                    <p>CloudFront handles file downloads, full-text indexes speed search routes, file streaming preserves memory.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Security</div>
                    <p>Pre-signed S3 links restrict downloads, clamd scanning checks uploads, and session JWTs verify users.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Tech Stack</div>
                    <p>Next.js, Node.js, Express, PostgreSQL database, AWS S3 buckets.</p>
                  </div>
                  <div class="rev-card">
                    <div class="rev-card-title">Key Challenge</div>
                    <p>Server memory crashes resolved by migrating from file buffering to direct network streams.</p>
                  </div>
                </div>
                """
            }
        }
    }
]

# RENDER INDIVIDUAL PAGES
content_pages_html = ""
current_page_idx = 4
total_pages_count = 129

# ROADMAP PAGE (PAGE 2)
roadmap_page = f"""
<div class="page" id="proj-roadmap">
  <div class="header">
    <div class="header-left">
      <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
      <div class="header-wordmark">GrindOS</div>
    </div>
    <div class="header-right">
      <div class="header-badge">ROADMAP &amp; SCOPE</div>
    </div>
  </div>
  
  <div style="padding: 24px 30px; flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 14px;">
    <h2 style="font-size: 20pt; font-weight: 800; color: #111; border-bottom: 2px solid #EA763F; padding-bottom: 6px;">Handbook Scope &amp; Project Priority</h2>
    <p style="font-size: 9.5pt; color: #4A5568; line-height: 1.5;">This handbook acts as an architectural blueprint of the key systems that define GrindOS. We break down the codebase into three tiers of systems engineering priority:</p>
    
    <div style="display: flex; flex-direction: column; gap: 10px;">
      <div style="background:#FFF5F0; border-left: 4px solid #EA763F; padding: 10px; border-radius: 4px;">
        <strong style="color: #EA763F; font-size: 10pt;">Tier 1 - Core Flagships (CraftaStudio, PlacePro, Mnemo)</strong>
        <p style="font-size: 8.5pt; color: #4A5568; margin-top: 2px;">High-yield systems focusing on graph scheduling engines, campus application transactional locks, and temporal semantic search algorithms.</p>
      </div>
      
      <div style="background:#F7FAFC; border-left: 4px solid #4A5568; padding: 10px; border-radius: 4px;">
        <strong style="color: #2D3748; font-size: 10pt;">Tier 2 - Collaborative Engines (ROVN, Travio)</strong>
        <p style="font-size: 8.5pt; color: #4A5568; margin-top: 2px;">Focuses on live message synchronization, Operational Transformation (OT) conflict sorting, and webhook ingestions.</p>
      </div>
      
      <div style="background:#F7FAFC; border-left: 4px solid #718096; padding: 10px; border-radius: 4px;">
        <strong style="color: #718096; font-size: 10pt;">Tier 3 - Systems Foundations (GrindOS Desktop, Sankalan)</strong>
        <p style="font-size: 8.5pt; color: #4A5568; margin-top: 2px;">Focuses on offline-first IndexedDB database replication, electron containers, and full-text index lookups.</p>
      </div>
    </div>
  </div>
  
  <div class="footer">
    <div class="footer-left">
      <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
      <div class="breadcrumb">GrindOS <span>›</span> Projects <span>›</span> <span>Roadmap</span></div>
    </div>
    <div class="page-number-premium">PAGE 02 / 129</div>
  </div>
</div>
"""

# TOC PAGE (PAGE 3)
toc_page = f"""
<div class="page" id="proj-toc">
  <div class="header">
    <div class="header-left">
      <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
      <div class="header-wordmark">GrindOS</div>
    </div>
    <div class="header-right">
      <div class="header-badge">TABLE OF CONTENTS</div>
    </div>
  </div>
  
  <div style="padding: 24px 30px; flex: 1; display: flex; flex-direction: column; justify-content: center;">
    <h2 style="font-size: 20pt; font-weight: 800; color: #111; border-bottom: 2px solid #EA763F; padding-bottom: 6px; margin-bottom: 14px;">Index of Engineering Systems</h2>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; font-size: 8pt; line-height: 1.45;">
      <div>
        <strong style="color: #EA763F; font-size: 9pt; display: block; border-bottom: 1px solid #EBE5DB; margin-bottom: 4px; padding-bottom: 2px;">Tier 1 Projects</strong>
        <ul style="list-style: none;">
          <li>• CraftaStudio (AI Code Gen) <span style="color:#A0AEC0;">....................</span> Page 04</li>
          <li>• PlacePro (Placement Portal) <span style="color:#A0AEC0;">....................</span> Page 22</li>
          <li>• Mnemo (Memory Layer) <span style="color:#A0AEC0;">.........................</span> Page 40</li>
        </ul>
        
        <strong style="color: #2D3748; font-size: 9pt; display: block; border-bottom: 1px solid #EBE5DB; margin-top: 10px; margin-bottom: 4px; padding-bottom: 2px;">Tier 2 Projects</strong>
        <ul style="list-style: none;">
          <li>• ROVN (Lead Co-Pilot) <span style="color:#A0AEC0;">..........................</span> Page 58</li>
          <li>• Travio (Trip Planner) <span style="color:#A0AEC0;">..........................</span> Page 76</li>
        </ul>
      </div>
      
      <div>
        <strong style="color: #718096; font-size: 9pt; display: block; border-bottom: 1px solid #EBE5DB; margin-bottom: 4px; padding-bottom: 2px;">Tier 3 Projects</strong>
        <ul style="list-style: none;">
          <li>• GrindOS (Offline Learning) <span style="color:#A0AEC0;">....................</span> Page 94</li>
          <li>• Sankalan (Resource Hub) <span style="color:#A0AEC0;">.....................</span> Page 112</li>
        </ul>
        
        <strong style="color: #E53E3E; font-size: 9pt; display: block; border-bottom: 1px solid #EBE5DB; margin-top: 10px; margin-bottom: 4px; padding-bottom: 2px;">System Revision Summary</strong>
        <p style="color: #4A5568;">For each project, we cover Executive Summary, Product Vision, Tech Stack, High-Level Architecture, Request Flow, Database, Auth, Core Systems, Scaling, Failovers, Monitoring, Costs, Security, Challenges, Roadmap, and Interview Deep Dives.</p>
      </div>
    </div>
  </div>
  
  <div class="footer">
    <div class="footer-left">
      <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
      <div class="breadcrumb">GrindOS <span>›</span> Projects <span>›</span> <span>Index</span></div>
    </div>
    <div class="page-number-premium">PAGE 03 / 129</div>
  </div>
</div>
"""

# CONSTRUCT 126 SYSTEM PAGES (18 per project * 7 projects)
for proj in projects_data:
    for sec_num in sorted(proj["sections"].keys()):
        sec = proj["sections"][sec_num]
        layout_type = sec["type"]
        title = sec["title"]
        content = sec["content"]
        
        # Build page HTML
        page_html = f"""
<div class="page" id="proj-{proj['name'].lower()}-{sec_num}">
  <div class="header">
    <div class="header-left">
      <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
      <div class="header-wordmark">GrindOS</div>
    </div>
    <div class="header-right">
      <div class="badge-yield">{proj['tagline'].upper()}</div>
      <div class="header-badge">{proj['name']}</div>
    </div>
  </div>
  
  <div class="topic-bar">
    <div class="topic-bar-top">
      <div class="topic-eyebrow">Section {sec_num} &mdash; {proj['name']}</div>
      <div class="yield-rating">Yield: <span class="stars-gold">★★★★★</span></div>
    </div>
    <div class="topic-title">{title}</div>
    <div class="topic-subtitle">{proj['subtitle']}</div>
  </div>
  
  <div class="body-container-{layout_type}">
    {content}
  </div>
  
  <div class="footer">
    <div class="footer-left">
      <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
      <div class="breadcrumb">GrindOS <span>›</span> {proj['name']} <span>›</span> <span>{title}</span></div>
    </div>
    <div class="page-number-premium">PAGE {str(current_page_idx).zfill(2)} / {total_pages_count}</div>
  </div>
</div>
"""
        content_pages_html += page_html
        current_page_idx += 1

# COVER PAGE (PAGE 1)
cover_page = f"""
<div class="page cover-page" id="proj-cover">
  <div class="cover-logo-container">
    <img src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS">
  </div>
  <div class="cover-eyebrow">GrindOS Flagship Series</div>
  <div class="cover-title">Projects &amp;<br>Architecture</div>
  <div class="cover-subtitle">Engineering Systems, Architecture, Scalability &amp;<br>Interview Preparation Handbook</div>
  <div style="font-size: 11pt; color: #718096; font-weight: 700; margin-top: -30px; margin-bottom: 50px;">Created by Pranav Gawai</div>
  <div class="cover-footer">
    <img src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
    <a href="https://grindos.pranavx.in">grindos.pranavx.in</a>
  </div>
</div>
"""

# CSS SYSTEMS
css = f"""
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
  @page {{ size: A4 portrait; margin: 0; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ font-family: 'DM Sans', sans-serif; background: #E5E7EB; color: #2D3748; }}
  
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
  .cover-title {{ font-size: 38pt; font-weight: 800; color: #111; line-height: 1.1; margin-bottom: 30px; letter-spacing: -1.5px; }}
  .cover-subtitle {{ font-size: 15pt; color: #666; font-weight: 600; margin-bottom: 60px; line-height: 1.4; }}
  .cover-footer {{ position: absolute; bottom: 60px; font-size: 12pt; font-weight: 800; color: #888; letter-spacing: 1px; display: flex; align-items: center; gap: 12px; }}
  .cover-footer img {{ height: 24px; }}
  .cover-footer a {{ text-decoration: none; color: inherit; }}

  /* HEADER (L1) */
  .header {{ height: 11mm; padding: 0 24px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1.5px solid #F3EDE2; flex-shrink: 0; background: #FAF8F5; margin-top: 5mm; margin-left: 5mm; margin-right: 5mm; }}
  .header-left {{ display: flex; align-items: center; gap: 8px; }}
  .header-logo {{ height: 18px; }}
  .header-wordmark {{ font-size: 12pt; font-weight: 800; color: #1A202C; letter-spacing: -0.5px; }}
  .header-right {{ display: flex; align-items: center; gap: 8px; }}
  .header-badge {{ font-size: 7.5pt; font-weight: 800; color: #718096; background: #EDF2F7; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.5px; }}
  .badge-yield {{ font-size: 7.5pt; font-weight: 800; padding: 3px 8px; border-radius: 4px; letter-spacing: 0.5px; background: #FFF5F0; color: #EA763F; border: 1px solid #FEEBC8; }}

  /* TOPIC BAR (L2) */
  .topic-bar {{ padding: 12px 24px; border-bottom: 1px solid #EDE5D8; background: #FCFAF7; flex-shrink: 0; margin-left: 5mm; margin-right: 5mm; }}
  .topic-bar-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }}
  .topic-eyebrow {{ font-size: 8.5pt; font-weight: 800; color: #EA763F; text-transform: uppercase; letter-spacing: 1px; }}
  .yield-rating {{ font-size: 8.5pt; font-weight: 700; color: #718096; }}
  .stars-gold {{ color: #DD6B20; font-weight: 800; }}
  .topic-title {{ font-size: 16pt; font-weight: 800; color: #111; letter-spacing: -0.5px; }}
  .topic-subtitle {{ font-size: 9pt; color: #718096; font-weight: 500; margin-top: 1px; }}

  /* BODY CONTAINER TYPES (L3) */
  [class^="body-container-"] {{
    flex: 1;
    overflow: hidden;
    padding: 16px 24px;
    margin-left: 5mm;
    margin-right: 5mm;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}

  /* CASE STUDY PAGE LAYOUT */
  .case-study-grid {{ display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 12px; height: 100%; }}
  .cs-card {{ border: 1px solid #EBE5DB; border-radius: 8px; padding: 12px 14px; background: #FCFAF7; display: flex; flex-direction: column; justify-content: center; }}
  .cs-card-title {{ font-size: 9.5pt; font-weight: 800; color: #EA763F; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px; }}
  .cs-card p {{ font-size: 8pt; line-height: 1.45; color: #2D3748; }}

  /* SYSTEM LAYOUT */
  .system-section {{ display: flex; flex-direction: column; gap: 10px; height: 100%; justify-content: center; }}
  .system-section h3 {{ font-size: 10pt; font-weight: 800; color: #EA763F; border-bottom: 1.5px solid #F3EDE2; padding-bottom: 4px; }}
  .system-section p {{ font-size: 8pt; line-height: 1.45; color: #4A5568; }}
  .system-section ul {{ list-style-type: square; margin-left: 16px; font-size: 8pt; line-height: 1.45; color: #4A5568; }}

  /* COMPARISON LAYOUT */
  .comparison-table {{ width: 100%; border-collapse: collapse; font-size: 7.5pt; text-align: left; margin: auto 0; }}
  .comparison-table th {{ background: #FAF8F5; color: #EA763F; font-weight: 800; padding: 8px; border-bottom: 2px solid #EBE5DB; border-top: 1px solid #EBE5DB; }}
  .comparison-table td {{ padding: 8px; border-bottom: 1px solid #EBE5DB; line-height: 1.35; }}
  .comparison-table tr:nth-child(even) {{ background: #FCFAF7; }}

  /* ARCHITECTURE LAYOUT */
  .arch-diagram {{
    background: #2D3748;
    color: #F7FAFC;
    padding: 10px;
    border-radius: 8px;
    font-family: monospace;
    font-size: 6.5pt;
    line-height: 1.3;
    white-space: pre;
    overflow-x: auto;
    text-align: center;
    border: 1px solid #1A202C;
    margin: auto 0;
  }}
  .arch-description {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 7.5pt; line-height: 1.4; color: #4A5568; margin-top: 6px; }}

  /* FLOW LAYOUT */
  .flow-diagram {{
    background: #F7FAFC;
    color: #2D3748;
    padding: 10px;
    border-radius: 8px;
    font-family: monospace;
    font-size: 6.5pt;
    line-height: 1.3;
    white-space: pre;
    overflow-x: auto;
    border: 1px solid #E2E8F0;
    margin: auto 0;
  }}
  .flow-steps {{ font-size: 7.5pt; line-height: 1.4; color: #4A5568; margin-top: 6px; }}
  .flow-steps ol {{ margin-left: 16px; }}

  /* DATABASE LAYOUT */
  .db-table {{ width: 100%; border-collapse: collapse; font-size: 7.5pt; text-align: left; margin: auto 0; }}
  .db-table th {{ background: #FAF8F5; color: #EA763F; font-weight: 800; padding: 6px; border-bottom: 2px solid #EBE5DB; }}
  .db-table td {{ padding: 6px; border-bottom: 1px solid #EBE5DB; }}
  .db-notes {{ font-size: 7.5pt; line-height: 1.4; color: #4A5568; margin-top: 8px; }}

  /* INTERVIEW LAYOUT */
  .interview-qa {{ display: flex; flex-direction: column; gap: 12px; height: 100%; justify-content: center; }}
  .qa-block {{ border: 1px solid #E2E8F0; border-radius: 8px; overflow: hidden; }}
  .question-header {{ background: #FFF5F0; border-bottom: 1px solid #FEEBC8; color: #EA763F; font-weight: 800; font-size: 8.5pt; padding: 6px 10px; }}
  .model-answer {{ background: #FFFFFF; padding: 8px 10px; font-size: 8pt; line-height: 1.4; color: #2D3748; }}

  /* REVISION LAYOUT */
  .revision-grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 10px; height: 100%; }}
  .rev-card {{ border: 1px solid #EBE5DB; border-radius: 8px; padding: 10px; background: #FCFAF7; display: flex; flex-direction: column; justify-content: center; }}
  .rev-card-title {{ font-size: 8.5pt; font-weight: 800; color: #EA763F; margin-bottom: 4px; text-transform: uppercase; }}
  .rev-card p {{ font-size: 7.5pt; line-height: 1.35; color: #4A5568; }}

  /* STANDARD TABLE STYLING */
  .visual-table {{ width: 100%; border-collapse: collapse; font-size: 7.5pt; text-align: left; margin: 4px 0; }}
  .visual-table th {{ background: #F7FAFC; color: #4A5568; padding: 6px; border-bottom: 1.5px solid #CBD5E0; font-weight: 800; }}
  .visual-table td {{ padding: 6px; border-bottom: 1px solid #E2E8F0; }}

  /* BUZZWORD TAGS */
  .buzzword-tags {{ display: flex; gap: 4px; flex-wrap: wrap; margin-top: 4px; }}
  .buzz-tag {{ background: #F5EBFE; border: 1px solid #E9D8FD; color: #6B46C1; padding: 2px 6px; border-radius: 4px; font-weight: 800; font-size: 6.5pt; text-transform: uppercase; }}

  /* FOOTER (L5) */
  .footer {{ width: 100%; height: 36px; background: white; border-top: 1px solid #EDE5D8; display: flex; justify-content: space-between; align-items: center; padding: 0 24px; font-size: 8.5pt; color: #718096; flex-shrink: 0; font-weight: 700; margin-bottom: 5mm; margin-left: 5mm; margin-right: 5mm; }}
  .footer-left {{ display: flex; align-items: center; gap: 8px; }}
  .footer-logo {{ height: 14px; }}
  .breadcrumb {{ color: #A0AEC0; }}
  .breadcrumb span {{ color: #4A5568; font-weight: 800; margin: 0 4px; }}
  .page-number-premium {{ font-size: 8.5pt; font-weight: 800; color: #EA763F; letter-spacing: 1px; background: #FFF5F0; padding: 3px 10px; border-radius: 4px; border: 1px solid #FBD38D; }}
"""

# COMPILE FINAL HTML TEMPLATE
html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Projects &amp; Architecture Handbook</title>
<style>{css}</style>
</head>
<body>
  <!-- COVER PAGE -->
  {cover_page}
  
  <!-- ROADMAP PAGE -->
  {roadmap_page}
  
  <!-- TOC PAGE -->
  {toc_page}
  
  <!-- CONTENT PAGES -->
  {content_pages_html}
</body>
</html>
"""

# Write output HTML file
os.makedirs("subjects/projects", exist_ok=True)
output_path = "subjects/projects/01_projects.html"
with open(output_path, "w") as f:
    f.write(html_out)

print(f"Successfully generated Projects & Architecture Handbook with {current_page_idx - 1} pages.")
