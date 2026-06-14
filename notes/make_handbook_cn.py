import base64
import os

# Load logo
with open("../logo.png", "rb") as img_file:
    LOGO_BASE64 = base64.b64encode(img_file.read()).decode('utf-8')

# ─────────────────────────────────────────
# 24 COMPUTER NETWORKS INTERVIEW TOPICS
# ─────────────────────────────────────────
topics = [
    {
        "id": "sub-osi",
        "num": "01",
        "chapter": "Network Architecture & Models",
        "title": "The OSI Reference Model",
        "subtitle": "The 7-layer theoretical framework for network communication.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Definition &amp; Key Concepts</div>
  <p>Standardizes network communication into 7 logical layers. Separates concerns: software/user space (L5-7) vs transport/routing (L3-4) vs hardware/cables (L1-2).</p>
</div>
<div class="concept-visual">
  <table class="visual-table">
    <thead>
      <tr>
        <th>L#</th>
        <th>Layer Name</th>
        <th>PDU</th>
        <th>Devices / Protocols</th>
      </tr>
    </thead>
    <tbody>
      <tr class="row-app"><td>7</td><td>Application</td><td>Data</td><td>HTTP, DNS, SMTP</td></tr>
      <tr class="row-app"><td>6</td><td>Presentation</td><td>Data</td><td>SSL/TLS, ASCII, JPEG</td></tr>
      <tr class="row-app"><td>5</td><td>Session</td><td>Data</td><td>Sockets, RPC, NetBIOS</td></tr>
      <tr class="row-trans"><td>4</td><td>Transport</td><td>Segment</td><td>TCP, UDP, Ports</td></tr>
      <tr class="row-net"><td>3</td><td>Network</td><td>Packet</td><td>IP, ICMP, Routers</td></tr>
      <tr class="row-link"><td>2</td><td>Data Link</td><td>Frame</td><td>Ethernet, MAC, Switches</td></tr>
      <tr class="row-phy"><td>1</td><td>Physical</td><td>Bit</td><td>Cables, Hubs, Repeaters</td></tr>
    </tbody>
  </table>
</div>
<div class="box box-industry">
  <div class="box-title">Real-World Troubleshooting Use-Case</div>
  <p>Used to isolate bugs bottom-up. If a client can't fetch data: test L1 (cable/WiFi status) → L3 (ping server IP) → L4 (telnet to port) → L7 (verify HTTP payload response).</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"At which layer does a Router operate, and how does it differ from a Layer 2 Switch?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Logical Addressing</span>
    <span class="buzz-tag">MAC Forwarding</span>
    <span class="buzz-tag">Layer 3 Packet</span>
    <span class="buzz-tag">Layer 2 Frame</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A Router operates at Layer 3 (Network). It reads IP packets and forwards them between different subnets using routing tables. A Switch operates at Layer 2 (Data Link) and forwards Ethernet frames within the same local network using MAC address tables."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a Layer 3 Switch?"</p>
  <p class="followup-a">A hardware-optimized switch capable of routing IP packets at wire speed between VLANs, combining routing tables with MAC learning.</p>
</div>
""",
        "trap": "Saying that the OSI model is actively used on the internet. It is strictly a theoretical reference model; the internet runs on the TCP/IP model.",
        "trick": "Please Do Not Throw Sausage Pizza Away (Physical, Data Link, Network, Transport, Session, Presentation, Application)"
    },
    {
        "id": "sub-tcpip",
        "num": "02",
        "chapter": "Network Architecture & Models",
        "title": "TCP/IP Model Suite",
        "subtitle": "The practical 4-layer architecture powering the Internet.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Practical Layer Consolidation</div>
  <p>The Transmission Control Protocol/Internet Protocol suite collapses the 7 theoretical OSI layers into 4 highly functional layers optimized for real implementation.</p>
</div>
<div class="concept-visual">
  <div class="flow-container">
    <div class="flow-block block-orange">Application (OSI 5,6,7)<br><span class="desc">HTTP, DNS, SSH</span></div>
    <div class="flow-arrow">↓↑ Port Addressing</div>
    <div class="flow-block block-blue">Transport (OSI 4)<br><span class="desc">TCP, UDP</span></div>
    <div class="flow-arrow">↓↑ Logical Routing</div>
    <div class="flow-block block-green">Internet (OSI 3)<br><span class="desc">IP, ICMP</span></div>
    <div class="flow-arrow">↓↑ Physical Delivery</div>
    <div class="flow-block block-grey">Network Access (OSI 1,2)<br><span class="desc">Ethernet, Wi-Fi</span></div>
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">Why TCP/IP Won Over OSI</div>
  <p>OSI was designed by standard committees before protocols were fully written. TCP/IP was built by practitioners (DARPA) who implemented software first. Practice beat theory.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How does the TCP/IP Model handle data delivery differently from OSI?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Internet Layer</span>
    <span class="buzz-tag">Concise Layers</span>
    <span class="buzz-tag">Horizontal Routing</span>
    <span class="buzz-tag">End-to-End Reliability</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"TCP/IP combines the Application, Presentation, and Session layers into a single Application layer, leaving data formatting and session state to the application itself. The Internet layer represents the Network layer, ensuring global routing via IP protocols."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"Which layer handles encryption in TCP/IP?"</p>
  <p class="followup-a">Typically the Application layer (e.g., TLS handles encryption for HTTPS before data reaches TCP transport layer).</p>
</div>
""",
        "trap": "Don't confuse the TCP/IP Internet Layer name with the OSI Network Layer name, though they do the exact same job.",
        "trick": "TCP/IP is OSI in a tight corset — squeezed from 7 layers down to a highly practical 4."
    },
    {
        "id": "sub-tcp-udp",
        "num": "03",
        "chapter": "Transport Layer Protocols",
        "title": "TCP vs UDP",
        "subtitle": "Reliability and ordering vs raw speed and low overhead.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Core protocol trade-offs</div>
  <p><strong>TCP:</strong> Connection-oriented, guaranteed in-order delivery, flow control, congestion control. Slower due to handshakes and headers.</p>
  <p><strong>UDP:</strong> Connectionless, unconfirmed delivery, fast, thin header (8 bytes vs 20 bytes). Broadcast/multicast support.</p>
</div>
<div class="concept-visual">
  <table class="visual-table contrast-table">
    <thead>
      <tr>
        <th>Feature</th>
        <th>TCP</th>
        <th>UDP</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>State</td><td>Stateful</td><td>Stateless</td></tr>
      <tr><td>Header</td><td>20-60 bytes</td><td>8 bytes</td></tr>
      <tr><td>Delivery</td><td>Guaranteed</td><td>Best-effort</td></tr>
      <tr><td>Flow Control</td><td>Yes (Sliding Window)</td><td>No</td></tr>
      <tr><td>Use-case</td><td>HTTP, SSH, Email</td><td>DNS, VoIP, Gaming</td></tr>
    </tbody>
  </table>
</div>
<div class="box box-industry">
  <div class="box-title">Real-World API Design Decision</div>
  <p>Zoom uses UDP for live audio/video frames (speed matters; dropped frames are skipped) but uses TCP for chat messages and authentication (no loss tolerated).</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why does UDP have a checksum if it is called an 'unreliable' protocol?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Data Integrity</span>
    <span class="buzz-tag">Silent Corruption</span>
    <span class="buzz-tag">Error Detection</span>
    <span class="buzz-tag">No Retransmission</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"UDP provides error detection but NOT error correction. The UDP checksum identifies if bits were corrupted in transit. If corrupt, the packet is discarded. It is 'unreliable' because it won't ask for a retransmission, but it won't deliver bad data."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is HTTP/3's connection model?"</p>
  <p class="followup-a">HTTP/3 runs over QUIC, which uses UDP to eliminate Head-of-Line blocking while implementing custom reliability and congestion control in user space.</p>
</div>
""",
        "trap": "Never say UDP is 'bad' or 'insecure' just because it's unreliable. UDP is the default choice for high-frequency, low-latency applications.",
        "trick": "TCP is a certified mail delivery with signature receipt. UDP is throwing a newspaper at a moving target."
    },
    {
        "id": "sub-ip-addressing",
        "num": "04",
        "chapter": "Network Layer Addressing",
        "title": "IP Addressing (IPv4 vs IPv6)",
        "subtitle": "Logical identification systems for global internet routing.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Format & Composition</div>
  <p><strong>IPv4:</strong> 32-bit address, dotted-decimal format (e.g., 192.168.1.1). Total address space ~4.3 billion (exhausted).</p>
  <p><strong>IPv6:</strong> 128-bit address, hexadecimal colon format (e.g., 2001:db8::ff00:42). Total space ~3.4×10^38. Built-in IPSec.</p>
</div>
<div class="concept-visual">
  <div class="diagram-grid">
    <div class="grid-item">
      <strong>IPv4 Address Structure</strong>
      <div style="font-family:monospace; margin-top:4px; font-size:7.5pt; color:#2B6CB0; background:#EBF2F9; padding:4px;">
        192.168.1.1 (4 Octets)<br>
        [Network Part] [Host Part]
      </div>
    </div>
    <div class="grid-item">
      <strong>IPv6 Address Structure</strong>
      <div style="font-family:monospace; margin-top:4px; font-size:7.5pt; color:#276749; background:#F0FFF4; padding:4px;">
        2001:0db8::8a2e:0370:7334<br>
        (8 groups of 16-bit hex values)
      </div>
    </div>
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">Loopback Addresses</div>
  <p>IPv4 uses <code>127.0.0.1</code> for loopback (localhost). IPv6 uses <code>::1</code>. Loopback traffic never leaves the local network interface card (NIC).</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What was the primary driver for IPv6, and what does it change other than address length?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Address Exhaustion</span>
    <span class="buzz-tag">Simplified Header</span>
    <span class="buzz-tag">No Broadcasts</span>
    <span class="buzz-tag">Autoconfiguration</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"IPv6 was created to solve IPv4 address exhaustion. Key architectural upgrades include: a fixed-size simplified header for faster router processing, native SLAAC (Stateless Address Autoconfiguration), replacing Broadcasts with Multicasts, and removing IP-level checksums."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"Why are broadcasts removed in IPv6?"</p>
  <p class="followup-a">Broadcasts force all devices on a local subnet to process the packet. IPv6 replaces broadcasts with targeted multicast groups to save device CPU cycles.</p>
</div>
""",
        "trap": "Don't confuse Classful Routing (A, B, C) with classless CIDR routing. Classful routing has been obsolete since 1993.",
        "trick": "IPv4 = 4 bytes (32-bit). IPv6 = 16 bytes (128-bit). Address space is large enough to assign an IP to every atom on Earth."
    },
    {
        "id": "sub-subnetting",
        "num": "05",
        "chapter": "Network Layer Addressing",
        "title": "Subnetting & CIDR",
        "subtitle": "Dividing single address spaces into multiple logical subnets.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Key Equations & Masks</div>
  <p>CIDR notation dictates the network prefix bits (e.g. <code>/24</code> has 24 network bits, 8 host bits). Host bits determine IPs.</p>
  <p style="margin-top:6px; font-weight:800; font-size:8.5pt;">Usable Hosts Formula: 2^(32 - CIDR) - 2</p>
</div>
<div class="concept-visual">
  <table class="visual-table subnet-table">
    <thead>
      <tr>
        <th>CIDR</th>
        <th>Subnet Mask</th>
        <th>Total IPs</th>
        <th>Usable Hosts</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>/24</td><td>255.255.255.0</td><td>256</td><td>254</td></tr>
      <tr><td>/25</td><td>255.255.255.128</td><td>128</td><td>126</td></tr>
      <tr><td>/26</td><td>255.255.255.192</td><td>64</td><td>62</td></tr>
      <tr><td>/27</td><td>255.255.255.224</td><td>32</td><td>30</td></tr>
      <tr><td>/30</td><td>255.255.255.252</td><td>4</td><td>2 (P2P WAN)</td></tr>
    </tbody>
  </table>
</div>
<div class="box box-industry">
  <div class="box-title">Cloud VPC Design</div>
  <p>AWS VPCs are typically allocated a <code>/16</code> block. Subnets inside are allocated <code>/24</code> blocks, separating Web, App, and Database layers logically.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why are there exactly 2 subtracted host addresses in every subnet calculation?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Network Address</span>
    <span class="buzz-tag">Broadcast Address</span>
    <span class="buzz-tag">Host Bits All Zeroes</span>
    <span class="buzz-tag">Host Bits All Ones</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"The first address (host bits all 0s) is the Network Identifier, which routers use to route to the subnet. The last address (host bits all 1s) is the Broadcast Address for sending packets to all hosts in the subnet. Neither can be assigned to a host device."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is the subnet size of a /32 block?"</p>
  <p class="followup-a">Exactly 1 IP. Used for individual host loopbacks or routing tables targeting a single specific server.</p>
</div>
""",
        "trap": "Don't miscalculate a /30 subnet! A /30 has 4 total IPs, but only 2 are usable, making it perfect for connecting exactly two routers.",
        "trick": "h is host bits. Subtract h from 32, double it iteratively: /30 has 2 host bits, 2^2 = 4 total IPs."
    },
    {
        "id": "sub-mac-arp",
        "num": "06",
        "chapter": "Data Link Layer & Resolution",
        "title": "MAC Address & ARP",
        "subtitle": "Mapping Layer 3 IP logical addresses to Layer 2 MAC physical addresses.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Logical vs Physical Address</div>
  <p><strong>MAC (Media Access Control):</strong> 48-bit burned-in physical hardware address, unique globally (e.g., 00:0a:95:9d:68:16).</p>
  <p><strong>ARP (Address Resolution Protocol):</strong> Dynamic mapping helper protocol. Discovers the MAC address of an IP on the local subnet.</p>
</div>
<div class="concept-visual">
  <div class="flow-container">
    <div style="font-size:7.5pt; border:1px solid #CBD5E0; padding:6px; background:white; border-radius:6px; text-align:center;">
      <strong>ARP Request (Broadcast)</strong><br>
      "Who has IP 192.168.1.5? Tell MAC 00:0A..."
    </div>
    <div style="font-size:12pt; text-align:center; color:#A0AEC0; margin:2px 0;">↓</div>
    <div style="font-size:7.5pt; border:1px solid #CBD5E0; padding:6px; background:white; border-radius:6px; text-align:center;">
      <strong>ARP Reply (Unicast)</strong><br>
      "IP 192.168.1.5 is at MAC 00:0B:44..."
    </div>
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">Security Exploit: ARP Spoofing</div>
  <p>Because ARP lacks authentication, an attacker can send fake ARP replies claiming their MAC address matches the default gateway IP, executing a Man-in-the-Middle (MitM) intercept.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How does a packet's MAC address and IP address change as it travels across different routers?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">End-to-End Constant</span>
    <span class="buzz-tag">Hop-by-Hop Rewrite</span>
    <span class="buzz-tag">Source/Dest MAC</span>
    <span class="buzz-tag">Default Gateway</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"The source and destination IP addresses remain constant end-to-end (from sender to receiver). However, the source and destination MAC addresses are rewritten at every router hop as the frame is de-encapsulated and re-encapsulated for the next physical link."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is gratuitous ARP?"</p>
  <p class="followup-a">An unprompted ARP reply broadcasted by a host to update the ARP tables of all other hosts on the network (e.g., when a backup server takes over an IP).</p>
</div>
""",
        "trap": "Don't say ARP broadcasts travel across routers. ARP is local; routers block broadcasts. You can only resolve MAC addresses on your local subnet.",
        "trick": "IP tells you where the package is going globally. MAC tells you who takes it to the next physical truck."
    },
    {
        "id": "sub-dns",
        "num": "07",
        "chapter": "Application Layer Services",
        "title": "Domain Name System (DNS)",
        "subtitle": "The distributed database translating human names to IP addresses.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Hierarchical Architecture</div>
  <p>Uses a tree-structured database space. Resolves names recursively via Root, Top-Level Domain (TLD), and Authoritative servers.</p>
</div>
<div class="concept-visual">
  <div class="flow-container">
    <div style="font-size:7pt; line-height:1.2;">
      Client → <strong>Resolver</strong> (ISP/1.1.1.1) <br>
      Resolver → <strong>Root Server</strong> (".") <br>
      Resolver → <strong>TLD Server</strong> (".com") <br>
      Resolver → <strong>Authoritative Server</strong> ("google.com") <br>
      Resolver returns IP to Client.
    </div>
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">Common DNS Record Types</div>
  <p><strong>A:</strong> IPv4 address. <strong>AAAA:</strong> IPv6 address. <strong>CNAME:</strong> Canonical name (alias). <strong>MX:</strong> Mail server. <strong>TXT:</strong> Domain verification codes.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Explain the difference between Recursive and Iterative DNS queries."</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Local Resolver</span>
    <span class="buzz-tag">Authoritative Answer</span>
    <span class="buzz-tag">Root Hints</span>
    <span class="buzz-tag">DNS Caching</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A Recursive query forces the server (resolver) to do all the work and return the final IP address or an error. In an Iterative query, the DNS server returns the best referral it has (e.g., 'I don't know the IP, but ask this TLD server')."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What transport protocol does DNS use?"</p>
  <p class="followup-a">DNS queries typically use UDP Port 53 for speed. However, zone transfers or large responses >512 bytes fallback to TCP Port 53.</p>
</div>
""",
        "trap": "Don't assume DNS changes take effect instantly. TTL (Time To Live) forces resolvers to cache old records until the TTL expires.",
        "trick": "Recursive = 'Get me the answer!' Iterative = 'Give me a phone book recommendation!'"
    },
    {
        "id": "sub-dhcp",
        "num": "08",
        "chapter": "Application Layer Services",
        "title": "DHCP Protocol",
        "subtitle": "Dynamically allocating IP configurations to connecting hosts.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Dynamic Allocation</div>
  <p>Eliminates static IP configuration. Automatically leases IP address, Subnet Mask, Default Gateway, and DNS servers to client hosts.</p>
</div>
<div class="concept-visual">
  <div class="flow-container" style="font-family:monospace; font-size:7.5pt; line-height:1.3; background:#FFF5F0; padding:8px;">
    [Client] &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [DHCP Server]<br>
    ── DISCOVER (Broadcast) ──&gt;<br>
    &lt;── OFFER (Unicast/Bcast) ──<br>
    ── REQUEST (Broadcast) ───&gt;<br>
    &lt;── ACKNOWLEDGE (Unicast) ──
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">DHCP Leases</div>
  <p>IPs aren't given forever. A host requests a renew halfway through the lease time (T1 threshold, typically 50% of lease duration) via unicast.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why is the DHCP Request packet sent as a broadcast if the server already offered an IP?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">DORA Process</span>
    <span class="buzz-tag">Multiple Servers</span>
    <span class="buzz-tag">Implicit Decline</span>
    <span class="buzz-tag">Port 67 / 68</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Multiple DHCP servers can hear a DISCOVER and send an OFFER. The client broadcasts the REQUEST to notify all listening servers which offer it accepted, allowing the rejected servers to release their reserved IPs back into the pool."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is DHCP Relay?"</p>
  <p class="followup-a">A feature on a router that catches local broadcast DHCP Discover packets and forwards them as unicast packets to a DHCP server on a different network subnet.</p>
</div>
""",
        "trap": "Don't confuse APIPA (169.254.x.x link-local IP assigned when DHCP fails) with a valid DHCP lease assignment.",
        "trick": "Remember the DORA acronym: Discover, Offer, Request, Acknowledge."
    },
    {
        "id": "sub-http",
        "num": "09",
        "chapter": "Application Layer Protocols",
        "title": "HTTP Evolution",
        "subtitle": "The protocol of the web: comparative analysis from HTTP/1.1 to HTTP/3.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">History & Evolution</div>
  <p><strong>HTTP/1.1:</strong> Added persistent connections (Keep-Alive) but suffered from Head-of-Line (HoL) blocking on the TCP level.</p>
  <p><strong>HTTP/2:</strong> Multiplexed streams over a single TCP connection, binary framing, HPACK header compression, Server Push.</p>
  <p><strong>HTTP/3:</strong> Replaces TCP with QUIC (over UDP) to eliminate TCP-level HoL blocking during packet loss.</p>
</div>
<div class="concept-visual">
  <table class="visual-table">
    <thead>
      <tr>
        <th>Protocol</th>
        <th>Transport</th>
        <th>Multiplexing</th>
        <th>Header</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>HTTP/1.1</td><td>TCP</td><td>Sequential</td><td>Text</td></tr>
      <tr><td>HTTP/2</td><td>TCP</td><td>Binary Streams</td><td>HPACK</td></tr>
      <tr><td>HTTP/3</td><td>UDP (QUIC)</td><td>Independent Streams</td><td>QPACK</td></tr>
    </tbody>
  </table>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is Head-of-Line (HoL) blocking, and how does HTTP/3 solve it?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">TCP Buffer Block</span>
    <span class="buzz-tag">QUIC Streams</span>
    <span class="buzz-tag">UDP Transport</span>
    <span class="buzz-tag">Independent Delivery</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"In HTTP/2, multiple requests share one TCP connection. If a single packet containing Stream A is lost, TCP pauses the entire connection buffer, blocking Stream B and C. HTTP/3 runs over UDP-based QUIC, where each stream is tracked independently. A lost packet only stalls its specific stream."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is HTTP Server Push?"</p>
  <p class="followup-a">A feature in HTTP/2 where the server proactively sends critical resources (like CSS or JS files) to the client's cache before the client parses the HTML and asks for them.</p>
</div>
""",
        "trap": "Don't say HTTP/3 is less secure because it uses UDP. Security (TLS 1.3) is natively embedded into QUIC's transport protocol, unlike TCP where it's a layer on top.",
        "trick": "HTTP/1.1 = One road with toll gates. HTTP/2 = Multi-lane highway, but one crash blocks all lanes. HTTP/3 = Multiple independent monorails."
    },
    {
        "id": "sub-https-ssl",
        "num": "10",
        "chapter": "Application Layer Protocols",
        "title": "HTTPS & SSL/TLS Handshake",
        "subtitle": "Encrypting web traffic to prevent eavesdropping and modification.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Cryptographic Architecture</div>
  <p>HTTPS = HTTP over SSL/TLS. Uses <strong>Asymmetric Cryptography</strong> (Public/Private keys) to negotiate a temporary, shared key, then uses <strong>Symmetric Cryptography</strong> (AES) for fast session data encryption.</p>
</div>
<div class="concept-visual" style="font-size:7pt; line-height:1.25; background:#FAFAFA; border:1px solid #E2E8F0; border-radius:6px; padding:10px;">
  1. Client sends <code>ClientHello</code> (Cipher suites, random)<br>
  2. Server replies <code>ServerHello</code>, Cert, Public Key<br>
  3. Client verifies Cert with Root CA database<br>
  4. Client encrypts <code>Pre-Master Secret</code> with Server's Public Key<br>
  5. Both derive matching <code>Session Key</code> (Symmetric)
</div>
<div class="box box-industry">
  <div class="box-title">Public Key Infrastructure (PKI)</div>
  <p>Certificates are cryptographically signed by Trusted Certificate Authorities (CAs) like Let's Encrypt. Browsers ship pre-loaded with these CA public keys to verify signatures.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why does HTTPS use both Asymmetric and Symmetric encryption instead of just Asymmetric?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Computational Overhead</span>
    <span class="buzz-tag">Key Exchange</span>
    <span class="buzz-tag">AES Encryption</span>
    <span class="buzz-tag">Symmetric Session Key</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Asymmetric encryption is computationally expensive and slow for encrypting large amounts of data. HTTPS uses asymmetric encryption solely to securely exchange a symmetric session key. Once shared, fast symmetric encryption (like AES) secures the actual web traffic."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is Perfect Forward Secrecy (PFS)?"</p>
  <p class="followup-a">A feature of key-agreement protocols (like Diffie-Hellman) that ensures session keys are unique. Compromise of the server's private key does not decrypt past recorded sessions.</p>
</div>
""",
        "trap": "Don't say HTTPS encrypts the IP headers. It only encrypts the HTTP payload, parameters, headers, and cookies. Attackers can still see the destination IP address.",
        "trick": "Asymmetric = Safe box key delivery. Symmetric = The actual padlock coding used for bulk transport."
    },
    {
        "id": "sub-tcp-handshake",
        "num": "11",
        "chapter": "Transport Layer Protocols",
        "title": "TCP 3-Way Handshake",
        "subtitle": "How TCP establishes a reliable bidirectional connection.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Connection Synchronization</div>
  <p>Ensures that both client and server are ready for transmission, synchronizes sequence numbers, and allocates buffer space.</p>
</div>
<div class="concept-visual">
  <div style="position:relative; height:120px; border-left:2px solid #CBD5E0; border-right:2px solid #CBD5E0; margin:10px 20px; font-size:8pt;">
    <div style="position:absolute; top:10px; left:0; right:0; border-bottom:1px dashed #3182CE; text-align:center;">
      <span style="background:white; padding:0 4px; color:#2B6CB0; font-weight:800;">SYN (Seq=X) ──&gt;</span>
    </div>
    <div style="position:absolute; top:50px; left:0; right:0; border-bottom:1px dashed #38A169; text-align:center;">
      <span style="background:white; padding:0 4px; color:#276749; font-weight:800;">&lt;── SYN-ACK (Seq=Y, Ack=X+1)</span>
    </div>
    <div style="position:absolute; top:90px; left:0; right:0; border-bottom:1px dashed #D69E2E; text-align:center;">
      <span style="background:white; padding:0 4px; color:#B7791F; font-weight:800;">ACK (Ack=Y+1) ──&gt;</span>
    </div>
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">Vulnerability: SYN Flood Attack</div>
  <p>An attacker sends thousands of SYN packets but never sends the final ACK. The server leaves connections "half-open" (SYN_RCVD), exhausting system memory buffers.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why is the TCP handshake 3 steps instead of 2?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Bidirectional Sync</span>
    <span class="buzz-tag">Half-Open Connection</span>
    <span class="buzz-tag">Sequence Numbers</span>
    <span class="buzz-tag">Two-Way Confirmation</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A reliable connection requires both sides to verify that they can transmit AND receive data. Step 1 verifies Client-to-Server path. Step 2 verifies Server-to-Client path. Step 3 confirms to the server that the client can hear it. 2 steps would leave the server uncertain of the client's receipt."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a SYN Cookie?"</p>
  <p class="followup-a">A defense mechanism where the server doesn't allocate buffer memory immediately. It encodes session information into the SYN-ACK sequence number (cookie) and verifies it upon final ACK.</p>
</div>
""",
        "trap": "Don't forget that data CAN be sent inside the final ACK packet of the handshake, although traditional implementations wait.",
        "trick": "Handshake = 1. 'Hello?' 2. 'I hear you, do you hear me?' 3. 'Yes, I hear you!'"
    },
    {
        "id": "sub-tcp-termination",
        "num": "12",
        "chapter": "Transport Layer Protocols",
        "title": "TCP Connection Termination",
        "subtitle": "The 4-way termination handshake to gracefully close active sessions.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Half-Close State</div>
  <p>TCP connection is full-duplex. Closing the connection is done independently for each direction, hence requiring a 4-step wave.</p>
</div>
<div class="concept-visual">
  <div style="position:relative; height:120px; border-left:2px solid #CBD5E0; border-right:2px solid #CBD5E0; margin:10px 20px; font-size:7.5pt;">
    <div style="position:absolute; top:5px; left:0; right:0; border-bottom:1px dashed #C53030; text-align:center;">
      <span style="background:white; padding:0 4px; color:#C53030; font-weight:800;">FIN (Active Close) ──&gt;</span>
    </div>
    <div style="position:absolute; top:35px; left:0; right:0; border-bottom:1px dashed #4A5568; text-align:center;">
      <span style="background:white; padding:0 4px; color:#4A5568; font-weight:800;">&lt;── ACK</span>
    </div>
    <div style="position:absolute; top:65px; left:0; right:0; border-bottom:1px dashed #C53030; text-align:center;">
      <span style="background:white; padding:0 4px; color:#C53030; font-weight:800;">&lt;── FIN (Passive Close)</span>
    </div>
    <div style="position:absolute; top:95px; left:0; right:0; border-bottom:1px dashed #4A5568; text-align:center;">
      <span style="background:white; padding:0 4px; color:#4A5568; font-weight:800;">ACK ──&gt;</span>
    </div>
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">Why the TIME_WAIT state exists</div>
  <p>The host that initiates the active close enters a <code>TIME_WAIT</code> state for 2*MSL (Maximum Segment Lifetime). This ensures the final ACK arrived safely at the server and clears stray packets.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why does TCP require 4 steps to terminate a connection but only 3 steps to establish it?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Independent Close</span>
    <span class="buzz-tag">Half-Closed State</span>
    <span class="buzz-tag">Full-Duplex Channel</span>
    <span class="buzz-tag">FIN Packet</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Because TCP is full-duplex, closing one direction doesn't mean the other side is ready to stop sending. The client sends FIN. The server ACKs to close Client→Server traffic. Only when the server completes its pending transmissions will it send its own FIN. The client then ACKs to close Server→Client."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a TCP Reset (RST) packet?"</p>
  <p class="followup-a">A hard termination indicator sent when a host receives a packet for a port that isn't open, or during client-side crashes where a connection is immediately aborted without a handshake.</p>
</div>
""",
        "trap": "Don't confuse CLOSE_WAIT with TIME_WAIT. CLOSE_WAIT is a passive close state indicating the application code must release the socket resources.",
        "trick": "FIN: I am done. ACK: Got it, let me finish. FIN: I am also done. ACK: Done."
    },
    {
        "id": "sub-flow-control",
        "num": "13",
        "chapter": "Transport Layer Mechanisms",
        "title": "Flow Control",
        "subtitle": "Preventing fast senders from overwhelming slow receivers.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Receiver Buffer Management</div>
  <p>Flow control matches the sender's transmission rate to the receiver's processing capabilities. Controlled entirely by the receiver's available buffer space.</p>
</div>
<div class="concept-visual">
  <div style="border:1px solid #CBD5E0; border-radius:6px; padding:10px; background:white;">
    <div style="font-size:8pt; font-weight:800; color:#4A5568; margin-bottom:6px; text-align:center;">TCP Header: Window Size</div>
    <div style="display:flex; justify-content:space-between; align-items:center; background:#FFF5F0; padding:6px; font-family:monospace; font-size:7.5pt; border-radius:4px;">
      <span>[Sender]</span>
      <span>── Data (Seq=1, Size=1000B) ──&gt;</span>
      <span>[Receiver]</span>
    </div>
    <div style="display:flex; justify-content:space-between; align-items:center; background:#EBF8FF; padding:6px; font-family:monospace; font-size:7.5pt; border-radius:4px; margin-top:4px;">
      <span>[Sender]</span>
      <span>&lt;── ACK (Ack=1001, Win=4000B) ──</span>
      <span>[Receiver]</span>
    </div>
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">Window Starvation & Probe Segment</div>
  <p>If receiver window drops to 0, sender stops. To prevent deadlock, the sender periodically transmits 1-byte <strong>Zero Window Probes</strong> to poll if buffer has cleared.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What mechanism does TCP use to advertise receiver buffer availability dynamically?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Sliding Window</span>
    <span class="buzz-tag">Advertised Window</span>
    <span class="buzz-tag">TCP Header Field</span>
    <span class="buzz-tag">Zero Window Probe</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"TCP uses the Sliding Window protocol. The receiver advertises its available buffer space in the 16-bit Window Size field of every ACK packet. The sender calculates: Max Sent = Last Byte Acked + Advertised Window. This dynamically throttles the sender."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is the Window Scale option?"</p>
  <p class="followup-a">Since the 16-bit window field maxes out at 64KB, the TCP option 'Window Scale' multiplies this value exponentially to support high-throughput, high-latency links.</p>
</div>
""",
        "trap": "Don't confuse Flow Control (matching sender speed to receiver speed) with Congestion Control (matching sender speed to network capacity).",
        "trick": "Flow Control is the receiver saying 'Don't talk too fast, my ears are full!'"
    },
    {
        "id": "sub-sliding-window",
        "num": "14",
        "chapter": "Transport Layer Mechanisms",
        "title": "Sliding Window Protocol",
        "subtitle": "Enabling efficient continuous transmission without waiting for individual ACKs.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Pipelined Transmission</div>
  <p>Instead of Stop-and-Wait (sending one packet and blocking until it is acknowledged), the sliding window allows sending multiple unacknowledged packets to maximize throughput.</p>
</div>
<div class="concept-visual">
  <div style="font-family:monospace; font-size:8pt; border:1px solid #CBD5E0; padding:10px; background:white; text-align:center;">
    [Acked] [ <strong>Sent but Unacked</strong> | <strong>Can Send</strong> ] [Cannot Send]<br>
    Bytes: 1 2 3 [ 4 5 6 7 | 8 9 10 ] 11 12<br>
    <div style="margin-top:6px; color:#EA763F; font-weight:800;">← Window Size = 7 Bytes →</div>
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">Go-Back-N vs Selective Repeat</div>
  <p><strong>Go-Back-N (GBN):</strong> Simplistic. If packet 3 is lost, receiver discards 4 and 5, forcing sender to retransmit everything starting from packet 3.<br>
  <strong>Selective Repeat (SR):</strong> Efficient. Receiver buffers out-of-order packets (4, 5) and ACKs them; sender only retransmits lost packet 3.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How does TCP implement pipelined delivery, and what determines its window boundaries?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Cumulative ACKs</span>
    <span class="buzz-tag">Go-Back-N</span>
    <span class="buzz-tag">Out-of-order Buffer</span>
    <span class="buzz-tag">Pipelining</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"TCP implements sliding window using cumulative ACKs. The window boundaries are dictated by sequence numbers. The left boundary slides forward when the lowest unacknowledged sequence number receives an ACK, allowing new packets to fall inside the window on the right."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is Selective ACK (SACK) in TCP?"</p>
  <p class="followup-a">A TCP extension allowing receivers to explicitly advertise non-contiguous ranges of successfully received segments, enabling selective retransmissions.</p>
</div>
""",
        "trap": "Don't say TCP is strictly Go-Back-N. Standard modern TCP implementations use SACK (Selective Acknowledgment) which functions like Selective Repeat.",
        "trick": "Sliding window is like a moving frame over a conveyor belt. Only what's inside the frame can be processed."
    },
    {
        "id": "sub-congestion-control",
        "num": "15",
        "chapter": "Transport Layer Mechanisms",
        "title": "TCP Congestion Control",
        "subtitle": "Avoiding network collapse by dynamically adjusting transmission windows.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Sender-Side Network Guard</div>
  <p>Protects routing queues from overflow. Governed by <code>cwnd</code> (Congestion Window) which adjusts based on network congestion indicators.</p>
</div>
<div class="concept-visual">
  <table class="visual-table contrast-table" style="font-size:7.5pt;">
    <thead>
      <tr>
        <th>Phase</th>
        <th>Trigger / Action</th>
        <th>cwnd Behavior</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Slow Start</td><td>Initial phase</td><td>Doubles every RTT</td></tr>
      <tr><td>Congestion Avoidance</td><td>cwnd &gt; ssthresh</td><td>Increments by 1 MSS / RTT</td></tr>
      <tr><td>Fast Recovery</td><td>3 Duplicate ACKs</td><td>Halves cwnd, sets ssthresh</td></tr>
    </tbody>
  </table>
</div>
<div class="box box-industry">
  <div class="box-title">Congestion Notification (ECN)</div>
  <p>Rather than dropping packets, modern routers mark the ECN bits in the IP header of packets when buffers are full. Receivers echo this to senders to preemptively reduce rates.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Explain the difference in how TCP reacts to a Packet Timeout vs receiving 3 Duplicate ACKs."</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Severe Congestion</span>
    <span class="buzz-tag">Fast Retransmit</span>
    <span class="buzz-tag">ssthresh Halved</span>
    <span class="buzz-tag">cwnd Reset</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A Timeout indicates severe congestion; TCP resets cwnd to 1 MSS, sets ssthresh to half of current cwnd, and returns to Slow Start. 3 Duplicate ACKs trigger Fast Retransmit: TCP halving cwnd (Multiplicative Decrease) and entering Congestion Avoidance, assuming some packets are still passing."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is AIMD?"</p>
  <p class="followup-a">Additive Increase Multiplicative Decrease. TCP increases rate slowly (linear) to test capacity, but drops rate aggressively (half) if congestion is detected to ensure stability.</p>
</div>
""",
        "trap": "Don't confuse ssthresh (Slow Start Threshold) with cwnd. ssthresh marks the switchover point from exponential growth to linear growth.",
        "trick": "Timeout = Panic button (reset to 1). 3 Dup ACKs = Caution signal (cut speed in half)."
    },
    {
        "id": "sub-mac-address",
        "num": "16",
        "chapter": "Data Link Layer & Routing",
        "title": "MAC vs IP Addressing",
        "subtitle": "Physical hardware addressing vs logical network location addressing.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Key Identifiers</div>
  <p><strong>Physical MAC Address:</strong> Flat, non-hierarchical space. Assigned by manufacturer. Burned into the Network Interface Card (NIC). Relates to physical link layer.</p>
  <p><strong>Logical IP Address:</strong> Hierarchical network addressing. Assigned dynamically. Relates to logical location and routing capabilities.</p>
</div>
<div class="concept-visual" style="font-size:7.5pt; font-family:monospace; background:#FAFAFA; border:1px solid #E2E8F0; padding:10px; border-radius:6px;">
  <strong>MAC Address Structure (48-bit)</strong><br>
  [ 3 Octets OUI ] [ 3 Octets NIC serial ]<br>
  e.g., 00:1A:2B : 3C:4D:5E<br><br>
  <strong>IP Address Structure (32-bit)</strong><br>
  [ Network ID ] &nbsp;[ Host ID ]
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why do we need both MAC and IP addresses? Why can't we use MAC addresses globally?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Hierarchical Routing</span>
    <span class="buzz-tag">Global Table Size</span>
    <span class="buzz-tag">Hardware Independence</span>
    <span class="buzz-tag">Flat Namespace</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"MAC addresses belong to a flat namespace with no geographical or routing context. If we routed using MACs, every router on Earth would need a routing table entry for billions of individual devices, causing memory collapse. Logical IPs segment hosts into network blocks, enabling hierarchical routing."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"Can a MAC address be spoofed?"</p>
  <p class="followup-a">Yes. Although burned into hardware, operating systems allow software overriding of the MAC address field in outbound Ethernet headers.</p>
</div>
""",
        "trap": "Don't say that MAC addresses are used in routers. Routers strip the MAC header entirely, inspect the IP header, and append a new MAC header before egress.",
        "trick": "MAC is your SSN (fixed identifier). IP is your mailing address (changes when you move)."
    },
    {
        "id": "sub-routing",
        "num": "17",
        "chapter": "Network Layer Concepts",
        "title": "Routing vs Forwarding",
        "subtitle": "Determining network pathways vs switching packets to exit interfaces.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Plane Separation</div>
  <p><strong>Routing (Control Plane):</strong> Process of determining the end-to-end path a packet should take. Slow, calculated in software.</p>
  <p><strong>Forwarding (Data Plane):</strong> Act of transferring a packet from a router's input port to the appropriate output port. High-speed, executed in hardware.</p>
</div>
<div class="concept-visual">
  <div style="border:1px solid #CBD5E0; border-radius:6px; padding:10px; background:white; text-align:center; font-size:8.5pt;">
    <div style="background:#EBF8FF; padding:4px; font-weight:800; color:#2B6CB0; border-radius:4px;">Control Plane (Routing Table)</div>
    <div style="margin:4px 0; color:#A0AEC0;">↓ populates</div>
    <div style="background:#F0FFF4; padding:4px; font-weight:800; color:#276749; border-radius:4px;">Data Plane (Forwarding Table / FIB)</div>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How do routing tables differ from forwarding tables inside a router?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Routing Table (RIB)</span>
    <span class="buzz-tag">Forwarding Table (FIB)</span>
    <span class="buzz-tag">ASIC Hardware</span>
    <span class="buzz-tag">Next-Hop Resolution</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"The Routing Table (RIB) is a control-plane database populated by routing protocols (BGP, OSPF) containing all potential paths. The Forwarding Table (FIB) is a streamlined data-plane table loaded directly into ASIC hardware, optimized for ultra-fast next-hop lookup for active packets."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is policy-based routing?"</p>
  <p class="followup-a">A technique where routing decisions are made based on metrics beyond destination IP (such as source IP, port numbers, or protocol types).</p>
</div>
""",
        "trap": "Don't confuse the two. If an interviewer asks how a router processes packets at 100Gbps, the answer is 'Forwarding table hardware (ASIC)', not routing calculations.",
        "trick": "Routing is planning the route on a map (Control). Forwarding is turning the steering wheel at the intersection (Data)."
    },
    {
        "id": "sub-routing-protocols",
        "num": "18",
        "chapter": "Network Layer Routing",
        "title": "Routing Protocols (OSPF vs BGP)",
        "subtitle": "Interior gateway routing (IGP) vs exterior gateway routing (EGP).",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Scale & Scope</div>
  <p><strong>OSPF (Open Shortest Path First):</strong> IGP link-state protocol. Used within an Autonomous System (AS). Metric is 'Cost' (bandwidth). Fast convergence.</p>
  <p><strong>BGP (Border Gateway Protocol):</strong> EGP path-vector protocol. Used to route traffic between Autonomous Systems. Metrics are policy-based attributes.</p>
</div>
<div class="concept-visual">
  <div style="display:flex; justify-content:space-between; font-size:8pt; gap:10px;">
    <div style="flex:1; border:1px solid #3182CE; padding:6px; background:#EBF8FF; border-radius:4px; text-align:center;">
      <strong>OSPF (Link State)</strong><br>
      Dijkstra Algorithm<br>
      Metric: Cost<br>
      Updates: Multicast
    </div>
    <div style="flex:1; border:1px solid #38A169; padding:6px; background:#F0FFF4; border-radius:4px; text-align:center;">
      <strong>BGP (Path Vector)</strong><br>
      Path Vector<br>
      Metric: Policies<br>
      Updates: TCP Port 179
    </div>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why does the Internet run on BGP rather than OSPF?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Autonomous Systems</span>
    <span class="buzz-tag">Policy Routing</span>
    <span class="buzz-tag">Dijkstra Scale Limit</span>
    <span class="buzz-tag">Route Summarization</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"OSPF requires all routers to compute Dijkstra's algorithm to map the entire network topology, which is computationally impossible at internet scale. BGP connects independent Autonomous Systems (AS) and routes based on business policies and paths (AS-Path), not raw bandwidth metrics."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is the difference between iBGP and eBGP?"</p>
  <p class="followup-a">eBGP routes traffic between different Autonomous Systems. iBGP distributes those external paths to internal routers within the same Autonomous System.</p>
</div>
""",
        "trap": "Don't confuse RIP with modern routing. RIP is a distance-vector protocol limited to 15 hops; it is rarely used in modern production networks.",
        "trick": "OSPF is a turn-by-turn city GPS map. BGP is a map showing interstate highway systems between major shipping ports."
    },
    {
        "id": "sub-nat",
        "num": "19",
        "chapter": "Network Layer Services",
        "title": "Network Address Translation (NAT)",
        "subtitle": "Conserving IPv4 addresses by sharing public IPs.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Private Address Translation</div>
  <p>Private IP ranges (e.g. 192.168.x.x, 10.x.x.x) are non-routable on the internet. A NAT router translates these private addresses to a single public IP address.</p>
</div>
<div class="concept-visual">
  <div style="border:1px solid #CBD5E0; border-radius:6px; padding:8px; background:white; font-size:7.5pt; text-align:center;">
    Local Host (192.168.1.10:8000)<br>
    ↓ packets egress<br>
    <strong>NAT Router Translates to:</strong><br>
    Public IP (203.0.113.1:54320)<br>
    (Maintains mapping in translation table)
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">Port Address Translation (PAT)</div>
  <p>The most common form of NAT (also called NAT Overload). Maps thousands of internal hosts to a single public IP by tracking distinct source port numbers.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How does a NAT router know which internal host should receive an incoming packet?"</p>
</div>
<div class="box box-buzzwords">
  <div class="buzzword-tags">
    <span class="buzz-tag">Translation Table</span>
    <span class="buzz-tag">NAT Overload / PAT</span>
    <span class="buzz-tag">Source Port Allocation</span>
    <span class="buzz-tag">Stateful Mapping</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"The NAT router maintains a dynamic NAT Translation Table. When an internal host sends a packet, the router rewrites the source IP and source port, recording this mapping. When a response returns, the router references the destination port against this table to identify the host."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is Static NAT?"</p>
  <p class="followup-a">A 1-to-1 mapping where a specific internal server is assigned a dedicated public IP, allowing incoming external connections (e.g. hosting a web server).</p>
</div>
""",
        "trap": "Don't say NAT is a security security tool. While it blocks unsolicited incoming requests by default, its primary design goal was conserving IPv4 addresses.",
        "trick": "NAT is like a corporate telephone switchboard: one public number, but calls get routed internally by extension numbers."
    },
    {
        "id": "sub-network-devices",
        "num": "20",
        "chapter": "Network Hardware & Infrastructure",
        "title": "Network Devices",
        "subtitle": "Analyzing Hubs, Switches, Routers, and L3 Switches.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Layer Segmentation</div>
  <p><strong>Hub (L1):</strong> Multi-port repeater. Broadcasts all data to all ports. Creates a single massive collision domain.</p>
  <p><strong>Switch (L2):</strong> Learns MAC addresses to forward frames selectively, creating isolated collision domains per port.</p>
  <p><strong>Router (L3):</strong> Uses IP tables to forward packets between networks. Limits broadcast domains.</p>
</div>
<div class="concept-visual">
  <table class="visual-table contrast-table" style="font-size:7.5pt;">
    <thead>
      <tr>
        <th>Device</th>
        <th>Layer</th>
        <th>Collision Domain</th>
        <th>Broadcast Domain</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Hub</td><td>L1</td><td>1 (All ports)</td><td>1 (All ports)</td></tr>
      <tr><td>Switch</td><td>L2</td><td>Isolated per port</td><td>1 (All ports)</td></tr>
      <tr><td>Router</td><td>L3</td><td>Isolated per port</td><td>Isolated per port</td></tr>
    </tbody>
  </table>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What happens to collision and broadcast domains when you replace a Hub with a L2 Switch?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Collision Isolation</span>
    <span class="buzz-tag">MAC Learning Table</span>
    <span class="buzz-tag">Broadcast Domain Width</span>
    <span class="buzz-tag">Microsegmentation</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Replacing a Hub with a Switch breaks one massive collision domain into separate collision domains for each individual port, preventing packets from colliding. The broadcast domain, however, remains unchanged; broadcasts are still forwarded out of all switch ports."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"How does a Switch build its MAC table?"</p>
  <p class="followup-a">By inspecting the source MAC address of incoming frames. If the MAC is not in its table, it associates the port with that address. If a destination is unknown, it floods the frame.</p>
</div>
""",
        "trap": "Don't confuse a L3 switch with a Router. A router handles diverse WAN interface types (fiber, coaxial, serial), while L3 switches primarily route Ethernet connections.",
        "trick": "Hubs yell to everyone. Switches speak to who they know. Routers look up directions to foreign cities."
    },
    {
        "id": "sub-switching",
        "num": "21",
        "chapter": "Network Core Technologies",
        "title": "Circuit vs Packet Switching",
        "subtitle": "Dedicated paths vs dynamically routed independent packets.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Fundamental Paradigms</div>
  <p><strong>Circuit Switching:</strong> Establishes a dedicated physical path between sender and receiver for the duration of the call (e.g. traditional telephone system).</p>
  <p><strong>Packet Switching:</strong> Breaks data into small packet units sent independently across shared nodes (e.g. internet routing).</p>
</div>
<div class="concept-visual">
  <div style="display:flex; justify-content:space-between; font-size:7.5pt; gap:10px;">
    <div style="flex:1; border:1px solid #B7791F; padding:6px; background:#FDF6E3; border-radius:4px; text-align:center;">
      <strong>Circuit Switching</strong><br>
      Dedicated bandwidth<br>
      No packet overhead<br>
      Poor channel utility
    </div>
    <div style="flex:1; border:1px solid #3182CE; padding:6px; background:#EBF8FF; border-radius:4px; text-align:center;">
      <strong>Packet Switching</strong><br>
      Shared pathways<br>
      Packet queues & delay<br>
      High channel utility
    </div>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"Why does the internet run on Packet Switching rather than Circuit Switching?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Bandwidth Utilization</span>
    <span class="buzz-tag">Burst Traffic</span>
    <span class="buzz-tag">Single Point of Failure</span>
    <span class="buzz-tag">Queueing Delay</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"Circuit switching is highly inefficient for bursty computer data, as reserved bandwidth sits idle when no data is sent. Packet switching allows thousands of users to share the same physical cable link. If a node fails, packets are dynamically rerouted, avoiding connection loss."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is statistical multiplexing?"</p>
  <p class="followup-a">A method where communication channels are shared dynamically based on demand, allocating transmission slots only to hosts actively sending packets.</p>
</div>
""",
        "trap": "Don't say packet switching is always faster. Circuit switching has zero queueing delay or jitter once established, making it optimal for legacy voice calls.",
        "trick": "Circuit is booking a private train lane. Packet is sending letters via the post office."
    },
    {
        "id": "sub-vpn",
        "num": "22",
        "chapter": "Network Security & VPNs",
        "title": "VPN & Tunneling",
        "subtitle": "Establishing secure encrypted channels over untrusted public networks.",
        "yield_stars": "★★★★☆",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Encapsulation & Cryptography</div>
  <p>A Virtual Private Network (VPN) creates an encrypted tunnel between a client and a gateway. Typically implemented using <strong>IPsec</strong> or <strong>SSL/TLS</strong>.</p>
</div>
<div class="concept-visual">
  <div style="background:#EBF8FF; border:1px solid #3182CE; padding:8px; border-radius:6px; font-size:7.5pt; text-align:center;">
    Client Host [Data | Original IP Header]<br>
    ↓ Encapsulated by IPsec Tunnel Mode<br>
    [New IP Header | <strong>ESP Header (Encrypted Payload)</strong>]
  </div>
</div>
<div class="box box-industry">
  <div class="box-title">IPsec: Transport vs Tunnel Mode</div>
  <p><strong>Transport Mode:</strong> Only encrypts the IP payload. Keeps the original IP headers intact. Used end-to-end.<br>
  <strong>Tunnel Mode:</strong> Encrypts the entire original IP packet and wraps it in a new IP header. Used router-to-router.</p>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"What is the difference between IPsec Tunnel Mode and Transport Mode?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Encapsulating Security Payload</span>
    <span class="buzz-tag">Header Encryption</span>
    <span class="buzz-tag">Gateway to Gateway</span>
    <span class="buzz-tag">Host to Host</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"In IPsec Transport Mode, only the payload of the IP packet is encrypted; the original IP header remains visible, leaving source/destination identities public. In Tunnel Mode, the entire original IP packet (header and payload) is encrypted and nested inside a new IP header, concealing internal IPs."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What protocol does SSL VPN use?"</p>
  <p class="followup-a">Uses standard TLS on Port 443. This is highly popular because Port 443 is open on almost all firewalls globally, preventing connection blocks.</p>
</div>
""",
        "trap": "Don't assume a VPN makes you anonymous on the web. It encrypts traffic from your ISP, but the VPN provider can see all DNS and IP destination routes.",
        "trick": "Transport Mode = Putting a letter in an envelope. Tunnel Mode = Putting the entire envelope inside a security parcel."
    },
    {
        "id": "sub-firewalls",
        "num": "23",
        "chapter": "Network Security & Firewalls",
        "title": "Firewalls (Stateful vs WAF)",
        "subtitle": "Inspecting network traffic based on rules, connection state, and application logic.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Firewall Taxonomy</div>
  <p><strong>Stateless (L3/4):</strong> Checks individual packets against Access Control Lists (ACLs). Quick, but misses multi-packet attack patterns.</p>
  <p><strong>Stateful (L3/4):</strong> Tracks connection states (SYN, ESTABLISHED). Dynamically permits return traffic.</p>
  <p><strong>WAF (L7):</strong> Inspects HTTP payloads for application-layer attacks (SQLi, XSS).</p>
</div>
<div class="concept-visual">
  <table class="visual-table contrast-table" style="font-size:7.5pt;">
    <thead>
      <tr>
        <th>Type</th>
        <th>Layer</th>
        <th>Inspection Depth</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Stateless</td><td>L3 / L4</td><td>IP, Port, Protocol</td></tr>
      <tr><td>Stateful</td><td>L3 / L4</td><td>Session State Tracker</td></tr>
      <tr><td>WAF</td><td>L7</td><td>HTTP headers, query, body</td></tr>
    </tbody>
  </table>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How does a Web Application Firewall (WAF) differ from a traditional Stateful Firewall?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">Deep Packet Inspection</span>
    <span class="buzz-tag">Layer 7 Payload</span>
    <span class="buzz-tag">SQL Injection (SQLi)</span>
    <span class="buzz-tag">TCP Connection State</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"A Stateful firewall operates at Layer 3 and 4, tracking TCP session states to confirm valid connections. It permits all traffic on port 443 blindly. A WAF operates at Layer 7, performing deep packet inspection of the HTTP payload to block threats like SQLi or XSS."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a Next-Generation Firewall (NGFW)?"</p>
  <p class="followup-a">A system combining L3/L4 stateful inspection with L7 application control, inline IPS/IDS prevention, and encrypted SSL decryption capabilities.</p>
</div>
""",
        "trap": "Don't state that a WAF is a drop-in replacement for a network firewall. Both are needed: network firewalls block network ports, while WAFs protect web servers.",
        "trick": "Stateless = Bouncer checking IDs. Stateful = Bouncer remembering who went out to smoke. WAF = Bouncer reading your backpack contents."
    },
    {
        "id": "sub-ddos",
        "num": "24",
        "chapter": "Network Attacks & Defenses",
        "title": "DDoS Attacks & Mitigation",
        "subtitle": "Flooding system pipelines with distributed botnet traffic.",
        "yield_stars": "★★★★★",
        "left_col": """
<div class="box box-theory">
  <div class="box-title">Attack Vectors</div>
  <p><strong>Volumetric Attacks:</strong> Flooding the bandwidth pipeline (e.g. DNS Amplification, NTP Reflection).</p>
  <p><strong>Protocol Attacks:</strong> Exploiting connection state limitations (e.g. TCP SYN Flood, Ping of Death).</p>
  <p><strong>Application Layer (L7):</strong> Spamming complex database queries or API endpoints (e.g. HTTP GET flood).</p>
</div>
<div class="concept-visual">
  <div style="border:1px solid #E53E3E; border-radius:6px; padding:10px; background:#FDEDEB; font-size:7.5pt; text-align:center;">
    <strong>DNS Amplification Attack Flow</strong><br>
    Attacker (Spoofs Target IP)<br>
    ↓ sends small request to open DNS servers<br>
    DNS Servers → send massive responses to spoofed <strong>Target IP</strong>
  </div>
</div>
""",
        "right_col": """
<div class="box box-question">
  <div class="box-title">Core Interview Question</div>
  <p>"How does a DNS Amplification attack work, and how can it be mitigated?"</p>
</div>
<div class="box box-buzzwords">
  <div class="box-title">Keywords to Drop</div>
  <div class="buzzword-tags">
    <span class="buzz-tag">IP Spoofing</span>
    <span class="buzz-tag">Reflection Attack</span>
    <span class="buzz-tag">Anycast Routing</span>
    <span class="buzz-tag">Rate Limiting</span>
  </div>
</div>
<div class="box box-answer">
  <div class="box-title">Model Answer</div>
  <p>"An attacker spoofs the source IP of DNS queries to match the target's IP, then queries open DNS resolvers. By requesting large DNSSEC records, a tiny 60-byte request triggers a 4000-byte response. This reflects and amplifies traffic, flooding the target interface."</p>
</div>
<div class="box box-question followup-box">
  <div class="box-title followup-title">Deep Dive Follow-Up</div>
  <p class="followup-q">"What is a CDNs role in DDoS mitigation?"</p>
  <p class="followup-a">CDNs (like Cloudflare) use Anycast routing to distribute massive incoming traffic across globally distributed data centers, preventing load spikes at origin.</p>
</div>
""",
        "trap": "Don't suggest simple IP blocking as a solution. In a distributed attack (DDoS), thousands of rotative IPs are used, making static blacklisting useless.",
        "trick": "DNS Amplification = Calling a pizza shop, spoofing your neighbor's caller ID, and ordering 50 family boxes to their house."
    }
]

# ─────────────────────────────────────────
# PLACEMENT BOOSTERS DICTIONARY
# ─────────────────────────────────────────
CN_BOOSTERS = {
    "sub-osi": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Explain OSI as a reference blueprint. In interviews, emphasize that L3/L4 deal with network routing and end-to-end delivery, while L7 interfaces directly with software application processes."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Saying the internet runs on OSI. It runs on TCP/IP. <strong>Depth:</strong> Know all layers, their order, and PDUs (Segment, Packet, Frame, Bit).</p>
</div>
""",
    "sub-tcpip": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Point out that TCP/IP consolidates OSI software layers (5,6,7) into a single Application layer, leaving session tracking and presentation syntax to the developer's client code."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Confusing layer names (e.g. Network vs Internet). <strong>Depth:</strong> Match OSI layers to TCP/IP and name key protocols of each layer.</p>
</div>
""",
    "sub-tcp-udp": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Frame this as a trade-off: TCP prioritizes reliability (3-way handshake, retransmissions) for web/email, while UDP prioritizes speed and low latency (8-byte header) for DNS/gaming."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking UDP is 'broken'. It simply lacks delivery checks. <strong>Depth:</strong> Compare header structures (20 vs 8 bytes) and socket API differences.</p>
</div>
""",
    "sub-handshake": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Explain that the 3-way handshake (SYN, SYN-ACK, ACK) synchronizes sequence numbers bidirectionally, establishing a virtual session before any application data is sent."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Forgetting why it is 3 steps (not 2 or 4). 2 isn't enough to confirm mutual acknowledgment. <strong>Depth:</strong> Draw sequence exchange diagram and list TCP flags.</p>
</div>
""",
    "sub-ip-address": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Explain CIDR as variable-length subnet masking that replaced rigid classful (A, B, C) address allocation to optimize and conserve the limited IPv4 address space."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Forgetting to subtract 2 for network & broadcast IP bounds. <strong>Depth:</strong> Fast subnet calculations (e.g., /24, /27, /30 host capacities).</p>
</div>
""",
    "sub-mac-arp": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"ARP bridges logical L3 IP addresses to physical L2 MAC addresses. Mention that ARP broadcasts requests locally but unicasts the mapped response back."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Saying ARP is routed globally. It is local broadcast only. <strong>Depth:</strong> Understand ARP cache lookup and cache poisoning risks.</p>
</div>
""",
    "sub-dns": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Describe DNS as the phonebook of the internet. It uses UDP port 53 for fast queries, but falls back to TCP if the response exceeds 512 bytes."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Not knowing recursive vs iterative lookup differences. <strong>Depth:</strong> Detail record types (A, AAAA, CNAME, MX, TXT).</p>
</div>
""",
    "sub-http-https": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"HTTPS is HTTP wrapped in SSL/TLS. Emphasize that HTTP sends plain text on port 80, whereas HTTPS encrypts session payloads on port 443."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking HTTPS encrypts the TCP header (IP/Ports remain visible). <strong>Depth:</strong> Explain HTTP status codes (200, 301, 400, 401, 403, 404, 500, 503).</p>
</div>
""",
    "sub-dhcp": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Explain the DORA process: Discover (broadcast) → Offer (unicast) → Request (broadcast) → Acknowledge (unicast). Mention that it runs over UDP."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking IP lease is permanent. IPs are leased for temporary sessions. <strong>Depth:</strong> Explain what static IP reservation is on routers.</p>
</div>
""",
    "sub-ssl-tls": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Detail the hybrid cryptography flow: Asymmetric encryption (RSA/Diffie-Hellman) is used to safely agree on a Symmetric Session Key for data encryption."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Saying symmetric key exchange is slow. Only asymmetric setup is slow. <strong>Depth:</strong> Explain certificates, CA validation, and SNI purpose.</p>
</div>
""",
    "sub-routing": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Explain routing protocols: OSPF is a Link-State protocol used internally (IGP), while BGP is a Path-Vector protocol routing between Autonomous Systems (EGP)."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Routing based on MAC addresses instead of IPs. <strong>Depth:</strong> Contrast Link-State (Dijkstra) vs Distance-Vector (Bellman-Ford).</p>
</div>
""",
    "sub-nat": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"NAT/PAT maps multiple private local IP addresses to a single public IP by modifying port numbers in the TCP/UDP headers, preserving public IPv4 space."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking NAT is a security firewall. It just hides internal IPs. <strong>Depth:</strong> Differentiate Static NAT, Dynamic NAT, and PAT (Overload).</p>
</div>
""",
    "sub-firewall": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Stateful firewalls monitor active connection states (SYN/ACK). They permit response traffic automatically, unlike stateless ACLs which need explicit rules."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Stateless ACLs check payload context. They only inspect headers. <strong>Depth:</strong> Explain packet filtering vs stateful inspection vs WAF.</p>
</div>
""",
    "sub-vpn": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"A VPN creates an encrypted tunnel (typically using IPsec or SSL/TLS) over the public internet, encapsulating and protecting packet payloads from sniffing."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking a VPN hides traffic volume or origin completely. <strong>Depth:</strong> Contrast Tunnel Mode (full packet crypt) vs Transport Mode.</p>
</div>
""",
    "sub-ddos": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"DDoS floods targets using botnets. Mitigate via Anycast routing (distributing load) or rate-limiting filters (identifying signature patterns)."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Assuming simple IP blocks stop DDoS. Botnets rotatively shift IPs. <strong>Depth:</strong> Explain SYN flood, UDP flood, and L7 HTTP floods.</p>
</div>
""",
    "sub-icmp": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"ICMP is a L3 protocol used for diagnostics (ping, traceroute). It sends control messages (Echo Request/Reply) without ports or TCP sessions."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Believing ICMP runs over TCP or UDP. It rides directly inside IP. <strong>Depth:</strong> Explain how TTL decrementing powers traceroute hops.</p>
</div>
""",
    "sub-load-balancer": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Contrast L4 vs L7 load balancing. L4 Balancers route packets at the TCP layer (IP/Port), while L7 Balancers inspect headers/cookies/URLs for routing."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking L4 load balancing is content-aware. It has zero payload visibility. <strong>Depth:</strong> Detail LB algorithms (Round Robin, Least Connections, IP Hash).</p>
</div>
""",
    "sub-proxy": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"A Forward Proxy acts for client anonymity or access control. A Reverse Proxy sits before web servers, handling load distribution, SSL termination, and caching."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Reversing the two roles. Client side = Forward; Server side = Reverse. <strong>Depth:</strong> Explain reverse proxy load balancing benefits.</p>
</div>
""",
    "sub-cdn": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"CDNs cache static assets (images, JS, CSS) at globally distributed edge servers, minimizing physical latency by bringing data closer to the client."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking CDNs handle dynamic DB writes. Edges cache read assets. <strong>Depth:</strong> Explain Origin vs Edge server relationship and TTL caching.</p>
</div>
""",
    "sub-sockets": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"A socket is an endpoint bound to an IP address and a Port. It provides the software API interface for applications to write to transport layers."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Confusing socket with port. Socket is the physical IP:Port bind instance. <strong>Depth:</strong> Explain socket syscall lifecycle (socket, bind, listen, accept).</p>
</div>
""",
    "sub-ipv4-v6": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Explain that IPv6 expands addresses to 128-bit hex formats, eliminating subnet NAT requirements. Transition methods include dual-stack and tunneling."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Saying IPv6 is backward compatible with IPv4. They are incompatible. <strong>Depth:</strong> Compare address counts and header field simplifications.</p>
</div>
""",
    "sub-cookies": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Cookies are client-side text files holding session tokens. Sessions are server-side data stores. The client passes the Session ID cookie on every request."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Storing password hashes in cookies. Only store session tokens. <strong>Depth:</strong> Explain HttpOnly, Secure, and SameSite cookie attributes.</p>
</div>
""",
    "sub-wireshark": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"Wireshark acts as a packet capture tool. Mention its use in diagnosing retransmissions, latency, and inspecting protocol handshakes in real time."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Believing Wireshark can decrypt HTTPS without session key logs. <strong>Depth:</strong> Differentiate Promiscuous Mode from standard NIC capture.</p>
</div>
""",
    "sub-http3": """
<div class="box box-say">
  <div class="box-title">💬 What To Say In Interview</div>
  <p>"HTTP/3 replaces TCP with UDP using the QUIC protocol. This solves TCP's head-of-line blocking by handling stream multiplexing natively at the link layer."</p>
</div>
<div class="box box-mistake">
  <div class="box-title">⚠️ Common Mistake &amp; Depth</div>
  <p><strong>Mistake:</strong> Thinking UDP makes HTTP/3 unreliable. QUIC handles reliability. <strong>Depth:</strong> Explain QUIC's 1-RTT handshake and connection migration features.</p>
</div>
"""
}

HIGH_YIELD_TOPICS = ["sub-osi", "sub-tcpip", "sub-tcp-udp", "sub-handshake", "sub-dns"]

# ─────────────────────────────────────────
# GENERATE_PAGE: 14-Section Template (No notes sponge)
# ─────────────────────────────────────────
def get_topic_followups(tid):
    followups_dict = {
        "sub-osi": "• Why does a gateway operate at all 7 layers?<br>• What is encapsulation/decapsulation?",
        "sub-tcpip": "• How does the Internet layer handle routing?<br>• Which layer handles encryption in TCP/IP?",
        "sub-tcp-udp": "• Why does DNS use UDP instead of TCP?<br>• Can we build a reliable protocol on top of UDP?",
        "sub-ip-addressing": "• What is the purpose of a subnet mask?<br>• Explain private vs public IP addressing.",
        "sub-subnetting": "• How do you calculate the network address of a subnet?<br>• What is the size of a /32 subnet?",
        "sub-mac-arp": "• How does a packet's MAC address change at router hops?<br>• What is gratuitous ARP?",
        "sub-dns": "• Differentiate recursive and iterative DNS queries.<br>• What is DNS cache poisoning?",
        "sub-dhcp": "• Describe the DHCP DORA process steps.<br>• What is DHCP relaying?",
        "sub-http": "• What is the difference between HTTP/1.1 and HTTP/2?<br>• Explain HTTP status code classes.",
        "sub-https-ssl": "• Why is symmetric encryption used for payload transit?<br>• What is SNI in TLS?",
        "sub-tcp-handshake": "• Why is a 2-way handshake insufficient?<br>• What is a SYN flood attack?",
        "sub-tcp-termination": "• Explain the 4-way TCP teardown sequence.<br>• Why is TIME_WAIT state necessary?",
        "sub-flow-control": "• What is the window size field in TCP header?<br>• What is sliding window window scaling?",
        "sub-sliding-window": "• Contrast Go-Back-N vs Selective Repeat.<br>• What is receiver buffer exhaustion?",
        "sub-congestion-control": "• Explain TCP Slow Start phase.<br>• How does AIMD work in congestion avoidance?",
        "sub-mac-address": "• How does a switch build its MAC table?<br>• Contrast L2 switch forwarding vs L3 routing.",
        "sub-routing": "• What is autonomous system routing?<br>• Contrast static routing vs dynamic routing.",
        "sub-routing-protocols": "• How does OSPF exchange routing updates?<br>• Why does BGP use TCP port 179?",
        "sub-nat": "• Differentiate Static NAT, Dynamic NAT, and PAT.<br>• What are the security limits of NAT?",
        "sub-network-devices": "• Explain the collision domains of hub vs switch.<br>• What is a broadcast storm?",
        "sub-switching": "• Contrast Layer 2 switches with Layer 3 switches.<br>• What is a VLAN tag?",
        "sub-vpn": "• Contrast tunnel mode vs transport mode in IPsec.<br>• What is SSL VPN?",
        "sub-firewalls": "• Contrast stateful inspection with stateless ACLs.<br>• What is a Web Application Firewall?",
        "sub-ddos": "• How does Anycast routing mitigate DDoS?<br>• Explain SYN cookie defenses."
    }
    return followups_dict.get(tid, "• Name related protocols at this layer.<br>• What are common troubleshooting steps?")

def get_cn_space_filler(tid):
    fillers = {
        "sub-osi": """
<div class="box box-depth">
  <div class="box-title">📈 Interview Depth Progression</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Basic):</strong> List all 7 layers and their physical order bottom-up.<br>
    <strong>Level 2 (PDU):</strong> Map layer data units (Segment, Packet, Frame, Bit).<br>
    <strong>Level 3 (Device):</strong> Explain why routers operate at L3 and switches at L2.<br>
    <strong>Level 4 (Gateway):</strong> Understand why firewalls/gateways run up to L7.
  </div>
</div>
""",
        "sub-tcpip": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "Why did the TCP/IP model win over the theoretical OSI model?"<br>
    <strong>Candidate:</strong> "OSI was designed by standard committees before software protocols were fully implemented. TCP/IP was built by DARPA engineers who wrote working code first. Practice beat theory."
  </div>
</div>
""",
        "sub-tcp-udp": """
<div class="box box-depth">
  <div class="box-title">⚖️ Protocol Trade-Off Analysis</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>TCP (Stateful):</strong> High overhead (20B header), guarantees order, handles congestion. Best for files, web, and database connections.<br>
    <strong>UDP (Stateless):</strong> Low overhead (8B header), no delivery checks. Best for DNS, VoIP, real-time gaming, and multiplexed streams.
  </div>
</div>
""",
        "sub-ip-addressing": """
<div class="box box-depth">
  <div class="box-title">📈 Address Depth Progression</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Basic):</strong> Differentiate 32-bit IPv4 from 128-bit IPv6 address size.<br>
    <strong>Level 2 (Format):</strong> Format IPv4 in dotted decimal and IPv6 in hexadecimal.<br>
    <strong>Level 3 (Exhaustion):</strong> Explain how NAT/CIDR delayed IPv4 address depletion.<br>
    <strong>Level 4 (IPsec):</strong> Identify that IPsec is built natively into the IPv6 standard.
  </div>
</div>
""",
        "sub-subnetting": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "If you allocate /26 subnets in your cloud VPC, how many servers can you run in each?"<br>
    <strong>Candidate:</strong> "A /26 subnet has 6 host bits, giving 64 total addresses. We subtract 2 for the network and broadcast addresses, leaving 62 usable host IPs."
  </div>
</div>
""",
        "sub-mac-arp": """
<div class="box box-depth">
  <div class="box-title">📈 Resolve Depth Progression</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Logical):</strong> Explain that ARP maps a Layer 3 IP to a Layer 2 MAC.<br>
    <strong>Level 2 (Process):</strong> Describe the ARP broadcast request and unicast reply flow.<br>
    <strong>Level 3 (Caching):</strong> State why ARP tables cache MAC mappings locally for speed.<br>
    <strong>Level 4 (Spoofing):</strong> Explain how gratuitous ARP allows ARP spoofing MitM attacks.
  </div>
</div>
""",
        "sub-dns": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "Why does DNS run on UDP instead of TCP?"<br>
    <strong>Candidate:</strong> "Speed and scale. DNS requests are small, fitting in one packet. UDP avoids connection setup round-trips. But if a response exceeds 512 bytes, DNS falls back to TCP."
  </div>
</div>
""",
        "sub-dhcp": """
<div class="box box-depth">
  <div class="box-title">📈 DHCP Allocation states</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (DORA):</strong> Define Discover, Offer, Request, and Acknowledge stages.<br>
    <strong>Level 2 (Port):</strong> Recall that DHCP uses UDP ports 67 (server) and 68 (client).<br>
    <strong>Level 3 (Leasing):</strong> Explain T1 (renewal at 50% time) and T2 (rebinding at 87.5% time).<br>
    <strong>Level 4 (Relay):</strong> Understand how DHCP relay agents route requests across subnets.
  </div>
</div>
""",
        "sub-http": """
<div class="box box-depth">
  <div class="box-title">📈 HTTP Version Progression</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>HTTP/1.1:</strong> Persistent connections, pipelining, chunked transfer encoding.<br>
    <strong>HTTP/2:</strong> Binary framing, multiplexing over single TCP connection, server push.<br>
    <strong>HTTP/3:</strong> Replaces TCP with QUIC over UDP, eliminating Head-of-Line blocking.
  </div>
</div>
""",
        "sub-https-ssl": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "Why do we use symmetric encryption in HTTPS if asymmetric is more secure?"<br>
    <strong>Candidate:</strong> "Symmetric encryption isn't less secure; it's just much faster. We use asymmetric encryption solely to safely exchange the symmetric session key, which encrypts payload."
  </div>
</div>
""",
        "sub-tcp-handshake": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "Why isn't a 2-way handshake enough to establish a TCP connection?"<br>
    <strong>Candidate:</strong> "A 2-way handshake only confirms the client can reach the server. The client cannot verify if the server received its acknowledgment, leaving the connection half-open."
  </div>
</div>
""",
        "sub-tcp-termination": """
<div class="box box-depth">
  <div class="box-title">📈 Teardown State Progression</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (FIN):</strong> Host A sends FIN segment indicating it has no more data.<br>
    <strong>Level 2 (ACK):</strong> Host B acknowledges FIN, entering CLOSE_WAIT state.<br>
    <strong>Level 3 (FIN-2):</strong> Host B finishes sending its data, then sends its own FIN.<br>
    <strong>Level 4 (TIME_WAIT):</strong> Host A enters TIME_WAIT (2*MSL) to ensure final ACK is received.
  </div>
</div>
""",
        "sub-flow-control": """
<div class="box box-depth">
  <div class="box-title">📈 Flow Control Progression</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Scope):</strong> Flow control is end-to-end (protects receiver buffer overflow).<br>
    <strong>Level 2 (Field):</strong> Controlled by the 16-bit Window Size field in the TCP header.<br>
    <strong>Level 3 (Scaling):</strong> Window Scaling option allows windows up to 1GB.<br>
    <strong>Level 4 (Zero Window):</strong> Sender stops sending when window is 0; polls with keep-alives.
  </div>
</div>
""",
        "sub-sliding-window": """
<div class="box box-depth">
  <div class="box-title">⚖️ Window Protocol Comparison</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Stop &amp; Wait:</strong> Sender sends 1 packet and waits for ACK before sending next.<br>
    <strong>Go-Back-N:</strong> Sends N packets. On loss, retransmits all packets starting from loss.<br>
    <strong>Selective Repeat:</strong> Sends N packets. Receiver buffers out-of-order; retransmits only loss.
  </div>
</div>
""",
        "sub-congestion-control": """
<div class="box box-depth">
  <div class="box-title">📈 Congestion Phases</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Slow Start:</strong> Exponential cwnd growth (doubles every RTT) up to ssthresh.<br>
    <strong>Congestion Avoidance:</strong> Linear cwnd growth (adds 1 MSS per RTT) via AIMD.<br>
    <strong>Fast Retransmit:</strong> Retransmits packet on receiving 3 duplicate ACKs.<br>
    <strong>Fast Recovery:</strong> Drops cwnd to half of current size, skips slow start back to linear.
  </div>
</div>
""",
        "sub-mac-address": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "What happens to the MAC addresses of a frame when passing a router?"<br>
    <strong>Candidate:</strong> "The router strips the source MAC and sets it to its egress port MAC. It sets the destination MAC to the next hop's ingress port MAC. IP addresses remain constant."
  </div>
</div>
""",
        "sub-routing": """
<div class="box box-depth">
  <div class="box-title">📈 Routing Depth Progression</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Logic):</strong> Router routes IP packets between subnets using a routing table.<br>
    <strong>Level 2 (Static):</strong> Administrator manually configures routes (used in stub networks).<br>
    <strong>Level 3 (Dynamic):</strong> Routing protocols dynamically exchange and calculate paths.<br>
    <strong>Level 4 (Tables):</strong> Inspecting destination IP prefix matches for longest prefix match.
  </div>
</div>
""",
        "sub-routing-protocols": """
<div class="box box-depth">
  <div class="box-title">⚖️ IGP vs EGP Comparison</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>OSPF (IGP Link-State):</strong> Uses Dijkstra. Fast convergence. Operates inside Autonomous Systems.<br>
    <strong>BGP (EGP Path-Vector):</strong> Uses TCP port 179. Policy-based routing. Connects different Autonomous Systems.
  </div>
</div>
""",
        "sub-nat": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "Why do we need Port Address Translation (PAT) instead of basic NAT?"<br>
    <strong>Candidate:</strong> "Basic NAT requires a 1:1 mapping of private IPs to public IPs. PAT maps multiple private IPs to a single public IP by translating port numbers, saving public IPs."
  </div>
</div>
""",
        "sub-network-devices": """
<div class="box box-depth">
  <div class="box-title">📈 Device Domain Progression</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Hub (L1):</strong> Shared collision domain, shared broadcast domain. Half duplex.<br>
    <strong>Switch (L2):</strong> Separate collision domain per port, shared broadcast domain. Full duplex.<br>
    <strong>Router (L3):</strong> Separate collision domain, separate broadcast domain. IP isolation.
  </div>
</div>
""",
        "sub-switching": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "What is a Layer 3 Switch and when do you use it instead of a router?"<br>
    <strong>Candidate:</strong> "A L3 switch performs routing in hardware using ASICs, which is much faster. It's used for high-speed routing between local VLANs, whereas routers connect WANs."
  </div>
</div>
""",
        "sub-vpn": """
<div class="box box-depth">
  <div class="box-title">📈 VPN Tunneling States</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Level 1 (Protocol):</strong> Encapsulates private packets inside public carrier protocols.<br>
    <strong>Level 2 (Modes):</strong> Tunnel Mode (encrypts full packet) vs Transport Mode (encrypts payload).<br>
    <strong>Level 3 (IPsec):</strong> Uses IKE for key exchange, ESP for encryption, AH for authentication.<br>
    <strong>Level 4 (SSL VPN):</strong> Runs over TLS, enabling secure remote access through web browsers.
  </div>
</div>
""",
        "sub-firewalls": """
<div class="box box-depth">
  <div class="box-title">📈 Firewall Progression</div>
  <div style="font-size: 7.5pt; line-height: 1.35;">
    <strong>Packet Filter (Stateless):</strong> Checks IP, ports, and protocols against ACL tables.<br>
    <strong>Stateful Inspection:</strong> Tracks active TCP handshake state tables, allowing dynamic responses.<br>
    <strong>Next-Gen / WAF:</strong> Deep packet inspection at Layer 7, validating SQL, scripting payloads.
  </div>
</div>
""",
        "sub-ddos": """
<div class="box box-scenario">
  <div class="box-title">🤝 Real Interview Scenario</div>
  <div style="font-size: 7.5pt; line-height: 1.35; color: #2D3748;">
    <strong>Interviewer:</strong> "How do you protect a web server from a SYN flood attack?"<br>
    <strong>Candidate:</strong> "We use SYN Cookies. The server responds with a SYN-ACK containing a cryptographic hash of parameters as the sequence number, allocating no connection state memory until client replies with ACK."
  </div>
</div>
"""
    }
    return fillers.get(tid, "")

