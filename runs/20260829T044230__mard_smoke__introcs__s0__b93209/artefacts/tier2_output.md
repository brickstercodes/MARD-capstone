Data vs. Information
- Data: raw symbols, signals, or measurements — bytes in memory, pixels in a file, numbers on a sheet. Data by itself is uninterpreted.
- Information: data given structure and meaning so it answers a question or conveys knowledge. Information is what results when a user, program, or protocol maps data to concepts (e.g., “the temperature is 22°C”, “this image shows a cat”).

Why representation matters for computation
Representation is how we turn information into data that computers can store and manipulate. Three aspects matter:

1. Encoding — how values are mapped to bit patterns
   - Examples: ASCII and Unicode map characters to numbers; IEEE 754 maps real numbers to bit patterns.
   - Why it matters: encoding determines what values can be represented, how many bits are needed, and whether conversion is needed between systems.

2. Structure — how encoded values are organized
   - Examples: sequences (arrays), key–value records (dictionaries), linked lists, trees, or relations (tables).
   - Why it matters: structure affects how easily and efficiently programs can find, update, or traverse information.

3. Meaning (semantics) — the interpretation rules and type information
   - Examples: interpreting the bit pattern 0x41 as the character 'A' vs. the number 65; tagging data with a type (integer vs. string).
   - Why it matters: semantics prevent misinterpretation, guide valid operations, and enable correct program behavior.

Concrete examples of different representations and their tradeoffs

1. Text: ASCII vs. Unicode vs. UTF-8
   - Same information: the characters of a document.
   - Tradeoffs:
     - ASCII: fixed 7-bit/8-bit mapping, compact for English but cannot represent non‑Latin scripts.
     - Unicode (code points): can represent virtually all scripts and emojis, but storing as fixed-width 32-bit units wastes space.
     - UTF-8: variable-length byte encoding that is compact for ASCII and supports all Unicode; decoding and indexing by character are more complex.
   - Impact: interoperability, file size, ease of substring/index operations.

2. Numbers: integer vs. floating-point vs. rational
   - Same information goal: represent a numeric quantity.
   - Tradeoffs:
     - Integer: exact for whole numbers, efficient, limited range.
     - Floating-point (IEEE 754): can represent very large and very small values, supports fractional numbers, but introduces rounding errors and special values (NaN, infinities).
     - Rational (pair of integers): exact fractional values, but arithmetic can be slower and numerator/denominator can grow large.
   - Impact: correctness (exactness), performance, memory use.

3. Images: bitmapped (raster) vs. vector
   - Same information: a visual picture (e.g., a logo).
   - Tradeoffs:
     - Raster: represents every pixel; simple to display and manipulate at pixel level, but scaling loses quality and files can be large at high resolution.
     - Vector: represents shapes and instructions; scales without loss, often smaller for diagrams, but complex photographic detail is hard to represent and rendering can be more costly.
   - Impact: scalability, editability, storage size, rendering complexity.

4. Dates/times: human-readable strings vs. epoch timestamps vs. structured objects
   - Same information: a moment in time.
   - Tradeoffs:
     - String (“March 5, 2026 10:00”): readable but ambiguous (time zone, format).
     - Epoch seconds (integer): compact, unambiguous for computation, but not human-friendly.
     - Structured object (year, month, day, tz): expressive and precise but larger and needs libraries for operations.
   - Impact: ease of parsing, arithmetic, sorting, and user display.

5. Storage vs. compressed formats
   - Same information: a file’s contents.
   - Tradeoffs:
     - Uncompressed: faster to read/write and edit in place.
     - Compressed (lossless): smaller on disk and over the network, but requires CPU to compress/decompress; random access may be harder.
     - Compressed (lossy, e.g., JPEG): much smaller, but some information is irretrievably lost.
   - Impact: bandwidth, storage cost, processing time, fidelity.

