import base64
import os
from handbook_engine import _mermaid, _mermaid_runtime, b_diagram, b_dossier

# Load logo
with open("../logo.png", "rb") as img_file:
    LOGO_BASE64 = base64.b64encode(img_file.read()).decode('utf-8')

# 80 SYSTEM DESIGN TOPICS GROUPED BY SECTION

CD = '''classDef client fill:#FBF8F4,stroke:#EA763F,stroke-width:2px,color:#0F172A;
classDef svc fill:#EFF4FF,stroke:#2563EB,stroke-width:2px,color:#0F172A;
classDef data fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#0F172A;
classDef queue fill:#FFFBEB,stroke:#D97706,stroke-width:2px,color:#0F172A;
classDef ext fill:#F5F3FF,stroke:#7C3AED,stroke-width:2px,color:#0F172A;
classDef bad fill:#FEF2F2,stroke:#DC2626,stroke-width:2px,color:#0F172A;
'''

topics_data = [
    # ── SECTION 1: FOUNDATIONS ──
    {
        "id": "sys-01",
        "num": "01",
        "section": "Foundations",
        "title": "What Is System Design",
        "def": "The process of defining the architecture, interfaces, and data models for a system to satisfy specific requirements.",
        "why": "It enables building scalable, reliable, and cost-effective software systems that can handle growth over time.",
        "usage": "Used by companies to transition from simple MVPs to distributed systems serving millions of users.",
        "diagram_arch_data": {
    "id": "sys-01-arch", "title": "System Design Architecture", "kind": "ARCHITECTURE",
    "code": """flowchart TB
  U([Client App]):::client
  GW[\"API Gateway\"]:::svc
  SVC[\"Microservices\"]:::svc
  DB[(\"Databases\")]:::data
  C[[\"Cache\"]]:::queue
  MQ[[\"Message Queue\"]]:::queue

  U --> GW
  GW --> SVC
  SVC --> DB
  SVC --> C
  SVC --> MQ""",
    "eraser": """// 1. Define nodes and logical groups
Client App [icon: smartphone, color: orange]
API Gateway [icon: server, color: blue]
Microservices [icon: code, color: blue]
Databases [icon: database, color: green]
Cache [icon: layers, color: yellow]
Message Queue [icon: list, color: yellow]

// 2. Define connections
Client App > API Gateway
API Gateway > Microservices
Microservices > Databases
Microservices > Cache
Microservices > Message Queue""",
    "components": [("Client App","The frontend interface."), ("API Gateway","Central entry point handling routing."), ("Microservices","Independent business logic servers."), ("Databases","Persistent storage.")],
    "layout": "The client sits at the top, directing traffic through a central gateway which fans out to internal services and storage layers."
}, "diagram_flow_data": {
    "id": "sys-01-flow", "title": "System Design Request Flow", "kind": "REQUEST FLOW",
    "code": """sequenceDiagram
  participant C as Client
  participant GW as Gateway
  participant AS as App Server
  participant DB as DB/Cache
  C->>GW: HTTP Request
  GW->>AS: Route
  AS->>DB: Query
  DB-->>AS: Results
  AS-->>C: 200 OK""",
    "eraser": """// Sequence
Client > Gateway: HTTP Request
Gateway > App Server: Route
App Server > DB: Query
DB > App Server: Results
App Server > Client: 200 OK""",
    "components": [("HTTP Request","Standard REST or gRPC call."), ("Route","Gateway forwards packet based on path."), ("Query","Service fetches required state.")],
    "layout": "Vertical sequence showing round-trip synchronous request processing."
}, "diagram": """
[Client App] ---> [API Gateway] ---> [Services] ---> [Databases]
                     |                  |
                     v                  v
                  [Cache]         [Message Queue]
""",
        "flow": "Client -> Gateway -> Application Server -> DB / Cache lookup -> Client Response.",
        "pros": "Ensures scalability, cost management, and maintainability.",
        "cons": "Adds design complexity and upfront development time overhead.",
        "tradeoff": "Upfront architecture planning vs rapid product release velocity.",
        "questions": "What is the difference between functional and non-functional requirements?",
        "followups": "How do you handle capacity estimation for storage?",
        "mistake": "Neglecting non-functional requirements like latency and availability during early planning.",
        "trick": "System design is like town planning: define roads (APIs) and zones (services) before building houses."
    },
    {
        "id": "sys-02",
        "num": "02",
        "section": "Foundations",
        "title": "Scalability",
        "def": "A system's ability to handle growing amounts of work by adding resources to the system.",
        "why": "Prevents system lockups during peak user traffic spikes.",
        "usage": "E-commerce platforms scaling compute instances during holiday shopping sales.",
        "diagram_arch_data": {
    "id": "sys-02-arch", "title": "Horizontal Scaling Architecture", "kind": "ARCHITECTURE",
    "code": """flowchart TB
  U([Users]):::client
  LB[\"Load Balancer\"]:::svc
  subgraph ASG[\"Auto-Scaling Group\"]
    WS1[\"Web Server 1\"]:::svc
    WSN[\"Web Server N\"]:::svc
  end
  DB[(\"Database\")]:::data
  U --> LB
  LB --> WS1 & WSN
  WS1 & WSN --> DB""",
    "eraser": """// Nodes
Users [icon: users, color: orange]
Load Balancer [icon: server, color: blue]
Group Auto-Scaling Group {
  Web Server 1 [icon: box, color: blue]
  Web Server N [icon: box, color: blue]
}
Database [icon: database, color: green]

// Edges
Users > Load Balancer
Load Balancer > Web Server 1
Load Balancer > Web Server N
Web Server 1 > Database
Web Server N > Database""",
    "components": [("Auto-Scaling Group","Dynamically adds/removes instances."), ("Load Balancer","Distributes traffic across active instances.")],
    "layout": "Traffic flows from users, splits at the load balancer, and converges at the database."
}, "diagram_flow_data": {
    "id": "sys-02-flow", "title": "Auto-Scaling Flow", "kind": "REQUEST FLOW",
    "code": """sequenceDiagram
  participant TS as Traffic
  participant AS as Auto Scaler
  participant CP as Cloud
  participant LB as Load Balancer
  TS->>AS: CPU > 80%
  AS->>CP: Request compute
  CP-->>AS: Instance booted
  AS->>LB: Register IP
  LB->>CP: Route traffic""",
    "eraser": """Traffic > Auto Scaler: CPU > 80%
Auto Scaler > Cloud: Request compute
Cloud > Auto Scaler: Instance booted
Auto Scaler > Load Balancer: Register IP
Load Balancer > Cloud: Route traffic""",
    "components": [("Trigger","Metric threshold exceeded."), ("Provision","Cloud allocates resources."), ("Register","LB adds instance to pool.")],
    "layout": "Shows the background asynchronous process of scaling infrastructure."
}, "diagram": """
                  +---> [Web Instance 1] ---> [DB]
[Load Balancer] --+---> [Web Instance 2]
                  +---> [Web Instance 3]
""",
        "flow": "Traffic Spikes -> Auto-scaler triggers -> New instances join load balancer pool -> Load balances.",
        "pros": "Prevents downtime, improves load speeds, and supports user growth.",
        "cons": "Increases cloud infrastructure costs and data synchronization lag.",
        "tradeoff": "Over-provisioning servers (high cost) vs active auto-scaling lag (brief downtime).",
        "questions": "How do you measure scalability?",
        "followups": "What are the limits of vertical scalability?",
        "mistake": "Assuming scaling is instant. Container spin-up times can take several minutes.",
        "trick": "Scalability is adding more checkout lanes at a supermarket when lines get long."
    },
    {
        "id": "sys-03",
        "num": "03",
        "section": "Foundations",
        "title": "Availability",
        "def": "The percentage of time a system remains operational and accessible to users.",
        "why": "Guarantees business continuity and meets Service Level Agreements (SLAs).",
        "usage": "High-availability financial gateways targeting 'five nines' (99.999%) uptime.",
        "diagram_arch_data": {
    "id": "sys-03-arch", "title": "High Availability Multi-Region", "kind": "ARCHITECTURE",
    "code": """flowchart TB
  U([Users]):::client
  DNS[\"Route 53\"]:::svc
  subgraph R1[\"US-East\"]
    DB1[(\"Primary\")]:::data
  end
  subgraph R2[\"EU-West\"]
    DB2[(\"Replica\")]:::data
  end
  U --> DNS
  DNS --> R1
  DB1 -.->|Replication| DB2
  DNS -.->|Failover| R2""",
    "eraser": """// Nodes
Users [icon: users, color: orange]
Route 53 [icon: compass, color: blue]
Group US-East { Primary [icon: database, color: green] }
Group EU-West { Replica [icon: database, color: green] }

// Edges
Users > Route 53
Route 53 > Primary
Primary > Replica [label: Replication, style: dashed]
Route 53 > Replica [label: Failover, style: dashed, color: red]""",
    "components": [("DNS Routing","Directs traffic to healthy regions."), ("Replication","Maintains state across geographic regions."), ("Failover","Fallback mechanism during regional outages.")],
    "layout": "Two distinct geographic clusters separated by a global DNS router."
}, "diagram_flow_data": {
    "id": "sys-03-flow", "title": "DNS Failover Sequence", "kind": "REQUEST FLOW",
    "code": """sequenceDiagram
  participant U as User
  participant DNS as DNS Router
  participant R1 as Primary Region
  participant R2 as Standby Region
  R1--xDNS: Health check fails
  DNS->>DNS: Swap IP
  U->>DNS: Request
  DNS->>R2: Route to Standby
  R2-->>U: Success""",
    "eraser": """Primary Region > DNS Router: Health check fails [color: red]
DNS Router > DNS Router: Swap IP
User > DNS Router: Request
DNS Router > Standby Region: Route to Standby
Standby Region > User: Success""",
    "components": [("Health Check","Periodic ping to verify region uptime."), ("TTL Swap","DNS updates routing IP record."), ("Promotion","Standby DB becomes primary.")],
    "layout": "Illustrates the failure detection and routing recovery sequence."
}, "diagram": """
[Region A (Active)] ---> [Database Primary]
                               | (Replication)
[Region B (Standby)] --> [Database Replica]
""",
        "flow": "Active Region drops -> DNS failover triggers -> Standby Region promoted to active.",
        "pros": "Maintains user trust, reduces transaction losses.",
        "cons": "Requires expensive active-active multi-region replication setups.",
        "tradeoff": "System availability vs database consistency during network partitions (CAP theorem).",
        "questions": "What is the difference between active-passive and active-active failover?",
        "followups": "How do you calculate system availability for serial components?",
        "mistake": "Confusing availability with reliability. A slow, buggy system can still be 'available'.",
        "trick": "Availability is keeping backup generators ready in case the main grid fails."
    },
    {
        "id": "sys-04",
        "num": "04",
        "section": "Foundations",
        "title": "Reliability",
        "def": "The probability that a system performs its required functions under stated conditions for a specified period.",
        "why": "Ensures calculations are correct and transactions complete successfully.",
        "usage": "Banking databases requiring strict transaction completions.",
        "diagram_arch_data": {
    "id": "sys-04-arch", "title": "Reliability and Write-Ahead Logging", "kind": "ARCHITECTURE",
    "code": """flowchart TB
  APP[\"App Server\"]:::svc
  WAL[[\"Write-Ahead Log\"]]:::queue
  DB[(\"Database\")]:::data
  APP -->|1. Write| WAL
  WAL -->|2. Commit| DB
  DB -->|3. Ack| APP""",
    "eraser": """// Nodes
App Server [icon: server, color: blue]
Write-Ahead Log [icon: list, color: yellow]
Database [icon: database, color: green]

// Edges
App Server > Write-Ahead Log [label: 1. Write]
Write-Ahead Log > Database [label: 2. Commit]
Database > App Server [label: 3. Ack]""",
    "components": [("Write-Ahead Log","Append-only ledger guaranteeing writes."), ("Database Store","Final resting place for structured state.")],
    "layout": "A sequential triad showing the safety buffer between application and storage."
}, "diagram_flow_data": {
    "id": "sys-04-flow", "title": "Atomic Commit Sequence", "kind": "REQUEST FLOW",
    "code": """sequenceDiagram
  participant APP as App Server
  participant WAL as WAL
  participant DB as Database
  APP->>WAL: Append log
  WAL-->>APP: Log synced
  WAL->>DB: Execute state change
  DB-->>APP: Committed""",
    "eraser": """App Server > WAL: Append log
WAL > App Server: Log synced
WAL > Database: Execute state change
Database > App Server: Committed""",
    "components": [("Sync Disk","Flushing log to physical storage."), ("Execute","Applying change to DB memory structures.")],
    "layout": "Shows the blocking atomic wait states during a reliable commit."
}, "diagram": """
[Application] ---> [Write-Ahead Log] ---> [DB Store]
                        | (Commit)
                        v
                 [Success Return]
""",
        "flow": "Input -> Log transaction -> Execute state change -> Return verified output.",
        "pros": "Ensures transaction safety, data accuracy, and user trust.",
        "cons": "Slightly slows down processing due to safety checks.",
        "tradeoff": "Execution speed (no logs) vs transaction reliability (atomic writes).",
        "questions": "How do you guarantee transaction reliability?",
        "followups": "What is a write-ahead log?",
        "mistake": "Believing redundant servers guarantee reliability. Redundancy only supports availability.",
        "trick": "Reliability is a car that starts every time; availability is having two cars."
    },
    {
        "id": "sys-05",
        "num": "05",
        "section": "Foundations",
        "title": "Fault Tolerance",
        "def": "A system's ability to continue operating properly in the event of the failure of some of its components.",
        "why": "Prevents single component failures from bringing down the entire application.",
        "usage": "Netflix using Chaos Monkey to terminate servers in production to test resilience.",
        "diagram_arch_data": {
    "id": "sys-05-arch", "title": "Active-Passive Node Failover", "kind": "ARCHITECTURE",
    "code": """flowchart TB
  C([Clients]):::client
  LB[\"Load Balancer\"]:::svc
  N1[\"Node A (Primary)\"]:::svc
  N2[\"Node B (Standby)\"]:::svc
  C --> LB
  LB --> N1
  N1 -.->|Heartbeat| N2
  LB -.->|Takes over| N2""",
    "eraser": """// Nodes
Clients [icon: users, color: orange]
Load Balancer [icon: server, color: blue]
Node A [icon: box, color: blue]
Node B [icon: box, color: blue]

// Edges
Clients > Load Balancer
Load Balancer > Node A
Node A > Node B [label: Heartbeat, style: dashed]
Load Balancer > Node B [label: Failover, style: dashed, color: red]""",
    "components": [("Primary Node","Handles active connections."), ("Standby Node","Idles until failure detection."), ("Heartbeat","Pulse check between nodes.")],
    "layout": "Parallel active and passive nodes connected via a heartbeat bridge."
}, "diagram_flow_data": {
    "id": "sys-05-flow", "title": "Failover Recovery Sequence", "kind": "REQUEST FLOW",
    "code": """sequenceDiagram
  participant LB as Load Balancer
  participant N1 as Primary
  participant N2 as Standby
  N1->>N2: Heartbeat (ok)
  N1--xN2: Heartbeat (dropped)
  N2->>LB: Assume Primary
  LB->>N2: Route traffic""",
    "eraser": """Primary > Standby: Heartbeat (ok)
Primary > Standby: Heartbeat (dropped) [color: red]
Standby > Load Balancer: Assume Primary
Load Balancer > Standby: Route traffic""",
    "components": [("Detection","Standby notices missing pings."), ("Assumption","Standby elevates privileges."), ("Re-route","LB updates target group.")],
    "layout": "Chronological timeline of a node death and subsequent takeover."
}, "diagram": """
[Node A (Primary)] --+ (Heartbeat)
                     v
[Node B (Standby)] --+ (Takes over on drop)
""",
        "flow": "Primary fails -> Standby detects loss of heartbeat -> Standby assumes primary role.",
        "pros": "Prevents total system outages, enabling graceful degradation.",
        "cons": "Requires hardware redundancy, increasing costs.",
        "tradeoff": "System component redundancy vs operational infrastructure budget.",
        "questions": "What is a single point of failure (SPOF)?",
        "followups": "How does split-brain happen in active-active cluster failovers?",
        "mistake": "Assuming failover is zero-latency. Promoting a standby db node takes time.",
        "trick": "Fault tolerance is dual tires on semi-trucks: if one pops, the truck keeps moving."
    },
    {
        "id": "sys-06",
        "num": "06",
        "section": "Foundations",
        "title": "Latency",
        "def": "The time it takes for a data packet to travel from source to destination.",
        "why": "Directly impacts user experience and interface responsiveness.",
        "usage": "High-frequency trading systems where millisecond delays cause lost transactions.",
        "diagram_arch_data": {
    "id": "sys-06-arch", "title": "CDN Edge Caching Architecture", "kind": "ARCHITECTURE",
    "code": """flowchart LR
  U([Client]):::client
  CDN[\"Edge CDN\"]:::svc
  SRV[\"Origin Server\"]:::svc
  DB[(\"Database\")]:::data
  U -->|10ms| CDN
  CDN -->|Miss: 50ms| SRV
  SRV -->|10ms| DB""",
    "eraser": """// Nodes
Client [icon: smartphone, color: orange]
Edge CDN [icon: server, color: blue]
Origin Server [icon: server, color: blue]
Database [icon: database, color: green]

// Edges
Client > Edge CDN [label: 10ms]
Edge CDN > Origin Server [label: Cache Miss, style: dashed]
Origin Server > Database [label: 10ms]""",
    "components": [("Edge Node","Geographically close caching server."), ("Origin","Source of truth handling dynamic requests.")],
    "layout": "Linear progression demonstrating physical distance impacts on network time."
}, "diagram_flow_data": {
    "id": "sys-06-flow", "title": "Cache Miss Sequence", "kind": "REQUEST FLOW",
    "code": """sequenceDiagram
  participant C as Client
  participant CDN as Edge Server
  participant SRV as Origin
  C->>CDN: Request
  CDN-->>C: Cache Hit (Fast)
  C->>CDN: Request 2
  CDN->>SRV: Cache Miss (Network)
  SRV-->>C: Response (Slow)""",
    "eraser": """Client > Edge Server: Request
Edge Server > Client: Cache Hit (Fast) [color: green]
Client > Edge Server: Request 2
Edge Server > Origin: Cache Miss (Network) [color: red]
Origin > Client: Response (Slow)""",
    "components": [("Cache Hit","Instant return from memory."), ("Cache Miss","Blocking network trip to origin server.")],
    "layout": "Contrasts the immediate turnaround of a hit vs the multi-hop delay of a miss."
}, "diagram": """
[Client] --- (Request: 50ms) ---> [Server]
[Client] <--- (Response: 50ms) --- [Server]
Total Round Trip Time (RTT): 100ms
""",
        "flow": "Network transmission -> Server processing -> Network transmission back.",
        "pros": "Improves page load speeds and user retention.",
        "cons": "Minimizing latency requires expensive CDNs and caching architectures.",
        "tradeoff": "Deep computation checks (higher latency) vs rapid cached returns.",
        "questions": "How do you reduce API latency?",
        "followups": "What is the difference between latency and round-trip time (RTT)?",
        "mistake": "Believing network bandwidth solves latency. Latency is limited by the speed of light.",
        "trick": "Latency is the time spent waiting for your food order to arrive at your table."
    },
    {
        "id": "sys-07",
        "num": "07",
        "section": "Foundations",
        "title": "Throughput",
        "def": "The number of requests or data transactions processed by a system within a given time frame.",
        "why": "Measures total processing capacities under heavy loads.",
        "usage": "Data streaming platforms measuring operations processed per second (RPS).",
        "diagram_arch_data": {
    "id": "sys-07-arch", "title": "High Throughput Batching", "kind": "ARCHITECTURE",
    "code": """flowchart TB
  IN[\"Incoming: 10k RPS\"]:::client
  Q[[\"Queue Buffer\"]]:::queue
  subgraph SC[\"Server Cluster\"]
    W1[\"Worker 1\"]:::svc
    W2[\"Worker 2\"]:::svc
  end
  DB[(\"Database\")]:::data
  IN --> Q
  Q --> SC
  SC -->|Processed: 9k RPS| DB
  IN -.->|1k dropped| Drop""",
    "eraser": """// Nodes
Incoming [icon: download, color: orange]
Queue Buffer [icon: list, color: yellow]
Group Server Cluster {
  Worker 1 [icon: box, color: blue]
  Worker 2 [icon: box, color: blue]
}
Database [icon: database, color: green]

// Edges
Incoming > Queue Buffer
Queue Buffer > Worker 1
Queue Buffer > Worker 2
Worker 1 > Database
Worker 2 > Database""",
    "components": [("Buffer","Absorbs immediate volume."), ("Worker Pool","Parallel processors draining queue.")],
    "layout": "Funnel architecture showing massive input converging through parallel processors."
}, "diagram_flow_data": {
    "id": "sys-07-flow", "title": "Parallel Queue Draining", "kind": "REQUEST FLOW",
    "code": """sequenceDiagram
  participant IN as Traffic
  participant Q as Queue
  participant W as Workers
  IN->>Q: Enqueue requests
  Q->>W: Pull batches
  W->>W: Process batch
  W-->>Q: Ack completion""",
    "eraser": """Traffic > Queue: Enqueue requests
Queue > Workers: Pull batches
Workers > Workers: Process batch
Workers > Queue: Ack completion""",
    "components": [("Batching","Grouping records for DB efficiency."), ("Parallelism","Simultaneous execution threads.")],
    "layout": "Shows asynchronous ingestion disconnected from processing speeds."
}, "diagram": """
[Incoming: 10k RPS] ---> [Server Cluster] ---> [Processed: 9k RPS]
                               | (1k dropped)
                               v
                       [Queue Buffers]
""",
        "flow": "Requests queue in buffer -> Cluster processes tasks in parallel -> Metric recorded.",
        "pros": "Enables processing high data volumes, supporting bulk transactions.",
        "cons": "High throughput systems can saturate network switches and memory buses.",
        "tradeoff": "High throughput (batch processing) vs low latency (instant single returns).",
        "questions": "How do you increase database throughput?",
        "followups": "How do latency and throughput relate?",
        "mistake": "Confusing throughput with speed. A pipeline can move tons of water slowly.",
        "trick": "Throughput is the width of the highway; latency is the speed limit."
    },
    {
        "id": "sys-08",
        "num": "08",
        "section": "Foundations",
        "title": "CAP Theorem",
        "def": "States that a distributed data store can simultaneously provide at most two of: Consistency, Availability, and Partition tolerance.",
        "why": "Provides a framework for understanding tradeoffs in distributed databases.",
        "usage": "Choosing Cassandra (AP) for high write speeds, or Postgres (CP) for transactions.",
        "diagram_arch_data": {
    "id": "sys-08-arch", "title": "CAP Theorem Tradeoffs", "kind": "ARCHITECTURE",
    "code": """flowchart TB
  subgraph CAP[\"Distributed Tradeoffs\"]
    C[\"Consistency\"]
    A[\"Availability\"]
    P[\"Partition Tolerance\"]
  end
  C ---|CP: Postgres| P
  A ---|AP: Cassandra| P
  C ---|CA: Single Node| A""",
    "eraser": """// Nodes
Consistency [icon: check-circle, color: blue]
Availability [icon: activity, color: green]
Partition Tolerance [icon: alert-triangle, color: red]

// Edges
Consistency - Partition Tolerance [label: CP]
Availability - Partition Tolerance [label: AP]
Consistency - Availability [label: CA]""",
    "components": [("Consistency","All reads receive the most recent write."), ("Availability","Every request receives a valid response.")],
    "layout": "Triangle matrix showing the impossibility of achieving all three vertices."
}, "diagram_flow_data": {
    "id": "sys-08-flow", "title": "Network Partition Resolution", "kind": "REQUEST FLOW",
    "code": """sequenceDiagram
  participant C as Client
  participant N1 as Node 1
  participant N2 as Node 2
  Note over N1,N2: Network Split (P)
  C->>N1: Write Data
  N1--xN2: Sync fails
  Note over N1: CP: Reject Write
  Note over N1: AP: Accept Write""",
    "eraser": """Client > Node 1: Write Data
Node 1 > Node 2: Sync fails [color: red]
Node 1 > Client: CP: Reject Write [color: red]
Node 1 > Client: AP: Accept Write [color: green]""",
    "components": [("Network Split","Communication break between nodes."), ("Reject","System stops to maintain accuracy.")],
    "layout": "Demonstrates the forced choice when a network line is severed."
}, "diagram": """
             Consistency (C)
                 /  \\
                /    \\
   (Postgres)  /  P   \\ (Cassandra)
              /________\\
    Availability (A)  Partition Tolerance (P)
""",
        "flow": "Network Split -> Choose to reject write (CP) OR write and allow drift (AP).",
        "pros": "Guides database technology selection for specific applications.",
        "cons": "Forces choosing between absolute consistency and constant availability.",
        "tradeoff": "Rejecting updates (Consistency) vs serving outdated data (Availability).",
        "questions": "What happens in an AP system during a network partition?",
        "followups": "Can a distributed database avoid Partitions (P)?",
        "mistake": "Believing partition tolerance is optional. Network drops WILL happen in distributed systems.",
        "trick": "CAP is choosing two: Fast delivery, Cheap price, or High quality."
    },
    {
        "id": "sys-09",
        "num": "09",
        "section": "Foundations",
        "title": "Consistency Models",
        "def": "Rules governing how database updates become visible to parallel read requests.",
        "why": "Balances read latencies against data synchronization constraints.",
        "usage": "Social media feeds using eventual consistency, while banks require strong consistency.",
        "diagram_arch_data": {
    "id": "sys-09-arch", "title": "Strong vs Eventual Consistency", "kind": "ARCHITECTURE",
    "code": """flowchart TB
  C([Client]):::client
  subgraph STRONG[\"Strong\"]
    W1[\"Write Node\"]:::svc ===|Sync lock| R1[\"Read Node\"]:::svc
  end
  subgraph EVENTUAL[\"Eventual\"]
    W2[\"Write Node\"]:::svc -.-|Async replica| R2[\"Read Node\"]:::svc
  end
  C --> STRONG & EVENTUAL""",
    "eraser": """// Nodes
Client [icon: user, color: orange]
Group Strong {
  W1 [icon: edit, color: blue]
  R1 [icon: eye, color: blue]
}
Group Eventual {
  W2 [icon: edit, color: green]
  R2 [icon: eye, color: green]
}

// Edges
Client > W1
Client > W2
W1 > R1 [label: Sync lock]
W2 > R2 [label: Async replica, style: dashed]""",
    "components": [("Sync Lock","Blocks returns until replication completes."), ("Async Replica","Returns immediately, replicates later.")],
    "layout": "Side-by-side comparison of synchronous blocking vs asynchronous background tasks."
}, "diagram_flow_data": {
    "id": "sys-09-flow", "title": "Consistency Timing", "kind": "REQUEST FLOW",
    "code": """sequenceDiagram
  participant C as Client
  participant W as Write Node
  participant R as Read Node
  C->>W: Strong Write
  W->>R: Sync
  R-->>W: Ack
  W-->>C: Success
  C->>W: Eventual Write
  W-->>C: Success (Fast)
  W-)+R: Async Sync""",
    "eraser": """Client > Write Node: Strong Write
Write Node > Read Node: Sync
Read Node > Write Node: Ack
Write Node > Client: Success
Client > Write Node: Eventual Write
Write Node > Client: Success (Fast) [color: green]
Write Node > Read Node: Async Sync [style: dashed]""",
    "components": [("Acknowledgment","Confirmation of safely written bytes."), ("Fast Return","Skipping the ack wait for speed.")],
    "layout": "Timeline emphasizing the extra latency penalty paid for strong data accuracy."
}, "diagram": """
[Write Node A] ---> [Sync Write Node B] (Strong Consistency)
[Write Node A] - - - (Async replication) - - -> [Node B] (Eventual)
""",
        "flow": "Strong: Write blocks until all replicas confirm. Eventual: Return success instantly, sync in background.",
        "pros": "Strong: Reads always return latest data. Eventual: Low latency writes.",
        "cons": "Strong: High latency writes. Eventual: Reads can return stale data.",
        "tradeoff": "Strict data accuracy (Strong) vs low-latency write performance (Eventual).",
        "questions": "What is read-after-write consistency?",
        "followups": "What is linearizability?",
        "mistake": "Assuming eventual consistency syncs within milliseconds under heavy network partition splits.",
        "trick": "Strong consistency is group chat calls; eventual consistency is sending letters."
    },
    {
        "id": "sys-10",
        "num": "10",
        "section": "Foundations",
        "title": "Horizontal vs Vertical Scaling",
        "def": "Scaling horizontally adds more machines to a system pool; scaling vertically upgrades existing server resources.",
        "why": "Defines the hardware scaling roadmap for growth.",
        "usage": "Upgrading a DB server CPU (Vertical) vs adding API nodes (Horizontal).",
        "diagram_arch_data": {
    "id": "sys-10-arch", "title": "Scaling Vectors", "kind": "ARCHITECTURE",
    "code": """flowchart TB
  subgraph V[\"Vertical (Scale Up)\"]
    S1[\"2 CPU\"]:::svc --> S2[\"64 CPU\"]:::svc
  end
  subgraph H[\"Horizontal (Scale Out)\"]
    S3[\"Server 1\"]:::svc -.-> S4[\"Server 2\"]:::svc -.-> S5[\"Server 3\"]:::svc
  end""",
    "eraser": """// Nodes
Group Vertical {
  2 CPU [icon: server, color: blue]
  64 CPU [icon: database, color: blue]
}
Group Horizontal {
  Server 1 [icon: box, color: green]
  Server 2 [icon: box, color: green]
  Server 3 [icon: box, color: green]
}

// Edges
2 CPU > 64 CPU
Server 1 > Server 2 [style: dashed]
Server 2 > Server 3 [style: dashed]""",
    "components": [("Vertical","Hardware upgrades to existing boxes."), ("Horizontal","Adding identical boxes to a pool.")],
    "layout": "Contrasts a single growing entity against a replicating swarm."
}, "diagram_flow_data": {
    "id": "sys-10-flow", "title": "Downtime vs Auto-Scale", "kind": "REQUEST FLOW",
    "code": """sequenceDiagram
  participant LB as LB
  participant S1 as Server 1
  participant S2 as Server 2
  Note over LB,S2: Horizontal Scale
  LB->>S1: Route
  LB->>S2: Route
  Note over LB,S2: Vertical Scale
  S1->>S1: Shutdown
  S1->>S1: Upgrade CPU
  S1->>S1: Restart (Downtime)""",
    "eraser": """LB > Server 1: Route
LB > Server 2: Route
Server 1 > Server 1: Shutdown [color: red]
Server 1 > Server 1: Upgrade CPU
Server 1 > Server 1: Restart (Downtime) [color: red]""",
    "components": [("Downtime","Vertical scaling requires reboots."), ("Routing","Horizontal scaling uses LB pools.")],
    "layout": "Shows the operational disruption of vertical upgrades vs seamless horizontal scaling."
}, "diagram": """
Vertical:   [Single Server] ---> [Upgraded Large Server]
Horizontal: [Server] ---> [Server] + [Server] + [Server]
""",
        "flow": "Vertical: Shutdown -> Upgrade -> Restart. Horizontal: Spin up node -> Register with Load Balancer.",
        "pros": "Vertical: Zero code change. Horizontal: Infinite scale ceiling.",
        "cons": "Vertical: Strict hardware limits. Horizontal: Complex state sync requirements.",
        "tradeoff": "Simplicity (Vertical) vs scalability limits and high availability (Horizontal).",
        "questions": "When should you scale vertically?",
        "followups": "How does sharding enable horizontal database scaling?",
        "mistake": "Assuming horizontal scaling is free of architectural changes. Application servers must be stateless.",
        "trick": "Vertical is buying a bigger truck; horizontal is hiring a fleet of trucks."
    },
    # ── SECTION 2: NETWORKING ──
    {
        "id": "sys-11",
        "num": "11",
        "section": "Networking",
        "title": "Load Balancer",
        "def": "A device or service that distributes network traffic across a cluster of servers.",
        "why": "Prevents single server overloads and ensures high availability.",
        "usage": "AWS ALB routing web requests to healthy target group instances.",
        "diagram": """
[Client HTTP] ---> [Load Balancer] --+---> [App Server 1] (Healthy)
                                      +---> [App Server 2] (Healthy)
""",
        "flow": "Request arrives -> Health check verifies node status -> Alg routes request.",
        "pros": "Ensures high availability, enables auto-scaling, and manages SSL termination.",
        "cons": "Acts as a single point of failure if not configured redundantly.",
        "tradeoff": "Layer 4 routing (fast, pure TCP) vs Layer 7 routing (slower, path-based parsing).",
        "questions": "What is SSL termination at the load balancer?",
        "followups": "Explain round-robin vs least-connections algorithms.",
        "mistake": "Neglecting health check configurations. Poor health checks route traffic to crashed nodes.",
        "trick": "A load balancer is a traffic cop directing cars to open highway lanes."
    },
    {
        "id": "sys-12",
        "num": "12",
        "section": "Networking",
        "title": "Reverse Proxy",
        "def": "A server that sits in front of backend servers, routing client requests to them.",
        "why": "Protects backend servers, manages SSL, caches static files, and compresses traffic.",
        "usage": "Nginx shielding internal Node.js backend ports from external access.",
        "diagram": """
[Public Web] ---> [Nginx (Reverse Proxy)] ---> [Internal App Port 8080]
                     | (Caches assets)
                     v
                [Local Disk]
""",
        "flow": "Client request -> Proxy filters request -> Fetches from backend -> Returns to client.",
        "pros": "Improves security, enables load balancing, and offloads encryption work.",
        "cons": "Adds an extra network hop, increasing latency slightly.",
        "tradeoff": "Centralized security configurations vs single point of failure risks.",
        "questions": "What is the difference between a forward proxy and a reverse proxy?",
        "followups": "How does Nginx handle static file caching?",
        "mistake": "Exposing internal backend ports directly to the internet, bypassing proxy protections.",
        "trick": "A reverse proxy is a receptionist who receives all packages and forwards them to workers."
    },
    {
        "id": "sys-13",
        "num": "13",
        "section": "Networking",
        "title": "CDN",
        "def": "Content Delivery Network: a geographically distributed group of servers caching content near users.",
        "why": "Minimizes page load latency by serving static assets from edge locations.",
        "usage": "Cloudflare caching website images, videos, and CSS stylesheets globally.",
        "diagram": """
[User in EU] ---> [CDN Edge Server (EU)] (Cache Hit - Fast)
[User in Asia]--> [Origin Server (US)]   (Cache Miss - Slow)
""",
        "flow": "Request static asset -> Check nearest edge cache -> If hit, return; if miss, fetch from origin.",
        "pros": "Speeds up page loads, reduces origin server load, and absorbs DDoS traffic.",
        "cons": "Requires managing cache invalidation configurations.",
        "tradeoff": "Immediate asset deployment (no CDN) vs edge caching speed (requires cache invalidation).",
        "questions": "How does CDN cache invalidation work?",
        "followups": "What is a push vs pull CDN configuration?",
        "mistake": "Caching dynamic HTML pages that contain user-specific session data on edge nodes.",
        "trick": "A CDN is like having local warehouses instead of shipping every package from headquarters."
    },
    {
        "id": "sys-14",
        "num": "14",
        "section": "Networking",
        "title": "API Gateway",
        "def": "A single entry point for client requests, managing routing, auth, rate limiting, and metrics gathering.",
        "why": "Simplifies client integration by centralizing microservices access.",
        "usage": "Kong or AWS API Gateway routing requests to internal microservice nodes.",
        "diagram": """
                     +---> [Auth Service]
[Client] ---> [API Gateway] --+---> [Cart Service]
                     +---> [User Service]
""",
        "flow": "Client request -> Validate JWT token -> Rate limit check -> Route to microservice.",
        "pros": "Centralizes auth, limits server abuse, and handles endpoint routing.",
        "cons": "Increases API hop latency and gateway configuration complexity.",
        "tradeoff": "Decoupled microservice security vs centralized gateway processing overheads.",
        "questions": "How does an API gateway handle service rate limiting?",
        "followups": "Explain API gateway routing vs reverse proxy routing.",
        "mistake": "Placing heavy business processing logic inside the API gateway configuration layer.",
        "trick": "An API gateway is the security desk at a corporate building: check ID and route visitors."
    },
    {
        "id": "sys-15",
        "num": "15",
        "section": "Networking",
        "title": "Service Discovery",
        "def": "The automatic detection of devices and services offered by a computer network.",
        "why": "Allows microservices to locate and connect with each other as IP addresses dynamically scale.",
        "usage": "Consul or Eureka tracking running instances of payment and catalog services.",
        "diagram": """
[Service A] ---> [Registry Database] (Lookup Service B IP)
                     ^
                     | (Registers IP)
[Service B] ---------+
""",
        "flow": "Service starts -> Registers IP with registry -> Senders query registry -> Route directly.",
        "pros": "Enables dynamic auto-scaling without manual configuration updates.",
        "cons": "Adds dependency on registry uptime and sync latencies.",
        "tradeoff": "Dynamic registry lookups (Consul) vs static configuration bindings.",
        "questions": "What is client-side vs server-side service discovery?",
        "followups": "How do heartbeat checks maintain registry integrity?",
        "mistake": "Hardcoding IP addresses in microservice config files instead of using discovery names.",
        "trick": "Service discovery is the yellow pages: lookup contact info before calling."
    },
    {
        "id": "sys-16",
        "num": "16",
        "section": "Networking",
        "title": "DNS Flow",
        "def": "The process of resolving human-readable domain names into machine-readable IP addresses.",
        "why": "Enables web browsers to locate and connect to servers hosting websites.",
        "usage": "Resolving domain 'grindos.pranavx.in' to IP address '192.0.2.1'.",
        "diagram": """
[Browser] ---> [Recursive DNS] ---> [Root Nameserver] ---> [TLD Nameserver]
                                                                  |
[Browser] <--- [IP: 192.0.2.1] <--------- [Authoritative DNS] <---+
""",
        "flow": "Check cache -> Query Root -> Query TLD -> Query Authoritative Nameserver -> Return IP.",
        "pros": "Translates domains, caches lookups, and supports geo-routing.",
        "cons": "Any authoritative DNS outage blocks website access globally.",
        "tradeoff": "Short DNS TTL (fast updates, high query load) vs long DNS TTL (slow updates, cached).",
        "questions": "What is the difference between recursive and authoritative DNS servers?",
        "followups": "What happens when DNS cache poison attacks succeed?",
        "mistake": "Setting long DNS TTLs during server migration windows, delaying IP updates.",
        "trick": "DNS is the contact contact list on your phone: lookup 'Mom' to call her number."
    },
    {
        "id": "sys-17",
        "num": "17",
        "section": "Networking",
        "title": "Caching Basics",
        "def": "A hardware or software component that stores data so future requests can be served faster.",
        "why": "Reduces read latencies and offloads database search compute loads.",
        "usage": "Redis caching user session profiles in application memory.",
        "diagram": """
[App Server] ---> [Cache Store] (Hit: return data - Fast)
[App Server] - - -> [Database]  (Miss: fetch and write to cache - Slow)
""",
        "flow": "Request arrives -> Check cache -> If hit, return; if miss, query DB and populate cache.",
        "pros": "Decreases response times, offloads databases, and handles traffic spikes.",
        "cons": "Adds risk of serving stale data and increases infrastructure complexity.",
        "tradeoff": "Immediate database queries (accurate, slow) vs cached memory lookups (stale risk, fast).",
        "questions": "Explain write-through vs write-behind caching strategies.",
        "followups": "What are cache eviction policies like LRU and LFU?",
        "mistake": "Neglecting to set TTLs (Time-to-Live) on cache keys, causing memory bloat.",
        "trick": "Caching is keeping your frequently used tools on your desk instead of in the toolbox."
    },
    # ── SECTION 3: DATABASES ──
    {
        "id": "sys-18",
        "num": "18",
        "section": "Databases",
        "title": "SQL vs NoSQL",
        "def": "SQL databases are relational and structured; NoSQL databases are non-relational and schema-less.",
        "why": "Guides database technology selection based on data models and scaling needs.",
        "usage": "Postgres (SQL) for financial ledgers; MongoDB (NoSQL) for user profiles.",
        "diagram": """
SQL (Structured Table):  [ID | Name | Email] (Relations enforced)
NoSQL (Document JSON):   { "id": 1, "profile": { "bio": "Hello" } }
""",
        "flow": "SQL: Strict schema parses writes -> join queries. NoSQL: Direct write BSON/JSON -> key lookup.",
        "pros": "SQL: ACID transactions, relational integrity. NoSQL: Horizontal scale, schema flexibility.",
        "cons": "SQL: Harder to scale horizontally. NoSQL: Lacks native relation constraints.",
        "tradeoff": "Relational query safety (SQL) vs schema flexibility and horizontal scale capabilities (NoSQL).",
        "questions": "Explain ACID compliance in relational databases.",
        "followups": "How do NoSQL databases scale horizontally?",
        "mistake": "Using NoSQL when your data models require deep relational queries and foreign key safety.",
        "trick": "SQL is an organized file cabinet; NoSQL is a storage box where you drop items."
    },
    {
        "id": "sys-19",
        "num": "19",
        "section": "Databases",
        "title": "Database Indexing",
        "def": "A database structure that improves the speed of data retrieval operations on a table.",
        "why": "Transforms slow full-table scans into fast index seeks.",
        "usage": "Creating a B-Tree index on a SQL `user_id` column to speed lookups.",
        "diagram": """
Table Scan:  [Scan Row 1] -> [Scan Row 2] -> [Scan Row N] (O(N) - Slow)
Index Seek:  [Root Node] -> [Leaf Node] -> [Target Row]   (O(log N) - Fast)
""",
        "flow": "Parse query -> Check index -> Traverse index tree -> Retrieve matching rows.",
        "pros": "Drastically reduces read latency and scales search operations.",
        "cons": "Slows down write queries (INSERT/UPDATE) and consumes disk storage.",
        "tradeoff": "Faster read performance vs slower write queries and index storage footprints.",
        "questions": "How does a B-Tree index work under the hood?",
        "followups": "What is the difference between a clustered and non-clustered index?",
        "mistake": "Indexing every single column. This bloats storage and degrades write performance.",
        "trick": "An index is the index at the back of a textbook: lookup page numbers directly."
    },
    {
        "id": "sys-20",
        "num": "20",
        "section": "Databases",
        "title": "Replication",
        "def": "The practice of copying data across multiple database servers to ensure reliability and accessibility.",
        "why": "Protects against database server hardware failures and data loss.",
        "usage": "Replicating primary DB transactions to a hot standby standby server.",
        "diagram": """
[App Write] ---> [Primary Database]
                        | (Sync / Async replication)
                        v
                 [Replica Database]
""",
        "flow": "Write commit -> Replicate log -> Replica applies update -> Replicas synced.",
        "pros": "Ensures disaster recovery, high availability, and data redundancy.",
        "cons": "Adds write replication lag and synchronization overhead.",
        "tradeoff": "Synchronous replication (safe, high latency) vs asynchronous replication (fast, data loss risk).",
        "questions": "What is the difference between master-slave and multi-master replication?",
        "followups": "Explain replication lag issues.",
        "mistake": "Assuming replication is a backup. If you run a bad DELETE query, it propagates to all replicas.",
        "trick": "Replication is carbon copying a document: one copy goes in the desk, one in the safe."
    },
    {
        "id": "sys-21",
        "num": "21",
        "section": "Databases",
        "title": "Read Replicas",
        "def": "Database server copies dedicated to serving read queries, offloading the primary database.",
        "why": "Increases system read capacities, allowing scaling of read-heavy systems.",
        "usage": "Directing user dashboard loads to read replicas, reserving write queries for the primary.",
        "diagram": """
                     +---> [Primary Database (Writes)]
[App Router] --------+---> [Read Replica 1 (Reads)]
                     +---> [Read Replica 2 (Reads)]
""",
        "flow": "App detects query type -> Routes select queries to read replicas -> Writes go to primary.",
        "pros": "Scales read query performance and prevents primary server locking.",
        "cons": "Reads can return stale data due to asynchronous replication lag.",
        "tradeoff": "Strict read consistency vs scaled read query throughput capacity.",
        "questions": "How do you handle read-after-write consistency with read replicas?",
        "followups": "What happens if a read replica crashes?",
        "mistake": "Sending write transactions to read replicas. Replicas are read-only and reject updates.",
        "trick": "A read replica is printing multiple copies of a menu so all customers can read at once."
    },
    {
        "id": "sys-22",
        "num": "22",
        "section": "Databases",
        "title": "Sharding",
        "def": "A database partitioning technique that splits a single database across multiple server instances.",
        "why": "Enables horizontal database scaling when single servers hit CPU/storage limits.",
        "usage": "Sharding users by hash ID: Users 1-10k on DB 1; Users 10k-20k on DB 2.",
        "diagram": """
                  +---> [Shard DB 1 (ID: A-M)]
[Shard Router] ---+
                  +---> [Shard DB 2 (ID: N-Z)]
""",
        "flow": "Insert record -> Hash shard key -> Route query directly to matching shard instance.",
        "pros": "Provides infinite database scaling potential and isolated fault zones.",
        "cons": "Precludes running joins across shards and complicates database schemas.",
        "tradeoff": "Single DB server simplicity vs distributed shard database scale capacities.",
        "questions": "What is a hot shard and how do you resolve it?",
        "followups": "Explain range-based vs hash-based sharding.",
        "mistake": "Sharding databases prematurely. It introduces massive query complexity that is hard to revert.",
        "trick": "Sharding is splitting a massive book index into separate alphabetical volume binders."
    },
    {
        "id": "sys-23",
        "num": "23",
        "section": "Databases",
        "title": "Partitioning",
        "def": "Splitting database tables into smaller logical parts within the same database server.",
        "why": "Improves query speeds and maintenance overheads on large tables.",
        "usage": "Partitioning an invoice table by year: `invoices_2025`, `invoices_2026`.",
        "diagram": """
              [Invoice Table (Logical)]
                    /           \\
                   v             v
       [Partition 2025]       [Partition 2026]
""",
        "flow": "Query invoices for 2026 -> Database engine queries partition 2026 directly, skipping 2025 data.",
        "pros": "Accelerates data pruning and query lookups by skipping irrelevant tables.",
        "cons": "Requires table partitions design planning and query tuning.",
        "tradeoff": "Table query simplicity vs table partition file size maintenance.",
        "questions": "What is the difference between horizontal and vertical partitioning?",
        "followups": "How does range partitioning differ from list partitioning?",
        "mistake": "Partitioning tables that have low row counts. This adds directory traversal overheads.",
        "trick": "Partitioning is sorting files into folders by year inside a single cabinet drawer."
    },
    {
        "id": "sys-24",
        "num": "24",
        "section": "Databases",
        "title": "CQRS",
        "def": "Command Query Responsibility Segregation: separating read models from write models.",
        "why": "Optimizes query performance and scaling by isolating write schemas from read indexes.",
        "usage": "Using an event store for writes, replicating to Elasticsearch for searches.",
        "diagram": """
             +---> [Command API] ---> [Write Database]
[Client] ----+                                | (Sync event)
             +---> [Query API] <----- [Read Cache / Search DB]
""",
        "flow": "Submit Command -> Write DB updates -> Sync event triggered -> Read index updated.",
        "pros": "Maximizes read query performances and isolates write transactional logic.",
        "cons": "Increases code complexity and sync lag latency.",
        "tradeoff": "Strict data synchronization (single DB) vs scaled query performance (decoupled CQRS).",
        "questions": "How do you handle sync lag in CQRS architecture?",
        "followups": "What is event sourcing and how does it relate to CQRS?",
        "mistake": "Implementing CQRS on simple CRUD applications. It adds unnecessary infrastructure overhead.",
        "trick": "CQRS is a restaurant kitchen: one group prepares food (write), a waiter delivers plates (read)."
    },
    {
        "id": "sys-25",
        "num": "25",
        "section": "Databases",
        "title": "Eventual Consistency",
        "def": "A consistency model where database replicas eventually sync updates if no new modifications occur.",
        "why": "Allows distributed databases to scale writes without blocking for sync loops.",
        "usage": "Social media likes updates: numbers sync across global user views within seconds.",
        "diagram": """
[Node A (Writes: 10)] - - (Replication delay) - -> [Node B (Reads: 9)]
[Node A (Writes: 10)] ------------ (Sync complete) ------------> [Node B (Reads: 10)]
""",
        "flow": "Update node A -> Node A returns success -> Sync updates background replicas -> Read nodes sync.",
        "pros": "Delivers fast API write performance and high system availability.",
        "cons": "Reads can temporarily return stale data during replication windows.",
        "tradeoff": "Immediate update accuracy (Strong) vs fast write speeds (Eventual).",
        "questions": "How does dynamo-style DB handle eventual consistency?",
        "followups": "Explain conflict resolution (LWW vs CRDT) in eventual consistency.",
        "mistake": "Relying on eventual consistency for bank account transactions, causing overdraft conflicts.",
        "trick": "Eventual consistency is sending mail: updates arrive at different times but eventually sync."
    },
    {
        "id": "sys-26",
        "num": "26",
        "section": "Databases",
        "title": "Distributed Transactions",
        "def": "Transactions that update tables across multiple distributed database nodes.",
        "why": "Enables transaction consistency (ACID) across independent databases.",
        "usage": "A payment service debiting balance in DB 1, while orders DB 2 records purchases.",
        "diagram": """
                    [Coordinator Node]
                     /              \\
         (Prepare?) v                v (Prepare?)
             [Database 1]          [Database 2]
""",
        "flow": "Coordinator sends Prepare -> Nodes vote Yes/No -> If all vote Yes, Coordinator sends Commit.",
        "pros": "Ensures transaction safety across distinct databases.",
        "cons": "Slows writes due to network round-trips and introduces deadlock risks.",
        "tradeoff": "Distributed data consistency (2PC) vs system performance and write availability.",
        "questions": "Explain the Two-Phase Commit (2PC) protocol.",
        "followups": "How does 3PC resolve the coordinator block limitation of 2PC?",
        "mistake": "Relying on 2PC over slow WAN connections, causing transaction timeouts and thread lockups.",
        "trick": "2PC is planning a trip with friends: everyone must say 'Yes' before booking tickets."
    },
    # ── SECTION 4: MESSAGING ──
    {
        "id": "sys-27",
        "num": "27",
        "section": "Messaging",
        "title": "Message Queues",
        "def": "A queue structure buffering messages asynchronously between sender and receiver processes.",
        "why": "Decouples services, manages spikes, and schedules background tasks.",
        "usage": "Pushing image upload paths to RabbitMQ for background resizing tasks.",
        "diagram": """
[App Server] ---> [Message Queue (FIFO)] ---> [Worker Node]
""",
        "flow": "App pushes task -> Queue stores message -> Worker pulls task -> Worker commits completion.",
        "pros": "Ensures background execution reliability and absorbs traffic spikes.",
        "cons": "Introduces sync lag latency and queue infrastructure overheads.",
        "tradeoff": "Synchronous API execution (instant confirmation) vs asynchronous background queues.",
        "questions": "What is the difference between push vs pull worker message queues?",
        "followups": "Explain message delivery guarantees (At-least-once, At-most-once).",
        "mistake": "Neglecting worker scale configurations, causing queue backlogs to grow indefinitely.",
        "trick": "A message queue is the inbox tray on a desk: pile up letters to process in order."
    },
    {
        "id": "sys-28",
        "num": "28",
        "section": "Messaging",
        "title": "Kafka",
        "def": "A distributed, partitioned, replicated commit log service optimized for high-volume streaming.",
        "why": "Enables processing millions of telemetry events per second with high durability.",
        "usage": "Streaming vehicle coordinate updates at Uber to calculate dynamic routes.",
        "diagram": """
[Producer] ---> [Topic Partitions (Log)] ---> [Consumer Group]
                [P1 | P2 | P3] (Offsets)
""",
        "flow": "Producer appends log -> Consumer groups read partition offsets -> Consumer stores progress.",
        "pros": "Delivers massive throughput speeds, persistence, and replayable message offsets.",
        "cons": "Requires ZooKeeper/KRaft deployment setups and complex configurations.",
        "tradeoff": "Complex log replay setups (Kafka) vs simple memory queue networks (RabbitMQ).",
        "questions": "How does Kafka achieve high write performance?",
        "followups": "Explain partition counts in consumer scaling groups.",
        "mistake": "Using Kafka for simple task scheduling where RabbitMQ can handle requirements.",
        "trick": "Kafka is a security tape recording: continuously record events to review or replay."
    },
    {
        "id": "sys-29",
        "num": "29",
        "section": "Messaging",
        "title": "RabbitMQ",
        "def": "A messaging broker implementing Advanced Message Queuing Protocol (AMQP).",
        "why": "Enables complex routing logic between microservices.",
        "usage": "Routing notifications to email/SMS queues using exchange routing keys.",
        "diagram": """
[Publisher] ---> [Exchange] --- (Routing Key) ---> [Queues] ---> [Workers]
""",
        "flow": "Push message to Exchange -> Exchange filters by key -> Enqueue in target queue -> Worker pulls.",
        "pros": "Supports flexible routing configurations and robust delivery confirmations.",
        "cons": "Memory limitations limit storage of large backlogs compared to Kafka.",
        "tradeoff": "Advanced routing configurations vs large message backlog storage limits.",
        "questions": "Explain Direct, Fanout, and Topic exchange routing types.",
        "followups": "How do publisher confirms ensure message delivery?",
        "mistake": "Failing to configure Dead Letter Exchanges, losing failed message payloads.",
        "trick": "RabbitMQ is the post office: sort letters by address and distribute to carrier routes."
    },
    {
        "id": "sys-30",
        "num": "30",
        "section": "Messaging",
        "title": "Pub/Sub",
        "def": "A messaging pattern where publishers categorise messages into classes, without knowledge of subscribers.",
        "why": "Enables real-time event broadcasting to multiple subscribers simultaneously.",
        "usage": "Broadcasting stock price changes to user terminal screen windows.",
        "diagram": """
[Publisher] ---> [Channel (Topic)] --+---> [Subscriber A]
                                     +---> [Subscriber B]
""",
        "flow": "Publish message to channel -> Server duplicates payload -> Broadcasts directly to active subscribers.",
        "pros": "Decouples senders from receivers, scaling messaging lookups.",
        "cons": "Messages are ephemeral; dropped if subscribers are offline.",
        "tradeoff": "Ephemeral live broadcasting (Pub/Sub) vs persistent message queue storage.",
        "questions": "How do you implement persistent delivery patterns in Pub/Sub networks?",
        "followups": "What is the difference between point-to-point and pub/sub messaging?",
        "mistake": "Relying on raw Pub/Sub for critical transactions that require guaranteed delivery.",
        "trick": "Pub/Sub is a radio broadcast: tune in to listen; miss it if you turn off the radio."
    },
    {
        "id": "sys-31",
        "num": "31",
        "section": "Messaging",
        "title": "Event Driven Architecture",
        "def": "A software architecture pattern where services respond to state change events.",
        "why": "Enables loose coupling and asynchronous scaling across microservices.",
        "usage": "Checkout triggers 'OrderPlaced' event; inventory and logistics react.",
        "diagram": """
[Order App] ---> (Event: OrderPlaced) --+---> [Inventory App]
                                         +---> [Shipping App]
""",
        "flow": "State change -> Publish event to bus -> Consumer apps trigger internal routines.",
        "pros": "Decouples microservices, supports extensions, and scales write loads.",
        "cons": "Harder to trace transaction flows and debug consistency issues.",
        "tradeoff": "Asynchronous service autonomy vs synchronous transactional consistency.",
        "questions": "How do you handle distributed trace tracking in event architectures?",
        "followups": "What is eventual consistency handling in event flows?",
        "mistake": "Creating circular event dependency loops, where Event A triggers Event B, triggering Event A.",
        "trick": "Event Driven is a restaurant order slip: kitchen, bar, and billing start processing."
    },
    {
        "id": "sys-32",
        "num": "32",
        "section": "Messaging",
        "title": "Dead Letter Queue",
        "def": "A queue holding message payloads that failed to process successfully.",
        "why": "Prevents faulty payloads from blocking worker thread queues (poison pills).",
        "usage": "Storing corrupt JSON payloads in DLQ for manual developer inspection.",
        "diagram": """
[Worker] ---> [Main Queue] ---> (Fails 3x) ---> [Dead Letter Queue (DLQ)]
""",
        "flow": "Pull job -> Error occurs -> Re-queue -> Hit max retry limit -> Move job to DLQ.",
        "pros": "Prevents queue blocking and isolates corrupt payloads.",
        "cons": "Requires setting up storage, alerts, and manual review routines.",
        "tradeoff": "Instantly deleting failed messages vs storing them for manual investigation (DLQ).",
        "questions": "What causes a message to become a poison pill?",
        "followups": "How do you configure DLQs in RabbitMQ vs SQS?",
        "mistake": "Failing to set alerting thresholds on DLQ sizes, letting failed jobs gather dust.",
        "trick": "A DLQ is the quarantine zone in a lab: isolate dangerous items for safety."
    },
    {
        "id": "sys-33",
        "num": "33",
        "section": "Messaging",
        "title": "Retry Patterns",
        "def": "Design patterns that handle transient service failures by retrying operations.",
        "why": "Enables applications to recover from brief network or external API drops.",
        "usage": "Retrying API calls with exponential backoff on HTTP 503 responses.",
        "diagram": """
[App Server] ---> (Call fails) ---> (Wait: 1s) ---> (Try 2) ---> (Wait: 2s) ---> Success
""",
        "flow": "Call fails -> Calculate backoff delay -> Wait -> Retry -> Limit attempts -> Throw error.",
        "pros": "Increases system resilience and reduces transaction failure rates.",
        "cons": "Can compound server loads if retrying requests indiscriminately.",
        "tradeoff": "Fast failure loops (fail fast) vs resilient retry loops (higher resource locks).",
        "questions": "Why is adding jitter crucial in exponential backoff algorithms?",
        "followups": "What is the difference between transient and permanent errors?",
        "mistake": "Retrying permanent errors (e.g., HTTP 401 Unauthorized), which only drains compute credits.",
        "trick": "Retry is dialing a busy phone number again after waiting a few seconds."
    },
    {
        "id": "sys-34",
        "num": "34",
        "section": "Messaging",
        "title": "Idempotency",
        "def": "The property where making an API call multiple times has the same effect as making it once.",
        "why": "Prevents duplicate charges or transactions on network retry operations.",
        "usage": "Payment APIs using idempotency keys: `idempotency_key = req_uuid`.",
        "diagram": """
[Client] --- (Pay $10, Key: 123) ---> [Payment API] (Processes write)
[Client] --- (Pay $10, Key: 123) ---> [Payment API] (Returns cached success)
""",
        "flow": "Request arrives -> Check key -> If processed, return cached response; if new, execute.",
        "pros": "Ensures transaction safety and prevents duplicate records.",
        "cons": "Requires database storage for idempotency keys.",
        "tradeoff": "Execution speed (no checks) vs duplicate safety (idempotency checks).",
        "questions": "How do you design an idempotency layer for REST APIs?",
        "followups": "What database storage setups work best for idempotency keys?",
        "mistake": "Using volatile memory caches to store idempotency keys, risking key losses on reboots.",
        "trick": "Idempotency is pressing the elevator call button multiple times: the lift still comes once."
    },
    # ── SECTION 5: MICROSERVICES ──
    {
        "id": "sys-35",
        "num": "35",
        "section": "Microservices",
        "title": "Monolith vs Microservices",
        "def": "Monoliths package code in a single executable; microservices split logic into independent services.",
        "why": "Defines system code modularity and team scaling roadmaps.",
        "usage": "Starting with a monolith MVP, splitting into microservices as engineering teams grow.",
        "diagram": """
Monolith:     [Auth | Order | Billing] ---> [Single Database]
Microservices: [Auth Node] -> [DB1] | [Order Node] -> [DB2] | [Billing Node] -> [DB3]
""",
        "flow": "Monolith: In-memory function call. Microservices: Network RPC call over HTTP/gRPC.",
        "pros": "Monolith: Simple setup, fast calls. Microservices: Scale independence, isolated failures.",
        "cons": "Monolith: Scale bottleneck. Microservices: Complex network tracking, data consistency lag.",
        "tradeoff": "Local speed and simplicity (Monolith) vs service independence and scale capabilities (Microservices).",
        "questions": "What is the database-per-service pattern?",
        "followups": "How do microservices communicate efficiently?",
        "mistake": "Migrating to microservices before your database schemas and service boundaries are clearly defined.",
        "trick": "Monolith is a Swiss army knife; microservices are a toolbox of specialized tools."
    },
    {
        "id": "sys-36",
        "num": "36",
        "section": "Microservices",
        "title": "Circuit Breaker",
        "def": "A design pattern that blocks requests to failing services, protecting system resources.",
        "why": "Prevents failing downstream services from creating cascading system timeouts.",
        "usage": "Tripping the payment breaker if payment gateway errors exceed 50% in 1 minute.",
        "diagram": """
[Normal]    [Client] ---> [Circuit Breaker (Closed)] ---> [Payment API]
[Failing]   [Client] ---> [Circuit Breaker (Open)]   -X- [Payment API] (Instantly fails)
""",
        "flow": "Success: Closed state -> Error threshold hit: Open state (block calls) -> Wait -> Half-Open (try calls).",
        "pros": "Prevents cascading failures and enables graceful system degradation.",
        "cons": "Adds fallback logic design and state monitoring complexities.",
        "tradeoff": "Retrying requests (hoping for recovery) vs blocking requests (resilience, instant errors).",
        "questions": "Explain Closed, Open, and Half-Open states in circuit breakers.",
        "followups": "What fallback options work best when a breaker opens?",
        "mistake": "Setting low timeout values on downstream calls, causing the breaker to open on brief spikes.",
        "trick": "A circuit breaker is the fuse box in your house: cuts power to prevent electrical fires."
    },
    {
        "id": "sys-37",
        "num": "37",
        "section": "Microservices",
        "title": "Service Mesh",
        "def": "A dedicated infrastructure layer managing service-to-service network communications.",
        "why": "Offloads networking logic (auth, tracing, routing) from application source code.",
        "usage": "Using Istio sidecar proxies (Envoy) to manage communication between Kubernetes pods.",
        "diagram": """
[Pod Service A] <---> [Sidecar Proxy] ===== (mTLS) =====> [Sidecar Proxy] <---> [Pod Service B]
""",
        "flow": "App request -> Sidecar intercepts -> Resolves IP -> Encrypts tunnel -> Relays to target sidecar.",
        "pros": "Secures communications, provides tracing, and handles retries.",
        "cons": "Increases cluster memory usage and adds deployment complexity.",
        "tradeoff": "Application-level security configs vs infrastructure-level sidecar proxy overheads.",
        "questions": "What is the data plane vs control plane in service mesh architectures?",
        "followups": "How does mTLS secure service communication?",
        "mistake": "Deploying a service mesh on small clusters. It adds unnecessary management complexity.",
        "trick": "A service mesh is having private security guards route and check all visitors in an office."
    },
    {
        "id": "sys-38",
        "num": "38",
        "section": "Microservices",
        "title": "Saga Pattern",
        "def": "A design pattern managing distributed transactions through a sequence of local transactions.",
        "why": "Enables transactional consistency across microservices without database-level write locks.",
        "usage": "Processing orders: charge card -> if catalog fails, trigger compensation refund flow.",
        "diagram": """
[Create Order] ---> [Charge Card] ---> (Fail Catalog Update)
                                            |
[Complete Order] <--- [Refund Card] <-------+ (Compensating Transaction)
""",
        "flow": "Local transaction succeeds -> Trigger next step -> If failure occurs -> Execute compensations.",
        "pros": "Enables consistency without locking databases, supporting microservice autonomy.",
        "cons": "Requires designing compensating transactions for all success steps.",
        "tradeoff": "Distributed consistency (2PC lock) vs eventual transaction consistency (Saga).",
        "questions": "Explain choreography-based vs orchestration-based Sagas.",
        "followups": "How do you handle failures in compensating transaction flows?",
        "mistake": "Believing Sagas are ACID. They only provide eventual consistency, allowing data anomalies.",
        "trick": "Saga is booking a vacation: refund flight ticket if the hotel reservation is rejected."
    },
    {
        "id": "sys-39",
        "num": "39",
        "section": "Microservices",
        "title": "Distributed Tracing",
        "def": "A method used to profile and monitor requests as they traverse distributed services.",
        "why": "Enables debugging latency bottlenecks and error sources across microservices.",
        "usage": "Using Jaeger to trace gateway request delays down to specific database queries.",
        "diagram": """
[Trace: Req-123] ---> [Gateway Node (50ms)]
                           |
                           +---> [User Service Node (120ms)]
                                      |
                                      +---> [Postgres DB (100ms)]
""",
        "flow": "Inject trace ID at gateway -> Propagate header -> Nodes report spans -> Assemble trace path.",
        "pros": "Pinpoints latency bottlenecks and traces distributed system call failures.",
        "cons": "Requires instrumentation overhead and log storage capacity.",
        "tradeoff": "Deep tracing data detail vs performance overheads and log storage costs.",
        "questions": "How does context propagation work in distributed tracing?",
        "followups": "What is the difference between trace ID and span ID?",
        "mistake": "Failing to pass trace headers in asynchronous worker queues, breaking trace links.",
        "trick": "Distributed tracing is GPS tracking a package through all sorting hubs."
    },
    {
        "id": "sys-40",
        "num": "40",
        "section": "Microservices",
        "title": "Rate Limiting",
        "def": "Throttling client requests based on specified resource limits.",
        "why": "Prevents resource starvation, brute-force attacks, and API abuse.",
        "usage": "Limiting public APIs to 100 requests per minute per IP address.",
        "diagram": """
[Incoming Client Requests] ---> [Token Bucket (Size: 10)] ---> Allowed
                                      | (No tokens left)
                                      v
                             [HTTP 429 Rate Limit]
""",
        "flow": "Request arrives -> Check key token balance -> Deduct and process OR return HTTP 429.",
        "pros": "Protects servers, manages API costs, and mitigates DDoS attempts.",
        "cons": "Can block legitimate users during traffic spikes if limits are tight.",
        "tradeoff": "Strict system protection vs flexible user query rate caps.",
        "questions": "Explain Token Bucket vs Leaky Bucket algorithms.",
        "followups": "How do you implement distributed rate limiting using Redis?",
        "mistake": "Storing rate limits in single-node memory arrays. Autoscaling nodes will not sync limits.",
        "trick": "Rate limiting is the ticket gate at a theater: only allow one person through at a time."
    },
    # ── SECTION 6: STORAGE ──
    {
        "id": "sys-41",
        "num": "41",
        "section": "Storage",
        "title": "Object Storage",
        "def": "A storage architecture that manages data as objects, rather than file hierarchies or database blocks.",
        "why": "Enables storing petabytes of unstructured files reliably and cheaply.",
        "usage": "Storing raw user uploads and profile photos on AWS S3.",
        "diagram": """
[Object Metadata (DB)] --+
                         +---> [Object Storage Bucket] (Raw File + ID)
[Client Web Reader] -----+
""",
        "flow": "Write: POST payload -> Storage assigns key -> Write success. Read: Fetch file URL via key.",
        "pros": "Provides horizontal scale capacity, low costs, and high durability.",
        "cons": "Poor search speeds for specific data modifications within objects.",
        "tradeoff": "Relational block search (DB) vs raw file storage scale capacities (Object Store).",
        "questions": "What is the difference between object storage and block storage?",
        "followups": "Explain eventual consistency in object storage updates.",
        "mistake": "Using object storage as an active database, continuously overwriting files.",
        "trick": "Object storage is checking bags at an airport: hand over your bag and receive a ticket tag."
    },
    {
        "id": "sys-42",
        "num": "42",
        "section": "Storage",
        "title": "Blob Storage",
        "def": "Binary Large Object Storage: a service optimized for storing unstructured binary data.",
        "why": "Provides storage systems for large binary media files (videos, audio, backups).",
        "usage": "Azure Blob Storage housing video assets for a media streaming platform.",
        "diagram": """
[App Server] ---> [Blob Storage Client] ---> [Blob Container File Store]
""",
        "flow": "Stream binary chunks -> Assemble file payload -> Store as block blob -> Expose static link.",
        "pros": "Handles large single files and supports data streaming.",
        "cons": "Lacks schema query tools or directory search indexes.",
        "tradeoff": "Structured block partition indexes vs raw binary storage volumes.",
        "questions": "What are block, page, and append blobs?",
        "followups": "How do you secure access to binary storage objects?",
        "mistake": "Storing sensitive corporate documents in public blob containers, exposing links to search indexers.",
        "trick": "Blob storage is a large storage bin: drop in raw materials without packaging."
    },
    {
        "id": "sys-43",
        "num": "43",
        "section": "Storage",
        "title": "File Upload Architecture",
        "def": "An architecture designed to stream, validate, and store user-uploaded files.",
        "why": "Saves server compute resources by offloading file transfer work.",
        "usage": "Using pre-signed S3 URLs so clients upload files directly to cloud storage.",
        "diagram": """
[Client App] ---> [API Gateway] (Request upload url) ---> returns pre-signed url
[Client App] === (Upload direct stream) ===> [Object Storage (S3)]
""",
        "flow": "Request signed URL -> Generate URL with expiration -> Upload file directly to S3 bucket.",
        "pros": "Offloads app servers, prevents memory overflows, and reduces latency.",
        "cons": "Complicates upload validation tracking and metadata writes.",
        "tradeoff": "Direct upload parsing (immediate validation) vs pre-signed direct S3 uploads.",
        "questions": "How do pre-signed URLs protect upload paths?",
        "followups": "How do you handle multi-part file uploads?",
        "mistake": "Buffering file uploads in web server memory, causing processes to crash.",
        "trick": "Pre-signed URL is a delivery pass: allows dropping packages at a warehouse."
    },
    {
        "id": "sys-44",
        "num": "44",
        "section": "Storage",
        "title": "Media Processing",
        "def": "A system architecture that processes, transcodes, and compresses media files.",
        "why": "Optimizes video delivery across varying network connection speeds.",
        "usage": "Transcoding raw video uploads into HLS streams (1080p, 720p, 480p) via workers.",
        "diagram": """
[Upload Bucket] ---> [Transcode Worker] --+---> [1080p Video] ---> [CDN]
                                           +---> [720p Video]
""",
        "flow": "File landing event -> Trigger worker -> Transcode to formats -> Save outputs -> Update metadata.",
        "pros": "Reduces user playback buffering and optimizes CDN delivery costs.",
        "cons": "Consumes heavy worker CPU resource pools and increases storage sizes.",
        "tradeoff": "High transcode cost/storage vs low user playback buffering speeds.",
        "questions": "Explain HLS and DASH streaming protocols.",
        "followups": "How do you optimize background transcode worker queues?",
        "mistake": "Processing video transcoding synchronously inside client-facing HTTP routes.",
        "trick": "Media processing is translating a book into different languages for global distribution."
    },
    {
        "id": "sys-45",
        "num": "45",
        "section": "Storage",
        "title": "Search Architecture",
        "def": "A system optimized to index and search unstructured text across databases.",
        "why": "Delivers fast, ranked query matches that standard databases cannot handle.",
        "usage": "Using Elasticsearch to index and search product catalogs with typo-tolerance.",
        "diagram": """
[App Server] ---> [Search Indexer] ---> [Elasticsearch Cluster]
                     ^
                     | (Sync writes)
[Database DB] -------+
""",
        "flow": "Write to DB -> Push update to Search Index -> Query search index -> Return ranked matches.",
        "pros": "Supports typo tolerance, search relevance scoring, and fast query execution.",
        "cons": "Adds index synchronization lag and double-write overheads.",
        "tradeoff": "Simple database LIKE scans (slow, synchronous) vs Elasticsearch indexing (fast, sync delay).",
        "questions": "How does an inverted index work?",
        "followups": "How do you sync database writes with Elasticsearch indexes?",
        "mistake": "Treating Elasticsearch as your primary database. It does not support ACID transactions.",
        "trick": "Search index is card catalog drawers in a library: find shelf numbers directly."
    },
    # ── SECTION 7: SECURITY ──
    {
        "id": "sys-46",
        "num": "46",
        "section": "Security",
        "title": "Authentication",
        "def": "The process of verifying the identity of a user or system client.",
        "why": "Ensures that users are who they claim to be, preventing access spoofing.",
        "usage": "Verifying user login credentials using salted password hashes.",
        "diagram": """
[Client Credentials] ---> [Auth Server] ---> verify hash ---> return Session JWT
""",
        "flow": "Submit credentials -> Server verifies hash -> Token/Session created -> Return token.",
        "pros": "Protects user accounts and secures API endpoints.",
        "cons": "Requires secure key storage setups and credential management.",
        "tradeoff": "User login convenience (MFA disabled) vs strict system security (MFA enabled).",
        "questions": "What is the difference between authentication and authorization?",
        "followups": "Explain password hashing algorithms like bcrypt.",
        "mistake": "Storing raw passwords in plaintext inside databases. Always salt and hash passwords.",
        "trick": "Authentication is showing your passport at border control to prove your identity."
    },
    {
        "id": "sys-47",
        "num": "47",
        "section": "Security",
        "title": "Authorization",
        "def": "The process of verifying what resources an authenticated user has permission to access.",
        "why": "Prevents users from modifying or viewing data outside their security scope.",
        "usage": "Blocking students from accessing recruiter dashboard API routes.",
        "diagram": """
[User Token] ---> [API Route] ---> (Check role == Admin) ---> Access Granted
""",
        "flow": "Request route -> Parse user role claim -> Verify route access rules -> Approve/Deny.",
        "pros": "Secures data access, supports compliance, and enforces role boundaries.",
        "cons": "Complicates API router logic and database query filters.",
        "tradeoff": "Fine-grained permissions (high management cost) vs simple admin-user roles.",
        "questions": "What is the principle of least privilege?",
        "followups": "How do you enforce authorization in microservice systems?",
        "mistake": "Neglecting backend authorization. Always verify roles on the server, not just on the UI.",
        "trick": "Authorization is using a hotel key card: proves you can enter room 204, but not room 305."
    },
    {
        "id": "sys-48",
        "num": "48",
        "section": "Security",
        "title": "JWT",
        "def": "JSON Web Token: an open standard for securely transmitting information between parties as a JSON object.",
        "why": "Enables stateless user session authentication across microservice clusters.",
        "usage": "Client attaches JWT token header to auth API requests.",
        "diagram": """
JWT Structure: [Header (SHA256)] . [Payload (claims)] . [Signature (HMAC)]
""",
        "flow": "Approve login -> Generate JWT signed with private key -> Client stores token -> Verify signature.",
        "pros": "Stateless verification, offloads database session checks, and works across domains.",
        "cons": "Cannot be easily revoked before expiration limits are reached.",
        "tradeoff": "Stateless API speed (JWT) vs immediate token revocation capacities (Stateful Sessions).",
        "questions": "How do you handle JWT token revocation?",
        "followups": "Explain the difference between JWT access tokens and refresh tokens.",
        "mistake": "Storing sensitive information like user passwords inside the public JWT payload.",
        "trick": "A JWT is a prepaid movie ticket: staff check the signature stamp without looking up database logs."
    },
    {
        "id": "sys-49",
        "num": "49",
        "section": "Security",
        "title": "OAuth",
        "def": "An open standard for authorization, allowing users to share private resources without sharing passwords.",
        "why": "Enables 'Login with Google/GitHub' integrations securely.",
        "usage": "Allowing GrindOS dashboards to load a user's GitHub repository lists.",
        "diagram": """
[App Server] ---> [OAuth Provider] ---> [User Authorizes] ---> [App receives Token]
""",
        "flow": "Redirect to provider -> User logins -> Return authorization code -> Exchange code for token.",
        "pros": "Saves password management costs, improves signup rates, and limits data sharing.",
        "cons": "Requires integration with third-party auth platforms.",
        "tradeoff": "Developing custom identity servers vs relying on external OAuth providers.",
        "questions": "Explain the OAuth 2.0 Authorization Code flow.",
        "followups": "What is OpenID Connect (OIDC)?",
        "mistake": "Failing to validate the state parameter, exposing systems to CSRF login attacks.",
        "trick": "OAuth is valet keys: opens the driver's door and starts the car, but cannot open the glove box."
    },
    {
        "id": "sys-50",
        "num": "50",
        "section": "Security",
        "title": "Session Auth",
        "def": "A stateful authentication method where session records are stored on the server.",
        "why": "Enables immediate session revocation and tight control over active users.",
        "usage": "Storing active session keys in Redis, verifying IDs on every HTTP request.",
        "diagram": """
[Client (Cookie ID)] ---> [Web Node] ---> [Query Redis Session] ---> Access OK
""",
        "flow": "Approve login -> Store session in DB/Redis -> Send session ID cookie -> Verify ID against DB.",
        "pros": "Allows immediate logout revocation, secures session data, and updates permissions instantly.",
        "cons": "Requires database/cache lookups on every request, scaling database loads.",
        "tradeoff": "Immediate session control (Stateful Sessions) vs stateless scale capacities (JWT).",
        "questions": "How does session hijacking occur and how do you prevent it?",
        "followups": "What are secure HttpOnly cookies?",
        "mistake": "Failing to set HttpOnly flags on session cookies, exposing them to XSS script theft.",
        "trick": "Session auth is checking the guest list on every entry to a private party."
    },
    {
        "id": "sys-51",
        "num": "51",
        "section": "Security",
        "title": "RBAC",
        "def": "Role-Based Access Control: restricting system access to authorized users based on roles.",
        "why": "Simplifies permission mapping as corporate organizations scale.",
        "usage": "Assigning roles: `admin`, `recruiter`, `student` to manage dashboard API scopes.",
        "diagram": """
[User] ---> [Assigned: Admin Role] ---> [Inherits permissions: Read, Write, Delete]
""",
        "flow": "Map user to role -> Map role to permissions list -> Check permissions on query execution.",
        "pros": "Simplifies user management and audit tracking loops.",
        "cons": "Lacks flexibility for fine-grained dynamic parameters rules.",
        "tradeoff": "Simple role management setups (RBAC) vs complex context rule configurations (ABAC).",
        "questions": "How do you implement hierarchical roles in RBAC databases?",
        "followups": "What is the difference between roles and permissions?",
        "mistake": "Creating too many specialized roles (role explosion), making permission auditing difficult.",
        "trick": "RBAC is keys based on job titles: all managers get keys to the manager office."
    },
    {
        "id": "sys-52",
        "num": "52",
        "section": "Security",
        "title": "ABAC",
        "def": "Attribute-Based Access Control: evaluating access rules dynamically using attributes.",
        "why": "Enables fine-grained security policies based on context (time, location, department).",
        "usage": "Allowing file access only if: `user.department == document.department` AND `time.hour < 17`.",
        "diagram": """
[User (Sales)] ---> [API Engine] (Check time < 17:00 & Dept == Sales) ---> Access OK
""",
        "flow": "Query route -> Gather attributes (user, resource, environment) -> Evaluate policy rules engine.",
        "pros": "Supports highly detailed access rules and dynamically evaluates context.",
        "cons": "Increases policy evaluation latencies and policy management complexity.",
        "tradeoff": "Strict context security (ABAC) vs system performance and configuration simplicity (RBAC).",
        "questions": "How does XACML define ABAC policies?",
        "followups": "What attributes compile environment contexts in ABAC?",
        "mistake": "Implementing ABAC when simple role checks are sufficient, slowing down API routing.",
        "trick": "ABAC is checking ID, age, local time, and ticket status before entry to an R-rated movie."
    },
    {
        "id": "sys-53",
        "num": "53",
        "section": "Security",
        "title": "Zero Trust",
        "def": "A security framework requiring continuous verification of every user and device, both inside and outside the network.",
        "why": "Prevents lateral movement attacks if perimeter security fails.",
        "usage": "Enforcing mTLS encryption and session validation for all internal microservices.",
        "diagram": """
[Service A] === (mTLS verification + Auth header) ===> [Service B (Verify on every call)]
""",
        "flow": "Request route -> Validate client certificate -> Check token permissions -> Authorize transaction.",
        "pros": "Reduces data breach risk and limits access scope during compromised server events.",
        "cons": "Increases latency profiles and network orchestration complexity.",
        "tradeoff": "Open internal network speeds (perimeter security) vs absolute request verification security (Zero Trust).",
        "questions": "What is lateral movement in network security breaches?",
        "followups": "How do you implement micro-segmentation in Kubernetes?",
        "mistake": "Assuming internal Kubernetes cluster traffic is safe by default, leaving API ports open.",
        "trick": "Zero Trust is checking passenger tickets and ID at every single station during a train ride."
    },
    # ── SECTION 8: OBSERVABILITY ──
    {
        "id": "sys-54",
        "num": "54",
        "section": "Observability",
        "title": "Logging",
        "def": "Recording application events, execution paths, and error stack traces to disk or storage.",
        "why": "Provides historical records to diagnose production crashes and bugs.",
        "usage": "Writing structured JSON logs: `{'level': 'ERROR', 'msg': 'DB connection failed'}`.",
        "diagram": """
[App Engine] ---> [Log Stream (stdout)] ---> [Fluentd Aggregator] ---> [S3 Archive]
""",
        "flow": "Event occurs -> Log output -> Log shipper gathers stream -> Store in search database.",
        "pros": "Essential for auditing, crash investigations, and tracking logic bugs.",
        "cons": "Consumes disk storage and search indexes require maintenance.",
        "tradeoff": "Detailed debug logging (high storage bills) vs minimal log tracking (harder to debug).",
        "questions": "Why are structured logs (JSON) preferred over plaintext strings?",
        "followups": "What are log aggregation pipelines like ELK or EFK?",
        "mistake": "Writing sensitive user data (passwords, credit card numbers) into logs, violating compliance.",
        "trick": "Logging is keeping a detailed diary of everything you did during the work day."
    },
    {
        "id": "sys-55",
        "num": "55",
        "section": "Observability",
        "title": "Monitoring",
        "def": "The real-time observation of system metrics, resource usage, and application health indicators.",
        "why": "Ensures systems are healthy, alerting teams before outages occur.",
        "usage": "Monitoring API error rates and CPU limits across microservice clusters.",
        "diagram": """
[Servers Pool] ---> [Prometheus Collector] ---> [Grafana Metrics Dashboard]
""",
        "flow": "Collect server metrics -> Parse data streams -> Update dashboard views -> Evaluate alert rules.",
        "pros": "Enables proactive warning tracking and keeps system health visible.",
        "cons": "Requires setting up dashboard infrastructures and alert rules.",
        "tradeoff": "Thorough monitoring systems (higher costs) vs minimal health tracking (reactive debug paths).",
        "questions": "What are the four golden signals of monitoring?",
        "followups": "What is black-box vs white-box monitoring?",
        "mistake": "Setting tight alert rules, causing alert fatigue and leading teams to ignore notifications.",
        "trick": "Monitoring is the dashboard gauges on a car: watch fuel levels and engine temp."
    },
    {
        "id": "sys-56",
        "num": "56",
        "section": "Observability",
        "title": "Metrics",
        "def": "Numeric data measurements of system resource usage gathered over time.",
        "why": "Provides quantitative data to identify usage trends and plan hardware expansions.",
        "usage": "Gathering database memory allocations and CPU utilization trends.",
        "diagram": """
Metrics Track:  [CPU Usage: 45%] -> [CPU Usage: 90% (Alert triggered)]
""",
        "flow": "Agent queries CPU/Memory status -> Sends metrics -> Stores as time-series data.",
        "pros": "Supports capacity planning, tracks trends, and enables auto-scaling checks.",
        "cons": "Storing time-series metrics at high resolution increases storage footprints.",
        "tradeoff": "High-frequency metrics gathering (detailed trends) vs low-frequency gathering (reduced storage costs).",
        "questions": "Explain counter, gauge, and histogram metric types.",
        "followups": "What are time-series databases (TSDB)?",
        "mistake": "Failing to index metric tags, slowing down dashboard load query runs.",
        "trick": "Metrics are your smart watch tracking your heart rate throughout the day."
    },
    {
        "id": "sys-57",
        "num": "57",
        "section": "Observability",
        "title": "Alerting",
        "def": "The system process of sending notifications to teams when metrics cross specified safety limits.",
        "why": "Notifies engineering teams of system issues before users experience downtime.",
        "usage": "Alerting Slack channels if API endpoint return times exceed 2 seconds for 5 minutes.",
        "diagram": """
[Metric: Err > 5%] ---> [Alert Rules Evaluator] ---> [PagerDuty PING SMS]
""",
        "flow": "Analyze metric logs -> Threshold crossed -> Queue alert dispatch -> Ring team via SMS/PagerDuty.",
        "pros": "Enables rapid incident response and limits downtime.",
        "cons": "Unconfigured alert rules can trigger false alarms and fatigue teams.",
        "tradeoff": "Immediate pager alerts (resolves issues fast) vs quiet notifications (reduces alert fatigue).",
        "questions": "How do you design a reliable on-call escalation rotation path?",
        "followups": "What causes alert fatigue and how do you resolve it?",
        "mistake": "Sending non-critical warning alerts to on-call phone pages at midnight, burning out engineers.",
        "trick": "Alerting is the smoke detector in your kitchen: rings loudly to warn of fire."
    },
    {
        "id": "sys-58",
        "num": "58",
        "section": "Observability",
        "title": "Tracing",
        "def": "Tracking the execution path of single transactions as they traverse distributed services.",
        "why": "Identifies microservice dependency delays and call bottlenecks.",
        "usage": "Using OpenTelemetry to trace user checkout request paths.",
        "diagram": """
[User Checkout Trace] ---> API Gateway (20ms) -> Cart Service (40ms) -> DB (80ms)
""",
        "flow": "Request arrives -> Inject trace ID header -> Track span durations -> Compile trace tree.",
        "pros": "Pinpoints trace call bottlenecks and maps system dependencies.",
        "cons": "Traces require network transit overhead and log index storages.",
        "tradeoff": "100% trace sampling (detailed logs, high cost) vs 5% request trace sampling (budget friendly).",
        "questions": "How does distributed tracing help debug cascading timeouts?",
        "followups": "What are tracing spans?",
        "mistake": "Sampling 100% of high-volume trace calls, causing log storage costs to skyrocket.",
        "trick": "Tracing is tracking a package through every transit hub using a barcode scanner."
    },
    {
        "id": "sys-59",
        "num": "59",
        "section": "Observability",
        "title": "Prometheus",
        "def": "A time-series monitoring system that pulls metrics from configured targets at regular intervals.",
        "why": "Provides an open-source metric gathering system with query logic (PromQL).",
        "usage": "Configuring Prometheus to scrape metrics from FastAPI app instances every 15 seconds.",
        "diagram": """
[FastAPI Instance (/metrics)] <=== (Scrape pull request) === [Prometheus TSDB]
""",
        "flow": "App exposes `/metrics` page -> Prometheus scrapes page -> Writes data to time-series DB.",
        "pros": "No service-to-service push dependencies, powerful query syntax, and light footprint.",
        "cons": "Scale limitations for storing long-term metrics history without external backends.",
        "tradeoff": "Pull-based scraping (simple setup) vs push-based metrics pipelines (better for ephemeral tasks).",
        "questions": "Explain pull vs push metrics collection paradigms.",
        "followups": "What is PromQL?",
        "mistake": "Relying on Prometheus for long-term data archiving without configuring external stores like Thanos.",
        "trick": "Prometheus is a teacher walking around the class, reading grades from student desks."
    },
    {
        "id": "sys-60",
        "num": "60",
        "section": "Observability",
        "title": "Grafana",
        "def": "An open-source visualization and analytics software system to query and visualize metrics.",
        "why": "Renders metrics databases as readable dashboards.",
        "usage": "Connecting Grafana to Prometheus, displaying live web traffic graphs on office screens.",
        "diagram": """
[Prometheus TSDB] ---> [Grafana Server] ---> [Dashboard Chart (Web UI)]
""",
        "flow": "Query data source -> Parse time-series metrics -> Render chart visuals on browser.",
        "pros": "Connects to multiple data sources, supports alerts, and provides clean dashboards.",
        "cons": "Dashboard management requires maintenance and configuration.",
        "tradeoff": "Custom dashboard creation vs predefined monitoring setups.",
        "questions": "How do you configure dynamic variables inside Grafana dashboards?",
        "followups": "What data sources does Grafana support natively?",
        "mistake": "Creating overly complex dashboards with too many charts, slowing down page loads.",
        "trick": "Grafana is the TV screen showing live charts and graphs in the flight control tower."
    },
    # ── SECTION 9: CASE STUDIES ──
    {
        "id": "sys-61",
        "num": "61",
        "section": "Case Studies",
        "title": "URL Shortener",
        "def": "A system design case study for a service that creates short aliases for long URLs (like tinyurl.com).",
        "why": "Demonstrates capacity estimation, database selections, and unique key generation logic.",
        "usage": "Converting 'https://grindos.pranavx.in/page' into a 7-character string 'tinyurl.com/a7B2x'.",
        "diagram": """
[Long URL] ---> [Base62 Encoder / DB] ---> [Short Key: a7B2x]
[Short Key] ---> [API Gateway / Redis] ---> [HTTP 301 Redirect to Long URL]
""",
        "flow": "Request write -> Check if exists -> Encode with Base62 -> Store in DB -> Return URL.",
        "pros": "Fast lookups using cache, saving database read queries.",
        "cons": "Redirect routes add HTTP network redirect hops for users.",
        "tradeoff": "Base62 conversion on write vs pre-generating unique keys in a registry database.",
        "questions": "Why choose Base62 encoding over Base64 encoding for URL paths?",
        "followups": "How do you handle redirect routing using HTTP 301 vs 302 statuses?",
        "mistake": "Pre-generating unique keys using databases without unique constraint checks, risking duplicate key collision bugs.",
        "trick": "A URL shortener is a coat check ticket: exchange your big coat for a small plastic tag."
    },
    {
        "id": "sys-62",
        "num": "62",
        "section": "Case Studies",
        "title": "WhatsApp",
        "def": "Designing a real-time messaging system supporting chat, delivery indicators, and group conversations.",
        "why": "Demonstrates real-time WebSocket scaling, connection mapping, and message queuing.",
        "usage": "Orchestrating messages across millions of mobile client applications globally.",
        "diagram": """
[Client A] ---> [WS Connection Node A] ---> [Message Bus] ---> [WS Node B] ---> [Client B]
                     |                                           |
                     +---> [User Session DB]                     +---> [Redis Cache]
""",
        "flow": "Client connects -> Map socket to node -> Send message -> Route to target node -> Push push notifications if offline.",
        "pros": "Low latency message delivery, offline queue sync, and secure connections.",
        "cons": "Managing persistent TCP socket states drains server memory resources.",
        "tradeoff": "Stateful persistent WebSockets vs stateless HTTP requests polling.",
        "questions": "How do you scale WebSocket servers to support millions of active connections?",
        "followups": "How do you handle chat indicators (delivered, read) asynchronously?",
        "mistake": "Storing chat history in central SQL tables without partitioning, slowing queries.",
        "trick": "WhatsApp is a post office sorting room: route messages directly to active carrier routes."
    },
    {
        "id": "sys-63",
        "num": "63",
        "section": "Case Studies",
        "title": "Instagram Feed",
        "def": "Designing a social media feed system supporting photo uploads, user follows, and dynamic home page feeds.",
        "why": "Demonstrates hybrid feed generation models (push vs pull) for active user groups.",
        "usage": "Generating home page content feeds for millions of active social media users.",
        "diagram": """
[User Post] ---> [Feed Fanout Engine] --+---> [Follower A Feed Cache]
                                         +---> [Follower B Feed Cache]
""",
        "flow": "Post photo -> Write metadata -> Fanout to follower cache lists -> Render feed on login.",
        "pros": "Delivers fast feed load times by pre-computing layouts.",
        "cons": "Fanout writes scale quadratically for users with high follower counts.",
        "tradeoff": "Pre-computed push models (fast reads, slow writes) vs pull query systems (slow reads, fast writes).",
        "questions": "How do you handle celebrity posts (celebrity problem) in feed generation?",
        "followups": "Explain feed cache eviction strategies.",
        "mistake": "Running dynamic relational join queries on feed loads, crashing databases under active use.",
        "trick": "Instagram feed is printing newspaper copies: print early so users read instantly."
    },
    {
        "id": "sys-64",
        "num": "64",
        "section": "Case Studies",
        "title": "YouTube",
        "def": "Designing a video streaming platform supporting uploads, transcoding, and video recommendations.",
        "why": "Demonstrates blob storage management, transcode queues, and CDN delivery networks.",
        "usage": "Delivering video content to global audiences across varying network configurations.",
        "diagram": """
[Raw Video] ---> [Transcode Cluster] --+---> [1080p Video File] ---> [Cloud CDN]
                                       +---> [720p Video File]
""",
        "flow": "Upload raw file -> Queue transcode task -> Slice video into chunks -> Transcode formats -> Push to CDN.",
        "pros": "Optimizes playback performance, reducing user buffering times.",
        "cons": "Requires massive storage volumes and expensive transcode workers.",
        "tradeoff": "Higher transcode server costs vs low client playback buffering latency.",
        "questions": "Why are video files split into chunks during transcoding?",
        "followups": "How do recommendations engines load dynamic suggestion feeds?",
        "mistake": "Exposing primary storage buckets to direct client downloads, bypassing CDN cache nodes.",
        "trick": "YouTube is a translator: translates raw text into multiple languages for regional readers."
    },
    {
        "id": "sys-65",
        "num": "65",
        "section": "Case Studies",
        "title": "Uber",
        "def": "Designing a ride-sharing dispatch system mapping dynamic coordinates and matching riders with drivers.",
        "why": "Demonstrates geospatial database indexing, coordinate streaming, and match algorithms.",
        "usage": "Matching active passenger ride requests with nearby drivers in under 2 seconds.",
        "diagram": """
[Driver Coordinates] ---> [Geospatial Index (H3/Quadtree)] <--- [Passenger Query]
                                      |
                                      v
                             [Match Engine Run]
""",
        "flow": "Stream coordinates -> Update location index -> Request ride -> Query nearby drivers -> Dispatch.",
        "pros": "Provides real-time dispatch matching, low connection latency, and dynamic pricing.",
        "cons": "High write traffic strains memory database clusters.",
        "tradeoff": "Real-time dispatch accuracy vs memory database compute costs.",
        "questions": "Explain spatial indexing models: Quadtree vs Google S2 vs Uber H3.",
        "followups": "How do you handle coordinate update bottlenecks?",
        "mistake": "Using flat SQL queries with mathematical range calculations to locate drivers, slowing database runs.",
        "trick": "Uber is a dispatcher with a map: group coordinates by grid sections to find nearest drivers."
    },
    {
        "id": "sys-66",
        "num": "66",
        "section": "Case Studies",
        "title": "Zomato",
        "def": "Designing a food delivery platform matching restaurants, drivers, and delivery routes.",
        "why": "Demonstrates search path filtering, route calculations, and order transactions.",
        "usage": "Routing order requests to restaurants and delivery drivers in real-time.",
        "diagram": """
[Restaurant menu] ---> [Catalog Cache] ---> [User Order App]
                                                  |
[Driver App] <--- [Routing Engine] <--------------+ (Match driver to restaurant)
""",
        "flow": "User checkout -> DB transaction write -> Match driver -> Dispatch driver -> Track route.",
        "pros": "Structured catalog lookup caching, fast order dispatch routes.",
        "cons": "Route calculations consume high server CPU capacities.",
        "tradeoff": "Accurate dynamic route updates vs server calculate latencies.",
        "questions": "How do you scale catalog cache databases under high check traffic?",
        "followups": "How does order status tracking sync across clients?",
        "mistake": "Directly querying primary databases for menu catalogs, slowing check transactions.",
        "trick": "Zomato is a dispatcher coordinating food pickup and delivery routes."
    },
    {
        "id": "sys-67",
        "num": "67",
        "section": "Case Studies",
        "title": "Google Drive",
        "def": "Designing a file cloud storage and synchronization system supporting file uploads and edit syncs.",
        "why": "Demonstrates block storage slice logic, sync engines, and metadata databases.",
        "usage": "Storing and synchronizing files across multiple user devices.",
        "diagram": """
[Local File Change] ---> [Local Sync App] (Slice blocks) -> POST metadata
[File Blocks Store] <=== (Stream chunks) === [Object Storage (S3)]
""",
        "flow": "Divide file into chunks -> Compare hashes -> Upload mutated blocks only -> Update database records.",
        "pros": "Reduces upload file transfer costs and minimizes storage space.",
        "cons": "Splitting files requires complex block assembly processes on reads.",
        "tradeoff": "Simple file replacement uploads vs block-level differential updates.",
        "questions": "Why divide files into block-level chunks for storage?",
        "followups": "How do block indexes optimize file synchronizations?",
        "mistake": "Uploading full documents on minor edits, draining user data limits.",
        "trick": "Google Drive is building modular homes: only ship modified parts to the site."
    },
    {
        "id": "sys-68",
        "num": "68",
        "section": "Case Studies",
        "title": "Notification System",
        "def": "Designing a multi-channel notification platform delivering SMS, email, and push alerts.",
        "why": "Demonstrates message queuing, provider integration, and rate limiting.",
        "usage": "Dispatching verification codes, newsletters, and order status alerts to users.",
        "diagram": """
[Trigger Event] ---> [API Gateway] ---> [BullMQ Queue] ---> [Worker Node] ---> [Twilio API]
""",
        "flow": "Ingest request -> Push task to queue -> Worker reads task -> Call delivery provider API.",
        "pros": "Ensures message delivery, scales write volumes, and isolates network calls.",
        "cons": "Delivery delays can occur under queue backlog surges.",
        "tradeoff": "Immediate synchronous API calls vs asynchronous background queues.",
        "questions": "How do you prevent duplicate alerts on message retry loops?",
        "followups": "Explain notification provider fallback routines.",
        "mistake": "Calling notification APIs inline, causing main application thread delays.",
        "trick": "A notification system is a call center: queue requests and delegate calls to workers."
    },
    {
        "id": "sys-69",
        "num": "69",
        "section": "Case Studies",
        "title": "Chat System",
        "def": "Designing a real-time messaging system supporting private chats and online status tracking.",
        "why": "Demonstrates WebSocket scaling, message queues, and session caching.",
        "usage": "Broadcasting messages across active user chat window channels in real-time.",
        "diagram": """
[Client A] ---> [WS Socket Node] ---> [Redis Pub/Sub] ---> [WS Node B] ---> [Client B]
""",
        "flow": "Client connects -> Bind socket to server -> Send message -> Redis routes to host -> Deliver.",
        "pros": "Sub-100ms message delivery and real-time status tracking.",
        "cons": "High memory consumption on socket server connection limits.",
        "tradeoff": "Stateless polling vs stateful persistent WebSockets.",
        "questions": "How do you scale user online status databases under high traffic?",
        "followups": "How do you handle message delivery confirmations?",
        "mistake": "Storing transient chat message details directly in relational DB tables, slowing system writes.",
        "trick": "A chat system is a telephone exchange: route lines directly between callers."
    },
    {
        "id": "sys-70",
        "num": "70",
        "section": "Case Studies",
        "title": "Rate Limiter",
        "def": "Designing a system to limit HTTP request rates based on IP addresses or API keys.",
        "why": "Demonstrates low-latency memory stores, token buckets, and sliding window designs.",
        "usage": "Protecting payment endpoints by restricting transactions to 5 per minute per card.",
        "diagram": """
[Client Request] ---> [Redis Key Counter] (Check count < limit) ---> Allow
                               | (Limit exceeded)
                               v
                     [HTTP 429 Rate Limit]
""",
        "flow": "Check IP key in Redis -> If count < limit, increment and allow; if limit reached, reject request.",
        "pros": "Protects APIs from denial-of-service spikes and cost drains.",
        "cons": "Adds key lookup network latency hops to request paths.",
        "tradeoff": "Token bucket algorithms (burst support) vs leaky bucket algorithms (smooth traffic).",
        "questions": "Explain sliding window counter rate limiting algorithms.",
        "followups": "How do you coordinate rate limits across server clusters?",
        "mistake": "Running rate limiter key reads on primary SQL databases, causing performance drops.",
        "trick": "A rate limiter is a security bouncer: only allow guests inside at a safe pace."
    },
    # ── SECTION 10: INTERVIEW FRAMEWORK ──
    {
        "id": "sys-71",
        "num": "71",
        "section": "Interview Framework",
        "title": "Requirement Gathering",
        "def": "The step in system design interviews to clarify ambiguities and define functional and non-functional requirements.",
        "why": "Prevents building the wrong system and outlines design bounds.",
        "usage": "Asking: 'How many daily active users?' and 'Should reads be real-time?' before planning.",
        "diagram": """
[Interview Start] ---> [Gather Functional Requirements] ---> [Define Latency & SLA Bounds]
""",
        "flow": "Ask clarifying questions -> Define inputs/outputs -> Write out requirements list.",
        "pros": "Ensures design targets match expectations and avoids layout changes later.",
        "cons": "Reduces actual design time if discussions drag.",
        "tradeoff": "Thorough requirements discussions vs early design phase starts.",
        "questions": "What questions define non-functional SLA requirements?",
        "followups": "How do you prioritize requirements during time limits?",
        "mistake": "Assuming requirements without asking. This shows poor developer communication.",
        "trick": "Requirement gathering is getting blue-prints from a client before building."
    },
    {
        "id": "sys-72",
        "num": "72",
        "section": "Interview Framework",
        "title": "Capacity Estimation",
        "def": "Calculating system scale bounds (storage, memory, network bandwidth) during interview planning.",
        "why": "Identifies system bottlenecks and guides database and hardware sizing choices.",
        "usage": "Calculating storage needs: `10M active users * 100 bytes = 1GB storage per day`.",
        "diagram": """
[Daily Active Users] ---> [Write RPS Check] ---> [Calculate Daily Storage size]
""",
        "flow": "Identify usage count -> Estimate average row size -> Calculate bandwidth and storage sizes.",
        "pros": "Justifies database scaling design decisions with concrete data.",
        "cons": "Calculations can be inaccurate if estimate metrics are off.",
        "tradeoff": "Accurate precision calculations vs quick, realistic range approximations.",
        "questions": "How do you calculate network bandwidth limits?",
        "followups": "Explain standard memory size bounds for caching.",
        "mistake": "Failing to convert raw metrics to standard sizes (e.g., converting bits to bytes).",
        "trick": "Capacity estimation is budget planning: estimate costs before buying furniture."
    },
    {
        "id": "sys-73",
        "num": "73",
        "section": "Interview Framework",
        "title": "API Design",
        "def": "Defining the REST/gRPC endpoints, request structures, and HTTP response codes for a system.",
        "why": "Establishes clear communication contracts between clients and backend servers.",
        "usage": "Designing route: `POST /v1/trips` with JSON request body parameters.",
        "diagram": """
Route: POST /v1/trips  ===> Payload: { "title": "Trip" }  ===> Return: HTTP 201 Created
""",
        "flow": "Define HTTP method -> Outline route path -> Define JSON schema -> Match response codes.",
        "pros": "Creates clean integration contracts, reducing implementation bugs.",
        "cons": "Changing APIs later requires backward compatibility configurations.",
        "tradeoff": "REST API simplicity vs gRPC performance and payload size advantages.",
        "questions": "What HTTP status codes represent user authentication issues?",
        "followups": "Explain idempotency keys inside API header definitions.",
        "mistake": "Using generic HTTP 200 codes for error events, complicating client-side error handling.",
        "trick": "API design is drawing up a contract: define terms before signing."
    },
    {
        "id": "sys-74",
        "num": "74",
        "section": "Interview Framework",
        "title": "Database Design",
        "def": "Selecting databases and designing table schemas, indices, and data paths.",
        "why": "Ensures transaction safety, data integrity, and query performance.",
        "usage": "Mapping relational tables, setting indexes, and outlining sharding strategies.",
        "diagram": """
[Schema Definition] ---> [Relational Keys Mapping] ---> [Query Index Optimization]
""",
        "flow": "Choose DB type -> Define table columns -> Set relations -> Identify index keys.",
        "pros": "Ensures data normalization, preventing search latencies.",
        "cons": "Data migration planning is complex if schema needs update.",
        "tradeoff": "Relational SQL normalizations vs NoSQL document read performance.",
        "questions": "When should you denormalize database schemas?",
        "followups": "How do composite indexes optimize query runs?",
        "mistake": "Neglecting index placement on foreign key columns, causing table join slowdowns.",
        "trick": "Database design is laying foundation blocks: build solid layers first."
    },
    {
        "id": "sys-75",
        "num": "75",
        "section": "Interview Framework",
        "title": "Bottleneck Analysis",
        "def": "Identifying performance bottlenecks and scaling constraints in system layouts.",
        "why": "Prevents system failures under high concurrent user loads.",
        "usage": "Analyzing database connections pool metrics during traffic spikes.",
        "diagram": """
[Load: 10k req] ---> API (Fast) ---> Queue (Fast) ---> [Database (Slow - Bottleneck)]
""",
        "flow": "Load test nodes -> Monitor queue backlogs -> Trace latency -> Identify slow queries.",
        "pros": "Enables proactive performance tuning, preventing production drops.",
        "cons": "Tracing bottlenecks requires monitoring infrastructure.",
        "tradeoff": "System performance checks vs application feature delivery velocity.",
        "questions": "How do you detect database query locks?",
        "followups": "What metrics indicate CPU bus limitations?",
        "mistake": "Assuming scaling memory limits resolves database write bottlenecks.",
        "trick": "Bottleneck analysis is locating traffic jams on highway maps."
    },
    {
        "id": "sys-76",
        "num": "76",
        "section": "Interview Framework",
        "title": "Scaling Strategy",
        "def": "Designing the scalability roadmap to transition from single instances to distributed clusters.",
        "why": "Enables systems to scale smoothly under increasing user demands.",
        "usage": "Integrating load balancers, caching, and database read-replicas.",
        "diagram": """
[Single Web Node] ---> [Scaled Load Balancers + Web Cluster + Replicas]
""",
        "flow": "Deploy web nodes -> Set autoscaling limits -> Route cache queries -> Add DB replicas.",
        "pros": "Handles high user concurrency, providing system resilience.",
        "cons": "Increases server orchestration and deployment infrastructure bills.",
        "tradeoff": "Proactive auto-scaling configurations vs on-demand resource provisioning costs.",
        "questions": "How does DNS routing optimize global system scaling?",
        "followups": "What are scaling issues in microservice messaging queues?",
        "mistake": "Scaling server pools before optimizing database query run configurations.",
        "trick": "Scaling strategy is adding engines to trains: pull heavier loads safely."
    },
    {
        "id": "sys-77",
        "num": "77",
        "section": "Interview Framework",
        "title": "Tradeoff Discussion",
        "def": "Analyzing the pros and cons of system choices during architectural evaluations.",
        "why": "Demonstrates engineering judgment and reasoning over blind technology choices.",
        "usage": "Comparing SQL ACID consistency benefits against NoSQL horizontal write performance.",
        "diagram": """
Choice A (Consistent, Slow) <=== [Tradeoff Balanced Line] ===> Choice B (Eventual, Fast)
""",
        "flow": "Identify option parameters -> List advantages/disadvantages -> Choose based on SLAs.",
        "pros": "Ensures choices match SLA parameters, preventing design regressions.",
        "cons": "Requires deep understanding of technology architectures.",
        "tradeoff": "Strict data security models vs API response latency profiles.",
        "questions": "What tradeoffs define database selection decisions?",
        "followups": "How does latency relate to system consistency choices?",
        "mistake": "Claiming a technology choice has 'zero drawbacks'. Every design choice has tradeoffs.",
        "trick": "Tradeoff discussion is buying a house: balance price, location, and space."
    },
    {
        "id": "sys-78",
        "num": "78",
        "section": "Interview Framework",
        "title": "Common Mistakes",
        "def": "Identifying and avoiding critical design anti-patterns during system planning.",
        "why": "Prevents architectural flaws that cause production crashes or data loss.",
        "usage": "Avoiding single points of failure (SPOF) in load balancer configurations.",
        "diagram": """
Bad:  [App Node] ---> [Single Database Instance] (SPOF)
Good: [App Node] ---> [Primary DB] ---> [Replica Standby DB]
""",
        "flow": "Review system layout -> Identify single points of failure -> Apply redundant design logic.",
        "pros": "Reduces system crash risks and builds durable architectures.",
        "cons": "Increases system design planning time requirements.",
        "tradeoff": "Simple fast layouts vs highly resilient redundant designs.",
        "questions": "What system configurations cause split-brain issues?",
        "followups": "Explain N+1 query patterns in ORM databases.",
        "mistake": "Failing to set timeouts on external API connections, locking server threads.",
        "trick": "Common mistakes is knowing where potholes are on roads to drive safely."
    },
    {
        "id": "sys-79",
        "num": "79",
        "section": "Interview Framework",
        "title": "Interview Framework",
        "def": "The step-by-step structure to navigate system design interviews in under 45 minutes.",
        "why": "Ensures all key design areas (requirements, APIs, databases, scaling) are covered systematically.",
        "usage": "Allocating: 5m requirements -> 10m API/schema -> 15m design -> 10m scaling.",
        "diagram": """
[Requirements: 5m] -> [API & DB: 10m] -> [High-Level Design: 15m] -> [Scaling: 10m]
""",
        "flow": "Gather requirements -> Estimate capacity -> Design APIs -> Draw architecture -> Analyze scaling.",
        "pros": "Prevents running out of time and ensures comprehensive design reviews.",
        "cons": "Requires strict time management during discussion loops.",
        "tradeoff": "Deep dive discussion details vs complete system overview delivery.",
        "questions": "How do you recover if you go off-track during interviews?",
        "followups": "What questions confirm interviewer alignment?",
        "mistake": "Jumping straight into drawing databases before clarifying requirements.",
        "trick": "Interview framework is a flight checklist: verify all points before taking off."
    },
    {
        "id": "sys-80",
        "num": "80",
        "section": "Interview Framework",
        "title": "Top 100 Questions",
        "def": "A list of high-yield system design interview questions and model answers.",
        "why": "Prepares candidates to answer common architectural design questions confidently.",
        "usage": "Reviewing questions on load balancing, caching, databases, and microservices.",
        "diagram": """
[Review Questions Pool] ---> [Practice Mock Interviews] ---> [Interview Readiness]
""",
        "flow": "Read question -> Draft solution -> Compare with model answer -> Review tradeoffs.",
        "pros": "Builds system design confidence and covers common edge cases.",
        "cons": "Requires consistent practice and study time.",
        "tradeoff": "Rote memorization of answers vs understanding core system design principles.",
        "questions": "What are the most common database scaling questions?",
        "followups": "How do you explain service mesh configurations clearly?",
        "mistake": "Giving generic answers without context. Always tailor your design to the problem's SLAs.",
        "trick": "Preparation is studying past maps before embarking on a journey."
    }
]

