const TOC_MAPS = {
  "GrindOS_CN_Booklet.pdf": [
    {
      "title": "NETWORK ARCHITECTURE & MODELS",
      "items": [
        {
          "title": "01  The OSI Reference Model",
          "page": 4
        },
        {
          "title": "02  TCP/IP Model Suite",
          "page": 5
        }
      ]
    },
    {
      "title": "TRANSPORT LAYER PROTOCOLS",
      "items": [
        {
          "title": "03  TCP vs UDP",
          "page": 6
        }
      ]
    },
    {
      "title": "NETWORK LAYER ADDRESSING",
      "items": [
        {
          "title": "04  IP Addressing (IPv4 vs IPv6)",
          "page": 7
        },
        {
          "title": "05  Subnetting & CIDR",
          "page": 8
        }
      ]
    },
    {
      "title": "DATA LINK LAYER & RESOLUTION",
      "items": [
        {
          "title": "06  MAC Address & ARP",
          "page": 9
        }
      ]
    },
    {
      "title": "APPLICATION LAYER SERVICES",
      "items": [
        {
          "title": "07  Domain Name System (DNS)",
          "page": 10
        },
        {
          "title": "08  DHCP Protocol",
          "page": 11
        }
      ]
    },
    {
      "title": "APPLICATION LAYER PROTOCOLS",
      "items": [
        {
          "title": "09  HTTP Evolution",
          "page": 12
        },
        {
          "title": "10  HTTPS & SSL/TLS Handshake",
          "page": 13
        }
      ]
    },
    {
      "title": "TRANSPORT LAYER PROTOCOLS",
      "items": [
        {
          "title": "11  TCP 3-Way Handshake",
          "page": 14
        },
        {
          "title": "12  TCP Connection Termination",
          "page": 15
        }
      ]
    },
    {
      "title": "TRANSPORT LAYER MECHANISMS",
      "items": [
        {
          "title": "13  Flow Control",
          "page": 16
        },
        {
          "title": "14  Sliding Window Protocol",
          "page": 17
        },
        {
          "title": "15  TCP Congestion Control",
          "page": 18
        }
      ]
    },
    {
      "title": "DATA LINK LAYER & ROUTING",
      "items": [
        {
          "title": "16  MAC vs IP Addressing",
          "page": 19
        }
      ]
    },
    {
      "title": "NETWORK LAYER CONCEPTS",
      "items": [
        {
          "title": "17  Routing vs Forwarding",
          "page": 20
        }
      ]
    },
    {
      "title": "NETWORK LAYER ROUTING",
      "items": [
        {
          "title": "18  Routing Protocols (OSPF vs BGP)",
          "page": 21
        }
      ]
    },
    {
      "title": "NETWORK LAYER SERVICES",
      "items": [
        {
          "title": "19  Network Address Translation (NAT)",
          "page": 22
        }
      ]
    },
    {
      "title": "NETWORK HARDWARE & INFRASTRUCTURE",
      "items": [
        {
          "title": "20  Network Devices",
          "page": 23
        }
      ]
    },
    {
      "title": "NETWORK CORE TECHNOLOGIES",
      "items": [
        {
          "title": "21  Circuit vs Packet Switching",
          "page": 24
        }
      ]
    },
    {
      "title": "NETWORK SECURITY & VPNS",
      "items": [
        {
          "title": "22  VPN & Tunneling",
          "page": 25
        }
      ]
    },
    {
      "title": "NETWORK SECURITY & FIREWALLS",
      "items": [
        {
          "title": "23  Firewalls (Stateful vs WAF)",
          "page": 26
        }
      ]
    },
    {
      "title": "NETWORK ATTACKS & DEFENSES",
      "items": [
        {
          "title": "24  DDoS Attacks & Mitigation",
          "page": 27
        }
      ]
    }
  ],
  "GrindOS_DBMS_Booklet.pdf": [
    {
      "title": "DBMS ARCHITECTURE & FUNDAMENTALS",
      "items": [
        {
          "title": "01  3-Tier Architecture",
          "page": 4
        },
        {
          "title": "02  Data Independence",
          "page": 5
        }
      ]
    },
    {
      "title": "RELATIONAL MODEL CORE",
      "items": [
        {
          "title": "03  Database Keys",
          "page": 6
        },
        {
          "title": "04  Normal Forms (1NF \u2192 BCNF)",
          "page": 7
        },
        {
          "title": "05  4NF & 5NF Normalization",
          "page": 8
        }
      ]
    },
    {
      "title": "DATABASE DESIGN & MODELS",
      "items": [
        {
          "title": "06  ER Model to Relational",
          "page": 9
        }
      ]
    },
    {
      "title": "TRANSACTION MANAGEMENT",
      "items": [
        {
          "title": "07  ACID Properties & WAL",
          "page": 10
        },
        {
          "title": "08  Transaction States",
          "page": 11
        }
      ]
    },
    {
      "title": "CONCURRENCY & ISOLATION",
      "items": [
        {
          "title": "09  Concurrency Anomalies",
          "page": 12
        },
        {
          "title": "10  Conflict & View Serializability",
          "page": 13
        },
        {
          "title": "11  Transaction Isolation Levels",
          "page": 14
        },
        {
          "title": "12  2-Phase Locking (2PL)",
          "page": 15
        },
        {
          "title": "13  DBMS Deadlocks",
          "page": 16
        }
      ]
    },
    {
      "title": "STORAGE & INDEXING",
      "items": [
        {
          "title": "14  B-Tree vs B+ Tree",
          "page": 17
        },
        {
          "title": "15  Static vs Dynamic Hashing",
          "page": 18
        }
      ]
    },
    {
      "title": "QUERY LANGUAGES & ALGEBRA",
      "items": [
        {
          "title": "16  Relational Algebra",
          "page": 19
        },
        {
          "title": "17  SQL Joins",
          "page": 20
        }
      ]
    },
    {
      "title": "SQL OPERATIONS",
      "items": [
        {
          "title": "18  Subqueries & Correlated",
          "page": 21
        },
        {
          "title": "19  Views vs Materialized Views",
          "page": 22
        },
        {
          "title": "20  Triggers & Stored Procs",
          "page": 23
        }
      ]
    },
    {
      "title": "TRANSACTION MANAGEMENT",
      "items": [
        {
          "title": "21  Database Recovery",
          "page": 24
        }
      ]
    },
    {
      "title": "RELATIONAL MODEL CORE",
      "items": [
        {
          "title": "22  SQL Constraints",
          "page": 25
        }
      ]
    },
    {
      "title": "ADVANCED DBMS CONCEPTS",
      "items": [
        {
          "title": "23  NoSQL vs SQL & CAP",
          "page": 26
        },
        {
          "title": "24  Sharding & Replication",
          "page": 27
        }
      ]
    },
    {
      "title": "SQL PRACTICE PAGES",
      "items": [
        {
          "title": "25  SQL: Nth Highest Salary",
          "page": 28
        },
        {
          "title": "26  SQL: Duplicate Emails",
          "page": 29
        },
        {
          "title": "27  SQL: Consecutive Numbers",
          "page": 30
        },
        {
          "title": "28  SQL: Department Top Salaries",
          "page": 31
        },
        {
          "title": "29  SQL: Exchange Seats",
          "page": 32
        },
        {
          "title": "30  SQL: Cancellation Rate",
          "page": 33
        }
      ]
    }
  ],
  "GrindOS_OOPS_Booklet.pdf": [
    {
      "title": "OOP FUNDAMENTALS",
      "items": [
        {
          "title": "01  Class & Object",
          "page": 4
        },
        {
          "title": "02  Constructor & Destructor",
          "page": 5
        }
      ]
    },
    {
      "title": "THE FOUR PILLARS",
      "items": [
        {
          "title": "03  Pillar 1: Inheritance",
          "page": 6
        },
        {
          "title": "04  Pillar 2: Polymorphism",
          "page": 7
        },
        {
          "title": "05  Pillar 3: Abstraction",
          "page": 8
        },
        {
          "title": "06  Pillar 4: Encapsulation",
          "page": 9
        }
      ]
    },
    {
      "title": "METHOD OPERATIONS",
      "items": [
        {
          "title": "07  Overloading vs Overriding",
          "page": 10
        },
        {
          "title": "08  Virtual Function & VTABLE",
          "page": 11
        }
      ]
    },
    {
      "title": "ABSTRACT CONTRACTS",
      "items": [
        {
          "title": "09  Abstract Class vs Interface",
          "page": 12
        }
      ]
    },
    {
      "title": "OBJECT RELATIONSHIPS",
      "items": [
        {
          "title": "10  Aggregation & Composition",
          "page": 13
        }
      ]
    },
    {
      "title": "SOLID PRINCIPLES",
      "items": [
        {
          "title": "11  SOLID: S & O Principles",
          "page": 14
        },
        {
          "title": "12  SOLID: L, I, & D Principles",
          "page": 15
        }
      ]
    },
    {
      "title": "LANGUAGE SPECIFICS",
      "items": [
        {
          "title": "13  Access Modifiers",
          "page": 16
        }
      ]
    },
    {
      "title": "METHOD OPERATIONS",
      "items": [
        {
          "title": "14  Static vs Dynamic Binding",
          "page": 17
        }
      ]
    },
    {
      "title": "MEMORY & MANAGEMENT",
      "items": [
        {
          "title": "15  Garbage Collection & Memory",
          "page": 18
        },
        {
          "title": "16  Shallow vs Deep Copy",
          "page": 19
        }
      ]
    },
    {
      "title": "LANGUAGE SPECIFICS",
      "items": [
        {
          "title": "17  Copy Const. & Assignment",
          "page": 20
        }
      ]
    }
  ],
  "GrindOS_OS_Booklet.pdf": [
    {
      "title": "PROCESS MANAGEMENT",
      "items": [
        {
          "title": "01  Process vs Thread",
          "page": 4
        },
        {
          "title": "02  CPU Scheduling Algorithms",
          "page": 5
        },
        {
          "title": "03  PCB & Context Switching",
          "page": 6
        },
        {
          "title": "04  Multi-Level Queue & Feedback Queue",
          "page": 7
        }
      ]
    },
    {
      "title": "MEMORY MANAGEMENT",
      "items": [
        {
          "title": "05  Paging & Segmentation",
          "page": 8
        },
        {
          "title": "06  Virtual Memory & Demand Paging",
          "page": 9
        },
        {
          "title": "07  Page Replacement Algorithms",
          "page": 10
        },
        {
          "title": "08  Page Fault & Thrashing",
          "page": 11
        }
      ]
    },
    {
      "title": "PROCESS SYNCHRONIZATION",
      "items": [
        {
          "title": "09  Critical Section Problem",
          "page": 12
        },
        {
          "title": "10  Mutex vs Semaphore vs Monitor",
          "page": 13
        },
        {
          "title": "11  Classic Synchronization Problems",
          "page": 14
        }
      ]
    },
    {
      "title": "DEADLOCKS",
      "items": [
        {
          "title": "12  Deadlock: Four Conditions",
          "page": 15
        },
        {
          "title": "13  Banker's Algorithm",
          "page": 16
        },
        {
          "title": "14  Deadlock Detection & Recovery",
          "page": 17
        }
      ]
    },
    {
      "title": "FILE SYSTEMS & STORAGE",
      "items": [
        {
          "title": "15  File Systems & Inodes",
          "page": 18
        },
        {
          "title": "16  Disk Scheduling Algorithms",
          "page": 19
        }
      ]
    },
    {
      "title": "OPERATING SYSTEM ARCHITECTURE",
      "items": [
        {
          "title": "17  Monolithic vs Microkernel",
          "page": 20
        },
        {
          "title": "18  System Calls (fork, exec)",
          "page": 21
        },
        {
          "title": "19  Inter-Process Communication",
          "page": 22
        }
      ]
    },
    {
      "title": "MEMORY MANAGEMENT",
      "items": [
        {
          "title": "20  Fragmentation (Internal vs External)",
          "page": 23
        },
        {
          "title": "21  TLB (Translation Lookaside Buffer)",
          "page": 24
        }
      ]
    },
    {
      "title": "OPERATING SYSTEM SECURITY",
      "items": [
        {
          "title": "22  User Mode vs Kernel Mode",
          "page": 25
        }
      ]
    },
    {
      "title": "OPERATING SYSTEM EXECUTION",
      "items": [
        {
          "title": "23  Dynamic vs Static Linking",
          "page": 26
        }
      ]
    },
    {
      "title": "OPERATING SYSTEM OPERATIONS",
      "items": [
        {
          "title": "24  Spooling vs Buffering",
          "page": 27
        }
      ]
    },
    {
      "title": "OPERATING SYSTEM ARCHITECTURES",
      "items": [
        {
          "title": "25  RTOS vs GPOS",
          "page": 28
        }
      ]
    }
  ],
  "GrindOS_SQL_Booklet.pdf": [
    {
      "title": "SQL FUNDAMENTALS",
      "items": [
        {
          "title": "01  SELECT Statement",
          "page": 4
        },
        {
          "title": "02  WHERE Clause",
          "page": 5
        },
        {
          "title": "03  ORDER BY Clause",
          "page": 6
        },
        {
          "title": "04  DISTINCT Clause",
          "page": 7
        },
        {
          "title": "05  LIMIT & OFFSET",
          "page": 8
        }
      ]
    },
    {
      "title": "FILTERING & AGGREGATION",
      "items": [
        {
          "title": "06  GROUP BY Clause",
          "page": 9
        },
        {
          "title": "07  HAVING Clause",
          "page": 10
        },
        {
          "title": "08  Aggregate Functions",
          "page": 11
        }
      ]
    },
    {
      "title": "JOINS",
      "items": [
        {
          "title": "09  INNER JOIN",
          "page": 12
        },
        {
          "title": "10  LEFT OUTER JOIN",
          "page": 13
        },
        {
          "title": "11  RIGHT OUTER JOIN",
          "page": 14
        },
        {
          "title": "12  FULL OUTER JOIN",
          "page": 15
        },
        {
          "title": "13  SELF JOIN",
          "page": 16
        },
        {
          "title": "14  CROSS JOIN",
          "page": 17
        }
      ]
    },
    {
      "title": "SUBQUERIES",
      "items": [
        {
          "title": "15  Subqueries (Nested Queries)",
          "page": 18
        },
        {
          "title": "16  Correlated Subqueries",
          "page": 19
        }
      ]
    },
    {
      "title": "ADVANCED SQL",
      "items": [
        {
          "title": "17  CTEs (Common Table Expressions)",
          "page": 20
        },
        {
          "title": "18  Window Functions",
          "page": 21
        },
        {
          "title": "19  ROW_NUMBER()",
          "page": 22
        },
        {
          "title": "20  RANK()",
          "page": 23
        },
        {
          "title": "21  DENSE_RANK()",
          "page": 24
        },
        {
          "title": "22  LEAD()",
          "page": 25
        },
        {
          "title": "23  LAG()",
          "page": 26
        }
      ]
    },
    {
      "title": "INDEXING & PERFORMANCE",
      "items": [
        {
          "title": "24  Database Indexing",
          "page": 27
        },
        {
          "title": "25  Clustered Index",
          "page": 28
        },
        {
          "title": "26  Non-Clustered Index",
          "page": 29
        },
        {
          "title": "27  Query Optimization",
          "page": 30
        },
        {
          "title": "28  Execution Plan Basics",
          "page": 31
        }
      ]
    },
    {
      "title": "TRANSACTIONS",
      "items": [
        {
          "title": "29  ACID Properties",
          "page": 32
        },
        {
          "title": "30  Transactions",
          "page": 33
        },
        {
          "title": "31  Locks & Concurrency",
          "page": 34
        }
      ]
    },
    {
      "title": "INTERVIEW SQL",
      "items": [
        {
          "title": "32  Nth Highest Salary",
          "page": 35
        },
        {
          "title": "33  Duplicate Records",
          "page": 36
        },
        {
          "title": "34  Consecutive Numbers",
          "page": 37
        },
        {
          "title": "35  Department Top Earners",
          "page": 38
        },
        {
          "title": "36  Running Total",
          "page": 39
        },
        {
          "title": "37  Top N Per Group",
          "page": 40
        },
        {
          "title": "38  Customer Retention",
          "page": 41
        },
        {
          "title": "39  Ranking Queries",
          "page": 42
        },
        {
          "title": "40  Date Queries",
          "page": 43
        }
      ]
    }
  ],
  "GrindOS_SYSTEM_DESIGN_Booklet.pdf": [
    {
      "title": "FOUNDATIONS",
      "items": [
        {
          "title": "01  What Is System Design",
          "page": 4
        },
        {
          "title": "02  Scalability",
          "page": 5
        },
        {
          "title": "03  Availability",
          "page": 6
        },
        {
          "title": "04  Reliability",
          "page": 7
        },
        {
          "title": "05  Fault Tolerance",
          "page": 8
        },
        {
          "title": "06  Latency",
          "page": 9
        },
        {
          "title": "07  Throughput",
          "page": 10
        },
        {
          "title": "08  CAP Theorem",
          "page": 11
        },
        {
          "title": "09  Consistency Models",
          "page": 12
        },
        {
          "title": "10  Horizontal vs Vertical Scaling",
          "page": 13
        }
      ]
    },
    {
      "title": "NETWORKING",
      "items": [
        {
          "title": "11  Load Balancer",
          "page": 14
        },
        {
          "title": "12  Reverse Proxy",
          "page": 15
        },
        {
          "title": "13  CDN",
          "page": 16
        },
        {
          "title": "14  API Gateway",
          "page": 17
        },
        {
          "title": "15  Service Discovery",
          "page": 18
        },
        {
          "title": "16  DNS Flow",
          "page": 19
        },
        {
          "title": "17  Caching Basics",
          "page": 20
        }
      ]
    },
    {
      "title": "DATABASES",
      "items": [
        {
          "title": "18  SQL vs NoSQL",
          "page": 21
        },
        {
          "title": "19  Database Indexing",
          "page": 22
        },
        {
          "title": "20  Replication",
          "page": 23
        },
        {
          "title": "21  Read Replicas",
          "page": 24
        },
        {
          "title": "22  Sharding",
          "page": 25
        },
        {
          "title": "23  Partitioning",
          "page": 26
        },
        {
          "title": "24  CQRS",
          "page": 27
        },
        {
          "title": "25  Eventual Consistency",
          "page": 28
        },
        {
          "title": "26  Distributed Transactions",
          "page": 29
        }
      ]
    },
    {
      "title": "MESSAGING",
      "items": [
        {
          "title": "27  Message Queues",
          "page": 30
        },
        {
          "title": "28  Kafka",
          "page": 31
        },
        {
          "title": "29  RabbitMQ",
          "page": 32
        },
        {
          "title": "30  Pub/Sub",
          "page": 33
        },
        {
          "title": "31  Event Driven Architecture",
          "page": 34
        },
        {
          "title": "32  Dead Letter Queue",
          "page": 35
        },
        {
          "title": "33  Retry Patterns",
          "page": 36
        },
        {
          "title": "34  Idempotency",
          "page": 37
        }
      ]
    },
    {
      "title": "MICROSERVICES",
      "items": [
        {
          "title": "35  Monolith vs Microservices",
          "page": 38
        },
        {
          "title": "36  Circuit Breaker",
          "page": 39
        },
        {
          "title": "37  Service Mesh",
          "page": 40
        },
        {
          "title": "38  Saga Pattern",
          "page": 41
        },
        {
          "title": "39  Distributed Tracing",
          "page": 42
        },
        {
          "title": "40  Rate Limiting",
          "page": 43
        }
      ]
    },
    {
      "title": "STORAGE",
      "items": [
        {
          "title": "41  Object Storage",
          "page": 44
        },
        {
          "title": "42  Blob Storage",
          "page": 45
        },
        {
          "title": "43  File Upload Architecture",
          "page": 46
        },
        {
          "title": "44  Media Processing",
          "page": 47
        },
        {
          "title": "45  Search Architecture",
          "page": 48
        }
      ]
    },
    {
      "title": "SECURITY",
      "items": [
        {
          "title": "46  Authentication",
          "page": 49
        },
        {
          "title": "47  Authorization",
          "page": 50
        },
        {
          "title": "48  JWT",
          "page": 51
        },
        {
          "title": "49  OAuth",
          "page": 52
        },
        {
          "title": "50  Session Auth",
          "page": 53
        },
        {
          "title": "51  RBAC",
          "page": 54
        },
        {
          "title": "52  ABAC",
          "page": 55
        },
        {
          "title": "53  Zero Trust",
          "page": 56
        }
      ]
    },
    {
      "title": "OBSERVABILITY",
      "items": [
        {
          "title": "54  Logging",
          "page": 57
        },
        {
          "title": "55  Monitoring",
          "page": 58
        },
        {
          "title": "56  Metrics",
          "page": 59
        },
        {
          "title": "57  Alerting",
          "page": 60
        },
        {
          "title": "58  Tracing",
          "page": 61
        },
        {
          "title": "59  Prometheus",
          "page": 62
        },
        {
          "title": "60  Grafana",
          "page": 63
        }
      ]
    },
    {
      "title": "CASE STUDIES",
      "items": [
        {
          "title": "61  URL Shortener",
          "page": 64
        },
        {
          "title": "62  WhatsApp",
          "page": 65
        },
        {
          "title": "63  Instagram Feed",
          "page": 66
        },
        {
          "title": "64  YouTube",
          "page": 67
        },
        {
          "title": "65  Uber",
          "page": 68
        },
        {
          "title": "66  Zomato",
          "page": 69
        },
        {
          "title": "67  Google Drive",
          "page": 70
        },
        {
          "title": "68  Notification System",
          "page": 71
        },
        {
          "title": "69  Chat System",
          "page": 72
        },
        {
          "title": "70  Rate Limiter",
          "page": 73
        }
      ]
    },
    {
      "title": "INTERVIEW FRAMEWORK",
      "items": [
        {
          "title": "71  Requirement Gathering",
          "page": 74
        },
        {
          "title": "72  Capacity Estimation",
          "page": 75
        },
        {
          "title": "73  API Design",
          "page": 76
        },
        {
          "title": "74  Database Design",
          "page": 77
        },
        {
          "title": "75  Bottleneck Analysis",
          "page": 78
        },
        {
          "title": "76  Scaling Strategy",
          "page": 79
        },
        {
          "title": "77  Tradeoff Discussion",
          "page": 80
        },
        {
          "title": "78  Common Mistakes",
          "page": 81
        },
        {
          "title": "79  Interview Framework",
          "page": 82
        },
        {
          "title": "80  Top 100 Questions",
          "page": 83
        }
      ]
    }
  ],
  "GrindOS_PROJECTS_Booklet.pdf": [
    {
      "title": "01 CRAFTASTUDIO",
      "items": [
        {
          "title": "01  Executive Summary",
          "page": 5
        },
        {
          "title": "02  Product Vision",
          "page": 6
        },
        {
          "title": "03  Business Problem",
          "page": 7
        },
        {
          "title": "04  User Journey",
          "page": 8
        },
        {
          "title": "05  Functional Requirements",
          "page": 9
        },
        {
          "title": "06  Non-Functional Requirements",
          "page": 10
        },
        {
          "title": "07  Tech Stack Decisions",
          "page": 11
        },
        {
          "title": "08  Architecture Overview",
          "page": 12
        },
        {
          "title": "09  Request Lifecycle",
          "page": 13
        },
        {
          "title": "10  Database Design",
          "page": 14
        },
        {
          "title": "11  Authentication Design",
          "page": 15
        },
        {
          "title": "12  Deployment Architecture",
          "page": 16
        },
        {
          "title": "13  Scalability Architecture",
          "page": 17
        },
        {
          "title": "14  Security Architecture",
          "page": 18
        },
        {
          "title": "15  Failure Recovery",
          "page": 19
        },
        {
          "title": "16  Monitoring & Observability",
          "page": 20
        },
        {
          "title": "17  Cost Optimization",
          "page": 21
        },
        {
          "title": "18  Engineering Challenges",
          "page": 22
        },
        {
          "title": "19  Architecture Tradeoffs",
          "page": 23
        },
        {
          "title": "20  Future Roadmap",
          "page": 24
        },
        {
          "title": "21  Interview Deep Dive",
          "page": 25
        },
        {
          "title": "22  Revision Sheet",
          "page": 26
        }
      ]
    },
    {
      "title": "02 PLACEPRO",
      "items": [
        {
          "title": "01  Executive Summary",
          "page": 28
        },
        {
          "title": "02  Product Vision",
          "page": 29
        },
        {
          "title": "03  Business Problem",
          "page": 30
        },
        {
          "title": "04  User Journey",
          "page": 31
        },
        {
          "title": "05  Functional Requirements",
          "page": 32
        },
        {
          "title": "06  Non-Functional Requirements",
          "page": 33
        },
        {
          "title": "07  Tech Stack Decisions",
          "page": 34
        },
        {
          "title": "08  Architecture Overview",
          "page": 35
        },
        {
          "title": "09  Request Lifecycle",
          "page": 36
        },
        {
          "title": "10  Database Design",
          "page": 37
        },
        {
          "title": "11  Authentication Design",
          "page": 38
        },
        {
          "title": "12  Deployment Architecture",
          "page": 39
        },
        {
          "title": "13  Scalability Architecture",
          "page": 40
        },
        {
          "title": "14  Security Architecture",
          "page": 41
        },
        {
          "title": "15  Failure Recovery",
          "page": 42
        },
        {
          "title": "16  Monitoring & Observability",
          "page": 43
        },
        {
          "title": "17  Cost Optimization",
          "page": 44
        },
        {
          "title": "18  Engineering Challenges",
          "page": 45
        },
        {
          "title": "19  Architecture Tradeoffs",
          "page": 46
        },
        {
          "title": "20  Future Roadmap",
          "page": 47
        },
        {
          "title": "21  Interview Deep Dive",
          "page": 48
        },
        {
          "title": "22  Revision Sheet",
          "page": 49
        }
      ]
    },
    {
      "title": "03 MNEMO",
      "items": [
        {
          "title": "01  Executive Summary",
          "page": 51
        },
        {
          "title": "02  Product Vision",
          "page": 52
        },
        {
          "title": "03  Business Problem",
          "page": 53
        },
        {
          "title": "04  User Journey",
          "page": 54
        },
        {
          "title": "05  Functional Requirements",
          "page": 55
        },
        {
          "title": "06  Non-Functional Requirements",
          "page": 56
        },
        {
          "title": "07  Tech Stack Decisions",
          "page": 57
        },
        {
          "title": "08  Architecture Overview",
          "page": 58
        },
        {
          "title": "09  Request Lifecycle",
          "page": 59
        },
        {
          "title": "10  Database Design",
          "page": 60
        },
        {
          "title": "11  Authentication Design",
          "page": 61
        },
        {
          "title": "12  Deployment Architecture",
          "page": 62
        },
        {
          "title": "13  Scalability Architecture",
          "page": 63
        },
        {
          "title": "14  Security Architecture",
          "page": 64
        },
        {
          "title": "15  Failure Recovery",
          "page": 65
        },
        {
          "title": "16  Monitoring & Observability",
          "page": 66
        },
        {
          "title": "17  Cost Optimization",
          "page": 67
        },
        {
          "title": "18  Engineering Challenges",
          "page": 68
        },
        {
          "title": "19  Architecture Tradeoffs",
          "page": 69
        },
        {
          "title": "20  Future Roadmap",
          "page": 70
        },
        {
          "title": "21  Interview Deep Dive",
          "page": 71
        },
        {
          "title": "22  Revision Sheet",
          "page": 72
        }
      ]
    },
    {
      "title": "04 ROVN",
      "items": [
        {
          "title": "01  Executive Summary",
          "page": 74
        },
        {
          "title": "02  Product Vision",
          "page": 75
        },
        {
          "title": "03  Business Problem",
          "page": 76
        },
        {
          "title": "04  User Journey",
          "page": 77
        },
        {
          "title": "05  Functional Requirements",
          "page": 78
        },
        {
          "title": "06  Non-Functional Requirements",
          "page": 79
        },
        {
          "title": "07  Tech Stack Decisions",
          "page": 80
        },
        {
          "title": "08  Architecture Overview",
          "page": 81
        },
        {
          "title": "09  Request Lifecycle",
          "page": 82
        },
        {
          "title": "10  Database Design",
          "page": 83
        },
        {
          "title": "11  Authentication Design",
          "page": 84
        },
        {
          "title": "12  Deployment Architecture",
          "page": 85
        },
        {
          "title": "13  Scalability Architecture",
          "page": 86
        },
        {
          "title": "14  Security Architecture",
          "page": 87
        },
        {
          "title": "15  Failure Recovery",
          "page": 88
        },
        {
          "title": "16  Monitoring & Observability",
          "page": 89
        },
        {
          "title": "17  Cost Optimization",
          "page": 90
        },
        {
          "title": "18  Engineering Challenges",
          "page": 91
        },
        {
          "title": "19  Architecture Tradeoffs",
          "page": 92
        },
        {
          "title": "20  Future Roadmap",
          "page": 93
        },
        {
          "title": "21  Interview Deep Dive",
          "page": 94
        },
        {
          "title": "22  Revision Sheet",
          "page": 95
        }
      ]
    },
    {
      "title": "05 TRAVIO",
      "items": [
        {
          "title": "01  Executive Summary",
          "page": 97
        },
        {
          "title": "02  Product Vision",
          "page": 98
        },
        {
          "title": "03  Business Problem",
          "page": 99
        },
        {
          "title": "04  User Journey",
          "page": 100
        },
        {
          "title": "05  Functional Requirements",
          "page": 101
        },
        {
          "title": "06  Non-Functional Requirements",
          "page": 102
        },
        {
          "title": "07  Tech Stack Decisions",
          "page": 103
        },
        {
          "title": "08  Architecture Overview",
          "page": 104
        },
        {
          "title": "09  Request Lifecycle",
          "page": 105
        },
        {
          "title": "10  Database Design",
          "page": 106
        },
        {
          "title": "11  Authentication Design",
          "page": 107
        },
        {
          "title": "12  Deployment Architecture",
          "page": 108
        },
        {
          "title": "13  Scalability Architecture",
          "page": 109
        },
        {
          "title": "14  Security Architecture",
          "page": 110
        },
        {
          "title": "15  Failure Recovery",
          "page": 111
        },
        {
          "title": "16  Monitoring & Observability",
          "page": 112
        },
        {
          "title": "17  Cost Optimization",
          "page": 113
        },
        {
          "title": "18  Engineering Challenges",
          "page": 114
        },
        {
          "title": "19  Architecture Tradeoffs",
          "page": 115
        },
        {
          "title": "20  Future Roadmap",
          "page": 116
        },
        {
          "title": "21  Interview Deep Dive",
          "page": 117
        },
        {
          "title": "22  Revision Sheet",
          "page": 118
        }
      ]
    },
    {
      "title": "06 GRINDOS",
      "items": [
        {
          "title": "01  Executive Summary",
          "page": 120
        },
        {
          "title": "02  Product Vision",
          "page": 121
        },
        {
          "title": "03  Business Problem",
          "page": 122
        },
        {
          "title": "04  User Journey",
          "page": 123
        },
        {
          "title": "05  Functional Requirements",
          "page": 124
        },
        {
          "title": "06  Non-Functional Requirements",
          "page": 125
        },
        {
          "title": "07  Tech Stack Decisions",
          "page": 126
        },
        {
          "title": "08  Architecture Overview",
          "page": 127
        },
        {
          "title": "09  Request Lifecycle",
          "page": 128
        },
        {
          "title": "10  Database Design",
          "page": 129
        },
        {
          "title": "11  Authentication Design",
          "page": 130
        },
        {
          "title": "12  Deployment Architecture",
          "page": 131
        },
        {
          "title": "13  Scalability Architecture",
          "page": 132
        },
        {
          "title": "14  Security Architecture",
          "page": 133
        },
        {
          "title": "15  Failure Recovery",
          "page": 134
        },
        {
          "title": "16  Monitoring & Observability",
          "page": 135
        },
        {
          "title": "17  Cost Optimization",
          "page": 136
        },
        {
          "title": "18  Engineering Challenges",
          "page": 137
        },
        {
          "title": "19  Architecture Tradeoffs",
          "page": 138
        },
        {
          "title": "20  Future Roadmap",
          "page": 139
        },
        {
          "title": "21  Interview Deep Dive",
          "page": 140
        },
        {
          "title": "22  Revision Sheet",
          "page": 141
        }
      ]
    },
    {
      "title": "07 SANKALAN",
      "items": [
        {
          "title": "01  Executive Summary",
          "page": 143
        },
        {
          "title": "02  Product Vision",
          "page": 144
        },
        {
          "title": "03  Business Problem",
          "page": 145
        },
        {
          "title": "04  User Journey",
          "page": 146
        },
        {
          "title": "05  Functional Requirements",
          "page": 147
        },
        {
          "title": "06  Non-Functional Requirements",
          "page": 148
        },
        {
          "title": "07  Tech Stack Decisions",
          "page": 149
        },
        {
          "title": "08  Architecture Overview",
          "page": 150
        },
        {
          "title": "09  Request Lifecycle",
          "page": 151
        },
        {
          "title": "10  Database Design",
          "page": 152
        },
        {
          "title": "11  Authentication Design",
          "page": 153
        },
        {
          "title": "12  Deployment Architecture",
          "page": 154
        },
        {
          "title": "13  Scalability Architecture",
          "page": 155
        },
        {
          "title": "14  Security Architecture",
          "page": 156
        },
        {
          "title": "15  Failure Recovery",
          "page": 157
        },
        {
          "title": "16  Monitoring & Observability",
          "page": 158
        },
        {
          "title": "17  Cost Optimization",
          "page": 159
        },
        {
          "title": "18  Engineering Challenges",
          "page": 160
        },
        {
          "title": "19  Architecture Tradeoffs",
          "page": 161
        },
        {
          "title": "20  Future Roadmap",
          "page": 162
        },
        {
          "title": "21  Interview Deep Dive",
          "page": 163
        },
        {
          "title": "22  Revision Sheet",
          "page": 164
        }
      ]
    }
  ]
};
