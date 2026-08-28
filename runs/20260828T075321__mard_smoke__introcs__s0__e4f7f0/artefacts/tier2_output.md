Data and Information Representation

Computers do not “know” concepts directly — they only manipulate symbols (bits) according to precise rules. Solving a problem on a computer therefore begins with representing the things in the problem (numbers, text, images, relationships, events, etc.) as data the machine can store and process. That mapping from real-world concepts to concrete encodings is what makes computation possible, and it strongly influences what solutions look like and how well they work.

What a representation does
- Makes information precise and unambiguous so a machine can store, copy, compare and transform it.
- Enables computation: algorithms are defined in terms of operations on particular data formats (e.g., arithmetic on integers, string concatenation, graph traversal on adjacency lists).
- Supports communication and interoperability: standard encodings (ASCII/Unicode, IEEE floating point, PNG, JSON) let different programs and machines exchange data.
- Hides irrelevant details (abstraction) so you can reason about a problem at the right level.

Common kinds of representations (examples)
- Numbers: binary integers (two’s complement), fixed-point, floating point (IEEE 754). Each choice fixes range, precision, and behavior for overflow/rounding.
- Text: ASCII, UTF-8/Unicode — how characters map to byte sequences matters for correctness and display.
- Images and audio: samples/pixels with color/depth, often compressed (lossless vs lossy).
- Structured data: arrays, records/objects, lists, trees, graphs — shapes that support particular algorithms and access patterns.
- Encodings and formats: how higher-level structures are serialized (JSON, XML, binary protocols).

Why representation matters for computation
- Correctness: some encodings introduce approximation (floating point, lossy compression) or limits (integer overflow), which can produce wrong answers if not accounted for.
- Efficiency: memory usage and running time depend on representation (sparse vs dense matrices, adjacency lists vs matrices for graphs).
- Expressiveness and simplicity: the right data type makes algorithms simpler and less error-prone (e.g., using timestamps rather than formatted strings).
- Interoperability: choosing standard encodings prevents misinterpretation across systems (character-set mismatches or endianness issues cause bugs).
- Feasibility: some problems are only practical with particular encodings (e.g., compressing large images makes storage and transfer possible).

Trade-offs and pitfalls
- Exact vs approximate: exact representations (integers, lossless formats) preserve information but may be larger; approximate ones (floats, JPEG) save space but can change values.
- Granularity and precision: choosing too coarse a representation loses important distinctions; too fine may be wasteful.
- Representation-dependent complexity: algorithms can have different costs depending on data layout (searching a sorted structure vs linear scan).
- Implicit assumptions: forgetting representation limits (precision, range, encoding) leads to subtle bugs.

How representation guides problem solving
- Model the domain with data types and structures that naturally express the entities and operations you need.
- Let the representation drive algorithm design: pick data layouts that make required operations efficient and correct.
- Be explicit about encoding choices and their consequences (precision, range, interoperability).
- Test and reason about edge cases introduced by the representation (overflow, rounding, encoding errors).

Bottom line
Representation is the bridge between human problems and machine solutions. Choosing how to encode information is not just an implementation detail — it determines whether a computation is correct, efficient, and even possible.

Computation (as used in this textbook)
- Computation is the systematic manipulation of information (symbols, numbers, bits) according to precisely specified rules. A computation takes one or more inputs, performs a sequence of well-defined steps (an algorithm), and produces outputs.
- The emphasis is not on the physical machine but on the procedure: what is being computed and how. The same computation can be carried out by different machines, formal systems, or programs as long as the rules are the same.

How computer science frames problems as computable tasks
- A problem is framed as a mapping from inputs to desired outputs. To make a problem computable you must:
  1. Specify the inputs (what form the data takes).
  2. Specify the outputs (what counts as a correct answer).
  3. Give a procedure (algorithm) that, in a finite number of well-defined steps, transforms any valid input into a correct output.
- Computer science studies how to design those procedures, how to represent and manipulate the data they operate on, and how to reason about their correctness and resource usage (time, memory).
- Problems are often expressed in abstract terms (functions, relations, decision questions) so we can reason about solvability and efficiency without tying the solution to a particular programming language or hardware.

