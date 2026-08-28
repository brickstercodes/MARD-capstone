Fields and Scalars (Underlying Number System)

- Definition and choice of field:
  - Every vector space is defined relative to a field F (most commonly F = ℝ or F = ℂ). The field supplies the scalars used in scalar multiplication and the arithmetic rules they obey.
  - When we say “V is a vector space,” we always mean “V is a vector space over a specified field F.” Always state the field (e.g., “V is a real vector space” or “a complex vector space”).

- How scalars act (scalar multiplication):
  - Scalar multiplication is a map F × V → V, written (a, v) ↦ a v, satisfying the axioms:
    1. a(u + v) = a u + a v for all a ∈ F and u, v ∈ V (distributivity over vector addition).
    2. (a + b) v = a v + b v for all a, b ∈ F and v ∈ V (distributivity over scalar addition).
    3. (ab) v = a (b v) for all a, b ∈ F and v ∈ V (compatibility with field multiplication).
    4. 1 v = v, where 1 is the multiplicative identity in F.
  - These properties guarantee that scalars “scale” vectors in a way consistent with the field’s arithmetic.

- Effect of changing the field:
  - Changing the field changes what maps count as scalar multiplication and thus can change whether a given set with operations is a vector space.
  - Example: R^2 is naturally a vector space over ℝ. It can also be viewed as a vector space over ℂ only if you define a compatible scalar multiplication by complex numbers; the standard structure of R^2 does not make it a complex vector space because multiplication by i would need to be a linear map R^2 → R^2 that squares to −I (which is not available without additional structure). Conversely, ℂ considered as a vector space over ℝ has dimension 2; over ℂ its dimension is 1.
  - In general, if V is a vector space over a field F and K is a subfield of F, then V is also a vector space over K by restricting scalars. If K is larger than F, V need not be a vector space over K unless you extend the scalar action appropriately (this process is called scalar extension or complexification when K = ℂ).

- Practical note:
  - Always keep the underlying field in mind: it affects linear independence, span, bases, dimension, and which linear maps are F-linear (i.e., respect scalar multiplication by elements of F).

Definition (Vector space over a field F)
A vector space V over a field F is a nonempty set equipped with two operations:
- addition: V × V → V, written u + v,
- scalar multiplication: F × V → V, written a v,
such that for all u, v, w ∈ V and all scalars a, b ∈ F the following axioms hold.

Axioms for addition
1. Commutativity: u + v = v + u.
2. Associativity: (u + v) + w = u + (v + w).
3. Additive identity: There exists an element 0 ∈ V with 0 + v = v for all v ∈ V.
4. Additive inverses: For every v ∈ V there exists an element −v ∈ V with v + (−v) = 0.

Axioms for scalar multiplication
5. Compatibility with field multiplication: (ab) v = a (b v).
6. Identity scalar: 1 v = v, where 1 is the multiplicative identity in F.
7. Distributivity over vector addition: a (u + v) = a u + a v.
8. Distributivity over field addition: (a + b) v = a v + b v.

(Closure under the two operations is usually assumed by stating the operations map into V as above.)

How to verify a given set with operations is a vector space
1. Verify the set is nonempty.
2. Check closure:
   - For any u, v in the set, ensure u + v (as defined) is also in the set.
   - For any scalar a in F and v in the set, ensure a v (as defined) is also in the set.
3. Verify the four addition axioms (commutativity, associativity, existence of a neutral element 0, and existence of additive inverses). Often you must identify the candidate 0 and show it satisfies 0 + v = v and is unique; show for each v there is a unique −v.
4. Verify the four scalar-multiplication axioms (compatibility with field multiplication, identity scalar, and the two distributivity laws).
5. If all eight axioms hold, the structure is a vector space over F.

Practical tips and common checks
- Show 0 ∈ V explicitly and check uniqueness of 0 and of additive inverses (though uniqueness follows from the axioms).
- To show associativity or distributivity, use the definitions of the operations and algebraic manipulation inside the set (for example, for function spaces check pointwise definitions).
- If an operation depends on extra structure (e.g., multiplication defined coordinatewise, or a weird scalar action), test the axioms that often fail: 1·v = v or (ab)v = a(bv) fail frequently for ad hoc scalar actions.
- When disproving a vector-space claim, it suffices to find one axiom that fails (common failures: no additive identity, additive inverses absent, scalar identity 1 acting incorrectly, or lack of closure).
- Use elementary consequences of the axioms when helpful (all can be proved from the axioms): 0·v = 0, a·0 = 0, (−1)v = −v, uniqueness of 0 and of −v.

Examples to exercise on (apply the checklist):
- R^n with coordinatewise operations (verify quickly; all axioms hold).
- Set of polynomials with usual addition and scalar multiplication.
- Non-example: natural numbers N with usual addition and scalar multiplication by real numbers (fails additive inverses and closure).
- Non-example: R^2 with addition as usual but scalar multiplication defined by a·(x,y) = (ax,0) (check 1·v = v or distributivity to find failure).

Canonical examples of vector spaces

1) F^n (n-tuples)
- Vectors: n-tuples (v1, v2, ..., vn) with each vi in the field F.
- Scalars: elements of the field F.
- Vector addition: (v1,...,vn) + (w1,...,wn) = (v1+w1, ..., vn+wn).
- Scalar multiplication: a·(v1,...,vn) = (a v1, ..., a vn) for a in F.
- Zero vector: (0,0,...,0) where 0 is the additive identity in F.

2) The space of m×n matrices, F^{m×n}
- Vectors: m×n matrices whose entries are in F.
- Scalars: elements of F.
- Vector addition: entrywise: (A + B)_{ij} = A_{ij} + B_{ij}.
- Scalar multiplication: (aA)_{ij} = a·A_{ij}.
- Zero vector: the m×n zero matrix (all entries 0).

3) Sequence spaces (F^∞ or sequences indexed by ℕ)
- Vectors: sequences (v1, v2, v3, ...) with each vi in F.
- Scalars: elements of F.
- Vector addition: (v + w)_i = v_i + w_i (termwise).
- Scalar multiplication: (a v)_i = a·v_i.
- Zero vector: the sequence (0,0,0,...).

4) Function spaces F^S (all functions from a set S to F)
- Vectors: functions f: S → F.
- Scalars: elements of F.
- Vector addition: (f + g)(s) = f(s) + g(s) for each s in S.
- Scalar multiplication: (a f)(s) = a·f(s).
- Zero vector: the zero function 0(s) = 0 for all s in S.
- Important special cases: real-valued functions on an interval, continuous functions, etc., obtained by restricting S and/or allowed functions (see next).

5) C([a,b], F) — continuous functions on [a,b] (a subspace of F^{[a,b]})
- Vectors: continuous functions f: [a,b] → F.
- Scalars: elements of F.
- Operations: same pointwise addition and scalar multiplication as in F^S.
- Zero vector: the zero function (identically zero).

6) Polynomial space P(F) (all polynomials with coefficients in F)
- Vectors: polynomials p(z) = a0 + a1 z + a2 z^2 + ... with finitely many nonzero ai in F.
- Scalars: elements of F.
- Vector addition: add coefficients: (p+q)(z) = p(z) + q(z).
- Scalar multiplication: multiply each coefficient by scalar: (a p)(z) = a·p(z).
- Zero vector: the zero polynomial (all coefficients 0).

7) P_m(F) — polynomials of degree at most m
- Vectors: polynomials p(z) = a0 + a1 z + ... + am z^m (degree ≤ m).
- Scalars: elements of F.
- Operations: coefficientwise addition and scalar multiplication as above.
- Zero vector: the polynomial with all ai = 0.
- Note: P_m(F) is finite-dimensional (dimension m+1 over F).

8) Spaces defined by algebraic constraints (examples)
- Example: {f in F^S : f(s0) = 0} (functions vanishing at a point)
  - Vectors: functions with the given property.
  - Scalars and operations: inherited pointwise operations from F^S.
  - Zero vector: still the zero function (satisfies the constraint).
- Example: {A in F^{n×n} : A is upper-triangular}
  - Vectors: upper-triangular n×n matrices.
  - Scalars and operations: inherited entrywise from F^{n×n}.
  - Zero vector: the upper-triangular zero matrix.

9) R as a vector space over itself and over Q
- R as an R-vector space:
  - Vectors: real numbers.
  - Scalars: real numbers.
  - Addition and scalar multiplication: the usual addition and multiplication of real numbers.
  - Zero vector: 0.
- R as a Q-vector space:
  - Vectors: real numbers.
  - Scalars: rational numbers.
  - Vector addition: usual addition of reals.
  - Scalar multiplication: rationals acting by usual multiplication on reals.
  - Zero vector: 0.
  - (Illustrates same set with different scalar field yields different vector-space structure.)

Remarks tying the examples together (brief)
- In all these examples the operations are defined elementwise (coordinate, entry, term, or value at a point) or coefficientwise; the scalar field F is what multiplies components/values/coefficients. The zero vector is the element that is zero in every coordinate/value/entry/coefficient. These concrete identifications show how the abstract axioms of a vector space are realized in familiar settings.

Subspace — definition and the subspace test

Definition
- Let V be a vector space over a field F. A subset W ⊆ V is a subspace of V if W itself is a vector space over F with the same addition and scalar multiplication as V. Concretely, W must be nonempty and must satisfy the vector-space axioms inherited from V.

Practical subspace test (closure conditions)
- To check that a nonempty subset W ⊆ V is a subspace it suffices to verify:
  1. Closed under addition: for all u, v in W, the sum u + v is in W.
  2. Closed under scalar multiplication: for all α in F and w in W, the product αw is in W.

Equivalently (often used as a convenient single-step test):
- For all u, v in W and all scalars α, β in F, the linear combination αu + βv lies in W.

Why these conditions are enough
- If W is nonempty and satisfies closure under addition and scalar multiplication, then:
  - 0 = 0·w ∈ W for any w ∈ W, so W contains the zero vector.
  - If w ∈ W then (−1)·w = −w ∈ W, so W contains additive inverses.
  - Associativity, commutativity, distributivity, and scalar associativity hold in W because they hold in V and W uses the same operations.
  Thus W satisfies all vector-space axioms and is a subspace.

Useful consequences and quick facts
- Any span of vectors, span{v1, …, vk}, is a subspace (it is closed under linear combinations by definition).
- The intersection of any collection of subspaces is a subspace.
- The union of two subspaces need not be a subspace (unless one is contained in the other). A simple counterexample: two distinct lines through the origin in R^2; their union is not closed under addition.
- A subset that does not contain the zero vector cannot be a subspace.

Typical checks when given a candidate subset W:
1. Is W nonempty? (Check for at least one element or directly check 0 ∈ W.)
2. Take arbitrary u, v ∈ W. Is u + v ∈ W?
3. Take arbitrary α ∈ F and w ∈ W. Is αw ∈ W?

If all three answers are yes, W is a subspace.

Span and Linear Combinations

Definitions
- Linear combination: Given vectors v1, v2, ..., vm in a vector space V and scalars a1, a2, ..., am (from the field over which V is defined), a linear combination of v1,...,vm is any vector of the form a1 v1 + a2 v2 + ... + am vm.
- Span: For a set S ⊆ V, the span of S, denoted span(S), is the set of all linear combinations of finitely many vectors from S. Equivalently,
  span(S) = {a1 v1 + ... + am vm : m ≥ 0, vi ∈ S, ai scalars}.
  (The case m = 0 yields the zero linear combination, so 0 ∈ span(S).)

Basic properties and facts
- span(S) is a subspace of V.
- span(S) is the smallest subspace of V that contains S: if U is any subspace with S ⊆ U, then span(S) ⊆ U.
  Proof sketch: span(S) is a subspace because it is closed under addition and scalar multiplication (linear combinations of linear combinations are linear combinations). Since S consists of linear combinations with one vector and coefficient 1, S ⊆ span(S). Any subspace U containing S must contain all linear combinations of elements of S, so it contains span(S); hence span(S) is minimal.
- span(∅) = {0}. (Only the zero linear combination is possible when no vectors are chosen.)
- If S = {v}, then span(S) = {a v : a a scalar} (the line through v and 0). If v = 0 then span({0}) = {0}.
- If one vector in S is a linear combination of others in S, removing it does not change span(S).

Computing spans — examples and methods
- To determine span{v1, v2, ..., vm}, ask: which vectors w can be written as a1 v1 + ... + am vm? Solve the linear system for the coefficients ai. If the vector space is R^n (or Fn), put v1,...,vm as columns of a matrix and use row reduction to determine which w are attainable (and to find relationships among the vi).
- Example 1: span{(1,0,0), (0,1,0)} in R^3 = {(x,y,0) : x,y ∈ R}. Reason: any linear combination a(1,0,0)+b(0,1,0) = (a,b,0). This is the xy-plane through the origin.
- Example 2: span{(1,2,3), (2,4,6)} in R^3. The second vector is 2 times the first, so span = {a(1,2,3) : a ∈ R}, a one-dimensional subspace (a line through the origin).
- Example 3: span{(1,0,0), (0,1,0), (0,0,1)} = R^3. These three vectors span all of R^3 because any (x,y,z) = x(1,0,0)+y(0,1,0)+z(0,0,1).
- Example 4 (polynomials): In P2 (polynomials of degree ≤ 2), span{1, x, x^2} = P2. Any quadratic ax^2 + bx + c is a linear combination c·1 + b·x + a·x^2.
- Example 5: span of an infinite set. If S = {e1, e2, e3, ...} in an infinite-dimensional space, span(S) means all finite linear combinations of these ei (so only finitely many nonzero coefficients allowed).

Interpreting span as the smallest containing subspace — practical use
- To check whether a subspace U equals span(S), show both S ⊆ U and that U is contained in span(S). Often you: (1) show every generator (element of S) lies in U, and (2) show any vector of U can be written as a linear combination of generators in S.
- To show a set S does not span V, find a vector in V that cannot be expressed as a linear combination of S (e.g., solve a linear system and find no solution).
- To reduce a spanning set to a smaller spanning set, remove any vector that is a linear combination of the others; this process leads toward a basis.

Summary (one-line)
- span(S) = all finite linear combinations of vectors from S; it is a subspace, and it is the smallest subspace of V that contains S.

Linear Independence and Dependence

Definition (via uniqueness of the zero representation):
A list of vectors v1, v2, …, vn in a vector space V is called linearly independent if the only scalars c1, c2, …, cn satisfying
c1 v1 + c2 v2 + … + cn vn = 0
are c1 = c2 = … = cn = 0. If there exists a nontrivial choice of scalars (some ci ≠ 0) that yields the zero vector, the list is linearly dependent.

Interpretation:
- Linear independence means the zero vector has a unique representation as a linear combination of the list (the trivial representation).
- Linear dependence means there is a nontrivial linear relation among the vectors: one of them can be expressed as a linear combination of the others.

How to determine independence/dependence (using the defining equation):
1. Write the equation c1 v1 + c2 v2 + … + cn vn = 0 with unknown scalars c1, …, cn.
2. Translate that vector equation into a system of linear equations (coordinate form) or form a matrix whose columns are v1,…,vn and row-reduce.
3. Solve for the scalars. 
   - If the only solution is the trivial solution (all ci = 0), the list is independent.
   - If there is a nontrivial solution, the list is dependent.

Short examples

Example 1 (independent):
Let v1 = (1, 0), v2 = (0, 1) in R^2. Solve c1(1,0) + c2(0,1) = (0,0). That gives c1 = 0 and c2 = 0, so {v1, v2} is linearly independent.

Example 2 (dependent):
Let v1 = (1, 2), v2 = (2, 4) in R^2. Solve c1(1,2) + c2(2,4) = (0,0). This yields the equations c1 + 2c2 = 0 and 2c1 + 4c2 = 0, which are the same equation; take c2 = 1, then c1 = -2 gives a nontrivial solution. Thus {v1, v2} is linearly dependent (indeed v2 = 2 v1).

Key remark:
A list containing the zero vector is always linearly dependent, because 1·0 + 0·(others) = 0 gives a nontrivial relation.

Section 7 — Basis

Definition
- A basis of a vector space V is a list of vectors v1, ..., vn in V that is both
  1) linearly independent, and
  2) spans V (every vector in V is a linear combination of v1, ..., vn).
- Note: “list” emphasizes order and allows repeated vectors; in particular a basis cannot contain the zero vector (that would make it linearly dependent).

Equivalent useful formulation
- A list v1, ..., vn is a basis of V exactly when every vector in V can be written uniquely as a linear combination of v1, ..., vn. (Uniqueness ⇔ linear independence; existence ⇔ spanning.)

How to verify a given list is a basis
1. Check spanning (existence):
   - Show an arbitrary vector of V can be written as a linear combination of the list.
   - Practically: set up the equation a1 v1 + ... + an vn = w for a general w and solve for the ai. If you can always solve, the list spans.
   - In coordinates (finite-dimensional V ≅ F^m), form a matrix whose columns are the coordinate vectors of v1,...,vn; spanning ⇔ the column space equals the whole space (matrix has a pivot in every row).

2. Check linear independence (uniqueness):
   - Show that a1 v1 + ... + an vn = 0 implies all ai = 0.
   - Practically: put the coordinate matrix (columns v1,...,vn) into reduced row-echelon form; linear independence ⇔ the only solution to the homogeneous system is the trivial one (matrix has a pivot in every column).

3. Dimension shortcut (when dim V known):
   - If V is finite-dimensional and you have a list of exactly dim V vectors, then showing either spanning or linear independence is enough: either property implies the other and thus the list is a basis.
   - If the list has more than dim V vectors it cannot be linearly independent; if fewer it cannot span.

Examples
- R^2: The list [(1,0), (0,1)] is a basis because it spans R^2 and is linearly independent. The list [(1,1), (2,2)] is not a basis because it is linearly dependent (second is scalar multiple of first), so it does not span R^2.
- P2 (polynomials of degree ≤2): The list [1, x, x^2] is a basis: any quadratic ax^2+bx+c is a linear combination, and independence follows because only the zero combination gives the zero polynomial.
- Non-example using dimension shortcut: In R^3 any list of 4 vectors cannot be a basis (too many → dependent). Any list of 2 vectors cannot be a basis (too few → cannot span).

Matrix test summary
- Make a matrix with the vectors as columns. Reduce to row-echelon form.
  - If there is a pivot in every column → independent.
  - If there is a pivot in every row (for an m×n matrix with m = dim V) → spans.
  - For n = m = dim V, pivots in every row ⇔ pivots in every column ⇔ basis.

Quick verification checklist (finite-dimensional V)
- If n = dim V:
  - Check one property (span or independence) → then list is a basis.
