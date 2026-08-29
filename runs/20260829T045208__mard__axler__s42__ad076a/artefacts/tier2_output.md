Definition and axioms

Let F be a field (for example R or C). A vector space V over F is a set equipped with two operations:
- vector addition: + : V × V → V, written u + v,
- scalar multiplication: · : F × V → V, written a v or a·v,

that satisfy the following axioms for all u, v, w in V and all scalars a, b in F.

1. (Additive closure) u + v is in V.
2. (Additive commutativity) u + v = v + u.
3. (Additive associativity) (u + v) + w = u + (v + w).
4. (Additive identity) There exists 0 in V such that 0 + v = v for all v.
5. (Additive inverse) For each v there exists −v in V with v + (−v) = 0.
6. (Scalar closure) a v is in V for every a in F and v in V.
7. (Compatibility of scalar multiplication) (ab) v = a (b v).
8. (Identity scalar) 1 v = v, where 1 is the multiplicative identity in F.
9. (Distributivity over vector addition) a (u + v) = a u + a v.
10. (Distributivity over scalar addition) (a + b) v = a v + b v.

(One can view axioms 1–5 as saying V is an abelian group under addition, and 6–10 as the interaction rules between F and V.)

Standard examples and verification

A. F^n (column vectors with entries in F)

Definition of the set and operations:
- The set: F^n = {(x1, …, xn) : xi ∈ F}.
- Addition: coordinatewise: (x1,…,xn) + (y1,…,yn) = (x1+y1, …, xn+yn).
- Scalar multiplication: coordinatewise: a(x1,…,xn) = (a x1, …, a xn).

Verification of axioms (sketch):
- Closure (addition and scalar multiplication): sums and scalar multiples of tuples have coordinates in F, so stay in F^n.
- Commutativity and associativity of addition: follow from commutativity/associativity in F applied coordinatewise.
- Additive identity: 0 = (0,…,0) works because 0 + xi = xi coordinatewise.
- Additive inverse: for v = (x1,…,xn), −v = (−x1,…,−xn) since xi + (−xi) = 0 in F.
- Compatibility (ab)v = a(bv): coordinatewise (ab) xi = a(b xi).
- Identity scalar: 1 v = (1·x1,…,1·xn) = v.
- Distributivity a(u+v) = au + av and (a+b)v = av + bv: check coordinatewise using distributivity in F.

Thus F^n with coordinatewise addition and scalar multiplication is a vector space over F.

B. Function space F^S (all functions from a set S to F)

Definition:
- The set: F^S = {f : S → F}.
- Addition: (f + g)(s) = f(s) + g(s) for all s ∈ S (pointwise addition).
- Scalar multiplication: (a f)(s) = a · f(s) for all s ∈ S (pointwise scalar multiplication).

Verification (sketch):
- Closure: f + g and a f are functions S → F because for each s the pointwise sum and scalar multiple lie in F.
- Additive commutativity and associativity: for each s, (f+g)(s) = f(s)+g(s) = g(s)+f(s) and similarly for associativity, using the field laws at each s.
- Additive identity: the zero function 0 defined by 0(s) = 0_F for all s satisfies 0 + f = f.
- Additive inverse: for f, define (−f)(s) = −(f(s)); then f + (−f) = 0 pointwise.
- Scalar laws: verify (ab)f, 1 f, a(f+g), and (a+b)f hold pointwise because they hold in F for each s.

Examples of function spaces:
- R^R (all real-valued functions on R) is a vector space over R with pointwise operations.
- The set of polynomials with coefficients in F (identified with suitable functions or sequences) is a subspace of F^S for S = F or S = N.

Distinguishing addition and scalar multiplication

In every example, emphasize that addition is an operation V × V → V combining two vectors, while scalar multiplication is an operation F × V → V combining a scalar and a vector. They are distinct operations with different types of inputs and different axioms governing them (e.g., addition has commutativity and inverses; scalar multiplication needs compatibility with field multiplication and distributivity laws). In F^n and F^S these operations are defined pointwise/coordinately, so verification reduces to checking the field axioms coordinatewise or pointwise.

Span, Linear Combinations, and Generating Sets

Definitions
- Linear combination: Given a vector space V over a field F and vectors v1, ..., vk in V, a linear combination of v1,...,vk is any vector of the form a1 v1 + a2 v2 + ... + ak vk where a1,...,ak are scalars in F.
- Span: For a subset S ⊆ V, the span of S, written span(S) or ⟨S⟩, is the set of all linear combinations of vectors from S:
  span(S) = {a1 v1 + ... + ak vk : k ≥ 0, vi ∈ S, ai ∈ F}.
  (The case k = 0 gives the zero vector, so span(∅) = {0}.)
- Generating set (or spanning set): A subset S of V is called a generating set of V (or S generates V, or S spans V) if span(S) = V. If span(S) = W for some subspace W ⊆ V, we say S generates the subspace W.

Basic facts
- span(S) is always a subspace of V.
- span(S) is the smallest subspace of V that contains S: any subspace containing S must also contain span(S).
- If S ⊆ T then span(S) ⊆ span(T).
- span({v}) for a nonzero v is the one-dimensional subspace {a v : a ∈ F} (a line through 0).
- span(∅) = {0}.

Computing spans (concrete examples)
1) R^2: Let S = {(1,0), (0,1)}. Any (x,y) ∈ R^2 equals x(1,0) + y(0,1), so span(S) = R^2. Thus S generates R^2.

2) Collinear vectors: S = {(1,1), (2,2)} ⊆ R^2. Note (2,2) = 2(1,1), so every linear combination a(1,1) + b(2,2) = (a+2b)(1,1). Therefore span(S) = {c(1,1) : c ∈ R}, the line through (1,1). S does not generate R^2.

3) Subspace in R^3: S = {(1,0,0), (0,1,0)}. Any (x,y,z) with z = 0 can be written as x(1,0,0) + y(0,1,0), so span(S) = {(x,y,0) : x,y ∈ R}, the xy-plane in R^3.

4) Polynomials: In P3 (polynomials of degree ≤ 3), let S = {1, x, x^2}. Then span(S) is the subspace of all polynomials of degree ≤ 2. For example, 3 + 2x − x^2 = 3·1 + 2·x + (−1)·x^2.

Deciding whether a vector is in a span (method)
- To test if w ∈ span(S) where S = {v1,...,vk}, set up the equation a1 v1 + ... + ak vk = w and solve for scalars a1,...,ak. If a solution exists, w is in the span; otherwise it is not.
- This reduces to solving a linear system (coordinate-wise equations) when V has coordinates (like R^n) or equating coefficients for polynomial/vector-function spaces.

Example check: Is w = (3,1) in span{(1,0),(1,1)}?
Solve a(1,0) + b(1,1) = (3,1) ⇒ (a+b, b) = (3,1) ⇒ b = 1, a + 1 = 3 ⇒ a = 2. Solution exists, so w is in the span.

Generating sets and minimality
- A generating set for a subspace W is any S with span(S) = W. Generating sets need not be minimal; redundant vectors can be removed if they are linear combinations of others.
- A minimal generating set that is also linearly independent is a basis. (This is the next step beyond generating sets.)

Summary of the idea
- Linear combinations create new vectors from a given set.
- The span of a set collects all such combinations and is the subspace that the set generates.
- Determining spans is done by expressing target vectors as linear combinations or solving the corresponding linear system.

Linear independence and dependence

Definition (unique-zero-coefficients). A list of vectors v1, …, vn in a vector space V is called linearly independent if the only scalars a1, …, an ∈ F for which
a1 v1 + ··· + an vn = 0
are a1 = ··· = an = 0. If there exists a nontrivial choice of scalars (not all zero) giving the zero vector, the list is linearly dependent.

Immediate consequences and tests
- Any list containing the zero vector is linearly dependent, because 1·0 + 0·(others) = 0 gives a nontrivial relation.
- To test a concrete list in a finite-dimensional coordinate space, set up the linear system for the coefficients and check whether only the trivial solution exists. In practice this means forming a matrix whose columns are the vectors and row-reducing to check for free variables.
- A single nonzero vector is independent; a single zero vector is dependent.

Examples
1) R^2: v1 = (1, 0), v2 = (0, 1). Solve a1 v1 + a2 v2 = 0 ⇒ (a1, a2) = (0, 0). So {v1, v2} is linearly independent.

2) R^3: v1 = (1, 2, 3), v2 = (2, 4, 6), v3 = (0, 1, 0). Observe v2 = 2 v1, so take a1 = 2, a2 = −1, a3 = 0 to get 0. Hence {v1, v2, v3} is linearly dependent.

3) Polynomials in P2: p1(x) = 1 + x, p2(x) = 1 − x, p3(x) = x. Solve a1 p1 + a2 p2 + a3 p3 = 0 (the zero polynomial). Writing coefficients of 1 and x gives:
a1 + a2 = 0, a1 − a2 + a3 = 0.
These force a1 = a2 = a3 = 0, so {p1, p2, p3} is independent.

Equivalent characterization (dependence via span)
The list v1, …, vn (n ≥ 1) is linearly dependent if and only if some vi is in the span of the remaining vectors {v1, …, vi−1, vi+1, …, vn}.

Proof sketch:
- If some vi is in the span of the others, vi = c1 v1 + ··· + ci−1 vi−1 + ci+1 vi+1 + ··· + cn vn. Rearranging gives a nontrivial linear relation, so the list is dependent.
- Conversely, if the list is dependent there exist scalars not all zero with a1 v1 + ··· + an vn = 0. Pick an index j with aj ≠ 0; then vj = (−1/aj)(a1 v1 + ··· + aj−1 vj−1 + aj+1 vj+1 + ··· + an vn), so vj is a linear combination of the others.

Use of the characterization
- This characterization gives a quick way to spot dependence: if any vector can be written from the others, the list is dependent.
- It also shows why in a dependent list one can remove at least one vector without changing the span of the list.

Summary (key points to remember)
- Linear independence = only trivial linear relation among the list.
- Linear dependence ⇔ some vector is in the span of the others.
- To test: set up and solve the coefficient system (or look for an evident dependence such as proportional columns or a zero vector).

Section 4 — Bases as Minimal Spanning / Maximal Independent Sets

Definition reminder (informal)
- A list of vectors is a basis iff it is linearly independent and spans the space.
- Two useful equivalent ways to recognize a basis without checking both properties directly:
  1. Minimal spanning list: it spans, and removing any vector makes it stop spanning.
  2. Maximal independent list: it is independent, and adding any vector from the space makes it dependent.

Why these are equivalent to “independent + spanning” (short, informal reasoning)
- If a list is spanning but not independent, it contains a redundant vector. Using the linear dependence lemma (Chapter 1), you can remove a dependent vector and still span. Repeating gives a spanning list with no redundant vectors — exactly a minimal spanning list, and such a list must be independent. Thus a minimal spanning list is independent and so is a basis.
- If a list is independent but does not span, there exists some vector not in its span. Adding that vector preserves independence, so the original list wasn't maximal. Hence a maximal independent list must span and is a basis.

Concrete checks you can do in practice
- To verify a spanning list is a basis: try removing each vector in turn. If every removal makes the list fail to span, the list is minimal spanning and therefore a basis.
- To verify an independent list is a basis: try adding vectors (preferably simple ones or a canonical set) from the ambient space. If every new vector you add makes the set dependent, the list was maximal independent and thus a basis.

Examples

1) R^2, list L = {(1,0), (0,1), (1,1)}.
- L spans R^2 (the first two already do), but it is not minimal spanning: removing (1,1) leaves {(1,0),(0,1)} which still spans. So L is not a basis as given. Removing redundant vectors yields the basis {(1,0),(0,1)}.

2) R^2, list M = {(1,0)}.
- M is independent but not maximal: adding (0,1) gives an independent list of size 2 which now spans R^2. So M is not a basis. The maximal independent extension {(1,0),(0,1)} is a basis.

3) R^3, list N = {(1,0,0),(0,1,0),(1,1,0)}.
- N spans the xy-plane but not all of R^3, so it does not span R^3 and cannot be a maximal independent list for R^3. It is independent (none is a scalar multiple or combination of the others), but since it does not span, it is not a basis for R^3. Adding (0,0,1) gives a maximal independent list (a basis) for R^3.

4) R^3, list P = {(1,0,0),(0,1,0),(0,0,1),(1,1,1)}.
- P spans R^3 but is dependent. Check minimality: remove (1,1,1) and the remaining three still span, so P is not minimal spanning. Using dependence you can remove redundant vectors until you reach a minimal spanning set of size 3, which will be a basis.

Useful practical heuristics
- If you have more vectors than the “expected” number for the space (e.g., many more than 2 in R^2), the list is necessarily dependent; look for and remove redundancies to find a minimal spanning subset.
- If a set is independent but too small to span (e.g., one vector in R^2), try adding simple coordinate vectors; if you can add one that preserves independence, your original set was not maximal.
- Minimal spanning and maximal independent characterizations are often the quickest way to certify a basis in computations: either show every removal breaks spanning, or show every possible addition breaks independence.

Takeaway
- You can recognize a basis by checking minimal spanning or maximal independence instead of verifying both span and independence directly. Practically: remove vectors to test minimality of a spanning list; try adding vectors to test maximality of an independent list.

Subspace — definition and the subspace test

Definition
- A subset W of a vector space V (over a field F) is a subspace if W is itself a vector space under the same addition and scalar multiplication as V.
- Equivalently: W is a subspace of V when W is nonempty and closed under vector addition and scalar multiplication.

Subspace criterion (practical test)
To show W ⊆ V is a subspace, it suffices to check:
1. W ≠ ∅ (or show 0 ∈ W).
2. For all u, v ∈ W, u + v ∈ W. (closure under addition)
3. For all a ∈ F and u ∈ W, a u ∈ W. (closure under scalar multiplication)

Notes on the criterion
- Showing 0 ∈ W is usually the easiest way to establish nonemptiness.
- If you prefer a single combined check, you can verify: for all u, v ∈ W and all scalars a, b ∈ F, a u + b v ∈ W. This implies the three items above.
- If any of the three conditions fails, W is not a subspace.

Common examples and counterexamples

Examples of subspaces
- {0} and V itself are always subspaces (the trivial subspaces).
- Span(S) for any subset S ⊆ V is a subspace.
- In R^3, sets like {(x, y, 0) : x, y ∈ R} and {(t, 2t, 3t) : t ∈ R} are subspaces (planes through the origin, lines through the origin).

Common counterexamples (fail one of the conditions)
- Not closed under addition:
  - The set of vectors in R^2 with positive coordinates: {(x, y) : x > 0, y > 0}. Nonempty and closed under positive scalar multiplication, but sum of two such vectors stays positive so here addition is OK; however it fails because 0 ∉ set. A clearer example: A = {(x, y) : x ≥ 0} is nonempty and contains 0 but not closed under additive inverses (e.g., (1,0) ∈ A but −(1,0) ∉ A), so not a subspace.
- Not closed under scalar multiplication:
  - The set of polynomials of degree exactly 2 in P(F). If p has degree 2 and c = 0, cp = 0 has degree −∞ (the zero polynomial), which is not degree 2, so closure under scalar multiplication fails.
  - In R^2, the set {(1, y) : y ∈ R} (all vectors whose first coordinate equals 1). Sum of two such vectors has first coordinate 2, so not closed under addition; also scalar multiple of (1,0) by 2 gives (2,0), not in the set.
- Not containing 0:
  - The set of nonzero vectors V \ {0} is not a subspace because 0 ∉ set.
- Union of subspaces:
  - The union of two subspaces is not necessarily a subspace (unless one subspace contains the other). Example: in R^2, let U = x-axis and W = y-axis. U ∪ W is not a subspace because (1,0) and (0,1) are in U ∪ W but their sum (1,1) is not.
- Intersections and sums:
  - The intersection of any collection of subspaces is always a subspace.
  - The sum (U + W = {u + w : u ∈ U, w ∈ W}) is a subspace.

Checklist to use on a given subset W ⊆ V
1. Is 0 ∈ W? If no → not a subspace.
2. Pick arbitrary u, v ∈ W. Is u + v ∈ W? If no → not a subspace.
3. Pick arbitrary scalar a ∈ F and u ∈ W. Is a u ∈ W? If no → not a subspace.
4. If all yes → W is a subspace.

Keep these typical counterexamples in mind when testing subsets: exclude ones that require a fixed nonzero coordinate, require a specific degree (exact degree), remove the zero vector, or are unions of distinct subspaces. These failures correspond directly to violations of the subspace criterion.

Sum of subspaces
- Let V be a vector space and U1, U2, ..., Um subspaces of V. The sum U1 + U2 + ... + Um is the set of all finite sums of vectors from the Ui:
  U1 + ... + Um = {u1 + u2 + ... + um : ui ∈ Ui for each i}.
- For two subspaces U and W, U + W = {u + w : u ∈ U, w ∈ W}.

Direct sum (definition and notation)
- The sum U1 + ... + Um is called a direct sum, written
  U1 ⊕ U2 ⊕ ... ⊕ Um,
  if every vector v in the sum has a unique representation v = u1 + u2 + ... + um with ui ∈ Ui.
- For two subspaces U and W, U ⊕ W means U + W and uniqueness of decomposition u + w for u ∈ U, w ∈ W.

Equivalent tests for directness
- Uniqueness test: U1 + ... + Um is direct iff whenever
  u1 + u2 + ... + um = 0 (with ui ∈ Ui),
  then u1 = u2 = ... = um = 0.
  (If the zero sum forces all components to be zero, then every representation is unique.)
- Intersection test (two subspaces): For U and W, U + W is a direct sum (U ⊕ W) iff U ∩ W = {0}.
- Intersection test (more than two): U1 + ... + Um is direct iff for each i,
  Ui ∩ (sum of the others) = {0}.
  Equivalently, no nonzero vector of any Ui can be written as a sum of vectors from the remaining Uj.

Dimension rule
- If U and W are finite-dimensional subspaces of V then
  dim(U + W) = dim U + dim W − dim(U ∩ W).
  In particular, U ⊕ W iff dim(U + W) = dim U + dim W (since dim(U ∩ W) = 0).

Simple computations / examples
1) R^2, standard coordinate subspaces
- Let U = span{(1,0)}, W = span{(0,1)}. Then U + W = R^2 and U ∩ W = {0}, so R^2 = U ⊕ W. Every (a,b) has the unique decomposition (a,0)+(0,b).

2) R^2, same line twice
- Let U = W = span{(1,0)}. Then U + W = span{(1,0)} but U ∩ W = U (nontrivial), so the sum is not direct. For example (1,0) = (1,0)+0 = 0+(1,0), nonunique.

3) R^2, two distinct lines through origin
- Let U = span{(1,1)}, W = span{(1,−1)}. Solve a(1,1) = b(1,−1) ⇒ a=b and a=−b ⇒ a=b=0, so U ∩ W = {0}. Hence U + W = R^2 and the sum is direct: R^2 = U ⊕ W.

4) Polynomials
- Let P2 be polynomials of degree ≤2. Let U = span{1, x}, W = span{x^2}. Then P2 = U ⊕ W because every p(x)=a+bx+cx^2 has a unique decomposition (a+bx) + (cx^2), and U ∩ W = {0}.

How to test a given decomposition
- Given subspaces Ui and a candidate decomposition V = U1 + ... + Um:
  1. Check that every v ∈ V can be written as a sum of elements from the Ui (spanning check).
  2. Check uniqueness: set u1 + ... + um = 0 and verify that this forces each ui = 0.
  3. For two summands, it suffices to check U ∩ W = {0}. For more summands, check each Ui ∩ (sum of others) = {0}.
- Use the dimension formula when dimensions are known: if dim(V) = sum dim(Ui) then the sum is direct.

Notation recap
- U + W denotes the sum.
- U ⊕ W denotes the direct sum (sum with unique decomposition).

Bases

Definition
- A subset B of a vector space V is a basis of V if B is linearly independent and B spans V.
- Equivalently, B is a basis iff every vector v in V can be written uniquely as a finite linear combination of elements of B.

Immediate consequences
- Uniqueness of coefficients: If B is a basis, then for each v in V there is exactly one finite list of scalars (all but finitely many zero) giving v as a linear combination of elements of B. This follows from linear independence: if two representations existed their difference would be a nontrivial linear relation among basis elements.
- Coordinate map: Choosing an ordering of a basis B = {b1, ..., bn} gives an isomorphism V ≅ F^n by sending v = a1b1 + ... + anbn to the coordinate tuple (a1,...,an).

Key results connecting bases, spanning sets, and linear independence
1. Bases are minimal spanning sets.
   - Statement: If B is a basis of V then no proper subset of B spans V.
   - Proof sketch: Removing an element b from B would leave b expressible from the remaining elements (since the remaining would still span V), contradicting linear independence.

2. Bases are maximal linearly independent sets.
   - Statement: If B is a basis then B is not a proper subset of any larger linearly independent set.
   - Proof sketch: If you could add x ∉ B while retaining linear independence, then B ∪ {x} would also be independent and hence could not span V, contradicting that B already spans V. More directly, x must be a linear combination of B because B spans V, so adding x creates a relation.

3. Characterizations (equivalences).
   For a subset S of V, the following are equivalent:
   - S is a basis of V.
   - S is a minimal spanning set (spans V and no proper subset spans V).
   - S is a maximal linearly independent set (is independent and any proper superset is dependent).
   Proofs follow from the two points above and the definitions.

Existence of bases in finite-dimensional spaces
- Finite-dimensional definition: V is finite-dimensional if V has a finite spanning set.
- Theorem (existence): If V is finite-dimensional and nonzero, then V has a basis.
  Proof sketch:
   1. Start with a finite spanning set S = {v1,...,vk}.
   2. Remove from S any vector that is a linear combination of earlier ones; continue until no such vector remains. This produces a linearly independent subset B that still spans V (because removing only redundant vectors preserves the span).
   3. Thus B is a finite linearly independent spanning set, hence a basis.

Extending independent sets and extracting bases
- Any finite linearly independent set can be extended to a basis.
  Proof sketch: If W is a finite independent set in finite-dimensional V, add vectors from a spanning set (or from V) one at a time that are not in the span of the current list until the span becomes all of V. This process ends because V is finite-dimensional.
- Any finite spanning set contains a basis.
  Proof sketch: As above, remove redundant vectors from the spanning set until what's left is independent; the result still spans V and so is a basis.

Exchange lemma (Steinitz exchange)
- Statement (informal): If B is a finite basis and S is a finite spanning set, then |S| ≥ |B|, and one can replace elements of S by elements of B to produce a spanning set of the same size. More usefully: given a finite independent set X and a finite spanning set S, |X| ≤ |S|, and elements of S can be swapped out to extend X toward a basis.
- Consequence: Any two bases of a finite-dimensional vector space have the same cardinality.

Dimension
- Definition: The dimension of a finite-dimensional vector space V is the number of vectors in any basis of V.
- Well-definedness follows from the exchange lemma: all bases have the same (finite) size.
- Corollary: If V has dimension n then every linearly independent set has at most n vectors, and every spanning set has at least n vectors. Moreover, a linearly independent set of size n or a spanning set of size n is automatically a basis.

Practical algorithms (finite-dimensional case)
- To find a basis from a spanning list: perform elimination (remove vectors that are linear combinations of others) until independence is reached.
- To extend a linearly independent list to a basis: repeatedly add a vector from a spanning set (or from V) not in the current span until the span equals V.

Summary of useful criteria
- To check a finite set S is a basis: verify S spans V and |S| = dim V, or verify S is independent and |S| = dim V.
- Minimality and maximality characterizations can simplify proofs: show S is spanning and no element can be removed, or S is independent and no element can be added.

These are the main facts about bases in finite-dimensional vector spaces: definition, uniqueness of coordinates, existence, how to obtain a basis from spanning/independent sets, Steinitz exchange, and the resulting notion of dimension.

Coordinates of a vector relative to a basis

Definition of coordinates
- Let V be an n-dimensional vector space over a field F and let B = (v1, v2, ..., vn) be an ordered basis of V. For every vector x in V there exist scalars a1, a2, ..., an in F such that
  x = a1 v1 + a2 v2 + ... + an vn.
  The n-tuple (a1, a2, ..., an) is called the coordinates of x with respect to the basis B, and is written [x]_B.