Kinds of problems that are in-scope
- Precisely defined tasks with clear success criteria, for example:
  - Numerical computation (add, multiply, solve equations).
  - Data processing and transformation (sort a list, filter records).
  - Search and retrieval (find an item, shortest path).
  - Decision problems (yes/no questions about data).
  - Optimization (find the best solution under constraints).
  - Simulation and modeling (predict system behavior given a model).
  - Communication, encoding, and storage tasks (compress, encrypt).
- These problems may be exact (exact arithmetic, exact match) or approximate (fit a model, approximate root), and may require probabilistic or heuristic methods when exact solutions are impractical.
- Also in-scope are meta-problems: proving correctness, measuring complexity, and classifying which problems are solvable at all.

What it means to solve a problem with a computer
- To solve a problem with a computer you must produce an algorithm and implement it so that:
  - For every valid input, the program produces an output that meets the specification (correctness).
  - The program runs in a finite amount of time and uses finite resources (feasibility). Practical solutions consider efficiency: time, memory, and other constraints.
  - If exact solutions are impossible or impractical, the program should provide acceptable approximations, probabilistic guarantees, or graceful degradation.
- Solvability has two senses:
  - Theoretical solvability (computability): Is there any algorithm that always produces the correct output in finite steps? Some tasks are provably uncomputable (e.g., the halting problem).
  - Practical solvability (tractability): Even if computable, is the problem solvable within reasonable time and resources? Some problems are computable but intractable for realistic input sizes.
- Solving with a computer also implies repeatability and automation: once implemented, the same procedure can be applied reliably to many problem instances.

Key consequences for how we approach problems
- We must formalize informal questions into precise specifications before writing a program.
- Decomposition and abstraction are used to turn large problems into smaller, computable subproblems.
- We choose representations and algorithms that balance correctness, efficiency, and resource limits.
- Some problems require new models (approximation, randomized algorithms, learning) when exact, deterministic computation is impractical.

In short: computation in this textbook is the formal, rule-based transformation of information; computer science turns real-world and abstract questions into precisely specified input→output tasks and studies how to implement, reason about, and optimize the algorithms that solve them, while recognizing the limits of what can be computed or done efficiently.

Algorithms

An algorithm is an explicit, well-defined recipe for solving a problem: a finite sequence of unambiguous steps that, when carried out, transforms given inputs into the desired outputs. In computation, algorithms are the essential link between a problem statement (what we want) and a program or machine that produces the answer (how we get it).

How algorithms relate to solving problems by computation
- A computational problem is described by the relationship between inputs and the outputs you want for those inputs. Designing an algorithm means deciding the precise steps a computer should perform to produce the correct outputs from the allowed inputs.
- An algorithm is independent of any particular programming language or machine: it is the abstract plan. Implementing the algorithm in a language produces a program that a computer can run.
- Computing a problem means executing the algorithm on a computer (or by hand) so that for every legal input the algorithm produces the correct output.

Key properties emphasized (informal)
- Step-by-step procedure: An algorithm specifies a sequence of concrete steps to be followed in order. Each step should be clear enough that it can be executed without additional invention.
- Inputs and outputs: An algorithm takes zero or more inputs (the data describing a specific instance of the problem) and produces one or more outputs (the solution for that instance). The relationship between inputs and outputs defines the problem the algorithm solves.
- Correctness: For every valid input, the algorithm should produce the intended output. Correctness is the guarantee that the algorithm actually solves the stated problem.
- Termination (finiteness): An algorithm must finish after a finite number of steps for every valid input. If it can run forever on some input, it is not a proper algorithm for that problem.
- Definiteness / unambiguity: Each step must be precisely specified so there is no confusion about what to do next.
- Effectiveness: Each step should be simple enough to be carried out mechanically (by a human following rules or by a machine).

Simple illustration (informal)
- Problem: find the maximum number in a nonempty list.
- Inputs/outputs: input = the list; output = the largest element.
- Algorithm sketch: start by assuming the first item is the maximum; examine each remaining item in turn; if an item is larger than the current maximum, update the maximum; after the last item, return the current maximum.
- This example shows a clear step-by-step procedure, defined input/output, it’s effective and unambiguous, it terminates when the list ends, and it is correct if implemented as stated.

In short: an algorithm is the finite, precise plan that tells a computer how to transform inputs into correct outputs. Designing good algorithms is the central task in solving computational problems.

Section: Programs as Implementations of Algorithms