- If n ≠ dim V:
  - Use row reduction to check both spanning and independence directly.

End of section.

Coordinate representation (with respect to a basis)

Definition
- Let V be a vector space over a field F and let B = (v1, v2, ..., vn) be an ordered basis of V. Every vector v in V can be written uniquely as a linear combination
  v = a1 v1 + a2 v2 + ... + an vn
  for scalars a1, ..., an in F. The list (a1, a2, ..., an) of scalars is called the coordinate tuple (or coordinate vector) of v with respect to the basis B.

Notation
- [v]_B denotes the coordinate vector of v relative to basis B:
  [v]_B = (a1, a2, ..., an) in F^n.
- Conversely, given coordinates (a1,...,an) one reconstructs v by the linear combination above.

Uniqueness
- Uniqueness follows from linear independence of the basis. If
  a1 v1 + ... + an vn = b1 v1 + ... + bn vn,
  then (a1 - b1) v1 + ... + (an - bn) vn = 0. Since the vi are linearly independent, each ai - bi = 0, so ai = bi for all i.

Properties
- The coordinate map C_B : V -> F^n defined by C_B(v) = [v]_B is a linear isomorphism:
  - Linear: C_B(u + v) = C_B(u) + C_B(v) and C_B(αv) = α C_B(v).
  - Bijective: surjective because any tuple (a1,...,an) corresponds to a1 v1 + ... + an vn; injective by uniqueness.
- Therefore computations in V can be transferred to computations in F^n via coordinates.

How to compute coordinates (procedure)
1. Given v and basis B = (v1,...,vn), set up the equation v = a1 v1 + ... + an vn.
2. Express the vi and v in a common concrete form (if available) and solve the resulting linear system for the ai.
3. The solution (a1,...,an) is [v]_B.

Examples
- If V = R^3 and B = ( (1,0,0), (0,1,0), (0,0,1) ), then [ (2, -1, 5) ]_B = (2, -1, 5).
- If B = ( (1,1,0), (0,1,1), (1,0,1) ) and v = (2,1,3), solve for a1,a2,a3 in
  a1(1,1,0) + a2(0,1,1) + a3(1,0,1) = (2,1,3)
  which yields a linear system; its solution is [v]_B.

Remarks
- Coordinates depend on the chosen basis. Different bases give different coordinate tuples for the same vector.
- Because C_B is an isomorphism, many structural questions about V reduce to questions about F^n via coordinates.

Definition
- If V is a finite-dimensional vector space, any basis of V has the same number of vectors. That common number is called the dimension of V and is written dim V.
- If V has no finite basis we say V is infinite-dimensional.

Why the number is well-defined (sketch)
- If B and B' are bases of V, then B is linearly independent and B' spans V. A standard argument (replace/augment or exchange lemma) shows |B| ≤ |B'|. Reversing the roles gives |B'| ≤ |B|, hence |B| = |B'|.

Basic consequences and useful facts
1. Existence of bases in finite-dimensional spaces
   - By definition finite-dimensional means V has a finite spanning set S. From S one can remove redundant vectors (those that are linear combinations of others) to obtain a basis. Thus every finite-dimensional V has a basis.

2. Comparison by spanning and independence
   - Let V be finite-dimensional.
     a) If S spans V then |S| ≥ dim V. (Any basis is a subset of a spanning set after some reductions; or use exchange lemma.)
     b) If S is linearly independent then |S| ≤ dim V. (Extend S to a basis if necessary; the extended basis has size dim V.)

   - In particular, no linearly independent set in V can have more than dim V vectors, and no spanning set can have fewer than dim V vectors.

3. Subspaces
   - If U is a subspace of a finite-dimensional V, then U is finite-dimensional and dim U ≤ dim V.
   - Moreover, dim U = dim V iff U = V.
   - Proof sketch: Any basis of U is a linearly independent set in V, so its size ≤ dim V. If equality holds, the basis of U is a basis of V, so U = V.

4. Extending and reducing sets (useful constructions)
   - Any linearly independent set in a finite-dimensional space can be extended to a basis.
   - Any spanning set can be reduced (remove redundant vectors) to a basis.

5. Linear maps and dimensions
   - If T: U → V is linear and injective, then dim U ≤ dim V.
   - If T: U → V is linear and surjective, then dim U ≥ dim V.
   - In particular, for linear operators on a finite-dimensional space, injective ⇔ surjective.

6. Dimension of sums and intersections (rank–nullity style consequences)
   - If U and W are subspaces of a finite-dimensional V, then dim(U + W) = dim U + dim W − dim(U ∩ W). (Proof: choose a basis of U ∩ W, extend to bases of U and W, combine.)

Quick consequences to remember
- A finite list of vectors is a basis iff it is linearly independent and has length dim V, or iff it spans V and has length dim V.
- Any two bases of a finite-dimensional space have the same cardinality (the dimension).
- Finite-dimensionality behaves well with subspaces, linear maps, and direct sums; the dimension provides a simple numerical invariant to compare these objects.

Definition
- A vector space V (over a field F) is finite-dimensional if there exists a finite list of vectors that spans V. Equivalently, V is finite-dimensional iff V has a finite basis. If no finite spanning list exists, V is infinite-dimensional.

How to decide in examples
- To show a space is finite-dimensional: exhibit a finite spanning list (or finite basis). Showing a finite spanning set immediately proves finiteness; producing a finite basis also gives the dimension.
- To show a space is infinite-dimensional: exhibit an infinite linearly independent set (if you can produce infinitely many linearly independent vectors, no finite list can span). Alternatively, argue that no finite list can generate certain independent directions (for example, by degree or by coordinates).

Standard examples (with quick justifications)
- F^n (column vectors of length n over F): finite-dimensional. The standard list e1, …, en spans and is a basis, so dim F^n = n.
- M_{m×n}(F) (m×n matrices): finite-dimensional. The mn matrices with a single 1 in one entry and 0s elsewhere form a basis, so dim = mn.
- P_n(F) (polynomials of degree ≤ n): finite-dimensional. The list 1, x, x^2, …, x^n spans and is a basis, so dim = n+1.
- P(F) (all polynomials): infinite-dimensional. The monomials 1, x, x^2, … are linearly independent, so no finite spanning list exists.
- F^N (all sequences indexed by natural numbers): infinite-dimensional. The coordinate basis vectors e1, e2, … are linearly independent; no finite list can span all sequences.
- The space of all functions F → F or C(R) (continuous functions on R): infinite-dimensional. For instance, the functions 1, x, x^2, … (or other infinite independent families) show infinitude.
- The subspace of sequences that are eventually zero: infinite-dimensional (basis e1, e2, …), hence countably infinite dimension.

Useful facts to apply quickly
- "Finite spanning list" and "finite basis" are equivalent characterizations of finite-dimensionality.
- Any subspace of a finite-dimensional space is finite-dimensional; if V is finite-dimensional and W ≤ V, then dim W ≤ dim V.
- If you can find an infinite linearly independent subset in V, then V is infinite-dimensional.

Practical checklist when faced with a space
1. Try to write down a finite collection of vectors that clearly generates every element (if successful → finite-dimensional).
2. If that fails, look for an obvious infinite independent family (monomials, coordinate unit vectors, indicator functions, etc.) to prove infiniteness.

Concept: Linear Combinations and Spanning in Finite Dimensions

Definitions and basic facts
- Linear combination: For vectors v1, …, vn in a vector space V and scalars a1, …, an from the field F, the vector a1v1 + … + anvn is a linear combination of v1, …, vn.
- Span: The span of a list S = {v1, …, vn}, written span(S) or span{v1, …, vn}, is the set of all linear combinations of vectors in S. It is the smallest subspace of V that contains S.
- Spanning list: A list v1, …, vn spans V if span{v1, …, vn} = V. Equivalently, every vector in V can be written as a linear combination of v1, …, vn.

Using a spanning list to express vectors
- If v1, …, vn spans V then for any v in V there exist scalars a1, …, an with v = a1v1 + … + anvn. Finding these scalars is a matter of solving a linear system determined by the coordinates of v and the coordinates of the vi relative to some basis or by using Gaussian elimination on the matrix with columns v1,…,vn.
- Uniqueness: The coefficients a1, …, an need not be unique unless the spanning list is also linearly independent. If v1, …, vn span V and are linearly independent (i.e., they form a basis), then the representation of each v ∈ V as a linear combination of the vi is unique.

Key finite-dimensional spanning arguments
1. Finite spanning implies finite-dimensional subspaces
   - If V is finite-dimensional and W is a subspace of V, then W is also finite-dimensional. In particular, every element of W is a linear combination of some finite list of vectors in W (one can take a basis of W, obtained by extending/adjusting independent lists from W).
   - Dimension inequality: If W ≤ V then dim W ≤ dim V.

2. Spanning + extra vectors
   - If v1, …, vn spans V and w is any vector in V, then v1, …, vn, w still span V (adding vectors cannot shrink the span). Conversely, if some vi is a linear combination of the others, you can remove it without changing the span.

3. Replacement lemma (useful finite-dimensional argument)
   - Suppose V is finite-dimensional, and {u1, …, um} is a linearly independent list in V while {v1, …, vn} spans V. Then m ≤ n, and it is possible to replace m of the vi with the uj to produce a spanning list of length n. Intuition: you cannot have a larger independent list than the size of a spanning list.

4. Spanning and sums of subspaces
   - If U and W are subspaces of V, then U + W = span(U ∪ W) is the smallest subspace containing both. If U and W are finite-dimensional, then U + W is finite-dimensional and dim(U + W) ≤ dim U + dim W (with equality iff U ∩ W = {0} in the direct-sum case).

Techniques and common moves
- To express v in terms of a spanning list:
  1. Write a formal combination v = a1v1 + … + anvn.
  2. Move to coordinates relative to a convenient basis or form a matrix with columns v1,…,vn and solve the linear system for coefficients (Gaussian elimination).
  3. If coefficients are not unique, pick any solution; if uniqueness is required, first reduce to a basis (remove dependent vectors) and then solve.

- To show a list spans a subspace:
  - Show every generator of the subspace is a linear combination of the list; equivalently, show the subspace is contained in span(the list).
  - For U + W, demonstrate any u + w (u ∈ U, w ∈ W) is a linear combination of vectors from U ∪ W.

- To prove a subspace W is finite-dimensional when V is finite-dimensional:
  - Take a basis of V. Restrict attention to those basis vectors that lie in W; extend an independent subset of W to a basis of W. Alternatively, every nonzero subspace of a finite-dimensional space has a finite basis obtained by taking a maximal linearly independent subset.

Examples
- Example 1 (expressing a vector): If v1 = (1,0,1), v2 = (0,1,1) in F^3, they span the plane {(x,y,x+y)}. To express v = (2,3,5) as a combination, solve a1(1,0,1) + a2(0,1,1) = (2,3,5). This gives a1 = 2, a2 = 3 and 2+3 = 5 checks. So v = 2v1 + 3v2.

- Example 2 (removing redundant vectors): If v1, v2, v3 span V but v3 = 2v1 − v2, then v1, v2 already span V. To express any v ∈ V, write v = a1v1 + a2v2 + a3v3 and substitute v3 to reduce to the v1, v2 combination.

- Example 3 (subspace spanning): Let V = P3(F) (polynomials degree ≤ 3). The set S = {1, x, x^2} spans the subspace of polynomials of degree ≤ 2. Any p(x) = a + bx + cx^2 can be written directly as a linear combination of S.

Important consequences to remember
- In a finite-dimensional space, "spanning" and "linear independence" are tightly linked via dimension: any spanning list has length at least dim V; any independent list has length at most dim V. Therefore bases (lists that are both spanning and independent) always have the same length = dim V.
- Spanning behaves monotonically under inclusion: if S ⊆ T then span(S) ⊆ span(T). The span of a set is the minimal subspace containing it.
- Working with spans reduces many problems about subspaces to problems about linear combinations and solving linear systems.

Practice prompts
- Given a spanning list for V, find coefficients expressing a particular vector v as a linear combination.
- Given a list that spans V with a dependent element, remove redundancy and produce a smaller spanning list.
- For subspaces U, W ≤ V with finite bases, compute a spanning list for U + W and determine dim(U + W) using bases and intersection arguments.

Subspaces in Finite-Dimensional Spaces

Key facts (finite-dimensional setting)
- A subspace U of a finite-dimensional vector space V is itself finite-dimensional.
- Every spanning list for a subspace U contains a basis of U (remove dependences).
- Every linearly independent list in U can be extended to a basis of U.
- Any two bases of U have the same number of vectors; that number is dim U.
- If U ⊆ V then dim U ≤ dim V; equality holds iff U = V.

Finding a basis of a subspace from a generating list
Goal: start with a list that spans U and extract a basis (a linearly independent spanning list).

Procedure (algorithmic):
1. Put the spanning vectors as rows (or columns) of a matrix.
2. Row-reduce to echelon form.
3. The nonzero rows (or the original vectors corresponding to pivot columns, if you used columns) form a basis.
Reason: row reduction reveals linear dependencies; pivot rows are independent and span the same row space. If you treat original vectors as columns, choose columns with pivots to get an independent spanning set.

Example:
Given vectors v1, v2, v3 in R^3 that span U, form matrix [v1 v2 v3], row-reduce. If one column is a linear combination of others, remove it; remaining columns are a basis.

Finding a basis of a subspace from a linearly independent list
Goal: start with LI list in U and extend to a basis of U (i.e., to a spanning list).

Procedure:
1. If your linearly independent list already spans U, done.
2. Otherwise add vectors from U (not in the span) one at a time, checking linear independence (e.g., augment matrix and check rank) until the list spans U.
Theory guarantees this process terminates with a basis since U is finite-dimensional.

Comparing subspaces via dimension
- Inclusion: If U ⊆ W then dim U ≤ dim W. If dim U = dim W and U ⊆ W, then U = W.
- Strict inequality: If U ⊂ W (proper subset) then dim U < dim W.
- Sum and intersection (Grassmann formula): For subspaces U, W of V,
  dim(U + W) = dim U + dim W − dim(U ∩ W).
Use this to compute unknown dimensions or detect nontrivial intersection.

Practical uses and examples
- To test whether a subspace U equals V: find dim U and dim V. If dims equal and U ⊆ V, conclude U = V.
- To decide linear independence of a list inside U: place vectors in a matrix and check rank ≤ dim U. If you have more than dim U vectors, the list is necessarily dependent.
- To compute dim(U ∩ W): compute dim U, dim W, dim(U + W) and use the Grassmann formula rearranged:
  dim(U ∩ W) = dim U + dim W − dim(U + W).

Worked sketch (example practice)
1. Given U = span{(1,0,1), (0,1,1), (1,1,2)} in R^3.
   - Form matrix with these as columns, row-reduce. You will find rank 2 → a basis can be taken as first two independent columns, dim U = 2.
2. Given U and W with dim U = 3, dim W = 4 inside a 5-dimensional V and dim(U + W) = 5.
   - dim(U ∩ W) = 3 + 4 − 5 = 2.

Checklist when analyzing subspaces (finite-dimensional)
- Is the list spanning? If yes, extract basis by removing dependent vectors (row-reduction).
- Is the list independent? If yes but not spanning, extend it to a basis by adding independent vectors.
- Compare dimensions to decide equality or proper inclusion.
- Use dimension formulas to compute intersections or sums.

Exercises (recommended)
- Given specific lists of vectors, practice extracting bases via row reduction.
- For two explicit subspaces, compute bases, dimensions, U + W and U ∩ W; verify Grassmann formula.
- Show that any list in U longer than dim U is linearly dependent.

This section equips you to generate and identify bases of subspaces using spanning lists and linear independence, and to compare subspaces using dimension counting and the sum–intersection formula.

Fundamental Theorem of Linear Maps (Rank–Nullity)

Statement
- Let V be a finite-dimensional vector space and T: V → W a linear map. Then
  dim V = dim ker T + dim range T.
- dim ker T is called the nullity of T; dim range T is called the rank of T. The equality is often written
  dim V = nullity(T) + rank(T).

Proof (standard basis-extension argument)
1. Let {v1, ..., vk} be a basis of ker T. So dim ker T = k.
2. Extend this basis to a basis of V: choose vectors vk+1, ..., vn so that {v1, ..., vk, vk+1, ..., vn} is a basis of V (possible because V is finite-dimensional). Thus dim V = n.
3. Claim: {T(vk+1), ..., T(vn)} is a basis of range T.
   - Spanning: For any v ∈ V, write v = a1v1 + ... + akvk + ak+1vk+1 + ... + anvn. Apply T: T(v) = ak+1T(vk+1) + ... + anT(vn) because T(v1)=...=T(vk)=0. Hence range T is contained in span{T(vk+1),...,T(vn)}; conversely each T(vj) lies in range T.
   - Linear independence: Suppose b_{k+1}T(v_{k+1}) + ... + b_nT(v_n) = 0. Then T(b_{k+1}v_{k+1} + ... + b_nv_n) = 0, so the vector b_{k+1}v_{k+1} + ... + b_nv_n lies in ker T. Writing it in the full basis of V forces all coefficients b_{k+1},...,b_n to be zero (because the ker-basis vectors v1,...,vk are the only basis vectors spanning ker T). Thus T(vk+1),...,T(vn) are linearly independent.
4. Therefore dim range T = n − k. Combining gives dim V = k + (n − k) = dim ker T + dim range T, which proves the theorem.

Consequences and common corollaries (finite-dimensional case)
- Injectivity criterion: T is injective ⇔ ker T = {0} ⇔ nullity(T) = 0 ⇔ rank(T) = dim V. So a linear map from V is injective exactly when its rank equals dim V.
- Surjectivity criterion onto W: If T: V → W, then T is surjective ⇔ range T = W ⇔ rank(T) = dim W.
- Dimensional comparisons:
  - If dim V > dim W, any linear map T: V → W cannot be injective (because rank(T) ≤ dim W < dim V, so nullity(T) = dim V − rank(T) > 0).
  - If dim V < dim W, any linear map T: V → W cannot be surjective (because rank(T) ≤ dim V < dim W).
  - If dim V = dim W (finite), then T is injective ⇔ T is surjective. Equivalently, for maps between equal finite dimensions, it suffices to check one of injectivity or surjectivity to get the other.
- Rank bounds and consequences: For any T: V → W,
  0 ≤ rank(T) ≤ min(dim V, dim W), and nullity(T) = dim V − rank(T).
  This gives quick impossibility results (e.g., no surjection from a smaller-dimension domain to a larger codomain).