Key tradeoff themes to remember
- Precision vs. size: more precise or expressive representations usually require more bits.
- Speed vs. space: compact encodings save storage/bandwidth but may cost CPU time to encode/decode.
- Simplicity vs. generality: simple representations are fast and easy to reason about but may not support all needed values or locales.
- Lossless vs. lossy: lossy formats save resources but destroy information needed for some tasks.
- Interoperability vs. specialization: standard encodings and types make sharing easier; specialized encodings can be optimal for a narrow purpose.

Bottom line
Choosing a representation is a design decision that affects correctness, performance, storage, and how easily other programs or people can use the data. Good software design makes the intended meaning explicit (types, metadata, formats) and selects encodings and structures that match the needs of the computation.

Computation and Algorithms

Computation is the process of transforming input data into output results by carrying out well-defined steps. In computer science, those steps must be precise enough that a machine (a CPU running a program) can follow them without needing human interpretation. An algorithm is a recipe for computation: a finite, unambiguous sequence of instructions that, when executed, produces the desired output from the given input.

Key properties of algorithms
- Finite: The algorithm must terminate after a finite number of steps (unless it is intentionally designed to run forever).
- Unambiguous: Each step must be precisely specified so a machine can perform it.
- Executable: Steps must be basic enough that the machine can carry them out (arithmetic, comparisons, assignments, loops, etc.).
- Input and output: An algorithm clearly identifies what it takes in and what it produces.

Example algorithm: compute the average of a list of numbers
Goal: Given several numbers, compute their arithmetic mean.

Inputs:
- A list of n numbers, nums = [x1, x2, ..., xn] (n > 0).

Output:
- A single number avg = (x1 + x2 + ... + xn) / n.

Step-by-step procedure (imperative style):
1. Let total ← 0.
2. Let count ← n (the number of elements in nums).
3. For each element x in nums, do:
   a. total ← total + x
4. avg ← total / count
5. Return avg.

Notes about this algorithm:
- It is finite: the loop runs exactly n times and then stops.
- It is unambiguous: each step describes a clear arithmetic or control operation.
- It is executable: a machine can implement the loop, additions, and division.
- Edge case: if count = 0 the algorithm must be adjusted (e.g., report an error or define behavior).

Alternative example: find the maximum element in a list
Inputs:
- A non-empty list nums = [x1, x2, ..., xn].

Output:
- maxValue, the largest element in nums.

Procedure:
1. Let maxValue ← x1.
2. For i from 2 to n:
   a. If xi > maxValue then maxValue ← xi.
3. Return maxValue.

This demonstrates the same algorithmic principles: defined inputs/outputs, a clear finite sequence of operations, and steps simple enough for a machine to execute.

Together, these ideas show how an abstract problem (“compute an average” or “find a maximum”) becomes a concrete, machine-executable sequence of operations via an algorithm.

Section 3 — Abstraction and Modeling

Core idea
- Abstraction is the practice of hiding irrelevant detail so you can manage complexity. You build a model that captures only what matters for the task at hand.
- A model is a simplified representation of reality that makes reasoning, communication, and computation easier. Different tasks call for different models of the same real-world situation.

Why hiding detail matters
- Real systems are complex: they contain many interacting parts and noisy information. If you tried to include every detail, solutions become huge, slow, fragile, and hard to understand.
- By removing or hiding details that don’t affect the task, you reduce cognitive load and you expose the structure you need to design algorithms and data structures.
- Good abstractions make the remaining relevant properties explicit and stable, so you can reason about behavior and prove correctness or performance.

Same problem, different abstraction levels — examples

1) Route planning
- High-level model: the road network is a graph of cities connected by roads; edge weights are travel time. Task: find the fastest route between city A and city B.
  - Effects on design: algorithms like Dijkstra or A* on graphs, store only nodes and weighted edges, ignore turn-by-turn instructions or traffic lights.
