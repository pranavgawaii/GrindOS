import base64
import os

# Load logo
with open("../logo.png", "rb") as img_file:
    LOGO_BASE64 = base64.b64encode(img_file.read()).decode('utf-8')

# ─────────────────────────────────────────
# 25 OPERATING SYSTEMS INTERVIEW TOPICS
# ─────────────────────────────────────────
topics = [
    {
        "id": "os-proc-thread",
        "num": "01",
        "chapter": "Process Management",
        "title": "Process vs Thread",
        "subtitle": "Understanding active execution units and memory allocation contexts.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Core Differences</div>
  <p><strong>Process:</strong> An executing program instance. Has its own private address space (code, data, heap, file descriptors). Heavyweight, slow creation.</p>
  <p><strong>Thread:</strong> A subset of a process (lightweight process). Shares code, data, and OS resources with sibling threads, but has its own Stack and Registers.</p>
</div>
<div class="concept-visual">
  <div style="border: 1px solid #CBD5E0; border-radius:6px; padding:10px; background:white; font-size:7.5pt; width:100%;">
    <strong style="color:#2B6CB0; display:block; text-align:center; margin-bottom:4px;">Process Memory Boundary</strong>
    <div style="background:#FFF5F0; padding:6px; border:1px solid #EA763F; border-radius:4px; font-weight:bold; margin-bottom:4px; text-align:center;">
      Shared: Code | Data | Heap | Files
    </div>
    <div style="display:flex; gap:6px;">
      <div style="flex:1; background:#EBF8FF; border:1px solid #3182CE; padding:4px; text-align:center; border-radius:4px;">
        Thread 1<br><span style="font-size:6.5pt; color:#4A5568;">Stack & Regs</span>
      </div>
      <div style="flex:1; background:#EBF8FF; border:1px solid #3182CE; padding:4px; text-align:center; border-radius:4px;">
        Thread 2<br><span style="font-size:6.5pt; color:#4A5568;">Stack & Regs</span>
      </div>
    </div>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why is context switching between threads faster than between processes?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Virtual Memory Space</span>
    <span class="buzz-tag">TLB Cache Flush</span>
    <span class="buzz-tag">Shared Address Space</span>
    <span class="buzz-tag">Cache Hotness</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Process context switching requires flushing the CPU TLB cache and loading a completely new page table directory. Thread switching preserves the virtual memory layout, meaning the TLB cache does not need to be flushed and cache lines stay warm, reducing overhead."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a zombie process?"</p>
  <p class="followup-a">A process that has finished execution but still has an entry in the process table so its parent can read its exit status code.</p>
</div>
""",
        "trap": "Don't say threads share stack space! Threads share heap and code, but each thread MUST have its own independent stack to track function call execution.",
        "trick": "Process = Independent houses (isolated yard). Thread = Rooms inside the same house (sharing kitchen, private bedrooms)."
    },
    {
        "id": "os-cpu-sched",
        "num": "02",
        "chapter": "Process Management",
        "title": "CPU Scheduling Algorithms",
        "subtitle": "Comparing FCFS, SJF, SRTF, and Round Robin scheduling paradigms.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Algorithm Metrics</div>
  <p>Used to decide which ready process gets CPU time next. Crucial metrics are <strong>Turnaround Time</strong> (completion - arrival) and <strong>Waiting Time</strong> (turnaround - burst).</p>
</div>
<div class="concept-visual">
  <table class="visual-table contrast-table" style="font-size:7pt;">
    <thead>
      <tr>
        <th>Algo</th>
        <th>Type</th>
        <th>Metric</th>
        <th>Downside</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>FCFS</td><td>Non-Prem</td><td>Arrival</td><td>Convoy Effect</td></tr>
      <tr><td>SJF</td><td>Non-Prem</td><td>Burst Time</td><td>Starvation of Long</td></tr>
      <tr><td>SRTF</td><td>Preemptive</td><td>Rem Time</td><td>High Overhead</td></tr>
      <tr><td>RR</td><td>Preemptive</td><td>Time Quantum</td><td>Quantum Sensitive</td></tr>
    </tbody>
  </table>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is the 'Convoy Effect' in FCFS scheduling, and how can it be resolved?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">FCFS Non-Preemptive</span>
    <span class="buzz-tag">Short vs Long Job</span>
    <span class="buzz-tag">Average Waiting Time</span>
    <span class="buzz-tag">Preemptive SRTF</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"The Convoy Effect occurs in FCFS when one CPU-bound process with a huge burst time blocks many short I/O-bound processes, increasing the average waiting time. It is resolved by using preemptive algorithms like Round Robin or Shortest Remaining Time First (SRTF)."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What determines the optimal time quantum in Round Robin?"</p>
  <p class="followup-a">If too large, RR degrades to FCFS. If too small, context switching overhead dominates CPU cycles. The sweet spot is context switch overhead < 10% of quantum.</p>
</div>
""",
        "trap": "Don't confuse Turnaround Time (TAT) with Waiting Time (WT). TAT is total lifecycle length; WT is the time process spent waiting in ready queue.",
        "trick": "FCFS = Traditional bank teller queue. Round Robin = Bouncing a mic between karaoke singers for 10 seconds each."
    },
    {
        "id": "os-pcb-ctx",
        "num": "03",
        "chapter": "Process Management",
        "title": "PCB & Context Switching",
        "subtitle": "Storing state metadata and transitioning execution across processes.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">PCB Data Structure</div>
  <p>The Process Control Block (PCB) is an OS kernel data structure containing all metadata about a process: PID, state, Program Counter (PC), CPU registers, memory limits, open file descriptors.</p>
</div>
<div class="concept-visual" style="font-family:monospace; font-size:7.5pt; line-height:1.3; background:#FAFAFA; border:1px solid #CBD5E0; padding:8px; border-radius:6px;">
  <strong>PCB Structure Block:</strong><br>
  - Process ID (PID)<br>
  - Process State (New, Ready, Running...)<br>
  - PC Pointer &amp; Registers<br>
  - CPU Scheduling Info<br>
  - Memory Management Map
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Explain the exact lifecycle steps of a CPU during a context switch from Process A to Process B."</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Save Register State</span>
    <span class="buzz-tag">Program Counter Ptr</span>
    <span class="buzz-tag">PCB Load / Store</span>
    <span class="buzz-tag">Interrupt Handler</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"During a context switch: 1. CPU triggers an interrupt (timer or system call). 2. OS saves the current registers, stack pointer, and Program Counter (PC) into Process A's PCB. 3. OS updates Process A's state. 4. OS schedules Process B, loads its saved registers and PC from Process B's PCB, and updates execution."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"Is context switching a pure overhead?"</p>
  <p class="followup-a">Yes. During context switching, the CPU performs no productive user-space computation; it is purely executing kernel setup code.</p>
</div>
""",
        "trap": "Don't state that context switching occurs inside user space. It is strictly a privileged Kernel-mode execution.",
        "trick": "PCB is the save state slot of a video game emulator. Context switch is saving Game A and loading Game B."
    },
    {
        "id": "os-mlq",
        "num": "04",
        "chapter": "Process Management",
        "title": "Multi-Level Queue & Feedback Queue",
        "subtitle": "Managing complex workloads by separating processes by characteristics.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Queue Partitioning</div>
  <p><strong>Multi-Level Queue (MLQ):</strong> Partition ready queue into separate queues (interactive vs batch). Processes belong permanently to a queue.</p>
  <p><strong>Feedback Queue (MLFQ):</strong> Allows processes to move between queues based on execution history (prevents starvation, optimizes interactive response).</p>
</div>
<div class="concept-visual">
  <div style="font-family:monospace; font-size:7.5pt; text-align:center;">
    [High Priority (Interactive)] Quantum=4ms<br>
    ↓ processes exceeding quantum demoted<br>
    [Medium Priority (Interactive)] Quantum=8ms<br>
    ↓ demoted<br>
    [Low Priority (Batch)] FCFS
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How does a Multi-Level Feedback Queue (MLFQ) dynamically prioritize interactive tasks over CPU-bound tasks?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Queue Demotion</span>
    <span class="buzz-tag">I/O Burst Priority</span>
    <span class="buzz-tag">Aging Mechanism</span>
    <span class="buzz-tag">CPU Hog Throttling</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"MLFQ starts all new processes at the highest priority queue with a short time quantum. If a process yields before its quantum (interactive I/O), it stays high. If it hogs the CPU for the entire quantum, it gets demoted to a lower priority queue with a longer quantum, keeping interactive response times low."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is 'Aging' in scheduling?"</p>
  <p class="followup-a">A safety valve mechanism where processes sitting in low-priority queues for a long time are promoted to higher queues to prevent CPU starvation.</p>
</div>
""",
        "trap": "Don't confuse MLQ with MLFQ. In MLQ, a process is locked to a single queue (e.g. system tasks queue). Only MLFQ supports queue migrations.",
        "trick": "MLFQ is like a corporate trial period: start at top; do good work, stay; take too long, demoted."
    },
    {
        "id": "os-mem-manage",
        "num": "05",
        "chapter": "Memory Management",
        "title": "Paging & Segmentation",
        "subtitle": "Analyzing non-contiguous virtual memory mapping paradigms.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Logical Space Layouts</div>
  <p><strong>Paging:</strong> Divides physical memory into fixed-sized blocks (frames) and virtual memory into pages. Eliminates external fragmentation. Causes internal fragmentation.</p>
  <p><strong>Segmentation:</strong> Divides memory into logical blocks of variable size (main program, stack, library functions). Causes external fragmentation.</p>
</div>
<div class="concept-visual">
  <table class="visual-table contrast-table" style="font-size:7.5pt;">
    <thead>
      <tr>
        <th>Metric</th>
        <th>Paging</th>
        <th>Segmentation</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Block Size</td><td>Fixed Size</td><td>Variable Size</td></tr>
      <tr><td>Mapping</td><td>Page Table</td><td>Segment Table</td></tr>
      <tr><td>Fragmentation</td><td>Internal</td><td>External</td></tr>
      <tr><td>User Visibility</td><td>Transparent</td><td>Visible (logical blocks)</td></tr>
    </tbody>
  </table>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why does Paging completely eliminate External Fragmentation but introduce Internal Fragmentation?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Fixed Page Size</span>
    <span class="buzz-tag">Last Page Remainder</span>
    <span class="buzz-tag">Non-contiguous Frames</span>
    <span class="buzz-tag">Internal Slack Space</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Paging splits memory into fixed frames. Any page can map to any frame, so no small unallocated holes (external fragmentation) are created. However, if a process requests 5KB and page size is 4KB, it gets 2 pages (8KB). The remaining 3KB of the second page is wasted, creating internal fragmentation."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a page table, and where does it live?"</p>
  <p class="followup-a">A table mapping page numbers to frame numbers. It lives in main memory (RAM) and its physical address is pointed to by a register (PTBR).</p>
</div>
""",
        "trap": "Don't say paging is user-visible. Paging is entirely managed by the operating system kernel and Memory Management Unit (MMU) hardware.",
        "trick": "Paging = Slicing a bread loaf into identical slices. Segmentation = Separating a meal into main, salad, dessert."
    },
    {
        "id": "os-virt-mem",
        "num": "06",
        "chapter": "Memory Management",
        "title": "Virtual Memory & Demand Paging",
        "subtitle": "Running processes larger than physical RAM via swap mapping.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Address Abstraction</div>
  <p>Virtual memory maps a process's virtual addresses to physical RAM, abstracting disk storage as a virtual expansion of physical RAM.</p>
  <p><strong>Demand Paging:</strong> Lazy swapper paradigm. A page is loaded into main memory only when a process references it.</p>
</div>
<div class="concept-visual" style="font-size:7.5pt; font-family:monospace; border:1px solid #CBD5E0; padding:10px; background:white; text-align:center;">
  [Virtual Address Space]<br>
  ↓ Page Table Lookup (Valid Bit = 0)<br>
  <strong>[PAGE FAULT INTERRUPT]</strong><br>
  ↓ OS retrieves page from Swap Space on Disk<br>
  [Frame Loaded into RAM] (Valid Bit → 1)
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Step-by-step, describe what happens inside the OS and CPU when a Page Fault occurs."</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Valid/Invalid Bit</span>
    <span class="buzz-tag">Page Fault Exception</span>
    <span class="buzz-tag">Swap Space Lookup</span>
    <span class="buzz-tag">I/O Disk Block</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"When a process requests an address, the MMU checks the page table. If the valid bit is 0, the MMU traps to the OS (Page Fault). The OS: 1. Pauses the process. 2. Locates the missing page on the swap disk. 3. Finds a free physical frame. 4. Reads the disk block into the frame. 5. Updates the Page Table bit to 1. 6. Restarts the instruction."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a dirty bit?"</p>
  <p class="followup-a">A bit in the page table indicating if the page was modified. If not modified (dirty bit = 0), the OS can discard it during swap out without writing back to disk.</p>
</div>
""",
        "trap": "Don't think virtual memory makes processes run faster. It increases overhead. It simply allows running larger processes than physical memory size allows.",
        "trick": "Virtual memory is like display books in a bookstore window: you can view the cover, but the salesman brings the book from the back only when asked."
    },
    {
        "id": "os-page-replace",
        "num": "07",
        "chapter": "Memory Management",
        "title": "Page Replacement Algorithms",
        "subtitle": "Deciding which frames to evict from physical memory.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Ejection Paradigms</div>
  <p><strong>FIFO:</strong> First In First Out. Simplest, suffers from Belady's Anomaly.</p>
  <p><strong>LRU (Least Recently Used):</strong> Replaces the page unused for the longest period. High tracking overhead.</p>
  <p><strong>Optimal (MIN):</strong> Replaces page that won't be used for the longest future duration. Impossible to implement (requires future knowledge).</p>
</div>
<div class="concept-visual">
  <div style="border: 1px solid #CBD5E0; border-radius:6px; padding:8px; background:white; font-size:7.5pt; width:100%;">
    <strong style="color:#B7791F; display:block; text-align:center; margin-bottom:4px;">Belady's Anomaly (FIFO)</strong>
    <p style="font-size:7pt; color:#4A5568;">Increasing physical frames actually causes MORE page faults for specific reference strings (e.g. 1,2,3,4,1,2,5,1,2,3,4,5).</p>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is Belady's Anomaly? Name the page replacement algorithms that never suffer from it."</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">FIFO Queue</span>
    <span class="buzz-tag">Frame Increase Faults</span>
    <span class="buzz-tag">Stack Algorithms</span>
    <span class="buzz-tag">LRU Reference Map</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Belady's Anomaly is a counter-intuitive phenomenon where increasing the number of physical memory frames causes an increase in page faults under FIFO. 'Stack' algorithms, such as LRU and Optimal, can never suffer from Belady's anomaly, as their frame allocation subset holds inclusion properties."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"How is LRU implemented in real systems?"</p>
  <p class="followup-a">Due to the high overhead of tracking memory accesses, OS kernels use approximations like the <strong>Second Chance (Clock) algorithm</strong> using reference bits.</p>
</div>
""",
        "trap": "Don't state that the Optimal algorithm is used in production. It is strictly a theoretical benchmark for comparing other algorithms, as the OS cannot predict future page accesses.",
        "trick": "FIFO = Queue at a bakery. LRU = Checking what tools at the bottom of your drawer haven't been touched recently."
    },
    {
        "id": "os-fault-thrashing",
        "num": "08",
        "chapter": "Memory Management",
        "title": "Page Fault & Thrashing",
        "subtitle": "Preventing system degradation caused by continuous paging.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Thrashing Definition</div>
  <p>Thrashing occurs when a process spends more time swapping pages in and out of disk than executing instructions. CPU utilization drops to near zero.</p>
</div>
<div class="concept-visual">
  <div style="border:1px solid #CBD5E0; border-radius:6px; padding:10px; background:white;">
    <div style="font-size:8pt; font-weight:800; color:#E53E3E; margin-bottom:6px; text-align:center;">CPU Utilization vs Degree of Multiprogramming</div>
    <div style="position:relative; height:60px; border-left:1.5px solid #A0AEC0; border-bottom:1.5px solid #A0AEC0; margin:0 20px;">
      <!-- Bell curve style path -->
      <svg width="100%" height="100%" viewBox="0 0 100 50">
        <path d="M 5 45 Q 40 5 60 45" fill="none" stroke="#EA763F" stroke-width="2" />
        <text x="65" y="25" font-size="6" fill="#C53030" font-weight="bold">Thrashing Zone</text>
      </svg>
    </div>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why does the OS scheduler increase multiprogramming when thrashing begins, and how does this make things worse?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">CPU Utilization Drop</span>
    <span class="buzz-tag">Page Fault Storm</span>
    <span class="buzz-tag">Working Set Model</span>
    <span class="buzz-tag">Locality Model</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"When thrashing starts, processes wait on disk I/O, causing CPU utilization to drop. The OS scheduler mistakes this for low load and launches new processes. These new processes steal pages from existing ones, causing more page faults and worsening thrashing."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"How can the OS mitigate thrashing?"</p>
  <p class="followup-a">By implementing the <strong>Working Set Model</strong>: estimating how many pages a process needs in its active locality, and suspending processes if total demand exceeds available frames.</p>
</div>
""",
        "trap": "Don't confuse context-switch delays with thrashing. Context switching is CPU bound; thrashing is disk I/O bound.",
        "trick": "Thrashing is trying to study 10 books at once when your desk only fits 2, spending all your time opening and closing books."
    },
    {
        "id": "os-crit-sec",
        "num": "09",
        "chapter": "Process Synchronization",
        "title": "Critical Section Problem",
        "subtitle": "Regulating access to shared resources to prevent data corruption.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition & Requirements</div>
  <p>A Critical Section is a code segment accessing shared variables or resources that must not be accessed concurrently by multiple threads.</p>
  <p style="margin-top:6px; font-weight:800; color:#EA763F;">3 Strict Requirements for any Solution:</p>
  <p>1. <strong>Mutual Exclusion:</strong> Only one thread inside critical section at a time.<br>
  2. <strong>Progress:</strong> Only threads wanting to enter determine who enters next.<br>
  3. <strong>Bounded Waiting:</strong> A thread cannot wait indefinitely to enter.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is a Race Condition, and how does a Critical Section solution prevent it?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Race Condition</span>
    <span class="buzz-tag">Atomic Execution</span>
    <span class="buzz-tag">Mutual Exclusion</span>
    <span class="buzz-tag">Interrupt Enable/Disable</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A Race Condition is a flaw where the system's output depends on the execution sequence of threads (e.g. concurrent balance increments). A Critical Section solution uses synchronization primitives (mutexes, locks) to serialize execution, guaranteeing database operations run atomically."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is Peterson's Solution?"</p>
  <p class="followup-a">A classic software-based solution for two processes. It uses a <code>turn</code> variable and an <code>interested</code> array to guarantee mutual exclusion, progress, and bounded waiting.</p>
</div>
""",
        "trap": "Don't say disabling interrupts is a good modern critical section solution. It crashes multi-core CPUs and blocks system clocks.",
        "trick": "Critical Section is a single-occupancy airplane restroom. The lock on the door is the synchronization primitive."
    },
    {
        "id": "os-sync-prims",
        "num": "10",
        "chapter": "Process Synchronization",
        "title": "Mutex vs Semaphore vs Monitor",
        "subtitle": "Contrasting locks, atomic counters, and high-level language constructs.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Primitive Architecture</div>
  <p><strong>Mutex:</strong> A locking mechanism. Ownership-based; only the thread that locks it can unlock it. Binary state.</p>
  <p><strong>Semaphore:</strong> An integer variable accessed via atomic functions: <code>wait()</code> (P) and <code>signal()</code> (V). No ownership. Can be binary or counting.</p>
  <p><strong>Monitor:</strong> High-level language encapsulation package (like Java synchronized blocks) handling locking implicitly.</p>
</div>
<div class="concept-visual">
  <table class="visual-table contrast-table" style="font-size:7pt;">
    <thead>
      <tr>
        <th>Primitive</th>
        <th>Concept</th>
        <th>Ownership</th>
        <th>Signal Safety</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Mutex</td><td>Key Lock</td><td>Yes</td><td>High</td></tr>
      <tr><td>Semaphore</td><td>Count Tokens</td><td>No</td><td>Medium</td></tr>
      <tr><td>Monitor</td><td>Object Package</td><td>Yes</td><td>Highest</td></tr>
    </tbody>
  </table>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Can a thread release a Mutex locked by another thread? How does a Semaphore differ?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Lock Ownership</span>
    <span class="buzz-tag">Counting Resource</span>
    <span class="buzz-tag">Wait / Signal (P/V)</span>
    <span class="buzz-tag">Priority Inversion</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"No, a Mutex enforces ownership; only the thread that acquired the lock can release it. A Semaphore has no ownership; any thread can trigger a <code>signal()</code> to increment its value, making it optimal for cross-thread scheduling signals."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a Binary Semaphore vs a Mutex?"</p>
  <p class="followup-a">A binary semaphore is a semaphore with a value of 0 or 1. Unlike a Mutex, it lacks ownership, has no priority inversion protection, and allows signal calls from any thread.</p>
</div>
""",
        "trap": "Don't confuse Semaphore wait/signal names. `wait()` (P) decrements. `signal()` (V) increments. Memory tip: V for 'Vroom Vroom' (increase/go).",
        "trick": "Mutex = One key to the restroom. Semaphore = A bowl containing 5 keycards for a parking garage."
    },
    {
        "id": "os-sync-problems",
        "num": "11",
        "chapter": "Process Synchronization",
        "title": "Classic Synchronization Problems",
        "subtitle": "Analyzing Producer-Consumer, Readers-Writers, and Dining Philosophers.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Problem Definitions</div>
  <p><strong>Producer-Consumer:</strong> Shared finite buffer. Producer shouldn't add if full; consumer shouldn't pull if empty.</p>
  <p><strong>Readers-Writers:</strong> Multiple readers allowed, but writers need exclusive access. Prevents data corruption.</p>
  <p><strong>Dining Philosophers:</strong> Resource allocation deadlock test. 5 thinkers sharing 5 chopsticks (needs 2 to eat).</p>
</div>
<div class="concept-visual" style="font-family:monospace; font-size:7.5pt; background:#FDF6E3; padding:8px; border:1px solid #F5E6B3; border-radius:6px;">
  <strong>Dining Philosophers Solution Rules:</strong><br>
  - Left chopstick: <code>i</code><br>
  - Right chopstick: <code>(i+1) % 5</code><br>
  - Break asymmetry: odd numbered pick left first, even pick right first (avoids deadlock).
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Explain the Dining Philosophers problem and how to prevent deadlock without using locks."</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Circular Wait</span>
    <span class="buzz-tag">Asymmetric Pickup</span>
    <span class="buzz-tag">Chopstick Semaphores</span>
    <span class="buzz-tag">Resource Hierarchy</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Deadlock occurs when all 5 philosophers pick up their left chopstick simultaneously, waiting forever for the right (Circular Wait). We resolve this by breaking the symmetry: odd philosophers pick up left first, even pick up right first. This breaks the cycle."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is the Readers-Writers priority problem?"</p>
  <p class="followup-a">If readers have priority, new readers block writers indefinitely (Starvation). If writers have priority, readers starve. Solved via fair queuing semaphores.</p>
</div>
""",
        "trap": "Don't suggest a solution that allows only one philosopher to eat at a time. It blocks progress and is highly inefficient.",
        "trick": "Dining Philosophers is a resource lock simulator. Chopsticks are sharing locks. Philosophers are threads."
    },
    {
        "id": "os-deadlock-conds",
        "num": "12",
        "chapter": "Deadlocks",
        "title": "Deadlock: Four Conditions",
        "subtitle": "Analyzing Coffman's four mandatory conditions for system deadlocks.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Coffman Conditions</div>
  <p>A deadlock is a state where a set of processes are blocked because each holds a resource and waits for another resource held by someone else.</p>
  <p style="margin-top:6px; font-weight:800; color:#E53E3E;">Four Conditions (Must occur simultaneously):</p>
  <p>1. <strong>Mutual Exclusion:</strong> Resources cannot be shared.<br>
  2. <strong>Hold and Wait:</strong> Process holds a resource while waiting for another.<br>
  3. <strong>No Preemption:</strong> Resources cannot be forcibly taken.<br>
  4. <strong>Circular Wait:</strong> P1 waits for P2... who waits for P1.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How can you eliminate 'Circular Wait' inside an application's database code?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Resource Ordering</span>
    <span class="buzz-tag">Acquisition Sequence</span>
    <span class="buzz-tag">Total Ordering</span>
    <span class="buzz-tag">Lock Hierarchy</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"We eliminate Circular Wait by establishing a global Lock Order. If Thread A and Thread B both need Lock 1 and Lock 2, they must acquire them in the same order (Lock 1 first, then Lock 2). This prevents a cycle where Thread A holds Lock 1 and Thread B holds Lock 2."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is the difference between Starvation and Deadlock?"</p>
  <p class="followup-a">Deadlock is a circular block of processes (none can progress). Starvation is a process waiting indefinitely for a resource while others bypass it.</p>
</div>
""",
        "trap": "Don't say you can resolve deadlocks by ignoring them. The 'Ostrich algorithm' is used in commodity OS designs, but it is not a technical solution.",
        "trick": "Remember the Coffman conditions: Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait (MHNC)."
    },
    {
        "id": "os-bankers",
        "num": "13",
        "chapter": "Deadlocks",
        "title": "Banker's Algorithm",
        "subtitle": "Deadlock avoidance using resource allocation state validation.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Safe vs Unsafe States</div>
  <p>Developed by Dijkstra. Used for deadlock avoidance in multi-resource systems. Evaluates if allocating a resource keeps the system in a **Safe State**.</p>
  <p style="margin-top:6px; font-weight:800; color:#EA763F;">Matrix Equations:</p>
  <p><code>Need[i][j] = Max[i][j] - Allocation[i][j]</code></p>
</div>
<div class="concept-visual">
  <div style="border:1px solid #CBD5E0; border-radius:6px; padding:10px; background:white; font-size:7.5pt; width:100%;">
    <strong style="color:#276749; display:block; text-align:center; margin-bottom:4px;">Allocation Check Sequence</strong>
    <p style="font-size:7pt; color:#4A5568; line-height:1.3;">If <code>Need <= Available</code>, the process runs to completion, releases resources, and updates: <code>Available = Available + Allocation</code>.</p>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Does an Unsafe State always lead to a Deadlock?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Safe Path</span>
    <span class="buzz-tag">Unsafe State</span>
    <span class="buzz-tag">Worst-Case Demand</span>
    <span class="buzz-tag">Resource Allocation</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"No, an Unsafe State does not guarantee a deadlock. It only indicates that the system cannot guarantee a safe execution path if all processes request their maximum declared resources simultaneously. If processes yield early, deadlock may not occur."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"Why is the Banker's algorithm not used in general-purpose OS designs?"</p>
  <p class="followup-a">It requires processes to declare their maximum resource needs in advance, which is impossible for dynamic, general-purpose workloads.</p>
</div>
""",
        "trap": "Don't confuse Deadlock Avoidance (Banker's) with Deadlock Prevention (breaking Coffman conditions). Prevention is static; avoidance is dynamic.",
        "trick": "Banker's is a loan officer checking if the bank has enough cash to cover worst-case credit lines before approving a loan."
    },
    {
        "id": "os-deadlock-det",
        "num": "14",
        "chapter": "Deadlocks",
        "title": "Deadlock Detection & Recovery",
        "subtitle": "Identifying active deadlock states and restoring system stability.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Detection Strategy</div>
  <p>If a system doesn't prevent or avoid deadlocks, it must periodically run a detection algorithm (Wait-For Graph search) to find cycles.</p>
  <p style="margin-top:6px; font-weight:800; color:#E53E3E;">Recovery Actions:</p>
  <p>1. <strong>Process Termination:</strong> Abort all deadlocked processes, or abort them one-by-one until the cycle is broken.<br>
  2. <strong>Resource Preemption:</strong> Reclaim resources from one process and assign to others (causes rollback issues).</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How does a Wait-For Graph (WFG) identify deadlocks, and how does it differ from a Resource Allocation Graph (RAG)?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Cycle Detection</span>
    <span class="buzz-tag">Directed Graph</span>
    <span class="buzz-tag">Node Simplification</span>
    <span class="buzz-tag">Cycle Search</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A Resource Allocation Graph (RAG) contains nodes for both processes and resource types. A Wait-For Graph is a simplified version containing only process nodes. If there is a cycle in a Wait-For Graph, a deadlock exists (for single-unit resource systems)."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is rollback in deadlock recovery?"</p>
  <p class="followup-a">Saving checkpoint states of processes. During recovery, the OS rolls a process back to a safe checkpoint state, relinquishing its locks.</p>
</div>
""",
        "trap": "Don't suggest rebooting the server as the primary deadlock recovery mechanism. It causes data loss; graceful process termination is preferred.",
        "trick": "RAG has shape nodes for resources. WFG simplifies them, leaving only arrows connecting blocked threads."
    },
    {
        "id": "os-file-systems",
        "num": "15",
        "chapter": "File Systems & Storage",
        "title": "File Systems & Inodes",
        "subtitle": "How UNIX-like operating systems structure files, directories, and metadata.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">The Index Node (Inode)</div>
  <p>An inode is a kernel structure containing metadata about a file. Crucially, **the inode does NOT store the file name** (names are stored in directory tables).</p>
</div>
<div class="concept-visual" style="font-size:7.5pt; font-family:monospace; border:1px solid #CBD5E0; padding:10px; background:white;">
  <strong>Inode Metadata Fields:</strong><br>
  - File Size (Bytes)<br>
  - Owner (UID/GID) &amp; Permissions<br>
  - Modification Timestamp<br>
  - 12 Direct Pointers to data blocks<br>
  - Indirect, Double Indirect, Triple Indirect Pointers
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Explain the difference between Hard Links and Soft Links (Symbolic Links) in UNIX."</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Inode Reference Count</span>
    <span class="buzz-tag">Path Pointer</span>
    <span class="buzz-tag">Directory Entry</span>
    <span class="buzz-tag">Link Invalidation</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A Hard Link creates a new directory entry pointing to the same underlying inode address; deleting the original file doesn't break the hard link. A Soft Link is a separate pointer file containing the file path string; if the original is deleted, the soft link becomes broken."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is the maximum file size limit of an inode?"</p>
  <p class="followup-a">Determined by block size and indexing depth. With a 4KB block size, 12 direct + single/double/triple indirect pointers support file sizes up to 4TB.</p>
</div>
""",
        "trap": "Don't confuse file content changes with link changes. Both hard and soft link changes modify the same underlying file content.",
        "trick": "Hard Link = A second name tag pointing to the same person. Soft Link = An address card with a map to their house."
    },
    {
        "id": "os-disk-sched",
        "num": "16",
        "chapter": "File Systems & Storage",
        "title": "Disk Scheduling Algorithms",
        "subtitle": "Minimizing head seek time in magnetic hard drives.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Algorithm Variations</div>
  <p><strong>FCFS:</strong> Fair but slow; causes random head jumps.</p>
  <p><strong>SSTF:</strong> Shortest Seek Time First. Starves distant requests.</p>
  <p><strong>SCAN:</strong> Elevator algorithm. Moves head end-to-end, serving requests along the way.</p>
  <p><strong>LOOK:</strong> Like SCAN, but turns around at the last request instead of going to the physical disk edge.</p>
</div>
<div class="concept-visual">
  <div style="border:1px solid #CBD5E0; border-radius:6px; padding:10px; background:white; text-align:center; font-size:7.5pt;">
    <strong>SCAN vs C-SCAN (Circular SCAN)</strong><br>
    <span style="color:#2B6CB0; font-weight:bold;">SCAN:</span> Serves incoming and outgoing sweeps.<br>
    <span style="color:#276749; font-weight:bold;">C-SCAN:</span> Serves only in one direction, returning instantly to the start for predictability.
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why does SSTF suffer from starvation, and how does SCAN solve it?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Shortest Seek Time</span>
    <span class="buzz-tag">Locality of Requests</span>
    <span class="buzz-tag">Elevator Sweep</span>
    <span class="buzz-tag">Fair Queueing</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"SSTF services the request closest to the current head position. If new requests keep arriving near the head, distant requests starve. SCAN sweeps end-to-end like an elevator, guaranteeing all queued sectors are serviced in a single pass."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"Do SSDs need disk scheduling?"</p>
  <p class="followup-a">No. SSDs have no moving physical parts (no seek time). SSD controllers use direct lookup tables, making disk scheduling obsolete for solid-state storage.</p>
</div>
""",
        "trap": "Don't confuse C-SCAN with C-LOOK. C-SCAN goes to the absolute physical edge of the disk. C-LOOK turns around at the last queued request in that direction.",
        "trick": "SCAN is a city bus completing its route. SSTF is a taxi choosing the closest fare next."
    },
    {
        "id": "os-kernel",
        "num": "17",
        "chapter": "Operating System Architecture",
        "title": "Monolithic vs Microkernel",
        "subtitle": "Analyzing kernel size and extension patterns.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Core Architectures</div>
  <p><strong>Monolithic Kernel:</strong> All OS services (scheduler, file system, drivers) run in kernel space. Fast execution, but a crash in a driver crashes the OS (e.g. Linux).</p>
  <p><strong>Microkernel:</strong> Only essential services (IPC, memory) run in kernel space; others run in user space. Stable, but slow due to IPC overhead (e.g. Mach).</p>
</div>
<div class="concept-visual">
  <div style="display:flex; justify-content:space-between; font-size:7.5pt; gap:10px; width:100%;">
    <div style="flex:1; border:1.5px solid #EA763F; background:#FFF5F0; padding:6px; border-radius:4px; text-align:center;">
      <strong>Monolithic</strong><br>
      Drivers in Kernel<br>
      Fast calls<br>
      High crash risk
    </div>
    <div style="flex:1; border:1.5px solid #3182CE; background:#EBF8FF; padding:6px; border-radius:4px; text-align:center;">
      <strong>Microkernel</strong><br>
      Drivers in User space<br>
      IPC overhead<br>
      High isolation
    </div>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why does a Microkernel suffer from performance overhead compared to a Monolithic kernel?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Message Passing (IPC)</span>
    <span class="buzz-tag">Context Switch Count</span>
    <span class="buzz-tag">User/Kernel Boundary</span>
    <span class="buzz-tag">Indirect Calls</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"In a Monolithic kernel, OS services communicate via direct function calls. In a Microkernel, services run in user space. Any request (e.g., writing a file) requires message passing (IPC), causing multiple context switches between user and kernel space, degrading performance."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a Hybrid Kernel?"</p>
  <p class="followup-a">A compromise (like Windows NT or macOS Darwin) that runs core services inside kernel space for speed, but adopts modular microkernel layouts.</p>
</div>
""",
        "trap": "Don't state that Linux is unstable. While monolithic, modular code architecture and testing make Linux robust in production systems.",
        "trick": "Monolithic is an open-plan office (fast sharing, one sick person infects all). Microkernel is individual cubicles."
    },
    {
        "id": "os-syscalls",
        "num": "18",
        "chapter": "Operating System Architecture",
        "title": "System Calls (fork, exec)",
        "subtitle": "Programmatic interface to kernel space and process spawning.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">System Call Interface</div>
  <p>A system call is the programmatic method by which a user-space program requests a service from the kernel. Uses software interrupts (traps).</p>
  <p style="margin-top:6px; font-weight:800; color:#EA763F;">Key Calls:</p>
  <p><strong>fork():</strong> Spawns a child process. Returns PID of child to parent, and 0 to the child.<br>
  <strong>exec():</strong> Replaces current process image with a new executable program.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Explain the difference in execution between fork() and exec(). How do they work together?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Duplicate Process</span>
    <span class="buzz-tag">Overwrite Address Space</span>
    <span class="buzz-tag">Return Value Check</span>
    <span class="buzz-tag">Copy-on-Write (COW)</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"<code>fork()</code> clones the calling process, creating a duplicate child with a matching memory layout. <code>exec()</code> replaces the current process's address space with a new program image. To run a new program, a process calls <code>fork()</code> first, then the child immediately calls <code>exec()</code>."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is Copy-on-Write (COW) in fork()?"</p>
  <p class="followup-a">A optimization where child and parent share the same physical memory frames initially. Physical frames are duplicated only when parent or child writes to them.</p>
</div>
""",
        "trap": "Remember that fork() duplicates the process at the exact line of execution. Any code below the fork() statement is executed by BOTH processes.",
        "trick": "fork() = Cloning yourself. exec() = Putting on a mask to become someone else."
    },
    {
        "id": "os-ipc",
        "num": "19",
        "chapter": "Operating System Architecture",
        "title": "Inter-Process Communication",
        "subtitle": "Mechanisms for processes to share data and coordinate activities.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">IPC Models</div>
  <p>Processes run in isolated address spaces. Sharing data requires explicit IPC channels managed by the operating system kernel.</p>
  <p><strong>Shared Memory:</strong> Processes share a physical memory segment. Fastest, but requires synchronization (mutexes) to prevent race conditions.</p>
  <p><strong>Message Passing:</strong> Processes send messages via kernel message queues. System-call bound, but safe across networks.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Compare Shared Memory and Message Passing in IPC. When is each preferred?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Address Space Sharing</span>
    <span class="buzz-tag">Kernel Overhead</span>
    <span class="buzz-tag">Socket Communication</span>
    <span class="buzz-tag">Race Condition Risk</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Shared Memory is preferred for high-speed, local data sharing (no kernel intervention after setup). However, it requires software synchronization. Message Passing is preferred for smaller payloads or distributed systems, as the kernel handles message buffers safely."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a Named Pipe (FIFO) in UNIX?"</p>
  <p class="followup-a">An extension of standard anonymous pipes. Named pipes appear as special files on disk, allowing unrelated processes to communicate.</p>
</div>
""",
        "trap": "Don't say shared memory has no race conditions. It is vulnerable to race conditions if developers fail to implement locks.",
        "trick": "Shared Memory = Two programmers editing the same Google Doc. Message Passing = Sending emails back and forth."
    },
    {
        "id": "os-segmentation-frag",
        "num": "20",
        "chapter": "Memory Management",
        "title": "Fragmentation (Internal vs External)",
        "subtitle": "Wasted space within allocated blocks vs unallocated holes.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Wasted Space Taxonomy</div>
  <p><strong>Internal Fragmentation:</strong> Memory block allocated to a process is larger than requested. The unused space inside the block is wasted (occurs in fixed-partition paging).</p>
  <p><strong>External Fragmentation:</strong> Total free space exists to satisfy a request, but it is not contiguous (occurs in variable-partition segmentation).</p>
</div>
<div class="concept-visual">
  <div style="border:1px solid #CBD5E0; border-radius:6px; padding:10px; background:white; font-size:7.5pt; width:100%;">
    <strong style="color:#C53030; display:block; text-align:center; margin-bottom:4px;">External Fragmentation</strong>
    <div style="display:flex; justify-content:space-between; align-items:center; background:#EDF2F7; padding:4px;">
      <span>[Proc A: 4MB]</span>
      <span style="background:#FFF5F5; padding:2px; border:1px dashed #E53E3E;">Free: 2MB</span>
      <span>[Proc B: 4MB]</span>
      <span style="background:#FFF5F5; padding:2px; border:1px dashed #E53E3E;">Free: 2MB</span>
    </div>
    <p style="font-size:6.5pt; color:#4A5568; margin-top:4px; text-align:center;">Cannot satisfy a new request of 3MB contiguously!</p>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How does Memory Compaction resolve external fragmentation? What is its main limitation?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Memory Compaction</span>
    <span class="buzz-tag">Relocation Register</span>
    <span class="buzz-tag">Execution-Time Binding</span>
    <span class="buzz-tag">I/O Performance Drop</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Compaction sweeps memory to slide all allocated blocks to one end, leaving a single large free block. Its main limitation is computational overhead: moving megabytes of active process memory is slow, requiring suspension of running programs."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What allocation strategies choose free blocks?"</p>
  <p class="followup-a"><strong>First-Fit:</strong> Allocates the first hole that fits. <strong>Best-Fit:</strong> Allocates the smallest hole that fits (worsens external fragmentation). <strong>Worst-Fit:</strong> Allocates the largest hole.</p>
</div>
""",
        "trap": "Don't say best-fit is always optimal. Best-fit produces tiny, unusable leftover holes, worsening external fragmentation over time.",
        "trick": "Internal = Buying a size 10 shoe for a size 9 foot. External = Having 5 empty single seats scattered across a bus, but a group of 3 cannot sit together."
    },
    {
        "id": "os-tlb-cache",
        "num": "21",
        "chapter": "Memory Management",
        "title": "TLB (Translation Lookaside Buffer)",
        "subtitle": "Accelerating address translations using associative cache hardware.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Translation Acceleration</div>
  <p>Every memory access in paging requires two RAM lookups: one to read the page table, and one to read the actual data. This halves CPU performance.</p>
  <p><strong>TLB:</strong> A small, ultra-fast hardware cache built into the MMU containing recently resolved page-to-frame mappings.</p>
</div>
<div class="concept-visual">
  <div style="border: 1px solid #CBD5E0; border-radius:6px; padding:10px; background:white; font-size:7.5pt; width:100%; text-align:center;">
    Virtual Page Number<br>
    ↓ check TLB cache<br>
    <strong>TLB Hit:</strong> Returns Frame ID instantly (1 clock cycle)<br>
    <strong>TLB Miss:</strong> Resolves via Page Table in RAM (100 clock cycles)
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Explain the concept of a TLB Hit and a TLB Miss. How does it affect effective access time?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Effective Memory Access</span>
    <span class="buzz-tag">MMU Associative Cache</span>
    <span class="buzz-tag">Hardware Page Walk</span>
    <span class="buzz-tag">Context Switch Flush</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"On a TLB Hit, the physical address is resolved in 1 clock cycle. On a TLB Miss, the CPU must perform a 'page walk' in RAM to resolve the frame, taking 100+ clock cycles. High TLB hit rates (typically >99%) keep effective memory access times low."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a TLB flush?"</p>
  <p class="followup-a">During a context switch, the OS flushes the TLB cache because the new process has a completely different page-to-frame mapping layout.</p>
</div>
""",
        "trap": "Don't confuse TLB with CPU L1/L2 caches. TLB caches virtual address translations; L1/L2 caches actual memory data bytes.",
        "trick": "TLB is looking up a phone number in your contacts list instead of walking to the municipal library directory."
    },
    {
        "id": "os-user-kernel",
        "num": "22",
        "chapter": "Operating System Security",
        "title": "User Mode vs Kernel Mode",
        "subtitle": "Securing kernel space via dual-mode CPU privilege execution.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Privileged Rings</div>
  <p>Modern CPUs enforce privilege separation to prevent user applications from crashing the system. Controlled by a <strong>Mode Bit</strong> in the CPU status register.</p>
  <p><strong>User Mode (Mode Bit = 1):</strong> Restricted instructions. Direct hardware access blocked.</p>
  <p><strong>Kernel Mode (Mode Bit = 0):</strong> Full access to physical hardware and kernel memory spaces.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What triggers a transition from User Mode to Kernel Mode?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Privileged Instruction</span>
    <span class="buzz-tag">Software Interrupt (Trap)</span>
    <span class="buzz-tag">Hardware Exception</span>
    <span class="buzz-tag">System Call Trap</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Transition is triggered by three events: 1. System Calls (programs requesting file writes via software traps). 2. Hardware Interrupts (keyboard inputs or NIC signals). 3. Hardware Exceptions (Zero Division or Page Faults). The CPU sets the mode bit to 0 and jumps to the interrupt vector table."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a privileged instruction?"</p>
  <p class="followup-a">Instructions that can only be executed in kernel mode, such as clearing RAM, disabling hardware interrupts, or writing to status registers.</p>
</div>
""",
        "trap": "Don't assume running programs as 'root' or 'Administrator' elevates them to kernel mode. Root programs still run in User Mode, but have file permission privileges.",
        "trick": "User Mode is a hotel guest (allowed in room and lobby). Kernel Mode is hotel staff with master keycards."
    },
    {
        "id": "os-linking-loading",
        "num": "23",
        "chapter": "Operating System Execution",
        "title": "Dynamic vs Static Linking",
        "subtitle": "Combining code libraries at compile time vs load time.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Binary Compilation</div>
  <p>Linking resolves references to external libraries (such as `libc` or `stdio`).</p>
  <p><strong>Static Linking:</strong> Library code is copied directly into the final executable. Creates a large self-contained binary.</p>
  <p><strong>Dynamic Linking:</strong> Shared libraries (`.so` or `.dll` files) are loaded into RAM once, and referenced by multiple programs at runtime.</p>
</div>
<div class="concept-visual">
  <div style="display:flex; justify-content:space-between; font-size:7.5pt; gap:10px; width:100%;">
    <div style="flex:1; border:1px solid #CBD5E0; padding:6px; background:#F7FAFC; border-radius:4px; text-align:center;">
      <strong>Static (.a / .lib)</strong><br>
      Self-contained binary<br>
      Large file size<br>
      No runtime dependency
    </div>
    <div style="flex:1; border:1px solid #7c6fee; padding:6px; background:#F5EBFE; border-radius:4px; text-align:center;">
      <strong>Dynamic (.so / .dll)</strong><br>
      Shared in RAM<br>
      Tiny file size<br>
      Update lib without compile
    </div>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why is dynamic linking preferred in modern operating systems?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Shared Memory Segment</span>
    <span class="buzz-tag">Disk Space Economy</span>
    <span class="buzz-tag">Dynamic Linker (ld.so)</span>
    <span class="buzz-tag">DLL Hell Versioning</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Dynamic linking saves disk space and RAM by loading shared libraries once into memory. It also allows updating libraries (e.g. patching security bugs) without recompiling the applications that depend on them."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a DLL stub?"</p>
  <p class="followup-a">A small placeholder compiled into static code indicating how to locate and load the dynamic library at runtime.</p>
</div>
""",
        "trap": "Don't assume dynamic linking is always better. Static binaries are highly portable, making them ideal for containerized microservices (Docker).",
        "trick": "Static = Copying a recipe into your cookbook. Dynamic = Linking to a YouTube cooking tutorial."
    },
    {
        "id": "os-spooling",
        "num": "24",
        "chapter": "Operating System Operations",
        "title": "Spooling vs Buffering",
        "subtitle": "Managing speed disparities between CPU and I/O devices.",
        "yield_stars": "★★★☆☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">I/O Intermediaries</div>
  <p><strong>Spooling (Simultaneous Peripheral Operations On-Line):</strong> Buffers I/O operations on disk storage. Acts as a queue for slow, non-shareable devices (e.g. print queues).</p>
  <p><strong>Buffering:</strong> Stores data in RAM temporarily while being transferred between fast CPU registers and slow I/O blocks (e.g. video pre-loading).</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Contrast Spooling and Buffering. How do they differ in storage media and target devices?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Disk Queue Spool</span>
    <span class="buzz-tag">RAM Memory Buffer</span>
    <span class="buzz-tag">Printer Spooler</span>
    <span class="buzz-tag">Temporary Storage</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Spooling uses disk storage to queue operations for slow, non-shareable devices, allowing the CPU to hand off tasks and continue. Buffering uses RAM to smooth out speed mismatches between active channels during a transfer."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"Why do video players use buffering?"</p>
  <p class="followup-a">Network download speeds fluctuate. Buffering pre-downloads video frames into RAM to ensure smooth playback during network dips.</p>
</div>
""",
        "trap": "Don't say spooling and buffering are identical. Spooling is disk-based and handles queuing; buffering is RAM-based and handles temporary speed smoothing.",
        "trick": "Spooling = A mailbox holding packages until you collect them. Buffering = Holding a sip of hot coffee in your mouth before swallowing."
    },
    {
        "id": "os-rtos",
        "num": "25",
        "chapter": "Operating System Architectures",
        "title": "RTOS vs GPOS",
        "subtitle": "Deterministic timing constraints vs fair throughput balancing.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">System Priorities</div>
  <p><strong>RTOS (Real-Time OS):</strong> Designed for embedded systems requiring microsecond precision. Focuses on **determinism** (predictable deadlines).</p>
  <p><strong>GPOS (General Purpose OS):</strong> Designed for general desktops and servers. Focuses on **throughput** and fair scheduling (e.g. Windows, macOS).</p>
</div>
<div class="concept-visual">
  <table class="visual-table contrast-table" style="font-size:7.5pt;">
    <thead>
      <tr>
        <th>Metric</th>
        <th>RTOS</th>
        <th>GPOS</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Goal</td><td>Meet Deadlines</td><td>Fair Resource Sharing</td></tr>
      <tr><td>Latency</td><td>Low and Predictable</td><td>High and Variable</td></tr>
      <tr><td>Scheduling</td><td>Priority Preemptive</td><td>Fair Share / Time Sliced</td></tr>
      <tr><td>Examples</td><td>VxWorks, FreeRTOS</td><td>Linux, macOS, Windows</td></tr>
    </tbody>
  </table>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is the difference between a Hard RTOS and a Soft RTOS?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Deterministic Bounds</span>
    <span class="buzz-tag">Missed Deadline Crash</span>
    <span class="buzz-tag">Predictable Latency</span>
    <span class="buzz-tag">Embedded Control</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A Hard RTOS guarantees that critical tasks complete within strict deadlines; missing a deadline is treated as a total system failure (e.g., pacemaker or ABS brakes). A Soft RTOS treats deadlines as goals, accepting occasional delays (e.g., video player)."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is priority inversion in RTOS?"</p>
  <p class="followup-a">A bug where a low-priority task holds a resource needed by a high-priority task, while a medium-priority task preempts the low-priority one, delaying the high-priority task.</p>
</div>
""",
        "trap": "Don't assume RTOS is faster at math than GPOS. It is simply more predictable; it guarantees a response within a strict timeframe, even if slow.",
        "trick": "GPOS = A bus driver driving fast but stopping for passengers. RTOS = An ambulance driving on a planned route with priority."
    }
]

# ─────────────────────────────────────────
# PLACEMENT BOOSTERS DICTIONARY
# ─────────────────────────────────────────
OS_BOOSTERS = {
    "os-proc-thread": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Highlight that processes are independent resource units with separate memory space, whereas threads are lightweight execution paths sharing the parent process's memory heap."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Saying threads don't share memory. They share heap but have private stacks. <strong>Depth:</strong> Draw process vs thread memory space.</p>
</div>
""",
    "os-cpu-sched": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Scheduling optimizes CPU throughput and latency. Explain preemption as interrupting a process, whereas non-preemptive run to completion."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Confusing job scheduler with CPU scheduler. CPU scheduler picks from ready queue. <strong>Depth:</strong> List CPU metrics (throughput, turnaround, waiting time).</p>
</div>
""",
    "os-pcb-ctx": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"PCB stores process states (registers, counters, locks). Context switching saves this state to switch execution, adding kernel CPU overhead."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking context switching has zero cost. It consumes CPU cycles and flushes cache. <strong>Depth:</strong> State transition cycle.</p>
</div>
""",
    "os-mlq": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Explain MLQ as partitioning the ready queue into multiple separate queues based on process type (foreground vs background) with different algorithms."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Saying processes can move between MLQ queues. That requires Multilevel Feedback Queue (MLFQ). <strong>Depth:</strong> Explain aging in MLFQ.</p>
</div>
""",
    "os-mem-manage": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Memory management allocates RAM to processes. Contrast First Fit (fastest), Best Fit (conserve memory, causes small fragments), and Worst Fit (causes largest leftover)."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking Best Fit is always best. It leaves useless tiny fragments. <strong>Depth:</strong> Calculate allocations for a memory block sequence.</p>
</div>
""",
    "os-virt-mem": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Virtual Memory gives processes the illusion of contiguous, private memory. Paging maps virtual pages to physical frames, avoiding external fragmentation."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Confusing internal and external fragmentation. Paging causes tiny internal fragmentation; segmentation causes external. <strong>Depth:</strong> Page tables & TLB lookup.</p>
</div>
""",
    "os-page-replace": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Page replacement kicks out pages when frames are full. Contrast FIFO (simple, Belady's anomaly) and LRU (uses historical stack, no anomaly, optimal practical)."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Stating LRU is mathematically optimal. The absolute Optimal algorithm requires knowing future requests. <strong>Depth:</strong> Trace page hits/misses for an array.</p>
</div>
""",
    "os-fault-thrashing": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"A page fault occurs when a requested page is not in RAM, forcing disk swap. Thrashing is when the system spends more time swapping pages than executing code."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking adding more processes stops thrashing. It worsens it. <strong>Depth:</strong> Explain working set model and page fault frequency.</p>
</div>
""",
    "os-crit-sec": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Critical section is the code block modifying shared data. Any solution must meet 3 conditions: Mutual Exclusion, Progress, and Bounded Waiting."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking mutual exclusion alone is enough. Progress is essential. <strong>Depth:</strong> Detail Peterson's software solution and test-and-set hardware locks.</p>
</div>
""",
    "os-sync-prims": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"A Mutex is a locking mechanism (binary: lock/unlock) owned by the thread that locked it. A Semaphore is a signaling tool (counting) with wait/signal operations."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Saying Mutex is just a binary semaphore. Mutex has ownership, semaphore does not. <strong>Depth:</strong> Explain priority inversion and inheritance.</p>
</div>
""",
    "os-sync-problems": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Classic problems like Producer-Consumer (buffers) and Dining Philosophers (locks) illustrate race conditions and how semaphore signals coordinate threads."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Forgetting buffer checks in Producer-Consumer. <strong>Depth:</strong> Write pseudo-code using semaphores for dynamic buffer tracking.</p>
</div>
""",
    "os-deadlock-conds": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"A deadlock occurs when processes are blocked waiting for resources held by each other. Remember Coffman's 4 conditions: Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Not knowing circular wait is the essential trigger. <strong>Depth:</strong> Differentiate prevention, avoidance, and detection.</p>
</div>
""",
    "os-bankers": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Banker's Algorithm is a deadlock avoidance method. It calculates if allocating resources keeps the system in a safe state where all processes can finish."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking unsafe state means deadlock. Unsafe only means deadlock is possible. <strong>Depth:</strong> Trace Banker's matrices (Allocation, Max, Need, Available).</p>
</div>
""",
    "os-deadlock-det": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Deadlock detection lets deadlock happen, periodically scans resource allocation graphs for cycles, and recovers by killing processes or preempting resources."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking deadlock detection is overhead-free. It adds CPU cycles. <strong>Depth:</strong> Compare process termination vs resource preemption recovery.</p>
</div>
""",
    "os-file-systems": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"File systems organize disk blocks. Contrast contiguous (fast, external fragmentation), linked (no fragmentation, slow random access), and indexed (uses index blocks)."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Saying FAT has no index table. The File Allocation Table is a linked allocation index. <strong>Depth:</strong> Explain UNIX inodes and direct/indirect pointer blocks.</p>
</div>
""",
    "os-disk-sched": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Disk scheduling reduces head movement. Contrast SSTF (shortest seek, starvation risk) and SCAN (elevator, goes end-to-end) / LOOK (reverses at last request)."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> SSTF is starvation-free. It is not; continuous local requests starve distant ones. <strong>Depth:</strong> Calculate total head movements for a sequence.</p>
</div>
""",
    "os-kernel": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Kernel is the core OS program. Monolithic kernels run all OS services in kernel space (fast, crash-prone). Microkernels run services in user space (modular, slower IPC)."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Saying Windows is strictly microkernel. It is a hybrid kernel. <strong>Depth:</strong> Detail microkernel IPC overhead and security boundaries.</p>
</div>
""",
    "os-syscalls": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Syscalls are the programming interface to request kernel resources. The CPU triggers a software interrupt (trap) to switch from user mode to kernel mode."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Confusing library calls with syscalls (e.g. `printf` calls `write` syscall). <strong>Depth:</strong> Name standard syscall categories (file, process, device).</p>
</div>
""",
    "os-ipc": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"IPC lets processes share data. Contrast shared memory (fast, developer manages sync) and message passing (kernel handles sync, slower context switches)."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Shared memory requires system calls for every write. Syscall is only needed to map it. <strong>Depth:</strong> Explain anonymous vs named pipes and sockets.</p>
</div>
""",
    "os-segmentation-frag": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Segmentation divides memory into logical blocks (code, heap, stack) matching programmer's view, causing external fragmentation over time."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Saying segmentation uses fixed size. Segments have dynamic lengths. <strong>Depth:</strong> Calculate physical address from segment table offset.</p>
</div>
""",
    "os-tlb-cache": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"TLB is a fast associative cache on the MMU. It caches page table translations to bypass double memory accesses, keeping address translation overhead low."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> TLB caches program data. It only caches address translations. <strong>Depth:</strong> Explain TLB hits, TLB misses, and page table walks.</p>
</div>
""",
    "os-user-kernel": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Dual mode protects the system. User applications run in ring 3 (restricted instruction set), while kernel mode runs in ring 0 with full access."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> User apps can write directly to disk. They must trap to kernel mode. <strong>Depth:</strong> Explain instruction sets and hardware protection rings.</p>
</div>
""",
    "os-linking-loading": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Linker binds compiled object files into one executable. Loader copies the executable into RAM, sets registers, and jumps to the starting instruction."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Static linking is runtime loadable. It is embedded at compile time. <strong>Depth:</strong> Contrast DLLs / Shared Libraries vs static libraries.</p>
</div>
""",
    "os-spooling": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Spooling (Simultaneous Peripheral Ops On-Line) uses disk buffers to let slow devices (printers) process data asynchronously without blocking fast CPUs."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Spooling is identical to buffering. Buffering overlaps I/O of single jobs; spooling queues multiple jobs. <strong>Depth:</strong> Print spooler architecture.</p>
</div>
""",
    "os-rtos": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"RTOS guarantees task execution within strict deadlines. Contrast hard RTOS (catastrophic failure if deadline missed) and soft RTOS (graceful degradation)."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking RTOS is faster at math than general OS. It is just more predictable. <strong>Depth:</strong> Explain rate-monotonic CPU scheduling.</p>
</div>
"""
}

HIGH_YIELD_TOPICS = ["os-proc-thread", "os-sync-prims", "os-deadlock-conds", "os-mem-manage", "os-virt-mem"]

# ─────────────────────────────────────────
# HELPERS FOR FOLLOW-UPS AND SPACE FILLERS
# ─────────────────────────────────────────
def get_topic_followups(tid):
    followups_dict = {
        "os-proc-thread": "• What is a thread pool?<br>• Differentiate user-level vs kernel-level threads.",
        "os-cpu-sched": "• What is convoy effect in FCFS?<br>• How is time quantum chosen in Round Robin?",
        "os-pcb-ctx": "• What is the ready queue storage structure?<br>• What triggers a context switch?",
        "os-mlq": "• What is the aging mechanism?<br>• How does feedback queue scheduling work?",
        "os-mem-manage": "• What is internal fragmentation?<br>• What is dynamic storage allocation?",
        "os-virt-mem": "• What is copy-on-write (COW)?<br>• How large is a standard page table?",
        "os-page-replace": "• Explain the LRU cache implementation.<br>• How does the Second Chance algorithm work?",
        "os-fault-thrashing": "• What is the working set model?<br>• How does a page fault rate monitor prevent thrashing?",
        "os-crit-sec": "• What are the three requirements for critical section?<br>• How does TestAndSet instruction work?",
        "os-sync-prims": "• What is priority inversion?<br>• Differentiate spinlock vs mutex.",
        "os-sync-problems": "• How does monitor differ from semaphore?<br>• Explain the dining philosophers deadlock solution.",
        "os-deadlock-conds": "• Differentiate deadlock vs starvation.<br>• How do we prevent circular wait?",
        "os-bankers": "• What is a safe state?<br>• What is the time complexity of Banker's?",
        "os-deadlock-det": "• How often should a deadlock detection run?<br>• What is resource preemption?",
        "os-file-systems": "• What is a superblock?<br>• How do hard links differ from soft links?",
        "os-disk-sched": "• Why does SSTF cause starvation?<br>• What is the difference between SCAN and C-SCAN?",
        "os-kernel": "• What is monolithic architecture?<br>• What is microkernel IPC overhead?",
        "os-syscalls": "• Differentiate hardware vs software interrupts.<br>• What is the purpose of interrupt vector table?",
        "os-ipc": "• Explain pipe vs socket.<br>• Differentiate synchronous vs asynchronous message passing.",
        "os-segmentation-frag": "• What is compaction in memory?<br>• Differentiate internal vs external fragmentation.",
        "os-tlb-cache": "• What is TLB reach?<br>• Explain TLB miss handling.",
        "os-user-kernel": "• What is dual-mode operation?<br>• List some privileged instructions.",
        "os-linking-loading": "• What does a linker do?<br>• Differentiate DLL vs static library.",
        "os-spooling": "• Why is spooling called concurrent?<br>• Where is the spool buffer located?",
        "os-rtos": "• Differentiate hard vs soft RTOS.<br>• What is rate monotonic scheduling?"
    }
    return followups_dict.get(tid, "• List related OS primitives.<br>• How does the kernel optimize this mechanism?")

def get_os_space_filler(tid):
    fillers = {
        "os-proc-thread": """
<div class="box box-depth">
  <div class="box-title">📈 Interview Depth Progression</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Basic):</strong> Contrast process isolation with thread resource sharing.<br>
    <strong>Level 2 (PDU):</strong> Detail thread stacks vs shared process heaps.<br>
    <strong>Level 3 (Switching):</strong> Explain why thread switching avoids TLB flushes.<br>
    <strong>Level 4 (Design):</strong> Explain thread pool architecture and worker queue limits.
  </div>
</div>
""",
        "os-cpu-sched": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "Why is preemptive scheduling used in interactive systems?"<br>
    <strong>Candidate:</strong> "To guarantee responsiveness. If a long process runs non-preemptively, user inputs will lag. Preemption enforces time-slicing (e.g., Round Robin), ensuring CPU access for GUI tasks."
  </div>
</div>
""",
        "os-pcb-ctx": """
<div class="box box-depth">
  <div class="box-title">📈 CPU Context Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (State):</strong> Explain that PCB stores process ID, program counter, and state.<br>
    <strong>Level 2 (Mechanism):</strong> Describe CPU register backup to PCB during interrupts.<br>
    <strong>Level 3 (Overhead):</strong> Explain why TLB miss penalty occurs post context switch.<br>
    <strong>Level 4 (Hardware):</strong> Discuss hardware-assisted context switching with register windows.
  </div>
</div>
""",
        "os-mlq": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "What is the key difference between MLQ and MLFQ?"<br>
    <strong>Candidate:</strong> "MLQ has static queues where processes stay in their assigned queues. MLFQ allows processes to move dynamically between queues based on CPU burst history, solving starvation via aging."
  </div>
</div>
""",
        "os-mem-manage": """
<div class="box box-depth">
  <div class="box-title">⚖️ Allocation Strategy Trade-offs</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>First Fit:</strong> Fastest search; allocates the first block that fits. Leaves fragments at the beginning.<br>
    <strong>Best Fit:</strong> Searches entire list to find smallest block that fits. Minimizes leftover size, but creates tiny useless fragments.<br>
    <strong>Worst Fit:</strong> Allocates largest available block. Leaves largest leftover block, which is reusable.
  </div>
</div>
""",
        "os-virt-mem": """
<div class="box box-depth">
  <div class="box-title">📈 Memory Depth Progression</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Concept):</strong> Virtual Memory provides contiguous private address space.<br>
    <strong>Level 2 (Paging):</strong> Maps virtual pages to non-contiguous physical frames via Page Tables.<br>
    <strong>Level 3 (MMU):</strong> Hardware MMU translates addresses using TLB cache queries.<br>
    <strong>Level 4 (Multi-Level):</strong> Hierarchical page tables save RAM but increase access RTTs.
  </div>
</div>
""",
        "os-page-replace": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "What is Belady's Anomaly and when does it occur?"<br>
    <strong>Candidate:</strong> "Belady's Anomaly is when a page replacement algorithm causes more page faults as physical memory frames increase. It occurs in FIFO page replacement, but never in stack-based algorithms like LRU."
  </div>
</div>
""",
        "os-fault-thrashing": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "How do you detect and fix thrashing in a system?"<br>
    <strong>Candidate:</strong> "We check if CPU utilization drops while paging rate spikes. We fix it by terminating active processes, adding RAM, or using the working-set model to allocate sufficient pages per process."
  </div>
</div>
""",
        "os-crit-sec": """
<div class="box box-depth">
  <div class="box-title">📈 Critical Section Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Goal):</strong> Prevent multiple threads from executing in critical code simultaneously.<br>
    <strong>Level 2 (Laws):</strong> Satisfy Mutual Exclusion, Progress, and Bounded Waiting.<br>
    <strong>Level 3 (Software):</strong> Analyze Peterson's two-process software algorithm limitations.<br>
    <strong>Level 4 (Hardware):</strong> Detail atomic instructions like TestAndSet or CompareAndSwap.
  </div>
</div>
""",
        "os-sync-prims": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "Can a thread release a Mutex it does not own?"<br>
    <strong>Candidate:</strong> "No. Mutexes have strict ownership; only the thread that locks can unlock. Semaphores are signaling variables without ownership, so any thread can call signal/release to unblock a waiter."
  </div>
</div>
""",
        "os-sync-problems": """
<div class="box box-depth">
  <div class="box-title">⚖️ Problem Sync Rules</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Bounded Buffer:</strong> Synchronizes producer and consumer. Uses empty/full counting semaphores to block queue boundaries.<br>
    <strong>Readers-Writers:</strong> Multiple readers allowed, but writers get exclusive access. Starvation occurs if readers stream constantly.<br>
    <strong>Dining Philosophers:</strong> Evaluates resource deadlocks. Solved by asymmetric seating or resource acquisition ordering.
  </div>
</div>
""",
        "os-deadlock-conds": """
<div class="box box-depth">
  <div class="box-title">📈 Deadlock Prevention Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Lock):</strong> Explain that deadlock is a circular block of threads waiting on locks.<br>
    <strong>Level 2 (Coffman):</strong> Identify Mutual Exclusion, Hold-Wait, No Preemption, and Circular Wait.<br>
    <strong>Level 3 (Break):</strong> Prevent deadlock by breaking Circular Wait (imposing resource indices).<br>
    <strong>Level 4 (Starve):</strong> Differentiate deadlock (stuck locks) from livelock (active state shifts).
  </div>
</div>
""",
        "os-bankers": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "Why isn't Banker's algorithm used in general-purpose operating systems?"<br>
    <strong>Candidate:</strong> "It requires processes to declare their maximum resource needs in advance, which dynamic desktop applications cannot do. It also assumes a fixed resource pool and has O(M*N^2) overhead."
  </div>
</div>
""",
        "os-deadlock-det": """
<div class="box box-depth">
  <div class="box-title">📈 Detection & Recovery Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Check):</strong> Run detection algorithms periodically using Resource Allocation Graphs.<br>
    <strong>Level 2 (Cycle):</strong> Detect cycles in single-instance systems using Wait-For Graph walks.<br>
    <strong>Level 3 (Kill):</strong> Recover by terminating deadlock cycle processes one-by-one.<br>
    <strong>Level 4 (Rollback):</strong> Preempt resources, rolling processes back to saved safe checkpoints.
  </div>
</div>
""",
        "os-file-systems": """
<div class="box box-depth">
  <div class="box-title">📈 Inode Storage Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Metadata):</strong> Inode stores file size, permissions, owner, and block pointers.<br>
    <strong>Level 2 (Block Pointers):</strong> Direct pointers link to file blocks; indirect pointers link to block lists.<br>
    <strong>Level 3 (Pointers):</strong> Single, double, and triple indirect pointers enable large file limits.<br>
    <strong>Level 4 (Links):</strong> Hard links point to the same inode; symbolic links point to paths.
  </div>
</div>
""",
        "os-disk-sched": """
<div class="box box-depth">
  <div class="box-title">⚖️ Disk Scan Trade-offs</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>SSTF:</strong> Serviced closest request. Minimizes seek time but suffers from severe starvation.<br>
    <strong>SCAN (Elevator):</strong> Head moves in one direction to end, then reverses. Solves starvation but causes queue unfairness.<br>
    <strong>C-SCAN (Circular):</strong> Head sweeps in one direction, then returns to beginning without servicing. Ensures uniform wait time.
  </div>
</div>
""",
        "os-kernel": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "Why does macOS use a hybrid kernel rather than a pure microkernel?"<br>
    <strong>Candidate:</strong> "Pure microkernels require extensive context switches and IPC message passing for simple tasks, degrading performance. Hybrid kernels keep security benefits but run core services in kernel space."
  </div>
</div>
""",
        "os-syscalls": """
<div class="box box-depth">
  <div class="box-title">📈 System Call Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (System):</strong> Syscalls provide the user-to-kernel interface for file/process operations.<br>
    <strong>Level 2 (Trap):</strong> CPU switches mode using a trap instruction, passing parameters via registers.<br>
    <strong>Level 3 (Interrupt):</strong> Kernel queries the Interrupt Vector Table to find the handler.<br>
    <strong>Level 4 (ISR):</strong> Interrupt Service Routine executes, resetting the CPU privilege state.
  </div>
</div>
""",
        "os-ipc": """
<div class="box box-depth">
  <div class="box-title">⚖️ Shared Memory vs Message Passing</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Shared Memory:</strong> High-speed mapping of RAM between process spaces. Zero kernel overhead after setup, but requires process-level synchronization (mutexes).<br>
    <strong>Message Passing:</strong> Kernel-mediated buffers (pipes/queues). Slower due to syscall overhead, but safe and easy to implement.
  </div>
</div>
""",
        "os-segmentation-frag": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "Why does segmentation lead to external fragmentation?"<br>
    <strong>Candidate:</strong> "Segments are logical units of variable size. As segments are allocated and deallocated from memory, the remaining free spaces become chopped into small, isolated holes that cannot satisfy large segment requests."
  </div>
</div>
""",
        "os-tlb-cache": """
<div class="box box-depth">
  <div class="box-title">📈 TLB Operation Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Cache):</strong> TLB is a fast hardware cache inside MMU to store active translations.<br>
    <strong>Level 2 (Lookup):</strong> On miss, CPU performs multi-level page table walks in RAM.<br>
    <strong>Level 3 (Context):</strong> Context switch flushes TLB to prevent cross-process data leakage.<br>
    <strong>Level 4 (Tags):</strong> Address Space Identifiers (ASID) tag translations, avoiding flush costs.
  </div>
</div>
""",
        "os-user-kernel": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "What happens if a user-mode application tries to run a privileged instruction?"<br>
    <strong>Candidate:</strong> "The CPU hardware blocks it, raises a general protection fault interrupt, traps to the kernel handler, and terminates the user process with a segmentation fault."
  </div>
</div>
""",
        "os-linking-loading": """
<div class="box box-depth">
  <div class="box-title">⚖️ Static vs Dynamic Linking</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Static Linking:</strong> Library code is copied directly into the binary at compile time. Large executables, but runs independently without runtime dependencies.<br>
    <strong>Dynamic Linking:</strong> Binary contains pointers to shared libraries (.so/.dll). Saves disk/RAM space, but fails if libraries are missing.
  </div>
</div>
""",
        "os-spooling": """
<div class="box box-depth">
  <div class="box-title">📈 Queue & Spool Depth</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Concept):</strong> Spooling uses disk queues to coordinate slow I/O device access.<br>
    <strong>Level 2 (Spool):</strong> Contrast buffering (RAM buffer for speed matches) with spooling (disk queues).<br>
    <strong>Level 3 (Concur):</strong> Spooling allows overlapping I/O of multiple concurrent jobs.<br>
    <strong>Level 4 (Kernel):</strong> Print spooler process reads disk queue blocks and sends them to printer NIC.
  </div>