Quick examples (illustrative)
- Linear map R^5 → R^3: Any such map has rank ≤ 3, so nullity ≥ 2; thus every map R^5 → R^3 has a nontrivial kernel.
- Linear map R^2 → R^2: If a 2×2 matrix has nonzero determinant, its nullity is 0 and rank is 2, so it is bijective. If determinant 0, rank < 2, so nullity > 0 and map is not injective (hence not surjective).

Practical use in problems
- To decide injectivity/surjectivity quickly, compute or bound dimensions of kernel or image (often via solving homogeneous equations or row-reduction). Use rank–nullity to convert between information about kernel and image and to deduce impossibility when dimensions disagree.

Definition
A map T : V → W between vector spaces over the same field F is called linear (or a linear map, or a linear transformation) if for all u, v in V and all scalars α in F both of the following hold:
- T(u + v) = T(u) + T(v)  (preserves addition)
- T(αv) = α T(v)          (preserves scalar multiplication)

Equivalently, T is linear iff for all u, v in V and all scalars α, β in F,
T(αu + βv) = α T(u) + β T(v).

Representative examples
- Zero map: T : V → W defined by T(v) = 0 (the zero vector of W) for every v ∈ V. Verification: T(u+v)=0=0+0=T(u)+T(v), and T(αv)=0=α·0=αT(v).
- Identity map: I : V → V given by I(v) = v. Trivially linear.
- Matrix multiplication: For finite-dimensional V = F^n, W = F^m, any m×n matrix A defines T(x) = Ax. Matrix multiplication satisfies T(αx+βy)=A(αx+βy)=αAx+βAy, so T is linear.
- Differentiation on polynomials: D : P(F) → P(F) with D(p) = p' is linear because (p+q)' = p' + q' and (αp)' = α p'.
- Evaluation at a point (linear functional): For fixed a in F, ev_a : P(F) → F defined by ev_a(p) = p(a) is linear: ev_a(αp+βq) = αp(a)+βq(a).
- Definite integration: I : C([a,b]) → F given by I(f) = ∫_a^b f(x) dx is linear: integral of a linear combination is that linear combination of integrals.
- Projection: If V = U ⊕ W, the projection onto U along W is linear.

Representative non-examples (maps that are not linear)
- Constant nonzero map: T(v) = w0 for all v, where w0 ≠ 0. This fails T(0) = w0 ≠ 0 = 0·T(0), or fails additivity.
- Translation/affine map: T(v) = Av + b with b ≠ 0 is not linear (it is affine). Example on R: T(x) = x + 1 is not linear because T(0) ≠ 0.
- Absolute value: |·| : R → R, |x| is not linear since |−1| = 1 ≠ −|1|.
- Norm/length: v ↦ ||v|| is not linear in general (does not preserve scalar multiplication for negative scalars and addition).
- Componentwise nonlinear operations: For example T(x,y) = (x^2, y) on R^2 is not linear because T(α(x,y)) ≠ αT(x,y) in general.
- Multiplying by a non-scalar-dependent function: For function spaces, the map M_g : f ↦ g·f is linear only when g is a fixed function; if g depends on f, it need not be linear.

Quick checks to test linearity
- Check T(0): For a linear T, T(0_V) must be 0_W. If not, T is not linear.
- Check homogeneity: Verify T(αv) = αT(v) for one nonzero scalar α and some v; failure shows nonlinearity.
- Check additivity: Verify T(u+v) = T(u)+T(v) for some u, v; failure shows nonlinearity.

Matrix of a linear map (with respect to bases)

Setup
- Let V and W be finite-dimensional vector spaces with dim V = n, dim W = m.
- Fix ordered bases B = (v1,...,vn) for V and C = (w1,...,wm) for W.
- Let T : V → W be a linear map.

How the matrix is defined
- For each basis vector vj of V, compute T(vj) ∈ W.
- Express T(vj) as a linear combination of the W-basis:
  T(vj) = a1j w1 + a2j w2 + ... + amj wm.
- The scalars aij are the entries of the m×n matrix [T]_{C←B} (read “matrix of T from B to C”). Column j of this matrix is the coordinate column of T(vj) relative to C:
  column j = [T(vj)]_C = (a1j, a2j, ..., amj)^T.

Applying the matrix to coordinates
- If v ∈ V has coordinate column x = [v]_B ∈ F^n (so v = x1 v1 + ... + xn vn), then T(v) has coordinate column y = [T(v)]_C ∈ F^m given by
  y = [T]_{C←B} x.
- In other words, to find T(v) you:
  1. Write v in coordinates relative to B.
  2. Multiply the matrix [T]_{C←B} by that coordinate column.
  3. The resulting column gives the coordinates of T(v) relative to C; reconstruct T(v) from those coordinates and the basis C if needed.

Properties and remarks
- The matrix is completely determined by how T acts on the basis B: its columns are exactly [T(v1)]_C, ... , [T(vn)]_C.
- The matrix depends on the choice and ordering of bases B and C; different bases give different matrices for the same linear map.
- If V = W and the same basis is used for domain and codomain, [T] is an n×n matrix and composition of linear maps corresponds to matrix multiplication (with respect to compatible bases).

Null space (kernel) and injectivity

Definition
- For a linear map T: V → W, the null space (or kernel) of T is
  null T = { v in V : T(v) = 0 }.
  It is a subspace of V.

Characterization of injectivity
- T is injective (one-to-one) ⇔ null T = {0}.
  Proof sketch:
  - If T is injective and v ∈ null T, then T(v) = 0 = T(0). Injectivity implies v = 0, so null T = {0}.
  - Conversely, if null T = {0} and T(v1) = T(v2), then T(v1 − v2) = T(v1) − T(v2) = 0, so v1 − v2 ∈ null T. Thus v1 − v2 = 0, hence v1 = v2, so T is injective.

How to test injectivity using the null space
- Solve T(v) = 0. If the only solution is v = 0, T is injective; if there exists a nonzero solution, T is not injective.
- In practice:
  - For a matrix representation A of T (with respect to chosen bases), compute the solution space of Ax = 0 (e.g., by row-reduction). If the only solution is x = 0, the linear map is injective.
  - In the finite-dimensional case, use the rank-nullity theorem: dim V = dim(range T) + dim(null T). Thus T is injective ⇔ dim(null T) = 0 ⇔ dim(range T) = dim V. Equivalently, for maps V → W with dim V > dim W, T cannot be injective.

Takeaway
- The null space is the precise test for injectivity: trivial kernel ⇔ injective map.

Range (image) of a linear map
- Definition. If T : V → W is a linear map, the range (also called the image) of T is
  Range(T) = {T(v) : v ∈ V} ⊆ W.
- Property. Range(T) is a subspace of W.

Surjectivity in terms of the range
- Definition. T is surjective (onto) if for every w ∈ W there exists v ∈ V with T(v) = w.
- Range characterization. T is surjective exactly when Range(T) = W.

How to test surjectivity
- Direct test. Show that for an arbitrary w ∈ W you can produce v ∈ V with T(v) = w.
- Span/test by generators. Show a generating set (or a basis) of W is contained in Range(T). Equivalently, show Range(T) spans W.
- Dimension test (finite-dimensional case). If V and W are finite-dimensional then T is surjective ⇔ dim Range(T) = dim W. Using rank-nullity: rank(T) = dim W ⇔ T is surjective.
  - Immediate corollary: if dim V < dim W then no linear map V → W can be surjective.
- Matrix criterion. If T is represented by a matrix A (with respect to bases of V and W), Range(T) is the column space of A. T is surjective ⇔ the columns of A span W ⇔ the column rank of A equals dim W. Practically, use row reduction to check whether the column space has full dimension.
- Computational approach. Solve the linear system A x = b for arbitrary b ∈ W; T is surjective iff every b yields at least one solution.

These tests are interchangeable: pick the one best suited to the context (direct construction, spanning/basis argument, dimension count, or matrix row-reduction).

Composition of linear maps
- Setup: If V, W, and U are vector spaces and S: V → W and T: W → U are linear maps, the composition T ∘ S: V → U is defined by (T ∘ S)(v) = T(S(v)) for all v ∈ V.
- Linearity: T ∘ S is linear.
- Domain/codomain rule: Composition is defined only when the codomain of the first map equals the domain of the second; i.e. S: V → W and T: W → U.
- Associativity: If R: U → X is another linear map, then R ∘ (T ∘ S) = (R ∘ T) ∘ S.
- Relation to matrices: If linear maps are represented by matrices with respect to chosen bases, composition corresponds to matrix multiplication (the matrix of T ∘ S is the product of the matrices of T and S, with appropriate bases).

Inverse maps and invertibility
- Definition of inverse: Let T: V → W be linear. An inverse of T is a linear map S: W → V such that S ∘ T = I_V and T ∘ S = I_W, where I_V and I_W are the identity maps on V and W respectively. If such an S exists, T is called invertible and that unique S is denoted T^{-1}.
- Uniqueness: If an inverse exists, it is unique. (If S and S' are both inverses of T, then S = S ∘ I_W = S ∘ (T ∘ S') = (S ∘ T) ∘ S' = I_V ∘ S' = S'.)

Criteria for invertibility
- Bijectivity criterion: A linear map T: V → W is invertible ⇔ T is bijective (both injective and surjective).
- Left/right inverses and one-sided criteria:
  - If there exists S: W → V with S ∘ T = I_V (a left inverse), then T is injective.
  - If there exists S: W → V with T ∘ S = I_W (a right inverse), then T is surjective.
  - For linear maps, existence of a left inverse and existence of a right inverse together are equivalent to existence of a two-sided inverse; moreover, on finite-dimensional spaces one-sided inverses already force the other side as explained next.
- Finite-dimensional simplification: If V and W are finite-dimensional and dim V = dim W, then for a linear map T: V → W the following are equivalent:
  - T is invertible.
  - T is injective.
  - T is surjective.
  Thus, on equal finite-dimensional spaces you need only check injectivity or only check surjectivity to conclude invertibility.
- Rank-nullity connection: For T: V → W with V finite-dimensional, T is injective ⇔ nullity(T) = 0 ⇔ rank(T) = dim V; and T is surjective ⇔ rank(T) = dim W. When dim V = dim W, these conditions coincide.

Useful identities for inverses
- (T^{-1})^{-1} = T.
- If S: V → W and T: W → U are invertible, then T ∘ S is invertible and (T ∘ S)^{-1} = S^{-1} ∘ T^{-1}.

These are the core definitions and invertibility criteria used when working with compositions and inverses of linear maps (especially in the finite-dimensional setting).

Characteristic polynomial (definition)
- For an n×n matrix A over a field F, the characteristic polynomial of A is
  p_A(λ) = det(λI_n − A).
- For a linear operator T: V → V on an n-dimensional vector space V, choose a basis B and let [T]_B be the matrix of T in that basis. The characteristic polynomial of T is
  p_T(λ) := det(λI_n − [T]_B).
  This p_T is well defined (independent of the chosen basis) — see below.

Roots ↔ eigenvalues
- A scalar λ ∈ F is an eigenvalue of A (or of T) ⇔ there exists a nonzero vector v with A v = λ v ⇔ (λI − A) is not invertible ⇔ det(λI − A) = 0.  
  Hence the eigenvalues are exactly the roots of the characteristic polynomial.
- The algebraic multiplicity of an eigenvalue λ is its multiplicity as a root of p_A(λ).

Basis dependence / independence
- The matrix [T]_B depends on the chosen basis B. If B and B′ are two bases and P is the change-of-basis matrix, then [T]_{B′} = P^{-1}[T]_B P (similar matrices).
- Similarity preserves the characteristic polynomial:
  det(λI − P^{-1}AP) = det(P^{-1}(λI − A)P) = det(λI − A).
  Therefore p_{[T]_B}(λ) is the same for every basis B, so p_T is intrinsic to the operator T (basis-independent).
- In other words, while the matrix entries change with a basis, the polynomial p_T(λ) does not.

Basic properties to keep in mind
- deg p_A = n, and p_A is monic (leading coefficient 1).
- p_A(0) = det(−A) = (−1)^n det A.
- If λ is an eigenvalue, its geometric multiplicity (dimension of eigenspace) is at least 1 and at most its algebraic multiplicity (multiplicity as a root of p_A).

(End of section)

Minimal polynomial — definition and basic properties

Definition
- Let V be a finite-dimensional vector space over a field F and let T ∈ L(V) (or let A be an n×n matrix over F). A polynomial m ∈ F[x] is called an annihilating polynomial for T if m(T) = 0 (the zero operator). The minimal polynomial of T is the unique monic polynomial μ ∈ F[x] of least degree such that μ(T) = 0. We denote it by μ_T or μ_A.

Existence (finite-dimensional case)
- Consider the sequence of operators I, T, T^2, … in L(V). Since V is finite-dimensional, L(V) is finite-dimensional, so the infinite list I, T, T^2, … is linearly dependent. Hence there exist scalars a0, a1, …, ak, not all zero, with
  a0 I + a1 T + ⋯ + ak T^k = 0.
  Viewing this as a polynomial relation gives a nonzero polynomial p(x) = a0 + a1 x + ⋯ + ak x^k with p(T) = 0. Thus some nonzero annihilating polynomial exists.
- Among all nonzero annihilating polynomials choose one of least degree and scale it to be monic; this is the minimal polynomial μ. So existence follows from linear dependence of the powers of T.

Uniqueness and divisibility property
- If μ is a monic annihilating polynomial of least degree, and p is any polynomial with p(T) = 0, perform polynomial division of p by μ: p = qμ + r with deg r < deg μ. Applying to T gives
  0 = p(T) = q(T)μ(T) + r(T) = r(T),
  since μ(T) = 0. By minimality of μ, the only possibility is r = 0. Hence μ divides p. In particular, μ is unique (the monic minimal-degree annihilator) and every annihilating polynomial is a multiple of μ.

Consequences / algebraic relations
1. Operator satisfies its minimal polynomial: μ(T) = 0 by definition.
2. μ divides every polynomial p with p(T) = 0. Therefore the set of annihilating polynomials is exactly μ·F[x].
3. Relation to the characteristic polynomial χ_T: Cayley–Hamilton asserts χ_T(T) = 0, so μ divides χ_T. Thus deg μ ≤ dim V and μ shares the same irreducible factors (with possibly lower multiplicities) as χ_T.
4. Invertibility criterion: T is invertible iff 0 is not a root of μ, equivalently the constant term μ(0) ≠ 0. (If μ(0) = 0 then x divides μ so μ(T) = 0 implies T has nontrivial kernel.)
5. Diagonalizability criterion (algebraic): If μ factorizes over F as a product of distinct linear factors (i.e. μ(x) = (x − λ1)…(x − λk) with no repeated factors), then T is diagonalizable. Conversely, if T is diagonalizable then its minimal polynomial is a product of distinct linear factors whose roots are the eigenvalues of T.
6. Structure information: The minimal polynomial encodes the sizes of Jordan blocks (over an algebraically closed field). Concretely, for each eigenvalue λ, the exponent of (x − λ) in μ equals the size of the largest Jordan block for λ; more generally, exponents in μ give the maximal sizes of cyclic blocks in the primary decomposition.

Remark (practical use)
- Knowing μ gives all polynomial relations p(T)=0: they are exactly the multiples of μ. It also bounds algebraic complexity of T (degree ≤ dim V) and provides criteria for invertibility and diagonalizability, and, together with the factorization of μ, leads to the primary decomposition of V into T-invariant subspaces.

Section 21 — Polynomial Division Algorithm

Statement (Division Algorithm for Polynomials).
Let F be a field. For any polynomials f(x), g(x) in F[x] with g(x) ≠ 0, there exist unique polynomials q(x) and r(x) in F[x] such that
f(x) = g(x) q(x) + r(x)
and either r(x) = 0 or deg r(x) < deg g(x).

Existence (sketch).
Proceed by induction on n = deg f.

- If deg f < deg g, take q = 0 and r = f; the conclusion holds.
- If deg f ≥ deg g, write deg f = m and deg g = d. Let a be the leading coefficient of f and b the leading coefficient of g. Define a monomial t(x) = (a/b) x^{m-d} ∈ F[x]. Then f(x) − t(x) g(x) has degree < m. By the induction hypothesis, we can write
  f(x) − t(x) g(x) = g(x) q1(x) + r(x)
  with deg r < d. Setting q(x) = t(x) + q1(x) gives f = g q + r with deg r < deg g.

Thus q and r exist.

Uniqueness.
Suppose f = g q1 + r1 = g q2 + r2 with deg r1 < deg g and deg r2 < deg g. Then
g (q1 − q2) = r2 − r1.
If q1 ≠ q2 then q1 − q2 ≠ 0 and deg[g(q1 − q2)] ≥ deg g + deg(q1 − q2) ≥ deg g, while deg(r2 − r1) < deg g. This is a contradiction. Hence q1 = q2, and then r1 = r2. So q and r are unique.

Remarks.
- The algorithm and the proof use only that F is a field (so leading coefficients are invertible). The same statement fails in general rings where leading coefficients may not be units.
- The division algorithm underlies the Euclidean algorithm for computing greatest common divisors in F[x].

Worked examples

Example 1 — Divide f(x) = x^3 + 2x^2 + 3x + 4 by g(x) = x + 1.
We perform polynomial long division (or synthetic division).

1. Leading term: x^3 divided by x gives x^2. Multiply g by x^2: (x + 1)x^2 = x^3 + x^2.
   Subtract: (x^3 + 2x^2 + 3x + 4) − (x^3 + x^2) = (2x^2 − x^2) + 3x + 4 = x^2 + 3x + 4.

2. Leading term: x^2 divided by x gives x. Multiply g by x: (x + 1)x = x^2 + x.
   Subtract: (x^2 + 3x + 4) − (x^2 + x) = 2x + 4.

3. Leading term: 2x divided by x gives 2. Multiply g by 2: (x + 1)2 = 2x + 2.
   Subtract: (2x + 4) − (2x + 2) = 2.

Remainder has degree 0 < deg g = 1. So
q(x) = x^2 + x + 2, r(x) = 2,
and indeed x^3 + 2x^2 + 3x + 4 = (x + 1)(x^2 + x + 2) + 2.

Example 2 — Divide f(x) = x^4 − x + 1 by g(x) = x^2 + 1.
1. Leading term: x^4 divided by x^2 gives x^2. Multiply: (x^2 + 1)x^2 = x^4 + x^2.
   Subtract: (x^4 + 0x^3 + 0x^2 − x + 1) − (x^4 + x^2) = −x^2 − x + 1.

2. Leading term: (−x^2) divided by x^2 gives −1. Multiply: (x^2 + 1)(−1) = −x^2 − 1.
   Subtract: (−x^2 − x + 1) − (−x^2 − 1) = (−x^2 + x^2) + (−x) + (1 + 1) = −x + 2.

