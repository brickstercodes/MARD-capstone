# Study Guide: Core Concepts in Computing (Dependency Order)

This guide presents foundational concepts in an order that builds on prior ideas. For each concept you’ll find: (a) a plain-language explanation, (b) why it matters, and (c) a single quick example or mental model to make it concrete.

---

## 1. Numbers and number systems (Arabic numerals, place value, zero)
- Plain-language explanation  
  Numbers are symbolic systems we use to represent quantities. The Arabic numeral system (0, 1, 2, 3, …) includes a symbol for zero and uses place value — the position of a digit determines its weight (ones, tens, hundreds, etc.). This combination makes arithmetic compact and scalable.
- Why it matters  
  Modern calculation, algorithms, and digital computing depend on efficient numeric notation. The introduction of zero and place value let people perform and reason about arithmetic more systematically than earlier physical tools.
- Quick example / mental model  
  Think of place value like parking lanes: a car in the “tens” lane counts for ten cars, while a car in the “ones” lane counts as one. Zero is an empty lane marker that lets you keep positions clear (e.g., 105 vs 15).

---

## 2. Algorithm (definition)
- Plain-language explanation  
  An algorithm is a precise sequence of instructions that transforms inputs into outputs through a finite series of steps. It’s a recipe for solving a problem or performing a computation.
- Why it matters  
  Algorithms are the core of computing: they tell hardware what to do. Understanding algorithms is essential to designing correct, efficient solutions for tasks from arithmetic to web services.
- Quick example / mental model  
  A baking recipe is an algorithm: given ingredients (inputs) and ordered instructions (steps), you produce a cake (output). The recipe must be clear and finite so anyone can follow it.

---

## 3. Computational thinking
- Plain-language explanation  
  Computational thinking is the habit of approaching problems as computations: breaking problems into parts, designing algorithms, recognizing patterns, and thinking about efficiency and correctness.
- Why it matters  
  It’s the mindset that lets you map real-world problems into algorithms and systems. Computational thinking is used across disciplines (science, business, education) to structure complex tasks.
- Quick example / mental model  
  When planning a road trip, you break the trip into legs, choose fastest routes, schedule stops — that’s decomposing a problem, searching options, and optimizing, all hallmarks of computational thinking.

---

## 4. Sorted data / sorted array
- Plain-language explanation  
  A sorted array is a list of items arranged in order (e.g., ascending numbers). Sorting organizes data so that certain operations — like searching — become much faster.
- Why it matters  
  Many efficient algorithms rely on sorted data. Sorting enables faster lookups, range queries, and supports algorithms that exploit order for performance gains.
- Quick example / mental model  
  A phone book sorted by last name: to find "Smith" you go to the S section instead of scanning every entry. That order makes the search far quicker.

---

## 5. Everyday algorithms (recipes analogy)
- Plain-language explanation  
  Everyday procedures — like cooking recipes, assembly instructions, or a checklist — are practical algorithms: explicit steps that, when followed, yield a predictable result.
- Why it matters  
  Framing familiar activities as algorithms helps demystify computing. It shows algorithms aren’t only abstract math but are present in daily life and can be improved or debugged.
- Quick example / mental model  
  A recipe lists ingredients and sequential steps (mix, bake, cool). If you follow them precisely, you get the dish; if you omit a step, you can debug the outcome just like a program.

---

## 6. Logarithms
- Plain-language explanation  
  A logarithm answers the question: “To what power must one number be raised to get another?” Logarithms convert multiplicative relationships into additive ones, simplifying many calculations.
- Why it matters  
  Logarithms historically reduced tedious calculations and enabled early analog calculators. In computing they appear in algorithms’ running-time analyses (e.g., binary search runs in logarithmic time).
- Quick example / mental model  
  If 2^3 = 8, then log base 2 of 8 is 3. Think of logarithms like counting doublings: how many times must you double 1 to reach a target?

---

## 7. Abacus (early physical calculators)
- Plain-language explanation  
  The abacus is a simple physical counting device that helps people tally, add, and perform basic arithmetic by moving beads or counters.
- Why it matters  
  It was one of the earliest general-purpose calculation tools used globally. The abacus shows how humans externalized computation before symbolic number systems and electronic calculators.
- Quick example / mental model  
  Visualize an abacus row as place-value lanes: beads moved in the tens lane add ten at a time, resembling how place value organizes numbers but limited compared to numeral notation with zero.

