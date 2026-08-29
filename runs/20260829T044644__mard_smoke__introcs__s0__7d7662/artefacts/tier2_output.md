Computer systems are built from many interacting parts. At a high level you can split those parts into hardware (the physical devices) and software (the programs and data that run on the devices). Understanding how these pieces fit together and how abstraction layers are used to hide complexity is a foundation for studying computing.

Hardware and software components, and how they interact
- Hardware components:
  - Processor (CPU): executes instructions, performs arithmetic and control decisions.
  - Main memory (RAM): stores instructions and data while programs run.
  - Storage (disk, SSD): holds data persistently when power is off.
  - I/O devices: keyboard, mouse, display, network interfaces, sensors and actuators.
  - Buses and controllers: move data between devices.
  - Digital logic and circuits: gates and flip-flops that implement the CPU and memory.
- Software components:
  - Firmware/bootloader: very low-level code that starts hardware and loads the operating system.
  - Operating system (OS): manages hardware resources (CPU scheduling, memory allocation, device drivers, file systems) and provides services to programs.
  - Language runtimes and libraries: provide support like memory allocation, I/O functions, garbage collection.
  - Applications: the end-user programs that implement specific tasks (a web browser, editor, calculator).
  - Tools: compilers, assemblers, linkers, debuggers that transform and manage code.

Interaction examples
- A web browser (application) requests a page: it issues system calls to the OS for network access and file storage. The OS commands the network controller (hardware) to send/receive packets. The CPU runs the browser’s code and the OS scheduler decides when the CPU executes browser threads.
- A compiler translates high-level source code into machine code that the CPU executes. The machine code manipulates memory addresses and I/O registers exposed by the hardware or by the OS.

Levels of abstraction and why they matter
- Abstraction is the practice of hiding lower-level details behind a well-defined interface so you can reason about a component without understanding its internals.
- Computer systems are typically organized into stacked abstraction layers. A common stack (bottom to top) is:
  1. Physical circuits (transistors, wires)
  2. Digital logic and microarchitecture (ALU, registers, pipelines)
  3. Instruction set architecture (ISA) or machine language (the CPU’s “visible” instructions)
  4. Operating system kernel and device drivers
  5. Language runtimes and libraries
  6. Applications and user interfaces
- Each layer exposes a small set of services and hides many implementation details of the layer(s) below. For example, a programmer using a high-level language need not know how a disk controller signals interrupts; they call a file-open function and the OS handles the rest.

Benefits of abstraction
- Manage complexity: you concentrate on one level of concern (e.g., algorithms, user interface) without being overwhelmed by hardware intricacies.
- Modularity and reuse: components with stable interfaces can be developed, tested, and reused independently (e.g., an OS can run many applications).
- Portability: software written to an abstraction (high-level language, OS API) can run on different hardware implementations that provide the same abstractions.
- Faster development: higher-level abstractions let programmers express ideas concisely without implementing low-level details.

Interfaces and contracts
- Abstractions only work when there is a clear interface or contract. Examples: an API call signature, the semantics of an instruction in an ISA, or the behavior of a file system call (open, read, write).
- The contract states what the caller can assume and what the implementation must provide. This enables independent development and reasoning.

When abstraction leaks
- Abstractions are not perfect. Sometimes low-level details affect higher-level behavior — for example:
  - Performance: cache behavior, memory layout, and I/O latency often determine a program’s speed.
  - Correctness: concurrency bugs or hardware limitations (e.g., integer overflow) can break assumptions in higher-level code.
- Good engineers know when to trust an abstraction and when to inspect lower layers to diagnose performance or correctness problems.

Summary of key ideas to remember
- A computer system is an organized collection of hardware and software components that cooperate to execute programs and manage data.
- Layers of abstraction hide lower-level complexity behind interfaces, making it possible to build and reason about large systems.
- Abstraction brings modularity, reuse, and portability, but sometimes low-level details “leak” and must be understood to solve real problems.

Computation operates over representations of information (data)

Computation does not work directly on “real-world” things; it works on symbols stored and manipulated inside a computer. Those symbols are representations of information: numbers, text, images, sounds, graphs, etc., all encoded in bits (and organized into higher-level data structures). A representation defines:

- what values can be expressed (range, precision, fidelity),
- how values are encoded (bit patterns, characters, pointers),
- what operations are defined and how they behave (addition, comparison, search),
- how much time and memory those operations require.

Why representation matters