</div>
""",
        "os-rtos": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "Why is standard Linux not suitable for safety-critical real-time applications?"<br>
    <strong>Candidate:</strong> "Standard Linux optimizes for average throughput, introducing unpredictable scheduling latency and priority inversion. Safety-critical systems require an RTOS to guarantee hard deadline constraints."
  </div>
</div>
"""
    }
    return fillers.get(tid, get_default_space_filler())

def get_default_space_filler():
    return """
<div class="box box-depth">
  <div class="box-title">📈 Depth Progression</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Basic):</strong> Understand the main definition and syntax.<br>
    <strong>Level 2 (Intermediate):</strong> Learn execution trace and typical memory states.<br>
    <strong>Level 3 (Advanced):</strong> Analyze corner cases and optimization schemes.<br>
    <strong>Level 4 (Expert):</strong> Handle system integration trade-offs.
  </div>
</div>
"""

def get_os_industry_box(tid):
    industry_usage = {
        "os-proc-thread": "Web servers like Nginx use a multi-process architecture for isolation, while database engines like MySQL use a multi-threaded approach to share memory buffers efficiently.",
        "os-cpu-sched": "Linux's Completely Fair Scheduler (CFS) uses red-black trees to schedule process execution, balancing interactive desktop threads and background database workers.",
        "os-pcb-ctx": "Hypervisors (like KVM or VMware ESXi) swap virtual CPU registers in physical CPU cores during guest VM context switches, adding virtualization overhead.",
        "os-mlq": "Real-time operating systems (RTOS) in automotive engine control units (ECUs) segregate critical safety-critical tasks from telemetry tasks in prioritized queues.",
        "os-mem-manage": "High-performance search engines (like Elasticsearch) configure JVM heap allocations using custom memory mapping (mmap) flags to avoid fragmentation latency.",
        "os-virt-mem": "Cloud hypervisors overcommit RAM by mapping guest physical memory pages to swap space on NVMe drives, optimizing server hardware utilization.",
        "os-page-replace": "Content Delivery Networks (CDNs) like Cloudflare use Least Recently Used (LRU) variants to cache assets, evicting cold assets from edge node RAM.",
        "os-fault-thrashing": "Kubernetes monitors page fault rates of container pods; high thrashing rates trigger automatic horizontal scaling or pod restarts.",
        "os-crit-sec": "Distributed lock managers (like Redis-based Redlock or ZooKeeper) enforce critical section locks across microservices to prevent double-spending bugs.",
        "os-sync-prims": "Node.js cluster workers coordinate shared memory ports using atomic buffers and mutex locks to process incoming TCP requests concurrently.",
        "os-sync-problems": "Browser rendering engines serialize document reads and concurrent canvas writes using read-write locks to prevent screen tearing artifact bugs.",
        "os-deadlock-conds": "Database transaction engines (like InnoDB) impose lock hierarchies (e.g., ordering primary key modifications) to break circular wait conditions.",
        "os-bankers": "Safety-critical aviation control systems use Banker's algorithm logic to pre-calculate resource limits before starting autonomous flight routines.",
        "os-deadlock-det": "PostgreSQL runs background deadlock detection workers to trace wait-for-graphs and abort blocked transactions to resume database execution.",
        "os-file-systems": "Modern cloud filesystems (like AWS EFS or GCP Filestore) manage metadata pointers using inodes, optimizing index block lookups for mass scale.",
        "os-disk-sched": "Solid-State Drive (SSD) controllers use internal Flash Translation Layers (FTL) to route flash sweeps, rendering traditional elevator disk sweeps obsolete.",
        "os-kernel": "Edge routers use monolithic kernels (like Linux) for maximum packet-routing speed, while secure smart cards use microkernels to isolate cryptographic tasks.",
        "os-syscalls": "Docker containers restrict system calls (like `ptrace` or `sys_chroot`) using SECCOMP profiles to prevent privilege escalation container escape bugs.",
        "os-ipc": "Microservice communication protocols (like gRPC or HTTP/2) run internal IPC pipes (like Unix domain sockets) when running on the same host to bypass TCP overhead.",
        "os-segmentation-frag": "Intel hardware memory controllers support segmentation registers to enforce sandbox boundaries for browser javascript sandboxing environments.",
        "os-tlb-cache": "High-frequency trading architectures run on CPU cores configured with HugePages (2MB or 1GB frames) to maximize TLB hits and reduce translation latency.",
        "os-user-kernel": "Nvidia GPU driver modules transition between user space APIs (like CUDA) and privileged kernel modules to coordinate parallel pipeline runs.",
        "os-linking-loading": "Application runtimes (like Java Virtual Machine or Node) resolve dynamic library bindings at startup, lazy-loading shared object files as needed.",
        "os-spooling": "Enterprise network print systems and queuing services (like RabbitMQ) spool batch requests onto persistent queues to decouple fast clients from slow devices.",
        "os-rtos": "Autonomous vehicle control units use real-time kernels (like QNX or FreeRTOS) to guarantee execution of collision avoidance logic within milliseconds."
    }
    desc = industry_usage.get(tid, "Operating system concepts are utilized by container runtimes, database engines, and networking stacks to coordinate hardware resource sharing.")
    return f"""
<div class="box box-industry" style="padding: 10px; margin-bottom: 0; border: 1px solid #F5E6B3; background: #FDF6E3;">
  <div class="box-title" style="font-size: 8pt; color: #B7791F; margin-bottom: 4px;">🏭 Where Used in Industry</div>
  <p style="font-size: 7.5pt; line-height: 1.35; color: #5C5438; margin: 0;">{desc}</p>
</div>
"""