- Low-level model: the environment is a continuous geometry with lanes, traffic signals, and other vehicles; vehicle dynamics constrain acceleration and turning.
  - Effects on design: motion planning algorithms, control theory, real-time sensing, collision avoidance. Data structures store geometry, velocities, and sensor inputs.
- Consequence: a high-level planner can give a route quickly but can’t be executed directly by an autonomous car; a low-level planner can produce drivable trajectories but is much more computationally expensive and must handle noisy input.

2) Email sorting
- Abstract model: each message is represented by features (sender, keywords, date) and a label (spam or not). Task: classify messages.
  - Effects on design: use supervised machine learning, feature vectors, training and testing datasets, evaluation metrics (accuracy, precision).
- Detailed model: include raw MIME structure, embedded images, scripts, encoding quirks, and timing of arrival.
  - Effects on design: need robust parsers, security checks, spam heuristics for attachments and embedded content. Performance and safety concerns become central.
- Consequence: the abstract classifier is useful for batch sorting, but a production mail server must combine abstract classification with detailed parsing and security handling.

3) Image representation
- Pixel-level model: an image is a grid of color values. Task: detect whether an image contains a cat.
  - Effects on design: convolutional neural networks, large numeric arrays, heavy computation on pixels.
- Object-level model: an image is a collection of objects with positions, shapes, and labels.
  - Effects on design: symbolic reasoning, object detection outputs, simpler logic for queries like “is there a cat?”
- Consequence: pixel models are powerful for raw perception; object models are easier for reasoning and composing with other modules (e.g., “move cat to left”).

How abstraction choice affects solution design
- Algorithms: different abstractions demand different algorithms. Graph search vs. control algorithms; statistical classifiers vs. symbolic rule systems.
- Data structures: the model determines what you store. Lists of nodes and edges, feature vectors, sensor streams, or geometric maps lead to different memory and access patterns.
- Correctness and guarantees: some abstractions let you prove strong guarantees (shortest path in a weighted graph), others only give probabilistic assurances (machine-learned classifiers).
- Performance and resources: simpler models can be computed faster and require less memory; richer models usually demand more compute and real-time handling.
- Interfaces and modularity: good abstractions produce clean interfaces between components (planner vs controller, perception vs reasoning), enabling separation of concerns and easier testing.
- Robustness and assumptions: every abstraction hides assumptions. If the hidden details change (e.g., sudden traffic, corrupted email MIME), the solution may fail unless the system updates the model or handles exceptions.

Choosing the right abstraction
- Start from the task: identify which aspects of reality actually affect the task’s success.
- Ask what you need to guarantee (correctness, speed, safety) and choose a model that supports those guarantees without unnecessary complexity.
- Use layered abstractions: separate high-level reasoning (fast, coarse) from low-level execution (slow, detailed). Define clear interfaces so higher layers don’t need low-level complexity.
- Be prepared to refine the model: when failures occur, either add detail where it matters or isolate exceptional cases rather than globally complicating the model.

Takeaway
Abstraction and modeling are about deliberately hiding detail to make problems tractable. The same real-world problem can and should be modeled at multiple levels; the chosen level directly shapes algorithms, data structures, guarantees, and system architecture. Good design selects the simplest model that captures what matters for the task and composes models in layers when both speed and fidelity are required.

Computer Systems and Architecture (hardware–software stack)

What the stack is
- Hardware: the physical components — CPU(s), main memory (RAM), caches, system bus, persistent storage (HDD/SSD), I/O devices (keyboard, display, network, sensors), and circuitry that connects them.
- Operating system (OS): software that manages hardware resources and provides abstractions to programs — process scheduling, memory management (virtual memory), file systems, device drivers, and system-call interfaces.
- Applications (user programs): the code you write or run — compiled binaries, interpreters, or virtual-machine programs that request services from the OS and are executed on the CPU.

