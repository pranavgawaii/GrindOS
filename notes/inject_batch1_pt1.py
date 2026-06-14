import re

with open("make_handbook_system_design.py", "r") as f:
    content = f.read()

def replace_topic_data(topic_id, arch_data, flow_data):
    global content
    # Find the topic dictionary
    pattern = r'(\{\s*"id":\s*"' + topic_id + r'".*?)("diagram":\s*""")'
    # We will inject diagram_arch_data and diagram_flow_data right before "diagram"
    replacement = r'\1"diagram_arch_data": ' + arch_data + r', "diagram_flow_data": ' + flow_data + r', \2'
    content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)

# 1. System Design
arch_1 = """{
    "id": "sys-01-arch", "title": "System Design Architecture", "kind": "ARCHITECTURE",
    "code": "flowchart TB\\n  U([Client App]):::client\\n  GW[\\\"API Gateway\\\"]:::svc\\n  SVC[\\\"Microservices\\\"]:::svc\\n  DB[(\\\"Databases\\\")]:::data\\n  C[[\\\"Cache\\\"]]:::queue\\n  MQ[[\\\"Message Queue\\\"]]:::queue\\n\\n  U --> GW\\n  GW --> SVC\\n  SVC --> DB\\n  SVC --> C\\n  SVC --> MQ",
    "eraser": "// 1. Define nodes and logical groups\\nClient App [icon: smartphone, color: orange]\\nAPI Gateway [icon: server, color: blue]\\nMicroservices [icon: code, color: blue]\\nDatabases [icon: database, color: green]\\nCache [icon: layers, color: yellow]\\nMessage Queue [icon: list, color: yellow]\\n\\n// 2. Define connections\\nClient App > API Gateway\\nAPI Gateway > Microservices\\nMicroservices > Databases\\nMicroservices > Cache\\nMicroservices > Message Queue",
    "components": [("Client App","The frontend interface."), ("API Gateway","Central entry point handling routing."), ("Microservices","Independent business logic servers."), ("Databases","Persistent storage.")],
    "layout": "The client sits at the top, directing traffic through a central gateway which fans out to internal services and storage layers."
}"""
flow_1 = """{
    "id": "sys-01-flow", "title": "System Design Request Flow", "kind": "REQUEST FLOW",
    "code": "sequenceDiagram\\n  participant C as Client\\n  participant GW as Gateway\\n  participant AS as App Server\\n  participant DB as DB/Cache\\n  C->>GW: HTTP Request\\n  GW->>AS: Route\\n  AS->>DB: Query\\n  DB-->>AS: Results\\n  AS-->>C: 200 OK",
    "eraser": "// Sequence\\nClient > Gateway: HTTP Request\\nGateway > App Server: Route\\nApp Server > DB: Query\\nDB > App Server: Results\\nApp Server > Client: 200 OK",
    "components": [("HTTP Request","Standard REST or gRPC call."), ("Route","Gateway forwards packet based on path."), ("Query","Service fetches required state.")],
    "layout": "Vertical sequence showing round-trip synchronous request processing."
}"""
replace_topic_data("sys-01", arch_1, flow_1)