What an algorithm is
- An algorithm is an abstract, precise recipe that describes how to transform inputs into outputs using a finite sequence of well-defined steps.
- It is independent of any particular programming language or machine; it specifies the logical operations, control flow, and termination conditions needed to solve a problem, often expressed in words or pseudocode.

What a program is
- A program is a concrete, language-specific implementation of an algorithm. It is a sequence of instructions written in a programming language whose syntax and semantics are precise enough for a computer (via a compiler or interpreter) to execute.
- A program must resolve all the choices left abstract by an algorithm: data representations, exact looping structures, boundary tests, error handling, and resource management.

How a program realizes an algorithm
- Encoding steps: Each step of the algorithm is translated into one or more statements in the programming language. High-level operations (e.g., “swap two elements”) become sequences of assignments and temporary variables.
- Representing data: The program picks concrete data structures (arrays, lists, records) and data encodings (integers, floating point, strings) to represent the abstract values the algorithm manipulates.
- Specifying control flow: Conditional branches, loops, and function calls in code implement the algorithm’s control structure (if-then-else, repetition, recursion).
- Handling edge cases and I/O: Programs add concrete checks, input/output code, and error handling that the algorithm’s abstract description may omit.
- Lowering to machine actions: A compiler or interpreter translates the source program into machine-level actions (instruction sequences, memory reads/writes, jumps) so the CPU can execute the intended operations. Thus, every abstract operation is ultimately realized as a sequence of primitive machine operations (arithmetic, load/store, branch).
- Runtime support: Some program behaviors depend on runtime systems (libraries, garbage collector, operating system services), which provide concrete implementations for higher-level facilities referenced by the algorithm.

Key distinctions and consequences
- Correctness vs. implementation: An algorithm can be correct in the abstract (it produces the intended result on paper) while a program can be incorrect due to bugs, wrong data representation, or mishandled edge cases. Program correctness requires proving or testing that the implementation faithfully realizes the algorithm for all inputs.
- Multiple programs can implement the same algorithm: Different languages, data structures, or micro-optimizations can produce different programs that implement the same high-level algorithm with varying performance and resource use.
- Performance and resources: Implementing an algorithm requires choices that affect time and space usage. Data layout, loop structure, and low-level calling conventions can change real-world performance even when the algorithm remains the same.
- From abstraction to execution: The central role of programming is to make the abstract steps of an algorithm concrete and executable on hardware, bridging human reasoning and machine constraints.

Compact example (conceptual)
- Algorithm: “Sort a list by repeatedly scanning and swapping out-of-order neighbors until the list is ordered” (bubble sort).
- Program: Code in a language that uses arrays, nested loops, index variables, and a swap routine; includes bounds checks and a stopping condition; compiled down to machine instructions that compare elements and swap memory locations.
- The program implements every detail required for a computer to perform the bubble-sort algorithm and add the practical machinery (input parsing, output formatting, and safety checks) the algorithm left unspecified.

Takeaway
- An algorithm is the idea; a program is the precise, executable realization of that idea. Writing a program is the process of concretizing the algorithm’s abstract steps so a computer can carry them out reliably and efficiently.

Computing systems are made of a few recurring parts that work together to turn programs and data into useful results. The chapter treats the following as the core components and explains their roles and interactions.

Core components
- Hardware
  - Central Processing Unit (CPU): performs arithmetic and logic, controls the machine-level instruction flow (fetch–decode–execute).
  - Memory (RAM): stores the currently running program’s instructions and the data it manipulates.
  - Persistent storage (disk/SSD): stores programs and data long-term; used to load programs into memory.
  - Input/Output devices: keyboards, mice, displays, network interfaces, sensors and actuators that move data between the machine and the outside world.
  - Buses and controllers: hardware that moves data between CPU, memory, and I/O.
- Software
  - Operating system (OS): manages hardware resources, isolates processes, provides services (file system, scheduling, drivers) and an API for programs.
  - System software (compilers, interpreters, runtimes): translate and prepare high-level programs into forms the hardware can execute, and provide runtime support.
  - Application programs: user-level programs that implement tasks and algorithms.
- Data: the bits and structures representing program state, inputs, outputs, and persistent information.
- People and networks (environment)
  - Users and programmers: provide requirements, write programs, and interpret results.
  - Other systems and networks: allow distributed computation, communication, and storage.