Uniqueness
- The representation x = a1 v1 + ... + an vn is unique: if
  x = b1 v1 + ... + bn vn
  as well, then subtracting gives 0 = (a1 − b1)v1 + ... + (an − bn)vn. Because (v1,...,vn) is a basis (hence linearly independent), each ai − bi = 0, so ai = bi for all i. Thus each vector has exactly one coordinate tuple relative to B.

Coordinate map and its properties
- Define the coordinate map C_B : V → F^n by C_B(x) = [x]_B = (a1, ..., an)^T where x = Σ ai vi.
- C_B is linear: for x,y in V and α in F,
  C_B(x + y) = C_B(x) + C_B(y),  C_B(αx) = α C_B(x).
- C_B is a vector space isomorphism: it is injective because distinct vectors have distinct coordinates (uniqueness above) and surjective because for any tuple (c1,...,cn) in F^n the vector Σ ci vi has those coordinates. Thus V ≅ F^n via C_B.

Computing coordinates
- To compute [x]_B, solve x = a1 v1 + ... + an vn for the scalars ai. Concretely:
  - If V = F^n and the basis B is given by column vectors v1,...,vn (as usual), form the n×n matrix M whose columns are the basis vectors. Then the coordinate vector [x]_B satisfies M [x]_B = x, so [x]_B = M^{-1} x (provided M is invertible, which holds because B is a basis).
  - In a general V, pick any representation of x and express it as a linear combination of the basis elements, e.g., by solving a linear system obtained from equalities of components in a chosen ambient coordinate system.

Change of coordinates (changing the basis)
- Let B = (v1,...,vn) and B' = (w1,...,wn) be two ordered bases of V. There is an invertible n×n matrix P (the change-of-coordinates matrix from B to B') such that for every x in V,
  [x]_{B'} = P [x]_B.
- How to form P: express each basis vector vj of B in coordinates relative to B':
  vj = c1j w1 + c2j w2 + ... + cnj wn.
  Then the jth column of P is [vj]_{B'} = (c1j, c2j, ..., cnj)^T. Equivalently, P is the matrix whose columns are the coordinate vectors of the old basis vectors relative to the new basis.
- P is invertible and its inverse is the change-of-coordinates matrix from B' to B:
  [x]_B = P^{-1} [x]_{B'}.
- Matrix viewpoint: if M_B and M_{B'} are the n×n matrices whose columns are the basis vectors of B and B' expressed in some fixed ambient coordinates, then P satisfies
  M_B = M_{B'} P,
  so P = M_{B'}^{-1} M_B.

Summary of the practical recipe
- To find coordinates of x in basis B: write x as a linear combination of the basis vectors (solve M [x]_B = x if bases are given as columns of M), the coefficients are the coordinates.
- To convert coordinates from basis B to B': multiply by the change-of-coordinates matrix P whose columns are the coordinates of the B-vectors relative to B'. Conversely multiply by P^{-1} to go the other way.

This establishes the one-to-one linear correspondence between vectors in V and their coordinate n-tuples relative to any chosen ordered basis, how to compute those tuples, and how to convert them when the basis changes.

Definition. Let V be a finite-dimensional vector space. A basis of V is a linearly independent list of vectors that spans V. The dimension of V, denoted dim V, is the length (number of vectors) of any basis of V.

Theorem (Well-definedness of dimension). If V is finite-dimensional then any two bases of V have the same length; hence dim V is well defined.

Proof. Let B and B' be two bases of V. Write |B| = n and |B'| = m. Since B is a basis, B is linearly independent and spans V. In particular B spans V, so every vector of B' is a linear combination of vectors from B. Thus B' ⊆ span(B). Because B' is linearly independent, the Exchange Lemma (Steinitz exchange) implies m ≤ n. Reversing the roles of B and B' gives n ≤ m. Hence n = m. Therefore every basis of V has the same length, so dim V is well defined. □

Comparing sizes: subspaces and spanning/independent sets

1. Independent sets cannot be larger than a basis.
Statement. If V is finite-dimensional with dim V = n and S is a linearly independent list in V, then |S| ≤ n. Moreover, if |S| = n then S is a basis of V.

Proof. Extend S to a basis S ∪ T of V (possible because every independent list can be extended to a basis). The extended basis has length n, so |S| + |T| = n, hence |S| ≤ n. If |S| = n then |T| = 0, so S already spans V and is a basis. □

2. Spanning lists cannot be smaller than a basis.
Statement. If V is finite-dimensional with dim V = n and S spans V, then |S| ≥ n. Moreover, if |S| = n then S is a basis of V.

Proof. Let B be a basis of V with |B| = n. Since S spans V, each vector of B is a linear combination of vectors from S. The Exchange Lemma implies n = |B| ≤ |S|. If |S| = n then again S is independent (otherwise you could remove a vector and still span, contradicting minimality), so S is a basis. □

3. Dimensions of subspaces.
Statement. If U is a subspace of a finite-dimensional space V, then U is finite-dimensional and dim U ≤ dim V. Moreover, dim U = dim V iff U = V.

Proof. Let dim V = n and let B be a basis of U. B is an independent list in V, so by (1) |B| ≤ n. Thus dim U = |B| ≤ n = dim V, and U is finite-dimensional. If dim U = dim V then any basis of U has n vectors and, being independent in V, must be a basis of V; therefore U = V. Conversely, if U = V then clearly dim U = dim V. □

Consequences and useful comparisons
- Any independent list in V has length at most dim V; maximal independent lists (those that are not strictly contained in a larger independent list) are bases and therefore have length dim V.
- Any spanning list in V has length at least dim V; minimal spanning lists (those that cease to span when any vector is removed) are bases and have length dim V.
- If U ⊆ W are subspaces of V then dim U ≤ dim W ≤ dim V, with equalities characterizing equality of the subspaces.

These facts let one compare "sizes" of subspaces and generating/independent sets by comparing their dimensions (or lengths), providing a precise numerical measure of the size of a finite-dimensional vector space.

Theorem (Size bound: independent ≤ spanning).
Let V be a vector space. Suppose u1,...,um is a linearly independent list in V and v1,...,vn is a spanning list of V (i.e. span(v1,...,vn)=V). If m is finite and n is finite then m ≤ n.

Proof (replacement/exchange argument).
We inductively build a spanning list that contains the u’s by replacing some of the v’s one at a time.

Start with the spanning list S0 = (v1,...,vn). Because S0 spans V and u1 ∈ V, u1 is a linear combination of the vi, so the list (u1,v1,...,vn) is linearly dependent. Hence one of the vectors in that list is a linear combination of the preceding ones; in particular there exists some index j such that vj ∈ span(u1,v1,...,v_{j-1},v_{j+1},...,vn). Removing that vj leaves a list of n vectors that still spans V but with u1 included. Thus we obtain a spanning list S1 of length n that contains u1.

Now suppose for k < m we have a spanning list Sk of length n that contains u1,...,uk. Consider uk+1. Since Sk spans V, uk+1 is in their span, so the list (u1,...,uk,uk+1, remaining vectors of Sk) is dependent, and one of the vectors can be removed without losing the spanning property. That removable vector cannot be one of u1,...,uk (because u1,...,uk,uk+1 are independent), so we can remove some original v and obtain a spanning list Sk+1 of length n that contains u1,...,u_{k+1}.

Continuing this process until k = m, we get a spanning list Sm of length n that contains u1,...,um. Since Sm has length n and contains the m distinct independent vectors u1,...,um, we must have m ≤ n. (If m > n we would have a linearly dependent list of > n vectors among n vectors, contradiction.)

Corollary (any two bases have the same size).
If B1 and B2 are finite bases of V, then applying the theorem with u's = B1 (independent) and v's = B2 (spanning) yields |B1| ≤ |B2|. Swapping roles gives |B2| ≤ |B1|, so |B1| = |B2|. This validates the notion of dimension as the common size of bases.

Theorem (Replacement/Exchange theorem).
Let V be finite-dimensional. Suppose B = (b1,...,bn) is a basis of V and u1,...,um is a linearly independent list in V. Then m ≤ n, and there exists a subset of B of size n−m such that (u1,...,um, that subset) is a basis of V. Equivalently, one can replace m vectors of B by u1,...,um to obtain a basis.

Proof.
From the previous theorem we already have m ≤ n. For the existence of a replacement, proceed inductively:

For k = 1: since B spans V and u1 ∈ V, u1 can be written in terms of B, so (u1,b1,...,bn) is dependent. Because u1 ≠ 0 (otherwise it would contradict independence), some basis vector bi is a linear combination of the others together with u1, hence removing that bi yields a list of n vectors that spans V and contains u1. Moreover that list is independent because it contains n vectors and spans V, so it is a basis.

Assume we have replaced k basis vectors to get a basis containing u1,...,uk. Consider uk+1. The current basis spans V, so uk+1 is in its span; add uk+1 and remove one of the original basis vectors (not among u1,...,uk) that is dependent on the rest. This preserves spanning and yields a basis containing u1,...,u_{k+1}. Continue until all u1,...,um are included. The result is a basis with exactly m of the original basis vectors replaced.

Corollary (spanning list contains a basis).
If v1,...,vn span V, then by removing dependent vectors one at a time (or by applying the above theorem with a maximal independent sublist) we obtain a subset of the vi that is a basis of V. Concretely: take a maximal linearly independent sublist among the vi; maximality forces it to span V, so it is a basis.

Corollary (independent list extends to a basis).
If V is finite-dimensional and u1,...,um is linearly independent, pick any basis B of V and apply the Replacement Theorem to get a basis containing u1,...,um. Thus every finite independent list can be extended to a basis.

Remarks on methodology.
All these results rely on the same simple exchange idea: because a spanning list expresses any vector as a linear combination, adding an independent vector to a spanning list creates a dependence that lets you remove one of the original spanning vectors without losing the span. Iterating this replacement yields the inequality between sizes and the constructive replacement/extension procedures above.

Quotient spaces V/U

Definition
- Let V be a vector space and U a subspace of V. For v in V, the coset of v relative to U is
  v + U = {v + u : u ∈ U}.
- The set of all cosets is the quotient space V/U:
  V/U = {v + U : v ∈ V}.

Intuition: v + U collects all vectors of V that differ from v by an element of U. Cosets partition V into equivalence classes under the relation v ~ w ⇔ v − w ∈ U.

Vector-space structure on V/U
- Addition: (v + U) + (w + U) := (v + w) + U.
- Scalar multiplication: a(v + U) := (av) + U for a in the field.

Well-definedness: If v + U = v′ + U and w + U = w′ + U, then v − v′ ∈ U and w − w′ ∈ U, so
  (v + w) − (v′ + w′) = (v − v′) + (w − w′) ∈ U,
hence (v + w) + U = (v′ + w′) + U. Similarly for scalars. Thus the operations do not depend on the choice of representatives.

With these operations V/U is a vector space: the vector-space axioms descend from those in V because the projection v ↦ v + U respects addition and scalar multiplication.

Canonical projection
- The map π: V → V/U given by π(v) = v + U is linear and surjective.
- Its kernel is ker π = U.

Dimension in the finite-dimensional case
- If V is finite-dimensional and U a subspace, then V/U is finite-dimensional and
  dim(V/U) = dim V − dim U.

Proof sketch:
1. Choose a basis {u1,...,uk} of U.
2. Extend it to a basis of V: {u1,...,uk, v1,...,vm} (possible because V is finite-dimensional).
3. Show the cosets {v1 + U, ..., vm + U} form a basis of V/U:
   - Spanning: For any v ∈ V write v = a1u1+...+akuk + b1v1+...+bmvm; then π(v) = b1(v1+U)+...+bm(vm+U).
   - Linear independence: If c1(v1+U)+...+cm(vm+U) = U (the zero coset), then c1v1+...+cmvm ∈ U, so expressing that vector in the basis of V shows all ci = 0 because the vi are independent of the uj.
4. Therefore dim(V/U) = m = dim V − k = dim V − dim U.

Remarks
- The quotient construction measures the "degrees of freedom" in V outside U.
- The first isomorphism theorem: for a linear map T: V → W, V/ker T is isomorphic to range T (use canonical projection and induced map).

Section 12 — Subspaces and Dimension (including sums)

Key facts (finite-dimensional V)

- If V is finite-dimensional and U ≤ V (U a subspace), then
  dim U ≤ dim V,
  with equality iff U = V.

- For two subspaces U, W ≤ V,
  dim(U + W) = dim U + dim W − dim(U ∩ W).
  Equivalently,
  dim(U ∩ W) = dim U + dim W − dim(U + W).

- Consequences / inequalities:
  - dim(U + W) ≤ dim U + dim W.
  - dim(U ∩ W) ≥ dim U + dim W − dim V (because U + W ≤ V so dim(U + W) ≤ dim V).
  - In particular 0 ≤ dim(U ∩ W) ≤ min{dim U, dim W}.
  - U ∩ W = {0} iff dim(U + W) = dim U + dim W; when this happens we say U and W sum directly and write U ⊕ W = U + W.

- For more than two subspaces U1,...,Um ≤ V,
  dim(U1 + ··· + Um) ≤ dim U1 + ··· + dim Um.
  (There is an inclusion–exclusion style identity for dimensions but the two-subspace formula is the fundamental tool.)

How to use these relationships (strategy)

1. To compute dim(U + W): find bases for U and for W, combine them, remove linear dependencies; the formula gives how many vectors must be removed: exactly dim(U ∩ W).
2. To find dim(U ∩ W): compute dim U + dim W and subtract dim(U + W) (or use bounding inequalities if dim(U + W) not known).
3. To determine whether U + W is direct: check whether dim(U + W) = dim U + dim W (or check U ∩ W = {0} directly).

Worked examples

Example 1 — possible dimensions of intersection
Let V be 4-dimensional. Suppose U, W ≤ V with dim U = 3 and dim W = 2. What are the possible values of dim(U ∩ W)?

Use dim(U ∩ W) = dim U + dim W − dim(U + W). Since U + W ≤ V, dim(U + W) ≤ 4. Also dim(U + W) ≥ max{dim U, dim W} = 3.
Thus dim(U ∩ W) = 3 + 2 − dim(U + W) ranges over
- if dim(U + W) = 4 then dim(U ∩ W) = 1,
- if dim(U + W) = 3 then dim(U ∩ W) = 2.
So possible intersection dimensions are 1 or 2. (Note dim(U ∩ W) cannot be 0 here because sum of dims 3+2=5 > 4 forces at least 1-dimensional overlap.)

Example 2 — dimension of sum when intersection known
In R^5 let U and W be subspaces with dim U = 3, dim W = 4, and suppose U ∩ W has dimension 2. Then
dim(U + W) = 3 + 4 − 2 = 5,
so U + W = R^5 (assuming V = R^5).

Example 3 — constructing a direct sum
Let V = P3 (polynomials degree ≤ 3). Let U = span{1, x} and W = span{x^2, x^3}. Then dim U = 2, dim W = 2. Their intersection is {0} (no nonzero polynomial of degree ≤ 1 can equal a nonzero polynomial of degree ≥ 2), so dim(U + W) = 2 + 2 = 4 = dim P3. Thus P3 = U ⊕ W.

Example 4 — combining bases to compute dimension
Let U = span{u1, u2} and W = span{w1, w2, w3} inside some finite-dimensional V. To compute dim(U + W) explicitly: form the list [u1, u2, w1, w2, w3], row-reduce (if vectors given coordinates) to count independent ones. The count equals dim(U + W). The formula tells you how many of the original five will be linearly dependent: exactly dim(U ∩ W).

Example 5 — matrix subspaces
Let V = M2×2(R). Let U be the subspace of symmetric matrices (dim 3) and W the subspace of matrices with zero trace (dim 3). What are dim(U + W) and dim(U ∩ W)?
- dim(U ∩ W): symmetric and trace-zero matrices are those of form [[a,b],[b,−a]]; basis {[[1,0],[0,−1]], [[0,1],[1,0]]}, so dim(U ∩ W) = 2.
- dim(U + W) = dim U + dim W − dim(U ∩ W) = 3 + 3 − 2 = 4 = dim M2×2, so U + W = M2×2.

Quick checklist when solving problems
- Write down dims of the subspaces.
- Use dim(U + W) = dim U + dim W − dim(U ∩ W) to relate unknown quantities.
- Use bounds 0 ≤ dim(U ∩ W) ≤ min{dim U, dim W} and dim(U + W) ≤ dim V.
- If asked about direct sums, check whether dim(U + W) = dim U + dim W (or test intersection = {0}).
- When explicit vectors are given, combine bases and count linearly independent vectors to get dim(U + W).

Practice problem (brief)
Let V = R^4. U = span{(1,0,0,0),(0,1,0,0)} (dim 2), W = span{(1,1,0,0),(0,0,1,0)} (dim 2). Find dim(U ∩ W) and dim(U + W).
Solution sketch: U ∩ W consists of vectors in U that are linear combos of the two generators of W. Solve α(1,0,0,0)+β(0,1,0,0) = γ(1,1,0,0)+δ(0,0,1,0). Comparing coordinates forces δ = 0 and α = γ, β = γ, so α = β. Thus intersection is span{(1,1,0,0)} so dim(U ∩ W) = 1. Then dim(U + W) = 2 + 2 − 1 = 3.

End of section.

Definition — Linear map
Let V and W be vector spaces over the same field F. A function T : V → W is a linear map (or linear transformation) if for all vectors u, v ∈ V and all scalars α ∈ F the following two properties hold:

1. Additivity: T(u + v) = T(u) + T(v).
2. Homogeneity (scalar multiplicativity): T(αv) = α T(v).

Equivalently, T is linear iff for all u, v ∈ V and all scalars α, β ∈ F,
T(αu + βv) = α T(u) + β T(v).
This single bilinear-looking condition combines additivity and homogeneity and is often convenient for checks.

How to verify linearity
- Direct check: show both additivity and homogeneity hold for the candidate map T.
- Combined check: show T(αu + βv) = αT(u) + βT(v) for arbitrary u, v and scalars α, β; this immediately implies the two defining properties.
- It suffices to check the defining property on a spanning set (or basis) of V: if S spans V and T satisfies linearity on linear combinations of vectors from S (or you verify T respects linear combinations of basis vectors), then T is linear on all of V.
- Check simple necessary consequences to detect nonlinearity quickly:
  - T(0) must equal 0_W (apply homogeneity with α = 0 or additivity with v = 0).
  - T(−v) must equal −T(v) (apply homogeneity with α = −1).
If a map fails either consequence, it is not linear.

Examples — verifying linearity
1. Matrix multiplication: For an m×n matrix A, define T: F^n → F^m by T(x) = A x. Then for u,v ∈ F^n and scalar α,
T(u+v) = A(u+v) = Au + Av = T(u)+T(v),
T(αv) = A(αv) = α(Av) = αT(v).
Thus T is linear.

2. Derivative on polynomials: Let P(F) be polynomials over F and D: P(F) → P(F) the derivative operator D(p) = p'. For p,q polynomials and scalar α,
D(p+q) = (p+q)' = p' + q' = D(p) + D(q),
D(αp) = (αp)' = α p' = α D(p).
Thus D is linear.

3. Zero map and identity map: The zero map Z(v) = 0_W and the identity I(v) = v satisfy the two properties trivially, so they are linear.

Examples — detecting nonlinearity
1. Squaring map on functions: S: C([0,1]) → C([0,1]) defined by S(f) = f^2 (pointwise square) is not linear because S(f+g) ≠ S(f) + S(g) in general.

2. Constant nonzero map: C(v) = w0 for some fixed nonzero w0 ∈ W. Then C(0) = w0 ≠ 0_W, so C is not linear.

3. Affine shift: T(x) = Ax + b on F^n is linear only when b = 0. If b ≠ 0, additivity fails: T(0) = b ≠ 0.

Common pitfalls
- Confusing linear maps with affine maps: linear maps must send 0 to 0 and preserve linear combinations; adding a constant term breaks linearity.
- Checking linearity on a few vectors is insufficient; you must verify the properties for arbitrary vectors (or use a spanning set/basis argument).
- Mixing fields: domain and codomain must be vector spaces over the same field for the map to be linear in this sense.

Summary checklist for verifying a candidate T: V → W
- Verify T(0_V) = 0_W (quick necessary test).
- Verify T(u+v) = T(u) + T(v) for arbitrary u,v, and T(αv) = αT(v) for arbitrary α,v; or verify the combined property T(αu+βv) = αT(u)+βT(v).
- Optionally reduce checks to a basis or spanning set when convenient.

Fundamental Theorem (Quotient / Isomorphism Theorem)

Statement
Let T: V → W be a linear map. Define N = Null(T). There is a well-defined linear map S: V/N → Range(T) by
  S(v + N) = T(v).
This S is an isomorphism. Equivalently,
  V / Null(T) ≅ Range(T).
Proof sketch: S is well defined because if v + N = v' + N then v − v' ∈ N so T(v) = T(v'). Linearity is immediate. S is surjective by definition of Range(T). Injectivity: S(v + N) = 0 ⇔ T(v) = 0 ⇔ v ∈ N ⇔ v + N = N (the zero coset). Hence S is an isomorphism.

Immediate consequences and uses
- Rank–Nullity: Taking dimensions (when V is finite-dimensional),
    dim V = dim Null(T) + dim Range(T).
  This follows because dim(V/N) = dim V − dim N and dim(V/N) = dim Range(T).

- Description of V relative to T: There exists a subspace U ⊆ V with V = N ⊕ U and T|_U : U → Range(T) is an isomorphism. Construction: choose a basis of Range(T), pick one preimage in V for each basis vector, and let U be the span of those preimages.

- Criteria for injectivity and surjectivity:
  • T is injective ⇔ Null(T) = {0} ⇔ V/N ≅ V and hence V ≅ Range(T).
  • T is surjective ⇔ Range(T) = W ⇔ V/N ≅ W, so W is (isomorphic to) a quotient of V by Null(T).

- Classification up to isomorphism: The structure of T is completely determined (up to isomorphism on domain and codomain) by the pair (dim Null(T), dim Range(T)). For finite-dimensional V and W, one can pick bases so that the matrix of T has the block form [I_r 0; 0 0] where r = rank(T).

Examples of application
- To show W is isomorphic to a quotient: If T: V → W is surjective, the theorem gives W ≅ V/Null(T). This is often used to transfer problems about W to problems about a quotient of V.
- To split V: Given T, pick U as above. Then elements of V are uniquely written as n + u with n ∈ Null(T), u ∈ U; T ignores the n-part and is invertible on U, so the study of T reduces to an isomorphism U → Range(T).

Takeaway
The Fundamental Theorem identifies the range of a linear map with the quotient of its domain by its null space. This identification gives the rank–nullity relation, produces a complementary subspace on which T restricts to an isomorphism, and clarifies how V and W relate through T (W is a quotient of V when T is surjective; Range(T) is a quotient of V in general).

Matrix of a Linear Map (Relative to Bases)

Let V and W be finite-dimensional vector spaces with ordered bases
- β = (v1, v2, ..., vn) for V, and
- γ = (w1, w2, ..., wm) for W.
Let T: V → W be a linear map. The matrix of T relative to the bases β and γ, denoted [T]_{γ←β}, is the m×n matrix whose j-th column is the coordinate vector of T(vj) relative to γ.

Construction (step-by-step)
1. For each basis vector vj in β, compute the image T(vj) in W.
2. Express T(vj) as a linear combination of the codomain basis γ:
   T(vj) = a1j w1 + a2j w2 + ... + amj wm.
   The scalars aij are the coordinates of T(vj) relative to γ.
3. Form the matrix [T]_{γ←β} whose j-th column is the column vector [a1j, a2j, ..., amj]^T:
   [T]_{γ←β} = [ [T(v1)]_γ  [T(v2)]_γ  ...  [T(vn)]_γ ].

Notation for entries
- The entry in row i and column j of [T]_{γ←β} is aij, so T(vj) = sum_{i=1}^m aij wi.

Matrix action on coordinates
If x ∈ V has coordinate vector [x]_β = [x1, x2, ..., xn]^T (so x = sum xj vj), then
[T(x)]_γ = [T]_{γ←β} [x]_β.
That is, to find the coordinates of T(x) in the basis γ, multiply the matrix [T]_{γ←β} by the coordinate vector of x in β.

Reason (brief)
Because T is linear,
T(x) = T(sum_{j} xj vj) = sum_{j} xj T(vj).
Writing each T(vj) = sum_{i} aij wi and collecting coefficients of the wi gives the i-th coordinate of T(x) as sum_{j} aij xj, which is exactly matrix multiplication.

Worked example
Let V = R^2 with β = (v1, v2) = ((1,0),(0,1)) (standard basis) and W = R^2 with γ = (w1,w2) = ((1,1),(1,-1)). Define T: R^2 → R^2 by T(x,y) = (2x+y, x+3y).

1. Compute images of β:
   T(v1) = T(1,0) = (2,1). Express in γ:
     find c1,c2 with (2,1) = c1(1,1) + c2(1,-1).
     Solve: c1 + c2 = 2, c1 - c2 = 1 ⇒ c1 = 3/2, c2 = 1/2.
     So [T(v1)]_γ = [3/2, 1/2]^T.
   T(v2) = T(0,1) = (1,3). Express in γ:
     solve c1 + c2 = 1, c1 - c2 = 3 ⇒ c1 = 2, c2 = -1.
     So [T(v2)]_γ = [2, -1]^T.

2. Form matrix:
   [T]_{γ←β} = [ [3/2, 2], [1/2, -1] ] as columns, i.e.
   [T]_{γ←β} = [[3/2, 2],
                [1/2, -1]].

3. Apply to a vector x = (x,y). Its β-coordinates are [x]_β = [x,y]^T.
   [T(x)]_γ = [T]_{γ←β} [x,y]^T = [ (3/2)x + 2y, (1/2)x - y ]^T.
   If desired, convert back to standard coordinates in W by combining with γ:
   T(x) = ( (3/2)x + 2y ) w1 + ( (1/2)x - y ) w2,
   and substituting w1,w2 gives the usual result (2x+y, x+3y).

Remarks
- The matrix depends on the choice and ordering of the bases β and γ.
- If both V and W are R^n with standard bases, this construction recovers the usual matrix representation of a linear transformation.
- Using these matrices, composition of linear maps corresponds to matrix multiplication (with appropriate relative bases).

Section 16 — Null Space (Kernel) and Injectivity

Definition
- For a linear map T : V → W, the null space (kernel) of T is
  null T = { v ∈ V : T(v) = 0 }.
  It is a subspace of V.

Why it matters
- null T measures how much of V is collapsed to 0 by T. It is central to understanding injectivity: T loses no information exactly when null T contains only the zero vector.

Characterization of injectivity
- Theorem. T is injective ⇐⇒ null T = {0}.
- Proof.
  - (⇒) If T is injective and v ∈ null T, then T(v) = 0 = T(0). By injectivity v = 0, so null T = {0}.
  - (⇐) If null T = {0} and T(v1) = T(v2), then T(v1 − v2) = 0, so v1 − v2 ∈ null T. Thus v1 − v2 = 0 and v1 = v2. Hence T is injective.

Computing the null space — general method
1. Choose a basis for V and write v ∈ V in coordinates (or express T by its action on basis vectors).
2. Set up the equation T(v) = 0. This becomes a homogeneous linear system in the coordinates of v.
3. Solve the system (Gaussian elimination or direct reasoning) to find all coordinate vectors of solutions.
4. Translate the solution space back into vectors in V; these form null T and provide a basis for null T.

Examples

1) Matrix example (R^3 → R^2).
Let T: R^3 → R^2 have matrix (with respect to standard bases)
    A = [ 1  2  -1
          0  1   3 ].
Find null T.
Solve A[x y z]^T = 0:
  1) x + 2y − z = 0
  2)     y + 3z = 0  ⇒ y = −3z.
Then x = −2y + z = −2(−3z) + z = 7z. So
  [x y z]^T = z [7, −3, 1]^T, z ∈ R.
Thus null T = span{ (7, −3, 1) }, a one-dimensional subspace. Since null T ≠ {0}, T is not injective.

2) Differentiation on polynomials (P3 → P2).
Let V = P3 (polynomials degree ≤ 3) and T(p) = p′.
Find null T.
T(p) = 0 ⇔ p′ = 0 ⇔ p is constant. So null T = { p : p(x) = c, c ∈ R } = span{1}. Dimension = 1, so T is not injective. (More generally, differentiation on Pn has null space = constants.)

3) Evaluation functional (function space → R).
Let V = R^R (all real-valued functions on R) and T(f) = f(0).
Find null T.
null T = { f : f(0) = 0 }, a large subspace (all functions vanishing at 0). Since null T contains nonzero functions, T is not injective.

4) Linear map that is injective.
Let T: R^2 → R^2 given by matrix B = [1 0; 0 2]. Solve B[x y]^T = 0:
  x = 0, 2y = 0 ⇒ x = y = 0. Hence null T = {0} and T is injective.

Remarks
- The nullity of T is dim(null T). In finite dimensions, rank-nullity theorem relates nullity + rank = dim V.
- Computing null T does not require determinants: use linear-algebraic solving (Axler’s emphasis on linear maps and subspaces rather than determinants).

Quick checklist when asked to find null T or check injectivity
- Write T(v) = 0 in coordinates (or via basis images).
- Solve the resulting homogeneous system.
- If the only solution is the zero vector, T is injective; otherwise not.

Range (image) of a linear map

Definition
- Let V and W be vector spaces and T: V → W a linear map. The range (or image) of T is
  Range(T) = Im(T) = {T(v) : v ∈ V}.
- Range(T) is a subspace of W.

Basic facts
- Range(T) = span{T(v) : v ∈ V}. In particular, if {v1,...,vn} is a spanning set (or a basis) of V then Range(T) = span{T(v1),...,T(vn)}.
- If T is represented by a matrix A (with respect to chosen bases), Range(T) is the column space of A.
- For finite-dimensional V, dim Range(T) is called the rank of T. The rank–nullity theorem gives
  dim V = dim Ker(T) + dim Range(T).

Computing the range (procedures)
- Using images of a basis: compute T on a basis of V and take their span.
- Using a matrix: reduce A to find a basis of the column space (pivot columns give a basis).
- Identify a familiar linear operator: e.g., differentiation, evaluation, projection—use a known description of outputs.

Examples

1) Matrix example
  Let T: R^3 → R^2 be given by the matrix A =
    [1  2  3
     0  1  4].
  The columns are c1 = (1,0), c2 = (2,1), c3 = (3,4). Range(T) = span{c1,c2,c3} = span{(1,0),(2,1)}.
  Since (1,0) and (2,1) are linearly independent in R^2, Range(T) = R^2 and T is surjective.

  If instead A = [1 2; 2 4] as a 2×2 example, columns are (1,2) and (2,4) which are dependent, so Range(T) = span{(1,2)} ≠ R^2; T is not surjective.

