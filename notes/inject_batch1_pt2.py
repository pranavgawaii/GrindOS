import re

with open("make_handbook_system_design.py", "r") as f:
    content = f.read()

def replace_topic_data(topic_id, arch_data, flow_data):
    global content
    pattern = r'(\{\s*"id":\s*"' + topic_id + r'".*?)("diagram":\s*""")'
    replacement = r'\1"diagram_arch_data": ' + arch_data + r', "diagram_flow_data": ' + flow_data + r', \2'
    content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)

# 6. Latency
arch_6 = """{
    "id": "sys-06-arch", "title": "CDN Edge Caching Architecture", "kind": "ARCHITECTURE",
    "code": "flowchart LR\\n  U([Client]):::client\\n  CDN[\\\"Edge CDN\\\"]:::svc\\n  SRV[\\\"Origin Server\\\"]:::svc\\n  DB[(\\\"Database\\\")]:::data\\n  U -->|10ms| CDN\\n  CDN -->|Miss: 50ms| SRV\\n  SRV -->|10ms| DB",
    "eraser": "// Nodes\\nClient [icon: smartphone, color: orange]\\nEdge CDN [icon: server, color: blue]\\nOrigin Server [icon: server, color: blue]\\nDatabase [icon: database, color: green]\\n\\n// Edges\\nClient > Edge CDN [label: 10ms]\\nEdge CDN > Origin Server [label: Cache Miss, style: dashed]\\nOrigin Server > Database [label: 10ms]",
    "components": [("Edge Node","Geographically close caching server."), ("Origin","Source of truth handling dynamic requests.")],
    "layout": "Linear progression demonstrating physical distance impacts on network time."
}"""
flow_6 = """{
    "id": "sys-06-flow", "title": "Cache Miss Sequence", "kind": "REQUEST FLOW",
    "code": "sequenceDiagram\\n  participant C as Client\\n  participant CDN as Edge Server\\n  participant SRV as Origin\\n  C->>CDN: Request\\n  CDN-->>C: Cache Hit (Fast)\\n  C->>CDN: Request 2\\n  CDN->>SRV: Cache Miss (Network)\\n  SRV-->>C: Response (Slow)",
    "eraser": "Client > Edge Server: Request\\nEdge Server > Client: Cache Hit (Fast) [color: green]\\nClient > Edge Server: Request 2\\nEdge Server > Origin: Cache Miss (Network) [color: red]\\nOrigin > Client: Response (Slow)",
    "components": [("Cache Hit","Instant return from memory."), ("Cache Miss","Blocking network trip to origin server.")],
    "layout": "Contrasts the immediate turnaround of a hit vs the multi-hop delay of a miss."
}"""
replace_topic_data("sys-06", arch_6, flow_6)

# 7. Throughput
arch_7 = """{
    "id": "sys-07-arch", "title": "High Throughput Batching", "kind": "ARCHITECTURE",
    "code": "flowchart TB\\n  IN[\\\"Incoming: 10k RPS\\\"]:::client\\n  Q[[\\\"Queue Buffer\\\"]]:::queue\\n  subgraph SC[\\\"Server Cluster\\\"]\\n    W1[\\\"Worker 1\\\"]:::svc\\n    W2[\\\"Worker 2\\\"]:::svc\\n  end\\n  DB[(\\\"Database\\\")]:::data\\n  IN --> Q\\n  Q --> SC\\n  SC -->|Processed: 9k RPS| DB\\n  IN -.->|1k dropped| Drop",
    "eraser": "// Nodes\\nIncoming [icon: download, color: orange]\\nQueue Buffer [icon: list, color: yellow]\\nGroup Server Cluster {\\n  Worker 1 [icon: box, color: blue]\\n  Worker 2 [icon: box, color: blue]\\n}\\nDatabase [icon: database, color: green]\\n\\n// Edges\\nIncoming > Queue Buffer\\nQueue Buffer > Worker 1\\nQueue Buffer > Worker 2\\nWorker 1 > Database\\nWorker 2 > Database",
    "components": [("Buffer","Absorbs immediate volume."), ("Worker Pool","Parallel processors draining queue.")],
    "layout": "Funnel architecture showing massive input converging through parallel processors."
}"""
flow_7 = """{
    "id": "sys-07-flow", "title": "Parallel Queue Draining", "kind": "REQUEST FLOW",
    "code": "sequenceDiagram\\n  participant IN as Traffic\\n  participant Q as Queue\\n  participant W as Workers\\n  IN->>Q: Enqueue requests\\n  Q->>W: Pull batches\\n  W->>W: Process batch\\n  W-->>Q: Ack completion",
    "eraser": "Traffic > Queue: Enqueue requests\\nQueue > Workers: Pull batches\\nWorkers > Workers: Process batch\\nWorkers > Queue: Ack completion",
    "components": [("Batching","Grouping records for DB efficiency."), ("Parallelism","Simultaneous execution threads.")],
    "layout": "Shows asynchronous ingestion disconnected from processing speeds."
}"""
replace_topic_data("sys-07", arch_7, flow_7)