1. What operations are possible or easy
   - Some representations make certain operations natural and efficient. Example: integers in binary support fast bitwise operations and arithmetic on fixed-size words; a linked list makes insertion and removal at arbitrary positions easy if you have the node pointer; an array makes random access (indexing) O(1).
   - Other operations may be awkward or expensive with the same representation. Example: removing an element from the middle of an array requires shifting many elements (O(n)), while a linked list can do it in O(1) if position is known but cannot do constant-time random access.

2. Correctness and expressiveness
   - Representations can be lossy or exact. Floating-point numbers approximate real numbers; some decimal fractions cannot be represented exactly, which can lead to rounding errors. If exact rational arithmetic is needed, use fractions or arbitrary-precision rationals instead.
   - Some representations constrain values: using a signed 32-bit integer disallows values outside its range; representing a graph as an adjacency matrix assumes a fixed vertex set and is less convenient for sparse graphs than adjacency lists.

3. Performance (time and space)
   - Different encodings and data structures have different complexity for basic operations. Example: searching an unordered array is O(n), but searching a hash table is expected O(1) and a balanced binary search tree is O(log n).
   - Space use matters: a dense bitmap may represent a set compactly when the domain is small, but for large sparse domains a sparse representation (list of elements, hash set, or compressed structure) uses much less memory.
   - Low-level encodings affect constant factors: compact representations reduce cache misses and I/O, improving real-world performance even when asymptotic complexity is similar.

4. Ease of implementation and reasoning
   - Some representations make algorithms simpler to write and prove correct. Using immutable values can avoid certain bugs; using types or tagged unions can prevent invalid states.
   - Converting between representations (serialization, parsing) costs time and may introduce errors, so keeping data in a suitable form for the operations you need avoids unnecessary conversions.

Examples that illustrate trade-offs
   - Text vs numeric: Storing “12345” as a string makes concatenation and pattern matching easy; storing it as an integer makes arithmetic efficient.
   - Binary vs ASCII: Binary encodings are compact and faster to process; ASCII/UTF-8 are human-readable and interoperable with text tools.
   - Array vs linked list: Arrays give fast indexing and compact storage; linked lists give cheap insert/delete at known positions.
   - Adjacency matrix vs adjacency list: Matrix supports O(1) edge-existence checks and is simple for dense graphs; lists are much more space- and time-efficient for sparse graphs.
   - Floating point vs arbitrary precision: Floating point is fast and uses fixed memory but has rounding error; arbitrary-precision arithmetic is exact but slower and uses variable memory.

Guidelines for choosing a representation
   - Match representation to the operations you need most often (optimize the common case).
   - Consider the data’s shape: dense vs sparse, fixed-size vs varying, bounded vs unbounded.
   - Balance time and space: smaller memory can improve speed (caching) but may increase CPU cost to encode/decode.
   - Beware of precision and range requirements: choose exact or approximate representations appropriately.
   - Leverage abstraction: use higher-level types and libraries that hide encoding details until you need to optimize.

Takeaway
Choosing how to represent information is a fundamental design decision. It determines which computations are straightforward or even possible, affects correctness (precision and validity), and controls performance (time and memory). Good choices align the representation with the problem’s operations and constraints.

Computation and Problems

Computation is any process that transforms inputs into outputs according to a precise procedure. In computing, we model that process so a machine (or a person following a recipe) can carry it out. A computation therefore requires three elements:
- inputs: the information you start with,
- outputs: the information you want to obtain,
- a well-defined mapping (procedure or algorithm) that reliably turns those inputs into those outputs.

Framing a real-world goal as a well-specified problem means taking an often vague intention and restating it so every part is precise and machine-actionable. To do this you should:

1. Identify the inputs explicitly.
   - What data will be given? In what form? (e.g., “a list of integers,” “a start and end address,” “an image file.”)
2. Specify the desired outputs exactly.
   - What should the result look like? What type, format, and constraints? (e.g., “the list sorted in nondecreasing order,” “the shortest driving route as a sequence of turns and distances.”)
3. Define the relation between inputs and outputs.
   - State the rule that maps any valid input to the correct output. This eliminates ambiguity about acceptable results.
4. State any assumptions and constraints.
   - Limits on input size, performance requirements (time, memory), or allowable approximations must be explicit.
5. Consider edge cases and error handling.
   - What should happen with malformed inputs, ties, or missing data?

Examples
- Vague goal: “Make my playlist better.” Well-specified problem: “Given a list of songs and a target mood score, produce a reordered list in which the moving average mood score never drops below the target; songs are represented by numeric mood values 0–100.”
- Vague goal: “Find a way to get there.” Well-specified problem: “Given a road graph with weighted edges (travel times) and two vertices, output a path with minimum total weight. If multiple shortest paths exist, return any one.”