def get_cn_industry_box(tid):
    industry_usage = {
        "sub-osi": "Web developers utilize the OSI model conceptually to isolate network bugs, deciding if a connection error is a routing issue (L3) or a TLS failure (L6).",
        "sub-tcpip": "The modern Internet backbone and cloud environments (like AWS VPCs) operate strictly on the 4-layer TCP/IP suite to route packet streams globally.",
        "sub-tcp-udp": "Real-time communication software (like Zoom or Discord) uses UDP for video/voice data streaming to eliminate lag, while using TCP for reliable chat messages.",
        "sub-ip-addressing": "Enterprise cloud architectures route traffic using Classless Inter-Domain Routing (CIDR) blocks (e.g. /16 or /24) to partition large subnets.",
        "sub-subnetting": "Network security teams partition corporate offices into logical subnets to isolate guest Wi-Fi networks from sensitive internal backend databases.",
        "sub-mac-arp": "Local area switches run Address Resolution Protocol (ARP) tables to translate dynamic IP addresses to static physical MAC card slots on local hardware.",
        "sub-dns": "Content Delivery Networks (like Cloudflare) use Geolocation DNS routing to direct domain requests to the nearest edge cache server, minimizing latency.",
        "sub-dhcp": "Public Wi-Fi routers dynamically assign IP configurations to thousands of customer smartphones using DHCP lease timers to recycle idle IP space.",
        "sub-http": "Browser engines fetch web documents using HTTP/2 multiplexing, allowing multiple image and script assets to load in parallel over a single TCP stream.",
        "sub-https-ssl": "Banking web applications run TLS handshakes to negotiate symmetric session keys, ensuring all customer transactions remain encrypted and tamper-proof.",
        "sub-tcp-handshake": "Web servers scale their backlog queues to manage concurrent incoming TCP SYN packets, preventing half-open connection memory exhaustion.",
        "sub-tcp-termination": "High-performance proxy servers (like Nginx) monitor sockets in TIME_WAIT state to ensure late arriving packet fragments don't pollute new connections.",
        "sub-flow-control": "Data processing pipelines tune the TCP receive window size to slow down high-speed senders when the local buffer memory runs full.",
        "sub-sliding-window": "File transfer protocols (like SFTP) utilize sliding window sequences to transmit batch segments before receiving individual acknowledgments.",
        "sub-congestion-control": "Video streaming services (like Netflix) throttle data rates using TCP congestion windows (AIMD algorithm) when network packet drops indicate path overload.",
        "sub-mac-address": "Local area networks implement MAC address filtering on switches to block unregistered devices from tapping corporate Ethernet ports.",
        "sub-routing": "Core Internet routers inspect global BGP routing tables to forward IP packets along the shortest path toward their destination subnet.",
        "sub-routing-protocols": "Corporate datacenters run Open Shortest Path First (OSPF) routing protocols to automatically recalculate paths when a fiber optic link breaks.",
        "sub-nat": "Home routers use Port Address Translation (PAT) to share a single public IP address among dozens of smart devices, conserving global IPv4 address space.",
        "sub-network-devices": "Network engineers deploy Layer 3 switches at core server racks for line-rate packet forwarding, while using hubs only in legacy labs.",
        "sub-switching": "Virtual Private Clouds (VPCs) run virtual switches to isolate broadcast traffic between tenants inside physical hypervisor chassis.",
        "sub-vpn": "Remote hybrid workforces connect to corporate offices using IPsec VPN tunnels to encrypt private intranet traffic over the public Internet.",
        "sub-firewalls": "Web Application Firewalls (WAFs) run deep packet inspection to block cross-site scripting (XSS) and SQL injection payloads in HTTP requests.",
        "sub-ddos": "Global traffic scrubbers (like AWS Shield) mitigate SYN floods and reflection attacks using distributed edge scrubbing centers."
    }
    desc = industry_usage.get(tid, "Network architectures use standard routing and transmission control protocols to coordinate reliable global communications.")
    return f"""
<div class="box box-industry" style="padding: 10px; margin-bottom: 0; border: 1px solid #F5E6B3; background: #FDF6E3;">
  <div class="box-title" style="font-size: 8pt; color: #B7791F; margin-bottom: 4px;">🏭 Where Used in Industry</div>
  <p style="font-size: 7.5pt; line-height: 1.35; color: #5C5438; margin: 0;">{desc}</p>
</div>
"""