2) Differentiation on polynomials
  Let D: P3 → P2 by D(p) = p'. For a basis {1, x, x^2, x^3} of P3,
  D(1)=0, D(x)=1, D(x^2)=2x, D(x^3)=3x^2, so Range(D) = span{1, x, x^2} = P2.
  Therefore D is surjective.

3) Projection/non-surjective example
  Let T: R^2 → R^2 be projection onto the x-axis: T(x,y) = (x,0). Range(T) = {(x,0): x∈R} is a 1-dimensional subspace, so T is not surjective.

Characterizing surjectivity with the range
- By definition, T is surjective ⇔ Range(T) = W (the entire codomain).
- For finite-dimensional spaces, T: V → W is surjective ⇔ dim Range(T) = dim W (i.e. rank(T) = dim W).
- In particular, if dim V = dim W < ∞, then T is surjective ⇔ T is injective (equivalently rank = dim V).

Useful equivalent tests (finite-dimensional)
- Using a matrix representation A of T: T is surjective ⇔ the columns of A span W ⇔ A has a pivot in every row ⇔ rank(A) = dim W.
- Using images of a basis: T is surjective iff the images of a basis of V span W.

Takeaway
- Compute Range(T) by taking the span of T applied to a basis (or the column space of a matrix). Surjectivity is exactly the condition that this span equals the whole codomain.

Invertibility / Isomorphism

Definition
- A linear map T : V → W is invertible (an isomorphism) if there exists a linear map S : W → V such that S ∘ T = I_V and T ∘ S = I_W. In that case S is called the inverse of T and is unique; we write S = T^{-1}.

Equivalent criteria
Let T : V → W be linear.

1. Bijectivity
- T is invertible ⇔ T is bijective (both injective and surjective).

2. Kernel and range
- T is injective ⇔ ker T = {0}.
- T is surjective ⇔ range T = W.
- Hence T is invertible ⇔ ker T = {0} and range T = W.

3. Finite-dimensional criterion (equal dimensions)
- If V and W are finite-dimensional with dim V = dim W, then
  T is injective ⇔ T is surjective ⇔ T is invertible.
- Equivalently, for finite-dimensional V and W with equal dimension, T is invertible ⇔ rank T = dim V.

4. Matrix criteria (choose ordered bases)
- If V and W are finite-dimensional and A is the matrix of T with respect to chosen bases, then T is invertible ⇔ there exists a matrix B with BA = I and AB = I (equivalently A is a two-sided inverse).
- Equivalent concrete matrix conditions:
  - The columns of A are linearly independent and span the codomain (so they form a basis).
  - A has full rank (rank = number of columns = number of rows when square).
  - A can be row-reduced to the identity (pivot in every row and every column when square).
  (In a square n×n situation these conditions are all equivalent to A being invertible.)

Remarks
- If T is invertible then T^{-1} is linear and (T^{-1})^{-1} = T.
- Composition: if T : U → V and S : V → W are invertible linear maps, then S ∘ T is invertible with (S ∘ T)^{-1} = T^{-1} ∘ S^{-1}.

Polynomial evaluation can be usefully viewed as a linear map. Doing so makes many elementary facts about roots, remainders, and the interaction of polynomials with linear operators immediate from linear-algebraic notions such as kernel and range.

Definition (evaluation at a scalar). Fix a scalar a in the field F. Define
  Ev_a : P(F) → F
by Ev_a(p) = p(a). Here P(F) is the vector space of all polynomials with coefficients in F. Ev_a is linear because for all p, q and all scalars α,
  Ev_a(p + q) = (p + q)(a) = p(a) + q(a) = Ev_a(p) + Ev_a(q),
  Ev_a(αp) = (αp)(a) = α p(a) = α Ev_a(p).

Kernel and the Factor Theorem. The kernel of Ev_a is
  ker(Ev_a) = { p ∈ P(F) : p(a) = 0 }.
By the usual algebraic Factor Theorem this is exactly the set of polynomials divisible by (x − a):
  ker(Ev_a) = (x − a)P(F) = { (x − a)q : q ∈ P(F) }.
From the linear-map point of view this says the kernel is a subspace (indeed an ideal) generated by the single polynomial x − a. Thus x − a is a linear generator of the kernel; equivalently, the kernel is one-dimensional as a module over P(F) and has codimension 1 as a subspace of P(F) when we restrict to polynomials of bounded degree.

Remainder theorem via quotient/range. Consider the subspace Pn of polynomials of degree ≤ n. The map Ev_a : Pn → F is a linear functional. Since Ev_a is surjective (constant polynomials realize any scalar value), its range is all of F, so by the rank–nullity theorem
  dim ker(Ev_a ∣ Pn) = n.
This yields the familiar unique decomposition: every p ∈ Pn can be written uniquely as
  p(x) = (x − a)q(x) + r
with q ∈ Pn−1 and r ∈ F (a constant). Uniqueness is exactly the statement that ker(Ev_a ∣ Pn) = (x − a)Pn−1 and the quotient Pn / ker(Ev_a ∣ Pn) is 1-dimensional (isomorphic to the range F). The scalar r is Ev_a(p) = p(a). Thus the remainder theorem and uniqueness of the remainder are linear-algebraic facts about the evaluation map.

Multiplicity of roots. Differentiation gives another linear map D on P(F). If (x − a)^k divides p, then p, Dp, D^2 p, …, D^{k−1} p all vanish at a. Conversely, the linear independence of the functionals Ev_a, Ev_a ∘ D, ..., Ev_a ∘ D^{k−1} can be used to detect the multiplicity of a root: the multiplicity is the largest k for which all these evaluation functionals vanish on p. Thus multiplicity can be phrased in terms of the joint kernel of a collection of linear maps.

Evaluation at an operator (preview). When a linear operator T ∈ L(V) replaces the scalar a, evaluation becomes a map from polynomials to operators:
  Ev_T : P(F) → L(V),   Ev_T(p) = p(T).
Ev_T is linear because p ↦ p(T) respects addition and scalar multiplication. The kernel of Ev_T is the set of annihilating polynomials for T:
  ker(Ev_T) = { p ∈ P(F) : p(T) = 0 }.
The kernel is an ideal in P(F). If V is finite-dimensional, this kernel is nontrivial (by dimension/rank arguments) and therefore — since P(F) is a principal ideal domain — generated by a unique monic polynomial of least degree, the minimal polynomial of T. That single generator has the same universal property as ker(Ev_T): every polynomial annihilating T is a multiple of the minimal polynomial. This linear-map viewpoint makes immediate why the minimal polynomial divides any annihilating polynomial and why p(T) = 0 exactly when the minimal polynomial divides p.

Consequences and uses
- The Factor/Remainder Theorem and uniqueness of remainder are immediate from rank–nullity applied to Ev_a on Pn.
- The set of roots of a nonzero polynomial has size at most its degree: Ev_a as a linear functional on Pn can have as kernel at most an n-dimensional subspace, so a polynomial of degree n cannot vanish on more than n distinct scalars (otherwise it would lie in the intersection of too many distinct codimension-1 kernels).
- When evaluating at an operator, kernel/range reasoning yields the existence and uniqueness (up to scalar multiple) of the minimal polynomial, and explains divisibility relations among annihilating polynomials.
- Many proofs about polynomials (e.g., Cayley–Hamilton, structure of cyclic subspaces, companion matrix facts) become transparent once Ev_T is treated as a linear map and one studies its kernel and image.

Keep in mind: treating evaluation as a linear map converts algebraic statements about divisibility and roots into linear-algebraic statements about kernels, ranges, and dimensions; this perspective is both unifying and powerful when polynomials act on vectors or operators.

Section 20 — Polynomial interpolation (existence and uniqueness, linear‐algebra approach)

Statement. Let F be a field, let a1,...,an be n distinct scalars in F, and let b1,...,bn be arbitrary scalars in F. Then there exists a unique polynomial p ∈ P_{n-1} (the vector space of polynomials over F of degree < n) such that
p(ai) = bi for i = 1,...,n.

Linear-algebra proof (conceptual).

1. Set-up as a linear map.
Define the evaluation map
T : P_{n-1} → F^n,   T(p) = (p(a1), p(a2), ..., p(an)).
T is linear because evaluation is linear. The domain P_{n-1} has dimension n and the codomain F^n has dimension n.

2. Injectivity ⇔ uniqueness.
Suppose p ∈ P_{n-1} satisfies p(ai) = 0 for every i = 1,...,n. Then p has n distinct roots a1,...,an. A nonzero polynomial of degree ≤ n−1 can have at most n−1 roots, so p must be the zero polynomial. Thus ker T = {0}, so T is injective. For a linear map between equal‑dimension spaces, injectivity implies surjectivity. Hence T is an isomorphism and, for every (b1,...,bn) ∈ F^n, there exists a unique p ∈ P_{n-1} with T(p) = (b1,...,bn). This proves existence and uniqueness.

Explicit construction (Lagrange form).

For a direct formula, define the Lagrange basis polynomials for j = 1,...,n:
Lj(x) = ∏_{i≠j} (x − a_i) / (a_j − a_i).
Each Lj is in P_{n-1} and satisfies Lj(a_k) = δ_{jk} (1 if k = j, 0 otherwise). Therefore the unique interpolant is
p(x) = ∑_{j=1}^n b_j Lj(x).
This polynomial has degree < n and p(a_i) = b_i for each i.

Alternative matrix viewpoint (Vandermonde).
Choose the standard basis {1, x, x^2, ..., x^{n-1}} of P_{n-1}. Writing p(x) = c0 + c1 x + ... + c_{n-1} x^{n-1}, the interpolation conditions p(ai)=bi give a linear system V c = b where V is the Vandermonde matrix
V_{ij} = a_i^{j-1} (rows indexed by i = 1..n, columns by j = 1..n),
c = column(c0,...,c_{n-1}), b = column(b1,...,bn).
The distinctness of the a_i implies det V ≠ 0, so V is invertible; hence the system has the unique solution c, giving the interpolating polynomial. The nonzero determinant of V is another form of the injectivity argument above.

Remarks.
- The argument used only linear-algebra facts (dimension, injectivity ⇒ surjectivity) and the elementary fact about the number of roots of a nonzero polynomial.
- The Lagrange formula is the concrete output of the linear-algebra construction; the Vandermonde viewpoint shows how one could solve for coefficients in any chosen basis.

Vector space of polynomials and the degree function

Definition of the space
- Let F be a field. Define P(F) (often written simply P) to be the set of all polynomials with coefficients in F:
  p(x) = a0 + a1 x + a2 x^2 + ... + an x^n
  with n a nonnegative integer and ai ∈ F. The zero polynomial (all coefficients 0) is included in P(F).

Vector-space structure
- Addition: If p(x) = ∑_{k=0}^m a_k x^k and q(x) = ∑_{k=0}^n b_k x^k, define (p+q)(x) = ∑_{k=0}^{max(m,n)} (a_k + b_k) x^k, where we take missing coefficients as 0. This operation is closed in P(F).
- Scalar multiplication: For c ∈ F and p(x) as above, define (c p)(x) = ∑_{k=0}^m (c a_k) x^k. This is closed in P(F).
- Zero vector: The zero polynomial 0(x) with every coefficient 0 is the additive identity.
- Additive inverse: For p(x) = ∑ a_k x^k, the inverse is (−p)(x) = ∑ (−a_k) x^k.
- The usual vector-space axioms (associativity, commutativity of addition, distributivity of scalar multiplication, etc.) hold by checking them coefficientwise in F. Thus P(F) is a vector space over F.

Degree function
- For a nonzero polynomial p(x) = a_n x^n + ... + a_0 with a_n ≠ 0, define deg p = n.
- For the zero polynomial define deg 0 = −∞ (this convenient convention makes many degree formulas uniform; −∞ is taken to be less than every integer and satisfies max(k, −∞) = k).
Properties of degree under vector-space operations
1. Degree under scalar multiplication
   - If c ∈ F and p ∈ P(F), then
     deg(c p) = { deg p, if c ≠ 0; −∞, if c = 0 }.
   - Proof: multiplying by a nonzero scalar does not change the leading coefficient or its position; multiplying by 0 yields the zero polynomial.

2. Degree under addition
   - For p, q ∈ P(F),
     deg(p + q) ≤ max(deg p, deg q).
   - Moreover, if deg p ≠ deg q then deg(p + q) = max(deg p, deg q).
   - Proof sketch: write p and q with coefficients; the coefficient of x^k in p+q is the sum of the coefficients. The highest possible degree of p+q cannot exceed the larger of deg p and deg q. If degrees differ, the highest-degree term of the polynomial with larger degree survives (its coefficient is not canceled), so equality holds. If degrees are equal, cancellation of the leading coefficients can occur, giving a strictly smaller degree.

Examples and remarks
- Example: p(x)=x^3+2x, q(x)=−x^3+5 have deg p = 3, deg q = 3, but p+q = 2x+5 has degree 1 because the x^3 terms cancel.
- Zero polynomial: deg 0 = −∞ makes statements like deg(p+q) ≤ max(deg p, deg q) and deg(c p) = deg p for c ≠ 0 hold with no special-case exceptions.
- Basis and finite-dimensional subspaces: The monomials {1, x, x^2, ...} form a basis for the space of all polynomials only if one allows infinite linear combinations; for fixed n the set {1, x, ..., x^n} is a basis of the subspace of polynomials of degree ≤ n, which is (n+1)-dimensional.

This defines P(F) as a vector space, specifies the degree function (including deg 0 = −∞), and records how addition and scalar multiplication affect degree.

Division algorithm for polynomials

Statement.
Let F be a field. For any polynomials p, s ∈ F[x] with s ≠ 0 there exist unique polynomials q, r ∈ F[x] such that
p = s q + r
and either r = 0 or deg r < deg s.

Existence (construction sketch).
Write deg p = m, deg s = n. If m < n take q = 0 and r = p. If m ≥ n, choose a monomial t = (leading coefficient of p)/(leading coefficient of s) · x^{m-n}. Subtract t·s from p to eliminate the highest-degree term of p; the remainder has degree < m. Repeat this process finitely many times (each step lowers degree) to obtain q as the sum of the chosen monomials and r the final remainder with deg r < n (or r = 0). This is the usual polynomial long division.

Uniqueness.
Suppose p = s q1 + r1 = s q2 + r2 with deg r1, deg r2 < deg s. Then s(q1 − q2) = r2 − r1. If q1 ≠ q2 then q1 − q2 ≠ 0, so the left side has degree at least deg s (since deg s + deg(q1 − q2) ≥ deg s). But the right side has degree < deg s, a contradiction. Hence q1 = q2 and then r1 = r2; q and r are unique.

Degree bounds and simple consequences.
- If p = 0 then q = 0 and r = 0. If p ≠ 0 and s ≠ 0, then in the division with deg p = m and deg s = n we get deg q ≤ m − n. In fact, when m ≥ n one constructs q so that deg q = m − n (by choosing the leading-term ratio in the first step), so deg q = m − n unless q = 0 (the precise statement: if deg p ≥ deg s then deg q = deg p − deg s; if deg p < deg s then q = 0).
- If deg p < deg s, the algorithm yields q = 0 and r = p.
- Remainder theorem (special case): dividing by s(x) = x − a gives p(x) = (x − a)q(x) + r with r constant; evaluating at x = a yields r = p(a). Thus the remainder on division by x − a equals p(a).
- Factor theorem: x − a divides p (i.e., there exists q with p = (x − a)q) iff p(a) = 0.
- No nontrivial multiple of s of degree less than deg s: if s ≠ 0 and t·s has degree < deg s then t = 0. This is implicit in the uniqueness argument.

Remarks on algorithmic use.
The division algorithm provides the foundation for polynomial computations analogous to integer division: it yields quotients and remainders, allows repeated application to compute greatest common divisors (Euclidean algorithm), and underlies interpolation and factorization arguments.

Section 23 — The Minimal Polynomial

Setting and definition
- Let V be a finite-dimensional vector space over a field F and let T ∈ L(V) be a linear operator. A polynomial p ∈ F[x] is said to annihilate T if p(T) = 0 (the zero operator). The set of all polynomials that annihilate T is an ideal in the principal ideal domain F[x], so it is generated by a single polynomial.
- Definition. The minimal polynomial m_T(x) of T is the unique monic generator of the ideal { p ∈ F[x] : p(T) = 0 }.

Existence and uniqueness
- Existence: Each basis vector v_i ∈ V is annihilated by some nonzero polynomial (because the sequence v_i, T v_i, T^2 v_i, ... is linearly dependent in V). Let m_i be a nonzero annihilating polynomial for v_i; then the least common multiple lcm(m_1,...,m_n) annihilates every basis vector, hence annihilates T. Thus a nonzero annihilating polynomial for T exists, so the annihilator set is a nonzero ideal and has a monic generator.
- Uniqueness: Because F[x] is a PID, the annihilator ideal has a unique monic generator; that generator is m_T.

Basic properties
1. Minimality and divisibility
   - By construction m_T is monic and m_T(T)=0.
   - If p ∈ F[x] and p(T)=0 then m_T divides p. Equivalently, m_T is the monic polynomial of least degree that annihilates T.