# RENDER INDIVIDUAL PAGES
content_pages_html = ""
current_page_idx = 5
total_pages_count = 240

# ROADMAP & INTRODUCTION PAGES (PAGE 2, 3, 4)
roadmap_intro_pages = f"""
<div class="page" id="sys-intro-1">
  <div class="header">
    <div class="header-left">
      <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
      <div class="header-wordmark">GrindOS</div>
    </div>
    <div class="header-right">
      <div class="header-badge">INTRODUCTION</div>
    </div>
  </div>
  
  <div style="padding: 24px 30px; flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 14px;">
    <h2 style="font-size: 20pt; font-weight: 800; color: #111; border-bottom: 2px solid #EA763F; padding-bottom: 6px;">System Design Foundations</h2>
    <p style="font-size: 9.5pt; color: #4A5568; line-height: 1.5;">This handbook serves as a comprehensive guide to system design, transitioning from core fundamentals to interview readiness. We organize the content into 10 structured sections covering networking, databases, messaging, microservices, storage, security, observability, case studies, and interview frameworks.</p>
    
    <div style="display: flex; flex-direction: column; gap: 10px;">
      <div style="background:#FFF5F0; border-left: 4px solid #EA763F; padding: 10px; border-radius: 4px;">
        <strong style="color: #EA763F; font-size: 10pt;">System Architecture &amp; Scalability</strong>
        <p style="font-size: 8.5pt; color: #4A5568; margin-top: 2px;">Understanding tradeoffs between consistency and availability (CAP theorem), horizontal and vertical scaling, and caching architectures.</p>
      </div>
      
      <div style="background:#F7FAFC; border-left: 4px solid #4A5568; padding: 10px; border-radius: 4px;">
        <strong style="color: #2D3748; font-size: 10pt;">Microservice Orchestrations</strong>
        <p style="font-size: 8.5pt; color: #4A5568; margin-top: 2px;">Tracing requests across distributed services, applying circuit breakers, service meshes, rate limiting, and event-driven queues.</p>
      </div>
    </div>
  </div>
  
  <div class="footer">
    <div class="footer-left">
      <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
      <div class="breadcrumb">GrindOS <span>›</span> System Design <span>›</span> <span>Intro</span></div>
    </div>
    <div class="page-number-premium">PAGE 02 / 85</div>
  </div>
</div>

<div class="page" id="sys-intro-2">
  <div class="header">
    <div class="header-left">
      <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
      <div class="header-wordmark">GrindOS</div>
    </div>
    <div class="header-right">
      <div class="header-badge">TOC PART 1</div>
    </div>
  </div>
  
  <div style="padding: 24px 30px; flex: 1; display: flex; flex-direction: column; justify-content: center;">
    <h2 style="font-size: 18pt; font-weight: 800; color: #111; border-bottom: 2px solid #EA763F; padding-bottom: 4px; margin-bottom: 12px;">Index: Foundations to Messaging</h2>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; font-size: 8pt; line-height: 1.4;">
      <div>
        <strong style="color: #EA763F; font-size: 9pt; display: block; border-bottom: 1px solid #EBE5DB; margin-bottom: 4px;">Section 1: Foundations</strong>
        <ul style="list-style: none;">
          <li>• 01. What Is System Design <span style="color:#A0AEC0;">........</span> Page 05</li>
          <li>• 02. Scalability <span style="color:#A0AEC0;">.................</span> Page 06</li>
          <li>• 03. Availability <span style="color:#A0AEC0;">................</span> Page 07</li>
          <li>• 04. Reliability <span style="color:#A0AEC0;">.................</span> Page 08</li>
          <li>• 05. Fault Tolerance <span style="color:#A0AEC0;">.............</span> Page 09</li>
          <li>• 06. Latency <span style="color:#A0AEC0;">.....................</span> Page 10</li>
          <li>• 07. Throughput <span style="color:#A0AEC0;">..................</span> Page 11</li>
          <li>• 08. CAP Theorem <span style="color:#A0AEC0;">.................</span> Page 12</li>
          <li>• 09. Consistency Models <span style="color:#A0AEC0;">...........</span> Page 13</li>
          <li>• 10. Horizontal vs Vertical <span style="color:#A0AEC0;">........</span> Page 14</li>
        </ul>
        
        <strong style="color: #2D3748; font-size: 9pt; display: block; border-bottom: 1px solid #EBE5DB; margin-top: 8px; margin-bottom: 4px;">Section 2: Networking</strong>
        <ul style="list-style: none;">
          <li>• 11. Load Balancer <span style="color:#A0AEC0;">...............</span> Page 15</li>
          <li>• 12. Reverse Proxy <span style="color:#A0AEC0;">................</span> Page 16</li>
          <li>• 13. CDN <span style="color:#A0AEC0;">..........................</span> Page 17</li>
          <li>• 14. API Gateway <span style="color:#A0AEC0;">.................</span> Page 18</li>
          <li>• 15. Service Discovery <span style="color:#A0AEC0;">...........</span> Page 19</li>
          <li>• 16. DNS Flow <span style="color:#A0AEC0;">.....................</span> Page 20</li>
          <li>• 17. Caching Basics <span style="color:#A0AEC0;">...............</span> Page 21</li>
        </ul>
      </div>
      
      <div>
        <strong style="color: #718096; font-size: 9pt; display: block; border-bottom: 1px solid #EBE5DB; margin-bottom: 4px;">Section 3: Databases</strong>
        <ul style="list-style: none;">
          <li>• 18. SQL vs NoSQL <span style="color:#A0AEC0;">................</span> Page 22</li>
          <li>• 19. Database Indexing <span style="color:#A0AEC0;">............</span> Page 23</li>
          <li>• 20. Replication <span style="color:#A0AEC0;">.................</span> Page 24</li>
          <li>• 21. Read Replicas <span style="color:#A0AEC0;">...............</span> Page 25</li>
          <li>• 22. Sharding <span style="color:#A0AEC0;">....................</span> Page 26</li>
          <li>• 23. Partitioning <span style="color:#A0AEC0;">................</span> Page 27</li>
          <li>• 24. CQRS <span style="color:#A0AEC0;">........................</span> Page 28</li>
          <li>• 25. Eventual Consistency <span style="color:#A0AEC0;">........</span> Page 29</li>
          <li>• 26. Distributed Transactions <span style="color:#A0AEC0;">.....</span> Page 30</li>
        </ul>
        
        <strong style="color: #4A5568; font-size: 9pt; display: block; border-bottom: 1px solid #EBE5DB; margin-top: 8px; margin-bottom: 4px;">Section 4: Messaging</strong>
        <ul style="list-style: none;">
          <li>• 27. Message Queues <span style="color:#A0AEC0;">..............</span> Page 31</li>
          <li>• 28. Kafka <span style="color:#A0AEC0;">.........................</span> Page 32</li>
          <li>• 29. RabbitMQ <span style="color:#A0AEC0;">......................</span> Page 33</li>
          <li>• 30. Pub/Sub <span style="color:#A0AEC0;">.......................</span> Page 34</li>
          <li>• 31. Event Driven Architecture <span style="color:#A0AEC0;">.....</span> Page 35</li>
          <li>• 32. Dead Letter Queue <span style="color:#A0AEC0;">............</span> Page 36</li>
          <li>• 33. Retry Patterns <span style="color:#A0AEC0;">...............</span> Page 37</li>
          <li>• 34. Idempotency <span style="color:#A0AEC0;">..................</span> Page 38</li>
        </ul>
      </div>
    </div>
  </div>
  
  <div class="footer">
    <div class="footer-left">
      <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
      <div class="breadcrumb">GrindOS <span>›</span> Index <span>›</span> <span>Part 1</span></div>
    </div>
    <div class="page-number-premium">PAGE 03 / 85</div>
  </div>
</div>

<div class="page" id="sys-intro-3">
  <div class="header">
    <div class="header-left">
      <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
      <div class="header-wordmark">GrindOS</div>
    </div>
    <div class="header-right">
      <div class="header-badge">TOC PART 2</div>
    </div>
  </div>
  
  <div style="padding: 24px 30px; flex: 1; display: flex; flex-direction: column; justify-content: center;">
    <h2 style="font-size: 18pt; font-weight: 800; color: #111; border-bottom: 2px solid #EA763F; padding-bottom: 4px; margin-bottom: 12px;">Index: Microservices to Interview Framework</h2>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; font-size: 8pt; line-height: 1.4;">
      <div>
        <strong style="color: #EA763F; font-size: 9pt; display: block; border-bottom: 1px solid #EBE5DB; margin-bottom: 4px;">Section 5: Microservices</strong>
        <ul style="list-style: none;">
          <li>• 35. Monolith vs Microservices <span style="color:#A0AEC0;">...</span> Page 39</li>
          <li>• 36. Circuit Breaker <span style="color:#A0AEC0;">............</span> Page 40</li>
          <li>• 37. Service Mesh <span style="color:#A0AEC0;">...............</span> Page 41</li>
          <li>• 38. Saga Pattern <span style="color:#A0AEC0;">...............</span> Page 42</li>
          <li>• 39. Distributed Tracing <span style="color:#A0AEC0;">.........</span> Page 43</li>
          <li>• 40. Rate Limiting <span style="color:#A0AEC0;">..............</span> Page 44</li>
        </ul>
        
        <strong style="color: #2D3748; font-size: 9pt; display: block; border-bottom: 1px solid #EBE5DB; margin-top: 8px; margin-bottom: 4px;">Section 6: Storage</strong>
        <ul style="list-style: none;">
          <li>• 41. Object Storage <span style="color:#A0AEC0;">..............</span> Page 45</li>
          <li>• 42. Blob Storage <span style="color:#A0AEC0;">................</span> Page 46</li>
          <li>• 43. File Upload Architecture <span style="color:#A0AEC0;">.....</span> Page 47</li>
          <li>• 44. Media Processing <span style="color:#A0AEC0;">............</span> Page 48</li>
          <li>• 45. Search Architecture <span style="color:#A0AEC0;">...........</span> Page 49</li>
        </ul>
        
        <strong style="color: #718096; font-size: 9pt; display: block; border-bottom: 1px solid #EBE5DB; margin-top: 8px; margin-bottom: 4px;">Section 7: Security</strong>
        <ul style="list-style: none;">
          <li>• 46. Authentication <span style="color:#A0AEC0;">.............</span> Page 50</li>
          <li>• 47. Authorization <span style="color:#A0AEC0;">..............</span> Page 51</li>
          <li>• 48. JWT <span style="color:#A0AEC0;">.........................</span> Page 52</li>
          <li>• 49. OAuth <span style="color:#A0AEC0;">.......................</span> Page 53</li>
          <li>• 50. Session Auth <span style="color:#A0AEC0;">................</span> Page 54</li>
          <li>• 51. RBAC <span style="color:#A0AEC0;">........................</span> Page 55</li>
          <li>• 52. ABAC <span style="color:#A0AEC0;">........................</span> Page 56</li>
          <li>• 53. Zero Trust <span style="color:#A0AEC0;">.................</span> Page 57</li>
        </ul>
      </div>
      
      <div>
        <strong style="color: #4A5568; font-size: 9pt; display: block; border-bottom: 1px solid #EBE5DB; margin-bottom: 4px;">Section 8: Observability</strong>
        <ul style="list-style: none;">
          <li>• 54. Logging <span style="color:#A0AEC0;">..................</span> Page 58</li>
          <li>• 55. Monitoring <span style="color:#A0AEC0;">...................</span> Page 59</li>
          <li>• 56. Metrics <span style="color:#A0AEC0;">......................</span> Page 60</li>
          <li>• 57. Alerting <span style="color:#A0AEC0;">.....................</span> Page 61</li>
          <li>• 58. Tracing <span style="color:#A0AEC0;">......................</span> Page 62</li>
          <li>• 59. Prometheus <span style="color:#A0AEC0;">...................</span> Page 63</li>
          <li>• 60. Grafana <span style="color:#A0AEC0;">......................</span> Page 64</li>
        </ul>
        
        <strong style="color: #2F855A; font-size: 9pt; display: block; border-bottom: 1px solid #EBE5DB; margin-top: 8px; margin-bottom: 4px;">Section 9: Case Studies</strong>
        <ul style="list-style: none;">
          <li>• 61. URL Shortener <span style="color:#A0AEC0;">...............</span> Page 65</li>
          <li>• 62. WhatsApp <span style="color:#A0AEC0;">....................</span> Page 66</li>
          <li>• 63. Instagram Feed <span style="color:#A0AEC0;">.............</span> Page 67</li>
          <li>• 64. YouTube <span style="color:#A0AEC0;">.....................</span> Page 68</li>
          <li>• 65. Uber <span style="color:#A0AEC0;">........................</span> Page 69</li>
          <li>• 66. Zomato <span style="color:#A0AEC0;">......................</span> Page 70</li>
          <li>• 67. Google Drive <span style="color:#A0AEC0;">.................</span> Page 71</li>
          <li>• 68. Notification System <span style="color:#A0AEC0;">..........</span> Page 72</li>
          <li>• 69. Chat System <span style="color:#A0AEC0;">..................</span> Page 73</li>
          <li>• 70. Rate Limiter <span style="color:#A0AEC0;">.................</span> Page 74</li>
        </ul>
        
        <strong style="color: #6B46C1; font-size: 9pt; display: block; border-bottom: 1px solid #EBE5DB; margin-top: 8px; margin-bottom: 4px;">Section 10: Framework</strong>
        <ul style="list-style: none;">
          <li>• 71. Requirement Gathering <span style="color:#A0AEC0;">.......</span> Page 75</li>
          <li>• 72. Capacity Estimation <span style="color:#A0AEC0;">........</span> Page 76</li>
          <li>• 73. API Design <span style="color:#A0AEC0;">..................</span> Page 77</li>
          <li>• 74. Database Design <span style="color:#A0AEC0;">.............</span> Page 78</li>
          <li>• 75. Bottleneck Analysis <span style="color:#A0AEC0;">..........</span> Page 79</li>
          <li>• 76. Scaling Strategy <span style="color:#A0AEC0;">............</span> Page 80</li>
          <li>• 77. Tradeoff Discussion <span style="color:#A0AEC0;">...........</span> Page 81</li>
          <li>• 78. Common Mistakes <span style="color:#A0AEC0;">..............</span> Page 82</li>
          <li>• 79. Interview Framework <span style="color:#A0AEC0;">..........</span> Page 83</li>
          <li>• 80. Top 100 Questions <span style="color:#A0AEC0;">............</span> Page 84</li>
        </ul>
      </div>
    </div>
  </div>
  
  <div class="footer">
    <div class="footer-left">
      <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
      <div class="breadcrumb">GrindOS <span>›</span> Index <span>›</span> <span>Part 2</span></div>
    </div>
    <div class="page-number-premium">PAGE 04 / 85</div>
  </div>
</div>
"""