def get_os_depth_box(tid):
    depth_levels = {
        "os-proc-thread": [
            "Process vs Thread isolation models.",
            "Memory differences (private stack vs shared heap).",
            "Process/Thread Control Block kernel allocations.",
            "TLB preservation differences during thread switches.",
            "User-space green threads vs kernel-level scheduling mapping."
        ],
        "os-cpu-sched": [
            "Preemptive vs non-preemptive scheduling algorithms.",
            "Starvation prevention using aging schemes.",
            "Multi-level feedback queue parameter calibration.",
            "Linux CFS red-black tree scheduler mechanics.",
            "Affinity scheduling on multi-core symmetric multiprocessing."
        ],
        "os-pcb-ctx": [
            "PCB structure: PID, Program Counter, registers, files.",
            "Context switch register save/restore lifecycle.",
            "TLB invalidation and CPU cache invalidation costs.",
            "Hardware-level CPU register window swapping.",
            "Interrupt service routine execution context switching."
        ],
        "os-mlq": [
            "Multi-Level Queue partition boundaries.",
            "Priority queues scheduling configurations.",
            "Feedback Queue aging dynamically migrating processes.",
            "Fixed priority preemption with time-sliced background queues.",
            "Solving priority inversion using priority inheritance protocol."
        ],
        "os-mem-manage": [
            "Contiguous memory allocation schemes (First/Best/Worst Fit).",
            "Internal vs External fragmentation causes.",
            "Dynamic memory compaction and relocation overhead.",
            "Linux slab/buddy allocator page distribution.",
            "Process address space virtual layout sections."
        ],
        "os-virt-mem": [
            "Virtual-to-physical address space mapping.",
            "Paging vs Segmentation structural boundaries.",
            "Page table directories structure (Multi-level page tables).",
            "Virtual page eviction flags (dirty, reference, present).",
            "Memory overcommit configurations and OOM killer rules."
        ],
        "os-page-replace": [
            "Page replacement algorithms: FIFO, LRU, Optimal.",
            "Belady's Anomaly triggering on FIFO replacement.",
            "LRU approximation using reference bits (Clock algorithm).",
            "Page buffering and dirty page flushing strategies.",
            "Working set model and page reference string analysis."
        ],
        "os-fault-thrashing": [
            "Page fault handling sequence from trap to disk fetch.",
            "Thrashing triggers: CPU utilization drop vs page fault rise.",
            "Locality model of process memory execution paths.",
            "Page Fault Frequency (PFF) dynamic frame allocation.",
            "Swap space storage configuration on NVMe vs SSD."
        ],
        "os-crit-sec": [
            "Critical Section problem: Mutual Exclusion, Progress, Bounded Waiting.",
            "Software critical section guards (Peterson's solution).",
            "Hardware-assisted synchronization (Test-And-Set, Compare-And-Swap).",
            "Spinlocks busy-waiting vs blocking locks sleep contexts.",
            "Lock-free data structures using atomic CAS primitives."
        ],
        "os-sync-prims": [
            "Mutex vs Semaphore locking/signaling behaviors.",
            "Counting semaphores vs Binary semaphores.",
            "Priority inversion traps and inheritance protocols.",
            "Sleep-wake synchronization queues inside kernel.",
            "Deadlock-free locks using lock timeouts and try-lock."
        ],
        "os-sync-problems": [
            "Bounded-Buffer (Producer-Consumer) queue sync.",
            "Readers-Writers problem priority configurations.",
            "Dining Philosophers resource resource lock structures.",
            "Thread synchronization using monitors and condition variables.",
            "Message passing IPC vs shared memory synchronizations."
        ],
        "os-deadlock-conds": [
            "Coffman conditions: Mutual Exclusion, Hold-Wait, No Preemption, Circular Wait.",
            "Deadlock prevention by breaking hold-and-wait.",
            "Deadlock prevention by breaking circular wait.",
            "Resource allocation graph cycle tracing loops.",
            "Livelock vs Deadlock active thread state execution."
        ],
        "os-bankers": [
            "Deadlock avoidance safe vs unsafe state boundaries.",
            "Banker's algorithm matrix structures (Allocation, Max, Available, Need).",
            "Safety check loop algorithm steps.",
            "Resource request algorithm interception logic.",
            "Banker's algorithm time complexity limitations."
        ],
        "os-deadlock-det": [
            "Deadlock detection algorithms for single/multiple resource types.",
            "Wait-for-graph (WFG) reduction loops.",
            "Recovery strategies: process termination vs resource preemption.",
            "Rollback points to recover database state post deadlock.",
            "Selecting victim processes based on CPU usage and lock durations."
        ],
        "os-file-systems": [
            "File allocation schemes: Contiguous, Linked, Indexed.",
            "Inode structure: Direct blocks, single/double/triple indirect blocks.",
            "Directory structure mapping filenames to inode numbers.",
            "File Allocation Table (FAT) vs Unix Fast File System (FFS) tables.",
            "Journaling filesystems transaction logs write-ahead logs."
        ],
        "os-disk-sched": [
            "Disk arm scheduling algorithms: FCFS, SSTF, SCAN, C-SCAN.",
            "SSTF starvation risks for boundary cylinder sectors.",
            "SCAN/C-SCAN boundary bounce cycles.",
            "Elevator algorithm execution in magnetic disk drivers.",
            "SSD flash block writes garbage collection loops."
        ],
        "os-kernel": [
            "Monolithic vs Microkernel architecture structures.",
            "IPC communication overhead inside Microkernels.",
            "Hybrid kernel architectures (Windows NT kernel).",
            "Exokernel bare-metal resource multiplexing.",
            "Loadable Kernel Modules (LKMs) dynamic load pathways."
        ],
        "os-syscalls": [
            "System call interrupt trap instruction execution.",
            "User space to kernel space hardware CPU ring transitions.",
            "System call table lookup dispatch sequence.",
            "Parameter passing mechanisms (CPU registers vs stack memory).",
            "Virtual System Calls (vDSO) to avoid user-kernel switch context costs."
        ],
        "os-ipc": [
            "IPC mechanisms: Shared Memory, Message Queues, Pipes, Sockets.",
            "Anonymous pipes vs Named pipes (FIFOs) folder files.",
            "Shared memory page mapping context setup.",
            "Blocking vs non-blocking message queue reads.",
            "Unix domain socket performance vs network TCP sockets."
        ],
        "os-segmentation-frag": [
            "Logical segmentation vs physical paging structures.",
            "External fragmentation causing alloc failures.",
            "Segmentation registers base/limit offset checks.",
            "Paged segmentation address translation maps.",
            "Dynamic memory allocator heap fragmentation compaction."
        ],
        "os-tlb-cache": [
            "Translation Lookaside Buffer translation caching.",
            "TLB hit ratio calculation and access time lookup.",
            "TLB miss page table search context walks.",
            "TLB flushes during context switches vs ASID tags.",
            "Multi-level page table TLB access penalties."
        ],
        "os-user-kernel": [
            "Privileged ring-0 kernel mode vs ring-3 user mode.",
            "Kernel mode instruction protection checks.",
            "Privilege escalation attacks using stack overflow buffer writes.",
            "Hardware interrupt vector table routing.",
            "Context save structures (trap frames) in kernel stack."
        ],
        "os-linking-loading": [
            "Static linking object merges vs Dynamic linking stub calls.",
            "Dynamic Linker runtime relocations.",
            "Position Independent Code (PIC) global offset tables.",
            "Loader heap setup and environment variables parser.",
            "Lazy binding PLT/GOT resolution pathways."
        ],
        "os-spooling": [
            "Spooling concurrent batch queues vs Buffering streams.",
            "Spooling temporary storage directories.",
            "Printer daemon spool files parsing sweeps.",
            "Message broker disk spools and consumer offsets.",
            "Spool overflow crash mitigation configurations."
        ],
        "os-rtos": [
            "Hard vs Soft RTOS deadlines guarantees.",
            "Rate Monotonic Scheduling (RMS) static priority math.",
            "Earliest Deadline First (EDF) dynamic scheduling limits.",
            "Interrupt latency and dispatch latency limits.",
            "Priority ceiling protocol to mitigate priority inversion."
        ]
    }
    levels = depth_levels.get(tid, [
        "Core syntax and basic conceptual definitions.",
        "Algorithm steps, scheduling, or access rules.",
        "CPU register states and kernel data structures.",
        "System performance costs and caching behaviors.",
        "Enterprise-scale usage and cloud platform limits."
    ])
    return f"""
<div class="box box-depth" style="padding: 10px; margin-bottom: 0; border-left-color: #3182CE; background: #EBF8FF;">
  <div class="box-title" style="font-size: 8pt; color: #3182CE; margin-bottom: 4px;">📊 Interview Depth</div>
  <div style="font-size: 7.2pt; line-height: 1.35; color: #2D3748;">
    <strong>L1:</strong> {levels[0]}<br>
    <strong>L2:</strong> {levels[1]}<br>
    <strong>L3:</strong> {levels[2]}<br>
    <strong>L4:</strong> {levels[3]}<br>
    <strong>L5:</strong> {levels[4]}
  </div>
</div>
"""