Why this matters
- A well-specified problem lets you design or choose an algorithm and reason about correctness and resources. If the goal remains vague, you cannot guarantee that a computation will meet the intended purpose.
- Some real-world goals cannot be fully captured or may require approximation; making assumptions explicit clarifies when an exact computation is possible and when approximations or heuristics are needed.

In short: computation is transforming clearly specified inputs into outputs; framing a real-world goal as a computable problem requires making inputs, outputs, mapping rules, and constraints precise so an algorithm can be applied.

Algorithms

An algorithm is a precise recipe for solving a specific problem: a finite, unambiguous sequence of steps that, when followed, transforms given input into the desired output. Each step must be clear (so a person or machine can carry it out without guessing), the procedure must eventually stop (finiteness/termination), and it should produce the correct result for all allowed inputs.

Key properties of an algorithm
- Finite: It must stop after a bounded number of steps for every valid input.
- Unambiguous: Every step is stated clearly and exactly; there is no room for interpretation.
- Inputs and outputs: An algorithm specifies what inputs it expects and what outputs it will produce.
- Effectiveness: Each step must be basic enough to be executed with the available operations.
- Correctness: For every valid input the algorithm must produce the required output (this is a property to be proved or tested).
- (Often considered) Efficiency: Algorithms can be compared by how much time and space (memory) they use.

Problem statement vs a particular algorithm
- Problem statement: A high-level description of what you want to solve; it does not tell how to do it. It specifies the allowed inputs and the required relation between inputs and outputs.
  Example: “Sort a list of numbers in nondecreasing order.” This tells the goal but not how to achieve it.
- Particular algorithm: A concrete sequence of steps that accomplishes the problem’s goal for all allowed inputs.
  Example: “Insertion sort: repeatedly take the next element and insert it into its place among the previously sorted elements” — this is one specific way to solve the sorting problem.

Why the distinction matters
- Many algorithms can solve the same problem. Choosing among them depends on correctness, simplicity, and efficiency for the expected inputs.
- The same algorithm can be implemented in many programming languages; the algorithm itself is the abstract idea, the program is one concrete implementation.
- When designing or analyzing solutions, separate the problem specification (what you need) from the algorithm (how you proceed).

Short examples
1. Problem: “Compute the average of two numbers x and y.”
   Algorithm (one possible solution):
   - Step 1: Read numbers x and y.
   - Step 2: Compute sum = x + y.
   - Step 3: Compute average = sum / 2.
   - Step 4: Output average.
   This algorithm is finite, unambiguous, and directly solves the stated problem.

2. Problem: “Find the greatest common divisor (GCD) of two positive integers.”
   Two different algorithms:
   - Naive algorithm: Try all integers from min(x,y) down to 1 to find the largest that divides both (correct but slow).
   - Euclidean algorithm: Repeatedly replace (a, b) with (b, a mod b) until b is 0; the nonzero a is the GCD (correct and efficient).
   Both solve the same problem statement, but they differ in steps and performance.

Takeaway
Always distinguish the specification of a task (the problem statement) from one or more concrete sequences of steps (algorithms) that accomplish it. An algorithm must be finite and unambiguous so it can be reliably executed and analyzed.

Efficiency matters because computers have limited resources. Time (how long a program takes) and space (how much memory it uses) determine whether a program finishes in a reasonable time, fits on a device, or can handle realistic inputs. A correct program that takes weeks or runs out of memory is not useful; small differences in how work scales with input size quickly become huge as inputs get bigger.

Input size drives running time
- Think of the input size n as the quantity that grows: number of items in a list, characters in a file, nodes in a graph, etc. When n is small, almost any sensible program will run quickly. As n grows, the way running time depends on n becomes the dominant factor.
- Simple examples:
  - Scanning a list once (adding all numbers, finding the max) does a fixed amount of work per item, so the work grows roughly in proportion to n. Doubling n roughly doubles the time.
  - Nested loops over the same list (compare every pair of items) do about n × n = n^2 steps. Doubling n makes the work about four times larger.
  - Binary search on a sorted list cuts the remaining work roughly in half each step, so the number of steps grows like log n — doubling n adds only one extra step.
- The important intuitive point: constant-factor differences (2× vs 3× work) matter less than how the time grows with n (linear vs quadratic vs logarithmic). For small n the constant can dominate, but for large n the growth rate (the “shape” of the curve) dominates.