Now deg(−x + 2) = 1 < deg g = 2, so stop. Therefore
q(x) = x^2 − 1, r(x) = −x + 2,
and x^4 − x + 1 = (x^2 + 1)(x^2 − 1) + (−x + 2).

Example 3 — Over a finite field: divide f(t) = t^3 + 2t + 1 by g(t) = t^2 + 1 in F3 (coefficients mod 3).
Work mod 3.

1. t^3 divided by t^2 gives t. Multiply: (t^2 + 1)t = t^3 + t.
   Subtract: (t^3 + 0t^2 + 2t + 1) − (t^3 + t) = (2t − t) + 1 = t + 1 (since 2 − 1 ≡ 1 mod 3).

Now deg(t + 1) = 1 < 2, so q(t) = t and r(t) = t + 1. Check:
t^3 + 2t + 1 ≡ (t^2 + 1)t + (t + 1) (mod 3).

These examples illustrate: given any f and nonzero g in F[x], repeated subtraction of suitable multiples of g (reducing the leading power at each step) produces a quotient q and remainder r satisfying the degree bound; uniqueness follows from degree considerations.

Definition
Let V be a vector space over a field F, let T: V → V be a linear operator, and let
p(z) = a0 + a1 z + ··· + an z^n
be a polynomial with coefficients in F. Define the operator p(T): V → V by
p(T) = a0 I + a1 T + ··· + an T^n,
where I is the identity operator on V and T^k denotes the k-fold composition of T (with T^0 = I).

Basic examples
- If p(z) = 1 then p(T) = I.
- If p(z) = z then p(T) = T.
- If p(z) = z^n then p(T) = T^n.

Algebraic properties
Let p and q be polynomials and α ∈ F. Then the map p ↦ p(T) respects the usual polynomial algebra operations:

1) Addition:
(p + q)(T) = p(T) + q(T).
Proof: Write p(z) = ∑ ai z^i and q(z) = ∑ bi z^i. Then
(p + q)(T) = ∑ (ai + bi) T^i = ∑ ai T^i + ∑ bi T^i = p(T) + q(T).

2) Scalar multiplication:
(αp)(T) = α p(T).
Proof: (αp)(T) = ∑ (α ai) T^i = α ∑ ai T^i = α p(T).

3) Multiplication (product of polynomials corresponds to composition/product of operators):
(pq)(T) = p(T) q(T).
Proof: Expand p(z) = ∑ ai z^i and q(z) = ∑ bj z^j. Then
(pq)(z) = ∑i ∑j ai bj z^{i+j},
so
(pq)(T) = ∑i ∑j ai bj T^{i+j} = (∑i ai T^i)(∑j bj T^j) = p(T) q(T),
where the product of operators on the right is composition (or equivalently operator multiplication), and the double sum collapses to the expected composition sum because T^i T^j = T^{i+j}.

Consequences
- The assignment p ↦ p(T) is an F-algebra homomorphism from the polynomial algebra F[z] into the algebra of linear operators on V.
- p(T) commutes with T: T p(T) = p(T) T (since T T^i = T^i T).
- More generally, if S is any operator that commutes with T (ST = TS), then S commutes with p(T): S p(T) = p(T) S (this follows by linearity and the fact S commutes with each T^i).

These facts let us treat polynomials in the operator T exactly as we treat ordinary polynomials, with multiplication interpreted as composition of operators.

Polynomial vector space P(F) and degree

Definition. Let F be a field. P(F) denotes the set of all polynomials with coefficients in F:
p(x) = a0 + a1 x + a2 x^2 + ··· + an x^n,
where n ≥ 0, ai ∈ F and only finitely many ai are nonzero. Addition and scalar multiplication are defined coefficientwise:
(p+q)(x) = (a0+b0) + (a1+b1)x + ···,
(αp)(x) = (αa0) + (αa1)x + ···,
for p(x)=∑ ai x^i, q(x)=∑ bi x^i and α∈F.

Degree. For p ≠ 0, deg p is the largest i with ai ≠ 0. By convention deg 0 = −∞ (or sometimes undefined), so that deg(p+q) ≤ max(deg p, deg q) and deg(αp) = deg p for α ≠ 0.

Standard basis. The sequence {1, x, x^2, x^3, …} is the standard (monomial) basis of P(F): every polynomial p can be written uniquely as a finite linear combination
p = a0·1 + a1·x + a2·x^2 + ··· + an·x^n.
Each monomial x^i corresponds to the vector with a 1 in the i-th coefficient and 0 elsewhere. {1, x, x^2, …} is linearly independent because a finite linear relation ∑ ci x^i = 0 forces each coefficient ci = 0, and it spans P(F) by construction. Thus P(F) is an infinite-dimensional vector space over F. The subspace Pn(F) of polynomials of degree ≤ n is finite-dimensional with basis {1, x, …, x^n}.

Verification of vector space axioms (sketch). Using coefficientwise operations, the vector space axioms hold:

- Closure under addition: sum of two polynomials has coefficients a_i + b_i, finitely many nonzero, so is a polynomial.
- Commutativity: (p+q)(x) = ∑ (ai+bi)x^i = ∑ (bi+ai)x^i = (q+p)(x).
- Associativity: (p+(q+r))(x) and ((p+q)+r)(x) have identical coefficients by associativity of addition in F.
- Additive identity: the zero polynomial 0 (all coefficients 0) satisfies p+0 = p.
- Additive inverses: for p = ∑ ai x^i, −p = ∑ (−ai) x^i is in P(F) and p+(−p)=0.
- Closure under scalar multiplication: αp has coefficients αai, finitely many nonzero.
- Compatibility of scalar multiplication:
  - (αβ)p = α(βp) follows from field multiplication.
  - 1·p = p since 1·ai = ai.
  - Distributivity over vector addition: α(p+q) = αp+αq coefficientwise.
  - Distributivity over field addition: (α+β)p = αp+βp coefficientwise.

Examples. If p(x)=2+3x and q(x)=1−x+4x^2 in F = ℝ then
p+q = 3 + 2x + 4x^2,
2·p = 4 + 6x.
Degrees: deg p = 1, deg q = 2, deg(p+q) ≤ 2, deg(2·p) = 1.

Remarks. Because each polynomial involves only finitely many basis vectors, linear combinations are finite. P(F) is therefore the span of {1,x,x^2,…} and has the usual algebraic structure used throughout polynomial theory.

Zeros (Roots) and Linear Factors

- Zero ↔ linear factor: If p is a polynomial over a field F and a ∈ F satisfies p(a) = 0, then the polynomial x − a is a factor of p; that is, there exists q ∈ F[x] with p(x) = (x − a) q(x). Conversely, if p(x) = (x − a) q(x) then p(a) = 0.

- Multiplicity as repeated factors: The multiplicity of a zero a is the exponent of the linear factor x − a in the factorization of p. More precisely, a has multiplicity m ≥ 1 if and only if
  (x − a)^m divides p(x) but (x − a)^{m+1} does not. Equivalently, p(x) can be written as p(x) = (x − a)^m r(x) with r(a) ≠ 0.

- Consequences:
  - Counting multiplicity: If p factors over F as p(x) = c ∏_{i=1}^k (x − a_i)^{m_i} (where the a_i are distinct and c ∈ F\{0}), then the degree of p is ∑_{i=1}^k m_i and each a_i is a root of multiplicity m_i.
  - Upper bound on distinct zeros: A nonzero polynomial of degree n over a field has at most n distinct zeros; counting multiplicity, the total number of zeros (with multiplicity) equals n when p splits completely over the field.

- Detecting multiplicity (derivative test): If p(a) = 0, then a is a simple root (multiplicity 1) exactly when p′(a) ≠ 0. More generally, a has multiplicity m iff p(a) = p′(a) = … = p^{(m−1)}(a) = 0 and p^{(m)}(a) ≠ 0.

- Example: p(x) = (x − 2)^3(x + 1). Here 2 is a root of multiplicity 3 (the factor (x − 2) appears three times) and −1 is a root of multiplicity 1.

This relationship between zeros and linear factors lets us move freely between root information and algebraic factorization.

Characteristic polynomial (linear map or matrix)
- Let V be an n-dimensional vector space and T : V → V a linear map. Choose a basis of V and let A be the matrix of T in that basis. The characteristic polynomial of T (or of A) is the polynomial
  p_T(t) = det(tI – A).
  This is a monic polynomial of degree n and is independent of the choice of basis, so it is a well-defined invariant of the linear map T.

Zeros are eigenvalues
- A scalar λ ∈ F is an eigenvalue of T ⇔ there exists a nonzero v ∈ V with T(v) = λv ⇔ T – λI is not injective ⇔ T – λI is not invertible ⇔ det(T – λI) = 0.
  Equivalently, representing T by A, λ is an eigenvalue ⇔ det(A – λI) = 0 ⇔ p_T(λ) = 0. Thus the eigenvalues of T are exactly the roots (zeros) of the characteristic polynomial.

Algebraic multiplicity
- If λ is a root of p_T(t), its algebraic multiplicity is the multiplicity of λ as a root of p_T(t); i.e. if p_T(t) factors (over the field) as
  p_T(t) = (t – λ)^m q(t)
  with q(λ) ≠ 0, then the algebraic multiplicity of λ is m.
- Remarks: algebraic multiplicity is a positive integer ≤ n and the sum of algebraic multiplicities of all (possibly repeated) roots equals n.

Section: Diagonalization via Eigenvectors

Criterion (basic and practical)
- An operator T on a finite-dimensional vector space V (or an n×n matrix A) is diagonalizable precisely when V has a basis consisting of eigenvectors of T. Equivalently:
  1. There exists an ordered basis (v1,...,vn) of V with Tvj = λj vj for scalars λj; or
  2. There exists an invertible matrix S such that S−1AS is diagonal (for A the matrix of T in some basis); or
  3. The direct sum of the eigenspaces equals V, i.e. V = ⊕_{λ∈Spec(T)} E(λ).

Algebraic vs geometric multiplicity criterion
- For each eigenvalue λ, let its algebraic multiplicity (multiplicity as a root of the characteristic polynomial) be m_a(λ) and its geometric multiplicity (dimension of the eigenspace E(λ)) be m_g(λ). T is diagonalizable iff for every eigenvalue λ we have m_g(λ) = m_a(λ). Equivalently, the sum of the dimensions of the eigenspaces equals dim V.

Why these are equivalent (sketch)
- If V has an eigenbasis {v1,...,vn} with Tvj = λj vj, the matrix of T in that basis is diagonal with entries λ1,...,λn, so T is represented by a diagonal matrix.
- Conversely, if S−1AS = D is diagonal, columns of S are a basis of eigenvectors of A (or T), because A(S e_j) = S D e_j = (S e_j) λ_j.
- The geometric vs algebraic multiplicity statement follows because within each eigenspace E(λ) you can choose m_g(λ) independent eigenvectors; diagonalizability requires that you can choose enough eigenvectors to total dim V, and you cannot have more than the algebraic multiplicity for a given λ, so equality is necessary and sufficient.

How the diagonal form represents the action of T
- Suppose {v1,...,vn} is an eigenbasis with Tvj = λj vj. Write any vector x ∈ V in coordinates relative to this basis: x = c1 v1 + ... + cn vn. Then
  T x = c1 λ1 v1 + ... + cn λn vn.
  In coordinate form this means the coordinate vector [x]_basis = (c1,...,cn)^T is mapped to [T x]_basis = diag(λ1,...,λn) [x]_basis.
- Interpretation: In an eigenbasis, T acts by independently scaling each coordinate by the corresponding eigenvalue. Thus the diagonal entries give the full action of T on the basis directions.

How to test and diagonalize (procedure)
1. Compute the characteristic polynomial and its eigenvalues λ.
2. For each eigenvalue λ, find a basis of the eigenspace E(λ) and record m_g(λ).
3. Check whether sum_{λ} m_g(λ) = n (equivalently m_g(λ) = m_a(λ) for each λ). If not, T is not diagonalizable.
4. If yes, form S whose columns are the chosen eigenvectors (one set per eigenvalue). Then S is invertible and S−1AS = D is diagonal with diagonal entries the corresponding eigenvalues (matching the column order of S).

Remark
- Distinct eigenvalues always produce linearly independent eigenvectors, so an operator with n distinct eigenvalues is automatically diagonalizable.
- Diagonalization simplifies many problems (powers, exponentials, functional calculus) because operations act entrywise on the diagonal.

Eigenspace corresponding to an eigenvalue

Definition. Let V be a vector space over a field F and let T ∈ L(V). For λ ∈ F the eigenspace of T corresponding to λ is
Eλ := {v ∈ V : Tv = λv}.
Equivalently, Eλ = {0} ∪ {v ∈ V \ {0} : v is an eigenvector of T with eigenvalue λ}.

Proposition. For each λ ∈ F, Eλ is a subspace of V. Moreover,
Eλ = null(T − λI),
where I is the identity operator on V. In particular, λ is an eigenvalue of T if and only if Eλ ≠ {0}.

Proof. Let S = T − λI. For v ∈ V,
v ∈ null S ⇔ S v = 0 ⇔ (T − λI)v = 0 ⇔ Tv = λv,
so Eλ = null S.

Since null S is the kernel of a linear map S ∈ L(V), it is a subspace of V. Concretely, check the subspace axioms for Eλ directly: 0 ∈ Eλ because T0 = 0 = λ0. If u, v ∈ Eλ then T(u+v) = Tu + Tv = λu + λv = λ(u+v), so u+v ∈ Eλ. If v ∈ Eλ and α ∈ F then T(αv) = αTv = α(λv) = λ(αv), so αv ∈ Eλ. Hence Eλ is closed under addition and scalar multiplication, and therefore is a subspace of V.

Finally, λ is an eigenvalue of T iff there exists a nonzero v with Tv = λv, i.e. iff Eλ contains a nonzero vector, i.e. iff Eλ ≠ {0}. Equivalently, λ is an eigenvalue iff null(T − λI) ≠ {0}.
∎

Definition
- Let V be a vector space over a field F and T: V → V a linear map (operator). A scalar λ in F is an eigenvalue of T if there exists a nonzero vector v in V such that
  T(v) = λ v.
  Any nonzero v satisfying this equation is called an eigenvector of T corresponding to λ.

Verifying the eigenvector/eigenvalue equation
1. Nonzero vector: first check v ≠ 0. The zero vector is never an eigenvector.
2. Apply T to v: compute T(v).
3. Compare to λv: compute λv.
4. Conclusion:
   - If T(v) = λv, then v is an eigenvector and λ is its eigenvalue.
   - If T(v) ≠ λv for the given pair (λ,v), then they do not satisfy the eigen-equation.
Practical algebraic test (for matrices): if T is represented by a matrix A relative to some basis, then v is an eigenvector with eigenvalue λ exactly when (A − λI)v = 0. Equivalently, λ is an eigenvalue precisely when det(A − λI) = 0 (the characteristic polynomial has λ as a root).

Geometric interpretation
- Eigenvectors indicate directions in V that T leaves invariant as lines: T sends each eigenvector v to a scalar multiple of itself, so the line spanned by v is mapped into itself.
- Eigenvalues are the scale factors (and orientation effects) along those invariant directions:
  - If λ > 1, T stretches vectors on that line.
  - If 0 < λ < 1, T contracts them.
  - If λ = 0, T collapses the entire eigenline to the zero vector (the operator is not injective).
  - If λ < 0, T flips the direction and scales by |λ|.
- When no real eigenvalue exists (e.g., a pure rotation in R^2), there is no real direction that is merely scaled; the action is genuinely rotational rather than collinear scaling.
- Eigenvectors thus identify the “principal” directions of T; decomposing V into invariant subspaces spanned by eigenvectors (when possible) reveals how T acts simply by scaling on those subspaces.

Geometric multiplicity and its relation to algebraic multiplicity

Definition
- The geometric multiplicity of an eigenvalue λ of a linear operator T on a finite-dimensional vector space V is the dimension of the eigenspace for λ, i.e. geometric multiplicity(λ) = dim ker(T − λI).

Key inequality (geometric ≤ algebraic)
- If λ is an eigenvalue of T, its geometric multiplicity is at least 1 and never exceeds its algebraic multiplicity (the multiplicity of λ as a root of the characteristic polynomial). In symbols:
  1 ≤ dim ker(T − λI) ≤ algebraic multiplicity of λ.

Proof (dimension/Null space argument)
1. Let n = dim V and set k = dim ker(T − λI) (the geometric multiplicity). Choose a basis v1, …, vk of ker(T − λI) and extend it to a basis v1, …, vk, w1, …, w_{n−k} of V.
2. With respect to this basis the matrix of the operator T − λI has the form
   [ 0  * ]
   [ 0  B ]
   where the first k columns are zero (because (T − λI)vj = 0 for j = 1,…,k). The block B is an (n−k)×(n−k) matrix.
3. The characteristic polynomial of T − λI is det((T − λI) − tI). Because the matrix has the k zero columns in its upper-left block, this polynomial is divisible by t^k. Equivalently, t = 0 is a root of multiplicity at least k of the characteristic polynomial of T − λI.
4. Translating back to T, this says that (λ) is a root of the characteristic polynomial of T of multiplicity at least k. Thus the algebraic multiplicity of λ is ≥ k = geometric multiplicity.

Remarks tying null space and range
- The dimension of the eigenspace is the nullity of T − λI, and nullity + rank = n (the Rank–Nullity Theorem). The fact that nullity(T − λI) appears as the exponent of t dividing the characteristic polynomial follows from the block-zero structure obtained by choosing a basis containing an eigenspace basis. This is the central dimension/counting mechanism that yields the geometric ≤ algebraic inequality.
- In general the geometric multiplicity can be smaller than the algebraic multiplicity; equality holds exactly when the operator is diagonalizable (i.e., V is the direct sum of the eigenspaces).

Eigenvalues of triangular matrices

Key fact and proof idea
- If A is upper or lower triangular, then A − λI is triangular for every scalar λ. The determinant of a triangular matrix equals the product of its diagonal entries.
- Therefore det(A − λI) = ∏i (aii − λ). The characteristic polynomial factors as (a11 − λ)(a22 − λ)···(ann − λ). The eigenvalues are exactly the roots of this polynomial, so they are the diagonal entries a11, a22, …, ann (counted with algebraic multiplicity).
- Intuition: triangular form shows that no new polynomial factors appear off the diagonal — the diagonal entries already give the full characteristic polynomial.