def get_cn_depth_box(tid):
    depth_levels = {
        "sub-osi": [
            "Purpose of the 7 layers and layer boundaries.",
            "Data Encapsulation formats (Segment, Packet, Frame, Bits).",
            "Comparison: Presentation (encryption/compression) vs Application layer.",
            "Physical hardware mapping (Cables at L1, Switches at L2, Routers at L3).",
            "Decapsulation sequence and error boundary checks during packet arrival."
        ],
        "sub-tcpip": [
            "4-layer TCP/IP layout vs 7-layer OSI layout.",
            "Link, Internet, Transport, and Application layers.",
            "Header overhead across encapsulation layers.",
            "Multiplexing/demultiplexing using protocol numbers and port selectors.",
            "Kernel networking stack architecture (socket queues, ring buffers)."
        ],
        "sub-tcp-udp": [
            "Connection-oriented (TCP) vs connectionless (UDP) behaviors.",
            "Reliability tools: ACKs, checksums, and sequence IDs in TCP.",
            "Header comparisons: 20-60 byte TCP header vs 8-byte UDP header.",
            "Use cases: gaming/streaming (UDP) vs web page/file transfer (TCP).",
            "User-space reliability layers (e.g. QUIC protocol) running on top of UDP."
        ],
        "sub-ip-addressing": [
            "IPv4 address classes (A, B, C) and private IP ranges.",
            "Classless Inter-Domain Routing (CIDR) prefix formats.",
            "IPv6 features (128-bit space, SLAAC, header layout differences).",
            "Loopback addresses (127.0.0.1) and APIPA ranges (169.254.x.x).",
            "Hierarchical IP routing blocks and prefix aggregation."
        ],
        "sub-subnetting": [
            "Calculating network ID, host ID, and broadcast IP.",
            "Subnet masks conversion to binary representation.",
            "Variable Length Subnet Masking (VLSM) partitioning schemas.",
            "Usable host range equations: 2^(32-N) - 2.",
            "Inter-VLAN routing interfaces and route table setups."
        ],
        "sub-mac-arp": [
            "MAC physical addresses vs IP logical addresses.",
            "ARP DORA phases: Request (broadcast) and Reply (unicast).",
            "ARP cache tables timeouts and local sweeps.",
            "ARP Spoofing attacks and dynamic ARP inspection (DAI) guards.",
            "Proxy ARP routing across subnet interfaces."
        ],
        "sub-dns": [
            "DNS domain names hierarchy (Root, TLD, Authoritative DNS).",
            "Recursive vs Iterative query resolutions.",
            "DNS record classes (A, AAAA, CNAME, MX, TXT, NS).",
            "TTL (Time-To-Live) cache invalidation settings on clients.",
            "Anycast DNS routing and DNSSEC cryptographic validations."
        ],
        "sub-dhcp": [
            "DHCP DORA sequence: Discover, Offer, Request, Acknowledge.",
            "DHCP lease negotiation timers (T1 at 50%, T2 at 87.5%).",
            "DHCP Relay Agents forwarding broadcasts across subnet links.",
            "IP pool exhaustion and static MAC-IP reservations.",
            "Rogue DHCP server attacks and DHCP Snooping protection."
        ],
        "sub-http": [
            "HTTP Request (GET/POST/PUT) and Response (status codes) structures.",
            "HTTP/1.1 persistent connections, pipelining, and HoL blocking.",
            "HTTP/2 binary framing, stream multiplexing, and server push.",
            "HTTP/3 QUIC stream independence and connection migration.",
            "Browser caching controls (Cache-Control, ETag validation)."
        ],
        "sub-https-ssl": [
            "HTTPS port 443 vs HTTP port 80 credentials security.",
            "TLS handshake phases: Cipher negotiation, Key exchange (DH), Cert validation.",
            "Asymmetric encryption (session setup) vs symmetric encryption (payload).",
            "Certificate Authorities (CAs), trust store root certs, and CRLs.",
            "ALPN negotiation and TLS 1.3 0-RTT handshakes."
        ],
        "sub-tcp-handshake": [
            "Three-way handshake states: SYN, SYN-ACK, ACK.",
            "Initial Sequence Number (ISN) generation logic.",
            "Half-open queue (SYN backlog) and accept queue allocations.",
            "SYN flood attacks and cookie-based stateless defenses.",
            "TCP Fast Open (TFO) payload exchange during handshake."
        ],
        "sub-tcp-termination": [
            "Four-way handshake states: FIN, ACK, FIN, ACK.",
            "Half-closed states (FIN_WAIT_1, FIN_WAIT_2, CLOSE_WAIT).",
            "TIME_WAIT state purpose (2*MSL wait duration).",
            "Socket reuse problems and SO_REUSEADDR socket options.",
            "RST (Reset) flag overrides for immediate termination."
        ],
        "sub-flow-control": [
            "End-to-end flow control vs network congestion control.",
            "TCP Advertised Window field in header blocks.",
            "Sender sliding window adjustments based on receiver buffers.",
            "Zero Window conditions and keep-alive probe packets.",
            "Silly Window Syndrome prevention using Nagle's algorithm."
        ],
        "sub-sliding-window": [
            "Sliding window boundaries (Send window, Receive window).",
            "Stop-and-Wait protocol inefficiency.",
            "Go-Back-N (GBN) retransmission rules on packet losses.",
            "Selective Repeat (SR) individual buffering and dedicated ACKs.",
            "Bandwidth-Delay Product (BDP) capacity scaling."
        ],
        "sub-congestion-control": [
            "Congestion triggers (buffer bloat, packet drops, high delays).",
            "Slow Start exponential cwnd expansion up to ssthresh.",
            "Congestion Avoidance linear AIMD growth rules.",
            "Fast Retransmit (3 duplicate ACKs) and Fast Recovery.",
            "Congestion algorithms comparisons (Tahoe, Reno, Cubic, BBR)."
        ],
        "sub-mac-address": [
            "48-bit hex layout (OUI vs NIC specific blocks).",
            "Unicast, Multicast, and Broadcast MAC targets.",
            "How switches learn MAC addresses in CAM tables.",
            "MAC flooding attacks and port security limits.",
            "MAC address randomization protocols on mobile devices."
        ],
        "sub-routing": [
            "Routing Tables: Destination prefix, next hop, egress interface.",
            "Longest Prefix Match (LPM) algorithm in hardware lookup tables.",
            "Static routing vs default routing (0.0.0.0/0).",
            "Administrative Distance (AD) and metric comparisons.",
            "IP Time-to-Live (TTL) decrementing and ICMP Time Exceeded packets."
        ],
        "sub-routing-protocols": [
            "Interior Gateway Protocols (IGP) vs Exterior Gateway Protocols (EGP).",
            "Distance Vector (RIP) hop count loops and split horizon rules.",
            "Link State (OSPF) Dijkstra calculation and link state databases.",
            "Path Vector (BGP) policy-based routing and TCP port 179 sessions.",
            "Fast convergence algorithms in routing fabrics."
        ],
        "sub-nat": [
            "Static NAT, Dynamic NAT, and Port Address Translation (PAT).",
            "NAT translation tables (Private IP + Port <=> Public IP + Port).",
            "NAT traversal techniques (STUN, TURN) for P2P connections.",
            "Hairpinning NAT local loopbacks.",
            "Double NAT routing issues and IPv6 native address paths."
        ],
        "sub-network-devices": [
            "Hubs, Switches, Routers, and Gateways.",
            "Collision domains vs broadcast domains boundaries.",
            "Half-duplex vs full-duplex CSMA/CD logic.",
            "Layer 3 switches vs Layer 7 load balancers.",
            "Software-Defined Networking (SDN) data plane vs control plane."
        ],
        "sub-switching": [
            "Store-and-forward vs cut-through vs fragment-free switching.",
            "VLAN tagging (802.1Q headers) and trunk port trunks.",
            "Spanning Tree Protocol (STP) loop prevention (blocking states).",
            "CAM table overflows and switch replication floods.",
            "Link Aggregation (LACP) bandwidth groupings."
        ],
        "sub-vpn": [
            "Tunneling concept (private packet inside public header).",
            "Site-to-Site vs Remote Access VPN structures.",
            "IPsec framework: AH (authentication) vs ESP (encryption).",
            "IKE (Internet Key Exchange) phases and security associations.",
            "TLS/SSL VPNs executing over web browser connections."
        ],
        "sub-firewalls": [
            "Stateless packet filtering (ACL rules checking).",
            "Stateful packet inspection (connection state tracking tables).",
            "Application-level gateway (proxy firewalls).",
            "Next-Generation Firewalls (NGFW) deep packet inspection.",
            "Egress filtering to prevent command and control callouts."
        ],
        "sub-ddos": [
            "DoS vs DDoS distributed attack architectures.",
            "Volumetric attacks (DNS Amplification, NTP Reflection).",
            "Protocol attacks (SYN floods, Ping of Death).",
            "Application layer attacks (HTTP GET/POST floods).",
            "Anycast routing mitigation and CDN edge absorption."
        ]
    }
    levels = depth_levels.get(tid, [
        "Core syntax and basic conceptual definitions.",
        "ISO model, TCP segments, or routing path algorithms.",
        "Multiplexing streams, TLS validation, or window adjustments.",
        "Congestion boundaries and load balancer operations.",
        "Enterprise global CDNs and Software-Defined Networks."
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

HIGH_YIELD_TOPICS = ["sub-osi", "sub-tcpip", "sub-tcp-udp", "sub-handshake", "sub-dns"]

# ─────────────────────────────────────────
# GENERATE_PAGE: 14-Section Template with 2x2 Bottom Grid
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
    space_filler = get_cn_space_filler(tid)
    industry_box = get_cn_industry_box(tid)
    depth_box = get_cn_depth_box(tid)
    left_col_updated = left_col + "\n" + industry_box + "\n" + depth_box
    
    # Extract Mistake from booster HTML using re
    import re
    booster_html = CN_BOOSTERS.get(tid, "")
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
        <div class="breadcrumb">GrindOS <span>›</span> CN <span>›</span> <span>{title}</span></div>
      </div>
      <div class="page-number-premium">
        {page_indicator}
      </div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# ROADMAP PAGE
# ─────────────────────────────────────────
roadmap_page = f"""
  <div class="page roadmap-page" id="cn-roadmap">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="header-badge" style="background: rgba(255,255,255,0.25);">CN ROADMAP</div>
      </div>
    </div>
    
    <div style="padding: 30px 40px; flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
      <div>
        <div style="font-size: 26pt; font-weight: 800; color: #111; margin-bottom: 8px;">Computer Networks Roadmap</div>
        <div style="font-size: 11pt; color: #EA763F; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px;">Placement Preparation Guide</div>
        
        <div style="background: #FFF5F0; border-left: 5px solid #EA763F; padding: 14px 20px; border-radius: 6px; margin-bottom: 25px;">
          <strong style="color: #EA763F; font-size: 11pt; display: block; margin-bottom: 6px;">How to use this Handbook:</strong>
          <p style="font-size: 9.5pt; color: #4A5568; line-height: 1.5;">Every single page covers exactly one critical core topic. Spend 2 minutes reading the <strong>Definition</strong> and <strong>Visual Diagram</strong> on the left, memorize the <strong>Model Answer</strong> and <strong>Buzzwords</strong> on the right, and review the <strong>Interviewer Trap</strong> to avoid falling into common placement traps.</p>
        </div>

        <div style="margin-top: 15px;">
          <div style="font-size: 12pt; font-weight: 800; color: #1A202C; margin-bottom: 12px; border-bottom: 2px solid #E2E8F0; padding-bottom: 6px;">🎯 Three-Phase Learning Plan</div>
          
          <div style="display: flex; gap: 15px; margin-bottom: 15px;">
            <div style="background: #EBF8FF; border: 1px solid #BEE3F8; border-radius: 8px; padding: 12px; flex: 1;">
              <span style="background: #3182CE; color: white; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 7.5pt; text-transform: uppercase;">Phase 1</span>
              <strong style="display: block; font-size: 9.5pt; margin-top: 6px; color: #2B6CB0;">Basics &amp; Models</strong>
              <p style="font-size: 8pt; color: #4A5568; margin-top: 4px;">Master OSI &amp; TCP/IP architectures, IP addressing schemas, and MAC mapping logic. (Topics 1 - 6)</p>
            </div>
            
            <div style="background: #F0FFF4; border: 1px solid #C6F6D5; border-radius: 8px; padding: 12px; flex: 1;">
              <span style="background: #38A169; color: white; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 7.5pt; text-transform: uppercase;">Phase 2</span>
              <strong style="display: block; font-size: 9.5pt; margin-top: 6px; color: #276749;">Transport &amp; App Core</strong>
              <p style="font-size: 8pt; color: #4A5568; margin-top: 4px;">Deep-dive into TCP state machines, sliding windows, congestion control algorithms, DNS, and HTTP headers. (Topics 7 - 15)</p>
            </div>
            
            <div style="background: #FFFFF0; border: 1px solid #FEFCBF; border-radius: 8px; padding: 12px; flex: 1;">
              <span style="background: #D69E2E; color: white; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 7.5pt; text-transform: uppercase;">Phase 3</span>
              <strong style="display: block; font-size: 9.5pt; margin-top: 6px; color: #B7791F;">Routing &amp; Security</strong>
              <p style="font-size: 8pt; color: #4A5568; margin-top: 4px;">Learn routing policies (BGP vs OSPF), NAT logic, stateful firewalls, VPN tunneling, and DDoS mitigations. (Topics 16 - 24)</p>
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
        <div class="breadcrumb">GrindOS <span>›</span> CN <span>›</span> <span>Roadmap</span></div>
      </div>
      <div class="page-number-premium">PAGE 02 / 34</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# DYNAMIC TABLE OF CONTENTS
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
  <div class="page toc-page" id="cn-toc">
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
        <div style="font-size: 9pt; color: #A0AEC0; font-weight: 600; margin-bottom: 12px;">Computer Networks · Placement Preparation Handbook</div>
        {toc_rows}
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> CN <span>›</span> <span>Index</span></div>
      </div>
      <div class="page-number-premium">PAGE 03 / 34</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# FINAL REVISION PAGE (Page 28)
# ─────────────────────────────────────────
final_revision_page = f"""
  <div class="page final-rev-page" id="cn-finalrev">
    <div class="header">
      <div class="header-left">
        <img class="header-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS Logo">
        <div class="header-wordmark">GrindOS</div>
      </div>
      <div class="header-right">
        <div class="badge-yield" style="background:#FFF5F0; color:#EA763F;">⚡ CRAM SHEET</div>
        <div class="header-badge">CN Final Revision</div>
      </div>
    </div>
    
    <div style="padding: 24px 30px; display: flex; flex-direction: column; gap: 14px; flex: 1;">
      <div style="text-align: center;">
        <div style="font-size: 20pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">CN Last-Minute Revision Sheet</div>
        <div style="font-size: 9.5pt; color: #EA763F; font-weight: 700; margin-top: 4px;">Top Formulas, Port Mappings, and High-Yield Summaries</div>
      </div>
      
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
        <div style="border: 1px solid #CBD5E0; border-radius: 8px; padding: 12px; background: white;">
          <strong style="color: #EA763F; font-size: 9pt; display: block; margin-bottom: 6px; border-bottom: 1.5px solid #EA763F; padding-bottom: 2px;">⚡ CRITICAL PORT NUMBERS</strong>
          <table style="width: 100%; font-size: 8pt; border-collapse: collapse;">
            <tr style="border-bottom: 1px solid #E2E8F0;"><td style="font-weight:bold; padding:3px 0;">DNS</td><td>Port 53 (UDP/TCP)</td></tr>
            <tr style="border-bottom: 1px solid #E2E8F0;"><td style="font-weight:bold; padding:3px 0;">HTTP / HTTPS</td><td>Port 80 / 443 (TCP)</td></tr>
            <tr style="border-bottom: 1px solid #E2E8F0;"><td style="font-weight:bold; padding:3px 0;">DHCP Server/Client</td><td>Port 67 / 68 (UDP)</td></tr>
            <tr style="border-bottom: 1px solid #E2E8F0;"><td style="font-weight:bold; padding:3px 0;">BGP / OSPF</td><td>Port 179 (TCP) / Prot. 89</td></tr>
            <tr style="border-bottom: 1px solid #E2E8F0;"><td style="font-weight:bold; padding:3px 0;">SSH / FTP</td><td>Port 22 / Port 20,21 (TCP)</td></tr>
          </table>
        </div>
        
        <div style="border: 1px solid #CBD5E0; border-radius: 8px; padding: 12px; background: white;">
          <strong style="color: #2B6CB0; font-size: 9pt; display: block; margin-bottom: 6px; border-bottom: 1.5px solid #2B6CB0; padding-bottom: 2px;">📏 FORMULAS &amp; METRICS</strong>
          <ul style="font-size: 8pt; list-style-type: square; padding-left: 14px; line-height: 1.4; color: #4A5568;">
            <li><strong>Usable Subnet Host IPs:</strong> <code>2^(32 - CIDR) - 2</code></li>
            <li><strong>IPv4 Address Size:</strong> 32 bits (4 Bytes)</li>
            <li><strong>IPv6 Address Size:</strong> 128 bits (16 Bytes)</li>
            <li><strong>Ethernet MAC Address Size:</strong> 48 bits (6 Bytes)</li>
            <li><strong>TCP Header Size:</strong> 20 bytes min, 60 bytes max</li>
            <li><strong>UDP Header Size:</strong> Fixed 8 bytes</li>
          </ul>
        </div>
      </div>
      
      <div style="border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px; background: #FEF8F4;">
        <strong style="color: #276749; font-size: 9.5pt; display: block; margin-bottom: 6px;">💡 TOP 5 INTERVIEW CONCEPTS TO RECALL</strong>
        <ol style="font-size: 8.5pt; padding-left: 18px; line-height: 1.5; color: #2D3748;">
          <li><strong>TCP Handshake:</strong> Client (SYN) → Server (SYN-ACK) → Client (ACK). Syncs sequence numbers bidirectionally.</li>
          <li><strong>IP vs MAC:</strong> IP is logical location routing context (rewritten nowhere). MAC is hop-by-hop physical link ID (rewritten at every router).</li>
          <li><strong>HoL Blocking:</strong> Solved in HTTP/3 by replacing TCP with UDP (QUIC), allowing packet losses to affect only one independent stream.</li>
          <li><strong>ARP Process:</strong> Broadcasts local ARP requests to map IP addresses to MAC physical card addresses, caching responses locally.</li>
          <li><strong>Stateful Firewalls:</strong> Inspect connection tables dynamically, allowing unsolicited response segments through otherwise closed ports.</li>
        </ol>
      </div>

      <div style="border: 1px dashed #EA763F; border-radius: 8px; padding: 12px; background: white; text-align: center;">
        <span style="font-size: 9pt; font-weight: 800; color: #EA763F; display: block; margin-bottom: 4px;">🎯 QUICK SELF-TEST CHECKLIST</span>
        <div style="display: flex; justify-content: center; gap: 20px; font-size: 8pt; color: #718096; font-weight: bold;">
          <span>[ ] Trace a packet's MAC changes</span>
          <span>[ ] Draw a TCP 3-way handshake</span>
          <span>[ ] Calculate a /27 subnet size</span>
        </div>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> CN <span>›</span> <span>Cheatsheet</span></div>
      </div>
      <div class="page-number-premium">PAGE 28 / 34</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# COMPARISON CHEAT SHEET PAGE (Page 29)
# ─────────────────────────────────────────
def generate_comparison_cheat_sheet(LOGO_BASE64):
    return f"""
  <div class="page" id="cn-cheatsheet-comparison">
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
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">CN Comparison Cheat Sheet</div>
        <div style="font-size: 9pt; color: #EA763F; font-weight: 700;">Quick Reference Contrast Tables for Fresher Interviews</div>
      </div>
      
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; flex: 1;">
        <!-- Left Column -->
        <div style="display: flex; flex-direction: column; gap: 8px;">
          <!-- TCP vs UDP -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 8px; background: white;">
            <div style="font-size: 8pt; font-weight: 800; color: #EA763F; border-bottom: 1.5px solid #EA763F; padding-bottom: 2px; margin-bottom: 4px; text-transform: uppercase;">TCP vs UDP</div>
            <table style="width: 100%; font-size: 7.2pt; border-collapse: collapse; text-align: left;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>TCP</th><th>UDP</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Connection</td><td>Connection-oriented</td><td>Connectionless</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Reliability</td><td>Guaranteed (Retransmission)</td><td>Best-effort (No ACK)</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Header Size</td><td>20 - 60 Bytes</td><td>8 Bytes</td></tr>
              <tr><td>Ordering</td><td>Strict in-order delivery</td><td>Out-of-order allowed</td></tr>
            </table>
          </div>
          
          <!-- HTTP vs HTTPS -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 8px; background: white;">
            <div style="font-size: 8pt; font-weight: 800; color: #2B6CB0; border-bottom: 1.5px solid #2B6CB0; padding-bottom: 2px; margin-bottom: 4px; text-transform: uppercase;">HTTP vs HTTPS</div>
            <table style="width: 100%; font-size: 7.2pt; border-collapse: collapse; text-align: left;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>HTTP</th><th>HTTPS</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Encryption</td><td>Plaintext (None)</td><td>SSL/TLS Encrypted</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Port</td><td>Port 80</td><td>Port 443</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Overhead</td><td>Low latency (No handshake)</td><td>Higher (TLS handshake)</td></tr>
              <tr><td>Security</td><td>Vulnerable to MitM</td><td>Protected from sniffing</td></tr>
            </table>
          </div>

          <!-- IPv4 vs IPv6 -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 8px; background: white;">
            <div style="font-size: 8pt; font-weight: 800; color: #276749; border-bottom: 1.5px solid #276749; padding-bottom: 2px; margin-bottom: 4px; text-transform: uppercase;">IPv4 vs IPv6</div>
            <table style="width: 100%; font-size: 7.2pt; border-collapse: collapse; text-align: left;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>IPv4</th><th>IPv6</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Address Size</td><td>32-bit (4 Bytes)</td><td>128-bit (16 Bytes)</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Notation</td><td>Dotted decimal (e.g. 192.168.1.1)</td><td>Hexadecimal colon (e.g. 2001::1)</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Header</td><td>Variable (20-60 Bytes)</td><td>Fixed (40 Bytes)</td></tr>
              <tr><td>Security</td><td>IPsec optional</td><td>IPsec native/mandatory</td></tr>
            </table>
          </div>

          <!-- MAC vs IP -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 8px; background: white;">
            <div style="font-size: 8pt; font-weight: 800; color: #4A5568; border-bottom: 1.5px solid #4A5568; padding-bottom: 2px; margin-bottom: 4px; text-transform: uppercase;">MAC vs IP</div>
            <table style="width: 100%; font-size: 7.2pt; border-collapse: collapse; text-align: left;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>MAC Address</th><th>IP Address</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Layer</td><td>Layer 2 (Data Link)</td><td>Layer 3 (Network)</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Assignment</td><td>Physical (NIC manufacturer)</td><td>Logical (DHCP/Admin)</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Scope</td><td>Local network delivery</td><td>Global internet routing</td></tr>
              <tr><td>Transit Change</td><td>Rewritten at every router</td><td>Unchanged end-to-end</td></tr>
            </table>
          </div>
        </div>
        
        <!-- Right Column -->
        <div style="display: flex; flex-direction: column; gap: 8px;">
          <!-- Router vs Switch -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 8px; background: white;">
            <div style="font-size: 8pt; font-weight: 800; color: #7B341E; border-bottom: 1.5px solid #7B341E; padding-bottom: 2px; margin-bottom: 4px; text-transform: uppercase;">Router vs Switch</div>
            <table style="width: 100%; font-size: 7.2pt; border-collapse: collapse; text-align: left;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Router</th><th>Switch</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>OSI Layer</td><td>Layer 3 (Network)</td><td>Layer 2 (Data Link)</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Address Used</td><td>IP Address</td><td>MAC Address</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Traffic Scope</td><td>Connects different subnets</td><td>Connects hosts in same subnet</td></tr>
              <tr><td>Table Type</td><td>Routing Table</td><td>MAC Address Table</td></tr>
            </table>
          </div>

          <!-- Hub vs Switch -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 8px; background: white;">
            <div style="font-size: 8pt; font-weight: 800; color: #6B46C1; border-bottom: 1.5px solid #6B46C1; padding-bottom: 2px; margin-bottom: 4px; text-transform: uppercase;">Hub vs Switch</div>
            <table style="width: 100%; font-size: 7.2pt; border-collapse: collapse; text-align: left;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Hub</th><th>Switch</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Layer</td><td>Layer 1 (Physical)</td><td>Layer 2 (Data Link)</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Forwarding</td><td>Broadcasts to all ports</td><td>Unicasts to targeted port</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Collision Domain</td><td>Single shared domain</td><td>Separate per port</td></tr>
              <tr><td>Transmission</td><td>Half-duplex (slow)</td><td>Full-duplex (fast)</td></tr>
            </table>
          </div>

          <!-- Flow Control vs Congestion Control -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 8px; background: white;">
            <div style="font-size: 8pt; font-weight: 800; color: #319795; border-bottom: 1.5px solid #319795; padding-bottom: 2px; margin-bottom: 4px; text-transform: uppercase;">Flow vs Congestion Control</div>
            <table style="width: 100%; font-size: 7.2pt; border-collapse: collapse; text-align: left;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Flow Control</th><th>Congestion Control</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Scope</td><td>End-to-end (Sender to Receiver)</td><td>Network-wide (Routers/Links)</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Trigger</td><td>Receiver buffer full</td><td>Transit link capacity overload</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Feedback</td><td>Receiver advertised window field</td><td>Packet loss (timeouts / triple ACKs)</td></tr>
              <tr><td>Mechanisms</td><td>Sliding Window</td><td>Slow Start, AIMD, Fast Recovery</td></tr>
            </table>
          </div>

          <!-- Proxy vs Reverse Proxy -->
          <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 6px 8px; background: white;">
            <div style="font-size: 8pt; font-weight: 800; color: #553C9A; border-bottom: 1.5px solid #553C9A; padding-bottom: 2px; margin-bottom: 4px; text-transform: uppercase;">Proxy vs Reverse Proxy</div>
            <table style="width: 100%; font-size: 7.2pt; border-collapse: collapse; text-align: left;">
              <tr style="border-bottom: 1px solid #E2E8F0; font-weight: bold; background: #F7FAFC;"><th>Feature</th><th>Forward Proxy</th><th>Reverse Proxy</th></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Protects</td><td>Clients (private LAN)</td><td>Servers (backend pool)</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Visibility</td><td>Client aware; Server doesn't see</td><td>Client unaware; sees Proxy IP</td></tr>
              <tr style="border-bottom: 1px solid #E2E8F0;"><td>Use Case</td><td>Bypassing blocks, egress filter</td><td>Load balancing, SSL termination</td></tr>
              <tr><td>Direction</td><td>Outbound requests</td><td>Inbound requests</td></tr>
            </table>
          </div>
        </div>
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> CN <span>›</span> <span>Comparisons</span> <span style="font-size:7.5pt; color:#A0AEC0; font-weight:normal; margin-left:10px;">Created by Pranav Gawai</span></div>
      </div>
      <div class="page-number-premium">PAGE 29 / 34</div>
    </div>
  </div>
  """

# ─────────────────────────────────────────
# EXPECTED Q&A GENERATION (Pages 30-31)
# ─────────────────────────────────────────
def generate_expected_qa_pages_new(LOGO_BASE64):
    qas = [
        {
            "q": "What happens when you type 'google.com' in your browser and press Enter?",
            "a": "First, the browser needs the server's IP address, so it checks local caches like the browser, OS, and router cache. If not found, it queries the DNS resolver, which recursively asks Root, TLD, and Authoritative DNS servers to get the IP. Once the IP is resolved, the browser initiates a TCP 3-way handshake to establish a reliable connection. After that, since it's HTTPS, a SSL/TLS handshake occurs to validate the certificate and generate symmetric session keys. The browser then sends an HTTP GET request, the web server processes it and returns an HTTP 200 response with the HTML/CSS files, and finally the browser's rendering engine parses the documents and displays the visual page.",
            "keywords": ["DNS Resolution", "TCP Handshake", "SSL/TLS Session Keys", "HTTP GET", "Browser Rendering"],
            "followups": "How does DNS caching work? What is SNI in TLS?",
            "mistake": "Skipping the TCP/TLS handshakes and saying the HTTP request goes out immediately after DNS resolution.",
            "depth": "Must explain the sequence of handshakes. Senior candidates should details browser layout tree generation."
        },
        {
            "q": "Why does TCP use a 3-way handshake to establish a connection? Why isn't a 2-way handshake sufficient?",
            "a": "TCP uses a 3-way handshake to synchronize initial sequence numbers bidirectionally and verify that both the client and server can send and receive data before any application payload is sent. The client sends a SYN, the server responds with SYN-ACK, and the client sends a final ACK. A 2-way handshake is insufficient because it doesn't prevent duplicate historical connections. For example, if a client sends a SYN packet that is delayed in the network, the client might timeout and open a connection via a second SYN. If the delayed SYN finally reaches the server later, a 2-way handshake would force the server to establish a second active connection, wasting resources because the server cannot verify if the client is actually alive and listening.",
            "keywords": ["Bidirectional Synchronization", "Sequence Numbers", "Half-Open Connection", "Resource Exhaustion"],
            "followups": "What is a SYN flood attack? How does TCP close a connection?",
            "mistake": "Claiming that the 3-way handshake is strictly for security. It is actually for reliability and state synchronization.",
            "depth": "Understand how SYN cookies protect against SYN floods during handshake stages."
        },
        {
            "q": "As an IP packet travels from a source laptop to a web server across multiple routers, how do its MAC addresses and IP addresses change?",
            "a": "The source and destination IP addresses remain completely constant and unchanged end-to-end, since they represent the global logical source and destination of the packet. However, the source and destination MAC addresses are rewritten hop-by-hop at every single router interface. When the packet moves from one physical link to another, the router decapsulates the Layer 2 Ethernet frame, reads the Layer 3 IP header to make a routing decision, and then re-encapsulates the packet into a new frame with the router's egress port MAC as the source and the next-hop router's ingress MAC as the destination.",
            "keywords": ["End-to-End Constant", "Hop-by-Hop Rewrite", "Frame Decapsulation", "MAC Routing Boundary"],
            "followups": "What is ARP spoofing? What happens if a router has no route for a destination IP?",
            "mistake": "Saying that IP addresses are rewritten at each hop. They are only rewritten if NAT is active at a boundary.",
            "depth": "Differentiate Layer 2 local switching from Layer 3 routed network domains."
        },
        {
            "q": "What is Head-of-Line (HoL) blocking in TCP, and how does HTTP/3 solve it using QUIC over UDP?",
            "a": "In TCP, data is delivered as a single ordered byte stream. In HTTP/2, we multiplexed multiple request streams over that single TCP connection. However, if one TCP packet is dropped in transit, TCP pauses the entire connection, halting all streams until that lost packet is retransmitted. This is Head-of-Line blocking. HTTP/3 solves this by replacing TCP with QUIC, which runs on UDP. QUIC implements packet recovery and connection state in user space and treats each stream as completely independent. If a packet on Stream A is dropped, QUIC continues to deliver packets for Stream B and C to the browser immediately, completely eliminating connection-level HoL blocking.",
            "keywords": ["Multiplexed Streams", "Ordered Byte Stream", "QUIC UDP Foundation", "Stream Independence", "Connection Migration"],
            "followups": "Why does QUIC run in user space instead of kernel space? What is 0-RTT connection setup?",
            "mistake": "Saying HTTP/3 is unreliable because it runs over UDP. QUIC handles packet recovery and congestion control, not UDP.",
            "depth": "Explain how connection migration uses connection IDs rather than IP/Ports to maintain sessions during network shifts."
        }
    ]
    
    p1_html = f"""
  <div class="page" id="cn-expectedqa-new-1">
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
        <div class="breadcrumb">GrindOS <span>›</span> CN <span>›</span> <span>Expected Q&amp;A</span></div>
      </div>
      <div class="page-number-premium">PAGE 30 / 34</div>
    </div>
  </div>
  """
  
    p2_html = f"""
  <div class="page" id="cn-expectedqa-new-2">
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
        <div class="breadcrumb">GrindOS <span>›</span> CN <span>›</span> <span>Expected Q&amp;A</span></div>
      </div>
      <div class="page-number-premium">PAGE 31 / 34</div>
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
# RAPID FIRE QUESTIONS PAGE (Page 32)
# ─────────────────────────────────────────
def generate_rapid_fire_page(LOGO_BASE64):
    qas = [
        ("What port does DNS use?", "Port 53 (UDP for queries, TCP for large responses)."),
        ("What is the size of an IPv6 address?", "128 bits (16 bytes), written in 8 hex groups."),
        ("Which protocol runs traceroute?", "ICMP (via TTL decrementing at each hop)."),
        ("What is the DORA process in DHCP?", "Discover, Offer, Request, Acknowledge."),
        ("What is loopback for IPv4/IPv6?", "IPv4: 127.0.0.1; IPv6: ::1 (localhost)."),
        ("What port does HTTPS run on?", "Port 443 (HTTP runs on Port 80)."),
        ("Usable hosts in a /28 subnet?", "2^(32-28) - 2 = 16 - 2 = 14 usable host IPs."),
        ("What is the Transport Layer PDU?", "Segment (for TCP) or Datagram (for UDP)."),
        ("Size of an Ethernet MAC address?", "48 bits (6 bytes), physical hardware identifier."),
        ("What port does BGP use?", "TCP Port 179 (OSPF uses IP Protocol 89)."),
        ("What is PAT in network routing?", "Port Address Translation; maps many private IPs to one public IP via ports."),
        ("What is a default gateway?", "The router port IP that routes local subnet traffic to external networks.")
    ]
    
    left_col_cards = "".join([render_rapid_card(q, a) for q, a in qas[:6]])
    right_col_cards = "".join([render_rapid_card(q, a) for q, a in qas[6:]])
    
    return f"""
  <div class="page" id="cn-rapidfire-page">
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
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">CN Rapid Fire Questions</div>
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
        <div class="breadcrumb">GrindOS <span>›</span> CN <span>›</span> <span>Rapid Fire</span></div>
      </div>
      <div class="page-number-premium">PAGE 32 / 34</div>
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
# COMMON TRAPS PAGE (Page 33)
# ─────────────────────────────────────────
def generate_common_traps_page(LOGO_BASE64):
    traps = [
        {
            "title": "Trap 1: The UDP 'Insecure' Accusation",
            "question": "\"Since UDP doesn't establish a connection and has no handshakes, does that mean it is unsafe and insecure to use?\"",
            "intercept": "Explain that 'reliability' and 'security' are separate concerns. UDP is connectionless and unreliable (no delivery checks), but security (encryption/auth) is handled at the application layer (e.g., using DTLS or custom payload encryption). UDP is optimal for gaming and VoIP where speed is paramount."
        },
        {
            "title": "Trap 2: The HTTPS Header Encryption Illusion",
            "question": "\"Does HTTPS encrypt the source and destination IP addresses to protect user identity?\"",
            "intercept": "State clearly that HTTPS (via TLS) only encrypts the Layer 7 Application payload and headers (like URLs and cookies). The Layer 3 IP header and Layer 4 TCP header must remain in plaintext. If they were encrypted, intermediate routers could not route the packet and firewalls could not track ports."
        },
        {
            "title": "Trap 3: The DNS Protocol Exclusivity",
            "question": "\"Is it true that DNS queries run exclusively on UDP?\"",
            "intercept": "Clarify that DNS uses UDP Port 53 for standard name queries because it is fast and lightweight. However, DNS falls back to TCP Port 53 if the response payload exceeds 512 bytes, during zone transfers between primary and secondary nameservers, or when using DNSSEC."
        },
        {
            "title": "Trap 4: Public Routing of RFC 1918 Private IPs",
            "question": "\"What happens if a router on the public internet receives a packet with a destination IP of 192.168.1.50?\"",
            "intercept": "State that public internet routers are configured by standard policies to drop RFC 1918 private addresses immediately. Private IPs are non-routable on the public WAN and must go through Network Address Translation (NAT) to map to a valid public IP before leaving the local gateway."
        },
        {
            "title": "Trap 5: The Handshake Step Redundancy",
            "question": "\"Why don't we use a 4-way handshake to establish a TCP connection for extra validation?\"",
            "intercept": "Explain that a 3-way handshake is the mathematical minimum required to synchronize initial sequence numbers (ISNs) bidirectionally. A 4th packet would simply be a redundant ACK, adding network round-trip latency without providing any new connection state verification."
        }
    ]
    
    rows = ""
    for item in traps:
        rows += f"""
        <div style="border: 1px solid #CBD5E0; border-radius: 6px; padding: 8px 10px; background: white; margin-bottom: 6px;">
          <div style="font-weight: 800; font-size: 8.5pt; color: #C53030; margin-bottom: 2px;">{item['title']}</div>
          <div style="font-size: 7.5pt; font-style: italic; color: #4A5568; margin-bottom: 4px;">Interviewer: {item['question']}</div>
          <div style="font-size: 7.5pt; color: #2D3748; line-height: 1.35; border-left: 2px solid #E53E3E; padding-left: 6px;">
            <strong>Deflection:</strong> {item['intercept']}
          </div>
        </div>
        """
        
    return f"""
  <div class="page" id="cn-commontraps-page">
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
        <div style="font-size: 18pt; font-weight: 800; color: #111; letter-spacing: -0.5px;">CN Common Traps &amp; Deflections</div>
        <div style="font-size: 9pt; color: #C53030; font-weight: 700;">Tactics to Evade Trick Interview Questions with Confident Answers</div>
      </div>
      
      <div style="display: flex; flex-direction: column; gap: 2px;">
        {rows}
      </div>
    </div>
    
    <div class="footer">
      <div class="footer-left">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_BASE64}" alt="Logo">
        <div class="breadcrumb">GrindOS <span>›</span> CN <span>›</span> <span>Traps</span></div>
      </div>
      <div class="page-number-premium">PAGE 33 / 34</div>
    </div>
  </div>
  """

# ─────────────────────────────────────────
# BLANK NOTES PAGES (Page 34)
# ─────────────────────────────────────────
blank_notes_pages = f"""
  <div class="page" id="cn-notes-1">
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
        <div class="breadcrumb">GrindOS <span>›</span> CN <span>›</span> <span>Notes</span> <span style="font-size:7.5pt; color:#A0AEC0; font-weight:normal; margin-left:10px;">grindos.pranavx.in</span></div>
      </div>
      <div class="page-number-premium">PAGE 34 / 34</div>
    </div>
  </div>
"""

# ─────────────────────────────────────────
# COMPILING HTML PAGES
# ─────────────────────────────────────────
total_content_pages = len(topics)
# Total pages: Cover(1), Roadmap(1), TOC(1), Content(24), Cram(1), Comparison(1), ExpectedQA(2), RapidFire(1), Traps(1), Notes(1) = 34
content_pages_html = "".join([generate_page(t, i+4, 34) for i, t in enumerate(topics)])
expected_qa_html = generate_expected_qa_pages_new(LOGO_BASE64)
comparison_cheat_sheet_html = generate_comparison_cheat_sheet(LOGO_BASE64)
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
  .box-scenario {{ border-left: 4px solid #805AD5; background: #F5EBFE; }}
  .box-scenario .box-title {{ color: #805AD5; }}
  .box-comparison {{ border-left: 4px solid #319795; background: #E6FFFA; }}
  .box-comparison .box-title {{ color: #319795; }}
  
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

  /* BOTTOM PLACEMENT GRID (L4) */
  .bottom-placement-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 6px;
    padding: 6px 12px;
    background: #FDFBF7;
    border-top: 2px solid #EBE5DB;
    flex-shrink: 0;
    min-height: 120px;
    max-height: 135px;
    margin-left: 5mm;
    margin-right: 5mm;
  }}
  .placement-block {{
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 7.5pt;
    line-height: 1.25;
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

  /* FOOTER WITH PREMIUM PAGE NUMBERS */
  .footer {{ height: 36px; background: white; border-top: 1px solid #EDE5D8; display: flex; justify-content: space-between; align-items: center; padding: 0 24px; font-size: 8.5pt; color: #718096; flex-shrink: 0; font-weight: 700; margin-bottom: 5mm; margin-left: 5mm; margin-right: 5mm; }}
  .footer-left {{ display: flex; align-items: center; gap: 8px; }}
  .footer-logo {{ height: 14px; }}
  .breadcrumb {{ color: #A0AEC0; }}
  .breadcrumb span {{ color: #4A5568; font-weight: 800; margin: 0 4px; }}
  .page-number-premium {{ font-size: 8.5pt; font-weight: 800; color: #EA763F; letter-spacing: 1px; background: #FFF5F0; padding: 3px 10px; border-radius: 4px; border: 1px solid #FBD38D; }}
"""

# Compile final template
html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CN Placement Handbook</title>
<style>{css}</style>
</head>
<body>
  <!-- COVER PAGE -->
  <div class="page cover-page" id="cn-cover">
    <div class="cover-logo-container">
      <img src="data:image/png;base64,{LOGO_BASE64}" alt="GrindOS">
    </div>
    <div class="cover-eyebrow">Core Computer Science</div>
    <div class="cover-title">Computer<br>Networks</div>
    <div class="cover-subtitle">Placement Preparation Handbook</div>
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
os.makedirs("subjects/cn", exist_ok=True)
output_path = "subjects/cn/01_networking.html"
with open(output_path, "w") as f:
    f.write(html_out)

print(f"Generated complete Computer Networks Handbook with {len(topics)} topics.")