2. Degree bound
   - deg m_T ≤ dim V. (Sketch: the sequence I, T, T^2, ... of operators is linearly dependent in the finite-dimensional space L(V) spanned by operators obtained from a basis-dependent viewpoint, or more concretely obtain annihilating polynomials for basis vectors and take lcm; in either case the resulting polynomial has degree at most dim V.)

3. Relation with characteristic polynomial
   - m_T divides the characteristic polynomial χ_T(x) (Cayley–Hamilton yields χ_T(T)=0, so by property 1 m_T | χ_T). Hence every root of m_T is a root of χ_T (counted without multiplicity information here).

4. Eigenvalues and roots
   - If λ ∈ F is an eigenvalue of T, then m_T(λ) = 0. Conversely, if m_T(λ) = 0 then λ is an eigenvalue of T. (Sketch: If m_T(λ) = 0, factor m_T = (x−λ)^k q(x) with q(λ) ≠ 0; then (T−λI)^k q(T) = 0, and one can find a nonzero vector v with (T−λI)^k v = 0 but (T−λI)^{k−1} v ≠ 0; in particular T has an eigenvector for λ.)
   - Thus the set of eigenvalues equals the set of roots of m_T (in F), though multiplicities in m_T reflect sizes of nilpotent blocks (see later).

5. Invariance under similarity / change of basis
   - If A is the matrix of T in some basis and B is the matrix of T in another basis, then m_A = m_B = m_T. In particular, m_T depends only on the operator and not on a particular matrix representation.

6. Behavior on invariant subspaces and direct sums
   - If W ⊆ V is T-invariant, then m_{T|W} divides m_T.
   - If V = U ⊕ W with both U and W T-invariant, then m_T = lcm( m_{T|U}, m_{T|W} ).

7. Minimal polynomial and diagonalizability
   - T is diagonalizable (over F) iff m_T splits over F as a product of distinct linear factors (i.e., m_T has no repeated roots). Proof idea: if m_T has no repeated roots, then by the primary decomposition (or simple argument using relatively prime annihilating factors) V decomposes into a direct sum of eigenspaces. Conversely, if T is diagonalizable then T satisfies a square-free polynomial whose roots are the eigenvalues, so m_T is square-free.

8. Degree and cyclic subspaces
   - For any v ≠ 0, define m_{T,v} to be the monic polynomial of least degree with m_{T,v}(T)v = 0 (the minimal polynomial of T relative to v). Then m_{T,v} divides m_T, and m_T = lcm{ m_{T,v} : v runs over a basis of V }. If V is cyclic for T (there exists v with span{T^k v : k ≥ 0} = V), then m_T = m_{T,v} and deg m_T = dim V.

Remarks for later use
- m_T encodes the algebraic constraints on T and is the central invariant used in operator decompositions (primary decomposition, rational canonical form, companion matrices). Later chapters will use the facts that m_T divides χ_T, that m_T factors into primary (p(x)^k) factors corresponding to T's behavior on generalized eigenspaces, and that diagonalizability is characterized by m_T being square-free. The lcm property for direct sums and divisibility for invariant subspaces are essential when assembling the global minimal polynomial from local pieces.

Zeros, linear factors, and multiplicity

Definitions
- Zero (root). For a polynomial p with coefficients in a field F, a ∈ F is a zero (or root) of p if p(a) = 0.
- Linear factor. The polynomial (z − a) is a linear factor corresponding to the root a.
- Multiplicity (algebraic multiplicity). If (z − a)^m divides p but (z − a)^(m+1) does not, we say a is a zero of p of multiplicity m (or an m-fold root).

Equivalence of zeros and linear factors
- Basic equivalence. a is a zero of p if and only if (z − a) is a factor of p.
  Proof sketch: If p(z) = (z − a)q(z) then p(a) = 0. Conversely, by the division algorithm there exist q and r with p(z) = (z − a)q(z) + r where r is constant; evaluating at z = a gives r = p(a). So p(a) = 0 implies r = 0 and hence (z − a) divides p.

Multiplicity characterized by derivatives
- Let p be a polynomial and a ∈ F. Then a has multiplicity m as a zero of p iff
  p(a) = p'(a) = p''(a) = ··· = p^(m−1)(a) = 0 and p^(m)(a) ≠ 0.
  Proof idea: If p(z) = (z − a)^m q(z) with q(a) ≠ 0, repeated application of the product rule shows the first m − 1 derivatives vanish at a while the m-th derivative equals m! q(a) ≠ 0. Conversely, if the first m − 1 derivatives vanish, Taylor expansion about a (or repeated factoring by division) yields a factor (z − a)^m.

Consequences and facts
- Degree bound. The sum of multiplicities of distinct zeros of p cannot exceed deg p.
  Reason: If p factors as (z − a1)^{m1} ··· (z − ak)^{mk} q(z) with q(a_i) ≠ 0, then deg p ≥ m1 + ··· + mk.
- Simple root. A root of multiplicity 1 is called simple. If a is a simple root, p'(a) ≠ 0.
- Repeated root tests. A polynomial p has a repeated root a (multiplicity ≥ 2) iff gcd(p, p') is nonconstant; equivalently p and p' share a common factor (z − a).

Factorization using roots and multiplicities
- If you can find a zero a of p, divide p by (z − a) to reduce degree and continue. Repeated division by (z − a) until the remainder is nonzero gives the multiplicity of a.
- When all roots lie in the coefficient field (p “splits”), p factors as
  p(z) = c∏_{i=1}^k (z − a_i)^{m_i},
  where c ≠ 0 is the leading coefficient, the a_i are the distinct roots, and m_i their multiplicities.
- Over R, not every polynomial splits into linear factors; irreducible real factors have degree 1 or 2. Over C (by the Fundamental Theorem of Algebra), every nonconstant polynomial splits into linear factors.

Examples
1) p(x) = (x − 2)^3(x + 1).
   - Roots: 2 with multiplicity 3, −1 with multiplicity 1.
   - p'(x) vanishes at 2 and at −1? p'(2) = 0 (since multiplicity ≥ 2), p'(−1) ≠ 0.

2) q(x) = x^3 − 3x^2 + 3x − 1 = (x − 1)^3.
   - q(1) = q'(1) = q''(1) = 0, q'''(1) = 6 ≠ 0, so 1 is a root of multiplicity 3.

3) r(x) = x^2 + 1 over R.
   - No real zeros, so no real linear factors; over C, r(z) = (z − i)(z + i).

Practical steps to factor p when roots are known or suspected
1. Test likely values a (rational root test if coefficients are integers) to find zeros.
2. Use polynomial long division or synthetic division to divide out (z − a) repeatedly to determine multiplicity.
3. Continue factoring the quotient until no further linear factors in the field remain.
4. If needed, check multiplicities via derivatives: evaluate p, p', p'', ... at suspected roots.

Summary (one-line)
A is a root of p iff (z − a) divides p; the multiplicity m is how many times (z − a) divides p, equivalently the order of vanishing controlled by successive derivatives; repeated division by linear factors lets you factor p up to the factorization possible in the coefficient field.

Characteristic polynomial

Let V be an n-dimensional vector space over a field F and let T: V → V be a linear operator. The characteristic polynomial of T is the polynomial p_T(λ) ∈ F[λ] defined by
p_T(λ) = det(T − λI),
where I is the identity operator on V and we regard T − λI as a linear operator depending polynomially on the scalar λ.

If A is the matrix of T with respect to any ordered basis of V, then the characteristic polynomial can be computed from that matrix as
p_T(λ) = det(A − λI_n),
where I_n is the n × n identity matrix. (Equivalently one often sees det(λI_n − A); these two differ by a factor (−1)^n, so they define the same set of roots.) Because similarity preserves determinants, p_T(λ) is independent of the choice of basis.

Basic properties:
- p_T(λ) is a monic polynomial of degree n up to the sign convention: written as det(λI − A) it is monic of degree n; written as det(A − λI) its leading coefficient is (−1)^n.
- The roots of p_T(λ) (in an algebraic closure of F) are exactly the eigenvalues of T. That is, λ0 is an eigenvalue of T if and only if p_T(λ0) = 0. Proof sketch: λ0 is an eigenvalue ⇔ T − λ0I is not invertible ⇔ det(T − λ0I) = 0.
- The multiplicity of a root λ0 of p_T is called the algebraic multiplicity of the eigenvalue λ0.

How to compute from a matrix (example for 2×2 and sketch for general n):
- For A = [[a, b], [c, d]], form A − λI = [[a − λ, b], [c, d − λ]] and compute
p_A(λ) = det(A − λI) = (a − λ)(d − λ) − bc = λ^2 − (a + d)λ + (ad − bc).
The eigenvalues are the roots of this quadratic.

- For larger n, form A − λI and compute its determinant by expansion, row/column operations that preserve the determinant up to known factors, or more efficient algorithms (LU/characteristic polynomial algorithms). Conceptually, the determinant produces an nth-degree polynomial whose zeros are precisely the eigenvalues of A.

Thus the characteristic polynomial provides an intrinsic polynomial whose roots give the spectrum of the linear operator and whose coefficients are (up to signs) elementary symmetric polynomials in the eigenvalues.

Algebraic multiplicity

Definition.
Let V be an n-dimensional vector space over a field F and T: V → V a linear operator. The characteristic polynomial of T is p_T(t) = det(tI − T). If λ ∈ F is a root of p_T(t), the algebraic multiplicity of λ is the multiplicity of λ as a root of p_T(t): that is, the largest positive integer m such that (t − λ)^m divides p_T(t). We write alg mult(λ) = m.

Basic consequences.
- λ is an eigenvalue of T if and only if alg mult(λ) ≥ 1 (equivalently p_T(λ) = 0).
- The characteristic polynomial has degree n, so the algebraic multiplicities of all eigenvalues (counted with multiplicity) sum to n. In particular, the number of distinct eigenvalues is at most n.

Relation to eigenspaces (geometric multiplicity).
For an eigenvalue λ, the eigenspace E_λ = ker(T − λI) has finite dimension, called the geometric multiplicity geom mult(λ) = dim E_λ. These multiplicities satisfy the inequalities
1 ≤ geom mult(λ) ≤ alg mult(λ).
Thus the algebraic multiplicity provides an upper bound on the number of linearly independent eigenvectors associated to λ.

Remarks on why geom ≤ alg.
Intuitively, alg mult(λ) measures how many “copies” of the factor (t − λ) occur in the characteristic polynomial, while geom mult(λ) counts how many independent eigenvectors remain after accounting for those multiplicities. Concretely, after choosing a basis that puts T into an upper-triangular (or Jordan) form, each Jordan block for λ contributes exactly one to the eigenspace dimension but contributes its block size to the algebraic multiplicity. Hence the number of blocks (geom mult) cannot exceed the total size of those blocks (alg mult).

Useful corollaries.
- If all eigenvalues of T are distinct, each has algebraic multiplicity 1, and therefore each eigenspace is one-dimensional; in particular T has n linearly independent eigenvectors.
- The sum of geometric multiplicities over all distinct eigenvalues is ≤ n (and equals n precisely when T is diagonalizable).

Eigenspace (definition)
Let V be a vector space over field F and T : V → V linear. For λ ∈ F, the eigenspace corresponding to λ is
Eλ = {v ∈ V : T v = λ v}.
Equivalently, Eλ = ker(T − λ I).

Eigenspace is a subspace (proof)
Since Eλ = ker(T − λ I) and the kernel of any linear map is a subspace, Eλ is a subspace of V. Equivalently, check directly:
- 0 ∈ Eλ because T0 = 0 = λ0.
- If u, v ∈ Eλ then T(u + v) = Tu + Tv = λu + λv = λ(u + v), so u + v ∈ Eλ.
- If c ∈ F and v ∈ Eλ then T(cv) = cTv = cλv = λ(cv), so cv ∈ Eλ.
Thus Eλ is closed under addition and scalar multiplication, hence a subspace.

Geometric multiplicity and number of independent eigenvectors
The dimension of Eλ, denoted dim Eλ, is called the geometric multiplicity of the eigenvalue λ. The geometric multiplicity equals the maximum number of linearly independent eigenvectors associated with λ. Precisely:
- If dim Eλ = k then there exist k linearly independent vectors v1,…,vk in V with T vi = λ vi, and no set of more than k eigenvectors for λ can be linearly independent.
- Conversely, any set of linearly independent eigenvectors for λ is a linearly independent subset of Eλ, so its size ≤ dim Eλ.

Thus the eigenspace gives exactly the space of eigenvectors for λ (together with 0), and its dimension tells you how many independent eigenvectors for λ you can obtain. In particular, λ is an eigenvalue ⇔ dim Eλ ≥ 1.

Definition
- Let V be a vector space over a field F and let T : V → V be a linear operator. A scalar λ in F is an eigenvalue of T if there exists a nonzero vector v in V such that
  T(v) = λ v.
  Any such nonzero v is called an eigenvector of T corresponding to λ.
- Equivalently, v is an eigenvector for λ exactly when v ≠ 0 and (T − λ I)v = 0, i.e. v lies in the null space of T − λ I.

Notes
- The zero vector is never an eigenvector.
- Eigenvalues and eigenvectors depend on the underlying field F. For example, a real operator may have no real eigenvalues but may have complex eigenvalues if we extend scalars to C.
- For a matrix A representing T with respect to some basis, the same definitions apply: λ is an eigenvalue of A if there exists x ≠ 0 with A x = λ x.

How to verify an eigenpair (λ, v)
1. Direct check (operator or matrix): compute T(v) (or A x). If T(v) equals λ v and v ≠ 0, then λ is an eigenvalue and v an eigenvector.
2. Solve (T − λ I)v = 0:
   - For a suspected λ, solve the homogeneous linear system (T − λ I)v = 0. If there is a nonzero solution, λ is an eigenvalue and every nonzero solution is an eigenvector.
3. Characteristic equation (matrix method): for finite-dimensional V and matrix A, λ is an eigenvalue iff det(A − λ I) = 0. The determinant gives the characteristic polynomial; its roots are the eigenvalues. (After finding λ, find eigenvectors by solving (A − λ I)x = 0.)

Basic examples
1. Scalar multiple (dilation) on R^n:
   - T(x) = c x for some scalar c. Every nonzero vector x satisfies T(x) = c x, so c is an eigenvalue and every nonzero vector is an eigenvector.
2. Diagonal matrix:
   - A = diag(2, 3) on R^2. The standard basis vectors e1 and e2 satisfy A e1 = 2 e1 and A e2 = 3 e2. Thus 2 and 3 are eigenvalues with eigenvectors spanning the coordinate axes.
3. Projection onto a line L in R^2:
   - Let P be orthogonal projection onto L. Then vectors in L satisfy P(v) = v (eigenvalue 1) and vectors orthogonal to L satisfy P(w) = 0 (eigenvalue 0). So 1 and 0 are eigenvalues; eigenvectors are nonzero vectors in L and in L⊥ respectively.
4. Reflection across a line in R^2:
   - Reflection R has R(v) = v for vectors along the mirror (eigenvalue 1) and R(w) = −w for vectors perpendicular to the mirror (eigenvalue −1).

Basic nonexamples / common pitfalls
1. Rotation by a nonzero angle in R^2:
   - A rotation by 90° (or any angle not 0 or π) has no real eigenvectors because no nonzero real v satisfies rotation(v) = λ v for a real scalar λ. Over C one can have complex eigenvalues, but over R there are none.
2. Zero vector mistakenly called an eigenvector:
   - If T(v) = λ v holds with v = 0 for every λ, this does not make λ an eigenvalue. The definition requires a nonzero v.
3. A vector v with T(v) not a scalar multiple of v:
   - For example, with A = [[0,1],[0,0]] and v = e1, A e1 = 0 which is 0·e1, so e1 is an eigenvector for λ = 0; but e2 satisfies A e2 = e1, which is not a scalar multiple of e2, so e2 is not an eigenvector. Checking must show exact scalar proportionality.
4. Assuming distinct eigenvalues for different bases:
   - Eigenvalues are intrinsic to the operator (not to the basis). A change of basis gives a similar matrix with the same eigenvalues. However, a particular vector that looks like an eigenvector in one coordinate representation might not be an eigenvector of the operator unless it is the same geometric vector.

Quick verification examples
- Example 1 (direct): A = [[2,0],[0,3]], x = (1,0)^T. Compute A x = (2,0)^T = 2 x. So λ = 2, x is an eigenpair.
- Example 2 (solve nullspace): A = [[1,1],[0,1]]. Characteristic polynomial det(A − λ I) = (1−λ)^2; λ = 1 only. Solve (A − I)x = [[0,1],[0,0]] x = 0 gives x = t(1,0)^T, t ≠ 0. So eigenvectors are nonzero multiples of (1,0)^T; (A − I) has a nontrivial nullspace so λ = 1 is an eigenvalue.
- Example 3 (nonexample — rotation): Rθ on R^2 with θ = 90°. For any real λ and nonzero v, Rθ(v) is orthogonal to v while λ v is parallel to v, so equality cannot hold; no real eigenvalues.

Summary checklist when given T (or A) and a candidate λ or v
- To verify λ is an eigenvalue: check existence of nonzero v with (T − λ I)v = 0. For matrices, compute det(A − λ I) to locate candidates, then solve for nullspace.
- To verify v is an eigenvector: check v ≠ 0 and T(v) is exactly a scalar multiple of v; read off that scalar as the eigenvalue.
- Remember field matters (real vs complex) and the zero vector is never allowed as an eigenvector.

Diagonalization and Eigenbases

Definition
- An operator T on a finite-dimensional vector space V (or an n×n matrix A) is diagonalizable if there exists a basis of V with respect to which the matrix of T is diagonal. Equivalently, A is diagonalizable if there is an invertible P with P^{-1}AP = D a diagonal matrix.

Basic equivalent criteria
The following are equivalent for T ∈ L(V) (dim V = n) or A ∈ F^{n×n}:
1. T is diagonalizable.
2. V has a basis consisting entirely of eigenvectors of T.
3. V is the direct sum of its eigenspaces: V = ⊕_{λ} E_λ, where E_λ = {v ∈ V : T v = λ v} and the sum runs over all eigenvalues λ of T.
4. There exists an invertible P whose columns are eigenvectors of T such that P^{-1}AP is diagonal; the diagonal entries are the eigenvalues corresponding to those columns.

Practical check (how to use the criteria)
1. Find all eigenvalues λ of T (solve (T − λI)v = 0 or det(A − λI) = 0 if using matrices).
2. For each eigenvalue λ compute the eigenspace E_λ = null(T − λI) and its dimension dim E_λ (the geometric multiplicity).
3. T is diagonalizable iff the sum of the dimensions of the eigenspaces equals n:
   sum_{λ} dim E_λ = n.
   Equivalently, for every eigenvalue λ, the geometric multiplicity equals its algebraic multiplicity (the multiplicity of λ as a root of the characteristic polynomial).
4. If diagonalizable, pick bases of each eigenspace and concatenate them to get a basis of V of eigenvectors. Form P with those eigenvectors as columns; then P^{-1}AP = D is diagonal with the corresponding eigenvalues on the diagonal.

Useful sufficient/necessary conditions
- Sufficient: If A has n distinct eigenvalues (all eigenvalues are different), then A is diagonalizable. (Distinct eigenvalues ⇒ eigenspaces are 1-dimensional and independent.)
- Necessary and sufficient: For each eigenvalue, geometric multiplicity ≤ algebraic multiplicity, and equality for every eigenvalue is necessary and sufficient for diagonalizability.
- Polynomial criterion: If the minimal polynomial of T splits into distinct linear factors (i.e., has no repeated roots), then T is diagonalizable. Conversely, if T is diagonalizable then its minimal polynomial splits into distinct linear factors.

What diagonalization does to matrix form
- Diagonalization is a change of basis: if P is the invertible matrix whose columns are a basis of eigenvectors, then D = P^{-1}AP is diagonal.
- The diagonal entries of D are eigenvalues of A; the multiplicity of an eigenvalue on the diagonal equals the dimension of the corresponding eigenspace used in the basis.
- Diagonal matrices are simplest for computations: powers, exponentials, and functions of the matrix are computed entrywise on the diagonal.

Remarks and pitfalls
- Having eigenvectors is not enough: they must form a basis (i.e., be linearly independent and number n).
- Over a field where the characteristic polynomial does not split (e.g., real numbers and complex eigenvalues), diagonalization over that field may be impossible even if diagonalizable over an extension field.
- Non-diagonalizable matrices include Jordan blocks of size >1; these have fewer than n linearly independent eigenvectors.

Quick summary checklist to decide diagonalizability
- Compute eigenvalues.
- For each eigenvalue, compute dim E_λ.
- If sum dim E_λ = n (equivalently each geometric multiplicity = algebraic multiplicity), then diagonalizable; construct P from eigenvectors to obtain D = P^{-1}AP.

Minimal polynomial viewpoint for eigenvalues and diagonalizability

Definition and basic fact
- The minimal polynomial m_T of a linear operator T ∈ L(V) (over a field F) is the unique monic polynomial of least degree such that m_T(T) = 0.
- For any scalar λ ∈ F, if v ≠ 0 is an eigenvector with eigenvalue λ, then m_T(λ) = 0. Thus every eigenvalue of T is a root of m_T.

Roots of the minimal polynomial vs. eigenvalues
- If m_T splits over F (i.e. factors as a product of linear factors in F[x]), then the set of roots of m_T equals the set of eigenvalues of T.
  - Reason: If (x − λ) divides m_T, then m_T(T) = 0 implies (T − λI) is not invertible, so ker(T − λI) ≠ {0} and λ is an eigenvalue. Combined with the basic fact above, the roots exactly coincide with eigenvalues when m_T splits.
- If m_T does not split over F, its roots in an extension field give the eigenvalues of T over that extension; over F one only sees those eigenvalues lying in F.

Degree constraint
- deg m_T ≤ dim V. In particular the number of distinct eigenvalues (over a splitting field) is at most dim V.

Factorization and diagonalizability
- Suppose m_T factors over F as
  m_T(x) = ∏_{i=1}^r (x − λ_i)^{k_i},
  with distinct λ_i ∈ F and positive integers k_i.
- T is diagonalizable ⇔ every exponent k_i = 1 (equivalently, m_T has no repeated factors).
  - Proof (⇒): If T is diagonalizable, V has a basis of eigenvectors for the distinct eigenvalues λ_1,...,λ_r. On that basis T acts by scalars, so the polynomial p(x) = ∏_{i=1}^r (x − λ_i) annihilates T. By minimality of m_T, m_T divides p, hence m_T equals p (up to monic normalization) and has only simple factors.
  - Proof (⇐): If m_T has only simple linear factors, m_T = ∏_{i=1}^r (x − λ_i), then the factors (x − λ_i) are pairwise coprime. By the Chinese Remainder/Lagrange-interpolation functional calculus one can construct polynomials e_i(x) with e_i(x) ≡ 1 (mod x − λ_i) and e_i(x) ≡ 0 (mod x − λ_j) for j ≠ i. Then P_i := e_i(T) are projections onto nonzero subspaces V_i = ker(T − λ_i I), satisfy P_i P_j = 0 for i ≠ j and ∑_i P_i = I, giving a direct-sum decomposition V = ⊕_i V_i. Each V_i is an eigenspace, so V has a basis of eigenvectors and T is diagonalizable.
- Equivalently: T diagonalizable ⇔ m_T splits into distinct linear factors over F.

Corollaries and remarks
- If some factor (x − λ)^k with k ≥ 2 divides m_T, then T is not diagonalizable: there is necessarily a generalized eigenvector chain for λ of length > 1.
- The algebraic multiplicity of λ as a root of the characteristic polynomial can exceed 1 while the exponent k_i in m_T measures the size of the largest Jordan block for λ (over a splitting field). Diagonalizability requires all such largest-block sizes be 1.
- Practical use: compute or bound m_T (or find any annihilating polynomial) to locate possible eigenvalues quickly — any candidate eigenvalue must be a root of every annihilating polynomial, in particular of the minimal polynomial.

