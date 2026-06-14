import sys

ROVN_CODE = """
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
 "sec_callout":["Validate webhooks"],
 "golden":[{"ic":"⏱️","h":"Latency","p":"E2E"}],
 "alerts":[["DLQ > 0","Check LLM"]],
 "cost_lead":"Batch LLM calls.",
 "cost_kpis":[{"v":"Cheap","l":"LLM"}],
 "cost_moves":["Batch"],
 "incident":["Kafka lag."],
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
 "sec_callout":["Secure WS"],
 "golden":[{"ic":"⏱️","h":"Sync Lat","p":"ms"}],
 "alerts":[["WS Drop","Check"]],
 "cost_lead":"WS conns.",
 "cost_kpis":[{"v":"Low","l":"Cost"}],
 "cost_moves":["Scale"],
 "incident":["OT split."],
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
"""

with open("/Users/8teen/Downloads/04_/Active/GrindOS/notes/projects_data.py", "a") as f:
    f.write("\n" + ROVN_CODE)
print("Projects appended.")