# 2. Scalability
arch_2 = """{
    "id": "sys-02-arch", "title": "Horizontal Scaling Architecture", "kind": "ARCHITECTURE",
    "code": "flowchart TB\\n  U([Users]):::client\\n  LB[\\\"Load Balancer\\\"]:::svc\\n  subgraph ASG[\\\"Auto-Scaling Group\\\"]\\n    WS1[\\\"Web Server 1\\\"]:::svc\\n    WSN[\\\"Web Server N\\\"]:::svc\\n  end\\n  DB[(\\\"Database\\\")]:::data\\n  U --> LB\\n  LB --> WS1 & WSN\\n  WS1 & WSN --> DB",
    "eraser": "// Nodes\\nUsers [icon: users, color: orange]\\nLoad Balancer [icon: server, color: blue]\\nGroup Auto-Scaling Group {\\n  Web Server 1 [icon: box, color: blue]\\n  Web Server N [icon: box, color: blue]\\n}\\nDatabase [icon: database, color: green]\\n\\n// Edges\\nUsers > Load Balancer\\nLoad Balancer > Web Server 1\\nLoad Balancer > Web Server N\\nWeb Server 1 > Database\\nWeb Server N > Database",
    "components": [("Auto-Scaling Group","Dynamically adds/removes instances."), ("Load Balancer","Distributes traffic across active instances.")],
    "layout": "Traffic flows from users, splits at the load balancer, and converges at the database."
}"""
flow_2 = """{
    "id": "sys-02-flow", "title": "Auto-Scaling Flow", "kind": "REQUEST FLOW",
    "code": "sequenceDiagram\\n  participant TS as Traffic\\n  participant AS as Auto Scaler\\n  participant CP as Cloud\\n  participant LB as Load Balancer\\n  TS->>AS: CPU > 80%\\n  AS->>CP: Request compute\\n  CP-->>AS: Instance booted\\n  AS->>LB: Register IP\\n  LB->>CP: Route traffic",
    "eraser": "Traffic > Auto Scaler: CPU > 80%\\nAuto Scaler > Cloud: Request compute\\nCloud > Auto Scaler: Instance booted\\nAuto Scaler > Load Balancer: Register IP\\nLoad Balancer > Cloud: Route traffic",
    "components": [("Trigger","Metric threshold exceeded."), ("Provision","Cloud allocates resources."), ("Register","LB adds instance to pool.")],
    "layout": "Shows the background asynchronous process of scaling infrastructure."
}"""
replace_topic_data("sys-02", arch_2, flow_2)

# 3. Availability
arch_3 = """{
    "id": "sys-03-arch", "title": "High Availability Multi-Region", "kind": "ARCHITECTURE",
    "code": "flowchart TB\\n  U([Users]):::client\\n  DNS[\\\"Route 53\\\"]:::svc\\n  subgraph R1[\\\"US-East\\\"]\\n    DB1[(\\\"Primary\\\")]:::data\\n  end\\n  subgraph R2[\\\"EU-West\\\"]\\n    DB2[(\\\"Replica\\\")]:::data\\n  end\\n  U --> DNS\\n  DNS --> R1\\n  DB1 -.->|Replication| DB2\\n  DNS -.->|Failover| R2",
    "eraser": "// Nodes\\nUsers [icon: users, color: orange]\\nRoute 53 [icon: compass, color: blue]\\nGroup US-East { Primary [icon: database, color: green] }\\nGroup EU-West { Replica [icon: database, color: green] }\\n\\n// Edges\\nUsers > Route 53\\nRoute 53 > Primary\\nPrimary > Replica [label: Replication, style: dashed]\\nRoute 53 > Replica [label: Failover, style: dashed, color: red]",
    "components": [("DNS Routing","Directs traffic to healthy regions."), ("Replication","Maintains state across geographic regions."), ("Failover","Fallback mechanism during regional outages.")],
    "layout": "Two distinct geographic clusters separated by a global DNS router."
}"""
flow_3 = """{
    "id": "sys-03-flow", "title": "DNS Failover Sequence", "kind": "REQUEST FLOW",
    "code": "sequenceDiagram\\n  participant U as User\\n  participant DNS as DNS Router\\n  participant R1 as Primary Region\\n  participant R2 as Standby Region\\n  R1--xDNS: Health check fails\\n  DNS->>DNS: Swap IP\\n  U->>DNS: Request\\n  DNS->>R2: Route to Standby\\n  R2-->>U: Success",
    "eraser": "Primary Region > DNS Router: Health check fails [color: red]\\nDNS Router > DNS Router: Swap IP\\nUser > DNS Router: Request\\nDNS Router > Standby Region: Route to Standby\\nStandby Region > User: Success",
    "components": [("Health Check","Periodic ping to verify region uptime."), ("TTL Swap","DNS updates routing IP record."), ("Promotion","Standby DB becomes primary.")],
    "layout": "Illustrates the failure detection and routing recovery sequence."
}"""
replace_topic_data("sys-03", arch_3, flow_3)