# 8. CAP Theorem
arch_8 = """{
    "id": "sys-08-arch", "title": "CAP Theorem Tradeoffs", "kind": "ARCHITECTURE",
    "code": "flowchart TB\\n  subgraph CAP[\\\"Distributed Tradeoffs\\\"]\\n    C[\\\"Consistency\\\"]\\n    A[\\\"Availability\\\"]\\n    P[\\\"Partition Tolerance\\\"]\\n  end\\n  C ---|CP: Postgres| P\\n  A ---|AP: Cassandra| P\\n  C ---|CA: Single Node| A",
    "eraser": "// Nodes\\nConsistency [icon: check-circle, color: blue]\\nAvailability [icon: activity, color: green]\\nPartition Tolerance [icon: alert-triangle, color: red]\\n\\n// Edges\\nConsistency - Partition Tolerance [label: CP]\\nAvailability - Partition Tolerance [label: AP]\\nConsistency - Availability [label: CA]",
    "components": [("Consistency","All reads receive the most recent write."), ("Availability","Every request receives a valid response.")],
    "layout": "Triangle matrix showing the impossibility of achieving all three vertices."
}"""
flow_8 = """{
    "id": "sys-08-flow", "title": "Network Partition Resolution", "kind": "REQUEST FLOW",
    "code": "sequenceDiagram\\n  participant C as Client\\n  participant N1 as Node 1\\n  participant N2 as Node 2\\n  Note over N1,N2: Network Split (P)\\n  C->>N1: Write Data\\n  N1--xN2: Sync fails\\n  Note over N1: CP: Reject Write\\n  Note over N1: AP: Accept Write",
    "eraser": "Client > Node 1: Write Data\\nNode 1 > Node 2: Sync fails [color: red]\\nNode 1 > Client: CP: Reject Write [color: red]\\nNode 1 > Client: AP: Accept Write [color: green]",
    "components": [("Network Split","Communication break between nodes."), ("Reject","System stops to maintain accuracy.")],
    "layout": "Demonstrates the forced choice when a network line is severed."
}"""
replace_topic_data("sys-08", arch_8, flow_8)