Consequences to remember
- You do not need to expand a determinant or compute cofactors for triangular matrices: read off the diagonal.
- Multiplicity: if a diagonal value c appears k times on the diagonal, then c is an eigenvalue of algebraic multiplicity k.
- This holds over any field (real or complex) because the determinant-product property and triangularity are algebraic.

Examples

1) Upper-triangular 3×3
A = [ 2  1  0
      0  3  4
      0  0 −1 ]
A − λI is upper triangular with diagonal entries 2−λ, 3−λ, −1−λ, so
char poly = (2−λ)(3−λ)(−1−λ).
Eigenvalues: 2, 3, −1 (each with multiplicity 1).

2) Repeated diagonal value
B = [ 5  2  1
      0  5  0
      0  0  7 ]
char poly = (5−λ)(5−λ)(7−λ) = (5−λ)^2(7−λ).
Eigenvalues: 5 (algebraic multiplicity 2) and 7 (multiplicity 1). Whether 5 is geometrically multiplicity 1 or 2 depends on the eigenspace; triangular form does not by itself guarantee diagonalizability.

3) Lower-triangular with complex/negative entries
C = [ −1  0   0
       6  4   0
       3  2   4 ]
Diagonal entries: −1, 4, 4, so char poly = (−1−λ)(4−λ)(4−λ). Eigenvalues: −1 (mult. 1) and 4 (mult. 2).

Quick checklist to find eigenvalues of a triangular matrix
1. Read off the diagonal entries a11, …, ann.
2. List them as eigenvalues, recording multiplicities equal to how many times each appears on the diagonal.
3. If you need eigenvectors or to check diagonalizability, solve (A − λI)x = 0 for each eigenvalue (triangularity makes back-substitution straightforward).

That is why triangular matrices let you find eigenvalues efficiently: the characteristic polynomial is the simple product of diagonal linear factors.

Section 31 — Inner Product (definition and basic properties)

Definition.
Let V be a vector space over the field F, where F = R or C. An inner product on V is a function
⟨·,·⟩ : V × V → F
that assigns to each ordered pair (u,v) a scalar ⟨u,v⟩ and satisfies the following axioms for all u,v,w ∈ V and all scalars α ∈ F.

Axioms.
1. Conjugate symmetry:
   ⟨u,v⟩ = overline{⟨v,u⟩}.
   (In the real case this becomes symmetry ⟨u,v⟩ = ⟨v,u⟩.)

2. Linearity in the first argument:
   ⟨αu + v, w⟩ = α⟨u,w⟩ + ⟨v,w⟩.
   (Equivalently, conjugate-linearity holds in the second argument: ⟨u, αv + w⟩ = overline{α}⟨u,v⟩ + ⟨u,w⟩.)

3. Positive-definiteness:
   ⟨v,v⟩ ≥ 0 for all v, and ⟨v,v⟩ = 0 iff v = 0.

Remarks / immediate consequences.
- For all v ∈ V, ⟨v,v⟩ is a real nonnegative number (by conjugate symmetry).
- The inner product induces a norm via ‖v‖ = sqrt(⟨v,v⟩).
- Standard inequalities and identities (e.g., Cauchy–Schwarz, triangle inequality for the induced norm, polarization identities) follow from these axioms.

Standard examples (especially on F^n).
1. Euclidean inner product on R^n:
   For x = (x1,...,xn), y = (y1,...,yn) ∈ R^n,
   ⟨x,y⟩ = x1y1 + x2y2 + ... + xnyn.
   This is symmetric, bilinear, and positive definite.

2. Standard inner product on C^n (Axler convention — linear in the first argument):
   For x = (x1,...,xn), y = (y1,...,yn) ∈ C^n,
   ⟨x,y⟩ = x1 overline{y1} + x2 overline{y2} + ... + xn overline{yn}.
   This satisfies conjugate symmetry ⟨x,y⟩ = overline{⟨y,x⟩}, is linear in the first slot, conjugate-linear in the second, and positive definite.

   (Note: some texts place the conjugation on the first coordinate instead; the two conventions are equivalent up to taking complex conjugates of the inner product.)

3. L2 inner product on function spaces:
   Let V be the space of complex-valued square-integrable functions on an interval [a,b]. Define
   ⟨f,g⟩ = ∫_a^b f(t) overline{g(t)} dt.
   This is conjugate-symmetric, linear in the first argument, and positive definite (modulo identification of functions equal almost everywhere).

4. Weighted inner product on F^n:
   Given a positive-definite Hermitian matrix A (n×n), define for x,y ∈ F^n
   ⟨x,y⟩_A = x^* A y
   (where x^* is the conjugate-transpose of x). This is an inner product; when A = I one recovers the standard inner product.

These capture the typical examples used throughout finite- and infinite-dimensional inner product spaces.

Norm and distance induced by an inner product

Let V be an inner-product space over R or C with inner product ⟨·,·⟩. Define the norm (length) of v ∈ V by
||v|| := sqrt(⟨v,v⟩).
Define the distance between v,w ∈ V by
d(v,w) := ||v − w||.

Key properties and inequalities

1. Positivity and homogeneity
- ||v|| ≥ 0 for all v, and ||v|| = 0 iff v = 0 (positivity/definiteness).
- For scalar α, ||αv|| = |α| ||v|| (absolute homogeneity).

These follow immediately from properties of the inner product.

2. Cauchy–Schwarz inequality
For all v,w ∈ V,
|⟨v,w⟩| ≤ ||v|| · ||w||.
Proof sketch: If w = 0 the inequality is trivial. If w ≠ 0, consider the function of scalar t ∈ F (F = R or C)
f(t) = ⟨v − tw, v − tw⟩ ≥ 0 for all t.
Choose t = ⟨v,w⟩/⟨w,w⟩ (or minimize f(t)); expanding and using nonnegativity yields
0 ≤ ||v||^2 − |⟨v,w⟩|^2 / ||w||^2,
which rearranges to |⟨v,w⟩| ≤ ||v|| ||w||.

Equality holds iff v and w are linearly dependent (over R or C): v = 0 or v = λw for some scalar λ.

3. Triangle inequality
For all v,w ∈ V,
||v + w|| ≤ ||v|| + ||w||.
Proof sketch: Expand the square and apply Cauchy–Schwarz:
||v + w||^2 = ||v||^2 + 2 Re⟨v,w⟩ + ||w||^2 ≤ ||v||^2 + 2|⟨v,w⟩| + ||w||^2
≤ ||v||^2 + 2||v|| ||w|| + ||w||^2 = (||v|| + ||w||)^2.
Taking square roots gives the triangle inequality.

Equality in the triangle inequality occurs exactly when v and w are positively collinear (v = λw with λ ≥ 0 in the real case; in the complex case the phase must align so Re⟨v,w⟩ = |⟨v,w⟩|).

4. Distance properties
d(v,w) = ||v − w|| defines a metric on V:
- d(v,w) ≥ 0, and d(v,w) = 0 iff v = w.
- d(v,w) = d(w,v).
- Triangle inequality: d(v,z) ≤ d(v,w) + d(w,z), which follows from the triangle inequality for the norm.

Remarks
- The norm and distance above are the canonical ones induced by the inner product; many important inequalities and geometric notions in inner-product spaces (orthogonality, projections, angles) depend on these definitions and on Cauchy–Schwarz and the triangle inequality.

Orthogonality, Orthonormal Sets, and Orthonormal Bases

Definitions
- Two vectors u and v in an inner-product space V are orthogonal if ⟨u, v⟩ = 0. We write u ⟂ v.
- A set S of vectors is orthogonal if every distinct pair of vectors in S is orthogonal.
- An orthonormal set is an orthogonal set whose vectors all have unit length: for each e in S, ||e|| = 1 (equivalently ⟨e,e⟩ = 1).
- An orthonormal basis of V is a set that is both orthonormal and a basis of V (i.e., it is orthonormal and spans V).

Basic consequences

1) Linear independence
- Any orthogonal set of nonzero vectors is linearly independent.  
  Sketch: If a1v1 + ··· + ank vk = 0 and you take inner product with vj, orthogonality kills all other terms, leaving aj||vj||^2 = 0, so aj = 0.

2) Coordinates with respect to an orthonormal set or basis
- If {e1, …, en} is an orthonormal set and v lies in span{e1,…,en}, then the coefficients in the unique linear combination
  v = c1 e1 + ··· + cn en
  are given by
  cj = ⟨v, ej⟩ for j = 1,…,n.
  Thus inner products with the basis vectors yield the coordinates directly.

- In particular, if {e1, …, en} is an orthonormal basis of V, every v in V has coordinates (⟨v,e1⟩, …, ⟨v,en⟩).

3) Lengths and energy (Pythagorean/Parseval)
- For an orthonormal set {e1,…,en} and v = ∑ cj ej in their span,
  ||v||^2 = |c1|^2 + ··· + |cn|^2.
  Using the coordinate formula, for v in the span,
  ||v||^2 = ∑ |⟨v, ej⟩|^2.
- If {e1,…,en} is an orthonormal basis of V, this identity holds for every v in V (often called Parseval's identity).

4) Orthogonal projection (useful for computing coordinates when the set is a basis)
- If {e1,…,en} is an orthonormal set, the orthogonal projection of v onto span{e1,…,en} is
  Proj(v) = ∑ ⟨v, ej⟩ ej.
  When the set is an orthonormal basis of V, Proj(v) = v, and the sum gives the expansion of v.

Remarks
- Orthonormal bases make coordinate computations and norm computations immediate via inner products, and they simplify many proofs and algorithms (e.g., Gram–Schmidt builds orthonormal sets from independent sets).

Gram–Schmidt Orthonormalization

What it requires
- Input: a finite linearly independent list (v1, v2, ..., vn) in an inner-product space V. In particular, it may be a basis of a subspace of V.
- Inner product: the procedure uses the inner product on V to form projections and compute norms.

What it produces
- Output: an orthonormal list (e1, e2, ..., en) with the same span as the input list; in particular, if the input is a basis of some subspace W, the output is an orthonormal basis of W.

The procedure (finite case)
1. Set u1 = v1.
2. Normalize: e1 = u1 / ||u1||.
3. For k = 2, ..., n do:
   - Remove components of vk in the directions already produced:
     uk = vk − sum_{j=1}^{k−1} <vk, ej> ej.
   - Normalize: ek = uk / ||uk||.
(Here <·,·> denotes the inner product and ||·|| the associated norm. Each uk is nonzero because the original list is linearly independent.)

Equivalent projection formula
- uk is vk with the orthogonal projection of vk onto span{e1,...,e_{k−1}} subtracted:
  uk = vk − Proj_{span{e1,...,e_{k−1}}}(vk),
  where Proj_{span{e1,...,e_{k−1}}}(x) = sum_{j=1}^{k−1} <x, ej> ej.

Key properties and remarks
- Orthonormality: by construction, the ej are unit vectors and mutually orthogonal: <ei, ej> = 0 for i ≠ j and ||ej|| = 1.
- Span preservation: for each k, span{e1,...,ek} = span{v1,...,vk}. Hence span{e1,...,en} = span{v1,...,vn}.
- Order matters: different orders of the input list generally give different orthonormal lists.
- Works in any finite-dimensional inner-product space (or for any finite linearly independent list in an inner-product space).
- If some vk becomes orthogonal to previous e's and hence uk = 0, that indicates linear dependence among the inputs; Gram–Schmidt requires a linearly independent input list (or else it produces fewer than n orthonormal vectors corresponding to a basis of the span).

Use
- Produce orthonormal bases for subspaces, simplify coordinate computations, and form orthogonal projections and orthogonal decompositions.

Orthogonal complement
- Let V be an inner-product space and U a subspace of V. The orthogonal complement of U is
  U^⊥ = { w in V : <w, u> = 0 for all u in U }.
  U^⊥ is a subspace of V consisting of all vectors orthogonal to every vector of U.

Orthogonal projection and decomposition theorem
- Suppose V is a finite-dimensional inner-product space and U a subspace of V. Then every vector v in V can be written uniquely as
  v = u + w
  with u in U and w in U^⊥. The vector u is called the orthogonal projection of v onto U and is usually denoted Proj_U(v) (or P_U v); w = v − Proj_U(v) is the orthogonal remainder.
- Equivalently: V = U ⊕ U^⊥ (direct sum).

Characterizations and properties
- Orthogonality characterization: u = Proj_U(v) is the unique vector in U such that v − u is orthogonal to every vector of U.
- Minimization/closest-point property: Proj_U(v) is the unique vector in U minimizing the distance to v:
  ||v − Proj_U(v)|| = min{ ||v − u'|| : u' in U }.
  In particular, for every u' in U,
  ||v − u'||^2 = ||v − Proj_U(v)||^2 + ||Proj_U(v) − u'||^2,
  so equality holds iff u' = Proj_U(v).
- If {e1,...,ek} is an orthonormal basis of U, then
  Proj_U(v) = sum_{j=1}^k <v, ej> ej.
- The projection map P_U : V → U given by P_U(v) = Proj_U(v) is linear, idempotent (P_U^2 = P_U), has range P_U(V) = U and kernel Ker(P_U) = U^⊥.

These statements give both the algebraic decomposition of vectors into a component in U and a component orthogonal to U and the geometric fact that the projection is the closest point of U to v.

Riesz Representation (finite-dimensional inner product spaces)

Theorem (Riesz). Let V be a finite-dimensional inner product space over F (R or C). For every linear functional φ ∈ V* there exists a unique vector y ∈ V such that
φ(v) = ⟨v, y⟩ for all v ∈ V.
Thus the map V → V*, y ↦ φ_y defined by φ_y(v) = ⟨v,y⟩ is a vector-space isomorphism (over R). Over C this map is conjugate-linear (i.e. linear if the inner product is linear in the second slot and conjugate-linear if it is linear in the first).

Proof sketch. Pick an orthonormal basis {e1,...,en} of V. Write an arbitrary v ∈ V as v = Σ ⟨v, ei⟩ ei. For φ ∈ V*,
φ(v) = Σ ⟨v, ei⟩ φ(ei) = ⟨v, Σ conj(φ(ei)) ei⟩,
so taking y = Σ conj(φ(ei)) ei gives φ(v) = ⟨v,y⟩ for all v. Uniqueness: if ⟨v,y⟩ = 0 for all v then y = 0, so the representing vector is unique.

Dependence on orthonormal bases. If {ei} is an orthonormal basis, the coordinates of the representing vector y are the conjugates of the functional’s values on the basis:
y = Σ conj(φ(ei)) ei,
so φ(ei) = ⟨ei, y⟩. In matrix/coordinate terms, if v has coordinate column vector [v] and y has coordinate column [y] relative to the same orthonormal basis, then the functional φ corresponds to the row vector [φ] = [y]* (the conjugate-transpose of [y]) and φ(v) = [φ][v] = [y]*[v].

Remarks
- The theorem gives a concrete identification of V and V*: every linear functional is “inner product with a unique vector.”
- The appearance of complex conjugation in coordinates is why the isomorphism is conjugate-linear over C (the coordinates of y are conj(φ(ei))).

Adjoint operator — definition and key facts

Definition
- Let V be an inner-product space (over R or C) and T: V → V linear. The adjoint T* is the (unique, when it exists) linear operator on V such that
  <T v, w> = <v, T* w> for all v, w ∈ V.
- Characterizing property: T* is exactly the operator that moves T from the first slot of the inner product to the second while conjugating scalars as required by the inner product.

Existence and uniqueness
- In finite-dimensional inner-product spaces (the setting in Axler), an adjoint always exists and is unique.

Core algebraic identities
- (S + T)* = S* + T*
- (α T)* = overline{α} T*  for scalar α
- (S T)* = T* S*
- (T*)* = T
- T is self-adjoint (Hermitian) iff T* = T.
- T is normal iff T T* = T* T.
- ker(T*) = (range T)⊥, and (in finite dimensions) range(T*) = (ker T)⊥.
- ||T|| = ||T*|| (operator norm equality).

Computing T* from inner-product data
- To find T* directly from the defining relation, solve the linear equations given by
  <T v, w> = <v, x> for unknown x depending linearly on w; then x = T* w.
  Concretely: for each fixed w, the linear functional v ↦ <T v, w> equals v ↦ <v, T* w>, so identify T* w by Riesz representation.

Matrix formulas (orthonormal basis)
- If (e1,...,en) is an orthonormal basis and A is the matrix of T relative to that basis (so Tv has coordinate vector A [v]), then the matrix of T* relative to the same orthonormal basis is A* = conjugate-transpose of A:
  [T*] = A* = overline{A}^T.
- Equivalently, columns of A* are the coordinate vectors of T* applied to basis vectors.

Matrix formula (non-orthonormal basis)
- If the basis is not orthonormal and G is the Gram matrix G_{ij} = <ei, ej>, and A is the matrix of T in that basis, then the matrix of T* is
  [T*] = G^{-1} A* G,
  where A* denotes the conjugate-transpose of A (taken as usual) and G is invertible in finite dimensions.

Remarks
- The adjoint converts algebraic operator relations to inner-product identities and is fundamental for notions like orthogonal projection, normal and self-adjoint operators, and unitary operators (T* = T^{-1} for unitary T).

Normal operators

Definition
- Let V be an inner-product space over F (R or C). An operator T in L(V) is called normal if it commutes with its adjoint:
  TT* = T*T.

Immediate equivalent characterization
- T is normal iff for every v in V, ||T v|| = ||T* v||.
  Sketch: ||T v||^2 = <T v, T v> = <T* T v, v> and ||T* v||^2 = <T T* v, v>. If TT* = T*T these are equal for all v, and conversely equality of these quadratic forms for all v implies TT* = T*T.

Basic consequences emphasized in Axler

1. Eigenvectors and eigenvalues
- If v ≠ 0 is an eigenvector of a normal operator T with eigenvalue λ (T v = λ v), then v is also an eigenvector of T* with eigenvalue conjugate(λ):
  T* v = conjugate(λ) v.
  Proof: From T v = λ v we have <T v, v> = λ <v, v>. But <T v, v> = <v, T* v>, so <v, T* v> = λ <v, v>. Taking complex conjugates shows <T* v, v> = conjugate(λ) <v, v>, and comparing gives T* v = conjugate(λ) v because v ≠ 0 and normality implies compatibility of these relations (one can also apply TT* = T*T directly to deduce this).

- Eigenvectors corresponding to distinct eigenvalues are orthogonal.
  Proof: Let T v = λ v and T w = μ w with λ ≠ μ. Compute
  λ <v, w> = <T v, w> = <v, T* w> = <v, conjugate(μ) w> = μ <v, w>.
  Since λ ≠ μ this forces <v, w> = 0.