# ─────────────────────────────────────────
# GENERATE_PAGE: 14-Section Template with Bottom Grid
# ─────────────────────────────────────────
def generate_page(topic, current_page, total_pages):
    num = topic['num']
    title = topic['title']
    subtitle = topic['subtitle']
    chapter = topic['chapter']
    left_col = topic['left_col']
    right_col = topic['right_col']
    trap = topic['trap']
    trick = topic['trick']
    tid = topic['id']
    stars = topic['yield_stars']
    
    page_indicator = f"PAGE {str(current_page).zfill(2)} / {str(total_pages).zfill(2)}"
    
    # Conditional High Yield Badge (Top 20%)
    header_right_content = """
        <div class="badge-yield">🔥 HIGH YIELD</div>
        <div class="header-badge">Placement Handbook</div>
    """ if tid in HIGH_YIELD_TOPICS else """
        <div class="header-badge">Core CS Notes</div>
    """
    
    # Space Filler Content
    space_filler = get_os_space_filler(tid)
    industry_box = get_os_industry_box(tid)
    depth_box = get_os_depth_box(tid)
    left_col_updated = left_col + "\n" + industry_box + "\n" + depth_box
    
    # Extract Mistake from booster HTML using re
    import re
    booster_html = OS_BOOSTERS.get(tid, "")
    mistake_text = "Believing that textbook definitions are sufficient; always lead with real-world trade-offs."
    
    mistake_match = re.search(r"Mistake:</strong>\s*(.*?)\s*<strong>", booster_html)
    if not mistake_match:
        mistake_match = re.search(r"Mistake:</strong>\s*(.*?)\s*$", booster_html)
    if mistake_match:
        mistake_text = mistake_match.group(1).replace("</p>", "").strip()
        
    followups_text = get_topic_followups(tid)
    
    return f"""
  <div class="page" id="{tid}">
    <!-- Header (L1) -->
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        {header_right_content}
      </div>
    </div>

    <!-- Topic Bar (L2) -->
    <div class="topic-bar">
      <div class="topic-bar-top">
        <div class="topic-eyebrow">{chapter}</div>
        <div class="yield-rating">Yield: <span class="stars-gold">{stars}</span></div>
      </div>
      <div class="topic-title">{num} - {title}</div>
      <div class="topic-subtitle">{subtitle}</div>
    </div>

    <!-- Body Container (L3) -->
    <div class="body-container">
      <!-- Left Column -->
      <div class="col-left">
        {left_col_updated}
      </div>
      
      <!-- Right Column -->
      <div class="col-right">
        {right_col}
        <!-- Space Filler replacing the old What to Say booster -->
        {space_filler}
      </div>
    </div>

    <!-- Bottom Placement Grid (L4) - 4-part placement section above the footer -->
    <div class="bottom-placement-grid">
      <div class="placement-block block-mistake">
        <div class="placement-block-title">⚠️ Common Mistake</div>
        <div>{mistake_text}</div>
      </div>
      <div class="placement-block block-trap">
        <div class="placement-block-title">🛑 Interviewer Trap</div>
        <div>{trap}</div>
      </div>
      <div class="placement-block block-followups">
        <div class="placement-block-title">🔄 Top Follow-Ups</div>
        <div>{followups_text}</div>
      </div>
      <div class="placement-block block-trick">
        <div class="placement-block-title">💡 Memory Trick</div>
        <div>{trick}</div>
      </div>
    </div>
    
    <!-- Footer (L5) -->
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> OS <span>›</span> <span>{title}</span></div>
      </div>
      <div class="page-number-premium">
        {page_indicator}
      </div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# ROADMAP PAGE (Page 2)
# ─────────────────────────────────────────
roadmap_page = f"""
  <div class="page roadmap-page" id="os-roadmap">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="header-badge" style="background: rgba(255,255,255,0.25);">OS ROADMAP</div>
      </div>
    </div>
    
    <div style="padding: 30px 40px; flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
      <div>
        <div style="font-size: 26pt; font-weight: 800; color: #111; margin-bottom: 8px;">Operating Systems Roadmap</div>
        <div style="font-size: 11pt; color: #EA763F; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px;">Placement Preparation Guide</div>
        
        <div style="background: #FFF5F0; border-left: 5px solid #EA763F; padding: 14px 20px; border-radius: 6px; margin-bottom: 25px;">
          <strong style="color: #EA763F; font-size: 11pt; display: block; margin-bottom: 6px;">How to use this Handbook:</strong>
          <p style="font-size: 9.5pt; color: #4A5568; line-height: 1.5;">Operating system concepts are heavily tested using comparative questions (Mutex vs Semaphore, Paging vs Segmentation). Focus on how the kernel coordinates system calls, context switching, RAM paging boundaries, and deadlock prevention states.</p>
        </div>

        <div style="margin-top: 15px;">
          <div style="font-size: 12pt; font-weight: 800; color: #1A202C; margin-bottom: 12px; border-bottom: 2px solid #E2E8F0; padding-bottom: 6px;">🎯 Three-Phase Learning Plan</div>
          
          <div style="display: flex; gap: 15px; margin-bottom: 15px;">
            <div style="background: #EBF8FF; border: 1px solid #BEE3F8; border-radius: 8px; padding: 12px; flex: 1;">
              <span style="background: #3182CE; color: white; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 7.5pt; text-transform: uppercase;">Phase 1</span>
              <strong style="display: block; font-size: 9.5pt; margin-top: 6px; color: #2B6CB0;">Scheduling &amp; Memory</strong>
              <p style="font-size: 8pt; color: #4A5568; margin-top: 4px;">Master CPU scheduling algorithms, processes vs threads, paging, segmentation, and virtual swapping. (Topics 1 - 8)</p>
            </div>
            
            <div style="background: #F0FFF4; border: 1px solid #C6F6D5; border-radius: 8px; padding: 12px; flex: 1;">
              <span style="background: #38A169; color: white; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 7.5pt; text-transform: uppercase;">Phase 2</span>
              <strong style="display: block; font-size: 9.5pt; margin-top: 6px; color: #276749;">Synchronization &amp; Deadlock</strong>
              <p style="font-size: 8pt; color: #4A5568; margin-top: 4px;">Deep-dive into mutexes, semaphores, classic dining philosophers solutions, and Banker's deadlock safety checks. (Topics 9 - 14)</p>
            </div>
            
            <div style="background: #FFFFF0; border: 1px solid #FEFCBF; border-radius: 8px; padding: 12px; flex: 1;">
              <span style="background: #D69E2E; color: white; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 7.5pt; text-transform: uppercase;">Phase 3</span>
              <strong style="display: block; font-size: 9.5pt; margin-top: 6px; color: #B7791F;">Architecture &amp; Storage</strong>
              <p style="font-size: 8pt; color: #4A5568; margin-top: 4px;">Study inodes, disk sweeps, system call interrupts, IPC, privileged CPU modes, and dynamic linker stubs. (Topics 15 - 25)</p>
            </div>
          </div>
        </div>
      </div>

      <div style="border-top: 2px solid #E2E8F0; padding-top: 20px; display: flex; justify-content: space-between; align-items: center;">
        <div style="font-size: 8.5pt; color: #718096;">
          <strong>Target Completion:</strong> 2 Hours Core Study &amp; 30 Mins Self-Recall
        </div>
        <div style="font-size: 8.5pt; color: #EA763F; font-weight: 800; text-align: right; line-height: 1.3;">
          Created by Pranav Gawai<br>
          <span style="font-size: 7.5pt; color: #718096; font-weight: 500;">grindos.pranavx.in</span>
        </div>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> OS <span>›</span> <span>Roadmap</span></div>
      </div>
      <div class="page-number-premium">PAGE 02 / 35</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# DYNAMIC TABLE OF CONTENTS (Page 3)