How these components cooperate to carry out computation (high level)
1. A programmer writes a program (source code) and stores it on persistent storage.
2. A compiler or interpreter (system software) translates source code into machine-executable form (a binary or bytecode plus runtime support).
3. The operating system loads the executable into memory and allocates CPU time and other resources (files, devices).
4. The CPU repeatedly performs the fetch–decode–execute cycle:
   - Fetch the next instruction from memory.
   - Decode what the instruction requests.
   - Execute it using the ALU, registers, and memory, possibly producing outputs or updating state.
5. I/O devices provide inputs (e.g., user keystrokes, network packets) and consume outputs (display, files). Device drivers mediate between the OS and hardware.
6. The OS multiplexes resources (scheduling, virtual memory, file management), handles interrupts and exceptions, and enforces protection so multiple programs can run safely.
7. Persistent storage and networks provide longer-term or remote storage and communication, enabling programs to save results and interact with other systems or users.

Roles of hardware vs. software in executing programs (high level)
- Hardware provides the physical substrate and primitive operations:
  - The CPU implements the instruction set and performs low-level arithmetic/logical operations.
  - Memory and buses hold and move bits.
  - I/O devices sense and affect the external world.
  - Hardware enforces timing, electrical signaling, and low-level data movement.
- Software provides abstraction, control, and behavior:
  - System software (OS, drivers, runtimes) hides hardware complexity, allocates resources, translates high-level requests into hardware actions, and enforces policies (security, scheduling).
  - Compilers and interpreters translate human-readable programs into sequences of machine instructions the hardware can execute.
  - Application software expresses algorithms and user-facing behavior built on the services the OS and hardware provide.
- In short: hardware executes the primitive instructions; software decides which instructions to run, organizes them into meaningful tasks, and manages resources so multiple tasks and users can coexist.

Together, hardware supplies the capabilities and raw speed, while software supplies the logic and organization. Their cooperation—translation of high-level code, managed allocation of resources, and execution of machine instructions—produces correct, efficient computation.

6. Levels of Abstraction in Computing

What the chapter emphasizes: computing problems are understood and solved through a stack of abstraction layers. Each layer hides lower-level detail so we can reason at the right scale:

- Problem specification (the “what”): a clear statement of the task in domain terms (e.g., “sort these names” or “find the shortest path”).
- Algorithm (the “how” in logical steps): a language‑independent recipe that solves the problem (e.g., merge sort, Dijkstra’s algorithm). Algorithms are judged by correctness and resource bounds (time/space).
- Program (the “how” in code): a concrete implementation of an algorithm in a programming language. This introduces syntax, libraries, data structures, and implementation choices.
- Machine execution (the “how” physically): compiled/translated instructions, machine code, memory layout, CPU cycles, caches — the real operations performed by hardware.

Why abstraction matters
- Manages complexity: by hiding low-level detail, each layer reduces what you must keep in mind. You can design an algorithm without simultaneously thinking about registers and cache lines.
- Enables reuse and modularity: programs can use libraries and compilers without reimplementing every detail; algorithms can be applied to many programs.
- Separates concerns: correctness can be argued at the algorithm level, performance tuned at the program or machine level.
- Improves communication: people (and tools) operate at the level that matches their goals — domain experts specify problems; developers write programs; compilers and hardware implement execution.

Short example: “Sort a list of numbers”
- Problem level: “Given a list of integers, produce a list with the same integers in nondecreasing order.”
- Algorithm level: “Use merge sort: recursively split the list in half, sort each half, then merge the sorted halves.” (Complexity: O(n log n) time, O(n) extra space.)
- Program level (Python sketch): 
  def mergesort(a):
      if len(a) <= 1:
          return a
      mid = len(a)//2
      left = mergesort(a[:mid])
      right = mergesort(a[mid:])
      return merge(left, right)
  (Here choices about slicing, recursion depth, and library functions affect performance and memory.)
- Machine execution level: the Python interpreter or compiled bytecode executes instructions that manipulate memory, call functions, allocate objects — CPU executes machine code, uses caches and RAM, and consumes cycles; these physical realities determine the actual running time and memory footprint.

Seeing the same task at these different levels lets you reason about correctness at the algorithm level, implement and debug at the program level, and optimize hotspots at the machine level — all without being overwhelmed by irrelevant details.