2. Invariance of orthogonal complements of eigenspaces
- If U = ker(T − λI) is an eigenspace of a normal operator T, then U⊥ is invariant under T (and under T*). 
  Reason: If w ∈ U⊥ and u ∈ U, then 0 = <w, u> = <T w, u> − <w, T* u> and using T* u = conjugate(λ) u one sees <T w, u> = conjugate(λ) <w, u> = 0, so T w ∈ U⊥.

3. Orthogonal decomposition into eigenspaces (finite-dimensional, partial)
- For a normal T on a finite-dimensional inner-product space, distinct eigenspaces are mutually orthogonal, so the direct sum of eigenspaces is an orthogonal sum. This is the key structural feature used later to prove full diagonalizability in the complex case.

Remarks and special cases
- Self-adjoint operators (T = T*) and unitary operators (T* = T^{-1}) are normal, so all the orthogonality properties above apply to them.
- Over C, the full spectral theorem (proved later) strengthens these consequences: a normal operator is unitarily diagonalizable — there exists an orthonormal basis of V consisting of eigenvectors of T. In this section we only note orthogonality of eigenspaces and related invariance properties; the complete diagonalization in the complex case is deferred to the later spectral theorem.

Orthogonal (real) and unitary (complex) operators — definitions and key facts

Definition
- Let V be a finite-dimensional inner-product space.
  - If V is over R, a linear operator T: V → V is called orthogonal.
  - If V is over C, T is called unitary.
- Both terms mean the same thing conceptually: T preserves the inner product (and hence lengths and angles):
  ⟨T x, T y⟩ = ⟨x, y⟩ for all x, y ∈ V.

Equivalent characterizations (all equivalent in finite dimensions)
- T preserves inner products: ⟨T x, T y⟩ = ⟨x, y⟩ for all x, y.
- T preserves norms: ‖T x‖ = ‖x‖ for all x (isometry).
- T preserves orthogonality: x ⟂ y ⇐⇒ T x ⟂ T y.
- T* T = I (so T* = T^{-1}).
- T is surjective (and hence invertible); equivalently T is an isometric isomorphism.
- With respect to any orthonormal basis, the matrix of T has orthonormal columns (and rows); that matrix is called orthogonal (real) or unitary (complex).

Immediate consequences / structural properties
- T is normal: T T* = T* T (because T* = T^{-1}), so unitary/orthogonal operators are a special case of normal operators.
- Eigenvalues lie on the unit circle: if T v = λ v with v ≠ 0 then |λ| = 1.
- Determinant has unit modulus: |det T| = 1 (for real orthogonal matrices det = ±1).
- Composition and adjoint:
  - The product of orthogonal/unitary operators is orthogonal/unitary.
  - The adjoint (T*) is orthogonal/unitary and equals the inverse of T.
- Orthogonal/unitary operators map orthonormal bases to orthonormal bases. Conversely, any linear map sending one orthonormal basis to another is orthogonal/unitary.
- Diagonalization:
  - Over C, a unitary operator is normal and hence unitarily diagonalizable: there exists an orthonormal basis of eigenvectors, and the matrix is diagonal with entries of modulus 1.
  - Over R, an orthogonal operator need not be diagonalizable over R; after extending scalars to C it is diagonalizable with eigenvalues on the unit circle. Over R an orthogonal operator can be put (relative to some orthonormal basis) into block-diagonal form with 1×1 blocks ±1 and 2×2 rotation blocks (rotations in planes).
- Stability of inner-product structure: unitary/orthogonal operators are exactly the linear isometries of the inner-product space, so they preserve all metric and angle information.

Useful short identities
- T is unitary/orthogonal ⇐⇒ T* = T^{-1} ⇐⇒ T* T = I ⇐⇒ T T* = I.
- For matrix A relative to an orthonormal basis: A* A = I (A* = transpose for real case, conjugate transpose for complex case).

These are the defining properties and the main structural consequences you should keep in mind when working with orthogonal and unitary operators.

Section 40 — Self‑Adjoint (Hermitian) Operators

Definition
- Let V be a finite-dimensional inner product space (real or complex). A linear operator T: V → V is self‑adjoint (Hermitian) if T* = T, i.e. for all u,v in V,
  <T u, v> = <u, T v>.

Basic spectral properties (statements used later)
1. Real eigenvalues
   - If T is self‑adjoint and λ is an eigenvalue of T, then λ is real.

2. Orthogonality of eigenvectors
   - If T is self‑adjoint and u and v are eigenvectors corresponding to distinct eigenvalues λ and μ (λ ≠ μ), then u and v are orthogonal: <u, v> = 0.

3. Existence of an orthonormal eigenbasis (Spectral Theorem, finite‑dimensional)
   - For a self‑adjoint operator T on a finite‑dimensional inner product space V, there exists an orthonormal basis of V consisting of eigenvectors of T. Equivalently, T is diagonalizable by a unitary (complex) or orthogonal (real) change of basis, and all diagonal entries (the eigenvalues) are real.

4. Multiplicity and invariant subspaces
   - For each eigenvalue λ of a self‑adjoint operator T, the eigenspace E(λ) = {v : T v = λ v} is the orthogonal complement of the direct sum of the other eigenspaces. In particular, geometric multiplicity equals algebraic multiplicity (no nontrivial Jordan blocks).

5. Functional calculus and polynomials
   - Any polynomial p(T) of a self‑adjoint operator is self‑adjoint when p has real coefficients. Diagonalization gives p(T) acts by p(λ) on an eigenvector of eigenvalue λ.

Useful corollaries and characterizations
- Norm and eigenvalues: For a self‑adjoint T, ||T|| = max{|λ| : λ is an eigenvalue of T} where the maximum is taken over the real spectrum.
- Positivity: T is positive semidefinite (i.e., <T v, v> ≥ 0 for all v) iff all eigenvalues of T are ≥ 0. T is positive definite iff all eigenvalues are > 0.
- Characterization via quadratic form: For self‑adjoint T, the quadratic form q(v) = <T v, v> is real-valued, and diagonalization expresses q as a weighted sum of squares with weights the eigenvalues.

Main theorems (formal statements)
- Theorem (Eigenvalues are real). If T = T*, then every eigenvalue λ ∈ C of T satisfies λ ∈ R.
- Theorem (Orthogonality of eigenvectors). If T = T* and Tu = λu, Tv = μv with λ ≠ μ, then <u, v> = 0.
- Spectral Theorem (finite-dimensional, self‑adjoint case). If V is finite-dimensional and T = T*, then there exists an orthonormal basis of V made of eigenvectors of T. Consequently, T is diagonalizable by a unitary (orthogonal in the real case) operator and its spectrum is real.
- Corollary (No nontrivial Jordan blocks). A self‑adjoint operator on a finite-dimensional space has a diagonal matrix representation (no Jordan blocks of size >1) in some orthonormal basis.

Remarks for use
- These properties are fundamental and are used repeatedly: diagonalization simplifies computations, orthogonality gives convenient decompositions, and the reality of the spectrum ties operator behavior to real quantities (e.g., energies in physical applications).
- In applications one often first shows T is self‑adjoint, then invokes the spectral theorem to pick an orthonormal eigenbasis and reduce problems about T to coordinatewise (scalar) problems on the eigenvalues.

Spectral Theorem for Self-Adjoint Operators

Statement used in the text
- Let V be a finite-dimensional inner-product space over R or C, and let T ∈ L(V) be self-adjoint (i.e. ⟨T v, w⟩ = ⟨v, T w⟩ for all v,w ∈ V). Then V has an orthonormal basis consisting of eigenvectors of T.
- Equivalently: there exists an orthonormal basis of V relative to which the matrix of T is diagonal, and all diagonal entries (the eigenvalues) are real.

How this is used to analyze operators
- Diagonalization: Representing T in an orthonormal eigenbasis reduces every problem about T to a problem about a diagonal matrix. Calculations of T^k, polynomials in T, and functions of T become entrywise operations on the eigenvalues.
- Spectrum and norm: The eigenvalues are exactly the spectrum of T and are real; the operator norm satisfies ||T|| = max{|λ| : λ an eigenvalue of T} when V is finite-dimensional.
- Orthogonal decomposition: V decomposes as an orthogonal direct sum of eigenspaces of T. This makes it straightforward to study invariant subspaces, projections, and to solve equations like T v = w by handling each eigenspace separately.
- Positivity and sign: Self-adjoint operators are positive (⟨T v,v⟩ ≥ 0 for all v) iff all eigenvalues are nonnegative; one can test positivity by checking eigenvalues in the diagonal form.
- Spectral projections and functional calculus: The diagonal form yields orthogonal projections onto eigenspaces and allows defining f(T) for functions f by applying f to eigenvalues (useful for exponentials, square roots, etc.).
- Classification and simplification: Many questions about normality, commutativity, and simultaneous diagonalization reduce to comparing eigenbases; commuting self-adjoint operators that are diagonalizable in a common orthonormal basis are particularly simple to handle.

Practical workflow when given a self-adjoint T
1. Find eigenvalues and orthogonal eigenvectors.
2. Orthonormalize eigenvectors to obtain an orthonormal eigenbasis.
3. Work with the diagonal matrix of eigenvalues to compute powers, norms, projections, and functionals of T, or to decompose V into orthogonal eigenspaces for further analysis.

Positive (semidefinite) operators and square roots

Definition
- Let V be a finite-dimensional inner-product space (real or complex). A linear operator T on V is called positive (or positive semidefinite) if T is self-adjoint and
  ⟨T v, v⟩ ≥ 0 for all v ∈ V.
- We write 0 ≤ T to mean T is positive.

Immediate consequences and characterizations
- Self-adjointness is part of the definition. Conversely, if T is self-adjoint then T is positive iff all eigenvalues of T are ≥ 0 (spectral characterization).
- Spectral theorem formulation: if T is positive, there is an orthonormal basis of eigenvectors of T and every eigenvalue λ satisfies λ ≥ 0. Hence T is diagonalizable with a diagonal whose entries are nonnegative.
- Quadratic-form test: T is positive ⇔ the quadratic form q(v)=⟨T v,v⟩ is nonnegative for all v.

Ordering of operators
- Define an order on self-adjoint operators by A ≤ B ⇔ B − A is positive.
- Basic facts about this order:
  - If 0 ≤ A ≤ B then ||A|| ≤ ||B|| (because the spectral radius / largest eigenvalue of A is ≤ that of B).
  - If 0 ≤ A and C is any operator, then C*AC is positive (congruence preserves positivity).
  - If 0 ≤ A ≤ B and C commutes with A and B, many spectral constructions applied to A and B respect the order (see functional consequences below).
  - Positivity is preserved under limits: a norm limit of positive operators is positive.

Functional consequences
- Polynomials (and continuous functional calculus): if p is a real polynomial with p(x) ≥ 0 for all x in the spectrum of a self-adjoint T, then p(T) is positive. In particular, if T is positive then T^k is positive for every positive integer k.
- If T is positive and invertible (i.e., all eigenvalues > 0) then T^−1 is positive.
- If 0 ≤ A ≤ B then for any nondecreasing continuous function f defined on an interval containing the spectra, f(A) ≤ f(B). In particular, if 0 ≤ A ≤ B then √A ≤ √B (monotonicity of square root).
- If T is positive, the kernel and range satisfy relations coming from spectral decomposition; e.g. ker T = span of eigenvectors for eigenvalue 0.

Factorizations
- Every positive operator T can be written as T = R*R for some operator R (take R = √T below). Conversely, any operator of the form R*R is positive. Thus positivity can be seen as “Gram-type” factorization.

Existence and uniqueness of positive square roots
- Existence: If T is positive then there exists a unique positive operator S such that S^2 = T. Construction:
  - Spectral approach: diagonalize T with an orthonormal eigenbasis. If T has eigenpairs (v_j, λ_j) with λ_j ≥ 0, define S on each eigenvector by S v_j = √λ_j v_j and extend linearly. Then S is self-adjoint, positive, and S^2 = T.
  - Functional calculus: apply the continuous function f(x)=√x to T.
- Uniqueness: If S is self-adjoint and positive with S^2 = T, then S is the operator constructed above, so the positive square root is unique. More concretely, if S1 and S2 are positive and S1^2 = S2^2, then S1 = S2.
- Additional properties of the square root:
  - If T is invertible positive, then √T is invertible positive and (√T)^−1 = √(T^−1).
  - If A commutes with T (i.e., AT = TA) and A is self-adjoint, then A commutes with √T as well. In particular, any operator that commutes with T commutes with every polynomial (and with continuous functions) of T.
  - If 0 ≤ A ≤ B then A = (√A)^2 and √A ≤ √B.
  - If T = R*R, then √T commutes with any operator that commutes with R*R; in finite dimensions the square root is a polynomial (continuous function) in T, so it shares the same commuting algebra.

Useful inequalities and remarks
- If T is positive then ⟨T v, w⟩ = ⟨√T v, √T w⟩, so the quadratic form factors through √T.
- Product of positives need not be positive: if A and B are positive, AB need not be self-adjoint and need not be positive. If A and B are positive and commute then AB is positive.
- Trace and determinant: for positive T, tr(T) ≥ 0 and det(T) ≥ 0 (det(T) = product of eigenvalues, nonnegative; strictly positive iff T is invertible).
- Norm characterization: for a self-adjoint operator A, A ≥ 0 iff ||I + tA|| ≥ 1 for all t ≥ 0 (an auxiliary test).

Proof sketch of uniqueness for the square root
- Suppose S is a positive operator with S^2 = T. Diagonalize T; on each eigenspace of T with eigenvalue λ, S must be a self-adjoint operator whose square is λ times identity on that eigenspace. Positivity forces S to act there by multiplication by √λ on each eigenvector, so S is determined uniquely on each eigenspace. Hence S is unique.

Takeaway
- Positive operators are exactly the self-adjoint operators whose spectra lie in [0, ∞). The spectral theorem (or functional calculus) is the principal tool: it yields existence and uniqueness of the positive square root and allows one to transfer scalar inequalities and monotonicity through functional calculus. The ordering A ≤ B (meaning B−A positive) behaves like the usual order on numbers when restricted to functions of a fixed self-adjoint operator, but one must be cautious about noncommutativity when comparing different operators.

Existence of eigenvalues over C

Theorem. Let V be a nonzero finite-dimensional complex vector space and T: V → V a linear operator. Then T has at least one eigenvalue.

Proof. Since V ≠ {0}, pick v ≠ 0. The vectors v, T v, T^2 v, …, T^n v (with n = dim V) are n+1 vectors in an n-dimensional space, so they are linearly dependent. Thus there exist complex scalars a0, a1, …, ak, not all zero, with
a0 v + a1 T v + … + ak T^k v = 0.
Equivalently, if p(z) = a0 + a1 z + … + ak z^k (a nonzero polynomial), then p(T)v = 0.

Because the field is C, p factors completely into linear factors:
p(z) = c (z − λ1)(z − λ2) … (z − λm)
with c ≠ 0 and λj ∈ C. Applying this factorization to operators gives
p(T) = c (T − λ1 I)(T − λ2 I) … (T − λm I),
so
c (T − λ1 I)(T − λ2 I) … (T − λm I) v = 0.

A product of linear maps sends v to 0, so some factor (T − λj I) fails to be injective on V (if each factor were injective their composition would be injective). Hence there exists a nonzero w ∈ V with (T − λj I)w = 0, i.e. T w = λj w. Thus λj is an eigenvalue of T.

Remark. The key use of C is that every nonconstant complex polynomial has a root, so any nonzero polynomial in T can be factored into linear factors; that factorization is what forces some (T − λI) to fail to be invertible, producing an eigenvector. This argument avoids determinants and uses only basic linear dependence and the fundamental algebraic fact that polynomials over C split into linear factors.

Schur Decomposition (Unitary Triangularization for Complex Operators)

Statement (Schur). Let V be a finite-dimensional complex inner-product space and let T : V → V be a linear operator. There exists an orthonormal basis of V in which the matrix of T is upper triangular. Equivalently, there is a unitary operator U (change-of-basis matrix) so that
U* T U = R
where R is upper triangular and the diagonal entries of R are the eigenvalues of T (counted with algebraic multiplicity).

Construction / proof sketch.
- Because the field is C, T has at least one eigenvalue λ. Pick a unit eigenvector v1 with T v1 = λ v1.
- Extend v1 to an orthonormal basis of V by choosing an orthonormal basis of the orthogonal complement (use Gram–Schmidt).
- With respect to the decomposition V = span{v1} ⊕ span{v1}⊥, the matrix of T has the block form
  [ λ  * ]
  [ 0  S ]
  where S is the compression of T to span{v1}⊥.
- Apply the same argument to S (induction on dimension) to produce an orthonormal basis of span{v1}⊥ making S upper triangular. Combining v1 with that basis yields an orthonormal basis of V in which T is upper triangular.
- Putting those orthonormal basis vectors as columns of a unitary matrix U gives U* T U = R.

Remarks about the diagonal and eigenvalues.
- The diagonal entries of the Schur form R are precisely the eigenvalues of T. In particular the spectrum of T appears on the diagonal (in some order).

Normal operators — unitary diagonalization.
- If T is normal (T*T = TT*), then any Schur triangular form R is itself normal (unitary similarity preserves normality). A normal upper-triangular matrix must be diagonal: for an upper-triangular R = (rij) normality forces all superdiagonal entries to be zero, so R is diagonal.
- Hence a normal operator T is unitarily diagonalizable: there exists a unitary U with U* T U = D diagonal. Equivalently, V has an orthonormal basis of eigenvectors of T.
- This is the usual spectral theorem for normal operators on finite-dimensional complex inner-product spaces.

Key consequences.
- Schur gives a convenient canonical form (upper triangular) for any complex operator via a unitary change of basis. For normal operators, the canonical form refines to a diagonal matrix, giving orthonormal eigenbases and unitary diagonalization.

Section: Spectral Theorem for Normal Operators (Complex Case)

Statement
- Let V be a finite-dimensional complex inner product space and let T ∈ L(V) be normal (i.e., TT* = T*T). Then there exists an orthonormal basis of V consisting of eigenvectors of T. Equivalently, T is diagonalizable by a unitary change of basis: with respect to some orthonormal basis, the matrix of T is diagonal with entries equal to the eigenvalues of T.

Key corollaries
- If A is an n×n complex matrix with A A* = A* A, then there exists a unitary matrix U such that U* A U is diagonal.
- Eigenvectors corresponding to distinct eigenvalues of a normal operator are orthogonal.
- T can be written as T = ∑_{j} λ_j P_j, where λ_j are the distinct eigenvalues and P_j are orthogonal projections onto the corresponding eigenspaces (spectral decomposition). The projections satisfy P_j P_k = 0 for j ≠ k and ∑_j P_j = I.