How they cooperate to execute programs (high-level flow)
1. Development/translation:
   - Source code is written, then translated to machine code (compiler) or bytecode (interpreter/VM). The result is an executable representation the OS and hardware can run.
2. Loading and starting:
   - The OS loader places the program into memory, sets up an initial process control block, and asks the scheduler to run it.
3. Scheduling and execution:
   - The OS scheduler gives the CPU time slices to run processes/threads. The CPU executes instructions via the fetch–decode–execute cycle.
4. Memory management:
   - The OS and hardware cooperate (MMU, page tables) to provide virtual memory: each process sees its own address space; physical memory is allocated and swapped as needed.
5. I/O and devices:
   - Applications request I/O through system calls. Device drivers translate these calls into device-specific operations. I/O may be synchronous or asynchronous; interrupts and DMA are used so the CPU isn’t blocked waiting for slow devices.
6. Interrupts and exceptions:
   - Hardware interrupts (I/O, timers) or exceptions (page faults, illegal instructions) transfer control to the OS to handle events, possibly causing context switches or I/O completion.
7. Termination and cleanup:
   - The OS reclaims resources (memory, file descriptors) when a program exits.

Key abstractions that matter
- Instruction Set Architecture (ISA): defines the instructions the CPU executes.
- System calls: controlled entry points for programs to request OS services.
- Virtual memory and paging: give the illusion of large, uniform memory, isolate processes, but introduce page-fault overhead.
- Files and streams: uniform abstraction for persistent data and many I/O devices.

How system design choices constrain or enable algorithms

Memory-related design choices
- RAM size and latency:
  - If data fits in RAM, algorithms that assume random access are feasible; if not, algorithms must use external-memory techniques (streaming, sorting by merging).
- Cache hierarchy and locality:
  - Caches reward spatial and temporal locality. Cache-aware or cache-oblivious algorithms (e.g., blocking for matrix multiply, tiling) run much faster than naive ones on modern machines.
- Virtual memory/page size:
  - Page faults are expensive; working sets larger than physical memory cause thrashing. Algorithms should strive for locality to reduce page faults.

Processing-related design choices
- Single vs multi-core/parallel CPUs:
  - Single-threaded algorithms can’t exploit multiple cores. Parallel algorithms, synchronized with locks or lock-free techniques, are required to scale; they must manage contention and coordination overhead.
- Vector/SIMD instructions and GPUs:
  - Data-parallel operations (SIMD) or massively parallel GPUs enable huge speedups for regular, parallelizable tasks (image processing, linear algebra) but require rethinking algorithms to expose parallelism and data layout.
- CPU frequency and pipeline depth:
  - Deep pipelines and out-of-order execution favor predictable control flow and data dependencies; branch-heavy code may suffer.

I/O-related design choices
- Bandwidth vs latency:
  - High bandwidth but high-latency channels (e.g., disks, networks) make throughput-oriented algorithms (batching, pipelining) preferable. Low-latency I/O is essential for interactive and real-time systems.
- Sequential vs random-access storage:
  - Disks historically favored sequential access; SSDs reduce this constraint but still have different performance characteristics. External algorithms (e.g., external merge sort) exploit sequential reads/writes.
- Network topology and reliability:
  - Distributed algorithms must handle latency, partial failures, and limited bandwidth. Consistency, replication, and fault-tolerance choices affect algorithm design (consensus, eventual consistency).

Other constraints and enabling factors
- Power and energy:
  - Mobile or embedded systems may limit computation and favor energy-efficient algorithms or approximate computing.
- Real-time constraints:
  - Hard real-time systems require predictable worst-case execution times (WCET). Algorithms must be analyzable for timing, often trading throughput for predictability.
- Security and isolation:
  - Sandboxing, permission models, and hardware support (MMU, TPM) constrain what algorithms can access, leading to designs that minimize privileges and data exposure.

Practical examples
- Sorting very large files:
  - If data > RAM, use external merge sort: read chunks that fit in memory, sort each chunk, then merge with sequential I/O to reduce random disk accesses.
