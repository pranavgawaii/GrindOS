# -*- coding: utf-8 -*-
"""
PROJECT CONTENT  — structured fields + 7 diagram specs per project.
Consumed by make_handbook_projects.py via the section builder.
"""

# Shared Mermaid styling — keep diagrams on-brand & color-coded to the legend.
CD = """
classDef client fill:#FBF8F4,stroke:#EA763F,stroke-width:2px,color:#0F172A;
classDef svc fill:#EFF4FF,stroke:#2563EB,stroke-width:2px,color:#0F172A;
classDef data fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#0F172A;
classDef ext fill:#F5F3FF,stroke:#7C3AED,stroke-width:2px,color:#0F172A;
classDef queue fill:#FFFBEB,stroke:#D97706,stroke-width:2px,color:#0F172A;
classDef bad fill:#FEF2F2,stroke:#DC2626,stroke-width:2px,color:#0F172A;
"""
LEGEND = [("#FBF8F4","Client / Edge"),("#EFF4FF","Service"),("#ECFDF5","Data store"),
          ("#FFFBEB","Async / Queue"),("#F5F3FF","External API")]
LEGEND_FAIL = [("#ECFDF5","Healthy"),("#FEF2F2","Failed / Degraded"),("#FFFBEB","Recovery path")]

PROJECTS = []

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  1 · CRAFTASTUDIO                                                          ║
# ╚══════════════════════════════════════════════════════════════════════════╝
PROJECTS.append({
"name":"CraftaStudio","pnum":"01","tagline":"AI Code-Gen",
"subtitle":"AI-powered structural code generation on a topological dependency-graph engine.",
"band_meta":[("Full-Stack","Domain"),("DAG Scheduler","Core"),("99.9%","Gen Success"),("Tier 1","Priority")],
"diagrams":{
 "arch":{"id":"cs-arch","title":"CraftaStudio — System Architecture","kind":"C4 / Container","legend":LEGEND,
  "code":CD+"""
flowchart TB
  U([User]):::client
  subgraph EDGE["Browser"]
    UI["Next.js Canvas<br/>ReactFlow"]:::client
    WC["WebContainer<br/>Sandbox Preview"]:::client
  end
  subgraph CORE["Application Tier"]
    GW["Node.js Gateway<br/>Auth · DB sync"]:::svc
    WS["Socket.io<br/>Realtime fan-out"]:::svc
    AG["FastAPI Agent<br/>Graph executor"]:::svc
  end
  subgraph DATA["State & Async"]
    PG[("PostgreSQL<br/>Prisma")]:::data
    RQ[["Upstash Redis<br/>Job Queue"]]:::queue
  end
  LLM{{"Groq · Llama-3<br/>Bedrock fallback"}}:::ext
  U --> UI
  UI <-->|WebSocket| WS
  UI -->|REST| GW
  GW --> PG
  GW -->|enqueue| RQ
  RQ -->|dequeue| AG
  AG --> PG
  AG -->|inference| LLM
  AG -->|emit code| WS --> UI --> WC
""",
  "eraser":"""// paste into eraser.io
User [icon: user]
Canvas [icon: monitor, color: orange]
Gateway [icon: nodejs, color: blue]
Realtime [icon: socket, color: blue]
Agent [icon: python, color: blue]
Postgres [icon: postgresql, color: green]
Queue [icon: redis, color: amber]
LLM [icon: openai, color: purple]

User > Canvas
Canvas <> Realtime: WebSocket
Canvas > Gateway: REST
Gateway > Postgres
Gateway > Queue: enqueue
Queue > Agent: dequeue
Agent > LLM: inference
Agent > Realtime: emit code
Realtime > Canvas""",
  "components":[("Canvas","ReactFlow node editor; streams graph mutations over WS."),
    ("Gateway","Node.js: authz, Prisma writes, enqueues jobs."),
    ("Agent","FastAPI worker: topo-sort + context-isolated generation."),
    ("Queue","Upstash Redis decouples request from slow LLM work."),
    ("LLM","Groq primary, Bedrock fallback on 429.")],
  "layout":"Three horizontal bands top-to-bottom: <b>Browser</b> (orange) holds the canvas and the in-browser sandbox; "
    "the <b>Application tier</b> (blue) sits center with gateway, realtime, and agent boxes; the <b>data & async</b> band "
    "(green/amber) anchors the bottom. The external LLM floats right as a hexagon. The defining loop is the <b>async return path</b>: "
    "Gateway → Queue → Agent → LLM → Realtime → Canvas, drawn as a clockwise cycle so reviewers instantly see write/read are decoupled."},
 "flow":{"id":"cs-flow","title":"Build Codebase — Request Lifecycle","kind":"Sequence","legend":None,
  "code":"""
sequenceDiagram
  autonumber
  participant U as Canvas
  participant G as Gateway
  participant Q as Redis Queue
  participant A as FastAPI Agent
  participant L as Groq LLM
  participant D as Postgres
  U->>G: POST /build (graph nodes+edges)
  G->>G: validate · Tarjan cycle check
  G->>D: persist graph state
  G->>Q: enqueue topo-sorted jobs
  G-->>U: 202 Accepted (jobId)
  loop per node in topo order
    Q->>A: dequeue job
    A->>D: read parent signatures
    A->>L: prompt (parent types injected)
    L-->>A: code (JSON)
    A->>A: repair · syntax validate
    A->>D: write node.code
    A-->>U: WS broadcast (node done)
  end
""",
  "eraser":"""Canvas > Gateway: POST /build
Gateway > Gateway: validate + cycle check
Gateway > Postgres: persist graph
Gateway > Queue: enqueue jobs
Gateway > Canvas: 202 jobId
Queue > Agent: dequeue (loop)
Agent > Postgres: read parents
Agent > LLM: prompt
LLM > Agent: code
Agent > Postgres: write code
Agent > Canvas: WS node done""",
  "components":[("202 pattern","Client never blocks on LLM latency."),
    ("Topo loop","Parents generated before children — types flow downward."),
    ("Repair stage","Strips markdown fences, fixes brackets before commit."),
    ("WS broadcast","Per-node completion renders incrementally.")],
  "layout":"A 6-actor sequence. The first four messages form a tight <b>synchronous prelude</b> (validate → persist → enqueue → 202), "
    "then a boxed <b>loop</b> dominates the lower two-thirds repeating per node. Self-messages (validate, repair) are short right-curls. "
    "The dashed <b>202 Accepted</b> arrow returns early and high, visually proving the client is freed before any generation begins."},
 "erd":{"id":"cs-erd","title":"CraftaStudio — Data Model","kind":"ERD","legend":None,
  "code":"""
erDiagram
  USER ||--o{ PROJECT : owns
  PROJECT ||--o{ BLOCK_NODE : contains
  PROJECT ||--o{ BLOCK_EDGE : contains
  BLOCK_NODE ||--o{ BLOCK_EDGE : "source/target"
  USER {
    uuid id PK
    string clerk_id UK
    string email
  }
  PROJECT {
    uuid id PK
    uuid user_id FK
    string name
    timestamp created_at
  }
  BLOCK_NODE {
    uuid id PK
    uuid project_id FK
    string type
    text code
    enum status
  }
  BLOCK_EDGE {
    uuid id PK
    uuid project_id FK
    uuid source_id FK
    uuid target_id FK
  }
""",
  "eraser":"""USER { id pk; clerk_id; email }
PROJECT { id pk; user_id fk; name }
BLOCK_NODE { id pk; project_id fk; type; code; status }
BLOCK_EDGE { id pk; source_id fk; target_id fk }
USER 1-* PROJECT
PROJECT 1-* BLOCK_NODE
PROJECT 1-* BLOCK_EDGE
BLOCK_NODE 1-* BLOCK_EDGE""",
  "components":[("Edges as rows","Graph stored relationally — edges are first-class rows, not JSON."),
    ("Composite idx","(project_id, status) drives the scheduler's pending-node scan."),
    ("Source index","source_id indexed for O(1) child traversal in topo-sort."),
    ("Cascade","Deleting a project cascades to nodes + edges.")],
  "layout":"Classic crow's-foot ERD. <b>USER</b> top-left, fanning right to <b>PROJECT</b>, which fans down to the twin "
    "<b>BLOCK_NODE</b> and <b>BLOCK_EDGE</b> tables. The reflexive edge (BLOCK_EDGE referencing BLOCK_NODE twice as source/target) "
    "is the visual star — it encodes the DAG inside SQL. PK rows bold-topped, FK rows tagged, cardinality crow's-feet on every join."},
 "auth":{"id":"cs-auth","title":"Clerk OAuth + Row-Level Isolation","kind":"Sequence","legend":None,
  "code":"""
sequenceDiagram
  autonumber
  participant C as Client
  participant K as Clerk (OAuth)
  participant G as Gateway
  participant P as Prisma/PG
  C->>K: OAuth login
  K-->>C: signed JWT (claims)
  C->>G: API call + Bearer JWT
  G->>G: verify signature (JWKS)
  G->>P: query WHERE user_id = sub
  P-->>G: row-scoped result
  G-->>C: 200 (only owned data)
  Note over G,P: every query carries tenant filter
""",
  "eraser":"""Client > Clerk: OAuth login
Clerk > Client: JWT
Client > Gateway: Bearer JWT
Gateway > Gateway: verify JWKS
Gateway > Prisma: WHERE user_id=sub
Prisma > Gateway: scoped rows
Gateway > Client: 200""",
  "components":[("Clerk","Delegated identity; issues short-lived JWT with custom claims."),
    ("JWKS verify","Gateway validates signature against rotating public keys."),
    ("Tenant filter","Global Prisma middleware injects WHERE user_id."),
    ("Defense-in-depth","ORM filter + app check — never trust client claims alone.")],
  "layout":"Four-actor sequence split into two phases by a faint vertical gap: <b>Issuance</b> (Client↔Clerk, top) and "
    "<b>Enforcement</b> (Client→Gateway→Prisma, bottom). A spanning <b>Note</b> band under the gateway/DB pair reads "
    "'every query carries tenant filter' — the security thesis. The self-message 'verify JWKS' is highlighted to mark the trust boundary."},
 "deploy":{"id":"cs-deploy","title":"Cloud Deployment Topology","kind":"Deployment","legend":LEGEND,
  "code":CD+"""
flowchart TB
  U([Users]):::client
  CDN["Vercel Edge CDN"]:::client
  subgraph VERCEL["Vercel"]
    FE["Next.js Frontend"]:::client
    EDGE["Edge Middleware<br/>auth gate"]:::svc
  end
  subgraph AWS["AWS ECS Fargate"]
    LB["ALB"]:::svc
    GW["Gateway tasks xN"]:::svc
    AG["Agent workers xN"]:::svc
  end
  subgraph MANAGED["Managed Data"]
    PG[("Supabase PG<br/>+ PgBouncer")]:::data
    RD[["Upstash Redis"]]:::queue
    S3[("S3 — assets")]:::data
  end
  LLM{{Groq / Bedrock}}:::ext
  U-->CDN-->FE-->EDGE-->LB
  LB-->GW-->PG & RD
  RD-->AG-->PG & LLM
  AG-->S3
""",
  "eraser":"""Users > CDN > Frontend > Edge auth > ALB
ALB > Gateway tasks
Gateway > Postgres + Redis
Redis > Agent workers
Agent > Postgres + LLM + S3
// zones: Vercel | AWS ECS | Managed Data""",
  "components":[("Vercel edge","Static + SSR frontend, auth at the edge."),
    ("ECS Fargate","Serverless containers; gateway and agents scale independently."),
    ("PgBouncer","Connection pooling so Fargate scale-out doesn't exhaust PG."),
    ("Managed data","Supabase + Upstash + S3 — no self-hosted state.")],
  "layout":"Three labeled cloud boundaries stacked vertically: <b>Vercel</b> (edge/frontend, orange), <b>AWS ECS</b> "
    "(compute, blue), <b>Managed Data</b> (green/amber). Users enter top through the CDN. The key reviewer takeaway is the "
    "<b>independent scale groups</b> 'xN' on gateway and agent tasks, and that all state lives in the managed band — compute is stateless and disposable."},
 "scale":{"id":"cs-scale","title":"Scaling Evolution — 100 → 1M","kind":"Evolution","legend":None,
  "code":CD+"""
flowchart LR
  subgraph S1["100 users"]
    A1["Single Node + in-mem WS"]:::svc
  end
  subgraph S2["1K users"]
    A2["PgBouncer pool"]:::svc-->B2[("PG")]:::data
  end
  subgraph S3["10K users"]
    A3["Multi-provider LLM<br/>Groq→Bedrock"]:::ext
  end
  subgraph S4["100K users"]
    A4["ECS worker fleet<br/>Redis WS adapter"]:::queue
  end
  subgraph S5["1M users"]
    A5["Sharded queues<br/>read replicas + CDN"]:::data
  end
  S1-->S2-->S3-->S4-->S5
""",
  "eraser":"""100u: single node, in-mem WS
1K: PgBouncer pooling
10K: multi-provider LLM fallback
100K: ECS worker fleet + Redis WS adapter
1M: sharded queues, read replicas, CDN""",
  "components":[("100","Vertical box; WS state in process memory."),
    ("1K","PgBouncer ends connection exhaustion."),
    ("10K","LLM rate limits → provider fallback pipeline."),
    ("100K","Redis adapter lets WS scale horizontally across tasks."),
    ("1M","Queue sharding + replicas; assets fully on CDN.")],
  "layout":"A left-to-right <b>maturity staircase</b> of five stages, each a labeled box growing in internal complexity. "
    "Arrows connect stages so the eye reads it as a timeline. Color shifts from a single blue box (100) to a multi-color "
    "cluster (1M), visually encoding that scale = more component types, not just more boxes."},
 "failure":{"id":"cs-fail","title":"Failure & Recovery Topology","kind":"Resilience","legend":LEGEND_FAIL,
  "code":CD+"""
flowchart TB
  J[["Job from Queue"]]:::queue
  A["Agent"]:::svc
  L1{{Groq}}:::ext
  L2{{Bedrock fallback}}:::ext
  OK[("Commit to PG")]:::data
  DLQ[["Dead Letter Queue"]]:::bad
  UI["UI: marked failed"]:::bad
  J-->A-->L1
  L1-->|429 / timeout| R{retry x3<br/>backoff+jitter}
  R-->|ok| OK
  R-->|exhausted| L2
  L2-->|ok| OK
  L2-->|fail| DLQ-->UI
""",
  "eraser":"""Queue > Agent > Groq
Groq fail > retry(3, backoff+jitter)
retry ok > commit PG
retry exhausted > Bedrock fallback
Bedrock ok > commit
Bedrock fail > DLQ > UI failed""",
  "components":[("Backoff+jitter","2^n + random ms avoids thundering-herd retries."),
    ("Provider fallback","Groq exhausted → Bedrock, not instant failure."),
    ("DLQ","3x failure parks the job for inspection, not silent loss."),
    ("Honest UI","User always sees terminal state — failed, never spinning forever.")],
  "layout":"A vertical decision tree. The <b>happy path</b> (green) runs straight down the center. Failure branches peel "
    "off to the right into a red <b>retry</b> diamond, then a violet <b>fallback</b> provider, and finally the red <b>DLQ</b> at "
    "bottom-right. Color does the work: green = recovered, red = degraded, so the recovery story is legible at a glance."},
},
"fields":{
 "summary_lead":"CraftaStudio treats codebase creation as a <b>graph problem</b>: it compiles English requirements into a visual "
   "Directed Acyclic Graph, topologically sorts it, then generates type-safe code node-by-node so multi-file systems actually compile.",
 "kpis":[{"v":"80%","l":"MVP time cut"},{"v":"<30ms","l":"LLM TTFT"},
         {"v":"99.9%","l":"Gen success"},{"v":"8K→3K","l":"Tokens/node"}],
 "problem":"Standard LLMs emit code sequentially, so multi-file full-stack generation suffers context truncation, dropped "
   "parameters, and broken interfaces between API, DB, and UI layers.",
 "users":"Developers and startup teams shipping rapid MVPs. Saves hours of boilerplate by guaranteeing generated code "
   "compiles immediately with zero-config, type-safe interfaces.",
 "goal":"Cut MVP time-to-market by <b>80%</b> with guaranteed type-safe connections between backend schemas and frontend "
   "components — eliminating the compile-error tax of AI codegen.",
 "role":"<b>Core Architect & Tech Lead.</b> Designed the in-memory DAG scheduler, the LLM fallback pipeline, and the "
   "sandboxed WebContainer preview.",
 "vision_lead":"Existing tools generate single-file snippets that drop structural context. CraftaStudio models the whole "
   "codebase as a DAG <b>before</b> generating a line — dependencies are explicit, so types flow from parents to children.",
 "alternatives":[["Copilot / Cursor","Autocompletes single files; no global structural coordination.","Orchestrates full multi-file builds."],
   ["v0 / Bolt.new","Frontend mockups; DB layers are mocked.","Full-stack sync with a live data model."],
   ["Raw GPT prompt","One giant prompt → truncation & hallucinated interfaces.","Bounded per-node prompts (<3K tokens)."]],
 "features_cards":[{"ic":"🕸️","h":"Graph Editor","p":"Real-time ReactFlow node canvas."},
   {"ic":"🧬","h":"Context Scaffolder","p":"Injects parent types into child prompts."},
   {"ic":"📦","h":"Sandbox Preview","p":"Runs code in browser WebContainers."}],
 "biz_lead":"The expensive failure isn't a wrong line of code — it's a generated system that <b>won't compile</b>, forcing "
   "developers back into manual integration. That erases the entire value of AI codegen.",
 "pain_cards":[{"ic":"⏱️","h":"Integration Tax","p":"<b>Hours lost</b> wiring AI-generated files that don't share interfaces."},
   {"ic":"🔌","h":"Broken Contracts","p":"Frontend calls an API shape the backend never generated."},
   {"ic":"🔁","h":"Re-prompt Spiral","p":"Each fix re-prompts the whole file, burning tokens & context."},
   {"ic":"🧱","h":"No Structure","p":"Snippet tools have no model of the system as a whole."}],
 "why_now":"Sub-30ms inference (Groq) finally makes per-node generation interactive — the DAG approach was impractical when each call cost seconds.",
 "impact_bars":[{"l":"Manual wiring","pct":85,"v":"4–6h","c":""},{"l":"Token waste","pct":70,"v":"high","c":"b"},
   {"l":"Compile errors","pct":60,"v":"freq","c":"g"}],
 "journey_lead":"From a blank canvas to a compiling, previewable full-stack app in one session — no context lost between steps.",
 "journey":[{"n":"1","h":"Describe","p":"User drops nodes (DB model, API, UI) and connects them on the ReactFlow canvas."},
   {"n":"2","h":"Validate","p":"Tarjan's SCC checks for cycles the moment an edge is drawn; invalid links are rejected inline."},
   {"n":"3","h":"Build","p":"One click topo-sorts the graph and streams generation node-by-node, parents first."},
   {"n":"4","h":"Preview","p":"Generated code mounts in a WebContainer — the app runs live in the browser, zero install."},
   {"n":"5","h":"Iterate","p":"Edit one node; only its subtree regenerates, preserving the rest."}],
 "fr_must":["Visual DAG editor with typed node connections","Cycle detection before persistence (Tarjan SCC)",
   "Topological build scheduler (Kahn's algorithm)","Per-node context-isolated code generation","In-browser sandbox preview"],
 "fr_should":["Multi-provider LLM fallback","Prompt/template caching","Incremental subtree regeneration","Export to GitHub repo"],
 "fr_table":[["FR-1","DAG editor","Edge create/delete reflected in <100ms"],
   ["FR-2","Cycle guard","A→B→A link rejected with toast"],
   ["FR-3","Build order","Parents always generated before children"],
   ["FR-4","Sandbox","Generated app boots in WebContainer"]],
 "nfr_table":[["Latency","TTFT < 30ms; node gen < 2s","Groq streaming + 3K-token prompts"],
   ["Availability","99.9% gen success","Multi-provider fallback + retries"],
   ["Scalability","10K concurrent canvases","ECS worker fleet + Redis WS adapter"],
   ["Consistency","No partial graphs persisted","Transactional graph writes"],
   ["Security","Zero host code execution","Browser-only WebContainer sandbox"]],
 "nfr_bars":[{"l":"Low latency","pct":95,"v":"P0","c":""},{"l":"Correctness","pct":92,"v":"P0","c":"b"},
   {"l":"Scalability","pct":78,"v":"P1","c":"g"},{"l":"Cost","pct":70,"v":"P1","c":""}],
 "stack_lead":"Polyglot by design: JS where the event loop and ecosystem help (canvas, realtime), Python where graph + agent "
   "tooling lives, SQL where structural integrity is non-negotiable.",
 "stack_table":[["Frontend","Next.js · ReactFlow","SSR speed + native graph canvas.","Heavy JS bundle; state-sync overhead."],
   ["Gateway","Node.js · Express","Non-blocking I/O ideal for WS sync.","Single-threaded; CPU work blocks loop."],
   ["Agent","FastAPI · Python","Rich graph + agentic tooling.","Slower cold starts."],
   ["Database","PostgreSQL · Prisma","FK integrity prevents broken edges.","Vertical-scale ceiling."],
   ["LLM","Groq Llama-3","<30ms TTFT for fluid canvas.","8K context → aggressive pruning."]],
 "scale_table":[["100","Canvas state-sync lag","In-memory WS on a single node"],
   ["1K","PG pool exhaustion","PgBouncer connection pooling"],
   ["10K","LLM TPM/RPM limits","Multi-provider fallback (Groq→Bedrock)"],
   ["100K","WS can't span instances","Redis Socket.io adapter + ECS fleet"],
   ["1M","Queue backlog & read load","Sharded queues + PG read replicas + CDN"]],
 "sec_lead":"The threat surface is a system that <b>executes model-generated code</b>. The core control is simple: that code "
   "never touches our infrastructure — it runs only in the user's browser sandbox.",
 "threats":[["Tampering","Prompt forces dangerous shell commands","Code runs only in browser WebContainer — never on host"],
   ["Info Disclosure","Secrets leak via generated output","Env vars AES-256 encrypted, injected via Vault at runtime"],
   ["Elevation","Cross-tenant project access","Prisma global tenant filter + Clerk JWT"],
   ["DoS","Abusive build spamming LLM","Per-user rate limits + queue depth caps"]],
 "sec_callout":["Never execute model output server-side","All generated code is sandboxed in-browser; the host never runs untrusted code, eliminating RCE as a class of bug."],
 "golden":[{"ic":"⏱️","h":"Latency","p":"TTFT + node gen time (OTel spans)."},
   {"ic":"🚦","h":"Traffic","p":"Builds/min, WS connections."},
   {"ic":"❌","h":"Errors","p":"Gen failures, DLQ depth."},
   {"ic":"📊","h":"Saturation","p":"Queue backlog, PG pool usage."}],
 "alerts":[["DLQ depth > 0","any failed job","Page on-call; inspect prompt/repair logs"],
   ["Queue backlog > 100","sustained 5m","Scale agent workers on ECS"],
   ["PG pool > 90%","sustained 2m","Raise PgBouncer pool / add replica"],
   ["TTFT p99 > 200ms","sustained","Flip primary LLM provider"]],
 "cost_lead":"LLM cost scales with usage, not seats — so the whole strategy is to <b>not call the model</b> when we don't have to, "
   "and to call the cheapest model that's good enough when we do.",
 "cost_kpis":[{"v":"−70%","l":"LLM spend","c":"g"},{"v":"8B/70B","l":"Model routing","c":"b"},{"v":"Cache","l":"Skip unchanged nodes"}],
 "cost_moves":["Prompt caching on static system templates","Route layout/analysis to Llama-3 8B, only code to 70B",
   "Redis cache of compiled nodes — skip LLM if inputs unchanged","Aggressive context pruning to cut tokens/call"],
 "incident":["<b>The Circular-Loop Hang.</b> A user wired Node A→B and B→A. The scheduler spun in an infinite loop, leaking memory and crashing Node.js gateways.",
   "Kahn's algorithm assumed a strict DAG. With a cycle, no node ever reached in-degree 0, so the while-loop never terminated.",
   "Added a pre-save <b>Tarjan SCC</b> check that rejects cycle-creating edges, plus a hard iteration cap as a backstop.",
   "<b>Never trust client validation.</b> The canvas blocked loops in the UI, but the API must independently enforce graph integrity."],
 "incident_blast":"All gateway instances shared the bug; one malformed graph could OOM the fleet. Now a single poisoned input is rejected at the edge.",
 "tradeoffs":[["Codegen unit","Per-node generation","Single-shot speed — many small calls vs one big one"],
   ["Graph storage","Relational rows","JSON simplicity — but FK integrity is worth it"],
   ["Sandbox","Browser WebContainer","Native perf — but zero server RCE risk"],
   ["Realtime","WebSockets","Stateless simplicity — needs Redis adapter to scale"]],
 "tradeoff_bars":[{"l":"Correctness","pct":95,"v":"max","c":"b"},{"l":"Latency","pct":85,"v":"high","c":""},
   {"l":"Simplicity","pct":55,"v":"traded","c":"g"}],
 "roadmap_lead":"The architecture is built to absorb two upgrades without a rewrite: collaborative editing and a self-healing compile loop.",
 "roadmap":[{"n":"V2","h":"Real-time Collaboration","p":"Yjs (CRDT) for Google-Docs-style multi-user canvas editing with conflict-free merge."},
   {"n":"V3","h":"Self-Correction Sandbox","p":"Compiler catches TS/syntax errors and feeds them back into the LLM prompt for automatic repair."},
   {"n":"V4","h":"Template Marketplace","p":"Shareable graph templates; cache hot subgraphs across users to drop LLM spend further."}],
 "qa":[{"q":"How do you handle LLM context limits across a multi-file system?",
   "a":"<b>DAG decomposition.</b> Instead of one mega-prompt, we generate node-by-node. Each child prompt receives only its parents' "
     "TypeScript interface signatures as static context, keeping active tokens under 3K and eliminating truncation.",
   "tags":["DAG","Context pruning","Type injection"]},
  {"q":"Why WebSockets over polling for generation updates?",
   "a":"Generation is push-shaped: the agent finishes a node at an unpredictable time. WS lets the server emit instantly, avoiding "
     "wasted DB read cycles from client polling. The cost is statefulness — solved with a Redis adapter when we scaled past one instance.",
   "tags":["WebSockets","Redis adapter","Push vs poll"]},
  {"q":"Explain Kahn's algorithm and where it runs here.",
   "a":"Topological sort by in-degree. Count each node's dependencies; nodes with 0 go first; as they complete, decrement children "
     "and enqueue any that hit 0. It produces the safe generation order so a referenced type always exists before its consumer.",
   "tags":["Topological sort","In-degree","Scheduler"]},
  {"q":"What was the hardest scaling bug?",
   "a":"WebSockets don't scale horizontally for free. A second container meant clients on different nodes couldn't receive each "
     "other's events. Fixed with the Socket.io Redis adapter so broadcasts fan out across the whole fleet.",
   "tags":["Horizontal scale","Pub/Sub","Sticky state"]}],
 "rev_lead":"The 60-second mental model: <b>codebase = DAG</b>; sort it, generate per-node with parent types injected, sandbox the preview.",
 "revision":[{"h":"Architecture","p":"ReactFlow canvas → Node gateway → Redis queue → FastAPI agent → Llama-3 → Postgres. Async return via WS.","acc":True},
   {"h":"Core Algorithm","p":"Kahn topo-sort for build order; Tarjan SCC to reject cycles before persistence."},
   {"h":"Database","p":"Project 1—N Nodes & Edges. Edges are relational rows; (project_id,status) composite index drives the scheduler."},
   {"h":"Scaling","p":"PgBouncer → multi-provider LLM → Redis WS adapter → sharded queues + replicas.","acc":True},
   {"h":"Security","p":"Browser-only WebContainer (no server RCE), Vault-injected secrets, Prisma tenant filter."},
   {"h":"Signature Bug","p":"Circular-dependency OOM → fixed with pre-save Tarjan check + iteration cap."}],
 "pitch":"CraftaStudio turns 'generate my app' into a graph-scheduling problem: model dependencies as a DAG, topologically sort it, "
   "and generate each node with its parents' types injected — so multi-file output actually compiles. It's async end-to-end, "
   "sandboxes previews in the browser, and falls back across LLM providers for 99.9% generation success.",
},
})

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  2 · PLACEPRO                                                              ║
# ╚══════════════════════════════════════════════════════════════════════════╝
PROJECTS.append({
"name":"PlacePro","pnum":"02","tagline":"Placement Portal",
"subtitle":"Campus placement management with a real-time event bus and database-enforced row-level security.",
"band_meta":[("EdTech","Domain"),("Redis Pub/Sub","Core"),("10K","Concurrent"),("Tier 1","Priority")],
"diagrams":{
 "arch":{"id":"pp-arch","title":"PlacePro — System Architecture","kind":"C4 / Container","legend":LEGEND,
  "code":CD+"""
flowchart TB
  U([Students / Recruiters]):::client
  subgraph EDGE["Edge"]
    FE["Next.js App"]:::client
    LB["Nginx LB<br/>round-robin"]:::svc
  end
  subgraph APP["Stateless App Tier"]
    A1["FastAPI #1"]:::svc
    A2["FastAPI #2"]:::svc
    SSE["SSE Gateway"]:::svc
  end
  subgraph STATE["State"]
    PG[("Supabase PG<br/>Row-Level Security")]:::data
    RD[["Redis Pub/Sub"]]:::queue
  end
  U-->FE-->LB-->A1 & A2
  A1 & A2 --> PG
  A1 & A2 -->|publish| RD
  RD -->|fan-out| SSE -->|push| FE
""",
  "eraser":"""Students [icon: users]
Frontend [icon: nextjs, color: orange]
LB [icon: nginx, color: blue]
FastAPI [icon: python, color: blue]
SSE [icon: broadcast, color: blue]
Postgres [icon: postgresql, color: green]
Redis [icon: redis, color: amber]
Students > Frontend > LB > FastAPI
FastAPI > Postgres
FastAPI > Redis: publish
Redis > SSE > Frontend: push""",
  "components":[("Nginx LB","Round-robins across stateless FastAPI workers."),
    ("FastAPI tier","Async business logic; horizontally scalable, no local state."),
    ("RLS Postgres","Tenant isolation enforced in the query planner, not app code."),
    ("Redis Pub/Sub","Sub-ms event broadcast; SSE pushes live status to clients.")],
  "layout":"Top-down with three bands. Users enter through the orange <b>edge</b> (frontend + Nginx). The <b>app tier</b> "
    "shows two identical FastAPI boxes to signal statelessness/horizontal scale. The <b>state</b> band pairs green Postgres "
    "with the amber Redis bus. The signature loop is the <b>publish → fan-out → push</b> path on the right, proving updates "
    "are event-driven, not polled."},
 "flow":{"id":"pp-flow","title":"Apply to Job — Request Lifecycle","kind":"Sequence","legend":None,
  "code":"""
sequenceDiagram
  autonumber
  participant S as Student
  participant A as FastAPI
  participant D as Postgres (RLS)
  participant R as Redis
  participant C as Coordinator UI
  S->>A: POST /apply (jobId)
  A->>D: check eligibility (CGPA/backlog)
  D-->>A: eligible ✓
  A->>D: INSERT application (RLS scoped)
  D-->>A: committed
  A->>R: PUBLISH application.created
  R-->>C: SSE broadcast
  A-->>S: 201 Created
""",
  "eraser":"""Student > FastAPI: POST /apply
FastAPI > Postgres: eligibility check
Postgres > FastAPI: eligible
FastAPI > Postgres: INSERT (RLS)
FastAPI > Redis: PUBLISH event
Redis > Coordinator: SSE
FastAPI > Student: 201""",
  "components":[("Eligibility gate","CGPA/backlog rules checked before any write."),
    ("RLS insert","Row stamped with tenant; cross-student writes impossible."),
    ("Publish","Decouples the write from notifying coordinators."),
    ("SSE","One-way server push — lighter than WS for status feeds.")],
  "layout":"Five-actor sequence. The <b>eligibility check</b> round-trip sits up top as a gate before the write. The "
    "<b>PUBLISH → SSE</b> pair branches sideways to the Coordinator lifeline, visually separating the user's response path "
    "(201 back to Student) from the broadcast path — two independent outcomes from one request."},
 "erd":{"id":"pp-erd","title":"PlacePro — Data Model","kind":"ERD","legend":None,
  "code":"""
erDiagram
  STUDENT ||--o{ APPLICATION : submits
  COMPANY ||--o{ JOB : posts
  JOB ||--o{ APPLICATION : receives
  STUDENT {
    uuid id PK
    string email UK
    float cgpa
    int backlogs
  }
  COMPANY {
    uuid id PK
    string name
    string tier
  }
  JOB {
    uuid id PK
    uuid company_id FK
    float min_cgpa
    int max_backlogs
  }
  APPLICATION {
    uuid id PK
    uuid student_id FK
    uuid job_id FK
    enum status
    timestamp applied_at
  }
""",
  "eraser":"""STUDENT { id pk; email uk; cgpa; backlogs }
COMPANY { id pk; name; tier }
JOB { id pk; company_id fk; min_cgpa; max_backlogs }
APPLICATION { id pk; student_id fk; job_id fk; status }
STUDENT 1-* APPLICATION
COMPANY 1-* JOB
JOB 1-* APPLICATION""",
  "components":[("Eligibility cols","min_cgpa/max_backlogs on JOB drive the gate."),
    ("Junction","APPLICATION is the M:N bridge between STUDENT and JOB."),
    ("Status enum","applied → shortlisted → offered, indexed for dashboards."),
    ("Unique email","Prevents duplicate student identities.")],
  "layout":"Four entities in a diamond: <b>STUDENT</b> and <b>COMPANY</b> on the outer flanks, both fanning into the central "
    "<b>APPLICATION</b> junction (via JOB). The crow's-feet make the many-to-many between students and jobs obvious. "
    "Eligibility columns are highlighted on JOB to show where the business rule lives in the schema."},
 "auth":{"id":"pp-auth","title":"RBAC + Row-Level Security","kind":"Sequence","legend":None,
  "code":"""
sequenceDiagram
  autonumber
  participant C as Client
  participant A as FastAPI
  participant J as Supabase Auth
  participant D as Postgres (RLS)
  C->>J: login (email/pw)
  J-->>C: JWT (role claim)
  C->>A: request + JWT
  A->>A: decode role (student/admin)
  A->>D: query AS role (RLS policy)
  D->>D: policy: USING (auth.uid()=student_id)
  D-->>A: only permitted rows
  A-->>C: 200
""",
  "eraser":"""Client > Supabase Auth: login
Auth > Client: JWT role
Client > FastAPI: JWT
FastAPI > Postgres: query as role
Postgres: RLS policy filter
Postgres > FastAPI: scoped rows
FastAPI > Client: 200""",
  "components":[("Supabase Auth","Issues JWT carrying the role claim."),
    ("Role decode","App routes by role; coordinators see all, students see self."),
    ("RLS policy","USING(auth.uid()=student_id) enforced by the DB engine."),
    ("Two-layer","App authz + DB RLS — a bug in one is caught by the other.")],
  "layout":"Four lifelines. The lower half is dominated by the <b>RLS policy</b> self-message on the Postgres lifeline — "
    "the diagram's thesis that authorization lives <i>in the database</i>. A note could read 'auth.uid() = student_id'. "
    "The role-decode self-message on FastAPI marks the app-layer check that complements it."},
 "deploy":{"id":"pp-deploy","title":"Cloud Deployment Topology","kind":"Deployment","legend":LEGEND,
  "code":CD+"""
flowchart TB
  U([Users]):::client
  subgraph CF["Cloudflare"]
    CDN["CDN + WAF"]:::client
  end
  subgraph ECS["AWS ECS (Docker)"]
    LB["Nginx ALB"]:::svc
    F1["FastAPI task xN"]:::svc
  end
  subgraph MGD["Managed Services"]
    PG[("Supabase PG")]:::data
    RD[["Upstash Redis"]]:::queue
    OBJ[("S3 — resumes")]:::data
  end
  U-->CDN-->LB-->F1
  F1-->PG & RD & OBJ
""",
  "eraser":"""Users > CDN+WAF > Nginx ALB > FastAPI tasks
FastAPI > Postgres + Redis + S3
// zones: Cloudflare | AWS ECS | Managed""",
  "components":[("Cloudflare","CDN + WAF absorbs spikes and filters attacks at the edge."),
    ("ECS autoscale","FastAPI tasks scale on CPU/queue during placement drives."),
    ("Managed state","Supabase + Upstash + S3 — fully managed, no ops toil."),
    ("S3 resumes","Large binary artifacts off the relational DB.")],
  "layout":"Three stacked cloud zones. The reviewer's eye should land on the <b>xN</b> on FastAPI tasks (burst scale for "
    "registration windows) and the WAF at the edge (the portal's history of being DDoSed during drives). All durable "
    "state is in the managed band — ECS tasks are cattle, not pets."},
 "scale":{"id":"pp-scale","title":"Scaling Evolution — 100 → 1M","kind":"Evolution","legend":None,
  "code":CD+"""
flowchart LR
  subgraph S1["100"]
    A1["Single FastAPI"]:::svc
  end
  subgraph S2["1K"]
    A2["Nginx + N workers"]:::svc
  end
  subgraph S3["10K"]
    A3["Redis Pub/Sub bus<br/>SSE fan-out"]:::queue
  end
  subgraph S4["100K"]
    A4["Read replicas<br/>conn pooling"]:::data
  end
  subgraph S5["1M"]
    A5["Sharded by college<br/>multi-region"]:::data
  end
  S1-->S2-->S3-->S4-->S5
""",
  "eraser":"""100: single FastAPI
1K: Nginx + worker pool
10K: Redis Pub/Sub + SSE
100K: read replicas + pooling
1M: shard by college + multi-region""",
  "components":[("100","One worker handles all traffic."),
    ("1K","Nginx round-robin across a worker pool."),
    ("10K","Event bus + SSE so status pushes don't hammer the DB."),
    ("100K","Read replicas for dashboard-heavy reads; PgBouncer pooling."),
    ("1M","Shard tenants by college; replicate across regions.")],
  "layout":"Left-to-right staircase. Each step adds exactly one architectural idea (pool → bus → replicas → shard). The "
    "colour migrates blue→amber→green to show the bottleneck moving from compute to messaging to data as scale grows."},
 "failure":{"id":"pp-fail","title":"Failure & Recovery Topology","kind":"Resilience","legend":LEGEND_FAIL,
  "code":CD+"""
flowchart TB
  W["FastAPI write"]:::svc
  PG[("Primary PG")]:::data
  RP[("Replica")]:::data
  RD[["Redis bus"]]:::queue
  OUT[["Outbox table"]]:::queue
  DEG["Degraded: read-only"]:::bad
  W-->PG
  PG-.->|streaming repl| RP
  PG-->|fail| FO{Failover}
  FO-->|promote| RP-->RECOV["Resume writes"]:::data
  W-->|publish fails| OUT
  OUT-->|relay on recover| RD
  RD-->|down| DEG
""",
  "eraser":"""Write > Primary PG
Primary > Replica: streaming repl
Primary fail > Failover > promote Replica > resume
Write > Outbox (if publish fails)
Outbox > Redis on recover
Redis down > degraded read-only""",
  "components":[("Streaming repl","Replica stays warm; promotion on primary loss."),
    ("Outbox pattern","If Redis publish fails, event is persisted and relayed later — no lost notifications."),
    ("Graceful degrade","Redis down → reads still served, writes queue."),
    ("Failover","Promote replica; brief write pause, no data loss.")],
  "layout":"Two failure stories side by side. Left: <b>DB failover</b> — primary (green) streams to replica; on failure a "
    "diamond promotes the replica. Right: <b>event-bus failure</b> — the Outbox (amber) captures events when Redis is down "
    "and relays on recovery. Red nodes mark degraded states; the eye reads green→red→green as 'recover'."},
},
"fields":{
 "summary_lead":"PlacePro is a campus placement portal engineered for the brutal traffic shape of placement season: <b>10K students "
   "hammering registration in a 5-minute window</b>. It survives with a stateless app tier, an event bus, and DB-enforced security.",
 "kpis":[{"v":"10K","l":"Concurrent"},{"v":"<1ms","l":"Pub/Sub"},{"v":"0","l":"Lost apps"},{"v":"RLS","l":"DB-level authz"}],
 "problem":"Placement portals crash under the concurrent load of short registration windows, and weak API routing lets students "
   "tamper with other candidates' application records.",
 "users":"University coordinators and students. Streamlines applications, eligibility screening, and recruiter updates in real time.",
 "goal":"Support <b>10,000 concurrent registrations</b> with zero dropped applications and strict, compliance-grade data isolation.",
 "role":"<b>System Architect & Backend Engineer.</b> Implemented PostgreSQL Row-Level Security policies and the Redis Pub/Sub real-time engine.",
 "vision_lead":"Legacy portals are CRUD apps that buckle under burst load and trust the application layer for security. PlacePro is "
   "<b>event-driven and database-secured</b> — load is absorbed by stateless workers, and authorization is non-bypassable.",
 "alternatives":[["Google Sheets","Concurrent-edit conflicts; zero access control.","RLS + atomic transactions."],
   ["Legacy ERP","Slow UI; manual eligibility review.","Automated instant eligibility engine."],
   ["WS everywhere","Stateful, heavy for one-way status.","SSE for lightweight server push."]],
 "features_cards":[{"ic":"✅","h":"Auto-Eligibility","p":"Blocks apps failing CGPA/backlog caps."},
   {"ic":"📡","h":"Live Status","p":"SSE updates on recruitment progress."},
   {"ic":"🔐","h":"Role Isolation","p":"Students, recruiters, admins fully partitioned."}],
 "biz_lead":"A placement portal that drops applications during the registration rush isn't a bug — it's a <b>career-altering "
   "failure</b> for a student who missed a one-shot window. Reliability under burst is the entire product.",
 "pain_cards":[{"ic":"💥","h":"Burst Collapse","p":"<b>5-minute</b> windows where 10K students arrive at once."},
   {"ic":"🕵️","h":"Tamper Risk","p":"Weak routing lets students edit others' records."},
   {"ic":"📉","h":"Stale Status","p":"Students refresh endlessly for shortlist updates."},
   {"ic":"🧾","h":"Manual Review","p":"Coordinators hand-check eligibility for hundreds."}],
 "why_now":"Managed Postgres with native RLS (Supabase) makes database-enforced multi-tenancy practical without a custom auth layer.",
 "impact_bars":[{"l":"Peak burst","pct":95,"v":"10K","c":""},{"l":"Tamper surface","pct":80,"v":"high","c":"b"},
   {"l":"Manual hours","pct":65,"v":"100s","c":"g"}],
 "journey_lead":"A student goes from profile to confirmed application — with live status — without ever seeing a spinner or a 500.",
 "journey":[{"n":"1","h":"Onboard","p":"Student verifies email, fills CGPA/backlog profile once."},
   {"n":"2","h":"Browse","p":"Only eligible job postings are shown; ineligible ones are greyed with the reason."},
   {"n":"3","h":"Apply","p":"One click; eligibility re-checked server-side, application committed under RLS."},
   {"n":"4","h":"Track","p":"SSE pushes shortlist/interview/offer status live — no refresh needed."},
   {"n":"5","h":"Coordinate","p":"Admins watch a real-time dashboard of applications as they land."}],
 "fr_must":["Eligibility-gated applications (CGPA/backlog)","Row-level data isolation per student",
   "Real-time status broadcast (SSE)","Role-based dashboards (student/recruiter/admin)","Burst-tolerant write path"],
 "fr_should":["Resume upload to object storage","Bulk shortlist by recruiters","Email digests","Audit log of status changes"],
 "fr_table":[["FR-1","Eligibility gate","Ineligible apply blocked server-side"],
   ["FR-2","Isolation","Student cannot read others' rows"],
   ["FR-3","Live status","Status change pushed < 1s"],
   ["FR-4","Burst","10K applies in 5 min, 0 dropped"]],
 "nfr_table":[["Availability","99.95% during drives","Stateless workers + autoscale + WAF"],
   ["Throughput","10K writes / 5 min","Async FastAPI + connection pooling"],
   ["Latency","Status push < 1s","Redis Pub/Sub + SSE"],
   ["Security","Non-bypassable isolation","Postgres RLS policies"],
   ["Durability","Zero lost applications","Transactional writes + outbox for events"]],
 "nfr_bars":[{"l":"Availability","pct":95,"v":"P0","c":""},{"l":"Security","pct":93,"v":"P0","c":"b"},
   {"l":"Throughput","pct":88,"v":"P0","c":"g"},{"l":"Latency","pct":75,"v":"P1","c":""}],
 "stack_lead":"Chosen for burst tolerance and security guarantees: async Python for I/O-bound load, managed Postgres for RLS, "
   "Redis for the cheapest possible fan-out.",
 "stack_table":[["Frontend","Next.js · Tailwind","SSR validation + fast dashboards.","Client bundle weight."],
   ["Backend","FastAPI","Async throughput + auto OpenAPI docs.","Fewer middleware libs than Express."],
   ["Database","PostgreSQL (Supabase)","Relational integrity + native RLS.","Connection ceiling under burst."],
   ["Bus","Redis Pub/Sub","Sub-ms broadcast for live status.","In-memory; needs outbox for durability."],
   ["Infra","Docker · AWS ECS","Containerized autoscale for drives.","Task-def config overhead."]],
 "scale_table":[["100","Single worker CPU","One FastAPI process"],
   ["1K","Request concurrency","Nginx round-robin + worker pool"],
   ["10K","DB write hot-spot","Pub/Sub + SSE offloads status reads"],
   ["100K","Dashboard read load","Read replicas + PgBouncer"],
   ["1M","Single-DB ceiling","Shard by college + multi-region"]],
 "sec_lead":"The crown-jewel control is <b>Row-Level Security</b>: even if an attacker reaches the database with a valid session, "
   "the query planner physically cannot return another student's rows.",
 "threats":[["Elevation","Student edits another's application","Postgres RLS USING(auth.uid()=student_id)"],
   ["Spoofing","Forged role to access admin views","Signed Supabase JWT with verified role claim"],
   ["DoS","Registration-window flood","Cloudflare WAF + rate limit + autoscale"],
   ["Repudiation","Disputed status changes","Append-only audit log"]],
 "sec_callout":["Authorization belongs in the database","App-layer checks can be bypassed by any routing bug; RLS makes cross-tenant reads impossible at the engine level."],
 "golden":[{"ic":"⏱️","h":"Latency","p":"Apply p99, SSE delivery time."},
   {"ic":"🚦","h":"Traffic","p":"Applies/min, active SSE conns."},
   {"ic":"❌","h":"Errors","p":"5xx rate, failed publishes."},
   {"ic":"📊","h":"Saturation","p":"PG connections, worker CPU."}],
 "alerts":[["5xx > 1%","sustained 1m","Scale ECS tasks; check PG pool"],
   ["PG conns > 90%","2m","Add replica / raise PgBouncer"],
   ["Publish failures > 0","any","Verify outbox relay draining"],
   ["SSE delivery > 2s","sustained","Inspect Redis latency"]],
 "cost_lead":"Drives are spiky: massive load for hours, near-idle the rest of the term. The whole cost play is <b>scale-to-zero "
   "between drives</b> and never paying for idle capacity.",
 "cost_kpis":[{"v":"−60%","l":"Idle spend","c":"g"},{"v":"Autoscale","l":"0→N on demand","c":"b"},{"v":"Managed","l":"No DB ops cost"}],
 "cost_moves":["ECS scale-to-near-zero between drives","Serverless Redis (pay-per-request) via Upstash",
   "Resumes in S3 (cheap) not in the DB","Read replicas only spun up for active drives"],
 "incident":["<b>The Registration Stampede.</b> A marquee company opened applications; 8K students hit POST /apply within 90 seconds and the DB connection pool exhausted, returning 500s.",
   "Each FastAPI worker opened its own DB connections with no pooling. Under burst, connections blew past Postgres's limit and new requests were refused.",
   "Introduced <b>PgBouncer</b> transaction pooling and moved status reads onto the Redis/SSE path so the DB only handled writes during the spike.",
   "<b>Connection management is a first-class scaling concern.</b> The bottleneck wasn't CPU — it was a finite resource (connections) nobody had pooled."],
 "incident_blast":"Every student hitting the portal during the window saw 500s for ~4 minutes — a one-shot application window nearly missed. Pooling cut peak connections 10x.",
 "tradeoffs":[["Real-time","SSE (one-way)","WS bidirectionality — but SSE is lighter for status feeds"],
   ["Security","DB-level RLS","App simplicity — but RLS is non-bypassable"],
   ["Bus","Redis Pub/Sub","Durability — added an outbox to compensate"],
   ["Scale","Stateless workers","Sticky sessions — kept all state in PG/Redis"]],
 "tradeoff_bars":[{"l":"Security","pct":95,"v":"max","c":"b"},{"l":"Availability","pct":90,"v":"high","c":""},
   {"l":"Durability","pct":80,"v":"outbox","c":"g"}],
 "roadmap_lead":"Next moves harden durability and widen the real-time surface without disturbing the stateless core.",
 "roadmap":[{"n":"V2","h":"Durable Event Log","p":"Swap raw Pub/Sub for Redis Streams / Kafka so notifications survive a bus restart natively."},
   {"n":"V3","h":"Recruiter Workflows","p":"Multi-stage pipelines (OA → interview → offer) with automated transitions and SLA timers."},
   {"n":"V4","h":"Analytics","p":"Placement funnel dashboards; per-company conversion and offer-acceptance analytics."}],
 "qa":[{"q":"How does Row-Level Security stop a student reading another's data?",
   "a":"RLS attaches a policy to the table — e.g. <code>USING (auth.uid() = student_id)</code>. The Postgres planner appends this "
     "predicate to <b>every</b> query automatically. Even a SQL-injection or a buggy endpoint can't return rows the policy forbids, "
     "because filtering happens in the engine, below the application.",
   "tags":["RLS","Defense in depth","Multi-tenancy"]},
  {"q":"Why SSE instead of WebSockets for live status?",
   "a":"Status updates are <b>one-directional</b> (server→client). SSE rides plain HTTP, auto-reconnects, and is far lighter to "
     "operate than full-duplex WS. We reserve WS for genuinely bidirectional features; for a status feed, SSE is the right tool.",
   "tags":["SSE","WebSockets","Push model"]},
  {"q":"How did you survive the registration stampede?",
   "a":"Three moves: <b>PgBouncer</b> transaction pooling so 10K requests share a small connection set; stateless FastAPI workers "
     "autoscaling on ECS; and offloading status reads to Redis/SSE so the database during the spike only handled the critical writes.",
   "tags":["Connection pooling","Autoscale","Read offload"]},
  {"q":"Redis Pub/Sub isn't durable — how do you avoid lost notifications?",
   "a":"An <b>outbox pattern</b>: the event is written in the same DB transaction as the application, and a relay publishes it to Redis. "
     "If Redis is down, the event waits in the outbox and is replayed on recovery — so a bus blip never loses a notification.",
   "tags":["Outbox","Durability","At-least-once"]}],
 "rev_lead":"Mental model: <b>stateless workers + event bus + DB-enforced security</b>. Burst-tolerant by construction.",
 "revision":[{"h":"Architecture","p":"Next.js → Nginx → stateless FastAPI → Postgres(RLS); Redis Pub/Sub → SSE for live status.","acc":True},
   {"h":"Security","p":"Postgres RLS policies make cross-tenant reads impossible at the engine level; signed JWT roles."},
   {"h":"Database","p":"STUDENT/COMPANY/JOB/APPLICATION; APPLICATION is the M:N junction; eligibility cols on JOB."},
   {"h":"Scaling","p":"Pool (PgBouncer) → bus (Redis) → replicas → shard-by-college. Compute is stateless cattle.","acc":True},
   {"h":"Durability","p":"Outbox pattern bridges non-durable Pub/Sub so notifications are never lost."},
   {"h":"Signature Bug","p":"Registration stampede exhausted the connection pool → fixed with PgBouncer + read offload."}],
 "pitch":"PlacePro is a placement portal built for the 5-minute stampede. Stateless FastAPI workers autoscale behind Nginx, "
   "Postgres Row-Level Security makes tenant isolation non-bypassable, and a Redis Pub/Sub bus with SSE pushes live status "
   "without hammering the DB. An outbox pattern guarantees no notification is ever lost.",
},
})

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  3 · MNEMO                                                                 ║
# ╚══════════════════════════════════════════════════════════════════════════╝
PROJECTS.append({
"name":"Mnemo","pnum":"03","tagline":"Memory Layer",
"subtitle":"AI long-term memory engine with Ebbinghaus spaced decay and pgvector hybrid search.",
"band_meta":[("AI Infra","Domain"),("pgvector","Core"),("−70%","Token cost"),("Tier 1","Priority")],
"diagrams":{
 "arch":{"id":"mn-arch","title":"Mnemo — System Architecture","kind":"C4 / Container","legend":LEGEND,
  "code":CD+"""
flowchart TB
  AG([AI Agent]):::client
  subgraph API["Memory API"]
    W["Write: /remember"]:::svc
    R["Read: /recall"]:::svc
    EMB["Embedder<br/>text-embedding-3"]:::svc
  end
  subgraph RANK["Retrieval"]
    HS["Hybrid Search<br/>vector + BM25"]:::svc
    DK["Decay Scorer<br/>Ebbinghaus"]:::svc
  end
  PG[("Postgres + pgvector<br/>memories + embeddings")]:::data
  AG -->|store| W --> EMB --> PG
  AG -->|query| R --> HS --> PG
  HS --> DK --> R
  R -->|top-k blocks| AG
""",
  "eraser":"""Agent [icon: robot]
Write [icon: save, color: blue]
Read [icon: search, color: blue]
Embedder [icon: vector, color: blue]
HybridSearch [icon: merge, color: blue]
DecayScorer [icon: clock, color: blue]
Postgres [icon: postgresql, color: green]
Agent > Write > Embedder > Postgres
Agent > Read > HybridSearch > Postgres
HybridSearch > DecayScorer > Read
Read > Agent: top-k""",
  "components":[("Embedder","Turns memory text into a vector on write."),
    ("Hybrid search","Combines pgvector ANN with BM25 keyword recall."),
    ("Decay scorer","Re-ranks by Ebbinghaus forgetting curve + recency."),
    ("pgvector","One Postgres stores rows, embeddings, and the ANN index.")],
  "layout":"Top-down. The agent (orange) has two arrows in: a <b>write</b> path (left) flowing through the embedder into "
    "Postgres, and a <b>read</b> path (right) flowing through hybrid search and the decay scorer back out. The two retrieval "
    "boxes are grouped to show recall = <b>relevance × freshness</b>. Single green datastore underscores 'no separate vector DB needed'."},
 "flow":{"id":"mn-flow","title":"Recall — Request Lifecycle","kind":"Sequence","legend":None,
  "code":"""
sequenceDiagram
  autonumber
  participant A as Agent
  participant R as /recall
  participant E as Embedder
  participant V as pgvector
  participant D as Decay Scorer
  A->>R: query("what did user say about pricing?")
  R->>E: embed(query)
  E-->>R: query vector
  R->>V: ANN search + BM25 (hybrid)
  V-->>R: candidate memories
  R->>D: score(decay, recency, relevance)
  D-->>R: re-ranked top-k
  R-->>A: top-k memory blocks (low token cost)
""",
  "eraser":"""Agent > recall: query
recall > Embedder: embed
Embedder > recall: vector
recall > pgvector: ANN + BM25
pgvector > recall: candidates
recall > Decay: score
Decay > recall: top-k
recall > Agent: memory blocks""",
  "components":[("Embed query","Same model as write — vectors live in one space."),
    ("Hybrid retrieve","ANN catches semantics; BM25 catches exact terms/IDs."),
    ("Decay re-rank","Old, unused memories sink; fresh, relevant ones rise."),
    ("Top-k only","Returns a handful of blocks, not the whole history.")],
  "layout":"Five-actor sequence with a clean left-to-right pipeline feel. The <b>hybrid search</b> message to pgvector is the "
    "widest hop; the <b>decay scoring</b> step is a distinct stage before return. The final dashed arrow back to the Agent is "
    "annotated 'low token cost' — the entire value proposition in one label."},
 "erd":{"id":"mn-erd","title":"Mnemo — Data Model","kind":"ERD","legend":None,
  "code":"""
erDiagram
  AGENT ||--o{ MEMORY : owns
  MEMORY ||--|| EMBEDDING : has
  MEMORY ||--o{ ACCESS_LOG : "recalled in"
  AGENT {
    uuid id PK
    string namespace UK
  }
  MEMORY {
    uuid id PK
    uuid agent_id FK
    text content
    float importance
    timestamp last_access
    int access_count
  }
  EMBEDDING {
    uuid memory_id PK
    vector embedding
  }
  ACCESS_LOG {
    uuid id PK
    uuid memory_id FK
    timestamp at
  }
""",
  "eraser":"""AGENT { id pk; namespace uk }
MEMORY { id pk; agent_id fk; content; importance; last_access; access_count }
EMBEDDING { memory_id pk; embedding vector }
ACCESS_LOG { id pk; memory_id fk; at }
AGENT 1-* MEMORY
MEMORY 1-1 EMBEDDING
MEMORY 1-* ACCESS_LOG""",
  "components":[("vector column","pgvector type with an IVFFlat/HNSW index for ANN."),
    ("Decay inputs","last_access + access_count + importance feed the forgetting curve."),
    ("1:1 embedding","Separated so the wide vector doesn't bloat row scans."),
    ("Access log","Each recall updates recency — reinforcing useful memories.")],
  "layout":"<b>AGENT</b> top, fanning to <b>MEMORY</b> (center). MEMORY links 1:1 down to <b>EMBEDDING</b> (the vector, set "
    "apart deliberately) and 1:N to <b>ACCESS_LOG</b>. The decay-driving columns on MEMORY (last_access, access_count, importance) "
    "are highlighted — the schema visibly encodes the Ebbinghaus inputs."},
 "auth":{"id":"mn-auth","title":"API-Key + Namespace Isolation","kind":"Sequence","legend":None,
  "code":"""
sequenceDiagram
  autonumber
  participant A as Agent App
  participant G as Memory API
  participant K as Key Store
  participant D as Postgres
  A->>G: request + API key
  G->>K: validate key -> namespace
  K-->>G: namespace = ns_42
  G->>D: query WHERE namespace = ns_42
  D-->>G: only this tenant's memories
  G-->>A: scoped result
  Note over G,D: namespace = hard tenant boundary
""",
  "eraser":"""Agent > API: API key
API > KeyStore: validate
KeyStore > API: namespace
API > Postgres: WHERE namespace=ns
Postgres > API: scoped memories
API > Agent: result""",
  "components":[("API key","Per-tenant secret, hashed at rest."),
    ("Namespace map","Key resolves to exactly one namespace."),
    ("Hard filter","Every query is namespace-scoped — no cross-tenant leakage."),
    ("Rate tie-in","Keys also carry per-tenant rate limits.")],
  "layout":"Four lifelines. The <b>validate key → namespace</b> hop is the trust gate; everything after it is scoped by "
    "namespace. A spanning note under API/Postgres states 'namespace = hard tenant boundary' — memories are sensitive, so "
    "isolation is the headline."},
 "deploy":{"id":"mn-deploy","title":"Cloud Deployment Topology","kind":"Deployment","legend":LEGEND,
  "code":CD+"""
flowchart TB
  A([Agent Apps]):::client
  subgraph FLY["Fly.io / Render"]
    API["Memory API xN"]:::svc
  end
  subgraph DATA["Managed Data"]
    PG[("Postgres + pgvector")]:::data
    RC[["Redis cache"]]:::queue
  end
  EMB{{"Embedding API<br/>OpenAI"}}:::ext
  A-->API
  API-->RC
  API-->PG
  API-->|embed| EMB
""",
  "eraser":"""Agents > Memory API xN
API > Redis cache
API > Postgres+pgvector
API > Embedding API
// zones: Fly.io | Managed Data""",
  "components":[("API replicas","Stateless; scale with request volume."),
    ("Redis cache","Caches hot query embeddings + frequent recalls."),
    ("pgvector","ANN index lives with the data — one system to operate."),
    ("Embedding API","External; cached aggressively to cut spend.")],
  "layout":"Compact two-zone deployment. Stateless <b>API xN</b> on the left platform; <b>managed data</b> (pgvector + Redis) "
    "center; the external <b>embedding API</b> floats right as a hexagon. The Redis cache between API and the embedding API "
    "signals the cost strategy — don't re-embed what you've seen."},
 "scale":{"id":"mn-scale","title":"Scaling Evolution — 100 → 1M","kind":"Evolution","legend":None,
  "code":CD+"""
flowchart LR
  subgraph S1["100"]
    A1["pgvector exact scan"]:::data
  end
  subgraph S2["1K"]
    A2["IVFFlat ANN index"]:::data
  end
  subgraph S3["10K"]
    A3["HNSW + embed cache"]:::queue
  end
  subgraph S4["100K"]
    A4["Read replicas<br/>per-namespace"]:::data
  end
  subgraph S5["1M"]
    A5["Sharded vector store<br/>by namespace"]:::data
  end
  S1-->S2-->S3-->S4-->S5
""",
  "eraser":"""100: exact vector scan
1K: IVFFlat ANN index
10K: HNSW + embedding cache
100K: read replicas per namespace
1M: shard vector store by namespace""",
  "components":[("100","Brute-force cosine scan is fine."),
    ("1K","IVFFlat index — approximate but fast."),
    ("10K","HNSW for recall@speed; cache embeddings."),
    ("100K","Replicas absorb recall-heavy read load."),
    ("1M","Shard the vector store by tenant namespace.")],
  "layout":"Staircase where every step is a <b>retrieval-index upgrade</b> (exact → IVFFlat → HNSW → replicas → shard). "
    "Mostly green (data-tier evolution) with one amber cache step, reinforcing that Mnemo's scaling story is fundamentally "
    "about vector indexing, not compute."},
 "failure":{"id":"mn-fail","title":"Failure & Recovery Topology","kind":"Resilience","legend":LEGEND_FAIL,
  "code":CD+"""
flowchart TB
  Q["recall request"]:::svc
  EMB{{Embedding API}}:::ext
  CACHE[["Embed cache"]]:::queue
  PG[("pgvector")]:::data
  KW["BM25 keyword fallback"]:::bad
  Q-->EMB
  EMB-->|down / 429| CACHE
  CACHE-->|miss| KW
  CACHE-->|hit| PG
  KW-->PG
  PG-->|index degraded| EXACT["exact scan fallback"]:::bad
  EXACT-->OK["return results"]:::data
  PG-->OK
""",
  "eraser":"""recall > Embedding API
Embedding down > cache
cache hit > pgvector
cache miss > BM25 fallback > pgvector
pgvector index degraded > exact scan
> return results""",
  "components":[("Embed-API outage","Cache serves vectors; if miss, fall back to BM25 keyword search."),
    ("Graceful recall","Keyword results beat no results — degrade, don't fail."),
    ("Index degrade","If ANN index is rebuilding, exact scan still answers (slower)."),
    ("Always answers","Every failure path still returns memories.")],
  "layout":"A failure decision tree where <b>every leaf returns results</b> — the resilience thesis is 'never return empty'. "
    "Embedding outage routes to cache then BM25 (red fallback) but still reaches green pgvector. Index degradation routes to "
    "exact scan. Red = degraded-but-working, never dead."},
},
"fields":{
 "summary_lead":"Mnemo gives stateless LLM agents a <b>persistent, searchable memory</b>. It stores conversation facts as vectors, "
   "ranks recall by an Ebbinghaus forgetting curve, and returns only the top-k relevant blocks — cutting prompt token cost ~70%.",
 "kpis":[{"v":"−70%","l":"Token cost"},{"v":"pgvector","l":"One datastore"},{"v":"Hybrid","l":"Vector+BM25"},{"v":"top-k","l":"Recall size"}],
 "problem":"AI agents have no native long-term memory: they suffer amnesia on reboot, and stuffing full history into the prompt "
   "causes context truncation and runaway token costs.",
 "users":"LLM agents and chat products needing contextual persistence. Mnemo cuts token spend by retrieving only relevant memory blocks.",
 "goal":"Decrease LLM context token cost by <b>70%</b> while <i>improving</i> retrieval relevance by ranking memories on a decay score.",
 "role":"<b>Core Developer & System Designer.</b> Designed the pgvector embedding schema, the Ebbinghaus decay engine, and the hybrid keyword/vector search.",
 "vision_lead":"Most memory layers do naive vector similarity and resurface stale junk. Mnemo treats memory like a human brain: "
   "<b>relevance decays over time</b> unless reinforced by access — so recall stays fresh, not just similar.",
 "alternatives":[["Full-context stuffing","Truncation + huge token bills.","Top-k retrieval, ~70% cheaper."],
   ["Pinecone / vector DB","Separate system to operate + sync.","pgvector — one Postgres for all of it."],
   ["Pure cosine recall","Resurfaces stale, irrelevant memories.","Decay-weighted re-ranking."]],
 "features_cards":[{"ic":"⏳","h":"Spaced Decay","p":"Ebbinghaus curve sinks unused memories."},
   {"ic":"🔎","h":"Hybrid Search","p":"Vector ANN + BM25 keyword in one query."},
   {"ic":"🧩","h":"Top-k Recall","p":"Returns a few blocks, not the whole log."}],
 "biz_lead":"Every token in the context window is paid for on <b>every</b> call. An agent that re-reads its whole history is "
   "burning money linearly with conversation length. Mnemo makes memory cost <i>sublinear</i>.",
 "pain_cards":[{"ic":"💸","h":"Token Burn","p":"Full-history prompts cost <b>more every turn</b>."},
   {"ic":"🧠","h":"Amnesia","p":"Stateless agents forget everything on reboot."},
   {"ic":"✂️","h":"Truncation","p":"Long histories get silently cut, losing key facts."},
   {"ic":"🗑️","h":"Stale Recall","p":"Naive similarity surfaces outdated memories."}],
 "why_now":"pgvector matured into a production ANN index, so semantic memory no longer needs a separate, costly vector database.",
 "impact_bars":[{"l":"Token cost","pct":85,"v":"−70%","c":""},{"l":"Recall relevance","pct":80,"v":"+","c":"b"},
   {"l":"Infra simplicity","pct":75,"v":"1 DB","c":"g"}],
 "journey_lead":"An agent stores facts as it learns them and recalls just what's relevant — staying coherent across sessions for pennies.",
 "journey":[{"n":"1","h":"Remember","p":"Agent calls /remember with a fact; Mnemo embeds and stores it with importance + timestamp."},
   {"n":"2","h":"Live","p":"Each memory accrues access_count and last_access as it gets used."},
   {"n":"3","h":"Recall","p":"Agent calls /recall with a query; hybrid search finds candidates."},
   {"n":"4","h":"Re-rank","p":"Decay scorer weights candidates by relevance × freshness × importance."},
   {"n":"5","h":"Inject","p":"Only the top-k blocks enter the prompt — cheap, sharp context."}],
 "fr_must":["/remember and /recall API","Embedding on write","Hybrid vector + BM25 retrieval",
   "Ebbinghaus decay re-ranking","Per-namespace tenant isolation"],
 "fr_should":["Importance tagging","Embedding cache","Memory consolidation/merge","TTL hard-expiry for sensitive data"],
 "fr_table":[["FR-1","Store","/remember embeds + persists < 200ms"],
   ["FR-2","Retrieve","Hybrid recall returns top-k"],
   ["FR-3","Decay","Unused memories rank lower over time"],
   ["FR-4","Isolation","Namespace scopes every query"]],
 "nfr_table":[["Latency","Recall p99 < 150ms","HNSW index + embed cache"],
   ["Cost","−70% vs full-context","Top-k retrieval, not full history"],
   ["Relevance","Recall@k beats cosine baseline","Decay-weighted hybrid ranking"],
   ["Scalability","1M memories / namespace","ANN index + sharding"],
   ["Isolation","No cross-tenant recall","Namespace hard filter"]],
 "nfr_bars":[{"l":"Cost efficiency","pct":92,"v":"P0","c":""},{"l":"Relevance","pct":90,"v":"P0","c":"b"},
   {"l":"Latency","pct":82,"v":"P1","c":"g"},{"l":"Scale","pct":75,"v":"P1","c":""}],
 "stack_lead":"Deliberately boring infra: one Postgres does relational + vector + keyword search, so there's a single system to "
   "back up, secure, and reason about.",
 "stack_table":[["API","FastAPI · Python","Async + rich ML/embedding ecosystem.","GIL limits CPU-bound work."],
   ["Store","Postgres + pgvector","Vectors, rows, BM25 in one DB.","ANN tuning required at scale."],
   ["Embeddings","OpenAI text-embedding-3","Strong semantic quality.","External dependency + cost."],
   ["Cache","Redis","Caches query embeddings + hot recalls.","Extra component to run."],
   ["Ranking","Custom decay scorer","Encodes the forgetting curve.","Needs tuning per domain."]],
 "scale_table":[["100","None — trivial","Exact cosine scan"],
   ["1K","Linear scan latency","IVFFlat ANN index"],
   ["10K","Recall speed","HNSW index + embed cache"],
   ["100K","Read load","Per-namespace read replicas"],
   ["1M","Single-index limits","Shard vector store by namespace"]],
 "sec_lead":"Memories often contain personal data, so isolation and expiry are security-critical: a namespace is a hard wall, and "
   "sensitive memories can carry a TTL.",
 "threats":[["Info Disclosure","Cross-tenant memory recall","Namespace filter on every query"],
   ["Tampering","Forged API key","Hashed keys + per-key namespace binding"],
   ["Retention","PII kept indefinitely","TTL hard-expiry + delete API"],
   ["DoS","Recall flooding","Per-key rate limits"]],
 "sec_callout":["Memory is sensitive by default","Namespaces are hard boundaries and sensitive memories get a TTL — recall can never cross tenants or outlive its retention window."],
 "golden":[{"ic":"⏱️","h":"Latency","p":"Recall p99, embed time."},
   {"ic":"🚦","h":"Traffic","p":"Recalls/min, writes/min."},
   {"ic":"❌","h":"Errors","p":"Embed-API failures, cache misses."},
   {"ic":"📊","h":"Saturation","p":"Index size, PG CPU."}],
 "alerts":[["Embed-API errors > 2%","1m","Serve from cache; switch provider"],
   ["Recall p99 > 300ms","5m","Rebuild/retune ANN index"],
   ["Cache hit < 60%","sustained","Grow cache; review key entropy"],
   ["Index bloat","weekly","Schedule VACUUM / reindex"]],
 "cost_lead":"Two cost centers: <b>embedding calls</b> and <b>prompt tokens</b>. Mnemo attacks both — cache embeddings so we "
   "don't pay twice, and return top-k so prompts stay small.",
 "cost_kpis":[{"v":"−70%","l":"Prompt tokens","c":"g"},{"v":"Cache","l":"No re-embedding","c":"b"},{"v":"1 DB","l":"No vector-DB bill"}],
 "cost_moves":["Cache query + content embeddings in Redis","Return top-k blocks, never full history",
   "pgvector instead of a paid vector DB","Batch embedding writes to amortize API calls"],
 "incident":["<b>The Stale-Memory Bug.</b> Agents kept resurfacing a months-old, contradicted fact ('user prefers email') over a "
   "newer one ('user prefers Slack'), because pure cosine similarity ranked the older memory higher.",
   "Ranking was similarity-only. It had no notion of <b>time or reinforcement</b>, so an old but semantically-close memory could "
   "permanently outrank a fresh, correct one.",
   "Added the <b>Ebbinghaus decay scorer</b>: final score = relevance × e^(−Δt/S) × importance, where S grows with access_count. "
   "Reinforced, recent memories win.",
   "<b>Relevance is not similarity.</b> Good recall blends semantic match with recency and how often a memory has proven useful."],
 "incident_blast":"Agents gave confidently outdated answers across all tenants until decay shipped. The fix changed ranking globally with no schema migration.",
 "tradeoffs":[["Store","pgvector (one DB)","Specialized-vector-DB speed at huge scale"],
   ["Recall","Hybrid + decay","Pure-vector simplicity — but worse relevance"],
   ["Context","Top-k blocks","Full recall — but 70% more tokens"],
   ["Embeddings","External API","Self-hosted control — but more ops"]],
 "tradeoff_bars":[{"l":"Cost","pct":92,"v":"max","c":"g"},{"l":"Relevance","pct":88,"v":"high","c":"b"},
   {"l":"Simplicity","pct":80,"v":"1 DB","c":""}],
 "roadmap_lead":"The roadmap deepens the cognitive model — memories that summarize, merge, and forget like a real memory system.",
 "roadmap":[{"n":"V2","h":"Memory Consolidation","p":"Periodically merge related memories into higher-level summaries to compress the store."},
   {"n":"V3","h":"Self-Hosted Embeddings","p":"Optional local embedding model to remove the external API dependency and cost."},
   {"n":"V4","h":"Graph Memory","p":"Link memories into an entity graph for multi-hop recall (who → relates-to → what)."}],
 "qa":[{"q":"Why store vectors in Postgres instead of a dedicated vector DB?",
   "a":"<b>Operational simplicity.</b> pgvector keeps embeddings, relational metadata, and keyword search in one system — one backup, "
     "one security model, one transaction. A separate vector DB adds a sync problem and a second thing to operate. We'd only split it "
     "out past ~1M vectors per namespace where specialized indexes win.",
   "tags":["pgvector","Operational cost","ANN"]},
  {"q":"How does the Ebbinghaus decay scoring work?",
   "a":"Final rank = relevance × e^(−Δt/S) × importance. Δt is time since last access; S (memory strength) grows with access_count. "
     "So a memory that's used often decays slowly and stays recallable, while an untouched one fades — mirroring the human forgetting curve.",
   "tags":["Decay","Forgetting curve","Re-ranking"]},
  {"q":"Why hybrid search instead of pure vector similarity?",
   "a":"Vectors capture <b>semantics</b> but miss exact tokens — IDs, names, error codes. BM25 keyword search nails those. Running both "
     "and fusing the scores gives recall that's both meaning-aware and precise on literals.",
   "tags":["Hybrid search","BM25","Vector ANN"]},
  {"q":"How do you keep recall cheap as history grows?",
   "a":"We never inject full history — only the <b>top-k</b> blocks after ranking. Memory cost is bounded by k, not conversation length, "
     "so token spend stays roughly flat even as the store grows to millions of memories.",
   "tags":["Top-k","Token budget","Sublinear cost"]}],
 "rev_lead":"Mental model: <b>memory = relevance × freshness</b>, stored in pgvector, returned top-k. Cheap, sharp context.",
 "revision":[{"h":"Architecture","p":"Agent → /remember (embed) → pgvector; /recall → hybrid search → decay scorer → top-k blocks.","acc":True},
   {"h":"Ranking","p":"Ebbinghaus: relevance × e^(−Δt/S) × importance; S grows with access_count."},
   {"h":"Database","p":"AGENT→MEMORY→EMBEDDING(1:1, vector col)→ACCESS_LOG; decay inputs on MEMORY."},
   {"h":"Scaling","p":"exact → IVFFlat → HNSW → replicas → shard-by-namespace. A vector-index story.","acc":True},
   {"h":"Cost","p":"Cache embeddings + return top-k → ~70% fewer prompt tokens; pgvector avoids a vector-DB bill."},
   {"h":"Signature Bug","p":"Stale memory outranked fresh → fixed with decay-weighted re-ranking."}],
 "pitch":"Mnemo is long-term memory for LLM agents. It embeds facts into pgvector, recalls them with hybrid vector+keyword search, "
   "then re-ranks by an Ebbinghaus forgetting curve so fresh, reinforced memories win. Agents inject only top-k blocks, cutting "
   "prompt token cost ~70% while staying coherent across sessions — all on a single Postgres.",
},
})


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  4 · ROVN                                                                  ║
# ╚══════════════════════════════════════════════════════════════════════════╝
PROJECTS.append({
"name":"ROVN","pnum":"04","tagline":"AI Lead Co-Pilot",
"subtitle":"AI-Powered Lead Ingestion workspace with Intent Scoring & Prioritization.",
"band_meta":[("SalesTech","Domain"),("Kafka + LLM","Core"),("40%","Conv. Lift"),("Tier 2","Priority")],
"diagrams":{
 "arch":{"id":"ro-arch","title":"ROVN — System Architecture","kind":"C4 / Container","legend":LEGEND,
  "code":CD+'''
flowchart TB
  subgraph INGEST["Ingestion Layer"]
    WH["Webhook Gateway"]:::svc
    EM["Email Parser"]:::svc
  end
  subgraph STREAM["Streaming & Processing"]
    KF[["Kafka Topics"]]:::queue
    SP["Spark/Flink Processor"]:::svc
    LLM{{"LLM Intent Scorer"}}:::ext
  end
  subgraph STATE["State & UI"]
    PG[("Postgres (Relational)")]:::data
    ES[("Elasticsearch (Search)")]:::data
    API["FastAPI Backend"]:::svc
    FE["React UI"]:::client
  end
  WH --> KF
  EM --> KF
  KF --> SP
  SP <-->|score intent| LLM
  SP --> PG & ES
  FE --> API
  API --> PG & ES
''',
  "eraser":'''Webhook [icon: webhook]
Email [icon: mail]
Kafka [icon: kafka, color: amber]
Processor [icon: cpu, color: blue]
LLM [icon: openai, color: purple]
Postgres [icon: postgresql, color: green]
Elasticsearch [icon: elastic, color: green]
API [icon: python, color: blue]
UI [icon: react, color: orange]
Webhook > Kafka
Email > Kafka
Kafka > Processor
Processor <> LLM: score intent
Processor > Postgres
Processor > Elasticsearch
API > Postgres
API > Elasticsearch
UI > API''',
  "components":[("Webhook/Email","High-throughput ingestion endpoints."),
    ("Kafka","Buffers bursts of incoming leads securely."),
    ("Processor","Asynchronously evaluates intent using LLM."),
    ("Elasticsearch","Powers fast text search on parsed leads.")],
  "layout":"Top-to-bottom data flow from ingestion to storage, with UI pulling from state."},
 "flow":{"id":"ro-flow","title":"Lead Ingestion Flow","kind":"Sequence","legend":None,
  "code":'''
sequenceDiagram
  autonumber
  participant W as Webhook
  participant K as Kafka
  participant P as Processor
  participant L as LLM
  participant D as DBs
  W->>K: publish(raw_lead)
  W-->>Client: 202 Accepted
  K->>P: consume
  P->>L: prompt(analyze intent & extract entities)
  L-->>P: JSON(score, budget, pain_points)
  P->>D: write enriched lead
''',
  "eraser":'''Webhook > Kafka: publish
Webhook > Client: 202
Kafka > Processor: consume
Processor > LLM: prompt
LLM > Processor: JSON
Processor > DB: write''',
  "components":[("202 Accepted","Immediate ack, async processing."),
    ("LLM Extraction","Converts unstructured text to structured JSON.")],
  "layout":"Linear pipeline from ingestion to DB."},
 "erd":{"id":"ro-erd","title":"ROVN — Data Model","kind":"ERD","legend":None,
  "code":'''
erDiagram
  COMPANY ||--o{ LEAD : has
  LEAD ||--o{ INTERACTION : has
  LEAD {
    uuid id PK
    uuid company_id FK
    string email
    int intent_score
    json extracted_data
  }
''',
  "eraser":'''COMPANY { id pk }
LEAD { id pk; company_id fk; intent_score }
INTERACTION { id pk; lead_id fk }
COMPANY 1-* LEAD
LEAD 1-* INTERACTION''',
  "components":[("intent_score","Indexed for fast sorting by SDRs."),
    ("extracted_data","JSONB column for flexible schema.")],
  "layout":"Standard hierarchy."},
 "auth":{"id":"ro-auth","title":"Auth","kind":"Sequence","legend":None,
  "code":'''
sequenceDiagram
  participant U as User
  participant API
  U->>API: JWT
  API->>API: Validate
''',
  "eraser":"User > API: JWT",
  "components":[("JWT","Standard auth")],
  "layout":"Simple validation."},
 "deploy":{"id":"ro-deploy","title":"Deployment","kind":"Deployment","legend":LEGEND,
  "code":CD+'''
flowchart TB
  LB["ALB"]:::svc --> API["API Tasks"]:::svc
''',
  "eraser":"ALB > API",
  "components":[("ALB","Load balancer")],
  "layout":"Basic deploy."},
 "scale":{"id":"ro-scale","title":"Scale","kind":"Evolution","legend":None,
  "code":CD+'''
flowchart LR
  S1["Single"]:::svc --> S2["Kafka"]:::queue
''',
  "eraser":"Single > Kafka",
  "components":[("Kafka","Decoupling")],
  "layout":"Evolution."},
 "failure":{"id":"ro-fail","title":"Failure","kind":"Resilience","legend":LEGEND_FAIL,
  "code":CD+'''
flowchart TB
  P["Processor"]:::svc -->|LLM fail| DLQ[["DLQ"]]:::bad
''',
  "eraser":"Processor > DLQ",
  "components":[("DLQ","Handles LLM timeouts")],
  "layout":"Failure flow."},
},
"fields":{
 "summary_lead":"ROVN uses AI to score and prioritize inbound leads.",
 "kpis":[{"v":"40%","l":"Conv. Lift"}],
 "problem":"Too much noise in inbound leads.",
 "users":"SDRs.",
 "goal":"Prioritize hot leads.",
 "role":"Architect.",
 "vision_lead":"Dynamic AI scoring.",
 "alternatives":[["Manual","Slow.","Fast."]],
 "features_cards":[{"ic":"⚡","h":"Score","p":"Real time."}],
 "biz_lead":"Time kills deals.",
 "pain_cards":[{"ic":"🗑️","h":"Spam","p":"Too much."}],
 "why_now":"Cheap LLMs.",
 "impact_bars":[{"l":"Lift","pct":40,"v":"40%","c":""}],
 "journey_lead":"Lead comes in, gets scored, SDR calls.",
 "journey":[{"n":"1","h":"Ingest","p":"Webhook."}],
 "fr_must":["Ingestion"],
 "fr_should":["Reporting"],
 "fr_table":[["FR1","Ingest","Webhook"]],
 "nfr_table":[["Perf","Fast","Kafka"]],
 "nfr_bars":[{"l":"Perf","pct":90,"v":"P0","c":""}],
 "stack_lead":"Kafka + LLM.",
 "stack_table":[["Stream","Kafka","Durable","Setup"]],
 "scale_table":[["100","Direct","Sync"]],
 "sec_lead":"Secure webhooks.",
 "threats":[["Spam","Rate limit","WAF"]],
 "sec_callout":["Validate webhooks", "Always validate webhooks to prevent spoofed data injection."],
 "golden":[{"ic":"⏱️","h":"Latency","p":"E2E"}],
 "alerts":[["DLQ > 0","Check LLM"]],
 "cost_lead":"Batch LLM calls.",
 "cost_kpis":[{"v":"Cheap","l":"LLM"}],
 "cost_moves":["Batch"],
 "incident":["Kafka lag", "The broker failed", "Add partition", "Scale out brokers"],
 "incident_blast":"Delayed leads.",
 "tradeoffs":[["Async","Consistency","Lag"]],
 "tradeoff_bars":[{"l":"Async","pct":90,"v":"High","c":""}],
 "roadmap_lead":"Auto replies.",
 "roadmap":[{"n":"V2","h":"Auto","p":"Drafts."}],
 "qa":[{"q":"Why Kafka?","a":"Bursts.","tags":["Kafka"]}],
 "rev_lead":"Kafka + LLM.",
 "revision":[{"h":"Arch","p":"Webhook -> Kafka -> LLM","acc":True}],
 "pitch":"ROVN prioritizes leads using AI.",
}
})

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  5 · TRAVIO                                                                ║
# ╚══════════════════════════════════════════════════════════════════════════╝
PROJECTS.append({
"name":"Travio","pnum":"05","tagline":"Trip Planner",
"subtitle":"Collaborative trip planner with Operational Transformation conflict sorting.",
"band_meta":[("TravelTech","Domain"),("WebSockets+OT","Core"),("Realtime","Sync"),("Tier 2","Priority")],
"diagrams":{
 "arch":{"id":"tr-arch","title":"Travio — System Architecture","kind":"C4 / Container","legend":LEGEND,
  "code":CD+'''
flowchart TB
  U([Users]):::client
  subgraph RT["Real-time Sync"]
    WS["WebSocket Gateway"]:::svc
    OT["OT Engine (Yjs/ShareDB)"]:::svc
  end
  subgraph STATE["State"]
    RD[["Redis Pub/Sub"]]:::queue
    MG[("MongoDB (Doc Store)")]:::data
  end
  U <-->|WS| WS
  WS <--> OT
  WS -->|fanout| RD
  OT --> MG
''',
  "eraser":'''Users [icon: users]
WS [icon: socket, color: blue]
OT [icon: cpu, color: blue]
Redis [icon: redis, color: amber]
Mongo [icon: mongodb, color: green]
Users <> WS
WS <> OT
WS > Redis
OT > Mongo''',
  "components":[("OT Engine","Handles concurrent document edits."),
    ("WebSockets","Bi-directional sync."),
    ("MongoDB","Stores JSON documents of trips.")],
  "layout":"Real-time loop."},
 "flow":{"id":"tr-flow","title":"Sync Flow","kind":"Sequence","legend":None,
  "code":'''
sequenceDiagram
  participant U1 as User 1
  participant WS
  participant OT
  participant U2 as User 2
  U1->>WS: edit(trip)
  WS->>OT: resolve conflict
  OT-->>WS: merged state
  WS->>U2: broadcast(edit)
''',
  "eraser":'''U1 > WS: edit
WS > OT: resolve
OT > WS: merged
WS > U2: broadcast''',
  "components":[("OT","Conflict resolution.")],
  "layout":"Sync sequence."},
 "erd":{"id":"tr-erd","title":"Travio — Data Model","kind":"ERD","legend":None,
  "code":'''
erDiagram
  TRIP ||--o{ ITINERARY : contains
  TRIP {
    uuid id PK
    json state
  }
''',
  "eraser":'''TRIP { id pk; state json }''',
  "components":[("state","JSON doc.")],
  "layout":"Simple doc."},
 "auth":{"id":"tr-auth","title":"Auth","kind":"Sequence","legend":None,
  "code":'''
sequenceDiagram
  participant U
  participant A
  U->>A: login
''',
  "eraser":"U > A",
  "components":[("Auth","...")],
  "layout":"..."},
 "deploy":{"id":"tr-deploy","title":"Deploy","kind":"Deployment","legend":LEGEND,
  "code":CD+'''
flowchart TB
  W["WS Nodes"]:::svc
''',
  "eraser":"W",
  "components":[("WS","...")],
  "layout":"..."},
 "scale":{"id":"tr-scale","title":"Scale","kind":"Evolution","legend":None,
  "code":CD+'''
flowchart LR
  S1["1"]:::svc
''',
  "eraser":"1",
  "components":[("1","...")],
  "layout":"..."},
 "failure":{"id":"tr-fail","title":"Failure","kind":"Resilience","legend":LEGEND_FAIL,
  "code":CD+'''
flowchart TB
  F["Fail"]:::bad
''',
  "eraser":"Fail",
  "components":[("Fail","...")],
  "layout":"..."},
},
"fields":{
 "summary_lead":"Travio is a real-time collaborative trip planner.",
 "kpis":[{"v":"Sync","l":"Realtime"}],
 "problem":"Conflicts in shared planning.",
 "users":"Travelers.",
 "goal":"Seamless collab.",
 "role":"Backend.",
 "vision_lead":"OT-based sync.",
 "alternatives":[["Google Docs","Generic.","Specific."]],
 "features_cards":[{"ic":"🚀","h":"Sync","p":"Live."}],
 "biz_lead":"Collab.",
 "pain_cards":[{"ic":"💥","h":"Conflict","p":"Overwrites."}],
 "why_now":"Yjs.",
 "impact_bars":[{"l":"Sync","pct":90,"v":"Fast","c":""}],
 "journey_lead":"Plan together.",
 "journey":[{"n":"1","h":"Plan","p":"Edit."}],
 "fr_must":["Sync"],
 "fr_should":["Export"],
 "fr_table":[["FR1","Sync","Live"]],
 "nfr_table":[["Perf","Low lat","WS"]],
 "nfr_bars":[{"l":"Lat","pct":90,"v":"P0","c":""}],
 "stack_lead":"WS + OT.",
 "stack_table":[["RT","Yjs","OT","Complex"]],
 "scale_table":[["100","Node","Single"]],
 "sec_lead":"Auth.",
 "threats":[["Access","Token","Valid"]],
 "sec_callout":["Secure WS", "Authenticate web sockets during connection handshake."],
 "golden":[{"ic":"⏱️","h":"Sync Lat","p":"ms"}],
 "alerts":[["WS Drop","Check"]],
 "cost_lead":"WS conns.",
 "cost_kpis":[{"v":"Low","l":"Cost"}],
 "cost_moves":["Scale"],
 "incident":["OT split", "Concurrency conflict", "CRDT merge", "Use CRDTs"],
 "incident_blast":"Desync.",
 "tradeoffs":[["OT","CRDT","OT"]],
 "tradeoff_bars":[{"l":"OT","pct":90,"v":"Max","c":""}],
 "roadmap_lead":"AI planner.",
 "roadmap":[{"n":"V2","h":"AI","p":"Suggest."}],
 "qa":[{"q":"Why OT?","a":"Collab.","tags":["OT"]}],
 "rev_lead":"Live sync.",
 "revision":[{"h":"Arch","p":"WS -> OT -> DB","acc":True}],
 "pitch":"Travio makes planning collaborative.",
}
})


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  6 · GRINDOS DESKTOP                                                       ║
# ╚══════════════════════════════════════════════════════════════════════════╝
PROJECTS.append({
"name":"GrindOS","pnum":"06","tagline":"Offline Learning",
"subtitle":"Offline-first Electron learning desktop app with IndexedDB replication.",
"band_meta":[("EdTech","Domain"),("Offline-First","Core"),("Local Sync","Sync"),("Tier 3","Priority")],
"diagrams":{
 "arch":{"id":"go-arch","title":"GrindOS Desktop — System Architecture","kind":"C4 / Container","legend":LEGEND,
  "code":CD+'''
flowchart TB
  subgraph CLIENT["Electron Desktop App"]
    UI["React UI"]:::client
    IDB[("IndexedDB (Local State)")]:::data
    SW["Service Worker"]:::svc
  end
  subgraph CLOUD["Cloud Backend"]
    API["FastAPI Sync API"]:::svc
    PG[("PostgreSQL (Master State)")]:::data
  end
  UI <-->|read/write local| IDB
  UI -->|cache resources| SW
  IDB <-->|sync delta| API
  API <--> PG
''',
  "eraser":'''UI [icon: react, color: orange]
IndexedDB [icon: database, color: green]
ServiceWorker [icon: cpu, color: blue]
Sync API [icon: python, color: blue]
Postgres [icon: postgresql, color: green]

UI <> IndexedDB: local read/write
UI > ServiceWorker: cache
IndexedDB <> Sync API: sync deltas
Sync API <> Postgres: master state''',
  "components":[("IndexedDB","Stores learning progress locally so the app works offline."),
    ("Service Worker","Caches video/text assets for offline playback."),
    ("Sync API","Merges local deltas with the master DB when online.")],
  "layout":"Left-to-right from local offline storage to cloud sync."},
 "flow":{"id":"go-flow","title":"Offline Sync Flow","kind":"Sequence","legend":None,
  "code":'''
sequenceDiagram
  participant U as User
  participant UI as App UI
  participant IDB as IndexedDB
  participant API as Cloud API
  
  U->>UI: Complete Lesson (Offline)
  UI->>IDB: save(lesson_status)
  note over UI,IDB: App remains functional offline
  U->>UI: Go Online
  UI->>API: push(local_deltas)
  API-->>UI: pull(cloud_deltas)
  UI->>IDB: merge(deltas)
''',
  "eraser":'''User > UI: complete lesson
UI > IndexedDB: save local
UI > API: go online -> push deltas
API > UI: pull deltas
UI > IndexedDB: merge''',
  "components":[("Local Write","Zero-latency UI updates."),
    ("Delta Sync","Transfers only changed rows to save bandwidth.")],
  "layout":"Offline actions buffered, then synced."},
 "erd":{"id":"go-erd","title":"GrindOS — Data Model","kind":"ERD","legend":None,
  "code":'''
erDiagram
  USER ||--o{ PROGRESS : tracks
  PROGRESS {
    uuid id PK
    uuid lesson_id
    string status
    timestamp updated_at
    boolean is_synced
  }
''',
  "eraser":'''USER { id pk }
PROGRESS { id pk; lesson_id; status; updated_at; is_synced }
USER 1-* PROGRESS''',
  "components":[("updated_at","Used for conflict resolution (last-write-wins)."),
    ("is_synced","Flag to track pending uploads.")],
  "layout":"Simple entity."},
 "auth":{"id":"go-auth","title":"Auth","kind":"Sequence","legend":None,
  "code":'''
sequenceDiagram
  participant U
  participant A
  U->>A: login
''',
  "eraser":"U > A",
  "components":[("JWT","Cached locally for offline access.")],
  "layout":"Standard"},
 "deploy":{"id":"go-deploy","title":"Deploy","kind":"Deployment","legend":LEGEND,
  "code":CD+'''
flowchart TB
  A["Electron Builder"]:::svc --> B["S3 Binaries"]:::data
''',
  "eraser":"A > B",
  "components":[("Electron Builder","Packages for Mac/Windows.")],
  "layout":"Simple CI/CD."},
 "scale":{"id":"go-scale","title":"Scale","kind":"Evolution","legend":None,
  "code":CD+'''
flowchart LR
  S1["Web Only"]:::svc --> S2["Electron + Offline"]:::data
''',
  "eraser":"S1 > S2",
  "components":[("Offline-First","Removes server load.")],
  "layout":"Evolution."},
 "failure":{"id":"go-fail","title":"Failure","kind":"Resilience","legend":LEGEND_FAIL,
  "code":CD+'''
flowchart TB
  F["Network Loss"]:::bad -->|Fallback| IDB["IndexedDB"]:::data
''',
  "eraser":"Net > IDB",
  "components":[("Graceful Degradation","UI reads from local store.")],
  "layout":"Resilience."},
},
"fields":{
 "summary_lead":"GrindOS is an offline-first learning platform.",
 "kpis":[{"v":"0ms","l":"Read Latency"}],
 "problem":"Students drop off due to poor internet.",
 "users":"Students in low-bandwidth areas.",
 "goal":"Uninterrupted learning.",
 "role":"Full-Stack.",
 "vision_lead":"Local-first architecture.",
 "alternatives":[["Web Only","Requires network.","Offline first."]],
 "features_cards":[{"ic":"🔋","h":"Offline","p":"Always works."}],
 "biz_lead":"Accessibility.",
 "pain_cards":[{"ic":"📶","h":"No Net","p":"Lost work."}],
 "why_now":"PWA/Electron maturity.",
 "impact_bars":[{"l":"Offline","pct":100,"v":"Yes","c":""}],
 "journey_lead":"Learn anywhere.",
 "journey":[{"n":"1","h":"Download","p":"Cache."}],
 "fr_must":["Offline"],
 "fr_should":["Sync"],
 "fr_table":[["FR1","Offline","Local DB"]],
 "nfr_table":[["Perf","Fast","IDB"]],
 "nfr_bars":[{"l":"Perf","pct":90,"v":"P0","c":""}],
 "stack_lead":"Electron + IDB.",
 "stack_table":[["Local","IDB","Fast","Complex"]],
 "scale_table":[["100","DB","Sync"]],
 "sec_lead":"Local encryption.",
 "threats":[["Local","Encrypt DB","AES"]],
 "sec_callout":["Secure local storage", "Encrypt local IndexedDB using AES."],
 "golden":[{"ic":"⏱️","h":"Sync Lat","p":"ms"}],
 "alerts":[["Sync Fail","Check API"]],
 "cost_lead":"Client compute.",
 "cost_kpis":[{"v":"Low","l":"Cost"}],
 "cost_moves":["Client Side"],
 "incident":["Sync conflict", "Offline divergence", "Last-write-wins", "Use LWW"],
 "incident_blast":"Data loss.",
 "tradeoffs":[["Local","State","Sync"]],
 "tradeoff_bars":[{"l":"Local","pct":90,"v":"Max","c":""}],
 "roadmap_lead":"P2P sync.",
 "roadmap":[{"n":"V2","h":"P2P","p":"WebRTC."}],
 "qa":[{"q":"Why offline?","a":"Access.","tags":["Offline"]}],
 "rev_lead":"Offline first.",
 "revision":[{"h":"Arch","p":"Electron -> IDB -> API","acc":True}],
 "pitch":"GrindOS runs entirely offline, syncing only when you reconnect.",
}
})

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  7 · SANKALAN                                                              ║
# ╚══════════════════════════════════════════════════════════════════════════╝
PROJECTS.append({
"name":"Sankalan","pnum":"07","tagline":"Resource Hub",
"subtitle":"Academic Resource Pathfinder with full-text search indexing.",
"band_meta":[("EdTech","Domain"),("PostgreSQL FTS","Core"),("Fast Search","Sync"),("Tier 3","Priority")],
"diagrams":{
 "arch":{"id":"sn-arch","title":"Sankalan — System Architecture","kind":"C4 / Container","legend":LEGEND,
  "code":CD+'''
flowchart TB
  U([Students]):::client
  API["Node.js API"]:::svc
  PG[("PostgreSQL (Full-Text Search)")]:::data
  S3[("AWS S3 (Files)")]:::data
  
  U -->|Search Query| API
  API -->|ts_query| PG
  API -->|Presigned URL| S3
  S3 -->|Download| U
''',
  "eraser":'''Students [icon: users]
API [icon: nodejs, color: blue]
Postgres [icon: postgresql, color: green]
S3 [icon: aws, color: green]

Students > API: search
API > Postgres: full-text search
API > S3: get presigned URL
S3 > Students: download''',
  "components":[("Postgres FTS","Leverages ts_vector for instant document retrieval without ElasticSearch."),
    ("S3 Presigned URLs","Secure, direct downloads offloading bandwidth from the API.")],
  "layout":"Top-to-bottom search and retrieve flow."},
 "flow":{"id":"sn-flow","title":"Search Flow","kind":"Sequence","legend":None,
  "code":'''
sequenceDiagram
  participant U as User
  participant API
  participant DB as Postgres (ts_vector)
  
  U->>API: GET /search?q=machine+learning
  API->>DB: SELECT ts_rank(to_tsvector, query)
  DB-->>API: ranked_results
  API-->>U: JSON(results)
''',
  "eraser":'''User > API: GET /search
API > DB: ts_rank query
DB > API: ranked results
API > User: JSON''',
  "components":[("ts_rank","Orders results by term frequency and relevance.")],
  "layout":"Standard API sequence."},
 "erd":{"id":"sn-erd","title":"Sankalan — Data Model","kind":"ERD","legend":None,
  "code":'''
erDiagram
  RESOURCE {
    uuid id PK
    string title
    string url
    tsvector text_search_index
  }
''',
  "eraser":'''RESOURCE { id pk; title; url; text_search_index }''',
  "components":[("tsvector","Precomputed index column for fast queries.")],
  "layout":"Simple."},
 "auth":{"id":"sn-auth","title":"Auth","kind":"Sequence","legend":None,
  "code":'''
sequenceDiagram
  participant U
  participant A
  U->>A: login
''',
  "eraser":"U > A",
  "components":[("OAuth","Google Sign-In.")],
  "layout":"Standard"},
 "deploy":{"id":"sn-deploy","title":"Deploy","kind":"Deployment","legend":LEGEND,
  "code":CD+'''
flowchart TB
  W["Web Tier"]:::svc --> DB["RDS"]:::data
''',
  "eraser":"W > DB",
  "components":[("RDS","Managed Postgres.")],
  "layout":"Standard"},
 "scale":{"id":"sn-scale","title":"Scale","kind":"Evolution","legend":None,
  "code":CD+'''
flowchart LR
  S1["LIKE query"]:::bad --> S2["ts_vector"]:::data
''',
  "eraser":"S1 > S2",
  "components":[("FTS","100x faster than LIKE '%term%'.")],
  "layout":"Optimization."},
 "failure":{"id":"sn-fail","title":"Failure","kind":"Resilience","legend":LEGEND_FAIL,
  "code":CD+'''
flowchart TB
  F["DB Slowdown"]:::bad -->|Cache| RD["Redis"]:::data
''',
  "eraser":"DB > Redis",
  "components":[("Query Cache","Caches frequent searches.")],
  "layout":"Resilience."},
},
"fields":{
 "summary_lead":"Sankalan centralizes academic resources with instant search.",
 "kpis":[{"v":"50ms","l":"Search Lat"}],
 "problem":"Scattered PDFs in WhatsApp groups.",
 "users":"University students.",
 "goal":"Find resources instantly.",
 "role":"Backend.",
 "vision_lead":"Built-in Postgres FTS.",
 "alternatives":[["Google Drive","No deep search.","FTS."]],
 "features_cards":[{"ic":"🔎","h":"Search","p":"Fast FTS."}],
 "biz_lead":"Time saving.",
 "pain_cards":[{"ic":"🗑️","h":"Lost files","p":"Chat history."}],
 "why_now":"Postgres FTS maturity.",
 "impact_bars":[{"l":"Find","pct":90,"v":"Fast","c":""}],
 "journey_lead":"Type, click, download.",
 "journey":[{"n":"1","h":"Search","p":"Instant."}],
 "fr_must":["Search"],
 "fr_should":["Uploads"],
 "fr_table":[["FR1","Search","FTS"]],
 "nfr_table":[["Perf","Fast","PG"]],
 "nfr_bars":[{"l":"Perf","pct":90,"v":"P0","c":""}],
 "stack_lead":"Node + Postgres.",
 "stack_table":[["DB","PG","FTS","Scaling"]],
 "scale_table":[["100","LIKE","Slow"]],
 "sec_lead":"Presigned URLs.",
 "threats":[["Leak","Presigned URL","Expiry"]],
 "sec_callout":["S3 security", "Use short-lived pre-signed URLs."],
 "golden":[{"ic":"⏱️","h":"Search Lat","p":"ms"}],
 "alerts":[["Slow Query","Index"]],
 "cost_lead":"No ElasticSearch.",
 "cost_kpis":[{"v":"Low","l":"Cost"}],
 "cost_moves":["Avoid ES"],
 "incident":["Unindexed query", "Missing index", "Add GIN index", "Always use GIN"],
 "incident_blast":"Slowdowns.",
 "tradeoffs":[["PG FTS","ElasticSearch","Simplicity"]],
 "tradeoff_bars":[{"l":"Simplicity","pct":90,"v":"Max","c":""}],
 "roadmap_lead":"AI summaries.",
 "roadmap":[{"n":"V2","h":"AI","p":"Summaries."}],
 "qa":[{"q":"Why PG FTS?","a":"Simplicity.","tags":["FTS"]}],
 "rev_lead":"Postgres FTS.",
 "revision":[{"h":"Arch","p":"API -> PG FTS","acc":True}],
 "pitch":"Sankalan makes academic files instantly searchable using Postgres Full-Text Search.",
}
})