Proof idea (outline)
1. Use induction on dim V. If dim V = 1 the result is trivial.
2. For nonzero T, since the field is C, T has at least one eigenvalue λ and eigenvector v ≠ 0.
3. Show that the eigenspace E = {x : Tx = λx} is orthogonal to its orthogonal complement E⊥ and that E⊥ is invariant under T:
   - For w ∈ E⊥ and u ∈ E, ⟨T w, u⟩ = ⟨w, T* u⟩. But T* u = λ̄ u because T is normal and u is an eigenvector, so ⟨T w, u⟩ = λ̄ ⟨w, u⟩ = 0. Thus T w ∈ E⊥.
4. Restrict T to E⊥. By induction there is an orthonormal eigenbasis of E⊥. Adjoin an orthonormal basis of E to obtain an orthonormal eigenbasis of V.

How to apply the theorem (practical steps)
1. Verify normality: check T T* = T* T (or for a matrix A check A A* = A* A).
2. Find eigenvalues of T (roots of the characteristic polynomial over C).
3. For each eigenvalue λ, find its eigenspace and choose an orthonormal basis of that eigenspace (using Gram–Schmidt if needed).
4. Combine orthonormal bases for all eigenspaces to produce an orthonormal eigenbasis for V.
5. With respect to this basis, T is diagonal with the eigenvalues on the diagonal.

Example (matrix form)
- Let A = [[2, 1+i], [1-i, 3]]. Compute A A* and A* A to verify normality. Suppose A is normal. Find eigenvalues λ1, λ2 and corresponding orthonormal eigenvectors u1, u2. Then U = [u1 u2] is unitary and U* A U = diag(λ1, λ2).

Remarks and consequences
- Over C the spectral theorem guarantees a complete orthonormal eigenbasis for every normal operator; this fails over R in general (real symmetric matrices are a special real case that do diagonalize orthogonally, but real normal matrices need not have a full set of real eigenvectors).
- The spectral decomposition T = ∑ λ_j P_j gives an easy way to compute functions of T: for any polynomial p, p(T) = ∑ p(λ_j) P_j (and this extends to continuous functions on the spectrum via functional calculus).
- Normality is the exact condition that ensures diagonalizability by an orthonormal basis; self-adjoint, unitary, and normal operators are all covered by this theorem (self-adjoint ⇒ real eigenvalues; unitary ⇒ eigenvalues on the unit circle).

Exercises
- Verify the theorem on a concrete 3×3 normal matrix: check normality, compute eigenvalues and orthonormal eigenvectors, and find the unitary that diagonalizes it.
- Prove that if T is normal and λ is an eigenvalue of T, then T* has eigenvalue λ̄ with the same eigenspace.

Let T be a normal operator on a finite-dimensional complex inner-product space V. By the Spectral Theorem for normal operators, there is an orthonormal basis of V consisting of eigenvectors of T. Equivalently, there exists a unitary operator U and a diagonal matrix D (with diagonal entries λ1,...,λn) such that
T = U D U*,
where D = diag(λ1,...,λn) and U* is the adjoint (inverse) of U.

For any polynomial p(z) = a0 + a1 z + ... + ak z^k, define p(T) in the usual algebraic way by
p(T) = a0 I + a1 T + ... + ak T^k.
Using the diagonalization of T we can compute p(T) more directly:
T^m = U D^m U* for every m ≥ 0, so
p(T) = U p(D) U*,
where p(D) = diag(p(λ1),...,p(λn)). Thus p(T) is obtained by applying p to each diagonal entry of D and conjugating back by U.

Consequences:
- If v is an eigenvector of T with eigenvalue λ (Tv = λv), then p(T)v = p(λ) v. In particular, every eigenvector of T is an eigenvector of p(T) with eigenvalue p(λ).
- The spectrum (multiset of eigenvalues) of p(T) is {p(λ1),...,p(λn)} (counted with multiplicity).
- The definition p(T) = U p(D) U* is independent of the particular orthonormal eigenbasis chosen, so p(T) is well-defined.

Thus the polynomial functional calculus for a normal operator is implemented by diagonalizing T, applying the polynomial to the diagonal entries (the eigenvalues), and conjugating back.

Simultaneous Diagonalization of Commuting Normal Operators

Statement of the fact
- Let V be a finite-dimensional complex inner product space. If T1, ..., Tk are normal linear operators on V and they pairwise commute (Ti Tj = Tj Ti for all i,j), then there exists an orthonormal basis of V consisting of vectors that are simultaneous eigenvectors for all Ti. Equivalently, there is a single unitary change of basis that diagonalizes every Ti at once.

Why the hypotheses matter
- Normality: each Ti is unitarily diagonalizable on its own (spectral theorem). Normality guarantees an orthogonal decomposition of V into eigenspaces for Ti and that these eigenspaces are mutually orthogonal.
- Commutativity: if S and T commute and v is an eigenvector of S, then T preserves the eigenspace of S (because S(Tv)=T(Sv)=T(λv)=λ(Tv)). Thus commuting operators act invariantly on each eigenspace of the other operator(s). This invariance is the key mechanism allowing you to refine decompositions simultaneously.

Sketch of the proof idea (finite-dimensional, complex case)
1. Take one normal operator, say T1. By the spectral theorem, write V as an orthogonal direct sum of its eigenspaces V = ⊕λ Vλ.
2. Because each Ti commutes with T1, every Ti leaves each Vλ invariant. Restrict the remaining operators to each Vλ.
3. On each invariant subspace Vλ, apply the same procedure: choose one of the restricted normal operators, diagonalize it with an orthonormal basis of Vλ, and use commutativity again to see the rest preserve the new eigenspaces.
4. Inductively (or by simultaneously diagonalizing a commuting family of normal operators on each invariant block) you obtain an orthonormal basis of V made up of vectors that are eigenvectors for every Ti.

Remarks and variants
- Pair version: the same argument with k = 2 shows any two commuting normal operators have a common orthonormal eigenbasis.
- Necessity of commutativity: commuting is essential. Two normal operators that do not commute need not be simultaneously diagonalizable (counterexamples exist even for 2×2 normal matrices).
- Field: the result is standard over C (spectral theorem uses complex eigenvalues). Over R, extra care is required because real normal operators need not be diagonalizable over R into a basis of real eigenvectors.
- More general families: the result extends to any (possibly infinite) family of commuting normal operators on a finite-dimensional complex inner product space — the same invariance argument applied to joint spectral decomposition works.

Uses and consequences
- Simplifies simultaneous analysis: with a common orthonormal eigenbasis, each Ti acts by multiplying coordinates by scalars (its eigenvalues). Any polynomial (or continuous functional calculus) in the Ti acts coordinatewise on that basis.
- Commutative *-algebras of normal operators: a commuting family of normal operators generates a *-algebra that is simultaneously diagonalizable; this identifies the algebra with a space of diagonal matrices in the common eigenbasis.
- Applications: simplifies solving systems of linear operator equations where operators commute, computing joint spectra, and is fundamental in contexts such as quantum mechanics where commuting normal (self-adjoint) operators correspond to observables that can be measured simultaneously.
- Multiplicity handling: when eigenvalues have multiplicity >1, the commuting family further decomposes those eigenspaces into joint eigenspaces; if an eigenspace remains multidimensional for all operators, one chooses an orthonormal basis inside it of joint eigenvectors.

In short: on a finite-dimensional complex inner product space, pairwise commuting normal operators can be diagonalized simultaneously by a single orthonormal basis because commutativity forces invariance of eigenspaces produced by the spectral theorem, allowing an orthogonal refinement to a common eigenbasis.

Upper‑Triangular Form (Triangularization) of Operators

Goal. Given a linear operator T on a finite‑dimensional complex vector space V, produce a basis of V in which the matrix of T is upper‑triangular. Also identify what the diagonal entries of that triangular matrix mean.

Construction (inductive method).
1. Base fact. Over C every operator on a nonzero finite‑dimensional space has at least one eigenvalue and corresponding eigenvector. Let λ1 be an eigenvalue of T and choose a nonzero eigenvector v1 with T v1 = λ1 v1.

2. Extend to a basis. Extend {v1} to a basis {v1, v2, …, vn} of V. With respect to any such extension, the first column of the matrix of T has zeros below the first entry because T v1 = λ1 v1.

3. Reduce dimension. Let W be the subspace spanned by {v2, …, vn}. While W need not be T‑invariant, use the following standard step: consider the restriction of T to a complementary invariant chain. More concretely, modify the choice of v2,…,vn so that T maps span{v1, …, vk} into itself for each k (this is achieved inductively as below).

4. Inductive step. Assume we have chosen vectors v1,…,vk so that span{v1,…,vk} is T‑invariant and the matrix of T has zeros below the diagonal in the first k columns. If k = n we are done. Otherwise, consider the induced operator on the quotient space V / span{v1,…,vk}. This quotient has smaller positive dimension and so has an eigenvector class; lift that representative to a vector vk+1 in V. By construction span{v1,…,vk, vk+1} is T‑invariant and the matrix gains a new column with zeros below the (k+1)st diagonal entry. Continue until k = n.

5. Result. The final basis {v1,…,vn} satisfies T(vj) ∈ span{v1,…,vj} for each j, so the matrix of T with respect to this basis is upper‑triangular.

What the diagonal entries represent.
- Each diagonal entry in the resulting upper‑triangular matrix is an eigenvalue of T: the jth diagonal entry is the scalar by which T acts on the one‑dimensional quotient span{v1,…,vj}/span{v1,…,vj−1}, hence is an eigenvalue of the induced map and thus of T.
- Equivalently, the diagonal entries are exactly the eigenvalues of T, listed with multiplicity (they are the roots of the characteristic polynomial and their product equals det(T)).

Remarks.
- The construction relies on working over C so that eigenvalues always exist. Over other fields triangularization may fail if T has no eigenvalues in the field.
- The procedure can be viewed as building a flag of T‑invariant subspaces 0 ⊂ V1 ⊂ V2 ⊂ … ⊂ Vn = V with dim Vj = j; choosing basis vectors for successive one‑dimensional quotients yields the upper‑triangular form.

Section: Multilinear Maps

Definition
- Let V1, V2, …, Vk and W be vector spaces over the same field F. A map
  T : V1 × V2 × … × Vk → W
  is k-linear (or multilinear) if T is linear in each argument separately: for each j = 1,…,k, whenever all coordinates except the j-th are held fixed, the map
  vj ↦ T(v1,…, vj, …, vk)
  is a linear map Vj → W.
- When all Vi are equal to a single V, one may call T a k-linear map on V (or a k-linear form if W = F).

Key examples
- Bilinear forms: For vector spaces U and V, a bilinear map B : U × V → F is 2-linear. Examples include the standard dot product on R^n (or F^n) and the pairing (u, φ) ↦ φ(u) for u ∈ V, φ ∈ V*, the dual space.
- Matrix entry/evaluation maps: For fixed matrices A,B, the map (x,y) ↦ x^T A y is bilinear in the column vectors x and y.
- Determinant as an n-linear alternating form: For an n-dimensional space V, det : V^n → F is multilinear in the n column (or row) vectors and alternating (changes sign under swapping two slots).
- Coordinate projection and concatenation: The map that sends (v1,…,vk) to a chosen linear combination of one coordinate or to a linear operator applied to one coordinate is multilinear when that operator is linear.
- Tensor product universal map (conceptual): The canonical multilinear map V1 × … × Vk → V1 ⊗ … ⊗ Vk is multilinear by construction (serves as the universal example).

Basic algebraic properties
- Linearity in each slot: For fixed vectors in all slots except j, and for scalars a,b ∈ F and vectors x,y ∈ Vj,
  T(…, a x + b y, …) = a T(…, x, …) + b T(…, y, …).
- Fixing variables yields linear maps: If v1,…, vj−1, vj+1,…,vk are fixed, the resulting map Vj → W given by vj ↦ T(v1,…, vj, …, vk) is linear. In particular, fixing all but one variable reduces T to an ordinary linear map.
- Closure under addition and scalar multiplication: If T and S are k-linear V1×…×Vk → W and α ∈ F, then T+S and αT are k-linear. Thus the set L(V1,…,Vk; W) of all k-linear maps is a vector space.
- Currying / partial evaluation linearity: For any fixed choice of some slots, the map that sends the remaining slots to W is multilinear in the remaining variables. For example, fixing the first r slots gives a (k−r)-linear map in the remaining slots.
- Composition with linear maps:
  - Precomposition: If for some j we replace the j-th argument by a linear map S : U → Vj and define T' : V1 × … × V_{j−1} × U × V_{j+1} × … × Vk → W by T'(…, u, …) = T(…, S(u), …), then T' is multilinear.
  - Postcomposition: If L : W → W' is linear and T : V1 × … × Vk → W is multilinear, then L ∘ T : V1 × … × Vk → W' is multilinear.
- Behavior under bases: A k-linear map is determined by its values on k-tuples of basis vectors. In finite dimensions, specifying T on all k-fold products of basis vectors determines T uniquely and enables coordinate descriptions (multilinear maps correspond to multidimensional arrays of scalars).

Notes (brief)
- Multilinearity is a strong requirement: each slot independently respects addition and scalar multiplication. Additional properties (symmetry, alternation) are treated separately.

Tensor products and tensor algebra

Goal. Produce a vector space (the tensor product) into which tuples of vectors are sent so that every multilinear map out of those tuples factors uniquely through a linear map from the tensor product. Use that to define tensors and tensor powers and to manipulate them.

1. Universal property (characterization)
- Let V1, …, Vk be finite-dimensional vector spaces over the same field F. A tensor product of V1, …, Vk is a pair (T, τ) where T is an F–vector space and
  τ : V1 × ··· × Vk → T
  is a multilinear map with the universal property:
  For every vector space U and every multilinear map f : V1 × ··· × Vk → U there exists a unique linear map F : T → U such that f = F ∘ τ.
- In symbols: Hom_F(T, U) ≅ Multilin_F(V1 × ··· × Vk, U), naturally in U. We write T ≡ V1 ⊗ ··· ⊗ Vk and τ(v1, …, vk) as v1 ⊗ ··· ⊗ vk.
- The universal property determines V1 ⊗ ··· ⊗ Vk uniquely up to a unique isomorphism.

2. Concrete construction (quotient of a free vector space)
- Form the free vector space F on the set of formal symbols (v1, …, vk) with vi ∈ Vi. Let R be the subspace spanned by all relations that enforce multilinearity in each slot:
  for fixed i,
  (…, v_i + v_i', …) − (…, v_i, …) − (…, v_i', …),
  (…, c v_i, …) − c(…, v_i, …),
  and similarly relations where other slots vary.
- Define V1 ⊗ ··· ⊗ Vk := F / R and let τ(v1, …, vk) be the class of (v1, …, vk). The quotient construction satisfies the universal property.

3. Simple tensors and general tensors
- Elements of the form v1 ⊗ ··· ⊗ vk (images of tuples under τ) are called simple (or pure) tensors.
- General tensors are finite linear combinations of simple tensors. Not every tensor is simple when k ≥ 2 (except in trivial cases).
- Multilinearity of τ gives the usual identities, e.g.
  (v1 + v1') ⊗ v2 ⊗ ··· ⊗ vk = v1 ⊗ v2 ⊗ ··· ⊗ vk + v1' ⊗ v2 ⊗ ··· ⊗ vk,
  and c(v1 ⊗ ··· ⊗ vk) = (cv1) ⊗ v2 ⊗ ··· ⊗ vk = v1 ⊗ ··· ⊗ (c vk).

4. Correspondence between multilinear and linear maps
- Given multilinear f : V1 × ··· × Vk → U, the universal property gives a unique linear F : V1 ⊗ ··· ⊗ Vk → U with
  F(v1 ⊗ ··· ⊗ vk) = f(v1, …, vk).
- Conversely, every linear map L : V1 ⊗ ··· ⊗ Vk → U defines a multilinear map L ∘ τ. Thus
  Hom_F(V1 ⊗ ··· ⊗ Vk, U) ≅ Multilin_F(V1 × ··· × Vk, U).
- Important special case (k = 2): bilinear maps V × W → U correspond to linear maps V ⊗ W → U.

5. Bases and dimensions
- If Vi has basis {e_{i,α}} (α runs over appropriate index set) then the set of simple tensors
  e_{1,α1} ⊗ e_{2,α2} ⊗ ··· ⊗ e_{k,αk}
  is a basis of V1 ⊗ ··· ⊗ Vk. Hence
  dim(V1 ⊗ ··· ⊗ Vk) = ∏_{i=1}^k dim Vi.
- In particular, if V has basis {e1, …, en} then the pure tensors e_{i1} ⊗ ··· ⊗ e_{ik} (1 ≤ ij ≤ n) form a basis of V^{⊗ k} and dim V^{⊗ k} = n^k.

6. Tensor powers
- The k-th tensor power of V is V^{⊗ k} := V ⊗ ··· ⊗ V (k factors). By convention V^{⊗ 0} = F (the ground field) and V^{⊗ 1} = V.
- Elements of V^{⊗ k} are called k-tensors on V (note: in other contexts, “k-tensors” may mean multilinear maps on V^k; be attentive to conventions).

7. Natural isomorphisms and basic identities
- Associativity up to canonical isomorphism:
  (V ⊗ W) ⊗ U ≅ V ⊗ (W ⊗ U) ≅ V ⊗ W ⊗ U.
  We identify them when convenient; tensor products are associative in this canonical sense.
- Commutativity/flip (symmetry) isomorphism:
  V ⊗ W ≅ W ⊗ V via v ⊗ w ↦ w ⊗ v.
- Hom–tensor adjunction (finite-dimensional case):
  Hom_F(V ⊗ W, U) ≅ Hom_F(V, Hom_F(W, U)).
  In particular Hom_F(V ⊗ W, F) ≅ Hom_F(V, W^*) ≅ Bilin(V × W, F).
- If L : V → V' and M : W → W' are linear, there is an induced linear map L ⊗ M : V ⊗ W → V' ⊗ W' defined on simple tensors by (L ⊗ M)(v ⊗ w) = L(v) ⊗ M(w). This construction is bilinear in L and M and respects composition.

8. Tensor algebra
- The tensor algebra T(V) is the graded algebra
  T(V) := ⊕_{k=0}^∞ V^{⊗ k}
  with multiplication given by concatenation of tensors:
  (x ∈ V^{⊗ p}) · (y ∈ V^{⊗ q}) = x ⊗ y ∈ V^{⊗ (p+q)}.
- T(V) is an associative (noncommutative in general) unital algebra with unit 1 ∈ V^{⊗ 0} = F.
- Universal property of T(V): for any algebra A and linear map φ : V → A there is a unique algebra homomorphism Φ : T(V) → A extending φ. Thus T(V) is the “free algebra generated by V.”

9. Using tensors in practice (typical manipulations)
- To define a multilinear map f uniquely, it suffices to define its associated linear map on a basis of the tensor product. For V finite-dimensional with basis {e_i}, specifying values of F on e_{i1} ⊗ ··· ⊗ e_{ik} determines F on V^{⊗ k}.
- To check multilinearity identities, work on simple tensors and extend linearly.
- To test if a tensor is simple: for V finite-dimensional, a tensor t ∈ V ⊗ W corresponds to a linear map V* → W; t is simple iff that map has rank 1. More generally, decomposability tests reduce to linear-algebra rank conditions on flattenings/reshapings of coordinates.
- Constructions such as contraction, traces, symmetrization and antisymmetrization are performed by composing the associated linear maps with canonical maps between tensor powers (e.g., the projection to exterior/symmetric powers).

10. Summary of the key technical fact
- The universal property is the operational core: multilinear objects on V1 × ··· × Vk are exactly linear objects on the tensor product V1 ⊗ ··· ⊗ Vk. This lets you move freely between multilinear maps and linear algebra on tensor spaces, and it underlies the definitions of tensor powers, the tensor algebra, and all standard tensor manipulations.

Alternating multilinear forms and exterior algebra

Definition — alternating multilinear form
- Let V be a vector space over a field F. A k-linear map ω: V^k → F is alternating if ω(v1,...,vk) = 0 whenever two arguments are equal. Equivalently, for every permutation σ in the symmetric group Sk,
  ω(v_{σ(1)},...,v_{σ(k)}) = sgn(σ) ω(v1,...,vk).
- Alternating ⇒ skew-symmetric: swapping two arguments changes the sign: ω(...,vi,...,vj,...) = −ω(...,vj,...,vi,...).
- Consequence: If char(F) = 2, "alternating" and "skew-symmetric" coincide (signs collapse), but the defining zero-on-equal-arguments remains the clean invariant.

Space of alternating k-forms
- Denote Alt^k(V) the vector space of alternating k-linear forms V^k → F (also written Λ^k V* when emphasizing duals).
- Alt^0(V) ≅ F, Alt^1(V) ≅ V*.
- If dim V = n then Alt^k(V) = {0} for k > n. For finite n, dim Alt^k(V) = C(n,k) = n choose k.

Constructing exterior powers
Two equivalent constructions are commonly used: alternating projection on the tensor power, or quotient of the tensor power by the subspace generated by dependent tensors.

1) Alternating projection (antisymmetrization)
- Start with the tensor power V^{⊗ k}. Define the antisymmetrization operator A: V^{⊗ k} → V^{⊗ k} by
  A = (1/k!) ∑_{σ∈Sk} sgn(σ) P_σ,
  where P_σ permutes tensor factors according to σ.
