import re

with open("make_handbook_system_design.py", "r") as f:
    content = f.read()

def replace_topic(topic_id, new_arch, new_flow):
    global content
    # Find the topic dict
    pattern = r'(\{\s*"id":\s*"' + topic_id + r'".*?"diagram":\s*""")[\s\S]*?("""\s*,\s*"flow")'
    replacement = r'\1\n' + new_arch.strip() + r'\n\2'
    content = re.sub(pattern, replacement, content, count=1)
    
    # Insert flow_diagram
    if new_flow:
        insert_pattern = r'(\{\s*"id":\s*"' + topic_id + r'".*?"flow":\s*".*?"\s*,)'
        insert_replacement = r'\1\n        "flow_diagram": """\n' + new_flow.strip() + r'\n""",'
        content = re.sub(insert_pattern, insert_replacement, content, count=1)

# 1. System Design
replace_topic("sys-01", 
"flowchart TB\n  U([Client App]):::client\n  GW[\"API Gateway\"]:::svc\n  SVC[\"Microservices\"]:::svc\n  DB[(\"Databases\")]:::data\n  C[[\"Cache\"]]:::queue\n  MQ[[\"Message Queue\"]]:::queue\n\n  U --> GW\n  GW --> SVC\n  SVC --> DB\n  SVC --> C\n  SVC --> MQ",
"sequenceDiagram\n  participant C as Client\n  participant GW as Gateway\n  participant AS as App Server\n  participant DB as Database/Cache\n  C->>GW: HTTP Request\n  GW->>AS: Route\n  AS->>DB: Query Data\n  DB-->>AS: Results\n  AS-->>GW: JSON Response\n  GW-->>C: 200 OK")

# 2. Scalability
replace_topic("sys-02",
"flowchart TB\n  U([Users]):::client\n  LB[\"Load Balancer\"]:::svc\n  subgraph ASG[\"Auto-Scaling Group\"]\n    WS1[\"Web Server 1\"]:::svc\n    WS2[\"Web Server 2\"]:::svc\n    WSN[\"Web Server N\"]:::svc\n  end\n  DB[(\"Database\")]:::data\n  U --> LB\n  LB --> WS1 & WS2 & WSN\n  WS1 & WS2 & WSN --> DB",
"sequenceDiagram\n  participant TS as Traffic Spike\n  participant AS as Auto Scaler\n  participant CP as Cloud Provider\n  participant LB as Load Balancer\n  TS->>AS: Trigger CPU > 80%\n  AS->>CP: Request new compute\n  CP-->>AS: Instance booted\n  AS->>LB: Register new IP\n  LB->>CP: Route incoming traffic")

# 3. Availability
replace_topic("sys-03",
"flowchart TB\n  U([Users]):::client\n  DNS[\"DNS Router (Route 53)\"]:::svc\n  subgraph R1[\"Active Region (US-East)\"]\n    DB1[(\"Primary DB\")]:::data\n  end\n  subgraph R2[\"Standby Region (EU-West)\"]\n    DB2[(\"Replica DB\")]:::data\n  end\n  U --> DNS\n  DNS --> R1\n  DB1 -.->|Async Replication| DB2\n  DNS -.->|Failover| R2",
"sequenceDiagram\n  participant U as User\n  participant DNS as DNS Router\n  participant R1 as Active Region\n  participant R2 as Standby Region\n  R1--xDNS: Health check fails\n  DNS->>DNS: TTL Expires, Swap IP\n  U->>DNS: Request\n  DNS->>R2: Route to Standby\n  R2->>R2: Promote DB to Primary\n  R2-->>U: Success")

# 4. Reliability
replace_topic("sys-04",
"flowchart TB\n  APP[\"Application Server\"]:::svc\n  WAL[[\"Write-Ahead Log (WAL)\"]]:::queue\n  DB[(\"Primary DB Store\")]:::data\n  APP -->|1. Write to Log| WAL\n  WAL -->|2. Commit| DB\n  DB -->|3. Acknowledge| APP",
"sequenceDiagram\n  participant APP as App Server\n  participant WAL as Write-Ahead Log\n  participant DB as Database\n  APP->>WAL: Append transaction log\n  WAL-->>APP: Log synced to disk\n  WAL->>DB: Execute state change\n  DB-->>APP: Transaction committed")

# 5. Fault Tolerance
replace_topic("sys-05",
"flowchart TB\n  C([Clients]):::client\n  LB[\"Load Balancer\"]:::svc\n  N1[\"Node A (Primary)\"]:::svc\n  N2[\"Node B (Standby)\"]:::svc\n  C --> LB\n  LB --> N1\n  N1 -.->|Heartbeat| N2\n  LB -.->|Takes over on drop| N2",
"sequenceDiagram\n  participant LB as Load Balancer\n  participant N1 as Primary Node\n  participant N2 as Standby Node\n  N1->>N2: Heartbeat (ok)\n  N1--xN2: Heartbeat (dropped)\n  N2->>LB: Assume Primary Role\n  LB->>N2: Route new traffic")