# 4. Reliability
arch_4 = """{
    "id": "sys-04-arch", "title": "Reliability and Write-Ahead Logging", "kind": "ARCHITECTURE",
    "code": "flowchart TB\\n  APP[\\\"App Server\\\"]:::svc\\n  WAL[[\\\"Write-Ahead Log\\\"]]:::queue\\n  DB[(\\\"Database\\\")]:::data\\n  APP -->|1. Write| WAL\\n  WAL -->|2. Commit| DB\\n  DB -->|3. Ack| APP",
    "eraser": "// Nodes\\nApp Server [icon: server, color: blue]\\nWrite-Ahead Log [icon: list, color: yellow]\\nDatabase [icon: database, color: green]\\n\\n// Edges\\nApp Server > Write-Ahead Log [label: 1. Write]\\nWrite-Ahead Log > Database [label: 2. Commit]\\nDatabase > App Server [label: 3. Ack]",
    "components": [("Write-Ahead Log","Append-only ledger guaranteeing writes."), ("Database Store","Final resting place for structured state.")],
    "layout": "A sequential triad showing the safety buffer between application and storage."
}"""
flow_4 = """{
    "id": "sys-04-flow", "title": "Atomic Commit Sequence", "kind": "REQUEST FLOW",
    "code": "sequenceDiagram\\n  participant APP as App Server\\n  participant WAL as WAL\\n  participant DB as Database\\n  APP->>WAL: Append log\\n  WAL-->>APP: Log synced\\n  WAL->>DB: Execute state change\\n  DB-->>APP: Committed",
    "eraser": "App Server > WAL: Append log\\nWAL > App Server: Log synced\\nWAL > Database: Execute state change\\nDatabase > App Server: Committed",
    "components": [("Sync Disk","Flushing log to physical storage."), ("Execute","Applying change to DB memory structures.")],
    "layout": "Shows the blocking atomic wait states during a reliable commit."
}"""
replace_topic_data("sys-04", arch_4, flow_4)

# 5. Fault Tolerance
arch_5 = """{
    "id": "sys-05-arch", "title": "Active-Passive Node Failover", "kind": "ARCHITECTURE",
    "code": "flowchart TB\\n  C([Clients]):::client\\n  LB[\\\"Load Balancer\\\"]:::svc\\n  N1[\\\"Node A (Primary)\\\"]:::svc\\n  N2[\\\"Node B (Standby)\\\"]:::svc\\n  C --> LB\\n  LB --> N1\\n  N1 -.->|Heartbeat| N2\\n  LB -.->|Takes over| N2",
    "eraser": "// Nodes\\nClients [icon: users, color: orange]\\nLoad Balancer [icon: server, color: blue]\\nNode A [icon: box, color: blue]\\nNode B [icon: box, color: blue]\\n\\n// Edges\\nClients > Load Balancer\\nLoad Balancer > Node A\\nNode A > Node B [label: Heartbeat, style: dashed]\\nLoad Balancer > Node B [label: Failover, style: dashed, color: red]",
    "components": [("Primary Node","Handles active connections."), ("Standby Node","Idles until failure detection."), ("Heartbeat","Pulse check between nodes.")],
    "layout": "Parallel active and passive nodes connected via a heartbeat bridge."
}"""
flow_5 = """{
    "id": "sys-05-flow", "title": "Failover Recovery Sequence", "kind": "REQUEST FLOW",
    "code": "sequenceDiagram\\n  participant LB as Load Balancer\\n  participant N1 as Primary\\n  participant N2 as Standby\\n  N1->>N2: Heartbeat (ok)\\n  N1--xN2: Heartbeat (dropped)\\n  N2->>LB: Assume Primary\\n  LB->>N2: Route traffic",
    "eraser": "Primary > Standby: Heartbeat (ok)\\nPrimary > Standby: Heartbeat (dropped) [color: red]\\nStandby > Load Balancer: Assume Primary\\nLoad Balancer > Standby: Route traffic",
    "components": [("Detection","Standby notices missing pings."), ("Assumption","Standby elevates privileges."), ("Re-route","LB updates target group.")],
    "layout": "Chronological timeline of a node death and subsequent takeover."
}"""
replace_topic_data("sys-05", arch_5, flow_5)

with open("make_handbook_system_design.py", "w") as f:
    f.write(content)
print("Injected Topics 1-5.")