- The image of A consists of totally antisymmetric tensors. Define Λ^k V = Im(A). Elements are written as wedge products v1 ∧ ... ∧ vk (the image of v1 ⊗ ... ⊗ vk under A).
- Properties: A is a projection (A^2 = A) onto the antisymmetric subspace. For any permutation σ,
  A(v_{σ(1)} ⊗ ... ⊗ v_{σ(k)}) = sgn(σ) A(v1 ⊗ ... ⊗ vk).
- When working over fields not requiring division by k!, the quotient construction below avoids dividing by integers.

2) Quotient construction
- Let I_k be the subspace of V^{⊗ k} spanned by all simple tensors that have a repeated factor, i.e., tensors of the form v1 ⊗ ... ⊗ vk with vi = vj for some i ≠ j. Equivalently, take the subspace generated by elements of the form v1 ⊗ ... ⊗ vk + v1 ⊗ ... ⊗ vj ⊗ ... − swapped versions (an ideal forcing skew-symmetry).
- Define Λ^k V = V^{⊗ k} / J_k where J_k is the subspace generated by all tensors of the form v1 ⊗ ... ⊗ vk with vi = vj (or by all elements enforcing v⊗v = 0 and multilinearity in each slot). The quotient enforces alternating relations and yields the exterior power.
- The equivalence class of v1 ⊗ ... ⊗ vk in the quotient is written v1 ∧ ... ∧ vk.
- This construction works over any field (no division by k! required) and matches the antisymmetrization image when char(F) = 0 or when k! is invertible.

Universal property of Λ^k V
- Λ^k V with the wedge map w: V^k → Λ^k V defined by w(v1,...,vk) = v1 ∧ ... ∧ vk is universal among alternating k-linear maps: given any alternating k-linear map φ: V^k → W (W any vector space), there exists a unique linear map Φ: Λ^k V → W such that φ = Φ ∘ w.
- This universal property characterizes Λ^k V up to unique isomorphism and is often used to define the exterior power abstractly.

Wedge product
- The full exterior algebra is Λ V = ⊕_{k=0}^n Λ^k V with multiplication the wedge product ∧: Λ^p V × Λ^q V → Λ^{p+q} V.
- On simple wedges, define (v1 ∧ ... ∧ vp) ∧ (w1 ∧ ... ∧ wq) = v1 ∧ ... ∧ vp ∧ w1 ∧ ... ∧ wq, then extend bilinearly.
- The wedge product is associative and bilinear. It is graded-anticommutative:
  α ∧ β = (−1)^{pq} β ∧ α
  for α ∈ Λ^p V, β ∈ Λ^q V.
- In particular, for 1-forms x,y ∈ V* (or vectors viewed in Λ^1 V), x ∧ x = 0.

Core identities and properties
- Antisymmetry on generators: If you swap two consecutive vectors in a simple wedge you pick up a minus sign. For any transposition τ exchanging two factors, apply sgn(τ).
- Basis and dimension: If {e1,...,en} is a basis of V, then the set {ei1 ∧ ... ∧ eik : 1 ≤ i1 < ... < ik ≤ n} is a basis of Λ^k V. Thus dim Λ^k V = C(n,k).
- Decomposability: Not every element of Λ^k V is a single wedge of k vectors (those that are are called decomposable); linear combinations can be non-decomposable (except in low degrees).
- Contraction and interior product (if needed later): given v ∈ V there is an interior product iv: Λ^k V → Λ^{k−1} V lowering degree and satisfying iv( w1 ∧ ... ∧ wk ) = ∑_{j} (−1)^{j−1} ⟨v,wj⟩ w1 ∧ ... ∧ w_{j−1} ∧ w_{j+1} ∧ ... ∧ wk when pairing with a dual or in the presence of an inner product. (This is often introduced when ΛV is paired with ΛV*.)
- Relationship with determinants: Λ^n V is 1-dimensional when dim V = n; for a linear map T: V → V, the induced map Λ^n T: Λ^n V → Λ^n V is multiplication by det(T). So determinants arise naturally from the top exterior power.

Wedge and alternating forms correspondence
- There is an isomorphism between Λ^k V* and Alt^k(V) given by sending a simple tensor φ1 ∧ ... ∧ φk in Λ^k V* to the alternating k-form
  (v1,...,vk) ↦ det( [φi(vj)]_{i,j} ).
  More concretely, the evaluation of φ1 ∧ ... ∧ φk on v1 ∧ ... ∧ vk equals the determinant of the k×k matrix with entries φi(vj). This makes Λ^k V* the natural home of alternating k-linear functionals on V.
- Under this identification, wedge product corresponds to the exterior (composition) of alternating forms: (α ∧ β)(v1,...,vp+q) equals the alternating sum obtained by applying α to p of the vectors and β to the remaining q, appropriately signed.

Practical consequences to remember
- v1 ∧ ... ∧ vk = 0 if and only if v1,...,vk are linearly dependent.
- Wedge product gives a graded algebra capturing oriented volume elements, multilinear antisymmetric behavior, and the determinant in top degree.
- The exterior algebra is functorial: a linear map T: V → W induces Λ^k T: Λ^k V → Λ^k W satisfying Λ^k(T)(v1 ∧ ... ∧ vk) = T(v1) ∧ ... ∧ T(vk).

This completes the core definitions, constructions, and identities for alternating multilinear forms and the exterior algebra built from them.

Definition (determinant via alternating multilinearity).
Let V be an n-dimensional vector space over a field F, and fix an ordered basis. Consider functions D: V^n → F that are multilinear in the n vector arguments and alternating, meaning D(v1,...,vn) = 0 whenever two arguments are equal (equivalently D changes sign when two arguments are swapped). There is a unique such alternating multilinear function D with the normalization
D(e1,…,en) = 1
where e1,…,en are the standard basis vectors. For an n×n matrix A, regard its columns as vectors in V and define
det(A) := D(column1(A), …, columnn(A)).
This defines the determinant of A.

Uniqueness and existence (brief).
- Existence: one can construct D by the usual permutation formula
D(v1,…,vn) = ∑_{σ∈Sn} sgn(σ) Π_{i=1}^n a_{i,σ(i)}
when the vi are expressed in the fixed basis (this is the usual determinant polynomial in the matrix entries).
- Uniqueness: any alternating multilinear function is determined by its values on n-tuples of basis vectors; alternation forces the values on basis tuples to be ±1 or 0 and the normalization fixes the value on (e1,…,en), hence the function is unique.

Properties derived from multilinearity and alternation

1) Effect of column operations (and similarly row operations).
Let A be n×n with columns c1,…,cn. For scalar α and column index j:
- Scaling a column: replacing column j by αcj multiplies det by α:
det(..., αcj, ...) = α det(..., cj, ...),
because D is multilinear in each argument.
- Column addition: replacing column j by cj + v leaves det linear:
det(..., cj + v, ...) = det(..., cj, ...) + det(..., v, ...).
- Swapping columns i and j changes the sign:
det(..., ci, ..., cj, ...) = − det(..., cj, ..., ci, ...),
because alternation implies D changes sign under a transposition.
- If two columns are equal, det = 0, since alternation gives zero when arguments repeat.

Thus the usual elementary column operations have the expected effects:
- Multiply a column by α ⇒ determinant multiplied by α.
- Add a scalar multiple of one column to another ⇒ determinant unchanged.
- Swap two columns ⇒ determinant multiplied by −1.

All analogous statements hold for rows (apply the same definition to rows or use det(A) = det(A^T) which follows from alternation plus multilinearity).

2) Determinant of a product (multiplicativity).
For n×n matrices A and B,
det(AB) = det(A) det(B).

Proof sketch:
View the columns of AB as A applied to the columns of B: column j of AB is A(column j of B). Fix the alternating multilinear function D on columns. Define F(v1,…,vn) := D(Av1,…,Avn). Because D is multilinear and A is linear, F is alternating and multilinear in v1,…,vn. By uniqueness of the normalized alternating multilinear form, F must equal det(A)·D(v1,…,vn) (evaluate at the standard basis to check the scalar). Applying this with vj = column j of B gives
det(AB) = D(A·(col1(B)), …, A·(coln(B))) = det(A) D(col1(B),…,coln(B)) = det(A) det(B).

3) Determinant detects invertibility: det(A) = 0 iff A is not invertible.
- If A is invertible, then write I = A A^{-1} and take determinants to get 1 = det(I) = det(A) det(A^{-1}). Hence det(A) ≠ 0.
- Conversely, if det(A) ≠ 0, then det(A) det(adj(A)) = det(A·adj(A)) = det(det(A) I) = det(A)^n (one can argue using multiplicativity and properties of adjugate) which implies existence of an inverse; more directly in this development:
If det(A) ≠ 0 then the columns of A are linearly independent (if they were dependent, two columns could be expressed as a linear combination and multilinearity/alternation would give det(A)=0). Linear independence of the n columns in an n-dimensional space means they form a basis, so A is invertible. Thus det(A) = 0 ⇔ columns are linearly dependent ⇔ A is not invertible.

Consequences and useful corollaries
- det(I) = 1 by normalization.
- det(αA) = α^n det(A) (scaling every column by α multiplies determinant by α each time).
- det(A^T) = det(A) (transpose swaps rows and columns; the multilinear alternating form defined on columns or rows is the same up to the same normalization).
- If A is triangular (upper or lower), det(A) is the product of the diagonal entries, since expanding by multilinearity and alternation kills any term using an off-diagonal choice of basis vectors.

These properties follow directly from the defining multilinearity and alternation together with the normalization at the identity.

Characteristic Polynomial Coefficients and Determinant

Let V be an n-dimensional vector space over a field F and T ∈ L(V). The characteristic polynomial of T is
p_T(λ) = det(λI − T) ∈ F[λ].
When you expand p_T(λ) as a polynomial of degree n,
p_T(λ) = λ^n + a_{n-1} λ^{n-1} + ··· + a_1 λ + a_0,
the coefficients a_k carry invariant algebraic information about T. Two particular coefficients are most commonly used: the coefficient of λ^{n-1} (related to the trace) and the constant term a_0 (related to the determinant).

Relations with trace and determinant
- trace: The coefficient of λ^{n-1} is −tr(T). Equivalently,
p_T(λ) = λ^n − (tr T) λ^{n-1} + ··· .
Thus tr T = −a_{n-1}. In particular, when you factor p_T(λ) over an algebraic closure with eigenvalues λ_1,…,λ_n (counted with algebraic multiplicity),
p_T(λ) = ∏_{i=1}^n (λ − λ_i),
so tr T = λ_1 + ··· + λ_n (sum of eigenvalues).

- determinant: The constant term satisfies
a_0 = det(−T) = (−1)^n det T,
so det T = (−1)^n a_0 = (−1)^n p_T(0).
With the eigenvalue factorization above, det T = λ_1 ··· λ_n (product of eigenvalues).

More generally, the coefficient of λ^{n−k} (up to sign) is the k-th elementary symmetric polynomial in the eigenvalues: the coefficient of λ^{n−k} equals (−1)^k times the sum of all k-fold products of distinct eigenvalues.

Behavior under change of basis / similarity
If A is the matrix of T with respect to some basis and B is the matrix of T with respect to another basis, then A and B are similar: B = P^{-1}AP for some invertible P. Similar matrices have the same characteristic polynomial because
det(λI − P^{-1}AP) = det(P^{-1}(λI − A)P) = det(P^{-1}) det(λI − A) det(P) = det(λI − A).
Hence p_B = p_A = p_T. Therefore every coefficient of the characteristic polynomial is invariant under change of basis; in particular tr T and det T are intrinsic to the linear map (not to a chosen matrix).

Direct invariance proofs (matrix viewpoint)
- trace invariance: tr(P^{-1}AP) = tr(APP^{-1}) = tr(A) because tr(XY) = tr(YX) for all square matrices X,Y. Thus trace is similarity invariant.
- determinant invariance: det(P^{-1}AP) = det(P^{-1}) det(A) det(P) = det(A), so determinant is similarity invariant.

Consequences and useful formulas
- det T = (−1)^n p_T(0), so computing p_T(0) gives det T up to the sign (or directly gives it when you account for (−1)^n).
- tr T = −(coefficient of λ^{n−1} in p_T).
- If the eigenvalues λ_1,…,λ_n are known (over an algebraic closure), then p_T(λ) = ∏(λ − λ_i), tr T = ∑ λ_i, and det T = ∏ λ_i.
- All coefficients of p_T are similarity invariants; thus knowledge of the characteristic polynomial yields invariant scalar data about T (trace, determinant, and the elementary symmetric functions of the eigenvalues).

These relations explain why trace and determinant often appear in invariant statements about linear operators: they are simply the first and last nontrivial coefficients of the characteristic polynomial.

Determinant, Volume, and Orientation

Definition and geometric meaning
- For a real n-dimensional vector space V, the determinant of a linear map T: V → V is the scalar that measures how T changes oriented n-dimensional volume. Concretely, if v1, …, vn is an ordered basis of V, the parallelepiped spanned by these vectors has (oriented) volume Vol(v1, …, vn). The image parallelepiped spanned by Tv1, …, Tvn has oriented volume det(T) · Vol(v1, …, vn). This identity does not depend on the choice of ordered basis; det(T) is an intrinsic scalar associated to T.

Oriented volume vs. unsigned volume
- The oriented volume of an ordered basis can be positive or negative; its sign encodes an orientation. The absolute value |det(T)| gives the factor by which ordinary (unsigned) n-dimensional volume is scaled. The sign of det(T) indicates whether T preserves or reverses orientation: det(T) > 0 means orientation-preserving, det(T) < 0 means orientation-reversing. If det(T) = 0, T collapses V into a proper subspace and the n-volume is sent to zero.

Volume via the Gram determinant
- In an inner-product space, the squared (unsigned) volume of the parallelepiped spanned by vectors v1, …, vn equals the determinant of the Gram matrix G = [⟨vi, vj⟩]: Vol(v1, …, vn)^2 = det(G). This shows how inner products (lengths and angles) determine volume. For an orthonormal basis e1, …, en, the Gram matrix is the identity and Vol(e1, …, en) = 1, so determinants of matrices relative to orthonormal bases give the oriented scaling directly.

Change of basis and coordinate matrices
- If [T]_B is the matrix of T with respect to an ordered basis B, then det([T]_B) = det(T). Thus the determinant computed in coordinates equals the intrinsic oriented-volume scaling. Changing the ordered basis can change the sign of the oriented volume assigned to a given ordered list of vectors, but det(T) as the ratio of oriented volumes of images to originals is independent of that choice.

Relation to singular values and geometric decomposition
- In an inner-product space one can orthogonally diagonalize the positive semidefinite operator √(T*T). The singular values σ1, …, σn of T are the principal scale factors along mutually orthogonal directions, and
  |det(T)| = σ1 · σ2 · … · σn.
This expresses the volume-scaling as the product of orthogonal directional scalings. The sign of det(T) comes from orientation information not captured by singular values; orthogonal factors (like rotations or reflections) contribute ±1 to det(T).

Examples and intuition
- Rotations: orthogonal maps with determinant +1 preserve oriented volume (det = 1).
- Reflections: orthogonal maps reflecting across a hyperplane reverse orientation (det = −1) while preserving unsigned volume.
- Projection onto a proper subspace: det = 0, volumes collapse to zero.
- Shears: non-orthogonal maps can change volume; their determinant equals the net signed stretching of n-volumes.

Summary picture
- Think of det(T) as the signed multiplier applied to the n-dimensional “content” of any oriented parallelepiped under T: magnitude gives how much the n-volume is stretched or compressed; sign tells whether the orientation is kept or flipped. In inner-product spaces this connects directly to lengths and angles via the Gram determinant and to orthogonal decompositions via singular values.