# ─────────────────────────────────────────
toc_rows = ""
chapters_seen = {}
for t in topics:
    ch = t['chapter']
    if ch not in chapters_seen:
        chapters_seen[ch] = []
    chapters_seen[ch].append(t)

# Page indices: Cover = 1, Roadmap = 2, TOC = 3, content starts at 4
for ch_name, ch_topics in chapters_seen.items():
    toc_rows += f"""
    <div style="font-size: 9.5pt; font-weight: 800; color: #EA763F; text-transform: uppercase; letter-spacing: 1px; margin-top: 14px; margin-bottom: 6px;">{ch_name}</div>
    """
    for t in ch_topics:
        idx = int(t['num']) + 3
        page_str = str(idx).zfill(2)
        toc_rows += f"""
        <div style="display: flex; align-items: flex-end; margin-bottom: 6px; font-size: 10pt; font-weight: 700; color: #2D3748;">
          <a href="#{t['id']}" style="display: flex; width: 100%; align-items: flex-end; text-decoration: none; color: inherit;">
            <span style="color: #EA763F; width: 28px; font-weight: 800;">{t['num']}</span>
            <span style="background: white; padding-right: 8px;">{t['title']}</span>
            <span style="flex: 1; border-bottom: 2px dotted #CBD5E0; position: relative; top: -3px; margin: 0 6px;"></span>
            <span style="color: #718096; font-weight: 800; padding-left: 6px;">p.{page_str}</span>
          </a>
        </div>
        """