# CONSTRUCT 80 CONTENT PAGES (3 pages per topic)
for t in topics_data:
    # ── PAGE 1: OVERVIEW & GRIDS ──
    page_1 = f'''
<div class="page" id="{t['id']}-p1">
  <div class="header">
    <div class="header-left">
      <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
      <div class="header-wordmark">GrindOS</div>
    </div>
    <div class="header-right">
      <div class="badge-yield">🔥 HIGH YIELD</div>
      <div class="header-badge">{t['section'].upper()}</div>
    </div>
  </div>
  
  <div class="topic-bar">
    <div class="topic-bar-top">
      <div class="topic-eyebrow">Topic {t['num']} &mdash; {t['section']}</div>
      <div class="yield-rating">Yield: <span class="stars-gold">★★★★★</span></div>
    </div>
    <div class="topic-title">{t['title']}</div>
  </div>
  
  <div class="body-container-sysdesign" style="flex:1; display:flex; flex-direction:column; gap:20px;">
    
    <div class="sysdesign-top-grid">
      <div class="sysdesign-card">
        <div class="sysdesign-card-title">📖 Definition &amp; Why It Exists</div>
        <p><strong>Definition:</strong> {t['def']}</p>
        <p style="margin-top: 4px;"><strong>Why It Exists:</strong> {t['why']}</p>
      </div>
      <div class="sysdesign-card">
        <div class="sysdesign-card-title">🌐 Real World Usage &amp; Tradeoff</div>
        <p><strong>Usage:</strong> {t['usage']}</p>
        <p style="margin-top: 4px;"><strong>Trade-off:</strong> {t['tradeoff']}</p>
      </div>
    </div>
    
    <div style="flex:1;"></div>

    <div class="sysdesign-bottom-placement-grid" style="min-height: 250px;">
      <div class="sysdesign-placement-block block-mistake">
        <div class="sysdesign-placement-block-title">⚠️ Common Mistake</div>
        <div>{t['mistake']}</div>
      </div>
      <div class="sysdesign-placement-block block-trap">
        <div class="sysdesign-placement-block-title">🛑 Interviewer Trap</div>
        <div>{t['questions']}</div>
      </div>
      <div class="sysdesign-placement-block block-followups">
        <div class="sysdesign-placement-block-title">🔄 Top Follow-Up</div>
        <div>{t['followups']}</div>
      </div>
      <div class="sysdesign-placement-block block-trick">
        <div class="sysdesign-placement-block-title">💡 Memory Trick</div>
        <div>{t['trick']}</div>
      </div>
    </div>
  </div>
  
  <div class="footer">
    <div class="footer-left">
      <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
      <div class="breadcrumb">GrindOS <span>›</span> {t['section']} <span>›</span> <span>{t['title']}</span></div>
    </div>
    <div class="page-number-premium">PAGE {str(current_page_idx).zfill(2)} / {total_pages_count}</div>
  </div>
</div>
'''
    content_pages_html += page_1
    current_page_idx += 1

    # ── PAGE 2: ARCHITECTURE DOSSIER ──
    arch_diag = t.get('diagram_arch_data', {})
    if arch_diag:
        page_2 = f'''
<div class="page" id="{t['id']}-p2">
  <div class="header">
    <div class="header-left">
      <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
      <div class="header-wordmark">GrindOS</div>
    </div>
    <div class="header-right">
      <div class="header-badge">ARCHITECTURE SPEC</div>
    </div>
  </div>
  
  <div style="padding: 16px 24px; flex: 1; display: flex; flex-direction: column; overflow: hidden; background: #FAF8F5;">
    {b_diagram(arch_diag)}
    {b_dossier(arch_diag)}
  </div>
  
  <div class="footer">
    <div class="footer-left">
      <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
      <div class="breadcrumb">GrindOS <span>›</span> {t['section']} <span>›</span> <span>{t['title']} (Architecture)</span></div>
    </div>
    <div class="page-number-premium">PAGE {str(current_page_idx).zfill(2)} / {total_pages_count}</div>
  </div>
</div>
'''
        content_pages_html += page_2
        current_page_idx += 1

    # ── PAGE 3: REQUEST FLOW DOSSIER ──
    flow_diag = t.get('diagram_flow_data', {})
    if flow_diag:
        page_3 = f'''
<div class="page" id="{t['id']}-p3">
  <div class="header">
    <div class="header-left">
      <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
      <div class="header-wordmark">GrindOS</div>
    </div>
    <div class="header-right">
      <div class="header-badge">REQUEST FLOW SPEC</div>
    </div>
  </div>
  
  <div style="padding: 16px 24px; flex: 1; display: flex; flex-direction: column; overflow: hidden; background: #FAF8F5;">
    {b_diagram(flow_diag)}
    {b_dossier(flow_diag)}
    <div style="margin-top: 12px; padding: 12px; background: #fff; border: 1px solid #EBE5DB; border-radius: 4px; font-size: 8.5pt; color: #2D3748;">
      <p style="margin-bottom: 6px;"><strong>Request Flow:</strong> {t['flow']}</p>
      <p style="margin-bottom: 6px; color: #2F855A;"><strong>Pros:</strong> {t['pros']}</p>
      <p style="color: #C53030;"><strong>Cons:</strong> {t['cons']}</p>
    </div>
  </div>
  
  <div class="footer">
    <div class="footer-left">
      <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
      <div class="breadcrumb">GrindOS <span>›</span> {t['section']} <span>›</span> <span>{t['title']} (Request Flow)</span></div>
    </div>
    <div class="page-number-premium">PAGE {str(current_page_idx).zfill(2)} / {total_pages_count}</div>
  </div>
</div>
'''
        content_pages_html += page_3
        current_page_idx += 1