---

## 8. Binary search (example algorithm)
- Plain-language explanation  
  Binary search finds a target value in a sorted array by repeatedly halving the search interval: compare to the middle element, then continue in the lower or upper half until found or empty.
- Why it matters  
  Binary search is a classic efficient search algorithm with logarithmic time complexity. It demonstrates how using structure (sorted order) yields large performance gains.
- Quick example / mental model  
  Searching for a word in a dictionary: open near the middle; decide whether to go earlier or later; repeat halving until you find the word.

---

## 9. Dynamic programming
- Plain-language explanation  
  Dynamic programming is a method for solving complex problems by breaking them into overlapping subproblems, solving each once, and storing results for reuse.
- Why it matters  
  It turns expensive repeated computation into efficient reuse, enabling solutions to many optimization and decision problems that would otherwise be infeasible.
- Quick example / mental model  
  Climbing stairs where each step depends on previous steps: compute the number of ways up to step n by combining results for earlier steps and cache them instead of recomputing every time.

---

## 10. Charles Babbage's Difference Engine and Analytical Engine
- Plain-language explanation  
  Charles Babbage designed mechanical calculating machines: the Difference Engine automated polynomial and tabular calculation; the later Analytical Engine introduced general program control, memory, and arithmetic logic.
- Why it matters  
  These designs anticipated key computer elements: automation of calculation, stored data, and program-controlled operation — early blueprints for programmable machines.
- Quick example / mental model  
  Think of the Difference Engine as a specialized automatic calculator and the Analytical Engine as an early computer concept with separate storage (memory) and a processing unit executing stored instructions.

---

## 11. Punched cards (early input/program medium)
- Plain-language explanation  
  Punched cards encoded information by holes in specific positions; machines read these holes to input data or control sequences of operations.
- Why it matters  
  Punched cards were a practical way to store and feed both data and program instructions to mechanical and early electronic machines, enabling automation and repeatable processing.
- Quick example / mental model  
  Imagine a paper tape where the pattern of holes tells a machine which step to perform next—each card is one line of code or a chunk of data.

---

## 12. Ada Lovelace (first programmer)
- Plain-language explanation  
  Ada Lovelace worked with Babbage on the Analytical Engine and wrote sequences (using punched cards) that described how the machine could be instructed to perform computations; she is often credited as the first programmer.
- Why it matters  
  Her work showed that machines could be programmed with sequences to carry out complex calculations and foreshadowed the idea of software as separate from hardware.
- Quick example / mental model  
  Lovelace’s punched-card sequences are like an early program: a human-readable plan encoded into a medium the machine can execute step-by-step.

---

## 13. Herman Hollerith and punched-card tabulation
- Plain-language explanation  
  Herman Hollerith built a machine that punched and counted cards to tabulate census data; his system automated large-scale statistical processing for the 1890 U.S. census.
- Why it matters  
  Hollerith’s invention demonstrated how automating data recording and counting could scale information processing and laid groundwork for business machines and later computing companies.
- Quick example / mental model  
  Think of sorting stacks of punch cards by hole patterns to quickly count people by category instead of manual tallying — mechanized data aggregation.

---

## 14. Program / programming language
- Plain-language explanation  
  A program is an algorithm represented as a sequence of symbolic instructions that a computer can execute. A programming language is the set of symbols and rules used to write those instructions in a form the machine (or tools) can interpret.
- Why it matters  
  Programs are how humans specify computations for hardware. Programming languages make expression, modification, and sharing of algorithms practical and standardized.
- Quick example / mental model  
  A program is like a recipe written in a particular notation (language). Different languages are like recipe formats — some are terse and machine-oriented; others are more human-friendly.

---

## 15. Hardware components of a computer (processor, memory, network, storage)
- Plain-language explanation  
  Hardware comprises the physical parts that make computation possible: the processor executes instructions; memory stores data and instructions for quick access; storage holds data persistently; network connects devices to share information.
- Why it matters  
  Knowing these components clarifies how software and algorithms run in real machines and how system design choices affect performance, capacity, and communication.
- Quick example / mental model  
  Compare a computer to a kitchen: the processor is the cook, memory is the counter with ingredients being used now, storage is the pantry, and the network is the courier delivering supplies or sharing dishes.

---