# 9. Consistency Models
arch_9 = """{
    "id": "sys-09-arch", "title": "Strong vs Eventual Consistency", "kind": "ARCHITECTURE",
    "code": "flowchart TB\\n  C([Client]):::client\\n  subgraph STRONG[\\\"Strong\\\"]\\n    W1[\\\"Write Node\\\"]:::svc ===|Sync lock| R1[\\\"Read Node\\\"]:::svc\\n  end\\n  subgraph EVENTUAL[\\\"Eventual\\\"]\\n    W2[\\\"Write Node\\\"]:::svc -.-|Async replica| R2[\\\"Read Node\\\"]:::svc\\n  end\\n  C --> STRONG & EVENTUAL",
    "eraser": "// Nodes\\nClient [icon: user, color: orange]\\nGroup Strong {\\n  W1 [icon: edit, color: blue]\\n  R1 [icon: eye, color: blue]\\n}\\nGroup Eventual {\\n  W2 [icon: edit, color: green]\\n  R2 [icon: eye, color: green]\\n}\\n\\n// Edges\\nClient > W1\\nClient > W2\\nW1 > R1 [label: Sync lock]\\nW2 > R2 [label: Async replica, style: dashed]",
    "components": [("Sync Lock","Blocks returns until replication completes."), ("Async Replica","Returns immediately, replicates later.")],
    "layout": "Side-by-side comparison of synchronous blocking vs asynchronous background tasks."
}"""
flow_9 = """{
    "id": "sys-09-flow", "title": "Consistency Timing", "kind": "REQUEST FLOW",
    "code": "sequenceDiagram\\n  participant C as Client\\n  participant W as Write Node\\n  participant R as Read Node\\n  C->>W: Strong Write\\n  W->>R: Sync\\n  R-->>W: Ack\\n  W-->>C: Success\\n  C->>W: Eventual Write\\n  W-->>C: Success (Fast)\\n  W-)+R: Async Sync",
    "eraser": "Client > Write Node: Strong Write\\nWrite Node > Read Node: Sync\\nRead Node > Write Node: Ack\\nWrite Node > Client: Success\\nClient > Write Node: Eventual Write\\nWrite Node > Client: Success (Fast) [color: green]\\nWrite Node > Read Node: Async Sync [style: dashed]",
    "components": [("Acknowledgment","Confirmation of safely written bytes."), ("Fast Return","Skipping the ack wait for speed.")],
    "layout": "Timeline emphasizing the extra latency penalty paid for strong data accuracy."
}"""
replace_topic_data("sys-09", arch_9, flow_9)

# 10. Horizontal vs Vertical
arch_10 = """{
    "id": "sys-10-arch", "title": "Scaling Vectors", "kind": "ARCHITECTURE",
    "code": "flowchart TB\\n  subgraph V[\\\"Vertical (Scale Up)\\\"]\\n    S1[\\\"2 CPU\\\"]:::svc --> S2[\\\"64 CPU\\\"]:::svc\\n  end\\n  subgraph H[\\\"Horizontal (Scale Out)\\\"]\\n    S3[\\\"Server 1\\\"]:::svc -.-> S4[\\\"Server 2\\\"]:::svc -.-> S5[\\\"Server 3\\\"]:::svc\\n  end",
    "eraser": "// Nodes\\nGroup Vertical {\\n  2 CPU [icon: server, color: blue]\\n  64 CPU [icon: database, color: blue]\\n}\\nGroup Horizontal {\\n  Server 1 [icon: box, color: green]\\n  Server 2 [icon: box, color: green]\\n  Server 3 [icon: box, color: green]\\n}\\n\\n// Edges\\n2 CPU > 64 CPU\\nServer 1 > Server 2 [style: dashed]\\nServer 2 > Server 3 [style: dashed]",
    "components": [("Vertical","Hardware upgrades to existing boxes."), ("Horizontal","Adding identical boxes to a pool.")],
    "layout": "Contrasts a single growing entity against a replicating swarm."
}"""
flow_10 = """{
    "id": "sys-10-flow", "title": "Downtime vs Auto-Scale", "kind": "REQUEST FLOW",
    "code": "sequenceDiagram\\n  participant LB as LB\\n  participant S1 as Server 1\\n  participant S2 as Server 2\\n  Note over LB,S2: Horizontal Scale\\n  LB->>S1: Route\\n  LB->>S2: Route\\n  Note over LB,S2: Vertical Scale\\n  S1->>S1: Shutdown\\n  S1->>S1: Upgrade CPU\\n  S1->>S1: Restart (Downtime)",
    "eraser": "LB > Server 1: Route\\nLB > Server 2: Route\\nServer 1 > Server 1: Shutdown [color: red]\\nServer 1 > Server 1: Upgrade CPU\\nServer 1 > Server 1: Restart (Downtime) [color: red]",
    "components": [("Downtime","Vertical scaling requires reboots."), ("Routing","Horizontal scaling uses LB pools.")],
    "layout": "Shows the operational disruption of vertical upgrades vs seamless horizontal scaling."
}"""
replace_topic_data("sys-10", arch_10, flow_10)

with open("make_handbook_system_design.py", "w") as f:
    f.write(content)
print("Injected Topics 6-10.")