Example (illustrative)
- If m_T(x) = (x − 2)^3(x + 1), then the eigenvalues (over F containing 2 and −1) are 2 and −1, and T is not diagonalizable because (x − 2) appears with exponent 3 > 1.
- If m_T(x) = (x − 2)(x + 1), then T is diagonalizable (if m_T is over the base field), with eigenspaces ker(T − 2I) and ker(T + I).

Summary sentence
- The minimal polynomial both constrains which scalars can be eigenvalues (they must be its roots) and encodes diagonalizability: T is diagonalizable exactly when the minimal polynomial splits into distinct linear factors.

Gram–Schmidt Orthonormalization

Statement. Let V be an inner product space over R or C. Given a finite linearly independent list v1, v2, ..., vn in V, there exists an orthonormal list e1, e2, ..., en in V with
span(e1, ..., ek) = span(v1, ..., vk) for each k = 1,...,n.
In particular, e1,...,en span the same subspace as v1,...,vn.

Construction (Gram–Schmidt). Define vectors u1, ..., un and e1, ..., en recursively by
- u1 = v1,  e1 = u1 / ||u1||.
- For i = 2,...,n set
  ui = vi − sum_{j=1}^{i-1} <vi, ej> ej,
  ei = ui / ||ui||.
Here <·,·> denotes the inner product and ||·|| the induced norm.

Remarks on correctness and conditions.
- Linearly independent input is essential: if v1,...,vn are linearly independent then each ui produced above is nonzero, so the normalization step is valid. If at some step ui = 0 then vi lies in span(v1,...,v_{i-1}), so the original list was linearly dependent.
- The process works for any finite list in any inner product space (real or complex). For an arbitrary (possibly dependent) finite list, Gram–Schmidt produces an orthonormal list whose span equals the span of the original list after discarding zero ui’s.
- At each step i the vector ui is orthogonal to e1,...,e_{i-1} by construction, so the normalized ei are mutually orthonormal. The span equality span(e1,...,ei) = span(v1,...,vi) follows by induction because ui is in span(v1,...,vi) and vi is expressible using ui and earlier ej’s.

Key formulas.
- Projection of v onto the subspace spanned by e1,...,e_{i-1}: proj_{span(e1,...,e_{i-1})} v = sum_{j=1}^{i-1} <v, ej> ej.
- Orthogonal component used in step i: ui = vi − proj_{span(e1,...,e_{i-1})} vi.

Thus Gram–Schmidt converts a finite linearly independent list into an orthonormal list spanning the same subspace; if dependence occurs, the nonzero outputs give an orthonormal basis for the span of the original list.

Inner product (real and complex)
- Let V be a vector space over R or C. An inner product on V is a function ⟨·,·⟩ : V × V → R (real case) or → C (complex case) satisfying, for all u,v,w ∈ V and scalar α:
  1. Conjugate symmetry: ⟨u,v⟩ = overline{⟨v,u⟩}. (In the real case this is symmetry: ⟨u,v⟩ = ⟨v,u⟩.)
  2. Linearity in the first argument and conjugate-linearity in the second (Axler's convention): ⟨αu+v,w⟩ = α⟨u,w⟩ + ⟨v,w⟩ and ⟨u,αv+w⟩ = overline{α}⟨u,v⟩ + ⟨u,w⟩.
  3. Positive-definiteness: ⟨v,v⟩ ≥ 0 with equality iff v = 0.

Induced norm
- The inner product induces a norm (length) on V by
  ||v|| := sqrt(⟨v,v⟩).
  This satisfies the usual norm properties (nonnegativity, definiteness, homogeneity).

Core inequalities
- Cauchy–Schwarz inequality:
  |⟨u,v⟩| ≤ ||u|| · ||v|| for all u,v ∈ V.
  Equality holds iff u and v are linearly dependent (i.e., one is a scalar multiple of the other).

- Triangle inequality:
  ||u + v|| ≤ ||u|| + ||v|| for all u,v ∈ V.

These two inequalities are the fundamental facts that make the induced norm behave like geometric length.

Adjoints — definition and basic properties

Definition (Adjoint). Let V and W be inner product spaces over F (R or C). For a linear map T: V → W, an adjoint of T is a linear map T*: W → V satisfying
  <T v, w> = <v, T* w>
for all v ∈ V and w ∈ W. This inner-product identity is the defining characterization of the adjoint.

Existence and uniqueness. For finite-dimensional inner product spaces (or more generally when V is complete and one uses the Riesz representation theorem), the map T has a unique adjoint T*. Uniqueness follows immediately: if A and B both satisfy <T v, w> = <v, A w> = <v, B w> for all v, then <v, (A−B)w> = 0 for all v, hence (A−B)w = 0 for every w, so A = B. Existence is obtained by, for each fixed w ∈ W, viewing the functional v ↦ <T v, w> on V and applying Riesz to get a unique vector T* w representing that functional.

Basic algebraic properties. For linear maps between inner product spaces the adjoint has the following properties (where S, T are composable linear maps and a ∈ F):
- (S + T)* = S* + T*.
- (aT)* = \overline{a}\,T* (conjugation when F = C).
- (ST)* = T* S*.
- (T*)* = T.
- I* = I.
- If T is invertible, then (T^{-1})* = (T*)^{-1}.

Range and kernel relations. The adjoint relates ranges and nullspaces via orthogonal complements:
- null(T*) = (range T)⊥.
- range(T*) = (null T)⊥.
In particular, T is surjective iff T* is injective, and T is injective iff T* has dense range (or, in finite dimensions, iff T* is surjective).

Operator norm. The adjoint preserves the operator norm:
  ||T*|| = ||T||.

Matrix representation. If orthonormal bases are chosen for V and W, the matrix of T* is the conjugate-transpose (Hermitian transpose) of the matrix of T. Thus in matrix terms the inner-product identity becomes the usual relation A* = \overline{A}^T.

Takeaway. The adjoint is uniquely determined by the simple inner-product identity <T v, w> = <v, T* w>, and from that identity one derives all standard algebraic and geometric relations linking T, T*, ranges, nullspaces, and operator norms.

Linear Functionals and the Riesz Representation

Theorem (Riesz Representation for Finite-Dimensional Inner-Product Spaces).
Let V be a finite-dimensional inner-product space over F (R or C). For every linear functional φ ∈ V* there exists a unique u ∈ V such that
φ(v) = ⟨v, u⟩  for all v ∈ V.

Proof (construction via an orthonormal basis).
Let {e1,...,en} be an orthonormal basis of V. For v = ∑j vj ej we have ⟨v, ej⟩ = vj. Define scalars uj = φ(ej) (when F = C treat these as complex numbers). Put u = ∑j conj(uj) ej. Then for any v,
⟨v, u⟩ = ⟨∑j vj ej, ∑k conj(uk) ek⟩ = ∑j ∑k vj conj(uk) ⟨ej, ek⟩
= ∑j vj conj(uj) = ∑j vj φ(ej) = φ(∑j vj ej) = φ(v),
so φ(v) = ⟨v, u⟩ for all v.

Uniqueness.
If u and u' both satisfy φ(v) = ⟨v, u⟩ = ⟨v, u'⟩ for all v, then ⟨v, u - u'⟩ = 0 for all v. Taking v = u - u' gives ⟨u - u', u - u'⟩ = 0, hence u - u' = 0. Thus u = u'.

Alternative proof sketch (kernel + orthogonal complement).
Let K = ker φ. If φ ≡ 0 then u = 0 works. Otherwise K has codimension 1, so K⊥ is one-dimensional; choose nonzero w ∈ K⊥. For v write v = x + αw with x ∈ K and α ∈ F. Since φ(x) = 0 and φ(w) ≠ 0, define u = conj(φ(w))/∥w∥^2 · w. One checks φ(v) = ⟨v, u⟩ for all v, and uniqueness follows as above.

Remarks.
- The representation is canonical once an inner product is fixed; it gives an isomorphism V ≅ V* via u ↦ (v ↦ ⟨v,u⟩).
- Over C the conjugation in coefficients is essential (so coordinates of u involve complex conjugates of φ(ej)).

Orthogonal complement

- Definition. Let V be an inner-product space and W a subspace of V. The orthogonal complement of W is
  W⊥ = { v in V : ⟨v,w⟩ = 0 for all w in W }.
  W⊥ is itself a subspace of V.

- Key facts (finite-dimensional case; same conclusions hold when W is closed in an infinite-dimensional Hilbert space):
  - V decomposes as a direct sum V = W ⊕ W⊥. Equivalently, every v in V can be written uniquely as v = w + u with w ∈ W and u ∈ W⊥.
  - (W⊥)⊥ = W.
  - dim W + dim W⊥ = dim V.

Orthogonal projection

- Existence and uniqueness. Given v ∈ V and subspace W, there is a unique w ∈ W such that v − w ∈ W⊥. This w is called the orthogonal projection of v onto W and is denoted P_W v.

- Minimization / best-approximation property. The projected vector w = P_W v is the best approximation to v from W:
  ||v − w|| = min_{x ∈ W} ||v − x||.
  Moreover x ∈ W is a minimizer iff v − x ∈ W⊥, so the minimizer is unique.

- Linear operator and algebraic properties. The map P_W : V → W given by v ↦ P_W v is a linear operator satisfying
  - Idempotence: P_W^2 = P_W.
  - Self-adjointness: ⟨P_W v, u⟩ = ⟨v, P_W u⟩ for all u,v (so P_W* = P_W).
  - Range(P_W) = W and Null(P_W) = W⊥.
  - Norm inequality: ||P_W v|| ≤ ||v|| for all v.

- Formulas in coordinates.
  - If {w1,...,wk} is an orthonormal basis of W, then
    P_W v = Σ_{j=1}^k ⟨v, w_j⟩ w_j.
  - If the columns of a matrix A form a basis for W (over R or C) then the matrix of P_W is P = A (A* A)^{-1} A*, where A* is the conjugate-transpose; this is the usual least-squares/projection matrix.

- Geometric interpretation. Orthogonal projection splits v into its component in W (closest point in W) and its orthogonal error in W⊥. This decomposition is the reason projections give optimal least-squares approximations.

Orthogonality
- Two vectors v and w in an inner product space are orthogonal if their inner product is zero: <v, w> = 0. We write v ⟂ w.
- A set of vectors is an orthogonal set if every distinct pair of vectors in the set is orthogonal.

Key fact (orthogonality ⇒ linear independence)
- Any finite orthogonal set of nonzero vectors is linearly independent.
- Proof sketch: Suppose {v1,...,vk} is orthogonal and not all coefficients a_i in a1 v1 + ... + ak vk = 0 are zero. Take inner product with vj. Because <vi, vj> = 0 for i ≠ j and <vj, vj> ≠ 0, we get aj <vj, vj> = 0, so aj = 0. This contradiction shows all a_i = 0.

Orthonormal sets and bases
- An orthonormal set is an orthogonal set whose vectors each have norm 1: for each v in the set, ||v|| = 1 (equivalently <v,v> = 1).
- An orthonormal basis is an orthonormal set that is also a basis of the space (spans the space and is linearly independent).

Why orthonormal bases are useful (coordinate simplifications)
- Simple coordinates: If {e1,...,en} is an orthonormal basis for an inner product space V and v ∈ V, then the coordinates of v with respect to this basis are simply the inner products:
  coefficient along ej = <v, ej>.
  So v = sum_{j=1}^n <v, ej> ej.
- Projection formula: The orthogonal projection of v onto the span of an orthonormal subset {e1,...,em} is
  Proj(v) = sum_{j=1}^m <v, ej> ej.
- Parseval / Pythagorean identity: For an orthonormal basis {e1,...,en},
  ||v||^2 = sum_{j=1}^n |<v, ej>|^2.
  More generally, if {e1,...,em} is orthonormal (not necessarily a basis), then
  ||v||^2 = ||Proj(v)||^2 + ||v - Proj(v)||^2,
  with ||Proj(v)||^2 = sum_{j=1}^m |<v, ej>|^2.

Consequences and practical points
- Computing coordinates reduces to taking inner products; no linear system or matrix inversion needed.
- Orthonormal bases make checking independence trivial (nonzero orthogonal vectors) and simplify norm and inner-product computations.
- In practice one often converts a spanning set into an orthonormal basis via the Gram–Schmidt process so these simplifications become available.

Adjoint operators

Definition
- Let V be an inner-product space over F (R or C). For a linear operator T: V → V, an adjoint of T is a linear operator T*: V → V such that
  <T v, w> = <v, T* w> for all v, w ∈ V.
- If such an operator exists, it is called the adjoint of T.

Existence and uniqueness in finite dimensions
Theorem. If V is finite-dimensional, every linear operator T: V → V has a unique adjoint T*.

Proof.
1) Uniqueness. Suppose S and S' both satisfy <T v, w> = <v, S w> = <v, S' w> for all v,w. Then for every v,w we have <v, (S−S')w> = 0. Fix w; the linear functional v ↦ <v, (S−S')w> is identically zero, so (S−S')w = 0 (finite-dimensionality gives nondegeneracy of the inner product). Since this holds for all w, S−S' = 0, hence S = S'.

2) Existence. For each fixed w ∈ V define a linear functional φ_w on V by φ_w(v) = <T v, w>. By the Riesz Representation Theorem (valid in finite dimensions), there is a unique vector u ∈ V such that φ_w(v) = <v, u> for all v. Define T* w := u. Doing this for every w defines a map T*: V → V. Linearity of T*: for α,β ∈ F and w1,w2 ∈ V,
   φ_{α w1 + β w2}(v) = <T v, α w1 + β w2> = α <T v, w1> + β <T v, w2>
   = α <v, T* w1> + β <v, T* w2> = <v, α T* w1 + β T* w2>.
By uniqueness of the Riesz representative, T*(α w1 + β w2)=α T* w1 + β T* w2. Thus T* is linear and satisfies <T v, w> = <v, T* w> for all v,w. This proves existence.

Coordinate description and computation
- Orthonormal basis. Let {e1,...,en} be an orthonormal basis for V. Let A be the matrix of T in this basis, so T(ej) = Σ_i a_{ij} e_i and A = (a_{ij}). Then the matrix of T* in the same orthonormal basis is the conjugate transpose of A:
  [T*] = A* = (A)¯^T (i.e., (a_{ij}*) = overline(a_{ji})).
  Proof sketch: compute <T e_j, e_i> = a_{ij} and use <T e_j, e_i>=<e_j, T* e_i>= overline( (entry of T* at (j,i)) ).

- Real inner product spaces: conjugation is trivial, so the adjoint matrix is the transpose. For example, with the standard orthonormal basis in R^2, if A = [[1,2],[3,4]], then A* = A^T = [[1,3],[2,4]].

- Complex inner product spaces: the adjoint is the conjugate transpose. Example: A = [[1, i],[2−i, 3]] → A* = [[1̄, (2−i)̄],[ī, 3̄]]^T = [[1,2+i],[−i,3]].

- Non-orthonormal basis or nonstandard inner product. If {b1,...,bn} is any basis, let G be the Gram matrix G = (⟨b_j, b_i⟩) (rows indexed by i). If A is the matrix of T relative to this basis, then the matrix A# of the adjoint satisfies
  G A# = A^* G,
  so
  A# = G^{-1} A^* G,
  where A^* denotes the conjugate transpose of A (matrix adjoint in the usual sense). Equivalently, if the inner product is represented by G via ⟨x,y⟩ = x^* G y (coordinates), then the adjoint of the operator with matrix A is G^{-1} A^* G.

Worked example with a non-orthonormal basis
- Let V = R^2 with basis b1 = (1,1), b2 = (1,0) and the standard dot product. Gram matrix
  G = [⟨b_j,b_i⟩] = [[⟨b1,b1⟩,⟨b2,b1⟩],[⟨b1,b2⟩,⟨b2,b2⟩]] = [[2,1],[1,1]].
- Let T be given in this basis by A = [[0,1],[1,0]] (it swaps coordinates in this basis). Compute A^T = A (real symmetric). Then
  A# = G^{-1} A^T G.
  Compute G^{-1} = [[1,-1],[-1,2]] (check), then A# = G^{-1} A G. Carrying out the multiplication gives the matrix of T* in the b-basis; converting back to standard coordinates yields the operator in standard form.

Practice problems
1) Let T on C^2 (standard orthonormal basis) have matrix A = [[1+i, 2],[3−i, 4i]]. Compute T*.
2) On R^3 with standard inner product, show that the matrix of the adjoint is the transpose. Compute the adjoint of A = [[0,1,2],[−1,3,0],[4,0,5]].
3) Let V have basis b with Gram matrix G and let A be the matrix of T in this basis. Verify directly that the matrix A# = G^{-1} A^* G satisfies ⟨A x, y⟩ = ⟨x, A# y⟩ for coordinate vectors x,y.

Key takeaways
- The adjoint T* is defined by <T v, w> = <v, T* w>.
- In finite dimensions T* always exists and is unique.
- With respect to an orthonormal basis, the matrix of T* is the conjugate transpose of the matrix of T.
- For non-orthonormal bases, use the Gram matrix to convert: A# = G^{-1} A^* G.

Section 38 — Self‑Adjoint and Normal Operators

Definitions
- Self‑adjoint operator: T on an inner‑product space V is self‑adjoint if T = T*, i.e. <T x, y> = <x, T y> for all x,y in V.
- Normal operator: T is normal if T T* = T* T. Equivalently, ||T x|| = ||T* x|| for all x in V.

Basic consequences and identities
- For any operator T and vectors v,w, <T v, w> = <v, T* w>. This is used repeatedly.
- If T is normal then (T − λI) is normal for every scalar λ, and T and T* commute with polynomials in T (useful in spectral arguments).

Self‑adjoint operators (T = T*)
1. Eigenvalues are real.
   Proof: If T v = λ v with v ≠ 0, then
   λ <v,v> = <λ v, v> = <T v, v> = <v, T v> (since T = T*) = <v, λ v> = λ̄ <v,v>.
   As <v,v> ≠ 0, λ = λ̄, so λ ∈ R.

2. Eigenspaces for distinct eigenvalues are orthogonal.
   Proof: If T v = λ v and T w = μ w with λ ≠ μ, then
   λ <v,w> = <T v, w> = <v, T w> = <v, μ w> = μ̄ <v,w>.
   For a self‑adjoint operator μ̄ = μ (eigenvalues real), so (λ − μ) <v,w> = 0. Since λ ≠ μ, <v,w> = 0.

3. Orthogonal diagonalization (finite‑dimensional, over R or C): A self‑adjoint operator on a finite‑dimensional inner‑product space has an orthonormal basis of eigenvectors (this is the spectral theorem for self‑adjoint operators). Thus matrices of self‑adjoint operators are diagonalizable by a unitary (orthogonal) change of basis, with real diagonal entries.

Normal operators (T T* = T* T)
1. If T v = λ v (v ≠ 0), then T* v = λ̄ v.
   Proof: From <T v, v> = <v, T* v> we get λ <v,v> = <v, T* v>. Taking conjugates gives λ̄ <v,v> = <T* v, v> = <v, T v>̄ etc.; more directly: compute
   ||T v||^2 = <T v, T v> = <v, T* T v> = <v, T T* v> = <T* v, T* v> = ||T* v||^2.
   If Tv = λ v then ||T* v|| = |λ| ||v||, and one checks T* v is a scalar multiple of v, yielding T* v = λ̄ v.

2. Orthogonality relations for eigenvectors.
   - If Tv = λ v and Tw = μ w, then
     λ <v,w> = <T v, w> = <v, T* w> = μ̄ <v,w>,
     so (λ − μ̄) <v,w> = 0.
   - Consequences:
     * If λ and μ are distinct real numbers, then <v,w> = 0 (since μ̄ = μ).
     * In the typical complex case, whenever λ ≠ μ̄ the eigenvectors are orthogonal.
     * In particular for normal operators on a complex finite‑dimensional space, one can refine this to the standard spectral theorem: T is unitarily diagonalizable — there exists an orthonormal basis of V consisting of eigenvectors of T, and T is diagonal with respect to that basis. (This implies eigenvectors corresponding to distinct eigenvalues can be chosen orthogonal; in actual proofs one uses that eigenspaces for different eigenvalues are orthogonal and that V decomposes into the orthogonal direct sum of these eigenspaces.)

3. Norm identity.
   - For all x, ||T x|| = ||T* x|| when T is normal. This follows from <T x, T x> = <T* x, T* x> via T T* = T* T.

Examples and applications
1. Real symmetric matrices (A = A^T) and complex Hermitian matrices (A = A*) are self‑adjoint. Their eigenvalues are real and eigenvectors corresponding to different eigenvalues are orthogonal. Use this to diagonalize quadratic forms or to find orthonormal eigenbases.

2. Orthogonal (real) or unitary (complex) matrices U satisfy U* U = I, hence are normal (U U* = U* U = I). Their eigenvalues lie on the unit circle; they may not be real, so they need not be self‑adjoint. Nevertheless, a unitary matrix is diagonalizable by a unitary matrix (spectral theorem for normal operators).

   Example: A rotation matrix in R^2 by angle θ (θ ≠ 0,π) is not self‑adjoint (not symmetric) but is normal. Over C it has eigenvalues e^{± i θ} with orthonormal eigenvectors in C^2.

3. Orthogonal projection P onto a subspace is self‑adjoint and satisfies P^2 = P. Its eigenvalues are 0 and 1 (real), with eigenspaces equal to the subspace and its orthogonal complement — hence orthogonal decomposition V = range(P) ⊕ range(P)⊥.

4. A normal but non‑self‑adjoint example: take a diagonal matrix with entries i and −i on the diagonal (over C). It commutes with its adjoint (it is diagonal), so it is normal; its eigenvalues are nonreal and the standard basis gives an orthonormal eigenbasis.

How to use these facts in practice
- To test if eigenvalues must be real, check self‑adjointness T = T*. If so, immediately conclude eigenvalues ∈ R.
- To find orthonormal eigenbases: check normality. If T is normal and V finite‑dimensional over C, apply the spectral theorem to diagonalize T by a unitary matrix. For real symmetric matrices the same holds with orthogonal diagonalization.
- To prove orthogonality of two eigenvectors, use the identity (λ − μ̄) <v,w> = 0 derived from <T v, w> = <v, T* w>. For self‑adjoint T this simplifies to (λ − μ) <v,w> = 0, giving orthogonality whenever λ ≠ μ.

Key takeaways
- Self‑adjoint ⇒ real eigenvalues, eigenspaces for distinct eigenvalues orthogonal, orthonormal eigenbasis exists (finite‑dimensional).
- Normal ⇒ behaves like a “unitarily diagonalizable” operator: eigenvectors can be chosen orthonormal and T is diagonalizable by a unitary matrix (finite‑dimensional over C); eigenvalues need not be real but have controlled conjugation relations with T*.
- Use the inner‑product identities <T v, w> = <v, T* w> and the normality relation T T* = T* T to derive orthogonality and spectral facts.

Section 39 — Spectral Theorem (Real Case: Self‑Adjoint Operators)

Theorem (Real Spectral Theorem). Let V be a finite‑dimensional real inner product space and let T : V → V be self‑adjoint (i.e. ⟨T u, v⟩ = ⟨u, T v⟩ for all u, v). Then V has an orthonormal basis of eigenvectors of T. Equivalently, with respect to some orthonormal basis the matrix of T is diagonal with real entries (the eigenvalues).

Proof.
1. Existence of a real eigenvalue and eigenvector.
Define the Rayleigh quotient R on nonzero vectors by R(v) = ⟨T v, v⟩/⟨v, v⟩. Because the unit sphere {v : ⟨v, v⟩ = 1} is compact and R is continuous, R attains a maximum value λ at some unit vector v0. We claim T v0 = λ v0.

For any w ∈ V and real t small, set u(t) = v0 + t w. Consider φ(t) = R(u(t)). Because v0 is a maximizer and φ is differentiable at 0, φ′(0) = 0. Compute (using ⟨v0, v0⟩ = 1)
φ(t) = ⟨T(v0+tw), v0+tw⟩ / ⟨v0+tw, v0+tw⟩.
Differentiate at 0 to get
0 = φ′(0) = 2⟨T v0, w⟩ − 2λ⟨v0, w⟩,
so ⟨T v0 − λ v0, w⟩ = 0 for every w. Hence T v0 − λ v0 = 0, so v0 is an eigenvector with eigenvalue λ ∈ R (note λ is real because ⟨T v0, v0⟩ is real).