## 16. Material basis of hardware (silicon, lithium, vacuum tubes)
- Plain-language explanation  
  Computer hardware depends on physical materials: modern electronics rely on silicon semiconductors and lithium in batteries; earlier machines used vacuum tubes to represent binary states.
- Why it matters  
  Physical materials determine what kinds of devices and performance are possible; changes in materials (e.g., from vacuum tubes to silicon) enabled huge leaps in speed, size, and energy use.
- Quick example / mental model  
  Vacuum tubes behaved like on/off “light bulbs” for early memory; replacing them with silicon transistors is like replacing room-sized lightbulbs with tiny, energy-efficient LEDs to miniaturize and speed up computation.

---

## 17. ENIAC and vacuum-tube computers
- Plain-language explanation  
  ENIAC was an early general-purpose digital computer built with vacuum tubes. It could execute many programs, not just a single fixed task, and was programmed and operated in large physical rooms.
- Why it matters  
  ENIAC demonstrated that programmable electronic machines could replace manual calculation at scale; it is historically notable as a forerunner of modern digital computers.
- Quick example / mental model  
  Imagine a room full of thousands of lightbulb-like vacuum tubes wired to perform arithmetic; reconfiguring connections and settings let operators run different computations.

---

## 18. Software
- Plain-language explanation  
  Software is the collection of instructions (programs) and data that tell hardware how to perform tasks. It abstracts and implements algorithms so the physical machine can carry them out.
- Why it matters  
  Software turns raw hardware into useful systems: everything from small scripts to large web applications is software that shapes user experiences and societal functions.
- Quick example / mental model  
  Hardware is like musical instruments; software is the sheet music and conductor telling the instruments what to play and when.

---

## 19. Turing machine and formalization of computation
- Plain-language explanation  
  The Turing machine is a mathematical model that formalizes what it means to compute: an abstract device with a tape and rules that manipulates symbols step by step. It captures the essence of algorithms and computation.
- Why it matters  
  This formal model provides a rigorous way to reason about what problems can be computed, how algorithms behave, and forms the foundations of theoretical computer science.
- Quick example / mental model  
  Picture a tape with symbols and a head that reads, writes, and moves according to rules — a simplified, idealized computer for proving what computation is possible.

---

## 20. Turing-completeness (computational universality)
- Plain-language explanation  
  A system is Turing-complete if it can simulate a Turing machine — meaning it can perform any computation that any other programmable system can, given enough time and memory.
- Why it matters  
  Turing-completeness identifies general-purpose computing systems versus specialized devices. It underpins the idea that many different machines (old or new) can, in principle, compute the same things.
- Quick example / mental model  
  A modern PC and the ENIAC differ vastly in speed, but both are Turing-complete: with enough time, both could simulate the same algorithms even if one is much slower.

---

## 21. Theoretical computer science (decidability, complexity, efficiency)
- Plain-language explanation  
  Theoretical computer science studies the mathematical limits and properties of computation: what problems are solvable (decidability), how resources (time, memory) scale (complexity), and how to make computations efficient.
- Why it matters  
  It tells us which problems are inherently impossible, which are feasible, and which need clever algorithms or more resources — guiding practical system design and research.
- Quick example / mental model  
  Like a map that shows which roads are passable and which are blocked, theory tells programmers whether a computational “destination” exists and how long the trip might take.

---

## 22. Software engineering
- Plain-language explanation  
  Software engineering applies engineering principles to design, build, test, and maintain reliable, efficient, and maintainable software systems at scale.
- Why it matters  
  Good engineering practices are essential to make complex software systems that meet performance, scalability, and correctness needs in real-world contexts.
- Quick example / mental model  
  Building a large application is like constructing a building: you need architecture, standards, testing, and maintenance plans — not just individual code snippets.

---

## 23. Computational science
- Plain-language explanation  
  Computational science uses algorithms, models, and computing power to perform scientific experiments, simulations, and numerical analysis across disciplines like weather, engineering, and medicine.
- Why it matters  
  It enables scientific inquiry that would be impossible by hand, allowing simulations of complex systems and data-driven discovery at large scales.
- Quick example / mental model  
  Weather forecasting uses mathematical models and large-scale computation to predict future conditions — computational science turns equations into actionable forecasts.

---