# COVER PAGE (PAGE 1)
cover_page = f"""
<div class="page cover-page" id="sys-cover">
  <div class="cover-logo-container">
    <img src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS">
  </div>
  <div class="cover-eyebrow">GrindOS Flagship Series</div>
  <div class="cover-title">System Design<br>Handbook</div>
  <div class="cover-subtitle">From Fundamentals to Interview Readiness</div>
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
  .cover-subtitle {{ font-size: 16pt; color: #666; font-weight: 600; margin-bottom: 60px; }}
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
  .topic-bar {{ padding: 8px 24px; border-bottom: 1px solid #EDE5D8; background: #FCFAF7; flex-shrink: 0; margin-left: 5mm; margin-right: 5mm; }}
  .topic-bar-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px; }}
  .topic-eyebrow {{ font-size: 8pt; font-weight: 800; color: #EA763F; text-transform: uppercase; letter-spacing: 1px; }}
  .yield-rating {{ font-size: 8pt; font-weight: 700; color: #718096; }}
  .stars-gold {{ color: #DD6B20; font-weight: 800; }}
  .topic-title {{ font-size: 15pt; font-weight: 800; color: #111; letter-spacing: -0.5px; }}

  /* BODY CONTAINER (L3) */
  .body-container-sysdesign {{
    flex: 1;
    overflow: hidden;
    padding: 10px 16px;
    margin-left: 5mm;
    margin-right: 5mm;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}

  /* DESIGN CARDS & GRIDS */
  .sysdesign-top-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }}
  .sysdesign-card {{ border: 1px solid #EBE5DB; border-radius: 6px; padding: 8px 10px; background: #FCFAF7; }}
  .sysdesign-card-title {{ font-size: 8pt; font-weight: 800; color: #EA763F; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.5px; }}
  .sysdesign-card p {{ font-size: 7.5pt; line-height: 1.35; color: #2D3748; }}

  .sysdesign-mid-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; flex: 1; min-height: 0; overflow: hidden; }}
  .sysdesign-diagram-box {{ border: 1px solid #CBD5E0; border-radius: 6px; padding: 8px; background: #2D3748; color: #F7FAFC; display: flex; flex-direction: column; min-height: 0; overflow: hidden; }}
  .sysdesign-diagram-box .sysdesign-card-title {{ color: #FFF; }}
  .sysdesign-ascii-diag {{ font-family: monospace; font-size: 6.5pt; line-height: 1.25; white-space: pre-wrap; overflow-y: auto; flex: 1; margin-top: 4px; }}
  .sysdesign-flow-box {{ border: 1px solid #EBE5DB; border-radius: 6px; padding: 8px 10px; background: #FFFFFF; font-size: 7.5pt; line-height: 1.35; color: #2D3748; }}

  /* PLACEMENT GRID (L4) */
  .sysdesign-bottom-placement-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 6px;
    padding: 8px;
    background: #FDFBF7;
    border-top: 2px solid #EBE5DB;
    flex-shrink: 0;
    min-height: 100px;
    max-height: 110px;
  }}
  .sysdesign-placement-block {{
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 7.5pt;
    line-height: 1.3;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .sysdesign-placement-block-title {{
    font-size: 7pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 1px;
  }}
  .block-mistake {{ background: #FFF5F5; border-left: 3px solid #E53E3E; color: #742A2A; }}
  .block-mistake .sysdesign-placement-block-title {{ color: #C53030; }}
  .block-trap {{ background: #FFF5F0; border-left: 3px solid #EA763F; color: #7B341E; }}
  .block-trap .sysdesign-placement-block-title {{ color: #DD6B20; }}
  .block-followups {{ background: #F5EBFE; border-left: 3px solid #805AD5; color: #553C9A; }}
  .block-followups .sysdesign-placement-block-title {{ color: #6B46C1; }}
  .block-trick {{ background: #F0FFF4; border-left: 3px solid #38A169; color: #276749; }}
  .block-trick .sysdesign-placement-block-title {{ color: #2F855A; }}

  /* FOOTER (L5) */
  .footer {{ width: 100%; height: 36px; background: white; border-top: 1px solid #EDE5D8; display: flex; justify-content: space-between; align-items: center; padding: 0 24px; font-size: 8.5pt; color: #718096; flex-shrink: 0; font-weight: 700; margin-bottom: 5mm; margin-left: 5mm; margin-right: 5mm; }}
  .footer-left {{ display: flex; align-items: center; gap: 8px; }}
  .footer-logo {{ height: 14px; }}
  .breadcrumb {{ color: #A0AEC0; }}
  .breadcrumb span {{ color: #4A5568; font-weight: 800; margin: 0 4px; }}
  .page-number-premium {{ font-size: 8.5pt; font-weight: 800; color: #EA763F; letter-spacing: 1px; background: #FFF5F0; padding: 3px 10px; border-radius: 4px; border: 1px solid #FBD38D; }}

  /* NOTES LINES FOR BLANK PAGES */
  .notes-lines {{
    flex: 1;
    background-image: linear-gradient(#E2E8F0 1px, transparent 1px);
    background-size: 100% 24px;
    margin-top: 10px;
  }}
"""