2. Reduce dimension by orthogonal complement.
Let u = v0. Consider U = {u}⊥, the orthogonal complement of u. For any x ∈ U and any y ∈ U,
⟨T x, y⟩ = ⟨x, T y⟩ (self‑adjointness) and also ⟨T x, u⟩ = ⟨x, T u⟩ = ⟨x, λ u⟩ = 0,
so T x ∈ U. Thus the restriction T|U : U → U is self‑adjoint on the (dim V − 1)‑dimensional space U.

3. Induction to obtain an orthonormal eigenbasis.
By induction on dimension: the one‑dimensional case is trivial. Having found u and observed T|U is self‑adjoint on U, apply the same argument to T|U to obtain an orthonormal basis of U consisting of eigenvectors of T. Together with u this gives an orthonormal basis of V of eigenvectors of T. This completes the proof.

Remarks and consequences

- Diagonalization. If {e1, …, en} is an orthonormal eigenbasis with T ei = λi ei, then the matrix of T in that basis is diagonal diag(λ1, …, λn). Conversely, any real symmetric matrix (matrix of a self‑adjoint operator relative to an orthonormal basis) is orthogonally diagonalizable.

- Quadratic forms. Let Q(v) = ⟨T v, v⟩ be the quadratic form associated to T. Writing v = ∑ xi ei in the orthonormal eigenbasis, we get
  Q(v) = ∑ λi xi^2.
Thus a quadratic form reduces by an orthogonal change of variables to a sum of scaled squares. This immediately gives:
  * Q is positive definite ⇔ all eigenvalues λi > 0.
  * Q is positive semidefinite ⇔ all λi ≥ 0.
  * The numbers of positive, negative, and zero eigenvalues are intrinsic invariants of the quadratic form (they give the signature).

- Orthogonal decompositions by eigenspaces. Eigenspaces corresponding to distinct eigenvalues are orthogonal: if T u = λ u and T v = μ v with λ ≠ μ then
  (λ − μ)⟨u, v⟩ = ⟨T u, v⟩ − ⟨u, T v⟩ = 0,
so ⟨u, v⟩ = 0. Hence V decomposes as the orthogonal direct sum of the eigenspaces of T. In particular, projecting v onto an eigenspace is an orthogonal projection; one can express v uniquely as v = ∑ v_i where v_i lies in the eigenspace for λi.

- Practical uses.
  * To study a quadratic form Q, diagonalize the associated self‑adjoint operator and read off coefficients λi.
  * To solve optimization problems with a quadratic objective ⟨T v, v⟩ subject to ⟨v, v⟩ = 1, the extrema occur at eigenvectors; the maximum (resp. minimum) value is the largest (resp. smallest) eigenvalue.
  * For symmetric matrices A, find an orthogonal matrix P with P^T A P diagonal; this is the matrix version of the theorem.

Examples (illustrative).
  * If T is the orthogonal projection onto a subspace W, then eigenvalues are 1 (on W) and 0 (on W⊥); Q(v)=⟨T v, v⟩ = ||projection of v onto W||^2.
  * For a symmetric 2×2 matrix, the theorem guarantees an orthonormal eigenbasis, so every real quadratic form ax^2 + 2bxy + c y^2 can be written as λ1 X^2 + λ2 Y^2 by an orthogonal change of coordinates.

This completes the proof and shows how the real spectral theorem diagonalizes self‑adjoint operators and controls the behavior of associated quadratic forms and orthogonal decompositions.

Positive operators

Definition
- Let V be a finite-dimensional inner-product space (real or complex) and let T ∈ L(V). T is called positive (or positive semidefinite) if
  ⟨T v, v⟩ ≥ 0 for every v ∈ V.
- Notation: T ≥ 0 means T is positive. If, in addition, T is invertible (equivalently ⟨T v,v⟩ > 0 for all v ≠ 0), we say T is positive definite.

Relation with self-adjointness
- Every positive operator is self-adjoint. Proof: for any v ∈ V,
  ⟨(T − T*)v, v⟩ = ⟨T v, v⟩ − overline{⟨T v, v⟩} = 0,
  so ⟨(T − T*)v, v⟩ = 0 for all v. From polarization (or standard linear algebra arguments) this forces T − T* = 0, hence T = T*.
- Conversely, a self-adjoint operator T is positive iff all its eigenvalues are ≥ 0. Equivalently, by the spectral theorem (finite-dimensional), T is positive iff it has an orthonormal eigenbasis and every eigenvalue λ satisfies λ ≥ 0.

Existence and uniqueness of the positive square root
- Theorem (existence and uniqueness). If T ∈ L(V) is positive, then there exists a unique operator S ∈ L(V) such that
  (i) S is positive, and
  (ii) S^2 = T.
  We call S the positive square root of T and denote it by S = √T.
- Proof sketch (spectral construction). Diagonalize T by the spectral theorem: choose an orthonormal basis {e_j} of eigenvectors with T e_j = λ_j e_j, where each λ_j ≥ 0. Define S on that basis by S e_j = sqrt(λ_j) e_j. Then S is self-adjoint, positive, and S^2 e_j = (sqrt(λ_j))^2 e_j = λ_j e_j, so S^2 = T. Uniqueness: if R is any positive operator with R^2 = T, then R commutes with T and shares the same eigenvectors, so on each eigenspace of T the eigenvalues of R must be nonnegative square roots of the corresponding λ_j; positivity forces the choice sqrt(λ_j), so R = S.
- Note: the construction shows √T is obtained by applying the scalar function f(λ) = √λ to the spectrum of T.

Basic finite-dimensional functional-calculus consequences
- Spectral functional calculus (finite-dimensional). If T is self-adjoint with eigenpairs {λ_j, P_j} (P_j the orthogonal projection onto the λ_j-eigenspace), then for any function f defined on the finite set {λ_j} we define
  f(T) = Σ_j f(λ_j) P_j.
  In particular, √T = Σ_j √λ_j P_j.
- Polynomial representation. Because the spectrum of T is a finite set, there exists a polynomial p such that p(λ_j) = √λ_j for every eigenvalue λ_j (use Lagrange interpolation). Hence √T = p(T). Thus the positive square root is a polynomial in T.
- Commutation. If A ∈ L(V) commutes with T (AT = TA), then A commutes with √T. (Reason: A preserves the eigenspaces of T, so it commutes with each spectral projection P_j.)
- Positivity under congruence. For any linear C: V → V and any positive T, the operator C* T C is positive. In particular, if T ≥ 0 and M is invertible, then M* T M ≥ 0; if T > 0 then M* T M > 0.
- Invertibility and square roots. T is invertible and positive iff all eigenvalues λ_j > 0. In that case √T is invertible and (√T)^{-1} = √(T^{-1}).
- Operator monotonicity (finite-dimensional). If 0 ≤ S ≤ T (meaning T − S ≥ 0), then √S ≤ √T. In finite dimensions this follows from the spectral calculus and the fact that the function f(λ) = √λ is operator-monotone on [0, ∞).
- Positivity of polynomial/functional images. If T ≥ 0 and f is a real-valued function on the spectrum of T with f(λ) ≥ 0 for each eigenvalue λ, then f(T) ≥ 0. In particular, for any polynomial p with p(λ) ≥ 0 on the spectrum, p(T) ≥ 0.

Useful corollaries and remarks
- Every positive T has a unique positive nth root for any integer n ≥ 1 (take f(λ) = λ^{1/n} on the spectrum).
- If T ≥ 0 and U is unitary, then U* T U ≥ 0 and √(U* T U) = U* √T U.
- For finite-dimensional problems, spectral decomposition reduces many questions about positive operators to pointwise questions about nonnegative real numbers (their eigenvalues).

Unitary operators and isometries

Definition
- Let V be an inner-product space over F (R or C). A linear operator T: V → V is unitary if T* T = T T* = I. Equivalently T* = T^{-1}.
- A linear operator S: V → W (between inner-product spaces) is an isometry if it preserves norms: for all v in V, ||S v|| = ||v||. Equivalently, S* S = I on V (so S* S = I_V). An isometry need not be surjective; a unitary operator is a surjective isometry (invertible isometry).

Equivalent characterizations of unitary operators (finite- or infinite-dimensional)
- T is unitary ⇔ T* = T^{-1}.
- T is unitary ⇔ for all u, v in V, <T u, T v> = <u, v> (T preserves the inner product).
- T is unitary ⇔ for all v in V, ||T v|| = ||v|| (T preserves norms).
- T is unitary ⇔ T maps any orthonormal basis of V to another orthonormal basis of V.
These equivalences follow directly from the relations T* T = I and from the polarization identities linking inner product and norm.

Isometries vs unitaries (finite vs infinite dimension)
- If S: V → V satisfies S* S = I (an isometry on V), then S preserves norms and inner products. In finite-dimensional V, injectivity implies surjectivity, so S* S = I forces S S* = I as well and S is unitary. In infinite-dimensional spaces an isometry need not be surjective (examples: right-shift on l^2), so it may not be unitary.

Matrices, orthonormal bases, and geometry
- Fix an orthonormal basis of a finite-dimensional inner-product space V. The matrix [T] of a linear operator T relative to that basis satisfies [T]* [T] = I ⇔ T* T = I. Thus T is unitary ⇔ [T] is a unitary matrix (conjugate-transpose inverse). For real spaces the analogous notion is orthogonal: [T]^T [T] = I.
- Unitarians as geometric transformations: a unitary (or orthogonal) matrix represents a linear isometry of Euclidean/C^n geometry. Geometrically such maps preserve lengths and angles, so they are combinations of rotations and reflections (and, over C, additionally unitary phase multiplications on invariant subspaces). Examples: rotation matrices and reflection matrices are orthogonal/unitary; a complex diagonal matrix with unimodular diagonal entries is unitary (phase multipliers).

Key consequences and uses
- Unitary operators preserve orthonormal sets, orthogonal projections, and spectral structure related to normality. Because they preserve inner products, they are the natural notion of “distance- and angle-preserving” linear maps in inner-product spaces and provide coordinate changes that do not distort the inner-product geometry.

Polar decomposition

Statement. Let T be a linear operator on a finite-dimensional inner-product space V. Define P = (T* T)^{1/2}. Then P is positive (self-adjoint and positive semidefinite) and there exists a partial isometry U with initial space range(P) and final space range(T) such that
  T = U P.
Equivalently, defining Q = (T T*)^{1/2} one gets T = Q U' with U' a partial isometry from range(T*) to range(T). If T is invertible, U (or U') is unitary and the decomposition may be written T = U P (or T = P U), where U is unitary and P is the unique positive square root of T* T.

Construction. Set P = (T* T)^{1/2}. By properties of the functional calculus (or Theorem: positive operators have unique positive square roots), P is self-adjoint, positive semidefinite, and P^2 = T* T. Note that ker P = ker T (since T* T v = 0 iff T v = 0). On range(P) (which equals range(T*)), P is invertible. Define U on range(P) by
  U(Pv) = T v  for all v in V.
This is well defined: if Pv1 = Pv2 then P(v1 - v2) = 0 so v1 - v2 ∈ ker P = ker T, hence T v1 = T v2. The map U so defined preserves inner products on range(P):
  <U(Pv), U(Pw)> = <T v, T w> = <T* T v, w> = <P^2 v, w> = <P v, P w>,
so U is isometric on range(P). Extend U arbitrarily to a unitary operator on V (possible because the orthogonal complement of range(P) can be mapped isometrically onto the orthogonal complement of range(T)); if one prefers the partial-isometry version, regard U as defined only on range(P) with range equal to range(T). By construction,
  U P v = U(P v) = T v
for all v, so T = U P.

Using (T T*)^{1/2}. The same procedure applied to TT* gives Q = (T T*)^{1/2} and a partial isometry U' with initial space range(T*) and final space range(T) such that T = Q U'. When T is invertible, P and Q are both invertible and U = T P^{-1} = Q^{-1} T is unitary, so the two viewpoints are consistent and one may write T = U P = Q U.

Uniqueness. The positive factor P = (T* T)^{1/2} is unique: positive square roots of a positive operator are unique. The isometry U is uniquely determined on range(P) (equivalently on (ker T)^{⊥}) by the requirement U P = T. On ker P = ker T, U can be defined arbitrarily as a partial isometry into ker T⊥ to make U unitary on V; thus U is not unique in general. In the special case that T is invertible (so ker T = {0}), P is invertible and U = T P^{-1} is uniquely determined and unitary.

Summary of important facts
- P = (T* T)^{1/2} is the unique positive operator with P^2 = T* T.
- There exists a partial isometry U with initial space range(P) and final space range(T) such that T = U P.
- U is uniquely determined on range(P) and can be extended to a unitary on V; the extension is unique iff ker T = {0} (i.e., T is injective, equivalently invertible in finite dimensions).

Section 43 — Spectral Theorem on Complex Inner Product Spaces (Normal Operators)

Statement (Complex Spectral Theorem)
- Let V be a finite-dimensional complex inner product space and let T: V → V be a linear operator. T is normal (T*T = TT*) if and only if there exists an orthonormal basis of V consisting of eigenvectors of T. Equivalently, T is unitarily diagonalizable: there exists a unitary operator U and a diagonal matrix D (with complex entries) such that T = UDU* (in matrix language, U*TU = D).

Immediate consequences and equivalent characterizations
- Normal ⇔ unitarily diagonalizable. Thus normal operators behave like diagonal matrices in a suitably chosen orthonormal basis.
- The eigenvectors corresponding to distinct eigenvalues are orthogonal.
- T and T* have the same eigenvectors; the eigenvalue of T* corresponding to an eigenvector v is the complex conjugate of the eigenvalue of T for v.
- The spectral decomposition: if {v1,...,vn} is an orthonormal eigenbasis with Tvi = λivi, then for any vector x,
  x = Σ ⟨x, vi⟩ vi and T x = Σ λi ⟨x, vi⟩ vi.
- The operator norm and spectral radius coincide for normal operators: ||T|| = max |λi| where the λi are the eigenvalues. (In particular, the spectral norm is attained on an eigenvector.)

How to use the theorem (practical computations and structural analysis)
1. Diagonalize T by finding an orthonormal eigenbasis:
   - Compute eigenvalues λi of T.
   - For each eigenspace, choose an orthonormal basis (apply Gram–Schmidt if needed).
   - Collect these orthonormal eigenvectors to form a unitary matrix U with columns vi; then U*TU = diag(λ1,...,λn).
2. Compute powers and polynomials of T:
   - If p is a polynomial, p(T) is diagonal in the same basis: p(T)vi = p(λi)vi. So p(T) = U diag(p(λi)) U*.
   - In particular, T^k has eigenvalues λi^k and the same eigenvectors.
3. Compute matrix exponentials and other holomorphic functional calculus:
   - For analytic functions f, define f(T) = U diag(f(λi)) U*. Example: exp(T)vi = exp(λi)vi.
4. Norms, determinant, trace:
   - ||T|| = max_i |λi|.
   - det(T) = Π λi (with multiplicity).
   - trace(T) = Σ λi (with multiplicity).
5. Spectral projections and decomposition:
   - Let Eλ be orthogonal projection onto the eigenspace for λ. Then T = Σ λ Eλ, the sum over distinct eigenvalues. The Eλ are pairwise orthogonal and satisfy EλEμ = 0 (λ ≠ μ), Eλ* = Eλ, and Σ Eλ = I.
6. Commuting normal operators:
   - If T and S are normal and commute (TS = ST), then they are simultaneously unitarily diagonalizable: there exists an orthonormal basis of common eigenvectors. Thus one can diagonalize both operators by the same unitary and read off their joint action coordinatewise.

Applications and typical problem types
- Diagonalize a given normal matrix/operator: find a unitary U and diagonal D so that T = UDU*.
- Compute T^k, e^T, or p(T) efficiently using eigenvalues and eigenvectors.
- Show an operator is normal by demonstrating a unitary diagonalization (or conversely, show diagonalizability with an orthonormal eigenbasis implies normality).
- Decompose a vector into spectral components using the orthogonal projections Eλ and analyze how T acts on each component separately.
- Use the spectral theorem to prove properties that rely on orthogonality of eigenspaces (e.g., minimization problems, norm computations, stability analyses).

Sketch of why the theorem holds (key ideas)
- Existence: Over C, every operator has at least one eigenvalue. For a normal operator T, one can choose an eigenvector v for some eigenvalue λ and show v is orthogonal to (T − λI)-invariant complement; restricting T to that orthogonal complement gives another normal operator, and induction on dimension produces an orthonormal eigenbasis.
- Orthogonality: If T is normal and T v = λ v and T w = μ w with λ ≠ μ, then ⟨T v, w⟩ = λ ⟨v, w⟩ and ⟨v, T* w⟩ = μ̄ ⟨v, w⟩, but ⟨T v, w⟩ = ⟨v, T* w⟩, so (λ − μ̄)⟨v, w⟩ = 0; for distinct eigenvalues this forces ⟨v, w⟩ = 0.
- Necessity: If T has an orthonormal eigenbasis, then in that basis T is diagonal, and a diagonal matrix commutes with its conjugate transpose, so T is normal.

Warnings and remarks
- Over the real numbers the analogue requires symmetric (self-adjoint) operators for orthonormal diagonalization with real eigenvalues; normal real matrices need not be diagonalizable over R (they may require complex eigenvalues).
- Normality is strictly weaker than being self-adjoint (Hermitian): self-adjoint ⇒ normal, with the added property that eigenvalues are real. Unitary operators are normal with eigenvalues on the unit circle.
- Uniqueness: the eigenvalues and eigenspaces (and hence spectral projections) are intrinsic, but the choice of orthonormal basis within each eigenspace is not unique.

Quick examples
- Normal matrix with distinct eigenvalues: diagonalizable by a unique (up to phase) orthonormal eigenbasis.
- Projection P with P = P* = P^2 is normal; its eigenvalues are 0 and 1, and the spectral decomposition is P = 1·E1 + 0·E0 where E1 = P.
- Unitary U has eigenvalues of modulus 1; compute U^k by raising eigenvalues to k.

End of section.

Why Complex Scalars Matter (Contrasts with the Real Case)

Key point: several operator-structure results in Axler’s Chapter 8 use that the scalar field is algebraically closed (C). Over C every polynomial splits, so operators always have eigenvalues and can be put into the kinds of canonical/triangular forms those theorems assert. Over R that algebraic fact fails, and the corresponding structure theorems fail or must be weakened. Below are which results require complex scalars, what goes wrong over R, and simple counterexamples.

Which results require complex scalars
- Existence of an eigenvalue for every linear operator on a nonzero finite-dimensional space.
  - Reason: characteristic polynomial has a root because C is algebraically closed (Fundamental Theorem of Algebra).
- Triangularization (every operator is similar to an upper-triangular matrix).
  - Reason: build an eigenvector, reduce dimension, and proceed inductively; needs an eigenvalue at each step.
- Schur’s theorem (every operator on a complex inner product space has an upper-triangular matrix with respect to an orthonormal basis; in particular eigenvalues appear on the diagonal).
  - Builds on existence of eigenvectors and Gram–Schmidt; needs C.
- Jordan canonical form (full Jordan decomposition exists).
  - Requires splitting of the minimal/characteristic polynomial into linear factors.
- Full spectral classification of normal operators (normal ⇒ orthonormal basis of eigenvectors).
  - Over C, normal operators are diagonalizable by a unitary matrix. Over R this statement fails for all normal operators; it holds only for special classes (e.g., symmetric matrices).

Concrete contrasts and counterexamples over R
- A real operator with no real eigenvalue
  - Example: rotation by 90° on R^2, represented by
    [[0, -1],
     [1,  0]].
    Its characteristic polynomial is t^2 + 1, which has no real roots. So:
      - No real eigenvector ⇒ no real eigenvalue.
      - It cannot be put into an upper-triangular real matrix similar form (a triangular real 2×2 matrix would have its two diagonal entries equal to the real eigenvalues).
    Over C this same matrix has eigenvalues ±i and is triangularizable/diagonalizable.
- Triangularization can fail over R
  - Same rotation example: since there is no real eigenvalue, you cannot start the usual induction to produce a real triangular form. Over C you can.
- Schur/orthonormal-eigenbasis failure for real normal operators
  - The rotation matrix is orthogonal and normal, yet it has no real eigenvectors, so it cannot be diagonalized by a real orthogonal matrix. Thus the complex Schur/spectral conclusions do not carry over verbatim to R.
- Jordan form and irreducible factors
  - A real matrix whose characteristic polynomial contains an irreducible quadratic factor (like t^2+1) cannot be put into a real Jordan form consisting solely of 1×1 Jordan blocks. Over R such factors force 2×2 real blocks corresponding to complex conjugate eigenpairs; over C the polynomial splits and you get linear Jordan blocks.
- Minimal-polynomial arguments break
  - Many proofs that produce invariant subspaces of specific dimensions (e.g., cyclic subspace constructions, primary decomposition) rely on factoring polynomials into linear factors. Over R you can only factor into linear and irreducible quadratic factors, so you get a different canonical form (real canonical form with 2×2 blocks for complex conjugate pairs) rather than Jordan form.

Practical takeaway
- If you want the strongest structure theorems (every operator has an eigenvalue; every operator is triangularizable; Schur, Jordan, spectral theorem for normal operators in full generality), you need the scalar field to be algebraically closed — typically C.
- Over R you still have important positive results (e.g., every real symmetric matrix is diagonalizable by an orthogonal matrix), but you must expect 2×2 blocks for complex conjugate eigenpairs and cannot assume the existence of real eigenvectors in general.

Short checklist
- Requires C: existence-of-eigenvalue theorem; triangularization; Schur theorem; Jordan canonical form; full spectral theorem for normal operators.
- Over R: counterexamples come from rotations (t^2+1 factors), and generally from operators whose characteristic polynomials have irreducible real quadratic factors.

Polynomial functional calculus — definition and consequences

Definition
- For a polynomial p(z) = a0 + a1 z + ··· + an z^n and a linear operator T on a complex vector space V, define
  p(T) := a0 I + a1 T + ··· + an T^n.
  This is an operator on V obtained by substituting T for the variable z and I for the constant 1.

Basic algebraic properties
- Linearity: (αp + βq)(T) = α p(T) + β q(T) for scalars α, β and polynomials p, q.
- Multiplicativity: (pq)(T) = p(T) q(T). Proof: Expand both sides and use T^k T^ℓ = T^{k+ℓ}.
- If p(z) = (z − λ) q(z), then p(T) = (T − λ I) q(T). More generally, polynomial identities (factorizations, divisions) translate into the same operator identities after replacing z by T.

Consequences for eigenvalues and spectrum
- Eigenvalues: If v ≠ 0 and T v = λ v, then p(T) v = p(λ) v. Hence:
  - If p(λ) = 0 then every eigenvector for eigenvalue λ lies in ker p(T).
  - If p(T) = 0 (the zero operator), then every eigenvalue λ of T must be a root of p; equivalently, the spectrum σ(T) is contained in the set of zeros of p.
- Invertibility: If p(T) is invertible, then p(λ) ≠ 0 for every λ ∈ σ(T). Equivalently, σ(T) ⊆ {z : p(z) ≠ 0}.

Polynomial division and the minimal polynomial
- Let m be the minimal polynomial of T (the monic polynomial of least degree with m(T) = 0). For any polynomial p there exist unique q and r with deg r < deg m such that p = qm + r. Applying T gives p(T) = r(T), since m(T) = 0. Thus every polynomial in T is equal to some polynomial in T of degree < deg m.
- In particular, T satisfies its minimal polynomial, and σ(T) ⊆ {roots of m}. Conversely, every root of m is an eigenvalue, so the set of roots of m equals σ(T) (counted without algebraic multiplicity).

Invariant subspaces from polynomial factors
- If p = p1 p2 and p1 and p2 are relatively prime polynomials, then using the Bézout identity there exist a, b with a p1 + b p2 = 1. Applying T gives a(T) p1(T) + b(T) p2(T) = I, and from this one obtains the direct-sum decomposition
  V = ker p1(T) ⊕ ker p2(T).
  More generally, factorization of a polynomial into pairwise coprime factors yields a decomposition of V into invariant subspaces corresponding to those factors.
- Primary decomposition (spectral primary components): If the minimal polynomial factors as m(z) = ∏_{j=1}^k (z − λ_j)^{m_j} with distinct λ_j, then
  V = ⊕_{j=1}^k ker (T − λ_j I)^{m_j},
  and each summand is T-invariant. This follows by applying the previous coprime-factor decomposition to the relatively prime factors (z − λ_j)^{m_j}.

Spectral consequences of factor powers
- For each eigenvalue λ, the generalized eigenspace for λ equals ker (T − λ I)^{m_λ}, where m_λ is the exponent of (z − λ) in the minimal polynomial. All vectors in ker (T − λ I)^{m_λ} are annihilated by some power of (T − λ I), and the restriction of T − λ I to this space is nilpotent.
- The minimal polynomial is the least common multiple of the distinct polynomials (z − λ)^{m_λ} needed to annihilate each generalized eigenspace.

Practical uses
- To test whether an operator satisfies a polynomial identity, substitute T into the polynomial identity and use multiplicativity. For example, if p factors as ∏ (z − λ_j)^{k_j}, then p(T) factors as ∏ (T − λ_j I)^{k_j}; vanishing of p(T) yields annihilation relations (T − λ_j I)^{k_j} annihilate appropriate invariant subspaces.
- To compute functions of T that are polynomials (or reduce a polynomial in T), divide by the minimal polynomial to reduce degree.
- To decompose V into invariant subspaces tied to parts of the spectrum, factor the minimal polynomial and apply the coprime-factor decomposition to get primary components.

Sketch proofs of key points
- (pq)(T) = p(T) q(T): follows by expanding products and using T^a T^b = T^{a+b}.
- If p(T) = 0 then every eigenvalue λ satisfies p(λ) = 0: take eigenvector v, apply p(T) to get p(λ) v = 0, hence p(λ) = 0.
- Direct-sum decomposition for coprime factors: if gcd(p1, p2) = 1, find a, b with a p1 + b p2 = 1; apply T and show that each v decomposes uniquely as sum from the kernels of p1(T) and p2(T).

Summary (one-sentence)
- Replacing z by T in polynomial identities gives operator identities; using factorization and division of polynomials yields invariant decompositions (primary decomposition), relations among eigenvalues and generalized eigenspaces, and a practical method (via the minimal polynomial) to reduce polynomial expressions in T.

Minimal polynomial — existence, uniqueness, and basic consequences

Definition
- Let V be a finite-dimensional complex vector space and T ∈ L(V). A polynomial p ∈ C[z] is said to annihilate T if p(T) = 0 (the zero operator). The minimal polynomial m_T of T is the unique monic polynomial of least degree that annihilates T.

Existence
- Because V is finite-dimensional, the infinite list I, T, T^2, … is linearly dependent in L(V). Thus some nonzero polynomial q(z) = a_0 + a_1 z + ··· + a_n z^n satisfies q(T) = a_0 I + a_1 T + ··· + a_n T^n = 0. Hence there exists a nonzero annihilating polynomial, and therefore there is at least one nonzero polynomial of least degree among those annihilating T. Multiplying by a scalar we may take that least-degree polynomial to be monic. So m_T exists. Also deg m_T ≤ dim V because the dependence occurs among at most dim V + 1 operators.

Uniqueness and divisibility property
- Suppose m_T is a monic annihilating polynomial of minimal degree. Let p be any polynomial with p(T) = 0. Divide p by m_T with remainder: p = q m_T + r, with deg r < deg m_T. Then applying T gives 0 = p(T) = q(T) m_T(T) + r(T) = r(T). Minimality of deg m_T forces r = 0 (otherwise r would be a smaller-degree annihilating polynomial). Thus m_T divides p. In particular m_T is unique (there is only one monic polynomial generating the ideal of annihilating polynomials), and m_T is the monic generator of the ideal {p ∈ C[z] : p(T) = 0}.

Basic consequences

1) Eigenvalues and minimal polynomial
- λ ∈ C is an eigenvalue of T iff (z − λ) divides m_T.
  Proof: If λ is an eigenvalue, choose nonzero v with T v = λ v. Then (T − λ I) v = 0, so (z − λ) divides any annihilating polynomial (apply it to v), hence divides m_T. Conversely, if (z − λ) divides m_T, write m_T = (z − λ) q(z). Then 0 = m_T(T) = (T − λ I) q(T). So Range(q(T)) ⊆ ker(T − λ I). If q(T) ≠ 0 then ker(T − λ I) is nontrivial and λ is an eigenvalue. If q(T) = 0 then m_T would not be minimal (q would be a smaller-degree annihilating polynomial), contradiction. Thus λ is an eigenvalue.