- Matrix multiplication:
  - Naive triple-loop can be slow due to cache misses. Tiling/blocking increases cache reuse and dramatically improves performance on modern CPU caches.
- Searching/logging on streams:
  - For high-throughput streams where storage is limited, use streaming algorithms (e.g., approximate counting, sketching) that operate in sublinear memory.
- Parallel search or map-reduce:
  - Map-reduce style divides work across nodes/cores; communication cost and data partitioning become central design concerns.

Takeaway rules of thumb
- Know your machine model: memory size/latency, cache behavior, CPU parallelism, and I/O characteristics strongly affect which algorithm is best in practice.
- Favor locality: both temporal and spatial locality reduce costly memory and cache misses.
- Match the algorithm to constraints: if memory is limited, prefer streaming/external-memory algorithms; if parallelism is abundant, design for concurrency and minimize synchronization.
- Consider worst-case and average-case resource use: real systems need both good average performance and acceptable worst-case behavior (esp. for real-time or interactive apps).
- Measure and profile: theoretical complexity matters, but constant factors and system interactions (cache, I/O, concurrency) often determine actual performance.

This section connects the abstract algorithms you study to the concrete machines they run on. Understanding the hardware–software stack and common system trade-offs helps you pick or adapt algorithms that perform well in real environments.

Programs are the concrete realizations of algorithms. An algorithm is a step-by-step recipe for solving a problem. A program expresses that recipe in a programming language so a computer can follow it. The programming language gives the vocabulary and rules for describing data, control flow (like loops and conditionals), and the operations the machine should perform. By writing a program you translate an abstract algorithm into a sequence of precise instructions that a computer can execute.

Key pieces: source code, translation, and execution
- Source code: the human-readable text you write in a programming language (for example, Python, Java, or C). It contains declarations of data structures, functions or procedures, and the exact steps of the algorithm. Source code is intended to be read and edited by people.
- Compilation and interpretation (translation): most source code must be translated into a form the machine can run. There are three common patterns:
  - Compilation: a compiler translates the entire source program into machine code (native instructions for the processor) or into an intermediate form (e.g., bytecode). The result is an executable file that the operating system can run directly.
  - Interpretation: an interpreter reads the source code (or an intermediate representation) and executes it line-by-line or statement-by-statement, performing the described operations on the fly.
  - Hybrid (bytecode + virtual machine): source is compiled to bytecode, and a runtime environment or virtual machine (VM) interprets or just-in-time (JIT) compiles bytecode to machine code at execution time (common with Java and some implementations of Python).
- Execution: execution is the running of translated instructions on a computer (CPU, memory, I/O). During execution the program manipulates data, makes decisions, performs I/O, and produces results. The runtime environment provides services such as memory allocation, garbage collection, and access to libraries and system resources.

How software is developed
Software development is an organized process that turns requirements and algorithms into reliable programs. Main steps at a high level:
1. Requirements and design: decide what the software must do, design algorithms and data structures, and structure the program into modules or components.
2. Implementation: write source code that implements the design, using libraries and APIs as needed.
3. Testing: verify the program behaves correctly and meets requirements (see details below).
4. Debugging and refinement: find and fix defects, improve performance, and refactor code for clarity and maintainability.
5. Deployment: release the program to users or production systems.
6. Maintenance: update the software to fix bugs, add features, respond to changed requirements, and keep it secure and compatible with other systems.

Testing and quality assurance
Testing is a continuous and systematic activity to build confidence that a program implements its intended algorithm correctly and robustly.
- Unit testing: test small, individual components or functions in isolation.
- Integration testing: test combinations of components together to ensure they interact correctly.
- System testing: test the entire system in an environment similar to production.
- Acceptance testing: verify that the software meets the user's needs and requirements.
- Regression testing: re-run tests after changes to ensure existing functionality still works.
Automated testing (test suites run by tools), continuous integration (automatically building and testing after each change), and code review are common practices to catch errors early.