## 24. Distributed computing and high-performance resources
- Plain-language explanation  
  Distributed computing spreads computation across many machines; high-performance resources (clusters, supercomputers) provide the scale needed for large simulations or data processing.
- Why it matters  
  Some scientific and data problems require more memory and CPU than one machine can provide; distributing work makes it feasible and faster.
- Quick example / mental model  
  Solving a massive puzzle faster by having many people each work on different sections and share partial results, instead of one person doing it all.

---

## 25. Data science
- Plain-language explanation  
  Data science combines computing, statistics, and domain knowledge to extract insights from data — organizing, processing, analyzing, and communicating information for decisions.
- Why it matters  
  It’s central to modern business, research, and policy: turning raw measurements into actionable knowledge (recommendations, predictions, diagnoses).
- Quick example / mental model  
  A data scientist examining customer click logs to detect buying patterns and recommend products is turning noisy logs into strategic insights.

---

## 26. Spreadsheets as data-centric programming environments
- Plain-language explanation  
  Spreadsheets present computation centered on data: cells contain values and formulas, making programming approachable by manipulating tables visually rather than writing code.
- Why it matters  
  Millions use spreadsheets as de facto programming tools for analysis and decision-making. They make computation accessible but have limits (scale, data typing, error detection).
- Quick example / mental model  
  A budget spreadsheet where formulas compute totals and projections: non-programmers “program” calculations by arranging cells and formulas.

---

## 27. Big data (very large datasets)
- Plain-language explanation  
  Big data refers to datasets so large or complex that traditional tools (like spreadsheets) struggle to store, process, or analyze them efficiently.
- Why it matters  
  Many modern applications (web logs, sensor streams, genomics) generate massive data whose scale requires specialized storage, processing frameworks, and algorithms.
- Quick example / mental model  
  Tracking every web click for millions of users produces volumes beyond a spreadsheet’s capacity — you need databases, parallel processing, and scalable tools.

---

## 28. Machine learning (ML) as a subset of AI
- Plain-language explanation  
  Machine learning is a set of techniques that enable computers to improve performance on tasks by learning patterns from data. It’s a major part of artificial intelligence.
- Why it matters  
  ML automates pattern detection and prediction, powering applications like fraud detection, recommendations, and image recognition that are hard to program by rules.
- Quick example / mental model  
  Train a model on labeled transaction data so it learns the difference between fraudulent and legitimate purchases, then use it to flag suspicious activity automatically.

---

## 29. Artificial intelligence (AI)
- Plain-language explanation  
  AI is the field that builds systems to perform tasks that typically require human intelligence (perception, decision-making), often using machine learning and algorithmic architectures.
- Why it matters  
  AI enables automation and augmentation of complex tasks across domains, creating powerful new tools as well as ethical, social, and policy challenges.
- Quick example / mental model  
  An AI system that classifies images or suggests diagnostic tests is performing tasks that previously relied on human expertise.

---

## 30. Neural networks (AI architecture)
- Plain-language explanation  
  Neural networks are AI architectures inspired by brain networks: layers of interconnected artificial “neurons” whose numeric parameters are adjusted through training to recognize patterns.
- Why it matters  
  They excel at learning hierarchical features from large datasets and have powered recent advances in image, speech, and language tasks.
- Quick example / mental model  
  Early layers detect simple patterns (edges), middle layers combine edges into shapes, and deeper layers recognize objects — like assembling a picture from parts.

---

## 31. Image recognition (AI application)
- Plain-language explanation  
  Image recognition is the AI task of identifying objects, people, or other entities within images; modern approaches use neural networks to learn visual patterns from many examples.
- Why it matters  
  It’s a core capability for applications like medical imaging, autonomous vehicles, and agricultural robots, enabling automated visual decision-making.
- Quick example / mental model  
  An agricultural robot takes photos, a trained model labels each plant as crop or weed, and the robot decides whether to spray or spare it.

---

## 32. Adversarial attacks on ML systems
- Plain-language explanation  
  Adversarial attacks are deliberately crafted inputs designed to make machine-learning models behave incorrectly — for example, slight image changes causing misclassification.
- Why it matters  
  They expose vulnerabilities in AI systems and raise safety, security, and trust issues for deployment in critical domains.
- Quick example / mental model  
  Tweaking a single pixel or color in an image can trigger a neural network to misidentify an object — like adding a tiny sticker to a stop sign that confuses an automated detector.