2) Minimal polynomial and restrictions to invariant subspaces
- If U ⊆ V is T-invariant, then the minimal polynomial of T|_U divides m_T.
  Proof: Any p with p(T) = 0 also satisfies p(T|_U) = 0, so the minimal polynomial of T|_U divides every annihilating polynomial of T, in particular divides m_T.

3) Criterion for diagonalizability
- T is diagonalizable iff m_T splits as a product of distinct linear factors (i.e., m_T has no repeated roots).
  Proof:
  - If T is diagonalizable, there is a basis of eigenvectors and T is represented by a diagonal matrix with eigenvalues λ_1,…,λ_k (distinct eigenvalues among them). The minimal polynomial is then the product ∏_{i=1}^k (z − λ_i) (each eigenvalue appears to first power), so m_T has no repeated factors.
  - Conversely, assume m_T = ∏_{i=1}^k (z − λ_i) with distinct λ_i. For each i define p_i(z) = m_T(z)/(z − λ_i). The polynomials p_i are pairwise relatively prime (because the factors (z − λ_i) are distinct). By Bézout there exist polynomials a_i(z) with ∑ a_i(z) p_i(z) = 1. Applying this identity at T gives ∑ a_i(T) p_i(T) = I. But p_i(T) = ∏_{j ≠ i} (T − λ_j I), so Range(p_i(T)) ⊆ ker(T − λ_i I). Hence each v ∈ V can be written as v = ∑ a_i(T) p_i(T) v with a_i(T) p_i(T) v ∈ ker(T − λ_i I). Therefore V = ⊕_{i=1}^k ker(T − λ_i I), the direct sum of eigenspaces; that is, T is diagonalizable.

4) Relation with generalized eigenspaces / multiplicity
- In general, if m_T factors as ∏_{i} (z − λ_i)^{e_i} with e_i ≥ 1, then the exponent e_i is the size of the largest Jordan block for λ_i (equivalently, the index of nilpotency of (T − λ_i I) on the generalized eigenspace). In particular, m_T has no repeated factor for λ_i exactly when there are no nontrivial Jordan chains for λ_i beyond eigenvectors, which is the diagonalizable condition above.

5) Other useful facts
- deg m_T ≤ dim V.
- If V decomposes as an invariant direct sum V = U ⊕ W, then m_T = lcm(m_{T|_U}, m_{T|_W}).
- The characteristic polynomial χ_T is annihilating (Cayley–Hamilton), so m_T divides χ_T. Hence the spectral information in m_T is drawn from the spectrum given by χ_T but with exponents equal to the maximum sizes of Jordan blocks rather than algebraic multiplicities.

These properties make the minimal polynomial a compact algebraic invariant encoding the spectrum of T and the sizes of the nilpotent parts; it controls invariant subspaces, divisibility relations among annihilators, and provides the sharp criterion for diagonalizability.

Theorem (Triangularization over C).
Let V be a finite-dimensional vector space over C and T ∈ L(V). Then there exists a basis of V with respect to which the matrix of T is upper-triangular. Consequently, the eigenvalues of T appear on the diagonal of any such triangular matrix (counted with algebraic multiplicity), and several useful identities follow (determinant = product of diagonal entries, trace = sum of diagonal entries, T is invertible iff no diagonal entry is 0, etc.).

Proof.
We prove by induction on n = dim V.

Base (n = 1). Trivial: any 1×1 matrix is upper-triangular, and any nonzero vector is an eigenvector because the characteristic polynomial is linear over C.

Inductive step. Assume the statement holds for all complex vector spaces of dimension < n, and let dim V = n ≥ 2. Because the field is C, the characteristic polynomial of T has at least one root λ ∈ C, so T has an eigenvalue λ and a corresponding nonzero eigenvector v1 with T v1 = λ v1.

Extend v1 to a basis of V: pick vectors v2, …, vn so that B = (v1, v2, …, vn) is a basis. Let U = span{v1} and consider the quotient space V/U, which has dimension n − 1. The linear map T induces a linear operator T̄ on V/U by T̄(x + U) = T x + U. Because T maps U to U (Tv1 ∈ U), T̄ is well-defined. By the induction hypothesis, there exists a basis of V/U relative to which the matrix of T̄ is upper-triangular. Lift that basis back to V by choosing representatives w2, …, wn in V whose cosets form that basis of V/U; then (v1, w2, …, wn) is a basis of V and the matrix of T with respect to this basis has the form

[ λ  *  *  …  *
  0  *  *  …  *
  0  0  *  …  *
  ⋮  ⋮  ⋮  ⋱ ⋮
  0  0  0  …  * ]

that is, upper-triangular with λ in the (1,1)-entry and the lower-right (n−1)×(n−1) block upper-triangular by induction. Hence T has an upper-triangular matrix in some basis. □

Reading off eigenvalues and immediate consequences
- Diagonal entries are eigenvalues. If A is the matrix of T in an upper-triangular form, then for each diagonal entry aii the vector with 1 in the i-th coordinate and 0 elsewhere (in the chosen basis) yields (A − aii I) having a zero column at i, so aii is a root of the characteristic polynomial and hence an eigenvalue. Conversely, the characteristic polynomial equals the product ∏_{i=1}^n (t − aii) because the determinant of (tI − A) for an upper-triangular A is the product of the diagonal entries (t − aii). Thus the eigenvalues of T, counted with algebraic multiplicity, are exactly the diagonal entries of any upper-triangular matrix for T (in some order).

- Determinant and trace. From the triangular form,
  det T = product of diagonal entries = ∏ eigenvalues,
  tr T = sum of diagonal entries = sum of eigenvalues.
  In particular, T is invertible iff no diagonal entry (equivalently, no eigenvalue) is 0.

- Nilpotence. If T is nilpotent (T^k = 0 for some k), then every eigenvalue must be 0. Equivalently, in any triangular form all diagonal entries are 0; conversely, if all diagonal entries are 0 in some triangular form, then the characteristic polynomial is t^n, so T is nilpotent.

- Factorization of the characteristic polynomial. Triangularization shows directly that the characteristic polynomial of T factors completely over C as ∏_{i=1}^n (t − λ_i) where λ_i are the diagonal entries in a triangular form; this is another way to see that over C the characteristic polynomial always splits into linear factors.

Remarks (useful consequences and limitations)
- The theorem is sometimes stated as: every complex matrix is similar to an upper-triangular matrix. This is exactly the same statement in matrix language.
- Triangularization is weaker than diagonalization: not every operator is diagonalizable. Diagonalizability requires that a basis of eigenvectors exist (equivalently, that the geometric multiplicity of each eigenvalue equals its algebraic multiplicity).
- Simultaneous triangularization: a commuting family of operators on a complex finite-dimensional V can often be simultaneously triangularized (for instance, any commuting set of operators that is algebraically triangularizable can be triangularized together), but not every pair of operators can be simultaneously triangularized unless additional hypotheses hold.
- Schur’s Theorem gives a stronger form for inner-product spaces: every operator on a finite-dimensional complex inner-product space is unitarily similar to an upper-triangular matrix (i.e., triangularization can be achieved with a unitary change of basis).

This completes the section on triangularization over C and its immediate algebraic consequences.

Jordan-Type Structure (Generalized Eigenvectors and Jordan Blocks)

Definitions and basic idea
- For a linear operator T on a finite-dimensional complex vector space V and an eigenvalue λ, a generalized eigenvector of order k for λ is a vector v ≠ 0 with (T − λI)^k v = 0 for some k ≥ 1. Ordinary eigenvectors are the case k = 1.
- The generalized eigenspace for λ is the subspace
  Eλ = { v ∈ V : (T − λI)^m v = 0 for some m ≥ 1 } = ⋃_{m≥1} ker((T − λI)^m).
  For finite-dimensional V this stabilizes: Eλ = ker((T − λI)^s) for s large enough.
- On Eλ, the operator N = T − λI is nilpotent (some power N^s = 0). Understanding T on Eλ therefore reduces to understanding a nilpotent operator.

Generalized eigenvector chains and Jordan blocks
- A generalized eigenvector chain (or Jordan chain) of length r for λ is a sequence v1, v2, …, vr with
  (T − λI)v1 = 0, and (T − λI) v_{j+1} = v_j for j = 1, …, r−1.
  Thus v1 is an eigenvector, v2 is sent to v1 by (T − λI), etc. The top vector vr satisfies (T − λI)^r vr = 0 but (T − λI)^{r−1} vr ≠ 0.
- A direct-sum decomposition of Eλ into subspaces spanned by disjoint Jordan chains gives a block-diagonal form of T on Eλ. Each chain of length r corresponds to a Jordan block Jr(λ), the r×r matrix with λ on the diagonal, 1’s on the superdiagonal, and 0’s elsewhere:
  Jr(λ) = [ λ on diagonal, 1 on entries immediately above diagonal ].
- Choosing a basis consisting of the vectors of all chosen chains (arranged chain by chain) yields a matrix of T that is block-diagonal with Jordan blocks for each eigenvalue. Collecting blocks for all eigenvalues produces the Jordan-type (Jordan canonical) form.

How block sizes reflect algebraic and geometric multiplicity
- Algebraic multiplicity of λ: the multiplicity of (t−λ) as a factor of the characteristic polynomial. This equals the sum of the sizes (lengths) of all Jordan blocks corresponding to λ.
- Geometric multiplicity of λ: the dimension of ker(T − λI). This equals the number of Jordan blocks for λ (because each chain contributes exactly one independent eigenvector v1).
- Thus:
  sum of block sizes for λ = algebraic multiplicity,
  number of blocks for λ = geometric multiplicity.
  Consequently geometric multiplicity ≤ algebraic multiplicity, with equality exactly when all blocks are size 1 (i.e., T is diagonalizable at λ).

Relation to the minimal polynomial
- The minimal polynomial m_T(t) of T factors over C as ∏ (t − λ)^{s_λ}, where s_λ is the smallest exponent with (T − λI)^{s_λ} = 0 on Eλ. Each s_λ equals the size (length) of the largest Jordan block corresponding to λ.
- Equivalently, the minimal polynomial is the least common multiple of the minimal polynomials of the individual Jordan blocks; for a block of size r at eigenvalue λ the minimal polynomial factor contributed is (t − λ)^r. Hence s_λ = max{ sizes of Jordan blocks at λ }.
- Immediate consequences:
  - The operator is diagonalizable iff every s_λ = 1 (all Jordan blocks are 1×1), so the minimal polynomial has only simple roots.
  - Knowing the Jordan block sizes determines the minimal polynomial, and conversely the exponents s_λ determine the largest block sizes but not the full block partition.

Construction idea (how one finds chains)
- Work eigenvalue by eigenvalue. On Eλ consider the nilpotent operator N = T − λI.
- Build a basis by finding a basis of successive kernels:
  ker(N) ⊂ ker(N^2) ⊂ … ⊂ ker(N^s) = Eλ.
  Choose vectors in ker(N^k) that are not in ker(N^{k−1}) to serve as chain tops; repeatedly apply N to produce the lower chain vectors. This procedure produces chains whose lengths equal the largest k for which the chosen top lies in ker(N^k) \ ker(N^{k−1}).
- The multiplicities dim ker(N^k) encode the distribution of block sizes (one can recover block-counts from the sequence of dimensions by discrete differences).

Small illustrative example
- Suppose for λ we have algebraic multiplicity 5 and dim ker(T − λI) = 2 (geometric multiplicity 2). Possible Jordan block size partitions (summing to 5 with two parts) include 4+1, 3+2, or 3+1+1 is not allowed since that has three parts. Each partition gives a different nilpotent structure on Eλ. The minimal polynomial exponent s_λ is the size of the largest block: 4 for 4+1, 3 for 3+2.
- So knowing only algebraic and geometric multiplicities does not determine the full Jordan structure; the sizes of individual blocks (equivalently the sequence of dim ker(N^k)) are needed.

Key takeaways
- Generalized eigenvectors extend eigenvectors so that T decomposes into blocks (Jordan blocks) instead of necessarily diagonal form.
- The number of Jordan blocks for λ equals geometric multiplicity; the total sizes equal algebraic multiplicity; the largest size equals the exponent of (t − λ) in the minimal polynomial.
- The Jordan-type decomposition gives a precise, canonical description (up to block order) of the operator’s action on V over C.

Determinant criteria for invertibility and links to eigenvalues

Let V be a finite-dimensional vector space of dimension n over a field F, and let T ∈ L(V). We recall that det is the unique function from L(V) to F characterized (via any chosen ordered basis) as the determinant of the matrix of the operator; equivalently, it can be characterized abstractly as the scalar by which T multiplies any fixed nonzero alternating n-linear form. Using these properties we prove the standard determinant criteria for invertibility and relate det to eigenvalues and the characteristic polynomial.

1) det(T) = 0 if and only if T is not invertible.

- If T is invertible then T−1 exists, so using multiplicativity (proved below)
  det(I) = det(T T−1) = det(T) det(T−1).
  Since det(I) = 1, we get det(T) ≠ 0 and det(T−1) = det(T)^{-1}. Thus an invertible operator has nonzero determinant.

- Conversely, if T is not invertible then T has a nontrivial kernel. Let v ≠ 0 with T v = 0. Extend v to a basis v, v2, …, vn of V. The matrix of T with respect to this basis has the first column equal to the zero column, so its determinant is 0. Hence det(T) = 0. Therefore det(T) = 0 iff T is not invertible (equivalently, det(T) ≠ 0 iff T is invertible).

2) Multiplicativity: det(AB) = det(A) det(B) for A, B ∈ L(V).

Fix a nonzero alternating n-linear form ω on V (exists because dim V = n). For any S ∈ L(V) define the scalar det(S) by
  (S⋅ω)(v1,...,vn) := ω(S v1, ..., S vn) = det(S) ω(v1,...,vn).
The map S ↦ S⋅ω is again an alternating n-linear form, so it must be a scalar multiple of ω; that scalar is by definition det(S). Now for A, B ∈ L(V),
  (AB)⋅ω (v1,...,vn) = ω(AB v1, ..., AB vn)
                     = ω(A(B v1), ..., A(B vn))
                     = det(A) ω(B v1, ..., B vn)
                     = det(A) (B⋅ω)(v1,...,vn)
                     = det(A) det(B) ω(v1,...,vn).
Thus det(AB) = det(A) det(B). (This argument is coordinate-free; equivalently one may verify the same identity for matrix determinants.)

3) Determinant, characteristic polynomial, and eigenvalues.

The characteristic polynomial of T is defined by
  p_T(λ) = det(T − λ I).
This is a degree-n polynomial in λ with leading term (−1)^n λ^n. In particular the constant term p_T(0) equals det(T). Consequently:

- 0 is an eigenvalue of T ⇔ det(T) = 0. (Because 0 is an eigenvalue iff T − 0·I = T is singular ⇔ det(T) = 0.)

- Over an algebraically closed field (or working over an extension field where p_T splits), p_T factors as
  p_T(λ) = (λ1 − λ)(λ2 − λ)···(λn − λ)
where λ1, …, λn are the eigenvalues of T listed with algebraic multiplicity. Evaluating at λ = 0 gives
  det(T) = p_T(0) = (λ1)(λ2)···(λn),
so the determinant equals the product of the eigenvalues (counted with algebraic multiplicity).

Remarks:
- The product-of-eigenvalues statement requires working over a field in which the characteristic polynomial splits; it is nevertheless true in general if one allows eigenvalues in an algebraic closure.  
- The multiplicativity det(AB) immediately implies that similarity preserves determinant: if B = S^{-1} A S then det(B) = det(A). Hence det is a similarity invariant, consistent with its expression in terms of eigenvalues and the characteristic polynomial.

Section: Multilinear Maps

Definition.
Let V1, V2, ..., Vn and W be vector spaces over the same field F. A function
T : V1 × V2 × ... × Vn → W
is called multilinear (or n-linear) if T is linear in each argument separately: for each i (1 ≤ i ≤ n), for all vectors vj ∈ Vj (j ≠ i), and for all u, v ∈ Vi and scalar α ∈ F,
1) T(v1, ..., v_{i-1}, u + v, v_{i+1}, ..., v_n) = T(v1, ..., v_{i-1}, u, v_{i+1}, ..., v_n) + T(v1, ..., v_{i-1}, v, v_{i+1}, ..., v_n),
2) T(v1, ..., v_{i-1}, αu, v_{i+1}, ..., v_n) = α T(v1, ..., v_{i-1}, u, v_{i+1}, ..., v_n).

Notation: The space of all multilinear maps V1 × ... × Vn → W is denoted L(V1, ..., Vn; W).

Examples.
1) Linear maps as 1-linear maps. If n = 1, a multilinear map is just an ordinary linear map V1 → W.

2) Bilinear forms. If V1 = V2 = V and W = F, a bilinear map B: V × V → F is a bilinear form. Examples include the standard dot product on R^n and the bilinear form (x,y) ↦ x^T A y for a fixed matrix A.

3) Matrix multiplication (as bilinear in rows and columns). Fix sizes so that multiplication makes sense: treat multiplication (A, B) ↦ AB as bilinear in the entries over appropriate vector spaces of matrices.

4) Determinant as an n-linear alternating map. For V = F^n, the determinant det : V × ... × V → F (taking n column vectors) is multilinear in the n column arguments and alternating.

5) Product of linear functionals. If f ∈ V1* and g ∈ V2*, then T(v1, v2) = f(v1) g(v2) is a bilinear map V1 × V2 → F.

Basic consequences and proofs.

Proposition 1 (Additivity and homogeneity in each slot).
If T ∈ L(V1, ..., Vn; W), then for each fixed choice of all slots except the i-th, the map Vi → W obtained by varying the i-th slot is a linear map. Consequently, for fixed vectors in the other slots, T is additive and homogeneous in the i-th slot as in the definition.

Proof.
This is just a restatement of the definition: linearity in the i-th slot means the map Vi → W, u ↦ T(v1, ..., v_{i-1}, u, v_{i+1}, ..., v_n), satisfies additivity and homogeneity. □

Proposition 2 (Linearity under fixing variables).
Fix indices i1, ..., ik and fix vectors in those slots. If T ∈ L(V1, ..., Vn; W), then the partially applied map
T_fixed : (remaining product of Vj) → W
obtained by fixing v_{i1}, ..., v_{ik} is multilinear in the remaining slots.

Proof.
Fixing some slots replaces those arguments by constant vectors; the linearity conditions for the remaining slots are unaffected, so T_fixed remains linear in each unfixed slot. □

Proposition 3 (Multilinearity preserved by scalar multiplication and sums).
If T, S ∈ L(V1, ..., Vn; W) and α ∈ F, then T + S and α T are in L(V1, ..., Vn; W) (pointwise operations).

Proof.
Linearity in each slot is checked coordinatewise:
(T + S)(..., u + v, ...) = T(..., u + v, ...) + S(..., u + v, ...) = [T(..., u, ...) + T(..., v, ...)] + [S(..., u, ...) + S(..., v, ...)]
= (T + S)(..., u, ...) + (T + S)(..., v, ...),
and similarly for scalar multiplication. Thus closure under addition and scalar multiplication holds. □