Why this affects algorithm and data-structure choices
- Algorithms determine the amount of work needed to solve a problem. Choosing a better algorithm (e.g., using binary search instead of scanning, or a n log n sort instead of n^2 sorts) can change running time from impractical to practical for large inputs.
- Data structures change the cost of basic operations:
  - Arrays let you access any position quickly (constant time), but inserting in the middle costs linear time.
  - Linked lists make insertions and deletions cheap at known positions, but accessing the k-th element takes linear time.
  - Hash tables give average constant-time lookup and insertion, while balanced search trees give logarithmic-time ordered operations.
- Trade-offs matter: faster time may require more memory (caching, indexes, precomputation), and saving memory may slow down operations. Sometimes preprocessing (sorting or building an index) pays off because it reduces the cost of many future queries.

Practical guidance (informal)
- Identify the input size you expect. Micro-optimizations are pointless if n stays tiny; algorithmic improvements matter when n can be large.
- Prefer algorithms and data structures whose cost grows slowly with n (e.g., logarithmic or linear rather than quadratic), unless you have strong reasons otherwise.
- Consider worst-case vs average-case behavior depending on the application (real-time systems need worst-case guarantees).
- Measure and profile when unsure; analysis guides choices, but real data and resource limits decide what matters in practice.

In short: think about how work scales with input size, and pick algorithms and data structures that keep that scaling manageable for the sizes you expect to handle.

Programs as Implementations of Algorithms

What an algorithm is
- An algorithm is an abstract, language‑independent description of a step‑by‑step procedure that solves a problem. It specifies the logical operations, control flow (sequence, choice, repetition), and the data transformations required, but not the precise symbols or machine steps used to carry it out.

What a program is
- A program is a concrete encoding of an algorithm written in a programming language. The program uses the syntax and primitives of that language to represent the same sequence of operations and data manipulations the algorithm describes.
- The program must make the algorithm precise in ways the abstract description may leave open: exact data representations (e.g., integers vs. floats), boundary behaviors, error handling, resource allocation, and order of evaluation where the algorithm did not specify them.

How programs encode algorithms
- Control structures in the algorithm (sequence, if/else, loops, recursion) become language constructs (statements, conditionals, while/for, function calls).
- Data abstractions in the algorithm (lists, sets, records) become types and variables in the language (arrays, objects, structs).
- High‑level operations get implemented by combinations of lower‑level language constructs or by calling libraries that implement common primitives.
- Decisions about efficiency and resource use are encoded in algorithmic choices implemented as code (e.g., using an in‑place sort vs. copying, iterative vs. recursive).
- The same algorithm can be encoded in many different programs: different languages, different coding styles, or different optimizations produce different programs that implement the same underlying algorithm.

Relationship to machine execution
- A program alone is static text (source code). Machine execution is the dynamic process in which the computer follows the instructions represented by the program to perform computations.
- To run on hardware, the program must be translated into machine actions. That can happen via:
  - Compilation: a compiler translates source code into machine code (or bytecode), producing an executable that the CPU runs directly (or via an interpreter/VM).
  - Interpretation: an interpreter reads the source or an intermediate form and performs the specified operations directly, invoking machine instructions to implement each language construct.
  - Virtual machines/runtime systems: the program runs on software that maps language constructs to machine operations (e.g., the JVM).
- The runtime environment (OS services, libraries, garbage collector, hardware resources) mediates and implements many of the program’s behaviors at execution time.

Putting it together: algorithm → program → machine behavior
- Algorithm: the problem solution described abstractly (what to do).
- Program: a language‑level encoding of that algorithm (how to do it concretely).
- Machine execution: the actual carrying out of the program’s steps by hardware and runtime software (the physical performance of the task).
- Correctness and performance flow down the chain: a correct program faithfully implements the algorithm; machine execution realizes the program’s actions. Performance and resource usage depend both on the algorithmic complexity and on implementation choices and machine characteristics.

Practical consequences
- Abstraction separation: you can reason about algorithmic correctness and complexity independently of many low‑level coding details, but final behavior depends on the implementation and execution environment.
- Portability: the same program may run unchanged across machines only when translation (compilation/interpreting) targets those machines; the same algorithm may be implemented by different programs suited to different environments.
- Debugging and optimization: errors may come from algorithmic design, incorrect encoding in the program, or from execution issues (e.g., precision, concurrency, memory limits). Optimizations can be applied at the algorithm level or at the program/compilation level.

Key takeaway
- An algorithm is the abstract plan; a program is the concrete plan written in a programming language; machine execution is the realization of that plan by hardware and runtime software. Understanding all three layers and how they map to one another is essential for designing correct, efficient, and practical software.