---

## 33. Information science
- Plain-language explanation  
  Information science studies how information is created, organized, managed, and used in social and organizational contexts, including technologies and human interactions.
- Why it matters  
  It situates computing within societies, helping design information systems that serve people, organizations, and public needs responsibly.
- Quick example / mental model  
  Libraries evolving to digital catalogs and search systems are information-science problems: how to classify, retrieve, and present knowledge effectively.

---

## 34. Bioinformatics / DNA as information
- Plain-language explanation  
  Bioinformatics treats biological sequences like DNA as informational data. Computational methods process, compare, and interpret genomic data for biology and medicine.
- Why it matters  
  Sequencing and analysis of DNA enable personalized medicine, disease detection, and biological discovery — all reliant on algorithms, data structures, and hardware.
- Quick example / mental model  
  Sequencing a virus’s genome produces a long string of symbols; algorithms index and match these signatures to identify pathogens.

---

## 35. Human-Computer Interaction (HCI)
- Plain-language explanation  
  HCI studies how people interact with computers and designs interfaces that make technology usable, accessible, and effective for diverse users.
- Why it matters  
  Good HCI ensures that systems meet human needs, reducing errors and improving adoption; it centers social and cognitive aspects of computing.
- Quick example / mental model  
  Designing a clean, understandable app layout so users can accomplish tasks without confusion is an HCI exercise.

---

## 36. Computer science education (pedagogy and curricular history)
- Plain-language explanation  
  Computer science education examines how people learn computing and how curricula, tools, and pedagogies are designed — from LOGO’s learning-through-doing to modern degree programs.
- Why it matters  
  Teaching choices shape who becomes a computing professional and what skills are emphasized; historical biases have influenced curriculum focuses.
- Quick example / mental model  
  LOGO’s turtle encouraged learning geometry by programming movement; this is an example of designing education that leverages computation to teach other subjects.

---

## 37. Interdisciplinarity of computer science and subfield taxonomy
- Plain-language explanation  
  Computer science overlaps many fields (math, engineering, domain sciences). A common taxonomy divides the field into theoretical CS, computer systems, and applied CS (including HCI, software engineering).
- Why it matters  
  Understanding this structure clarifies how different perspectives (theory, systems, applications) contribute and where collaboration across disciplines is needed.
- Quick example / mental model  
  Building weather models requires algorithms (theory), large machines and networks (systems), and application-specific knowledge (applied CS) — all working together.

---

## 38. Responsible computing / ethics in computing
- Plain-language explanation  
  Responsible computing emphasizes designing, deploying, and governing computing systems with attention to social impacts, fairness, privacy, and safety.
- Why it matters  
  Computing technologies affect lives at scale; ethical practice helps prevent harm, bias, and unintended social consequences.
- Quick example / mental model  
  Considering whether a loan-approval model discriminates across groups and adjusting data and design to reduce unfair outcomes is responsible computing in action.

---

## 39. Y2K (millennium bug) as an ethical/engineering lesson
- Plain-language explanation  
  Y2K was a problem caused by storing years using only two digits; it highlights how short-term engineering choices can produce large systemic risks later.
- Why it matters  
  It teaches the importance of foresight, proper design, and accountability when building systems that persist and interact across society.
- Quick example / mental model  
  Storing "99" for 1999 saved memory early on but risked ambiguity in 2000 — like labeling binders without full dates and later losing track of which century each refers to.

---

## 40. Social determination of technology
- Plain-language explanation  
  The social determination of technology is the idea that technology’s design and effects are shaped by social forces and values rather than being neutral tools.
- Why it matters  
  Recognizing this helps designers see how choices embed values and can reproduce or challenge social inequalities.
- Quick example / mental model  
  An algorithm trained on biased historical data will reproduce those biases unless designers intervene — so the technology reflects social inputs, not neutrality.

---

## 41. Design Justice and 'build with, not for' principle
- Plain-language explanation  
  Design Justice advocates involving marginalized communities in the design process — building solutions with those affected rather than imposing solutions for them.
- Why it matters  
  It produces more equitable, appropriate technologies and reduces harm from top-down designs that misunderstand users’ contexts.
- Quick example / mental model  
  Instead of designing an education app for a community from afar, co-design workshops bring teachers and students into the process so the tool fits real classroom needs.

---