Kinds of errors and how they are found
- Syntax errors: violate the language rules; detected by the compiler or interpreter before or during translation.
- Runtime errors: occur while the program runs (e.g., dividing by zero, null references); found by running tests or through runtime monitoring.
- Logic errors (bugs): the program runs but implements the algorithm incorrectly; found by careful testing, assertions, and code review.

Maintenance and long-term evolution
Software typically lives longer than the initial development phase. Maintenance includes:
- Bug fixes and security patches.
- Feature additions and changes to meet new requirements.
- Performance improvements and refactoring to reduce technical debt and make the codebase easier to work with.
- Upgrades to dependencies, libraries, and runtime environments.
Good maintenance relies on readable source code, tests (so changes don’t break existing behavior), version control systems (to track changes and enable collaboration), documentation, and automated build and test infrastructure.

Libraries, modules, and reuse
Programs rarely start from scratch. Libraries and modules provide reusable implementations of common algorithms and services (for example, sorting routines, data structures, networking, or graphics). Using well-tested libraries speeds development and reduces bugs, but requires managing compatibility and updates.

Summary (high level)
- An algorithm is realized as a program by expressing it in a programming language (source code).
- Source code is translated by compilers or interpreters (or both) into a form that can run on hardware.
- Execution is the actual running of those translated instructions on a computer.
- Software development includes design, implementation, testing, deployment, and maintenance, with testing and version control being essential for producing reliable, evolving software.

CS Subfields and Their Big Questions

Below are the major subfields you will meet in an intro CS course, the core kinds of questions or problems each field tries to answer, and a set of concrete real‑world example problems mapped to the subfields that would most directly contribute solutions.

Major subfields and their key questions

- Algorithms & Complexity (Theory)
  - What are efficient ways to solve computational problems?
  - Which problems are inherently hard (infeasible) and how do we classify their difficulty?
  - How do we prove correctness and bound time/space usage?
- Programming Languages & Compilers
  - How should we design languages so programmers can express ideas clearly and safely?
  - How can source code be translated into fast, correct machine code?
  - How do type systems and language abstractions prevent bugs?
- Software Engineering
  - How do teams design, build, test, and maintain large software systems reliably and predictably?
  - What processes, architectures, and tools improve productivity and quality?
- Systems & Operating Systems
  - How do we manage hardware resources (CPU, memory, I/O) and provide abstractions to programs?
  - How do we build reliable, high‑performance software on real machines?
- Distributed Systems & Networking
  - How can many computers cooperate to provide a single service, tolerate failures, and scale to millions of users?
  - How do we move data reliably and efficiently across networks?
- Databases & Information Retrieval
  - How do we store, index, query, and retrieve large amounts of structured or unstructured data efficiently and correctly?
  - How do we design models and query languages that support data integrity and fast access?
- Artificial Intelligence & Machine Learning
  - How can machines perceive, reason, learn, and make decisions from data or experience?
  - What models and algorithms enable prediction, classification, planning, or reinforcement learning?
- Computer Graphics & Visualization
  - How do we generate images, animations, and interactive visual interfaces from models and data?
  - How do we map data to visual encodings to reveal patterns and support exploration?
- Human–Computer Interaction (HCI)
  - How should systems be designed so people can use them effectively, efficiently, and enjoyably?
  - How do we evaluate usability and design interfaces for different users and contexts?
- Security & Cryptography
  - How do we protect systems and data from attackers, ensure privacy, and provide secure communication?
  - What cryptographic techniques guarantee confidentiality, integrity, and authentication?
- Robotics & Control
  - How do we sense environments, plan motions, and control actuators so machines can accomplish physical tasks?
  - How do planning, perception, and feedback control integrate in real time?