Proposition 4 (Composition with linear maps — precomposition).
Let Ti : Ui → Vi be linear maps for i = 1,...,n, and let T ∈ L(V1, ..., Vn; W). Then the composition
S : U1 × ... × Un → W,  S(u1, ..., un) = T(T1(u1), ..., Tn(un))
is multilinear, i.e., S ∈ L(U1, ..., Un; W).

Proof.
Fix all slots except the i-th. For ui, ui' ∈ Ui and scalar α,
S(..., ui + ui', ...) = T(..., Ti(ui + ui'), ...) = T(..., Ti(ui) + Ti(ui'), ...) = T(..., Ti(ui), ...) + T(..., Ti(ui'), ...) = S(..., ui, ...) + S(..., ui', ...),
and similarly S(..., α ui, ...) = α S(..., ui, ...). Here we used linearity of Ti and linearity of T in the i-th slot. Hence S is multilinear. □

Proposition 5 (Composition with a linear map on the target — postcomposition).
If T ∈ L(V1, ..., Vn; W) and S : W → X is a linear map, then the composition S ◦ T : V1 × ... × Vn → X is multilinear.

Proof.
For a fixed i and for u, v ∈ Vi and scalar α,
(S ◦ T)(..., u + v, ...) = S(T(..., u + v, ...)) = S(T(..., u, ...) + T(..., v, ...)) = S(T(..., u, ...)) + S(T(..., v, ...)) = (S ◦ T)(..., u, ...) + (S ◦ T)(..., v, ...),
and likewise for scalar multiples, using linearity of S and T. □

Corollary (Pre- and postcomposition together).
If Ti : Ui → Vi are linear and S : W → X is linear, and T ∈ L(V1,...,Vn; W), then S ◦ T ◦ (T1 × ... × Tn) ∈ L(U1, ..., Un; X).

Remarks and useful observations.
- Multilinearity is weaker than full linearity on the product space V1 × ... × Vn: a map is multilinear iff it is linear in each coordinate separately, but not necessarily linear as a function of the entire product (unless one identifies the product with a direct sum and imposes additional structure).
- Fixing n − 1 inputs of an n-linear map yields a linear functional on the remaining space; doing this for each slot gives a family of linear maps parameterized by the choices of the other slots.
- The set L(V1, ..., Vn; W) is itself a vector space under pointwise operations (Proposition 3).
- Precomposing by linear maps allows us to “pull back” multilinear maps to other domain spaces; postcomposing by linear maps lets us “push forward” their values. These operations are the basic manipulations used throughout multilinear algebra.

Section: Alternating Multilinear Forms and the Determinant

Definitions and basic facts

- Let V be an n-dimensional vector space over a field F. An n-linear map φ : V^n → F is multilinear in each argument. We call φ alternating if φ(v1,...,vn) = 0 whenever two of the arguments are equal (equivalently, φ changes sign under any transposition of two arguments).

- If e = (e1,...,en) is an ordered basis of V, we say an alternating n-linear map φ is normalized on e if φ(e1,...,en) = 1.

The determinant as the unique alternating normalized n-linear form

Theorem (Existence and uniqueness of determinant). For a fixed ordered basis e = (e1,...,en) of V there exists a unique alternating n-linear map det_e : V^n → F such that det_e(e1,...,en) = 1. We call det_e the determinant (relative to the ordered basis e). When a linear operator T : V → V is represented by an n×n matrix [T]_e in the basis e, the scalar det_e(T(e1),...,T(en)) is the determinant of that matrix; we often write det[T]_e or simply det(T) when the basis is understood.

Proof (uniqueness). Let φ be any alternating n-linear map with φ(e1,...,en) = 1. Any n-tuple (v1,...,vn) of vectors can be written, for each j, vj = sum_{i=1}^n a_{ij} e_i. By multilinearity,
φ(v1,...,vn) = φ( sum_i a_{i1} e_i, ..., sum_i a_{in} e_i )
= sum_{i1,...,in} (a_{i1,1} ... a_{in,n}) φ(e_{i1},...,e_{in}).

Because φ is alternating, φ(e_{i1},...,e_{in}) vanishes whenever indices i1,...,in are not a permutation of 1,...,n, and for a permutation σ ∈ S_n,
φ(e_{σ(1)},...,e_{σ(n)}) = sign(σ) φ(e1,...,en) = sign(σ).
Thus φ is determined uniquely on all n-tuples by the scalars a_{ij} and the signs of permutations. Hence at most one alternating n-linear form is normalized on e.

Proof (existence — explicit formula). Define det_e by the permutation formula: for vj = sum_i a_{ij} e_i,
det_e(v1,...,vn) := sum_{σ∈S_n} sign(σ) ∏_{j=1}^n a_{σ(j),j}.
Multilinearity in each column and alternation (vanishing when two columns equal) are immediate from this formula, and det_e(e1,...,en) = 1 because only the identity permutation contributes 1. Thus det_e exists.

Notes: In matrix terms, if A = (a_{ij}) is the matrix whose j-th column gives coordinates of vj in the basis e, then the above sum is the usual permutation expansion det(A).

Consequences and standard determinant identities

1) Determinant of identity: det_e(e1,...,en) = 1, hence det(I) = 1.

2) Alternating implies zero on dependent lists: If v1,...,vn are linearly dependent, then det_e(v1,...,vn) = 0. Proof: if one vector is a linear combination of the others then the multilinearity and alternation give zero; equivalently, two columns can be made equal by a linear dependence and alternating forms vanish when two arguments are equal.

3) Effect of swapping two columns (or rows): For any alternating φ, swapping two arguments multiplies the value by −1. Hence for the determinant, interchanging two columns of a matrix negates the determinant.

4) Adding a multiple of one column to another leaves determinant unchanged: multilinearity in the affected column together with alternation gives invariance under column replacement v_j ↦ v_j + c v_k (with k ≠ j).

5) Scaling a column scales determinant: If one column v_j is multiplied by λ ∈ F then det is multiplied by λ (multilinearity). In particular, multiplying an entire matrix by scalar λ multiplies determinant by λ^n.

6) Determinant of a triangular matrix: If A is upper (or lower) triangular with diagonal entries d1,...,dn (in the chosen basis), then det(A) = d1 d2 ... dn. Proof: expand the permutation sum — only the identity permutation contributes a nonzero product because any nonidentity permutation picks some off-diagonal zero, so the product vanishes.

7) Determinant characteristic of invertibility: A linear operator T is invertible iff det_e(T(e1),...,T(en)) ≠ 0. Proof: If T is not injective the images of the basis are linearly dependent, so determinant is 0 by (2). Conversely, if det = 0 then the columns (images of the basis) are dependent, so T is not injective and hence not invertible.

8) Multiplicativity: If S, T : V → V are linear, then det_e(S∘T) = det_e(S) det_e(T). Proof: Fix an ordered basis e and let v_j = T(e_j). Then
det_e(S∘T(e1),...,S∘T(en)) = det_e(S(v1),...,S(vn)).
By multilinearity and alternation, the map ψ(w1,...,wn) := det_e(S(w1),...,S(wn)) is an alternating n-linear form on V. By uniqueness (any alternating normalized form is a scalar multiple of det_e), ψ = c · det_e for some scalar c. Evaluating at the basis e gives c = det_e(S(e1),...,S(en)) = det_e(S). Hence det_e(S∘T) = det_e(S) det_e(T). In matrix language this is det(ST) = det(S) det(T).

9) Determinant of transpose: For a matrix A, det(A^T) = det(A). This follows directly from the permutation formula (the product ∏_{j} a_{σ(j),j} is unchanged when indices are switched) or from multiplicativity plus the fact transposition permutes rows and columns an even number of times depending on parity, yielding equality.

10) Behavior under row operations (matrix viewpoint):
- Swapping two rows multiplies determinant by −1.
- Adding a multiple of one row to another leaves determinant unchanged.
- Multiplying a row by λ multiplies determinant by λ.
These follow from the corresponding column statements (apply to A^T if needed) and from multilinearity/alternation.

11) Determinant via columns or rows: The determinant is multilinear in the columns and alternating; equally it is multilinear and alternating in the rows. This gives the usual expansion along a row or column and Laplace expansions (derived by repeated multilinearity and alternation).

Remarks about linear operators vs. matrices

- The determinant det_e(T) depends on the choice of ordered basis e in the sense that if e' is another ordered basis then det_{e'}(T) = det(P)^{-1} det_e(T) det(P)??? (More precisely, if P is the change-of-basis matrix from e to e', then the matrix of T in the two bases are related by similarity, and det is similarity invariant so det does not depend on basis when viewed as a scalar attached to the linear operator.) Concretely, if A and B are matrix representations of the same linear operator in possibly different bases, they have the same determinant. Thus determinant can be seen both as a function on n-tuples of vectors (alternating n-linear form) and as a scalar invariant of linear operators.

Summary of the core logical structure

- Alternation + n-linearity forces any alternating normalized form to be exactly the permutation expansion formula; this gives existence and uniqueness of the determinant relative to a chosen ordered basis.
- With that characterization, the standard determinant identities (zero on dependent columns, scaling, sign under swaps, invariance under column-addition, multiplicativity, triangular product, transpose equality, and invertibility criterion) follow immediately from multilinearity and alternation.

Section: Determinant Properties and Computation

1. Basic computational rules for row/column operations
- Let A be an n×n matrix. Elementary row (or column) operations affect det(A) as follows:
  1. Swapping two rows multiplies the determinant by −1.
     Proof sketch: Swapping two rows reverses sign of any alternating multilinear function of the rows, so det is multiplied by −1.
  2. Multiplying a row by scalar c multiplies the determinant by c.
     Proof sketch: Determinant is multilinear in each row, so scaling one row scales det by the same factor.
  3. Adding a scalar multiple of one row to another row leaves the determinant unchanged.
     Proof sketch: Multilinearity plus alternation: treat the target row as (row + c·other row); the contribution from c·other row is zero because two rows become equal, so det is unchanged.

- The same statements hold for column operations (because det(A) can be defined equally in terms of columns).

These rules allow practical computation of det(A) by row-reduction to a triangular form, keeping track of the scalars and sign changes from swaps.

2. Triangular and diagonal matrices
- If A is upper (or lower) triangular, then det(A) is the product of the diagonal entries:
  det(A) = a11 · a22 · … · ann.
  Proof: Consider the expansion of det as a multilinear alternating function. For a triangular matrix every permutation contributing a nonzero term must pick diagonal entries (off-diagonal choices make a zero factor). Only the identity permutation contributes, giving the product of diagonal entries.
- If A is diagonal, the same formula applies.

This yields a fast way to compute determinants: row-reduce to triangular form using elementary operations and adjust determinant according to the rules above; then multiply the diagonal entries.

3. Expansion (Laplace expansion) and cofactors
- For fixed i (row) or j (column), the determinant can be expanded along that row or column:
  det(A) = sum_{k=1}^n (-1)^{i+k} a_{i,k} det(A_{i,k})
  det(A) = sum_{k=1}^n (-1)^{k+j} a_{k,j} det(A_{k,j})
  where A_{i,k} denotes the (n−1)×(n−1) submatrix obtained by deleting row i and column k.
  Proof idea: Use multilinearity and alternation. Fix the chosen row as a linear combination of standard basis vectors to isolate each term; signs come from the permutation parity after moving the chosen column to its position.

- Cofactor matrix and adjugate:
  Define the cofactor C_{i,j} = (-1)^{i+j} det(A_{i,j}). The adjugate (adjoint) matrix adj(A) is the transpose of cofactor matrix: adj(A)_{j,i} = C_{i,j}.
  Key identity: A · adj(A) = adj(A) · A = det(A) I.
  Proof sketch: Expand the matrix product entrywise using Laplace expansion: the (i,j)-entry of A·adj(A) equals sum_k a_{i,k} C_{j,k}, which equals 0 if i ≠ j (two equal rows in the expanded determinant) and equals det(A) if i = j (Laplace expansion of det(A) along row i). This gives the identity. Consequences: if det(A) ≠ 0 then A^{-1} = (1/det(A)) adj(A).

4. Multiplicativity: det(AB) = det(A) det(B)
- Statement: For n×n matrices A and B over a field, det(AB) = det(A) det(B).
- Proof (conceptual via columns and multilinearity):
  Let B have columns b1, …, bn. For fixed B, define the function f on n×n matrices by f(X) = det(XB). View f as a function of the columns of X. For each column index j, the j-th column of XB is X times b_j, which is a linear combination of the columns of X. Hence f is multilinear in the columns of X and alternating (if two columns of X are equal, two columns of XB are equal, so f=0). Therefore f is an alternating multilinear function of the columns of X. The determinant det(X) is (up to scalar) the unique such function normalized by det(I)=1; evaluating at X = I gives f(I) = det(B). Thus f(X) = det(B) det(X) for all X. Taking X = A gives det(AB) = det(A) det(B).

- Corollaries:
  1. det(I) = 1.
  2. det(A^T) = det(A) (since det(A^T) is alternating multilinear in rows iff det(A) is in columns; also det(AB)=det(BA) implies symmetry).
  3. det(cA) = c^n det(A) for scalar c (apply multiplicativity to cI and A: det(cI · A) = det(cI) det(A); but det(cI)=c^n).
  4. A is invertible iff det(A) ≠ 0. If invertible, det(A^{-1}) = 1/det(A).

5. Other useful identities
- det(A^{-1}) = 1/det(A) when det(A) ≠ 0 (from multiplicativity: det(A)det(A^{-1}) = det(I) = 1).
- det(A^k) = det(A)^k for integer k ≥ 0 (by induction using multiplicativity).
- If A is similar to B (B = P^{-1} A P), then det(B) = det(A) (since det(P^{-1} A P) = det(P^{-1}) det(A) det(P) = det(A)).
- Eigenvalue product: over an algebraically closed field, the determinant equals the product of eigenvalues counted with algebraic multiplicity. Reason: characteristic polynomial has constant term (−1)^n det(A), and eigenvalues are its roots.

6. Practical computation algorithm
- To compute det(A) numerically or by hand:
  1. Use elementary row operations to reduce A to an upper triangular matrix U.
  2. Track:
     - Each row swap multiplies det by −1.
     - Scaling a row by c multiplies det by c (if you scale to avoid fractions, account for factor).
     - Adding a multiple of one row to another does not change det.
  3. Once U is triangular, det(A) = (product of diagonal entries of U) multiplied by the accumulated scalar factor from tracked operations.
- Alternatively, perform LU decomposition A = P L U (with permutation matrix P). Then det(A) = det(P) det(L) det(U) = (±1)(1)(product of diagonal entries of U), since det(L)=1 when L has 1’s on its diagonal.

7. Example identities useful in proofs and computations
- If A has two equal rows (or columns) then det(A) = 0 (by alternation).
- Adding a multiple of one row to another can be used to introduce zeros below a pivot (Gaussian elimination) without changing det, enabling triangularization for determinant computation.
- Determinant of block-triangular matrix:
  If A = [B C; 0 D] with square blocks B and D on the diagonal, then det(A) = det(B) det(D). Proof: expand along the block structure or use triangular diagonal argument.

This collection of tools—row/column operation rules, triangular/diagonal formulas, Laplace expansion and adjugate identity, multiplicativity and its corollaries—gives both theoretical relations between determinants and linear maps/matrices and practical methods for computing determinants.

Exterior algebra and the wedge product (intro)

Goal. Build a linear algebraic setting that captures multilinear alternating behavior (sign changes when you swap arguments) and use it to view determinants as a linear action on a one-dimensional top exterior power.

1. Alternating multilinear maps
- An n-linear map f: V^k -> W (over field F) is alternating if f(v1,...,vk)=0 whenever two arguments are equal. Equivalently, swapping two arguments reverses sign: for any i≠j,
  f(..., vi, ..., vj, ...) = − f(..., vj, ..., vi, ...).
- Alternating maps vanish on any k-tuple that is linearly dependent (in particular if two entries agree). This is the key property that motivates quotienting the tensor algebra to enforce alternating relations.

2. Construction of the exterior power Λ^k V
- Start with the tensor power V^{⊗ k}. Impose the relations that swapping two tensor factors negates the tensor (so v⊗w = − w⊗v) and, in particular, v⊗v = 0. Formally factor V^{⊗ k} by the subspace generated by all tensors that become zero under these alternating relations. The resulting quotient space is denoted Λ^k V, the k-th exterior power of V.
- Elements of Λ^k V are equivalence classes typically written as v1 ∧ v2 ∧ ... ∧ vk (the wedge product of vectors). The wedge is multilinear in each slot and alternating: exchanging vi and vj introduces a sign (−1)^{swap parity}.
- Basic properties:
  - Multilinearity: (a v + b v') ∧ ... = a (v ∧ ...) + b (v' ∧ ...).
  - Alternation: if two factors are equal then the wedge is 0.
  - Anticommutativity for 1-vectors: u ∧ v = − v ∧ u. More generally, for α in Λ^p V and β in Λ^q V one has α ∧ β = (−1)^{pq} β ∧ α (graded-commutativity).
  - If {e1,...,en} is a basis of V, then the set {ei1 ∧ ... ∧ eik : 1 ≤ i1 < ... < ik ≤ n} is a basis of Λ^k V. In particular dim Λ^k V = C(n,k) for finite n.

3. Universal property and factorization of alternating maps
- Universal property: The wedge map w: V^k -> Λ^k V, w(v1,...,vk) = v1 ∧ ... ∧ vk, is alternating and multilinear, and it is universal for alternating multilinear maps from V^k. Concretely:
  For any vector space W and any alternating k-linear map f: V^k -> W, there exists a unique linear map F: Λ^k V -> W such that f = F ∘ w (i.e. f(v1,...,vk) = F(v1 ∧ ... ∧ vk)).
- Consequence: alternating k-linear structure on V is equivalent to linear structure on Λ^k V. This is what it means to say alternating multilinear maps "factor through" the exterior power.

4. Wedge product between exterior powers
- The wedge product extends to maps Λ^p V × Λ^q V -> Λ^{p+q} V, bilinear, associative, and alternating in the graded sense, given on pure wedges by
  (v1 ∧ ... ∧ vp) ∧ (w1 ∧ ... ∧ wq) = v1 ∧ ... ∧ vp ∧ w1 ∧ ... ∧ wq.
- This makes Λ^* V = ⊕_{k≥0} Λ^k V into an associative graded algebra, the exterior algebra.

5. Connection to determinants
- Let V be n-dimensional. Then Λ^n V is one-dimensional (dim = C(n,n) = 1). Choose a basis e1,...,en of V; then e1 ∧ ... ∧ en spans Λ^n V.
- Any linear operator T: V -> V induces a linear map Λ^n T: Λ^n V -> Λ^n V defined on pure wedges by
  Λ^n T (v1 ∧ ... ∧ vn) = T(v1) ∧ ... ∧ T(vn).
  This is well-defined and linear because T is linear and wedge is multilinear and alternating.
- Since Λ^n V is one-dimensional, Λ^n T acts by scalar multiplication: there is a scalar λ such that Λ^n T( e1 ∧ ... ∧ en ) = λ ( e1 ∧ ... ∧ en ). That scalar λ is exactly det(T).
- Thus determinant can be characterized invariantly: det(T) is the scalar by which T acts on the top exterior power Λ^n V. This viewpoint makes properties of the determinant transparent:
  - Multiplicativity: Λ^n(ST) = Λ^n S ∘ Λ^n T so det(ST) = det(S) det(T).
  - Change-of-basis sign and invariance come from how basis wedges transform.
  - T is invertible iff det(T) ≠ 0, because invertibility corresponds to Λ^n T being nonzero on the one-dimensional top exterior power.

6. Useful consequences and intuitions
- v1 ∧ ... ∧ vk = 0 in Λ^k V iff the vectors v1,...,vk are linearly dependent. So nonzero pure wedges represent k-dimensional oriented volume elements.
- The exterior algebra encodes oriented volumes and oriented subspaces: a nonzero element of Λ^k V represents a k-dimensional subspace with an orientation (up to scalar).
- Determinant is the scaling factor on oriented n-volumes under T.

Summary (one sentence). The exterior power Λ^k V is the universal recipient of alternating k-linear maps: any such map factors uniquely through the wedge V^k -> Λ^k V, and for k = n the induced action of a linear operator on Λ^n V is multiplication by its determinant, giving a coordinate-free interpretation of det(T).

Volume / orientation interpretation of the determinant

What the determinant measures
- For a linear map T: V → V on an n-dimensional real inner-product space, think of the determinant as the factor by which T scales n-dimensional volume, together with a sign that records whether T preserves or reverses orientation.
- Precisely: if E is any measurable n-dimensional region, then Vol(T(E)) = |det T| · Vol(E). The sign of det T is + when T preserves orientation and − when it reverses orientation, so det T itself is the oriented volume-scaling factor.

Geometric consequences
- Orientation reversal vs. preservation: det T > 0 means T preserves orientation (the orientation assigned to bases is the same after applying T). det T < 0 means T reverses orientation (the image of an oriented basis has the opposite orientation).
- Absolute value as volume scale: the factor |det T| is the ordinary (unsigned) volume-scaling factor. If |det T| = 2, volumes double; if |det T| = 0.5, volumes halve. If |det T| = 0, T collapses some dimension and sends every n-volume to zero.
- Invertibility: T is invertible exactly when det T ≠ 0. Geometrically det T = 0 means T collapses the n-dimensional space into a lower-dimensional subset, so no volume-preserving inverse exists.
- Composition: if S and T are linear maps, then the oriented volume change of S∘T is the product of the oriented volume changes: det(S∘T) = det S · det T. Geometrically apply T (scale by det T), then S (scale by det S) so total scale is the product.
- Reflections and rotations: an orthogonal transformation that preserves orientation (rotation) has det = +1 (volumes preserved, orientation preserved). A reflection has det = −1 (volumes preserved but orientation reversed).
- Scalar scaling: multiplying every vector by a scalar λ scales n-volumes by λ^n, so det(λ I) = λ^n.

How this viewpoint recovers algebraic properties
- Multiplicativity (det of a product): from volumes: applying T then S multiplies their volume factors, so det(S∘T) = det S · det T. This geometric argument gives the algebraic multiplicativity property without coordinate computation.
- Zero determinant characterizes linear dependence: if the images of an ordered basis are linearly dependent, the parallelepiped they span has zero volume, so det = 0. Conversely, nonzero det means images form a basis, so T is injective and hence invertible.
- Alternating/multilinear origin of sign: the determinant is an alternating multilinear function of the columns (or images of basis vectors). Geometrically, swapping two basis vectors reverses orientation of the spanned parallelepiped, so the sign of det flips. The alternating property encodes precisely the orientation information.
- Basis-independence and change of coordinates: the volume interpretation is intrinsic; choosing different bases changes coordinates but the oriented volume-scaling factor for T is the same. Algebraically this is the statement that det is well defined independent of basis and that det of the matrix of T changes by conjugation factors that cancel.
- Transpose and determinant: volume is unaffected by the particular inner-product duality used to represent linear maps as matrices, so det(T) = det(T^T) in coordinates; geometrically transpose corresponds to the same oriented volume factor.
- Determinant of a diagonal (or triangular) matrix: diagonal scaling by λ1,...,λn multiplies each coordinate direction's length independently, so volume scales by the product ∏ λi — recovering the algebraic formula det = product of diagonal entries for diagonal matrices.

Short examples to fix ideas
- 2×2 rotation by θ: matrix [[cosθ, −sinθ],[sinθ, cosθ]] has det = 1 (orientation preserved, area preserved).
- Reflection across x-axis: matrix [[1,0],[0,−1]] has det = −1 (area preserved, orientation reversed).
- Scaling by 3 in R^3 uniformly: det = 3^3 = 27 (volumes scaled by 27).
- Projection onto a plane in R^3: det = 0 (3-volumes collapse to zero).

Takeaway
- The determinant is the oriented n-volume-scaling factor of a linear map. Many algebraic properties of the determinant become transparent when understood geometrically: product rule from successive scaling, zero determinant from volume collapse, sign from orientation change, and the product formula for diagonal/triangular matrices from independent scaling in coordinate directions.