toc_page = f"""
  <div class="page toc-page" id="os-toc">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="header-badge" style="background: rgba(255,255,255,0.25);">INDEX</div>
      </div>
    </div>
    
    <div class="toc-inner" style="padding: 24px 40px; flex:1; display:flex; flex-direction:column; justify-content:space-between;">
      <div>
        <div style="font-size: 24pt; font-weight: 800; color: #111; border-bottom: 4px solid #EA763F; display: inline-block; padding-bottom: 6px; margin-bottom: 8px; letter-spacing: -0.5px;">Table of Contents</div>
        <div style="font-size: 9pt; color: #A0AEC0; font-weight: 600; margin-bottom: 12px;">Operating Systems · Placement Preparation Handbook</div>
        {toc_rows}
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> OS <span>›</span> <span>Index</span></div>
      </div>
      <div class="page-number-premium">PAGE 03 / 35</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# FINAL REVISION PAGE (Page 29)
# ─────────────────────────────────────────
final_revision_page = f"""
  <div class="page final-rev-page" id="os-finalrev">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="badge-yield" style="background:#FFF5F0; color:#EA763F;">⚡ CRAM SHEET</div>
        <div class="header-badge">OS Final Revision</div>
      </div>
    </div>
    
    <div style="padding: 24px 30px; display: flex; flex-direction: column; gap: 14px; flex: 1;">
      <div style="text-align: center;">
        <div style="font-size: 20pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">OS Last-Minute Revision Sheet</div>
        <div style="font-size: 9.5pt; color: #EA763F; font-weight: 700; margin-top: 4px;">Top Algorithms, Deadlock Laws, and High-Yield Summaries</div>
      </div>
      
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
        <div style="border: 1px solid #CBD5E0; border-radius: 8px; padding: 12px; background: white;">
          <strong style="color: #EA763F; font-size: 9pt; display: block; margin-bottom: 6px; border-bottom: 1.5px solid #EA763F; padding-bottom: 2px;">⚡ SCHEDULING &amp; MEMORY SUMMARY</strong>
          <table style="width: 100%; font-size: 8pt; border-collapse: collapse;">
            <tr style="border-bottom: 1px solid #E2E8F0;"><td style="font-weight:bold; padding:3px 0;">SJF</td><td>Optimal CPU scheduling, minimizes wait times.</td></tr>
            <tr style="border-bottom: 1px solid #E2E8F0;"><td style="font-weight:bold; padding:3px 0;">Round Robin</td><td>Uses time-slicing (quantum), ensures fairness.</td></tr>
            <tr style="border-bottom: 1px solid #E2E8F0;"><td style="font-weight:bold; padding:3px 0;">Paging</td><td>Virtual page → Physical frame map (No external frag).</td></tr>
            <tr style="border-bottom: 1px solid #E2E8F0;"><td style="font-weight:bold; padding:3px 0;">Segmentation</td><td>Variable-length blocks (stack/heap, causes external frag).</td></tr>
            <tr style="border-bottom: 1px solid #E2E8F0;"><td style="font-weight:bold; padding:3px 0;">Belady's Anomaly</td><td>FIFO page fault increases as physical frames increase.</td></tr>
          </table>
        </div>
        
        <div style="border: 1px solid #CBD5E0; border-radius: 8px; padding: 12px; background: white;">
          <strong style="color: #2B6CB0; font-size: 9pt; display: block; margin-bottom: 6px; border-bottom: 1.5px solid #2B6CB0; padding-bottom: 2px;">📏 OPERATING SYSTEM LAWS</strong>
          <ul style="font-size: 8pt; list-style-type: square; padding-left: 14px; line-height: 1.4; color: #4A5568;">
            <li><strong>Coffman Laws:</strong> Mutual exclusion, hold-wait, no-preemption, circular wait.</li>
            <li><strong>Banker's Goal:</strong> Allocate resource ONLY if it leaves system in Safe State.</li>
            <li><strong>TLB Mission:</strong> Cache page table translations to speed paging.</li>
            <li><strong>Aging Solution:</strong> Solve scheduling starvation by incrementing wait priorities.</li>
            <li><strong>Thrashing Trigger:</strong> CPU spends more time swapping pages than running tasks.</li>
          </ul>
        </div>
      </div>
      
      <div style="border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px; background: #FEF8F4;">
        <strong style="color: #276749; font-size: 9.5pt; display: block; margin-bottom: 6px;">💡 TOP 5 INTERVIEW CONCEPTS TO RECALL</strong>
        <ol style="font-size: 8.5pt; padding-left: 18px; line-height: 1.5; color: #2D3748;">
          <li><strong>Mutex vs Semaphore:</strong> Mutex = locking mechanism with ownership (thread-owned). Semaphore = signaling tool (counting).</li>
          <li><strong>Zombie vs Orphan:</strong> Zombie = exited but parent hasn't wait()-ed. Orphan = active but parent died, init adopts it.</li>
          <li><strong>Context Switch Cost:</strong> CPU registers are swapped out to kernel, cache is flushed. Significant kernel CPU overhead.</li>
          <li><strong>Peterson's Rule:</strong> Software critical-section guard. Satisfies mutual exclusion, progress, and bounded wait.</li>
          <li><strong>Micro vs Monolithic:</strong> Monolithic runs all inside kernel space (fast). Micro runs in user space, communicating via slower IPC.</li>
        </ol>
      </div>

      <div style="border: 1px dashed #EA763F; border-radius: 8px; padding: 12px; background: white; text-align: center;">
        <span style="font-size: 9pt; font-weight: 800; color: #EA763F; display: block; margin-bottom: 4px;">🎯 QUICK SELF-TEST CHECKLIST</span>
        <div style="display: flex; justify-content: center; gap: 20px; font-size: 8pt; color: #718096; font-weight: bold;">
          <span>[ ] Differentiate process and thread</span>
          <span>[ ] List Coffman deadlock conditions</span>
          <span>[ ] Trace LRU page hits</span>
        </div>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> OS <span>›</span> <span>Cheatsheet</span></div>
      </div>
      <div class="page-number-premium">PAGE 29 / 35</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# COMPARISON CHEAT SHEET PAGE (Page 30)