- Computer Architecture & Embedded Systems
  - How should computers be organized internally to execute programs efficiently?
  - How do we build specialized hardware or embedded devices with strict constraints (power, size, latency)?
- High‑Performance & Scientific Computing (Computational Science)
  - How do we design algorithms and systems to simulate and analyze large scientific problems using many processors?
  - How do we ensure numerical stability, efficiency, and scalability?
- Bioinformatics & Computational Biology
  - How can computational methods analyze biological sequences, structures, and large-scale biological data?
  - How do we model biological processes and extract actionable insights?

Mapping real-world problems to subfields

- Self‑driving car (perception, planning, control)
  - AI/Machine Learning (computer vision, perception), Robotics & Control (motion planning, feedback), Systems/Embedded (real‑time operation), Networking (V2X communication), Security (safety, adversarial robustness).
- Recommender system for an online retailer
  - Machine Learning (collaborative filtering, ranking), Databases (data storage and query), Algorithms (scaling, approximate methods), HCI (presentation and evaluation).
- Large‑scale web search engine
  - Algorithms & Complexity (indexing, ranking algorithms), Distributed Systems & Networking (crawl, indexing pipelines, serving), Databases (index storage), Machine Learning (ranking models), Security (spam, abuse).
- Real‑time high-frequency trading platform
  - Systems & Operating Systems (low latency), Networking (fast links), Algorithms (streaming, matching), Security (integrity), Databases (transactional persistence).
- Medical image diagnosis from MRI scans
  - Machine Learning & AI (image classification, segmentation), Computer Vision, Computational Science (image processing algorithms), HCI (interpretation interfaces), Security & Privacy (patient data protection).
- Video game development (3D action game)
  - Computer Graphics (rendering, shading), Software Engineering (architecture), Systems (performance optimization), HCI (gameplay design), Networking (multiplayer).
- Secure messaging app (end‑to‑end encryption)
  - Security & Cryptography (protocol design, key management), Networks (message delivery), Systems (secure storage), HCI (key exchange usability).
- Compiler for a new programming language
  - Programming Languages & Compilers (syntax, semantics, optimizations), Algorithms (dataflow, analyses), Systems (code generation, runtime).
- Climate modeling and simulation
  - High‑Performance & Scientific Computing (numerical methods, parallelization), Computational Science (modeling), Data Visualization (interpreting results).
- Social network analysis for misinformation spread
  - Databases (graph storage), Algorithms (graph algorithms, centrality), Machine Learning (classification of content/accounts), Distributed Systems (processing at scale), HCI (tools for analysts).
- Smart home IoT sensor network
  - Embedded Systems & Architecture (low‑power devices), Networking (mesh, protocols), Security (device authentication), Distributed Systems (coordination), HCI (control apps).
- DNA sequence assembly and analysis
  - Bioinformatics (sequence algorithms, statistical models), Algorithms (string matching, graph assembly), Databases (genomic data), Machine Learning (variant calling).
- Autonomous drone swarm coordination
  - Robotics & Control (local control, planning), Distributed Systems & Networking (coordination, consensus), AI (multi‑agent planning), Security (resilience to interference).
- Protecting an online voting system from tampering
  - Security & Cryptography (secure voting protocols, auditability), Distributed Systems (resilience), Software Engineering (reliability), HCI (voter usability).
- Optimizing delivery routes for a logistics company
  - Algorithms & Complexity (combinatorial optimization: vehicle routing), Machine Learning (demand forecasting), Distributed Systems/Databases (operational data), Systems (real‑time routing updates).

How to use this map
- When faced with a problem, identify its core challenges (computation, data, interaction, physical control, security).  
- Pick the subfield(s) whose questions match those challenges—most real problems require contributions from multiple subfields.  
- Use the mapped examples above as patterns: e.g., if the central issue is “making predictions from noisy high‑dimensional data,” start with AI/ML; if it is “coordinating many machines reliably,” start with Distributed Systems.

End of section.