## 42. Digital divide
- Plain-language explanation  
  The digital divide is the uneven access to technology and connectivity across populations due to geography, income, infrastructure, or other factors.
- Why it matters  
  Unequal access limits educational, economic, and social opportunities; technologies can widen or help bridge inequalities depending on design and deployment.
- Quick example / mental model  
  Communities lacking high-speed Internet can’t use cloud-based educational platforms effectively, creating gaps in learning access.

---

## 43. Computing for global development
- Plain-language explanation  
  Computing for global development focuses on designing technologies that address resource constraints and cultural contexts in low-income and underserved regions.
- Why it matters  
  Solutions that work in wealthy contexts often fail elsewhere; context-sensitive design is required to produce sustainable, useful technologies for diverse settings.
- Quick example / mental model  
  A data-collection app designed to work offline and sync when intermittent connectivity is available matches real constraints in many regions.

---

## 44. One Laptop Per Child (OLPC) critique and context-sensitive design
- Plain-language explanation  
  The OLPC initiative aimed to distribute low-cost laptops to children in the Global South; critiques note failures due to infrastructure, curriculum, and contextual mismatches.
- Why it matters  
  The case illustrates how technology deployment without local grounding can produce disappointing outcomes and stresses the need for holistic design.
- Quick example / mental model  
  Giving rugged laptops to a school without reliable electricity or teacher support is like giving gardening tools without soil or a gardener — tools alone won’t create the intended change.

---

## 45. Computers and racial justice / marginalized contributions (Hidden Figures, Black Software)
- Plain-language explanation  
  Computing’s history includes important contributions from marginalized groups (e.g., Black women at NASA) and cultural movements that used computing for community purposes; many stories have been overlooked.
- Why it matters  
  Recognizing diverse contributions corrects historical erasure, broadens role models, and reveals how technology both reflects and shapes power dynamics.
- Quick example / mental model  
  Human "computers" at NASA performed critical calculations for spaceflight; highlighting their work shows the human labor behind early computing achievements.

---

## 46. H-1B visas and global workforce implications
- Plain-language explanation  
  H-1B visas enable employers to recruit skilled workers from other countries for specialized roles (like computer science), addressing domestic labor shortages.
- Why it matters  
  The program affects global talent flows, workforce composition, and access to opportunities for international professionals — it’s an economic and policy lever in computing sectors.
- Quick example / mental model  
  A company hiring an overseas data scientist under an H-1B visa brings expertise it can’t find locally to build products that have global reach.

---

## 47. Targeted advertising and privacy/ethical concerns
- Plain-language explanation  
  Targeted advertising uses user data (e.g., browsing history) to personalize ads. While commercially powerful, it raises privacy, transparency, and political concerns.
- Why it matters  
  Targeting can influence behavior, shape democratic discourse, and exploit vulnerable populations; ethical oversight and transparency are essential.
- Quick example / mental model  
  Political campaigns placing microtargeted ads to narrow audiences that disappear after the fact is like whispering different messages to separate groups without public scrutiny.

---

## 48. Limits of computation vs human strengths (emotion, moral judgment, chaos)
- Plain-language explanation  
  Computation excels at pattern recognition and scale, but humans outperform machines in nuanced emotional understanding, moral reasoning, and handling chaotic, unpredictable systems.
- Why it matters  
  Knowing these limits helps decide when AI should assist, not replace, humans — and where human judgment or scientific humility is essential.
- Quick example / mental model  
  A machine might detect sentiment trends in text, but a human is better at interpreting empathy in a complex, context-rich conversation or making moral trade-offs.

---

## 49. Foundational technologies and co-evolution (AI, architectures, specialized hardware)
- Plain-language explanation  
  Foundational technologies (like algorithms, AI architectures, and specialized hardware) co-evolve: advances in one area (hardware speed, network scale) enable innovations in others (neural networks), and vice versa.
- Why it matters  
  Breakthroughs often depend on layered advances — hardware changes (e.g., specialized chips) can make new algorithms practical, and new algorithms can motivate new hardware designs.
- Quick example / mental model  
  Neural networks grew practical as larger datasets and faster or specialized hardware became available; it’s like powerful engines and better fuel together enabling faster cars and new driving techniques.

---

End of guide. Use this ordered map of concepts to build deeper study: each entry assumes earlier concepts as background, so review earlier items if something seems unfamiliar.