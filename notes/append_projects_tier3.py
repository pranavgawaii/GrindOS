import sys

TIER3_CODE = """
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
 "sec_callout":["Secure local storage"],
 "golden":[{"ic":"⏱️","h":"Sync Lat","p":"ms"}],
 "alerts":[["Sync Fail","Check API"]],
 "cost_lead":"Client compute.",
 "cost_kpis":[{"v":"Low","l":"Cost"}],
 "cost_moves":["Client Side"],
 "incident":["Sync conflict."],
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
 "sec_callout":["S3 security"],
 "golden":[{"ic":"⏱️","h":"Search Lat","p":"ms"}],
 "alerts":[["Slow Query","Index"]],
 "cost_lead":"No ElasticSearch.",
 "cost_kpis":[{"v":"Low","l":"Cost"}],
 "cost_moves":["Avoid ES"],
 "incident":["Unindexed query."],
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
"""

with open("/Users/8teen/Downloads/04_/Active/GrindOS/notes/projects_data.py", "a") as f:
    f.write("\n" + TIER3_CODE)
print("Tier 3 Projects appended.")
