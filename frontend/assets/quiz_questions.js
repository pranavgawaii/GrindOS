const QUIZ_QUESTIONS = {
  dbms: [
    {
      id: "dbms_q1",
      topic: "001",
      question: "Which of the following best describes the relationship between 'Data' and 'Information'?",
      options: [
        "Data is processed information, whereas information is raw facts.",
        "Data represents raw, unorganized facts, whereas information is processed, structured, and meaningful data.",
        "Data and information are completely identical in database contexts.",
        "Information is stored in database files, while data exists only in application memory."
      ],
      answer: 1,
      explanation: "Data is the raw facts and figures without context, while information is data that has been processed, organized, and presented in a structured, meaningful context."
    },
    {
      id: "dbms_q2",
      topic: "002",
      question: "Which type of database is optimized for storing hierarchical relationships and traversing interconnected nodes?",
      options: [
        "Relational Database",
        "Document Database",
        "Graph Database",
        "Key-Value Store"
      ],
      answer: 2,
      explanation: "Graph databases use nodes, edges, and properties to represent and store data, which makes them highly optimized for traversing networks and analyzing complex relationships."
    },
    {
      id: "dbms_q3",
      topic: "003",
      question: "Which of the following is a primary function of a Database Management System (DBMS)?",
      options: [
        "To compile high-level programming languages into machine code.",
        "To provide a secure, centralized interface for storing, retrieving, and managing data with concurrency control.",
        "To directly manage hardware network routing tables.",
        "To operate as the primary operating system kernel."
      ],
      answer: 1,
      explanation: "A DBMS provides a systematic way to create, retrieve, update, manage, and control access to data, supporting multi-user transaction integrity and security."
    },
    {
      id: "dbms_q4",
      topic: "005",
      question: "In the 3-Schema Architecture, which level of data abstraction defines how the data is physically stored on disk storage?",
      options: [
        "External Level / View Level",
        "Conceptual Level / Logical Level",
        "Internal Level / Physical Level",
        "Interface Level"
      ],
      answer: 2,
      explanation: "The Internal (or Physical) level defines the physical storage structure, file organization, indexing details, and access paths of the database on disk."
    },
    {
      id: "dbms_q5",
      topic: "006",
      question: "What is a major characteristic of a 3-tier DBMS architecture compared to a 2-tier architecture?",
      options: [
        "The application layer is merged directly into the database server.",
        "An intermediate application server lies between the client UI and the database backend, enhancing security and scalability.",
        "Clients interact directly with database files without any network protocols.",
        "Data redundancy is completely eliminated by removing logical schemas."
      ],
      answer: 1,
      explanation: "In a 3-tier architecture, the client (Presentation tier) communicates with an Application Server (Business Logic tier), which then queries the Database Server (Data tier). This decoupling improves security, modularity, and scalability."
    },
    {
      id: "dbms_q6",
      topic: "010",
      question: "In an Entity-Relationship (ER) model, what is represented by a double rectangle?",
      options: [
        "Multivalued Attribute",
        "Weak Entity Set",
        "Identifying Relationship Set",
        "Derived Attribute"
      ],
      answer: 1,
      explanation: "A weak entity set (which doesn't have a primary key of its own and depends on a strong entity) is represented by a double rectangle in ER diagrams."
    },
    {
      id: "dbms_q7",
      topic: "018",
      question: "What is the difference between the 'Intension' and 'Extension' of a database?",
      options: [
        "Intension is the database schema (metadata) which rarely changes; Extension is the database state (actual data) at a specific moment.",
        "Intension is the internal storage code; Extension is the external cloud replication layer.",
        "Intension represents user permissions; Extension represents SQL queries.",
        "Extension is the database schema; Intension is the database state."
      ],
      answer: 0,
      explanation: "The Intension of a database refers to its schema design/metadata structure, which is constant. The Extension is the actual population of data stored in it at any given point in time, which changes frequently."
    },
    {
      id: "dbms_q8",
      topic: "026",
      question: "Which of the following commands belongs to the Data Definition Language (DDL) in SQL?",
      options: [
        "SELECT",
        "INSERT",
        "ALTER",
        "GRANT"
      ],
      answer: 2,
      explanation: "DDL commands (like CREATE, ALTER, DROP, TRUNCATE) define or modify the structure of database schemas. INSERT is DML, SELECT is DQL, and GRANT is DCL."
    },
    {
      id: "dbms_q9",
      topic: "041",
      question: "Which NoSQL data model stores data in JSON-like structures and allows nested arrays or documents?",
      options: [
        "Key-Value Store",
        "Document-Oriented Database",
        "Column-Family Store",
        "Graph Database"
      ],
      answer: 1,
      explanation: "Document databases (like MongoDB) store semi-structured data as documents, typically using formats like JSON or BSON, enabling nested fields and dynamic schemas."
    },
    {
      id: "dbms_q10",
      topic: "056",
      question: "How does the Two-Phase Locking (2PL) protocol ensure serializability?",
      options: [
        "By enforcing that all lock acquisitions happen in the Growing Phase and all lock releases happen in the Shrinking Phase.",
        "By requiring all transactions to run in a single-threaded queue.",
        "By dynamically aborting transactions if they read uncommitted data.",
        "By avoiding locks altogether and using timestamp ordering."
      ],
      answer: 0,
      explanation: "The 2PL protocol divides locking into two distinct phases: Growing (locks are acquired, none released) and Shrinking (locks are released, none acquired). This guarantees serializability of execution schedules."
    },
    {
      id: "dbms_q11",
      topic: "073",
      question: "What is the primary role of the Log Sequence Number (LSN) in Write-Ahead Logging (WAL) recovery?",
      options: [
        "To count the number of users connected to the server.",
        "To uniquely identify database transactions in sequential order.",
        "To sequence log records and page modifications, ensuring changes are written to disk logs before pages are updated in place.",
        "To store backup files in secondary storage automatically."
      ],
      answer: 2,
      explanation: "LSNs index log records. The Write-Ahead Logging protocol dictates that the log record corresponding to a page modification (with a matching LSN) must be flushed to non-volatile storage before the database page itself is written to disk."
    },
    {
      id: "dbms_q12",
      topic: "075",
      question: "Why are B+ Trees preferred over standard Binary Search Trees for database indexes?",
      options: [
        "B+ Trees have a higher height, which makes search queries take longer but consume less memory.",
        "B+ Trees are balanced multi-way trees with high fan-out, reducing disk page reads, and all actual keys/pointers are stored in linked leaf nodes for range scans.",
        "Binary Search Trees cannot store string data.",
        "B+ Trees do not support index lookups, only linear scans."
      ],
      answer: 1,
      explanation: "B+ trees are shallow, wide trees (high fan-out) which minimizes disk I/O operations—the main bottleneck in database storage. The linked leaf nodes also allow highly efficient sorted range queries."
    }
  ],
  cn: [
    {
      id: "cn_q1",
      topic: "001",
      question: "Which network topology features a central hub or switch to which all other nodes are directly connected?",
      options: [
        "Mesh Topology",
        "Bus Topology",
        "Star Topology",
        "Ring Topology"
      ],
      answer: 2,
      explanation: "In a Star topology, all devices are connected to a central controller/hub/switch, which acts as a repeater and router for data packets."
    },
    {
      id: "cn_q2",
      topic: "002",
      question: "Which layer of the OSI model is responsible for routing packets across multiple networks, logical addressing, and path determination?",
      options: [
        "Data Link Layer",
        "Network Layer",
        "Transport Layer",
        "Physical Layer"
      ],
      answer: 1,
      explanation: "The Network layer (Layer 3) handles logical addressing (IP addresses), packet routing, and forwarding across networks."
    },
    {
      id: "cn_q3",
      topic: "003",
      question: "Which layer of the TCP/IP protocol suite corresponds to the Network layer of the OSI model?",
      options: [
        "Network Access Layer",
        "Application Layer",
        "Transport Layer",
        "Internet Layer"
      ],
      answer: 3,
      explanation: "The TCP/IP Internet layer maps directly to the OSI Network layer. It is responsible for logical packet addressing and routing (IP, ICMP, ARP)."
    },
    {
      id: "cn_q4",
      topic: "005",
      question: "Which transmission medium is immune to electromagnetic interference (EMI) and uses light pulses for data propagation?",
      options: [
        "Coaxial Cable",
        "Fiber Optic Cable",
        "Unshielded Twisted Pair (UTP)",
        "Radio Waves"
      ],
      answer: 1,
      explanation: "Fiber optic cables transmit data using light pulses inside glass/plastic fibers, which completely eliminates susceptibility to electromagnetic interference (EMI)."
    },
    {
      id: "cn_q5",
      topic: "010",
      question: "What is the network address of the Class C IP address 192.168.10.45 with a standard subnet mask (255.255.255.0)?",
      options: [
        "192.168.0.0",
        "192.168.10.0",
        "192.168.10.255",
        "192.0.0.0"
      ],
      answer: 1,
      explanation: "A Class C address has a 24-bit network prefix. Performing a bitwise AND of 192.168.10.45 and 255.255.255.0 yields the network address 192.168.10.0."
    },
    {
      id: "cn_q6",
      topic: "015",
      question: "Which of the following statement is correct regarding MAC addresses and IP addresses?",
      options: [
        "MAC addresses are logical and assigned by network administrators; IP addresses are physical and burned into the NIC.",
        "MAC addresses are physical (48-bit hex) and globally unique to the hardware NIC; IP addresses are logical (32-bit/128-bit) and represent location in a network.",
        "Both MAC and IP addresses are automatically assigned by the operating system kernel on boot.",
        "MAC addresses are only used on the Internet, while IP addresses are used locally."
      ],
      answer: 1,
      explanation: "MAC addresses (Layer 2) are physical, flat addresses hardcoded into the network interface card (NIC). IP addresses (Layer 3) are logical, hierarchical addresses assigned to identify host locations on a network."
    },
    {
      id: "cn_q7",
      topic: "020",
      question: "Which algorithm is used by Link State routing protocols like OSPF to compute the shortest routing path?",
      options: [
        "Bellman-Ford Algorithm",
        "Dijkstra's Algorithm",
        "Kruskal's Algorithm",
        "Floyd-Warshall Algorithm"
      ],
      answer: 1,
      explanation: "Link-state routing protocols (like OSPF) build a complete topological map of the network and run Dijkstra's shortest-path first (SPF) algorithm to calculate the optimal path to all destinations."
    },
    {
      id: "cn_q8",
      topic: "025",
      question: "Which of the following properties is characteristic of UDP (User Datagram Protocol) compared to TCP?",
      options: [
        "Reliable delivery guaranteed via sequence numbers and ACKs.",
        "Connection-oriented setup via a three-way handshake.",
        "Low-overhead, connectionless, and best-effort transmission without flow or congestion control.",
        "Enforces byte-stream segmentation."
      ],
      answer: 2,
      explanation: "UDP is a lightweight, connectionless protocol that sends datagrams without establishing a handshake, sequencing packets, or verifying receipt, making it faster and suitable for real-time traffic like streaming or gaming."
    },
    {
      id: "cn_q9",
      topic: "030",
      question: "In DNS resolution, what is the role of a Recursive Resolver?",
      options: [
        "To store authoritative zone records directly for public domains.",
        "To act as the client's agent, querying various DNS servers (Root, TLD, Authoritative) in sequence to locate and return the IP address.",
        "To encrypt HTTP packets during data transfer.",
        "To route physical packets between local networks."
      ],
      answer: 1,
      explanation: "A recursive resolver (usually provided by an ISP or public DNS provider like 8.8.8.8) receives queries from clients and executes iterative queries across Root, TLD, and Authoritative servers on the client's behalf."
    },
    {
      id: "cn_q10",
      topic: "035",
      question: "During a secure HTTPS connection setup, how are encryption keys exchanged using SSL/TLS?",
      options: [
        "The client and server share a static, unencrypted password.",
        "Asymmetric encryption is used to securely exchange or agree upon a temporary symmetric session key, which is then used to encrypt the actual data stream.",
        "The symmetric key is sent as cleartext inside the first TCP SYN packet.",
        "No keys are used; the connection relies entirely on physical security of the undersea fiber."
      ],
      answer: 1,
      explanation: "The TLS handshake uses public-key (asymmetric) cryptography to authenticate the server and securely negotiate a shared secret (symmetric key). Symmetric cryptography is then used to encrypt communications because it is computationally faster."
    }
  ],
  os: [
    {
      id: "os_q1",
      topic: "001",
      question: "What is the primary difference between a Process and a Thread?",
      options: [
        "A process is a lightweight execution unit; a thread is a heavyweight application.",
        "Processes share the same memory space directly; threads always have isolated memory spaces.",
        "A process is an independent program in execution with its own isolated address space; a thread is a unit of execution within a process that shares the process's code, data, and resources.",
        "Threads cannot run concurrently, whereas processes always run in parallel."
      ],
      answer: 2,
      explanation: "Processes are isolated resource containers. Threads are light execution paths within a parent process that share its global memory (code, data, heap) but have private stacks and registers."
    },
    {
      id: "os_q2",
      topic: "002",
      question: "Which CPU scheduling algorithm is non-preemptive and selects the process with the smallest execution time next, but can lead to starvation of longer processes?",
      options: [
        "First-Come, First-Served (FCFS)",
        "Shortest Job First (SJF)",
        "Round Robin (RR)",
        "Priority Scheduling (Preemptive)"
      ],
      answer: 1,
      explanation: "Shortest Job First (SJF) schedules the process with the minimum CPU burst time. While mathematically optimal for minimizing average waiting time, it can cause starvation if shorter tasks continuously enter the queue."
    },
    {
      id: "os_q3",
      topic: "003",
      question: "What is 'context switching overhead'?",
      options: [
        "The time the CPU spends writing output logs to the hard disk.",
        "The idle CPU time wasted while saving the register state of the running process and loading the state of the next scheduled process from its PCB.",
        "The network latency when switching from Wi-Fi to cellular data.",
        "The battery consumption of multitasking operating systems."
      ],
      answer: 1,
      explanation: "Context switching requires saving the CPU registers, program counter, and stack pointer of the current process into its Process Control Block (PCB), and loading the new process state from its PCB. During this time, the CPU performs no productive work."
    },
    {
      id: "os_q4",
      topic: "004",
      question: "How does a Multilevel Feedback Queue (MLFQ) scheduler prevent process starvation?",
      options: [
        "By executing all processes in a strict circular queue.",
        "By dynamically moving processes that wait too long in lower-priority queues to higher-priority queues (aging).",
        "By allocating equal CPU shares to all users.",
        "By termination of long running tasks automatically."
      ],
      answer: 1,
      explanation: "MLFQ schedulers prevent starvation using 'aging': if a process waits in a low-priority queue for too long, the scheduler boosts its priority queue level so it eventually executes."
    },
    {
      id: "os_q5",
      topic: "005",
      question: "In a paged memory system, how is the logical address translated to a physical address?",
      options: [
        "The logical address is looked up directly in a linear disk index.",
        "The page number (p) is used as an index into the Page Table to find the physical frame number (f), which is then combined with the offset (d) to yield the physical address.",
        "By multiplying the page offset by the total memory size.",
        "Through direct physical hardware registers without any translation tables."
      ],
      answer: 1,
      explanation: "A logical address consists of a page number and an offset. The MMU uses the page number to query the page table for the corresponding physical page frame. The offset remains unchanged and is appended to the frame address."
    },
    {
      id: "os_q6",
      topic: "006",
      question: "What is a key difference between Paging and Segmentation?",
      options: [
        "Paging divides memory into fixed-size blocks (pages); segmentation divides memory into variable-sized logical segments based on program structure (code, heap, stack).",
        "Segmentation suffers from internal fragmentation; paging suffers from external fragmentation.",
        "Paging is managed entirely by users, while segmentation is managed by physical hard disks.",
        "There is no difference; they are synonymous."
      ],
      answer: 0,
      explanation: "Paging is a physical allocation technique using uniform blocks, preventing external fragmentation. Segmentation divides memory into variable logical units representing code segments, stack, or variables, which can lead to external fragmentation."
    },
    {
      id: "os_q7",
      topic: "007",
      question: "What sequence of events is triggered when a process attempts to access a page marked as invalid (not present in main memory) in its page table?",
      options: [
        "The operating system crashes immediately.",
        "A page fault exception is generated, causing the OS to trap to the kernel, load the page from disk into a free frame, update the page table, and restart the instruction.",
        "The memory controller writes random data into the page table.",
        "The process is skipped and the next process in the ready queue is executed."
      ],
      answer: 1,
      explanation: "An invalid page access triggers a Page Fault. The OS handles this hardware trap by locating the page on disk (swap space), swapping it into physical memory (resolving any page replacement), updating the page table valid bit to 1, and restarting the faulted instruction."
    },
    {
      id: "os_q8",
      topic: "008",
      question: "Which page replacement algorithm replaces the page that has not been used for the longest period of time?",
      options: [
        "First-In, First-Out (FIFO)",
        "Least Recently Used (LRU)",
        "Optimal Page Replacement (OPT)",
        "Least Frequently Used (LFU)"
      ],
      answer: 1,
      explanation: "The Least Recently Used (LRU) algorithm tracks the history of page accesses and swaps out the page that has been idle for the longest duration, approximating optimal behavior based on temporal locality."
    },
    {
      id: "os_q9",
      topic: "010",
      question: "What is the key difference between a Binary Semaphore and a Mutex?",
      options: [
        "Mutexes can be incremented up to any integer value, while binary semaphores are strictly 0 and 1.",
        "A Mutex has the concept of ownership—only the thread that locked the Mutex can unlock it. A binary semaphore does not have ownership and can be signaled/unlocked by any thread.",
        "Binary semaphores are implemented in hardware, while mutexes are software-only constructs.",
        "Mutexes cause starvation, whereas binary semaphores prevent it."
      ],
      answer: 1,
      explanation: "Mutexes are locking mechanisms intended to serialize access to a resource and enforce ownership (lock and unlock must be called by the same thread). Semaphores are signaling mechanisms and can be posted/waited on by different threads."
    }
  ],
  oops: [
    {
      id: "oops_q1",
      topic: "001",
      question: "What is the relationship between a Class and an Object?",
      options: [
        "An object is a blueprint or template; a class is a concrete instance of that blueprint.",
        "A class is a static description of data; an object is a file containing that data.",
        "A class is a blueprint or prototype that defines variables and methods; an object is a concrete instance of a class that occupies memory.",
        "There is no operational difference between a class and an object."
      ],
      answer: 2,
      explanation: "A class acts as the template or schema defining the properties and behaviors (variables and functions). An object is a runtime instance created from that class template that holds state in memory."
    },
    {
      id: "oops_q2",
      topic: "002",
      question: "Which access modifier restricts access to members so they are visible only within the class itself and to derived (inherited) classes, but not to external classes?",
      options: [
        "private",
        "protected",
        "public",
        "default/package"
      ],
      answer: 1,
      explanation: "Protected members are accessible within their own class and by subclass (inherited) instances, but hidden from unrelated external package classes."
    },
    {
      id: "oops_q3",
      topic: "003",
      question: "How does Abstraction differ from Encapsulation?",
      options: [
        "Abstraction is the process of hiding implementation details and showing only essential features; Encapsulation is the process of binding data and functions into a single unit (class) to prevent direct external access.",
        "Abstraction hides data inside private variables, while encapsulation displays the source code.",
        "Abstraction is used in Java; Encapsulation is used in Python.",
        "Abstraction is a structural inheritance pattern; Encapsulation is a compiler optimization."
      ],
      answer: 0,
      explanation: "Abstraction focuses on 'what' an object does (exposing a simple interface and hiding complexity). Encapsulation focuses on 'how' it does it, binding data and behavior together and restricting direct variable access (information hiding)."
    },
    {
      id: "oops_q4",
      topic: "004",
      question: "In Python, which algorithm is used to resolve the Method Resolution Order (MRO) in multiple inheritance hierarchies?",
      options: [
        "Dijkstra's Path Resolution Algorithm",
        "C3 Linearization Algorithm",
        "Depth First Search (DFS)",
        "Post-Order Traversal"
      ],
      answer: 1,
      explanation: "Python uses the C3 Linearization algorithm to determine a consistent Method Resolution Order (MRO) when dealing with complex multiple inheritance (e.g., the Diamond Problem)."
    },
    {
      id: "oops_q5",
      topic: "005",
      question: "What is the difference between Method Overloading and Method Overriding?",
      options: [
        "Overloading is compile-time (static) polymorphism where multiple methods have the same name but different signatures. Overriding is runtime (dynamic) polymorphism where a subclass provides a specific implementation of a parent class method.",
        "Overriding is only possible in Python; overloading is only possible in C++.",
        "Overloading replaces the parent class method, while overriding adds new variables to it.",
        "Overloading requires inheritance, whereas overriding does not."
      ],
      answer: 0,
      explanation: "Overloading defines multiple methods with the same name but different parameters within the same scope. Overriding occurs when a subclass redefines a method with the same signature inherited from a parent class, resolved dynamically at runtime."
    },
    {
      id: "oops_q6",
      topic: "008",
      question: "What is the primary purpose of a Constructor in Object-Oriented Programming?",
      options: [
        "To compile class files into machine code.",
        "To delete objects and free memory when they go out of scope.",
        "To initialize the state of an object immediately upon its creation.",
        "To copy variable definitions to other classes."
      ],
      answer: 2,
      explanation: "A constructor is a special member function that is automatically invoked when an object is instantiated, allocated memory, and initialized with default or user-supplied starting values."
    },
    {
      id: "oops_q7",
      topic: "010",
      question: "Why is 'Composition' often preferred over 'Inheritance' in OOP design?",
      options: [
        "Composition is much faster to execute than inheritance.",
        "Composition represents a tight 'IS-A' binding, making it easier to share code directly.",
        "Composition creates a loose 'HAS-A' relationship, allowing components to be swapped out dynamically at runtime and reducing class hierarchy coupling.",
        "Composition does not require creating objects."
      ],
      answer: 2,
      explanation: "Inheritance ('IS-A') creates a tight, compile-time dependency on parent class internals (breaking encapsulation). Composition ('HAS-A') delegates behavior to helper objects, keeping interfaces clean, modular, and dynamic at runtime."
    }
  ],

  dsa: [
    {
      id: "dsa_q1",
      topic: "002",
      question: "What is the time complexity of binary search on a sorted array of n elements?",
      options: ["O(n)", "O(log n)", "O(n log n)", "O(1)"],
      answer: 1,
      explanation: "Binary search halves the search space at each step, so it takes at most log₂(n) comparisons. This gives O(log n) time complexity."
    },
    {
      id: "dsa_q4",
      topic: "007",
      question: "The Sliding Window technique is most useful for problems involving:",
      options: [
        "Finding shortest path in a graph",
        "Contiguous subarrays or substrings satisfying some condition",
        "Sorting a list in O(n log n)",
        "Finding the LCA in a binary tree"
      ],
      answer: 1,
      explanation: "Sliding Window maintains a window of elements and slides it across the array, making it ideal for contiguous subarray/substring problems like maximum sum subarray of size k."
    },

    {
      id: "dsa_q5",
      topic: "012",
      question: "What is the time complexity to access the k-th element in a singly linked list?",
      options: ["O(1)", "O(log n)", "O(k)", "O(n²)"],
      answer: 2,
      explanation: "Linked lists do not support random access. To reach the k-th node you must traverse from the head, taking O(k) time — O(n) in the worst case."
    },
    {
      id: "dsa_q6",
      topic: "016",
      question: "Which data structure uses LIFO (Last In, First Out) ordering?",
      options: ["Queue", "Stack", "Deque", "Priority Queue"],
      answer: 1,
      explanation: "A Stack follows LIFO — the last element pushed is the first one popped. Classic uses include undo operations, function call stacks, and expression parsing."
    },
    {
      id: "dsa_q7",
      topic: "021",
      question: "On average, what is the time complexity of lookup in a well-implemented hash table?",
      options: ["O(n)", "O(log n)", "O(1)", "O(n log n)"],
      answer: 2,
      explanation: "Hash tables use a hash function to map keys to array indices, giving O(1) average lookup. Worst case is O(n) due to collisions, but good hash functions make this rare."
    },
    {
      id: "dsa_q8",
      topic: "025",
      question: "In a Binary Tree, which traversal visits nodes in Left → Root → Right order?",
      options: ["Preorder", "Inorder", "Postorder", "Level-order"],
      answer: 1,
      explanation: "Inorder traversal visits Left subtree → Root → Right subtree. For a BST, inorder traversal produces elements in sorted ascending order."
    },
    {
      id: "dsa_q9",
      topic: "026",
      question: "What property makes a Binary Search Tree (BST) efficient for search?",
      options: [
        "All nodes have exactly two children",
        "Left child < parent < right child at every node",
        "The tree is always perfectly balanced",
        "Nodes are stored in a sorted array"
      ],
      answer: 1,
      explanation: "BST ordering property (left < root < right) allows eliminating half the remaining nodes at each step during search, giving O(h) time where h is tree height."
    },
    {
      id: "dsa_q10",
      topic: "040",
      question: "Dijkstra's algorithm fails on graphs with:",
      options: [
        "Weighted edges",
        "Negative weight edges",
        "Disconnected components",
        "More than 1000 nodes"
      ],
      answer: 1,
      explanation: "Dijkstra's greedy approach assumes that once a node is visited, its shortest path won't improve. Negative edges can violate this assumption. Use Bellman-Ford for graphs with negative weights."
    },
    {
      id: "dsa_q11",
      topic: "049",
      question: "Which condition is REQUIRED for Dynamic Programming to be applicable?",
      options: [
        "The problem must be solvable in polynomial time",
        "The problem must have optimal substructure and overlapping subproblems",
        "The problem must involve graph traversal",
        "The input must be a sorted array"
      ],
      answer: 1,
      explanation: "DP requires both optimal substructure (optimal solution can be built from optimal sub-solutions) and overlapping subproblems (same subproblems are solved multiple times). Without both, DP is unnecessary."
    },
    {
      id: "dsa_q12",
      topic: "045",
      question: "What is the time complexity of Merge Sort in the worst case?",
      options: ["O(n)", "O(n log n)", "O(n²)", "O(log n)"],
      answer: 1,
      explanation: "Merge Sort always divides the array in half (log n levels) and merges in O(n) time per level, giving O(n log n) in all cases — best, average, and worst."
    },
    {
      id: "dsa_q13",
      topic: "047",
      question: "Binary Search can only be applied when the input array is:",
      options: ["Unsorted", "Sorted", "Of even length", "Contains no duplicates"],
      answer: 1,
      explanation: "Binary Search requires the array to be sorted. It compares the target with the mid element and discards half the array — this only works correctly on sorted data."
    },
    {
      id: "dsa_q14",
      topic: "033",
      question: "In a Min-Heap, the element at the root is always:",
      options: [
        "The maximum element",
        "The minimum element",
        "The median element",
        "A random element"
      ],
      answer: 1,
      explanation: "A Min-Heap maintains the heap property: every parent ≤ its children. Therefore the root is always the smallest element, giving O(1) access to the minimum."
    },
    {
      id: "dsa_q15",
      topic: "038",
      question: "Which graph traversal algorithm uses a queue (FIFO) data structure?",
      options: ["DFS (Depth-First Search)", "BFS (Breadth-First Search)", "Dijkstra's Algorithm", "Topological Sort"],
      answer: 1,
      explanation: "BFS explores nodes level by level using a queue. It processes all neighbors at distance 1 before moving to distance 2, making it ideal for finding shortest paths in unweighted graphs."
    },
    {
      id: "dsa_q16",
      topic: "062",
      question: "Backtracking improves over brute force by:",
      options: [
        "Using dynamic programming to store results",
        "Abandoning a solution candidate as soon as it's determined to be invalid",
        "Sorting the input before processing",
        "Parallelizing computation across threads"
      ],
      answer: 1,
      explanation: "Backtracking prunes the search space by abandoning (backtracking from) a path as soon as it's detected that this path cannot lead to a valid solution, unlike brute force which explores every possibility."
    },
    {
      id: "dsa_q17",
      topic: "065",
      question: "What does the operation `n & (n-1)` do in bit manipulation?",
      options: [
        "Returns the lowest set bit of n",
        "Clears the lowest set bit of n",
        "Returns n + 1",
        "Checks if n is a power of 2"
      ],
      answer: 1,
      explanation: "`n & (n-1)` clears the lowest set bit of n. This is because subtracting 1 from n flips all bits up to and including the lowest set bit. If `n & (n-1) == 0`, then n is a power of 2."
    },
    {
      id: "dsa_q18",
      topic: "042",
      question: "Union-Find (Disjoint Set Union) is primarily used for:",
      options: [
        "Shortest path problems",
        "Detecting cycles and grouping connected components in a graph",
        "Sorting elements in O(n log n)",
        "Finding the maximum flow in a network"
      ],
      answer: 1,
      explanation: "Union-Find maintains a collection of disjoint sets and supports two operations efficiently: Union (merge two sets) and Find (determine which set an element belongs to). It's used in Kruskal's MST and cycle detection."
    },
    {
      id: "dsa_q19",
      topic: "032",
      question: "A Trie data structure is most efficient for:",
      options: [
        "Finding the median of a stream",
        "Prefix-based string search and autocomplete",
        "Shortest path in a weighted graph",
        "Balancing a binary search tree"
      ],
      answer: 1,
      explanation: "A Trie stores strings character by character, allowing O(m) prefix lookups where m is the query length — independent of the number of stored strings. Ideal for autocomplete, spell checking, and IP routing."
    },
    {
      id: "dsa_q20",
      topic: "053",
      question: "In the 0-1 Knapsack problem, 'fractional' weights are:",
      options: [
        "Allowed — you can take any fraction of an item",
        "Not allowed — each item is either taken completely or not at all",
        "Optional depending on item type",
        "Only allowed if the item value exceeds the capacity"
      ],
      answer: 1,
      explanation: "In the 0-1 Knapsack, each item must be either included fully (1) or excluded (0) — no fractions. For fractional knapsack (where fractions are allowed), a greedy approach by value/weight ratio works optimally."
    }
  ],

  webdev: [
    {
      id: "webdev_q1",
      topic: "002",
      question: "What is the main difference between HTTP and HTTPS?",
      options: [
        "HTTPS uses a different port and is slower than HTTP",
        "HTTPS encrypts traffic using TLS, providing secure communication",
        "HTTP supports more request methods than HTTPS",
        "HTTPS is only used for file downloads"
      ],
      answer: 1,
      explanation: "HTTPS (HTTP Secure) wraps HTTP in TLS (Transport Layer Security), encrypting all data in transit. This prevents man-in-the-middle attacks and eavesdropping. HTTP sends data in plain text."
    },
    {
      id: "webdev_q2",
      topic: "005",
      question: "Which HTML element is the correct semantic choice for the main navigation links of a website?",
      options: ["<div class='nav'>", "<section>", "<nav>", "<menu>"],
      answer: 2,
      explanation: "The <nav> element is the semantic HTML5 element specifically designed for navigation links. It helps screen readers and search engines understand the document's navigation structure."
    },
    {
      id: "webdev_q3",
      topic: "010",
      question: "In the CSS Box Model, which property (by default) is NOT included in an element's declared width?",
      options: ["Content", "Padding", "Border", "Margin"],
      answer: 3,
      explanation: "By default (box-sizing: content-box), width applies to content only. Padding and border are added outside. With box-sizing: border-box (recommended), width includes padding and border but never margin."
    },
    {
      id: "webdev_q4",
      topic: "011",
      question: "Which flexbox property controls spacing of items along the main axis?",
      options: ["align-items", "justify-content", "align-content", "flex-direction"],
      answer: 1,
      explanation: "justify-content controls how flex items are distributed along the main axis (horizontal for row, vertical for column). align-items controls alignment on the cross axis."
    },
    {
      id: "webdev_q5",
      topic: "017",
      question: "JavaScript is described as 'single-threaded' which means:",
      options: [
        "It can only handle one variable at a time",
        "It executes one operation at a time on a single call stack",
        "It cannot perform asynchronous operations",
        "It runs on only one CPU core permanently"
      ],
      answer: 1,
      explanation: "JavaScript has one call stack — it can only execute one piece of code at a time. Asynchronous operations (timers, fetch) are delegated to Web APIs and their callbacks are queued, but JS itself processes them one at a time via the event loop."
    },
    {
      id: "webdev_q6",
      topic: "019",
      question: "What does `Promise.all([p1, p2, p3])` do when p2 rejects?",
      options: [
        "Waits for all promises to settle before resolving",
        "Immediately rejects with p2's rejection reason",
        "Resolves with partial results from p1 and p3",
        "Ignores the rejection and resolves with undefined for p2"
      ],
      answer: 1,
      explanation: "Promise.all fails fast — if any promise rejects, the entire Promise.all rejects immediately with that rejection reason. Use Promise.allSettled if you want results from all promises regardless of individual failures."
    },
    {
      id: "webdev_q7",
      topic: "020",
      question: "What does ES6 destructuring assignment allow you to do?",
      options: [
        "Delete properties from an object",
        "Unpack values from arrays or properties from objects into distinct variables",
        "Create a deep copy of an object",
        "Merge two objects together"
      ],
      answer: 1,
      explanation: "Destructuring lets you extract values/properties in a concise syntax: `const {name, age} = user;` or `const [first, second] = arr;`. It avoids repetitive property access and makes code cleaner."
    },
    {
      id: "webdev_q8",
      topic: "028",
      question: "In React, what triggers a component to re-render?",
      options: [
        "Only when the parent component re-renders",
        "When its state or props change",
        "On every JavaScript timer tick",
        "Only when the user interacts with it"
      ],
      answer: 1,
      explanation: "React re-renders a component when its state changes (via setState or useState setter) or when its props change. Parent re-renders also cause child re-renders unless the child is wrapped with React.memo."
    },
    {
      id: "webdev_q9",
      topic: "029",
      question: "The React hook `useEffect` with an empty dependency array `[]` runs:",
      options: [
        "On every render",
        "Only once after the initial render",
        "Only when the component unmounts",
        "Before every render"
      ],
      answer: 1,
      explanation: "useEffect(() => { ... }, []) runs once after the first render (mount), equivalent to componentDidMount in class components. The cleanup function returned runs on unmount."
    },
    {
      id: "webdev_q10",
      topic: "034",
      question: "In Next.js App Router, which rendering strategy fetches data at build time and serves static HTML?",
      options: [
        "SSR (Server-Side Rendering)",
        "CSR (Client-Side Rendering)",
        "SSG (Static Site Generation)",
        "ISR (Incremental Static Regeneration)"
      ],
      answer: 2,
      explanation: "SSG (Static Site Generation) generates HTML at build time. The pre-built pages are served from a CDN with no per-request server computation, making it the fastest strategy for content that doesn't change frequently."
    },
    {
      id: "webdev_q11",
      topic: "035",
      question: "What is the Node.js Event Loop responsible for?",
      options: [
        "Executing CPU-intensive computations in parallel",
        "Offloading async operations and processing their callbacks when complete",
        "Managing memory allocation for JavaScript objects",
        "Parsing and compiling JavaScript code"
      ],
      answer: 1,
      explanation: "The Event Loop allows Node.js to perform non-blocking I/O by delegating async operations (file system, network) to the OS and processing callbacks when those operations complete, despite JavaScript being single-threaded."
    },
    {
      id: "webdev_q12",
      topic: "038",
      question: "What does JWT stand for, and what is it used for?",
      options: [
        "JavaScript Web Token — for storing user preferences",
        "JSON Web Token — for securely transmitting claims between parties",
        "Java Web Transfer — for server-to-server file transfers",
        "JSON Web Transfer — for database queries"
      ],
      answer: 1,
      explanation: "JWT (JSON Web Token) is a compact, self-contained token for securely transmitting information as a JSON object. It's commonly used for authentication: the server issues a JWT after login, and the client sends it with subsequent requests."
    },
    {
      id: "webdev_q13",
      topic: "045",
      question: "Which OWASP vulnerability involves injecting malicious scripts into web pages viewed by other users?",
      options: [
        "SQL Injection",
        "Cross-Site Scripting (XSS)",
        "Cross-Site Request Forgery (CSRF)",
        "Broken Authentication"
      ],
      answer: 1,
      explanation: "XSS (Cross-Site Scripting) allows attackers to inject client-side scripts into web pages. These scripts run in victims' browsers, potentially stealing cookies, session tokens, or performing actions on behalf of the user."
    },
    {
      id: "webdev_q14",
      topic: "049",
      question: "What is the purpose of a `.gitignore` file?",
      options: [
        "To list files that Git should delete automatically",
        "To specify files and directories that Git should not track",
        "To configure Git's merge strategy",
        "To define Git hooks that run before commits"
      ],
      answer: 1,
      explanation: ".gitignore tells Git which files/directories to intentionally ignore (not track). Common entries include node_modules/, .env files with secrets, build artifacts, and OS-specific files like .DS_Store."
    },
    {
      id: "webdev_q15",
      topic: "050",
      question: "Which Docker command builds an image from a Dockerfile?",
      options: ["docker run", "docker build", "docker push", "docker compose"],
      answer: 1,
      explanation: "`docker build -t my-image .` builds a Docker image from the Dockerfile in the current directory. `docker run` starts a container from an image, `docker push` uploads an image to a registry."
    },
    {
      id: "webdev_q16",
      topic: "054",
      question: "Which Core Web Vital measures how long it takes for the largest visible content element to render?",
      options: [
        "FID (First Input Delay)",
        "CLS (Cumulative Layout Shift)",
        "LCP (Largest Contentful Paint)",
        "TTFB (Time To First Byte)"
      ],
      answer: 2,
      explanation: "LCP (Largest Contentful Paint) measures when the largest content element (image, video, text block) becomes visible. A good LCP score is under 2.5 seconds. It's a key Google ranking signal."
    },
    {
      id: "webdev_q17",
      topic: "040",
      question: "What is the primary advantage of GraphQL over traditional REST APIs?",
      options: [
        "GraphQL is always faster than REST due to binary protocol",
        "Clients can request exactly the data they need, avoiding over/under-fetching",
        "GraphQL does not require any backend server",
        "GraphQL only works with React frontend"
      ],
      answer: 1,
      explanation: "GraphQL allows clients to specify exactly which fields they need in a single query, solving over-fetching (getting too much data) and under-fetching (requiring multiple round trips). REST returns fixed response shapes."
    },
    {
      id: "webdev_q18",
      topic: "021",
      question: "In JavaScript, what is a 'closure'?",
      options: [
        "A way to close/destroy a function after execution",
        "A function that remembers the variables from its outer scope even after the outer function returns",
        "A built-in method for closing browser windows",
        "A pattern for handling async operations"
      ],
      answer: 1,
      explanation: "A closure is formed when a function retains access to its outer lexical scope even after the outer function has returned. This is fundamental to patterns like data privacy, factory functions, and callbacks."
    },
    {
      id: "webdev_q19",
      topic: "058",
      question: "What is horizontal scaling in the context of web servers?",
      options: [
        "Adding more CPU and RAM to an existing server",
        "Adding more server instances and distributing load across them",
        "Increasing database storage capacity",
        "Optimizing CSS for faster rendering"
      ],
      answer: 1,
      explanation: "Horizontal scaling (scaling out) adds more instances of a service behind a load balancer. It's preferred for web apps because it provides better fault tolerance and near-unlimited scale. Vertical scaling (adding hardware) has practical limits."
    },
    {
      id: "webdev_q20",
      topic: "046",
      question: "What is CSRF (Cross-Site Request Forgery)?",
      options: [
        "Injecting SQL into database queries through form inputs",
        "Tricking a logged-in user's browser into sending unintended requests to a trusted site",
        "Intercepting HTTPS traffic between client and server",
        "Brute-forcing login credentials"
      ],
      answer: 1,
      explanation: "CSRF tricks an authenticated user's browser into making unauthorized requests to a site where they're logged in. Defenses include CSRF tokens, SameSite cookies, and checking the Origin/Referer header."
    }
  ],

  aptitude: [
    {
      id: "aptitude_q1",
      topic: "001",
      question: "What is the unit digit of 7^95 - 3^58?",
      options: ["0", "4", "6", "7"],
      answer: 1,
      explanation: "The cyclicity of 7 is 4. Divide 95 by 4, remainder is 3. Unit digit of 7^95 is unit digit of 7^3 = 3. The cyclicity of 3 is 4. Divide 58 by 4, remainder is 2. Unit digit of 3^58 is unit digit of 3^2 = 9. So 7^95 - 3^58 has unit digit of 3 - 9 = -6. Adding 10 (carry), we get 10 - 6 = 4."
    },
    {
      id: "aptitude_q2",
      topic: "002",
      question: "If the price of petrol increases by 25%, by what percentage must a consumer reduce consumption to keep the expenditure constant?",
      options: ["20%", "25%", "16.67%", "33.33%"],
      answer: 0,
      explanation: "Using the AB product constancy rule: if price increases by 25% (1/4), the consumption must decrease by 1/(4+1) = 1/5 = 20% to keep expenditure constant."
    },
    {
      id: "aptitude_q3",
      topic: "003",
      question: "A dealer marks his goods 20% above the cost price and allows a discount of 10% on the marked price. What is his net profit percentage?",
      options: ["5%", "8%", "10%", "12%"],
      answer: 1,
      explanation: "Using successive change formula: a = +20% (markup), b = -10% (discount). Net change = a + b + (ab/100) = 20 - 10 - (200/100) = 10 - 2 = 8% profit."
    },
    {
      id: "aptitude_q4",
      topic: "004",
      question: "What is the difference between Compound Interest and Simple Interest on a principal of $10,000 for 2 years at an annual interest rate of 8%?",
      options: ["$64", "$80", "$160", "$640"],
      answer: 0,
      explanation: "The difference between CI and SI for 2 years is given by D = P × (R/100)². Here, D = 10,000 × (8/100)² = 10,000 × 64/10,000 = $64."
    },
    {
      id: "aptitude_q5",
      topic: "005",
      question: "If A : B = 3 : 4 and B : C = 8 : 9, what is the ratio A : B : C?",
      options: ["3 : 8 : 9", "6 : 8 : 9", "3 : 4 : 9", "6 : 8 : 12"],
      answer: 1,
      explanation: "To merge ratios, make B's term equal. Multiply A : B = 3 : 4 by 2 to get 6 : 8. Since B : C = 8 : 9, the combined ratio is A : B : C = 6 : 8 : 9."
    },
    {
      id: "aptitude_q6",
      topic: "007",
      question: "In what ratio must water be mixed with milk costing $12 per litre to obtain a mixture worth $10 per litre?",
      options: ["1 : 5", "5 : 1", "1 : 6", "6 : 1"],
      answer: 0,
      explanation: "Using alligation rule: Cost of water is $0, Cost of milk is $12, Mean price is $10. Ratio of Water : Milk = (12 - 10) : (10 - 0) = 2 : 10 = 1 : 5."
    },
    {
      id: "aptitude_q7",
      topic: "010",
      question: "A train 150 meters long crosses a bridge 250 meters long in 20 seconds. What is the speed of the train in km/hr?",
      options: ["20 km/hr", "36 km/hr", "72 km/hr", "90 km/hr"],
      answer: 2,
      explanation: "Total distance to cover = Train length + Bridge length = 150 + 250 = 400 meters. Speed = Distance / Time = 400 / 20 = 20 m/s. Convert m/s to km/hr by multiplying by 18/5: 20 × 18/5 = 72 km/hr."
    },
    {
      id: "aptitude_q8",
      topic: "011",
      question: "A can complete a piece of work in 12 days and B can do it in 15 days. If they work together, how many days will they take to finish the work?",
      options: ["6 days", "6.67 days", "7.5 days", "10 days"],
      answer: 1,
      explanation: "Using LCM method: Let total work be LCM(12, 15) = 60 units. A's efficiency = 60/12 = 5 units/day. B's efficiency = 60/15 = 4 units/day. Combined efficiency = 9 units/day. Time taken = 60 / 9 = 20/3 = 6.67 days."
    },
    {
      id: "aptitude_q9",
      topic: "012",
      question: "What is the angle between the minute hand and the hour hand of a clock at 8:20?",
      options: ["130°", "120°", "110°", "100°"],
      answer: 0,
      explanation: "Using formula θ = |30H - 5.5M|: θ = |30(8) - 5.5(20)| = |240 - 110| = 130°."
    },
    {
      id: "aptitude_q10",
      topic: "013",
      question: "How many diagonals are there in a regular hexagon (6-sided polygon)?",
      options: ["6", "9", "12", "15"],
      answer: 1,
      explanation: "Number of diagonals in an n-sided polygon = n(n-3)/2. For a hexagon, n = 6: 6(6-3)/2 = 6 × 3 / 2 = 9 diagonals."
    },
    {
      id: "aptitude_q11",
      topic: "014",
      question: "Two fair dice are rolled. What is the probability that the sum of the numbers on the two dice is a prime number?",
      options: ["5/12", "7/18", "15/36", "11/36"],
      answer: 2,
      explanation: "Total outcomes = 36. Sums can be prime: 2, 3, 5, 7, 11. Sum 2: (1,1). Sum 3: (1,2),(2,1). Sum 5: (1,4),(4,1),(2,3),(3,2). Sum 7: (1,6),(6,1),(2,5),(5,2),(3,4),(4,3). Sum 11: (5,6),(6,5). Total favorable outcomes = 15. Probability = 15/36."
    },
    {
      id: "aptitude_q12",
      topic: "016",
      question: "If in a certain code language, 'MONKEY' is written as 'XDJMNL', how is 'TIGER' written in that code?",
      options: ["SDFHS", "QDFHS", "SHFDQ", "UJHFS"],
      answer: 1,
      explanation: "Pattern: The letters are written in reverse order, and each letter is decremented by 1 (minus 1). TIGER reversed is REGIT. Decrementing by 1 gives QDFHS."
    },
    {
      id: "aptitude_q13",
      topic: "017",
      question: "Pointing to a photograph of a boy, Suresh said, 'He is the son of the only son of my mother.' How is Suresh related to that boy?",
      options: ["Brother", "Uncle", "Cousin", "Father"],
      answer: 3,
      explanation: "'Only son of my mother' is Suresh himself (since Suresh is speaking). Therefore, the boy is the son of Suresh. Suresh is the father of the boy."
    },
    {
      id: "aptitude_q14",
      topic: "018",
      question: "A person walks 10m North, turns right and walks 10m, then turns right again and walks 5m. Finally, he turns right and walks 10m. How far is he from his starting point?",
      options: ["5m", "10m", "15m", "20m"],
      answer: 0,
      explanation: "Final position is 5m North of starting point. Shortest distance is 5m."
    },
    {
      id: "aptitude_q15",
      topic: "019",
      question: "Statements: I. All pens are pencils. II. Some pencils are rulers. Conclusions: 1. Some pens are rulers. 2. Some rulers are pens. What is true?",
      options: ["Only 1 follows", "Only 2 follows", "Both 1 and 2 follow", "Neither 1 nor 2 follows"],
      answer: 3,
      explanation: "Since the rulers circle might not intersect the pens circle, neither conclusion follows logically under all possible Venn diagrams."
    }
  ]
};

window.QUIZ_QUESTIONS = QUIZ_QUESTIONS;