# ─────────────────────────────────────────
def generate_comparison_cheat_sheet(LOGO_BASE64):
    return f"""
  <div class="page" id="os-cheatsheet-comparison">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="badge-yield" style="background:#FFF5F0; color:#EA763F;">⚖️ COMPARISON</div>
        <div class="header-badge">Cheat Sheet</div>
      </div>
    </div>
    
    <div style="padding: 20px 24px; display: flex; flex-direction: column; gap: 8px; flex: 1; overflow: hidden;">
      <div style="text-align: center; margin-bottom: 2px;">
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">OS Comparison Cheat Sheet</div>
        <div style="font-size: 9pt; color: #EA763F; font-weight: 700;">Quick Reference Contrast Tables for Fresher Interviews</div>
      </div>
      
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; flex: 1;">
        <!-- Left Column -->
        <div style="display: flex; flex-direction: column; gap: 8px;">
          <!-- Process vs Thread -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 8px; background: white;">
            <div style="font-size: 8pt; font-weight: 800; color: #EA763F; border-bottom: 1.5px solid #EA763F; padding-bottom: 2px; margin-bottom: 4px; text-transform: uppercase;">Process vs Thread</div>
            <table style="width: 100%; font-size: 7.2pt; border-collapse: collapse; text-align: left;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Process</th><th>Thread</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Address Space</td><td>Independent, private</td><td>Shared with parent</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Overhead</td><td>High (heavy creation)</td><td>Low (lightweight)</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Switching Cost</td><td>High (flushes TLB)</td><td>Low (preserves TLB)</td></tr>
              <tr><td>Fault Isolation</td><td>Strong (crashes alone)</td><td>Weak (crashes process)</td></tr>
            </table>
          </div>
          
          <!-- Mutex vs Semaphore -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 8px; background: white;">
            <div style="font-size: 8pt; font-weight: 800; color: #2B6CB0; border-bottom: 1.5px solid #2B6CB0; padding-bottom: 2px; margin-bottom: 4px; text-transform: uppercase;">Mutex vs Semaphore</div>
            <table style="width: 100%; font-size: 7.2pt; border-collapse: collapse; text-align: left;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Mutex</th><th>Semaphore</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Mechanism</td><td>Locking (Strict Excl)</td><td>Signaling variable</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Ownership</td><td>Yes (Only owner unlocks)</td><td>No (Any thread signals)</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Types</td><td>Single binary lock</td><td>Binary and Counting</td></tr>
              <tr><td>Value</td><td>0 (Locked) or 1 (Free)</td><td>Non-negative integer</td></tr>
            </table>
          </div>

          <!-- User Mode vs Kernel Mode -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 8px; background: white;">
            <div style="font-size: 8pt; font-weight: 800; color: #276749; border-bottom: 1.5px solid #276749; padding-bottom: 2px; margin-bottom: 4px; text-transform: uppercase;">User Mode vs Kernel Mode</div>
            <table style="width: 100%; font-size: 7.2pt; border-collapse: collapse; text-align: left;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>User Mode</th><th>Kernel Mode</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Privileges</td><td>Restricted instructions</td><td>Full hardware access</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Crash Impact</td><td>Process is terminated</td><td>System crashes (Panic)</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Address Space</td><td>User space mappings</td><td>Kernel space direct</td></tr>
              <tr><td>Transitions</td><td>Traps / System Calls</td><td>Resets state flag</td></tr>
            </table>
          </div>
        </div>
        
        <!-- Right Column -->
        <div style="display: flex; flex-direction: column; gap: 8px;">
          <!-- Paging vs Segmentation -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 8px; background: white;">
            <div style="font-size: 8pt; font-weight: 800; color: #7B341E; border-bottom: 1.5px solid #7B341E; padding-bottom: 2px; margin-bottom: 4px; text-transform: uppercase;">Paging vs Segmentation</div>
            <table style="width: 100%; font-size: 7.2pt; border-collapse: collapse; text-align: left;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Paging</th><th>Segmentation</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Block Size</td><td>Fixed (e.g., 4 KB)</td><td>Variable (logical)</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Fragmentation</td><td>Internal (last page)</td><td>External (holes)</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>User Visibility</td><td>Invisible (OS/Hardware)</td><td>Visible (Programmer)</td></tr>
              <tr><td>Address Format</td><td>Page # + Offset</td><td>Segment # + Offset</td></tr>
            </table>
          </div>

          <!-- Deadlock vs Starvation -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 8px; background: white;">
            <div style="font-size: 8pt; font-weight: 800; color: #6B46C1; border-bottom: 1.5px solid #6B46C1; padding-bottom: 2px; margin-bottom: 4px; text-transform: uppercase;">Deadlock vs Starvation</div>
            <table style="width: 100%; font-size: 7.2pt; border-collapse: collapse; text-align: left;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Deadlock</th><th>Starvation</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Description</td><td>Circular block state</td><td>Indefinite wait state</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Process Status</td><td>Blocked (waiting)</td><td>Ready (not scheduled)</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>System Action</td><td>Requires intervention</td><td>Requires Aging priority</td></tr>
              <tr><td>Trigger</td><td>Mutual lock request</td><td>Biased scheduler rules</td></tr>
            </table>
          </div>
        </div>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> OS <span>›</span> <span>Comparisons</span> <span style="font-size:7.5pt; color:#A0AEC0; font-weight:normal; margin-left:10px;">Created by Pranav Gawai</span></div>
      </div>
      <div class="page-number-premium">PAGE 30 / 35</div>
    </div>
  </div>
  """

# ─────────────────────────────────────────
# EXPECTED Q&A GENERATION (Pages 31-32)
# ─────────────────────────────────────────
def generate_expected_qa_pages_new(LOGO_BASE64):
    qas = [
        {
            "q": "What is the difference between a process and a thread, and how does the OS handle them differently?",
            "a": "A process is a completely isolated program instance with its own private address space containing code, data, heap, and file descriptors. Threads, on the other hand, are lightweight execution units that exist inside a process and share the parent's memory heap, code, and OS descriptors, though they each maintain a private stack and program counter. The OS handles processes by giving them strong isolation boundaries, meaning if one process crashes, it won't affect others, but communicating between them requires expensive system calls like IPC or shared memory. Threads share memory natively, which makes communication extremely fast, but a crash in one thread can crash the entire process, and they require synchronization like mutexes to prevent race conditions.",
            "keywords": ["Isolated Address Space", "Shared Heap", "Private Stack", "IPC Overhead", "Synchronization"],
            "followups": "What is a thread pool? How does copy-on-write optimize process fork?",
            "mistake": "Stating that threads share stacks. Each thread has its own private execution stack.",
            "depth": "Detail how virtual page directory mappings differ between process and thread switches."
        },
        {
            "q": "Explain the difference between a Mutex and a Semaphore. When would you use one over the other?",
            "a": "A Mutex is a locking mechanism designed strictly for mutual exclusion. It has a concept of ownership, meaning only the specific thread that acquired the lock can release it. A Semaphore, on the other hand, is a signaling mechanism that manages access to a pool of resources using an integer counter. It doesn't have ownership, so any thread can signal or wait on it. I would use a Mutex when I need to protect a shared variable or critical section of code from concurrent writes by multiple threads. I would use a counting semaphore when I have a finite pool of resources, like a database connection pool, where I want to allow up to 'N' threads to access the resources simultaneously, blocking the N+1th thread.",
            "keywords": ["Lock Ownership", "Signaling Mechanism", "Mutual Exclusion", "Resource Pool", "Thread Synchronization"],
            "followups": "What is a binary semaphore? What is priority inversion?",
            "mistake": "Releasing a Mutex from a different thread than the one that locked it.",
            "depth": "Explain spinlocks vs blocking mutexes and their CPU consumption trade-offs."
        },
        {
            "q": "What is a Deadlock, and what are the four conditions required for a deadlock to occur?",
            "a": "A deadlock is a state where a set of processes are permanently blocked because each process holds a resource and is waiting for another resource held by another process in the same set. For a deadlock to happen, all four Coffman conditions must hold simultaneously. First, Mutual Exclusion, meaning the resources cannot be shared. Second, Hold and Wait, where a process must be holding at least one resource while waiting to acquire another. Third, No Preemption, meaning resources cannot be forcibly taken from a process. And fourth, Circular Wait, where a closed loop of processes exists such that each process waits for a resource held by the next. If we can break even one of these four conditions—like imposing a global resource ordering to prevent circular wait—deadlocks can be completely prevented.",
            "keywords": ["Coffman Conditions", "Mutual Exclusion", "Hold & Wait", "Circular Wait", "Resource Ordering"],
            "followups": "Differentiate deadlock prevention vs avoidance. How does Banker's algorithm work?",
            "mistake": "Confusing deadlock prevention with deadlock detection. Prevention prevents the state, detection resolves it after it occurs.",
            "depth": "Detail the Banker's algorithm safety check time complexity and its practical limitations in modern OS."
        },
        {
            "q": "Differentiate Paging from Segmentation. How do they handle memory fragmentation differently?",
            "a": "Paging is a memory management scheme where virtual memory and physical memory are divided into fixed-size blocks called pages and frames. It completely eliminates external fragmentation because any free physical frame can be allocated to any process page, though it can cause minor internal fragmentation in the very last page of a process. Segmentation is a programmer-centric scheme where memory is divided into variable-sized logical segments, like code, stack, or heap. Because segment sizes vary, loading and unloading them leaves variable-sized holes in physical memory, which leads to external fragmentation over time. Modern systems often use a hybrid called paged segmentation to get the logical benefits of segments while using paging internally to prevent external fragmentation.",
            "keywords": ["Fixed-Size Pages", "Variable-Size Segments", "Internal Fragmentation", "External Fragmentation", "Paged Segmentation"],
            "followups": "What is the purpose of TLB? What is Belady's Anomaly?",
            "mistake": "Saying paging causes external fragmentation. Paging ONLY causes internal fragmentation.",
            "depth": "Explain multi-level page table lookups and how TLB reduces memory reference overhead."
        }
    ]
    
    p1_html = f"""
  <div class="page" id="os-expectedqa-new-1">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="header-badge" style="background: rgba(255,255,255,0.25);">EXPECTED Q&amp;A</div>
      </div>
    </div>
    
    <div style="padding: 20px 24px; flex: 1; display: flex; flex-direction: column; overflow: hidden;">
      <div style="text-align: center; margin-bottom: 10px;">
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">Top Expected Interview Questions</div>
        <div style="font-size: 9pt; color: #EA763F; font-weight: 700; margin-top: 2px;">Placement Q&amp;As · Created by Pranav Gawai (Part 1)</div>
      </div>
      
      <div style="display: flex; flex-direction: column; gap: 8px;">
        {render_qa_block(qas[0])}
        {render_qa_block(qas[1])}
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> OS <span>›</span> <span>Expected Q&amp;A</span></div>
      </div>
      <div class="page-number-premium">PAGE 31 / 35</div>
    </div>
  </div>
  """
  
    p2_html = f"""
  <div class="page" id="os-expectedqa-new-2">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="header-badge" style="background: rgba(255,255,255,0.25);">EXPECTED Q&amp;A</div>
      </div>
    </div>
    
    <div style="padding: 20px 24px; flex: 1; display: flex; flex-direction: column; overflow: hidden;">
      <div style="text-align: center; margin-bottom: 10px;">
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">Top Expected Interview Questions</div>
        <div style="font-size: 9pt; color: #EA763F; font-weight: 700; margin-top: 2px;">Placement Q&amp;As · Created by Pranav Gawai (Part 2)</div>
      </div>
      
      <div style="display: flex; flex-direction: column; gap: 8px;">
        {render_qa_block(qas[2])}
        {render_qa_block(qas[3])}
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> OS <span>›</span> <span>Expected Q&amp;A</span></div>
      </div>
      <div class="page-number-premium">PAGE 32 / 35</div>
    </div>
  </div>
  """
    return p1_html + p2_html

def render_qa_block(item):
    kw_tags = "".join([f'<span style="background: #F7FAFC; border: 1px solid #CBD5E0; padding: 1px 6px; border-radius: 4px; font-weight: bold; font-size: 7pt; color: #4A5568; text-transform: uppercase;">{kw}</span>' for kw in item['keywords']])
    return f"""
    <div style="border: 1px solid #CBD5E0; border-radius: 8px; padding: 10px 12px; background: white; display: flex; flex-direction: column; gap: 4px;">
      <div style="font-weight: 800; font-size: 9pt; color: #2B6CB0;">Q: {item['q']}</div>
      <div style="font-size: 8pt; color: #2D3748; line-height: 1.4; border-left: 3px solid #EA763F; padding-left: 8px; margin-bottom: 2px;">
        "{item['a']}"
      </div>
      <div style="display: flex; flex-wrap: wrap; gap: 4px; align-items: center; margin-top: 2px;">
        <span style="font-size: 7.5pt; font-weight: 800; color: #EA763F; text-transform: uppercase; margin-right: 4px;">Keywords:</span>
        {kw_tags}
      </div>
      <div style="font-size: 7.5pt; color: #4A5568; margin-top: 2px;">
        <strong>🔄 Follow-Up:</strong> {item['followups']}
      </div>
      <div style="font-size: 7.5pt; color: #C53030;">
        <strong>⚠️ Common Mistake:</strong> {item['mistake']}
      </div>
      <div style="font-size: 7.5pt; color: #276749;">
        <strong>📈 Expected Depth:</strong> {item['depth']}
      </div>
    </div>
"""

# ─────────────────────────────────────────
# RAPID FIRE QUESTIONS PAGE (Page 33)
# ─────────────────────────────────────────
def generate_rapid_fire_page(LOGO_BASE64):
    qas = [
        ("What is a PCB?", "Process Control Block; a kernel data structure storing process state."),
        ("What is the PID of the init process?", "PID 1, which adopts orphan processes."),
        ("What is Belady's Anomaly?", "FIFO page replacement causing more page faults as frame counts increase."),
        ("Name a scheduling algorithm that prevents starvation.", "Round Robin (time-sliced scheduling)."),
        ("What is a translation lookaside buffer?", "TLB is a fast hardware cache for virtual-to-physical address translations."),
        ("Difference between user mode and kernel mode?", "User mode is restricted; kernel mode has full hardware access."),
        ("What system call is used to create a process in Unix?", "`fork()` (duplicates the parent process)."),
        ("What is a spinlock?", "A lock where threads poll in a loop (busy-wait) until the lock is available."),
        ("What is thrashing?", "The system spends more time swapping pages in/out of disk than executing work."),
        ("What is Peterson's solution?", "A software-based algorithm that solves the critical section problem for two processes."),
        ("What is the Banker's algorithm used for?", "Deadlock avoidance by checking if resource allocation keeps the system in a safe state."),
        ("What is an inode?", "Index node; a filesystem structure storing file metadata, size, permissions, and block pointers.")
    ]
    
    left_col_cards = "".join([render_rapid_card(q, a) for q, a in qas[:6]])
    right_col_cards = "".join([render_rapid_card(q, a) for q, a in qas[6:]])
    
    return f"""
  <div class="page" id="os-rapidfire-page">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="badge-yield" style="background:#FFF5F0; color:#EA763F;">⚡ RAPID FIRE</div>
        <div class="header-badge">Placement Recall</div>
      </div>
    </div>
    
    <div style="padding: 20px 24px; display: flex; flex-direction: column; gap: 10px; flex: 1; overflow: hidden;">
      <div style="text-align: center; margin-bottom: 4px;">
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">OS Rapid Fire Questions</div>
        <div style="font-size: 9pt; color: #EA763F; font-weight: 700;">Fast-Recall Flashcards for Last-Minute Self-Testing</div>
      </div>
      
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; flex: 1;">
        <div style="display: flex; flex-direction: column; gap: 8px;">
          {left_col_cards}
        </div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
          {right_col_cards}
        </div>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> OS <span>›</span> <span>Rapid Fire</span></div>
      </div>
      <div class="page-number-premium">PAGE 33 / 36</div>
    </div>
  </div>
"""

def render_rapid_card(q, a):
    return f"""
    <div style="border: 1px solid #E2E8F0; border-radius: 6px; padding: 6px 8px; background: white;">
      <div style="font-weight: 800; font-size: 8pt; color: #EA763F; margin-bottom: 2px;">Q: {q}</div>
      <div style="font-size: 7.5pt; color: #4A5568; line-height: 1.3;">A: {a}</div>
    </div>
"""