# BLANK NOTES PAGES (Page 85)
blank_notes_pages = f"""
  <div class="page" id="sys-notes-1">
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
      <div style="font-size: 16pt; font-weight: 800; color: #111; border-bottom: 2px solid #EA763F; padding-bottom: 6px; margin-bottom: 12px;">Personal Notes &amp; System Designs</div>
      <div class="notes-lines" style="flex: 1; background-image: linear-gradient(#E2E8F0 1px, transparent 1px); background-size: 100% 24px; line-height: 24px; margin-top: 10px;"></div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> System Design <span>›</span> <span>Notes</span> <span style="font-size:7.5pt; color:#A0AEC0; font-weight:normal; margin-left:10px;">grindos.pranavx.in</span></div>
      </div>
      <div class="page-number-premium">PAGE 85 / 85</div>
    </div>
  </div>
"""

# COMPILE FINAL HTML TEMPLATE
html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>System Design Handbook</title>
<style>{css}</style>
</head>
<body>
  <!-- COVER PAGE -->
  {cover_page}
  
  <!-- ROADMAP & TOC PAGES -->
  {roadmap_intro_pages}
  
  <!-- CONTENT PAGES -->
  {content_pages_html}

  <!-- BLANK NOTES PAGE -->
  {blank_notes_pages}
  {_mermaid_runtime()}
</body>
</html>
"""

# Write output HTML file
os.makedirs("subjects/system_design", exist_ok=True)
output_path = "subjects/system_design/01_system_design.html"
with open(output_path, "w") as f:
    f.write(html_out)

print(f"Successfully generated System Design Handbook with {current_page_idx} pages.")