# 6. Latency
replace_topic("sys-06",
"flowchart LR\n  U([Client]):::client\n  CDN[\"Edge CDN\"]:::svc\n  SRV[\"Origin Server\"]:::svc\n  DB[(\"Database\")]:::data\n  U -->|10ms| CDN\n  CDN -->|Cache Miss: 50ms| SRV\n  SRV -->|10ms| DB",
"sequenceDiagram\n  participant C as Client\n  participant CDN as Edge Server\n  participant SRV as Origin Server\n  C->>CDN: Request\n  CDN-->>C: Cache Hit (Fast)\n  C->>CDN: Request 2\n  CDN->>SRV: Cache Miss (Network transit)\n  SRV-->>C: Response (Slow)")

# 7. Throughput
replace_topic("sys-07",
"flowchart TB\n  IN[\"Incoming: 10k RPS\"]:::client\n  Q[[\"Queue Buffer\"]]:::queue\n  subgraph SC[\"Server Cluster\"]\n    W1[\"Worker 1\"]:::svc\n    W2[\"Worker 2\"]:::svc\n  end\n  DB[(\"Database\")]:::data\n  IN --> Q\n  Q --> SC\n  SC -->|Processed: 9k RPS| DB\n  IN -.->|1k dropped| Drop",
"sequenceDiagram\n  participant IN as Incoming Traffic\n  participant Q as Buffer Queue\n  participant W as Worker Pool\n  IN->>Q: Rapid enqueue requests\n  Q->>W: Pull batches (Parallel)\n  W->>W: Process batch\n  W-->>Q: Ack completion")

# 8. CAP Theorem
replace_topic("sys-08",
"flowchart TB\n  subgraph CAP[\"Distributed Database Tradeoffs\"]\n    C[\"Consistency (C)\"]\n    A[\"Availability (A)\"]\n    P[\"Partition Tolerance (P)\"]\n  end\n  C ---|CP: Postgres / Mongo| P\n  A ---|AP: Cassandra / Dynamo| P\n  C ---|CA: Single Node| A",
"sequenceDiagram\n  participant C as Client\n  participant N1 as Node 1\n  participant N2 as Node 2\n  Note over N1,N2: Network Split (P occurs)\n  C->>N1: Write Data\n  N1--xN2: Sync fails\n  Note over N1: CP System: Reject Write\n  Note over N1: AP System: Accept Write (Data drift)")

# 9. Consistency Models
replace_topic("sys-09",
"flowchart TB\n  C([Client]):::client\n  subgraph STRONG[\"Strong Consistency\"]\n    W1[\"Write Node\"]:::svc\n    R1[\"Read Node\"]:::svc\n    W1 ===|Sync lock| R1\n  end\n  subgraph EVENTUAL[\"Eventual Consistency\"]\n    W2[\"Write Node\"]:::svc\n    R2[\"Read Node\"]:::svc\n    W2 -.-|Async replica| R2\n  end\n  C --> STRONG & EVENTUAL",
"sequenceDiagram\n  participant C as Client\n  participant W as Write Node\n  participant R as Read Node\n  Note over C,R: Strong Consistency\n  C->>W: Write(X)\n  W->>R: Sync(X)\n  R-->>W: Ack\n  W-->>C: Success\n  Note over C,R: Eventual Consistency\n  C->>W: Write(Y)\n  W-->>C: Success (Fast)\n  W-)+R: Async Sync(Y)")

# 10. Horizontal vs Vertical
replace_topic("sys-10",
"flowchart TB\n  subgraph V[\"Vertical Scaling (Scale Up)\"]\n    S1[\"Small Server (2 CPU)\"]:::svc --> S2[\"Large Server (64 CPU)\"]:::svc\n  end\n  subgraph H[\"Horizontal Scaling (Scale Out)\"]\n    S3[\"Server 1\"]:::svc\n    S4[\"Server 2\"]:::svc\n    S5[\"Server 3\"]:::svc\n    S3 -.-> S4 -.-> S5\n  end",
"sequenceDiagram\n  participant U as User\n  participant LB as Load Balancer\n  participant S1 as Server 1\n  participant S2 as Server 2\n  Note over U,S2: Horizontal Scale Out\n  LB->>S1: Route traffic\n  LB->>S2: Route traffic\n  Note over U,S2: Vertical Scale Up\n  S1->>S1: Shutdown\n  S1->>S1: Upgrade CPU\n  S1->>S1: Restart (Downtime)")


with open("make_handbook_system_design.py", "w") as f:
    f.write(content)
print("Injected Foundations premium diagrams.")