# ─────────────────────────────────────────
# COMMON TRAPS PAGE (Page 34)
# ─────────────────────────────────────────
def generate_common_traps_page(LOGO_BASE64):
    traps = [
        {
            "title": "Trap 1: The Multi-core Spinlock Illusion",
            "question": 'Why is a spinlock highly efficient on a single-core processor?',
            "intercept": "Correct the interviewer: Spinlocks are actually *terrible* on a single-core CPU. A thread waiting on a spinlock will spin in a loop, wasting the entire CPU time slice, and since there is only one core, the thread holding the lock cannot execute to release it. Spinlocks are only useful on multi-core systems where one core spins while another releases the lock."
        },
        {
            "title": "Trap 2: The Fork Heap Sharing Myth",
            "question": 'Since fork() creates a duplicate process, does it immediately copy the entire parent RAM heap?',
            "intercept": "Clarify that `fork()` uses Copy-on-Write (COW). It does not copy the RAM immediately; instead, it duplicates the page table pointers, marking them read-only. Both parent and child share the same physical memory until one of them writes, at which point a page fault occurs and a duplicate frame is created."
        },
        {
            "title": "Trap 3: The Starvation-Free CPU Scheduler",
            "question": 'Does Shortest Job First (SJF) guarantee that no process will starve?',
            "intercept": "State that SJF actually has a *high* risk of starvation for long processes. If a steady stream of short processes enters the queue, a long process will wait indefinitely. To prevent starvation, we must implement aging to increase process priority over time."
        },
        {
            "title": "Trap 4: The TLB Miss Page Table Flush",
            "question": 'When a TLB miss occurs, does the OS kernel immediately flush the entire TLB?',
            "intercept": "Explain that a TLB miss simply means the address translation isn't in cache. The CPU performs a page table walk to find it, caches it in the TLB, and resumes. Flushes only happen during a context switch to a different process (unless ASIDs are used) or when page tables are modified."
        },
        {
            "title": "Trap 5: The Thread Crash Isolation",
            "question": 'If a thread crashes due to a segmentation fault, does the rest of the process continue running?',
            "intercept": "No. Since threads share the same address space, a segmentation fault signals the OS that memory corruption has occurred. The OS sends a SIGSEGV signal to the entire process, terminating all of its sibling threads immediately. Threads lack fault isolation."
        }
    ]
    
    rows = ""
    for item in traps:
        rows += f"""
        <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 8px 10px; background: white; margin-bottom: 6px;">
          <div style="font-weight: 800; font-size: 8.5pt; color: #C53030; margin-bottom: 2px;">{item['title']}</div>
          <div style="font-size: 7.5pt; font-style: italic; color: #4A5568; margin-bottom: 4px;">Interviewer: "{item['question']}"</div>
          <div style="font-size: 7.5pt; color: #2D3748; line-height: 1.35; border-left: 2px solid #E53E3E; padding-left: 6px;">
            <strong>Deflection:</strong> {item['intercept']}
          </div>
        </div>
        """
        
    return f"""
  <div class="page" id="os-commontraps-page">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="badge-yield" style="background:#FFF5F5; color:#E53E3E;">🛑 INTERVIEW TRAPS</div>
        <div class="header-badge">Placement Tactics</div>
      </div>
    </div>
    
    <div style="padding: 20px 24px; display: flex; flex-direction: column; gap: 10px; flex: 1; overflow: hidden;">
      <div style="text-align: center; margin-bottom: 4px;">
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">OS Common Traps &amp; Deflections</div>
        <div style="font-size: 9pt; color: #E53E3E; font-weight: 700;">Tactical Responses to Deflect Tricky Placement Questions</div>
      </div>
      
      <div style="flex: 1; display: flex; flex-direction: column; justify-content: center;">
        {rows}
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> OS <span>›</span> <span>Common Traps</span></div>
      </div>
      <div class="page-number-premium">PAGE 34 / 35</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# BLANK NOTES PAGES (2 Pages)
# ─────────────────────────────────────────
blank_notes_pages = f"""
  <div class="page" id="os-notes-1">
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
      <div style="font-size: 16pt; font-weight: 800; color: #111; border-bottom: 2px solid #EA763F; padding-bottom: 6px; margin-bottom: 12px;">Personal Notes &amp; Scribbles</div>
      <div class="notes-lines" style="flex: 1; background-image: linear-gradient(#E2E8F0 1px, transparent 1px); background-size: 100% 24px; line-height: 24px; margin-top: 10px;"></div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> OS <span>›</span> <span>Notes</span></div>
      </div>
      <div class="page-number-premium">PAGE 35 / 35</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# COMPILING HTML PAGES
# ─────────────────────────────────────────
total_content_pages = len(topics)
content_pages_html = "".join([generate_page(t, i+4, 35) for i, t in enumerate(topics)])
comparison_cheat_sheet_html = generate_comparison_cheat_sheet(LOGO_BASE64)
expected_qa_html = generate_expected_qa_pages_new(LOGO_BASE64)
rapid_fire_html = generate_rapid_fire_page(LOGO_BASE64)
common_traps_html = generate_common_traps_page(LOGO_BASE64)

# ─────────────────────────────────────────
# CSS DESIGN SYSTEMS
# ─────────────────────────────────────────
css = f"""
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
  @page {{ size: A4 portrait; margin: 0; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ font-family: 'DM Sans', sans-serif; background: #E5E7EB; color: #333; }}
  
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
  .cover-title {{ font-size: 42pt; font-weight: 800; color: #111; line-height: 1.1; margin-bottom: 30px; letter-spacing: -1.5px; }}
  .cover-subtitle {{ font-size: 18pt; color: #666; font-weight: 600; margin-bottom: 60px; }}
  .cover-footer {{ position: absolute; bottom: 60px; font-size: 12pt; font-weight: 800; color: #888; letter-spacing: 1px; display: flex; align-items: center; gap: 12px; }}
  .cover-footer img {{ height: 24px; }}
  .cover-footer a {{ text-decoration: none; color: inherit; }}

  /* TOC PAGE */
  .toc-page {{ justify-content: flex-start; }}
  .toc-inner {{ padding: 30px 40px; width: 100%; }}

  /* HEADER */
  .header {{ background: #EA763F; height: 14mm; display: flex; justify-content: space-between; align-items: center; padding: 0 24px; color: white; flex-shrink: 0; margin-top: 5mm; margin-left: 5mm; margin-right: 5mm; }}
  .header-left {{ display: flex; align-items: center; gap: 12px; }}
  .header-logo {{ height: 8mm; filter: brightness(0) invert(1); }}
  .header-wordmark {{ font-size: 16pt; font-weight: 800; letter-spacing: -0.5px; }}
  .header-right {{ display: flex; align-items: center; gap: 8px; }}
  .badge-yield {{ background: #FFF; color: #E53E3E; padding: 4px 10px; border-radius: 20px; font-weight: 800; font-size: 8.5pt; display: flex; align-items: center; gap: 4px; }}
  .header-badge {{ background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 4px; font-weight: 700; font-size: 10pt; }}

  /* TOPIC BAR */
  .topic-bar {{ padding: 14px 24px; border-bottom: 2px solid #EBE5DB; background: white; flex-shrink: 0; margin-left: 5mm; margin-right: 5mm; }}
  .topic-bar-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }}
  .topic-eyebrow {{ font-size: 9pt; color: #EA763F; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px; }}
  .yield-rating {{ font-size: 9pt; font-weight: 800; color: #4A5568; }}
  .stars-gold {{ color: #D69E2E; font-size: 10pt; letter-spacing: 1px; }}
  .topic-title {{ font-size: 19pt; font-weight: 800; color: #111; margin-bottom: 2px; letter-spacing: -0.5px; }}
  .topic-subtitle {{ font-size: 9.5pt; color: #666; font-weight: 600; line-height: 1.3; }}

  /* BODY COLUMNS */
  .body-container {{ display: flex; flex: 1; overflow: hidden; margin-left: 5mm; margin-right: 5mm; }}
  .col-left {{ width: 50%; background: #FEF8F4; padding: 12px 16px; border-right: 1px solid #F0E6DD; overflow: hidden; display: flex; flex-direction: column; gap: 10px; }}
  .col-right {{ width: 50%; background: #FFFFFF; padding: 12px 16px; display: flex; flex-direction: column; gap: 10px; overflow: hidden; }}
  
  /* BOXES */
  .box {{ border-radius: 8px; padding: 10px 12px; font-size: 8.5pt; line-height: 1.45; }}
  .box-title {{ font-size: 8pt; font-weight: 800; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.8px; display: flex; align-items: center; gap: 6px; }}
  .box-theory {{ border-left: 4px solid #EA763F; background: #FFF5F0; }}
  .box-theory .box-title {{ color: #EA763F; }}
  .box-industry {{ background: #FDF6E3; border: 1px solid #F5E6B3; }}
  .box-industry .box-title {{ color: #B7791F; }}
  .box-question {{ background: #EBF2F9; border: 1px solid #C5D9ED; }}
  .box-question .box-title {{ color: #2B6CB0; }}
  .box-question p {{ font-weight: 700; color: #1A365D; font-size: 9.5pt; line-height: 1.35; }}
  .box-buzzwords {{ background: #FDF2F8; border: 1px dashed #FCC2D7; }}
  .box-buzzwords .box-title {{ color: #D53F8C; margin-bottom: 4px; }}
  .buzzword-tags {{ display: flex; gap: 4px; flex-wrap: wrap; }}
  .buzz-tag {{ background: white; border: 1px solid #FCC2D7; color: #B83280; padding: 3px 6px; border-radius: 4px; font-weight: 800; font-size: 7pt; text-transform: uppercase; letter-spacing: 0.5px; }}
  .box-answer {{ background: #FFFFFF; border: 1px solid #E2E8F0; box-shadow: 0 4px 10px rgba(0,0,0,0.03); }}
  .box-answer .box-title {{ color: #4A5568; }}
  
  /* NEW PLACEMENT BOOSTER BOXES */
  .box-say {{ border-left: 4px solid #38A169; background: #F0FFF4; }}
  .box-say .box-title {{ color: #38A169; }}
  .box-mistake {{ border-left: 4px solid #E53E3E; background: #FFF5F5; }}
  .box-mistake .box-title {{ color: #E53E3E; }}
  .box-depth {{ border-left: 4px solid #3182CE; background: #EBF8FF; }}
  .box-depth .box-title {{ color: #3182CE; }}
  
  /* FOLLOW-UP SUBSECTION */
  .followup-box {{ background: #F5EBFE; border: 1px solid #E9D8FD; }}
  .followup-title {{ color: #6B46C1; }}
  .followup-q {{ font-weight: 800; color: #44337A; font-size: 8.5pt; margin-bottom: 2px; }}
  .followup-q::before {{ content: "→ "; color: #805AD5; }}
  .followup-a {{ color: #553C9A; font-size: 8pt; line-height: 1.35; }}

  /* CONCEPT DIAGRAMS */
  .concept-visual {{ background: white; border-radius: 8px; padding: 10px; border: 1px solid #EBE5DB; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
  .visual-table {{ width: 100%; border-collapse: collapse; font-size: 7.5pt; text-align: center; }}
  .visual-table th {{ background: #EDF2F7; color: #4A5568; padding: 4px; border-bottom: 1.5px solid #CBD5E0; font-weight: 800; }}
  .visual-table td {{ padding: 4px; border-bottom: 1px solid #E2E8F0; }}
  
  .row-app {{ background: #FFF5F5; font-weight: bold; color: #C53030; }}
  .row-trans {{ background: #FFFFF0; font-weight: bold; color: #B7791F; }}
  .row-net {{ background: #EBF8FF; font-weight: bold; color: #2B6CB0; }}
  .row-link {{ background: #F0FFF4; font-weight: bold; color: #276749; }}
  .row-phy {{ background: #F7FAFC; font-weight: bold; color: #4A5568; }}
  
  .contrast-table td {{ font-weight: bold; }}
  .contrast-table tr:nth-child(even) {{ background: #F7FAFC; }}
  
  .flow-container {{ display: flex; flex-direction: column; width: 100%; align-items: center; justify-content: center; gap: 2px; }}
  .flow-block {{ width: 90%; text-align: center; padding: 6px; border-radius: 6px; font-size: 8pt; font-weight: 800; border: 1.5px solid; }}
  .block-orange {{ background: #FFF5F0; border-color: #EA763F; color: #EA763F; }}
  .block-blue {{ background: #EBF8FF; border-color: #3182CE; color: #3182CE; }}
  .block-green {{ background: #F0FFF4; border-color: #38A169; color: #38A169; }}
  .block-grey {{ background: #F7FAFC; border-color: #CBD5E0; color: #4A5568; }}
  .flow-arrow {{ font-size: 7pt; font-weight: bold; color: #A0AEC0; margin: 1px 0; }}
  
  .diagram-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; width: 100%; }}
  .grid-item {{ border: 1px solid #E2E8F0; padding: 6px; border-radius: 6px; font-size: 8pt; text-align: center; background: white; }}

  /* NOTES LINES FOR BLANK PAGES */
  .notes-lines {{
    flex: 1;
    background-image: linear-gradient(#E2E8F0 1px, transparent 1px);
    background-size: 100% 24px;
    margin-top: 10px;
  }}

  /* FOOTER WITH PREMIUM PAGE NUMBERS */
  .footer {{ height: 36px; background: white; border-top: 1px solid #EDE5D8; display: flex; justify-content: space-between; align-items: center; padding: 0 24px; font-size: 8.5pt; color: #718096; flex-shrink: 0; font-weight: 700; margin-bottom: 5mm; margin-left: 5mm; margin-right: 5mm; }}
  .footer-left {{ display: flex; align-items: center; gap: 8px; }}
  .footer-logo {{ height: 14px; }}
  .breadcrumb {{ color: #A0AEC0; }}
  .breadcrumb span {{ color: #4A5568; font-weight: 800; margin: 0 4px; }}
  .page-number-premium {{ font-size: 8.5pt; font-weight: 800; color: #EA763F; letter-spacing: 1px; background: #FFF5F0; padding: 3px 10px; border-radius: 4px; border: 1px solid #FBD38D; }}

  /* BOTTOM PLACEMENT GRID (L4) */
  .bottom-placement-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 8px;
    padding: 10px 16px;
    background: #FDFBF7;
    border-top: 2px solid #EBE5DB;
    flex-shrink: 0;
    min-height: 140px;
    max-height: 155px;
    margin-left: 5mm;
    margin-right: 5mm;
  }}
  .placement-block {{
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 8pt;
    line-height: 1.3;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .placement-block-title {{
    font-size: 7.5pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 2px;
    display: flex;
    align-items: center;
    gap: 4px;
  }}
  .block-mistake {{ background: #FFF5F5; border-left: 3px solid #E53E3E; color: #742A2A; }}
  .block-mistake .placement-block-title {{ color: #C53030; }}
  .block-trap {{ background: #FFF5F0; border-left: 3px solid #EA763F; color: #7B341E; }}
  .block-trap .placement-block-title {{ color: #DD6B20; }}
  .block-followups {{ background: #F5EBFE; border-left: 3px solid #805AD5; color: #553C9A; }}
  .block-followups .placement-block-title {{ color: #6B46C1; }}
  .block-trick {{ background: #F0FFF4; border-left: 3px solid #38A169; color: #276749; }}
  .block-trick .placement-block-title {{ color: #2F855A; }}
"""

# Compile final template
html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>OS Placement Handbook</title>
<style>{css}</style>
</head>
<body>
  <!-- COVER PAGE -->
  <div class="page cover-page" id="os-cover">
    <div class="cover-logo-container">
      <img src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS">
    </div>
    <div class="cover-eyebrow">Core Computer Science</div>
    <div class="cover-title">Operating<br>Systems</div>
    <div class="cover-subtitle">Placement Preparation Notes</div>
    <div style="font-size: 11pt; color: #718096; font-weight: 700; margin-top: -30px; margin-bottom: 50px;">Created by Pranav Gawai</div>
    <div class="cover-footer">
      <img src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
      <a href="https://grindos.pranavx.in">grindos.pranavx.in</a>
    </div>
  </div>

  <!-- ROADMAP PAGE -->
  {roadmap_page}

  <!-- TOC PAGE -->
  {toc_page}

  <!-- CONTENT PAGES -->
  {content_pages_html}

  <!-- FINAL REVISION SHEET -->
  {final_revision_page}

  <!-- COMPARISON CHEAT SHEET -->
  {comparison_cheat_sheet_html}

  <!-- EXPECTED Q&A PAGES -->
  {expected_qa_html}

  <!-- RAPID FIRE PAGE -->
  {rapid_fire_html}

  <!-- COMMON TRAPS PAGE -->
  {common_traps_html}

  <!-- BLANK NOTES PAGES -->
  {blank_notes_pages}
</body>
</html>
"""

# Write to file
os.makedirs("subjects/os", exist_ok=True)
output_path = "subjects/os/01_os_notes.html"
with open(output_path, "w") as f:
    f.write(html_out)

print(f"Generated complete Operating Systems Handbook with {len(topics)} topics.")
