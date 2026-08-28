Scalars
A scalar is an element of a field, the set from which the coefficients of vectors come. In most elementary treatments the field is either the real numbers R or the complex numbers C, so we say a vector space is over R or over C. The choice of field determines what scalar operations (addition, multiplication, additive inverses, multiplicative inverses for nonzero elements) are available.

How scalar multiplication interacts with vector addition
One of the vector space axioms describes how scalar multiplication distributes over vector addition. If v and w are vectors and a is a scalar, then
a(v + w) = av + aw.
This says multiplying a sum of vectors by a scalar is the same as multiplying each vector by the scalar and then adding.

There is a closely related axiom about how addition of scalars distributes over scalar multiplication: if a and b are scalars and v is a vector, then
(a + b)v = av + bv.
This says that adding scalars first and then scaling a vector equals scaling the vector by each scalar and adding the results.

Together with the other scalar-related axioms (associativity of scalar multiplication: a(bv) = (ab)v, and existence of multiplicative identity: 1·v = v), these distribution laws ensure scalar multiplication behaves compatibly with vector addition and the field structure of the scalars.

Section 2 — Vector Space (definition and axioms)

Definition
A vector space V over a field F (usually R or C) is a set equipped with two operations:
- Vector addition: + : V × V → V
- Scalar multiplication: · : F × V → V
These operations must satisfy the following axioms for all u, v, w in V and all scalars a, b in F.

Axioms
1. (Additive closure) u + v ∈ V.
2. (Commutativity of addition) u + v = v + u.
3. (Associativity of addition) (u + v) + w = u + (v + w).
4. (Additive identity) There exists 0 ∈ V such that 0 + v = v for all v ∈ V.
5. (Additive inverses) For each v ∈ V there exists an element −v ∈ V with v + (−v) = 0.
6. (Scalar multiplicative closure) a · v ∈ V.
7. (Distributivity of scalar over vector addition) a · (u + v) = a · u + a · v.
8. (Distributivity of scalar addition) (a + b) · v = a · v + b · v.
9. (Associativity of scalar multiplication) a · (b · v) = (ab) · v.
10. (Identity scalar) 1 · v = v, where 1 is the multiplicative identity in F.

Useful immediate consequences (often used in verification)
- The additive identity 0 is unique.
- Additive inverses are unique and equal to (−1)·v.
- 0·v = 0 (the zero vector).
- a·0 = 0 (for every scalar a).
- If a·v = 0 and a ≠ 0, then v = 0.
- (−a)·v = −(a·v) = a·(−v).

How to verify a given set with operations is a vector space — checklist
1. Confirm the set and operations are well-defined (every pair or scalar-vector pair yields an element in the set).
2. Check closure explicitly for addition and scalar multiplication.
3. Verify the ten axioms above. Typical order for checking:
   - Verify addition is associative and commutative.
   - Exhibit the additive identity and check it works.
   - Show every vector has an additive inverse.
   - Check distributivity laws, associativity of scalar multiplication, and the identity scalar property.
4. Use the immediate consequences to simplify checks (e.g., uniqueness of zero/inverse need not be separately proven if you derive them from axioms).
5. If any axiom fails, the structure is not a vector space. A single failing axiom suffices.

Common pitfalls / quick tests
- If scalar multiplication is defined in a way that depends on extra structure (e.g., multiplication of functions pointwise vs. some nonstandard rule), test distributivity and 1·v = v carefully.
- If the set is not closed under addition or scalar multiplication, it is not a vector space.
- If the “zero” element in the set is not the same as 1·v requirement (1·v should equal v for all v), the identity scalar axiom fails.
- Subsets of a vector space: to be a subspace, the subset must be nonempty and closed under addition and scalar multiplication (you do not need to re-check all axioms).

Examples to test
- R^n with usual addition and scalar multiplication: vector space.
- Set of continuous functions with pointwise operations: vector space.
- Set of polynomials of degree exactly n (not ≤ n): not a vector space (not closed under addition).
- Nonzero vectors alone with usual operations but without the zero vector: not a vector space.

When asked to verify a specific example, run through the checklist above and point out which axiom(s) hold or fail.

Linear combinations and span

Definition — linear combination
- Let V be a vector space over a field F. Given vectors v1, v2, …, vn in V and scalars a1, a2, …, an in F, the vector
  a1 v1 + a2 v2 + … + an vn
  is called a linear combination of v1, …, vn. By convention, a linear combination uses only finitely many vectors; the empty linear combination (no vectors) is defined to equal the zero vector 0.

Definition — span
- For a subset S ⊆ V, the span of S, denoted span(S), is the set of all linear combinations of vectors from S:
  span(S) = { a1 v1 + ··· + an vn : n ≥ 0, vi ∈ S, ai ∈ F }.
  In particular, span(∅) = {0}.

Basic facts
1. span(S) is a subspace of V.
   Proof sketch: The zero vector is in span(S) (empty combination). If x and y are linear combinations of vectors from S, and α, β ∈ F, then αx + βy is again a linear combination of vectors from S (combine the finite lists and scale the coefficients). Thus span(S) is closed under linear combinations and is a subspace.

2. S ⊆ span(S).
   Every s ∈ S is the linear combination 1·s, so S is contained in its span.

3. Minimality (smallest subspace containing S).
   - Let U be any subspace of V with S ⊆ U. Then every linear combination of vectors from S lies in U (because U is closed under scalar multiplication and addition). Hence span(S) ⊆ U.
   - Therefore span(S) is the smallest subspace of V that contains S: it is contained in every subspace that contains S, and it itself is a subspace containing S.

Alternative characterization
- span(S) = ⋂{ U : U is a subspace of V and S ⊆ U }.
  That is, the span is the intersection of all subspaces of V that contain S. This is an immediate corollary of the minimality property.

How to use span in practice
- Generating a subspace: To describe the smallest subspace containing some vectors v1,…,vm, write span({v1,…,vm}) = { a1 v1 + ··· + am vm : a1,…,am ∈ F }.
- Checking membership: To see if w ∈ span({v1,…,vm}), attempt to find scalars a1,…,am solving a1 v1 + ··· + am vm = w. If a solution exists, w lies in the subspace generated by the vi.
- Finite vs. infinite S: Even if S is infinite, every vector in span(S) is a finite linear combination of elements of S. Thus working with a finite generating subset (if one exists) reduces questions to finite linear algebra.

Examples
- span({v}) = {αv : α ∈ F} is the line through 0 and v (or {0} if v = 0).
- span({v1, v2}) consists of all vectors of the form αv1 + βv2 (a plane through 0 unless v2 is a scalar multiple of v1).
- span(∅) = {0}.

These notions let you concisely describe and reason about the subspace "generated by" or "spanned by" a given set of vectors: span(S) is precisely the smallest subspace containing S.

Linear independence — definition and basic consequences

Definition
- A list (or set) of vectors v1, v2, ..., vm in a vector space V is linearly independent if the only scalars a1,...,am for which
  a1 v1 + a2 v2 + ... + am vm = 0
  are a1 = a2 = ... = am = 0.
- If there exists a choice of scalars, not all zero, giving a1 v1 + ... + am vm = 0, then the list is linearly dependent.

Immediate observations and basic tests
- The empty list is linearly independent by convention.
- Any list containing the zero vector is linearly dependent, because 1·0 plus 0 times the other vectors gives a nontrivial relation.
- A single vector v is independent iff v ≠ 0.
- Two vectors v and w are linearly dependent iff one is a scalar multiple of the other. Equivalently, {v,w} is independent ⇔ v ≠ 0, w ≠ 0, and w is not αv for any scalar α.
- For a finite list, to decide independence set up the linear combination a1 v1 + ... + am vm = 0 and solve for the scalars. If the only solution is the trivial one, the list is independent; otherwise it is dependent.

Key consequences
- Uniqueness of coefficients: If v1,...,vm are linearly independent and a1 v1 + ... + am vm = b1 v1 + ... + bm vm, then (a1 − b1) v1 + ... + (am − bm) vm = 0. By independence all differences are zero, so ai = bi for each i. Thus coordinates (coefficients) of a vector relative to an independent list are unique.
- Dependence gives a nontrivial relation: If v1,...,vm are dependent, there exist scalars, not all zero, with a1 v1 + ... + am vm = 0. In particular at least one vector is a linear combination of the others. For finite lists you can always find an index j such that vj is a linear combination of the other vectors; hence you can remove vj without changing the span of the list.
- Subsets: Any subset of a linearly independent set is linearly independent. Any superset of a dependent set is dependent.
- Maximum size: In an n-dimensional vector space, every list of more than n vectors is linearly dependent (proof via rank/dimension/solving the homogeneous system).

Short proofs of important facts
- Uniqueness of representation (sketch): Suppose v1,...,vm are independent and x = a1 v1 + ... + am vm = b1 v1 + ... + bm vm. Subtract the two expressions to get (a1−b1) v1 + ... + (am−bm) vm = 0. Independence forces all a i − b i = 0.
- Dependence implies one is a combination of others (finite case, sketch): Given a nontrivial relation ∑ a i v i = 0, pick j with a j ≠ 0. Solve for v j: v j = −(1/a j) ∑_{i≠j} a i v i.

How to decide independence in practice
- Small lists: Use the simple criteria above for 1 or 2 vectors.
- Moderate lists in R^n or with coordinates: form the matrix whose columns are the vectors and check whether the only solution of the homogeneous system is trivial (e.g., row-reduce). Full column rank ⇔ columns independent.
- Look for obvious linear relationships (scalar multiples, repeated vectors, zero vector) to detect dependence quickly.

Typical consequences to keep in mind
- If a spanning list is independent, it is a basis; hence being independent + spanning implies unique coordinate representation.
- If a list is dependent, some vector can be removed without reducing the span, so dependent lists are not minimal spanning sets.

Bases and the idea of dimension

Definition. A subset B of a vector space V is called a basis of V if
- B spans V (every vector in V is a linear combination of vectors from B), and
- B is linearly independent (no nontrivial linear combination of vectors from B equals the zero vector).

Why this is the right definition. A basis is a smallest spanning set and simultaneously a largest linearly independent set. Intuitively, a basis picks out the essential directions in V: once you fix a basis, every vector in V is determined by how much it points in each of those directions.

Coordinates and uniqueness. If B = {b1, …, bn} is a basis of V, then every v in V can be written uniquely as v = a1 b1 + … + an bn. The scalars (a1, …, an) are the coordinates of v relative to the basis B. Uniqueness follows directly from linear independence: if two different coordinate lists produced the same v, their difference would give a nontrivial linear relation among the basis vectors.

Examples to build intuition.
- In R^2 the standard basis e1 = (1,0), e2 = (0,1) is a basis: it spans R^2 and is linearly independent. Any two noncollinear vectors in R^2 form a basis.  
- In the space P2 of polynomials of degree ≤ 2, the set {1, x, x^2} is a basis: every quadratic polynomial is a unique linear combination of these three polynomials.

The idea of dimension. With a basis in hand, it is natural to measure the “size” of V by the number of vectors in a basis. This number captures the number of independent directions or degrees of freedom in the space and is called the (vector space) dimension. For now think informally: R^2 has dimension 2 because two numbers (coordinates) are needed to specify a vector; P2 has dimension 3 because three coefficients determine a quadratic polynomial.

Two perspectives that connect to dimension.
- Minimal spanning viewpoint: a basis is a spanning set that ceases to span if any vector is removed. Thus the number of basis vectors is the minimal number needed to span V.
- Maximal independence viewpoint: a basis is a linearly independent set that cannot be enlarged without losing independence. Thus the number of basis vectors is the maximal number of mutually independent directions.

What to expect next. Later we will make the notion of dimension precise for finite-dimensional spaces and prove that every basis of a given finite-dimensional V has the same number of elements (so “the” dimension is well-defined). We will also develop constructive procedures to pass between spanning sets, independent sets, and bases, and to compute coordinates relative to chosen bases. For now, keep the picture in mind: a basis provides a complete, nonredundant description of a vector space, and its size is the dimension — the number of independent degrees of freedom.

Subspaces and the Subspace Test

Definition
- Let V be a vector space over a field F. A subset U ⊆ V is a subspace of V if U is itself a vector space over F under the same addition and scalar multiplication as V.

Subspace Test (standard criteria)
- A subset U ⊆ V is a subspace of V if and only if:
  1. U ≠ ∅ (equivalently: 0 ∈ U),
  2. U is closed under vector addition: for all u1, u2 ∈ U, u1 + u2 ∈ U,
  3. U is closed under scalar multiplication: for all α ∈ F and u ∈ U, αu ∈ U.

Proof sketch of the test
- (⇒) If U is a subspace, it is a vector space so it must contain 0 and be closed under addition and scalar multiplication.
- (⇐) If U satisfies the three conditions, the vector space axioms inherited from V hold automatically (associativity, commutativity of addition, distributivity, existence of additive inverses follows because for u ∈ U, −1·u ∈ U). Thus U is a vector space and hence a subspace.

Equivalent one-step criterion
- It is often convenient to check: U ≠ ∅ and for all u1, u2 ∈ U and all α, β ∈ F, the linear combination αu1 + βu2 ∈ U. This single closure under all linear combinations is equivalent to (1)–(3).

How to use the test in practice
- First check nonempty (usually by showing 0 ∈ U).
- Then prove closure properties. To show closure under scalar multiplication and addition, start with arbitrary elements of U and an arbitrary scalar and manipulate using the definition of the set.
- To show a set is not a subspace, it suffices to find one counterexample violating any of the three conditions (commonly: 0 not in the set, two elements whose sum is not in the set, or a scalar multiple not in the set).

Common examples of subspaces
- {0} (the zero subspace) and V itself.
- Span of any set of vectors: span{v1, ..., vk} is a subspace.
- Solution spaces of homogeneous linear systems: {x ∈ F^n : Ax = 0}.
- Polynomials of degree ≤ n inside the vector space of all polynomials.
- Continuous real-valued functions on an interval that satisfy a homogeneous linear condition (e.g., solutions to a homogeneous linear differential equation).
- Even functions (resp. odd functions) form a subspace of all functions when closed under the operations.
- All m×n matrices with a fixed row space/column space? (Be careful: sets defined by linear homogeneous constraints on matrix entries are subspaces.)

Common counterexamples (not subspaces) and why
- The set of vectors with all positive entries in R^n: fails because 0 ∉ set (nonempty/zero condition fails) and scalar multiplication by negative scalars leaves the set.
- The set of vectors of norm 1 in R^n (the unit sphere): 0 ∉ set and not closed under scalar multiplication.
- The set of polynomials of exact degree n (rather than degree ≤ n): not closed under addition (leading coefficients can cancel) and 0 is not of degree n.
- A translate of a subspace by a nonzero vector, e.g., {v0 + u : u ∈ U} with v0 ≠ 0: does not contain 0 unless v0 ∈ U, so generally not a subspace.
- The set of invertible matrices inside M_n(F): not closed under addition and does not contain 0.

Short illustrative examples
- Show span example: Let U = span{(1,1)} ⊆ R^2. 0 ∈ U, sums and scalar multiples of multiples of (1,1) are again multiples of (1,1), so U is a subspace.
- Show a failure: Let W = {(x,y) ∈ R^2 : x ≥ 0}. 0 ∈ W, but (1,0) ∈ W and (−1,0) ∉ W, so W is not closed under scalar multiplication; hence not a subspace.
- Homogeneous linear system example: For A ∈ M_{m×n}(F), the set {x ∈ F^n : Ax = 0} contains 0, and if Ax = 0 and Ay = 0 then A(αx+βy)=αAx+βAy=0, so it is a subspace.

Tips and common pitfalls
- Always check 0 ∈ U first — it’s quick and often rules out a candidate.
- Remember “closed under linear combinations” is stronger and often easier to use: show αu + βv ∈ U for arbitrary scalars α, β and u, v ∈ U.
- Beware sets defined by nonhomogeneous linear conditions (e.g., Ax = b with b ≠ 0) — these are typically affine subspaces (cosets) but not subspaces unless b = 0.

Bases

Definition
- A basis of a vector space V is a list of vectors that is both linearly independent and spans V.
- Equivalently, a basis is a minimal spanning list (removing any vector destroys the spanning property) or a maximal linearly independent list (adding any vector from V makes it linearly dependent).

Existence in finite-dimensional spaces
- A vector space V is finite-dimensional if it has a finite spanning list.
- In any finite-dimensional V there exists a basis. Two standard constructions show how to produce a basis starting either from a spanning list or from an independent list.

Building a basis from a spanning list (reduce the list)
1. Start with a finite spanning list (v1, v2, ..., vn).
2. Remove any vector that is a linear combination of preceding ones. Concretely, scan the list left to right and keep each vi only if it is not in the span of the earlier kept vectors.
3. The resulting list is still spanning and is linearly independent, hence a basis.
- Because the original list is finite, this process terminates and yields a finite basis.

Extending a linearly independent list to a basis (extend the list)
1. Start with a finite linearly independent list (u1, ..., uk) in V.
2. If the list already spans V, it is a basis. If not, pick a vector w in V not in the span of the current list and append it; the enlarged list remains independent.
3. Repeat: at each step pick a vector outside the current span and add it. Since V has a finite spanning list, this process cannot continue indefinitely; eventually the list spans V.
4. The final list is linearly independent and spans V, hence a basis.

Remarks
- Both procedures rely on finiteness to guarantee termination.
- The two viewpoints (reducing a spanning list and extending an independent list) are dual ways to produce bases in finite-dimensional spaces.

Coordinates relative to a basis

Definition
Let V be a finite-dimensional vector space over a field F and let B = (v1, v2, …, vn) be an ordered basis of V. For any vector v ∈ V there exist unique scalars c1, c2, …, cn ∈ F such that
v = c1 v1 + c2 v2 + … + cn vn.
The coordinate representation (or coordinate vector) of v relative to the basis B is the column vector of those scalars:
[v]B := (c1, c2, …, cn)^T ∈ F^n.

Uniqueness of coordinates
Suppose v has two representations relative to B:
v = c1 v1 + … + cn vn = d1 v1 + … + dn vn.
Subtracting gives 0 = (c1 − d1) v1 + … + (cn − dn) vn. Since B is linearly independent, the only solution is c1 − d1 = … = cn − dn = 0, so ci = di for each i. Hence the coordinates (ci) are unique.

How coordinates encode linear combinations
1) Recovering v from coordinates: If [v]B = (c1, …, cn)^T then v = c1 v1 + … + cn vn. Thus the coordinate vector encodes exactly which linear combination of the basis vectors equals v.

2) Linearity of coordinates: The map C_B : V → F^n given by C_B(v) = [v]B is linear. In particular, for u, v ∈ V and α ∈ F,
[u + v]B = [u]B + [v]B, [αv]B = α [v]B.
Proof: If [u]B = (a1,…,an)^T and [v]B = (b1,…,bn)^T, then u = Σ ai vi and v = Σ bi vi, so u + v = Σ (ai + bi) vi and αv = Σ (α bi) vi. Reading off coordinates gives the stated equalities.

3) Encoding arbitrary linear combinations: Given scalars a1,…,an and vectors v1,…,vn, the linear combination w = a1 v1 + … + an vn has coordinate vector [w]B = (a1,…,an)^T (provided the vi are the basis vectors in that order). More generally, if one has coordinates x = (x1,…,xn)^T and basis B, then the linear combination they represent is the matrix product
v = [v1 … vn] x,
where [v1 … vn] is thought of as the list of basis vectors and x are the coordinates.

Consequences (brief)
- C_B is a linear isomorphism between V and F^n: coordinates give a concrete identification of V with F^n.
- Computing with vectors in V reduces to computing with their coordinate vectors in F^n.

Finite-dimensional (definition)

A vector space V over a field F is called finite-dimensional if there exists a finite list of vectors v1, v2, ..., vn in V whose span equals V; that is,
V = span{v1, v2, ..., vn}.
Equivalently, V is finite-dimensional iff V has a basis consisting of finitely many vectors. If no such finite spanning set (or finite basis) exists, V is called infinite-dimensional.

Remarks and examples

- R^n (or F^n): The standard vectors e1, ..., en span F^n, so F^n is finite-dimensional (dimension n).

- Polynomial spaces:
  - Pm(F) = {polynomials over F of degree ≤ m} is finite-dimensional; a basis is {1, x, x^2, ..., x^m}, so dim Pm(F) = m + 1.
  - P(F) = {all polynomials over F} is infinite-dimensional. Reason: the monomials 1, x, x^2, ... are infinitely many and are linearly independent, so no finite set can span all polynomials.

- Sequence and function spaces:
  - The space F^N of all sequences (a1, a2, ...) is infinite-dimensional.
  - C(R), the space of all real-valued continuous functions on R, is infinite-dimensional (e.g., 1, x, x^2, ... are linearly independent in C(R)).

- The zero space {0} is finite-dimensional (dimension 0). Note that span of the empty list is {0}, so the empty list serves as a finite spanning set in the usual conventions.

In short: finite-dimensional means “spanned by finitely many vectors” (equivalently has a finite basis); typical concrete finite-dimensional examples are F^n and spaces of polynomials of bounded degree, while many natural spaces of functions or sequences are infinite-dimensional.

Dimension (length of a basis) — statement and consequences

Definition
- Let V be a finite-dimensional vector space. A basis of V is a linearly independent list of vectors that spans V. The dimension of V, written dim V, is defined to be the length (number of vectors) of any basis of V.

The key fact that makes this definition well-defined is that any two bases of a finite-dimensional vector space have the same length. We prove that now and then record several standard inequalities and equalities involving dimension.

Theorem (All bases have the same length)
If V is a finite-dimensional vector space and B and B' are bases of V, then B and B' have the same number of elements.

Proof
Let B = (v1, ..., vm) and B' = (w1, ..., wn). Since B is a basis, it spans V, so each wj is a linear combination of v1,...,vm. In particular, the list (w1,...,wn) is contained in span(v1,...,vm). Apply the Exchange Lemma (or the Basic Lemma): if a list of vectors spans a space and another list is linearly independent inside that space, then the length of the independent list is ≤ the length of the spanning list. Because B' is linearly independent and B spans V, n ≤ m.

Interchange the roles of B and B' to get m ≤ n. Hence m = n. □

Consequences and standard inequalities

1) Basis extension and bound on basis length
- If V has a spanning list with m vectors, then every basis of V has length ≤ m. Reason: any basis is linearly independent and the spanning list bounds the length by the Exchange Lemma.

- Conversely, if V has a linearly independent list with n vectors, then any spanning list must have length ≥ n. Therefore any basis has length ≥ n.

2) Subspaces
- If U is a subspace of a finite-dimensional space V, then U is finite-dimensional and dim U ≤ dim V.
Proof: let B be a basis of U (length k). B is a linearly independent list in V, so by extending B to a basis of V (or by the Exchange Lemma comparing B with a basis of V), the length of a basis of V is ≥ k.

- If U is a proper subspace of V (U ≠ V), then dim U < dim V.
Proof: A proper subspace cannot span V, so any basis of U is a strictly shorter linearly independent list than a basis of V; hence strict inequality.

3) Dimension of a sum and intersection
For subspaces U and W of a finite-dimensional space V,
dim(U + W) = dim U + dim W − dim(U ∩ W).
Proof sketch: choose a basis of U ∩ W, extend it to bases of U and of W, then combine the extensions to get a basis of U + W; counting yields the formula.

4) Rank–nullity (for linear maps)
If T: V → W is a linear map and V is finite-dimensional, then
rank(T) + nullity(T) = dim V,
where rank(T) = dim(range T) and nullity(T) = dim(ker T).
Proof sketch: choose a basis of ker T, extend it to a basis of V; the images of the extension form a basis of range T, and counting gives the equality.

5) Inequalities related to generating sets and independent sets
- Any spanning list of V has length ≥ dim V.
- Any linearly independent list in V has length ≤ dim V.
- Any list with more than dim V vectors is linearly dependent.
- Any spanning list with fewer than dim V vectors does not span.

Remarks
- Dimension is a nonnegative integer; dim{0} = 0 because the zero space has empty basis.
- The Exchange Lemma (replacement lemma) is the engine behind all these comparisons: it allows replacing spanning vectors with independent ones while controlling lengths.

This completes the section establishing dimension as the length of a basis and the standard inequalities/equalities that follow.

Linear independence and dependence for finite lists — practical criteria and consequences

Definition (finite lists)
- A finite list (v1, ..., vn) of vectors in a vector space V is linearly independent if the only scalars a1,...,an satisfying a1 v1 + ... + an vn = 0 are a1 = ... = an = 0. Otherwise the list is linearly dependent.

Key practical criteria
1. Zero-sum test (direct): To test independence of (v1,...,vn), set up the linear equation a1 v1 + ... + an vn = 0 and solve for the scalars. If a nontrivial solution exists (some ai ≠ 0) the list is dependent; if only the trivial solution exists it is independent.

2. Matrix/row-reduction test: Represent v1,...,vn as columns of a matrix (relative to some basis of V). Row-reduce:
   - Columns are linearly independent iff the column-reduced matrix has a pivot in every column.
   - Equivalently, the homogeneous system with that matrix has only the trivial solution.

3. Length vs. dimension: If V is finite-dimensional with dim V = m, then any list of more than m vectors in V is automatically linearly dependent. Conversely any independent list has length ≤ dim V.

4. Dependence ⇒ one vector is redundant (finite-list special property): For finite lists, dependence means some vector in the list is a linear combination of the others. More precisely:
   - If (v1,...,vn) is dependent, then there exists j such that vj ∈ span{v1,...,vj-1, vj+1,...,vn}. In particular you can solve the dependence relation for some vj and write vj as a linear combination of the remaining vectors.
   - This lets you remove vj without changing the span: span(v1,...,vn) = span(v1,...,vj-1,vj+1,...,vn).

Consequences and useful procedures
1. Removing redundancy to get an independent list (pruning):
   - Given a spanning list, repeatedly remove any vector that is a linear combination of earlier ones. After finitely many removals you obtain an independent sublist that still spans the same subspace (hence is a basis of that subspace). This is the standard way to extract a basis from a spanning list.

2. Extending independent lists to bases:
   - If you have an independent list that does not span V, you can add vectors (not in its span) until it spans V. In finite-dimensional spaces this process terminates with a basis. (This uses the fact independent lists have length ≤ dim V.)

3. Uniqueness of representation in independent lists:
   - If (v1,...,vn) is independent and v ∈ span(v1,...,vn), then the coefficients in any expression v = a1 v1 + ... + an vn are unique. Proof: subtract two expressions to get a dependence; independence forces the difference coefficients to be zero.

4. Dependence detection shortcuts:
   - If some vi = 0 then the list is dependent.
   - If any vi lies in the span of the preceding vectors, the whole list is dependent (and that vi is redundant).
   - In coordinate terms, if columns (or rows, depending how you set up) of a matrix are linearly dependent then the rank is less than the number of columns.

Examples of application
- To prove a long list of vectors is dependent, show one vector is a linear combination of earlier ones (or show the list length exceeds the known dimension).
- To produce a basis from a generating list, perform row-reduction on the matrix of coordinates and select columns with pivots; those columns correspond to an independent sublist that spans.

Short proofs of central facts
- Dependence implies some vector is combination of others (finite case): Suppose a1 v1 + ... + an vn = 0 with some ai ≠ 0. Let k be an index with ak ≠ 0. Solve for vk: vk = −(a1/ak) v1 − ... − (a_{k-1}/ak) v_{k-1} − (a_{k+1}/ak) v_{k+1} − ... − (an/ak) vn. So vk lies in the span of the other vectors.

- Removing such a vk does not change the span: any linear combination of all vectors can be rewritten using the expression for vk in terms of the rest, so span stays the same.

Summary of practical workflow
- To check independence: set up coefficients or matrix, row-reduce, look for nontrivial solutions or missing pivots.
- To simplify a spanning list to a basis: remove vectors that are linear combinations of earlier ones (or use pivot columns from row-reduction).
- Use the length-vs-dimension rule to get quick dependence conclusions.

These are the concrete, usable consequences of linear dependence/independence for finite lists: dependence gives explicit redundancy (one vector expressible from others), independence guarantees uniqueness of coefficients, and both properties guide algorithms to find bases and determine spans.

Concept: Spanning Lists and Their Properties

Definitions (recall)
- A list v1,...,vm in a vector space V spans V if span(v1,...,vm) = V, i.e., every vector of V is a linear combination of v1,...,vm.
- A list is linearly dependent if some nontrivial linear combination of its vectors equals 0; otherwise it is linearly independent.

Key results and how to use them

1) Removing a vector that is a linear combination of the others does not change the span.
- Statement: If vk is in span(v1,...,vk−1,vk+1,...,vm) then span(v1,...,vm) = span(v1,...,vk−1,vk+1,...,vm).
- Reason: Any linear combination that uses vk can be rewritten by substituting the representation of vk in terms of the other vectors, so nothing new is produced by keeping vk.
- Use: When simplifying a spanning list, you may discard any vector that is a linear combination of the remaining ones without shrinking the span.

2) Adding a vector that lies in the span does not change the span.
- Statement: If u ∈ span(v1,...,vm), then span(v1,...,vm,u) = span(v1,...,vm).
- Reason: u is already expressible by the v’s, so adding u cannot enlarge the set of linear combinations.
- Use: If you try to enlarge a spanning set but the new vector is redundant (lies in the span), you have not increased the span.

3) If adding a vector to a list produces linear dependence, that new vector lies in the span of the original list.
- Statement: Suppose v1,...,vm are given and u is any vector. If v1,...,vm,u are linearly dependent but v1,...,vm are linearly independent, then u ∈ span(v1,...,vm).
- Reason: Linear dependence of the extended list gives a nontrivial relation with u; solve for u in terms of the v’s.
- Use: To test if u enlarges an independent list into a bigger independent set: u does so iff u ∉ span(v1,...,vm).

4) If a list spans and one vector of the list is expressible in terms of the others, then the list is linearly dependent.
- Statement: If v1,...,vm spans V and some vk ∈ span(v1,...,vk−1,vk+1,...,vm), then v1,...,vm is linearly dependent.
- Reason: The representation of vk as a combination of the others gives a nontrivial relation among the list.
- Use: Redundancy in a spanning list signals linear dependence; you can often remove such vk without losing the spanning property (by item 1).

5) From any spanning list one can extract a basis (finite-dimensional case).
- Statement: If V is finite-dimensional and v1,...,vm spans V, then one can remove some of the vectors (those that are linear combinations of earlier ones) to obtain a linearly independent spanning list — hence a basis.
- Construction/Reason: Go through v1,...,vm in order, keep a vector only if it is not in the span of the previously kept ones. Because V is finite-dimensional, this process terminates with a finite independent spanning set.
- Use: This is the standard method to turn any spanning list into a basis; it shows every finite spanning list contains a basis.

6) Spanning lists and linear dependence interact via lengths (Steinitz-type consequence).
- Statement: In a finite-dimensional space V, any spanning list has length at least as large as any linearly independent list. Equivalently, every linearly independent list can be extended to a basis by adding vectors from any spanning list.
- Reason sketch: Replace vectors of the spanning list one by one by vectors from the independent list, preserving the span at each step (exchange argument). The process shows the spanning list cannot be shorter than the independent list.
- Use: This gives lower bounds on lengths of spanning sets and shows why bases all have the same size (finite dimension is well-defined).

Examples and typical applications
- Simplifying a spanning set: Given a spanning list, scan and remove any vector that lies in the span of the previous kept ones. The result is a basis.
- Testing redundancy: If adding u to a spanning set does not increase span, then u was redundant (u ∈ span of the set).
- Extending independence to a basis: Given an independent list, add vectors from a spanning list until you span V. Each added vector must lie outside the span of previously chosen ones.

Short proofs (sketches)
- Proof of (1): Suppose vk = a1v1 + ... + ak−1vk−1 + ak+1vk+1 + ... + amvm. Any combination ∑ ci vi can be rewritten eliminating vk using that relation, so every vector in span(v1,...,vm) is in span of the list without vk; the reverse inclusion is trivial.
- Proof of (3): Linear dependence of v1,...,vm,u gives scalars not all zero with ∑ ci vi + c u = 0. If c = 0 then the original v’s were dependent; so c ≠ 0 and u = −(1/c)∑ ci vi, hence u ∈ span(v1,...,vm).

Takeaway
- Spanning is preserved when you remove vectors that are linear combinations of the others and when you add vectors already in the span. These facts give practical procedures: prune spanning lists to bases, and test whether a candidate vector enlarges an independent set by checking membership in the current span.

Definition
- Let V and W be vector spaces over the same field F. A function T: V → W is a linear map (or linear transformation) if for all u, v in V and all scalars a in F:
  1) T(u + v) = T(u) + T(v)   (additivity)
  2) T(a v) = a T(v)         (homogeneity / scalar compatibility)

Equivalently, T is linear iff for all u, v in V and all scalars a, b in F,
  T(a u + b v) = a T(u) + b T(v).

Quick checks to verify linearity
1. Check additivity and homogeneity separately (use arbitrary u, v and scalar a). If either fails for some choice, T is not linear.
2. Use the combined property: verify T(a u + b v) = a T(u) + b T(v) for arbitrary a, b and u, v — often quicker in calculations.
3. Test the zero vector: a linear map must satisfy T(0) = 0 (this follows from homogeneity: T(0)=T(0·v)=0·T(v)=0). If T(0) ≠ 0, T is not linear.
4. Test scalar-zero behavior: T(0·v) = 0 must hold. If T(c v) ≠ c T(v) for some scalar c (including c = 0), T fails linearity.
5. If V is finite-dimensional, it suffices to check the linearity condition on a basis: define T on basis vectors and verify T extends linearly (i.e., check T(∑ a_i e_i) = ∑ a_i T(e_i)).

Worked examples
- Example 1: T: R^2 → R^2 given by T(x, y) = (2x − y, 3y).  
  Check additivity and homogeneity (componentwise): linear because each component is a linear combination of x and y with no constant term. Equivalently, T corresponds to a matrix, so T is linear.

- Example 2: S: R^2 → R^2 given by S(x, y) = (x + 1, y).  
  Check zero: S(0,0) = (1,0) ≠ (0,0), so S is not linear (it is an affine map, not linear).

- Example 3: U: R → R given by U(t) = t^2.  
  Homogeneity fails: U(2·1) = 4 but 2·U(1) = 2, so U is not linear.

- Example 4: P: P2 → P2 (polynomials degree ≤ 2) defined by P(p)(x) = p'(x) (the derivative).  
  Derivative is linear: (p+q)' = p' + q' and (a p)' = a p'.

Common pitfalls
- Presence of a constant term (nonzero value at 0) immediately disqualifies linearity.
- Nonlinear operations like multiplication of vector components (e.g., T(x,y) = (xy, x)) are not linear in general.
- Verifying only one of additivity or homogeneity is insufficient; both must hold.

Procedure to show nonlinearity with a counterexample
- Find specific u, v or scalar a such that either T(u+v) ≠ T(u)+T(v) or T(a v) ≠ a T(v). A single counterexample disproves linearity.

Procedure to prove linearity
- Either show the two defining properties for arbitrary vectors and scalars, or express T as multiplication by a matrix (or show T respects linear combinations) and derive the equalities for general a, b and u, v.

Matrix representation of a linear map (with respect to bases)

Let V and W be finite-dimensional vector spaces. Choose an ordered basis B = (v1, …, vn) of V and an ordered basis C = (w1, …, wm) of W. For a linear map T : V → W the choice of bases identifies T with an m×n matrix as follows.

- Form the columns: for each basis vector vj of V compute T(vj) ∈ W and express it in the basis C:
  T(vj) = a1j w1 + a2j w2 + … + amj wm.
  The j-th column of the matrix [T]_{C,B} is the column vector (a1j, a2j, …, amj)^T.
  Equivalently, the (i,j)-entry of the matrix is aij, the i-th coordinate of T(vj) with respect to C.

- Coordinate action: if x ∈ V has coordinate column vector [x]_B = (x1, …, xn)^T (so x = Σ xj vj), then
  [T(x)]_C = [T]_{C,B} · [x]_B.
  To obtain the actual vector T(x) in W, convert the coordinate vector [T(x)]_C back to the basis C:
  T(x) = Σ i ([T(x)]_C)_i wi.

Thus the matrix [T]_{C,B} completely encodes T once bases are fixed; applying T corresponds to multiplying the matrix by the coordinate vector of the input.

Worked example
- Let V = W = R^2. Take basis B = (v1=(1,0), v2=(1,1)) of V and use the standard basis C = (e1=(1,0), e2=(0,1)) of W. Define T(x,y) = (2x+y, x+3y).
- Compute columns:
  T(v1)=T(1,0)=(2,1) → first column = (2,1)^T.
  T(v2)=T(1,1)=(3,4) → second column = (3,4)^T.
  So [T]_{C,B} = [[2,3],[1,4]] (columns written left-to-right).
- Apply T to v = (2,3) ∈ V:
  first express v in basis B: find a,b with a v1 + b v2 = (2,3). Solving gives b = 3, a = -1, so [v]_B = (-1,3)^T.
  Multiply: [T(v)]_C = [T]_{C,B} · [v]_B = [[2,3],[1,4]] · [-1,3]^T = (7,11)^T.
  Convert back (here C is standard) to get T(v) = (7,11).

Key point: once bases are chosen, linear maps ↔ matrices; matrix multiplication on coordinate vectors computes outputs.

Composition and Identity Maps; Matrix Multiplication Link

Definitions
- Composition. If S : V → W and T : W → U are maps between vector spaces over a field F, the composition T ∘ S : V → U is defined by (T ∘ S)(v) = T(S(v)) for all v ∈ V.
- Identity map. For a vector space V, the identity map I_V : V → V is defined by I_V(v) = v for all v ∈ V.

Linearity preserved under composition
Claim: If S : V → W and T : W → U are linear maps, then T ∘ S : V → U is linear.

Proof:
Let a, b ∈ F and v, w ∈ V. Using linearity of S and T,
(T ∘ S)(a v + b w) = T(S(a v + b w))
= T(a S(v) + b S(w))       (S is linear)
= a T(S(v)) + b T(S(w))   (T is linear)
= a (T ∘ S)(v) + b (T ∘ S)(w).
Thus T ∘ S is linear. Also, the identity map I_V is linear because I_V(a v + b w) = a v + b w = a I_V(v) + b I_V(w).

Connection with matrices (finite-dimensional case)
Let V, W, U be finite-dimensional with bases
B = (v1, …, vn) for V,
C = (w1, …, wm) for W,
D = (u1, …, up) for U.
Let S : V → W and T : W → U be linear. Denote by [S]_{B}^{C} the m×n matrix of S with respect to B (domain) and C (codomain), and by [T]_{C}^{D} the p×m matrix of T with respect to C and D.

Recall: the jth column of [S]_{B}^{C} is the coordinate vector of S(vj) relative to C; the jth column of [T]_{B}^{D} would be the coordinates of (T ∘ S)(vj) relative to D.

Compute the matrix of the composition. For each basis vector vj of V,
(S(vj))_C = jth column of [S]_{B}^{C}.
Applying T and expressing in basis D,
(T(S(vj)))_D = [T]_{C}^{D} · (S(vj))_C.
Hence the jth column of [T ∘ S]_{B}^{D} equals [T]_{C}^{D} times the jth column of [S]_{B}^{C}. Since this holds for every column j, we obtain the matrix product relation
[T ∘ S]_{B}^{D} = [T]_{C}^{D} · [S]_{B}^{C}.

Remarks
- The identity map corresponds to the identity matrix: [I_V]_{B}^{B} = I_n (the n×n identity matrix).
- This columnwise derivation explains why composition of linear maps corresponds to multiplication of their matrices and why matrix multiplication is defined as it is.

Null space and range (image)

Definition
- Let V and W be vector spaces and T: V → W be a linear map.
  - The null space (kernel) of T is Null(T) = {v ∈ V : T(v) = 0_W}.
  - The range (image) of T is Range(T) = {w ∈ W : there exists v ∈ V with T(v) = w} = T(V).

Null(T) is a subspace of V
- Need to check nonempty, closed under addition and scalar multiplication.
  - Nonempty: 0_V ∈ Null(T) because T(0_V) = 0_W by linearity.
  - Closed under addition: if u, v ∈ Null(T) then T(u+v) = T(u)+T(v) = 0_W + 0_W = 0_W, so u+v ∈ Null(T).
  - Closed under scalar multiplication: if v ∈ Null(T) and α ∈ F then T(αv) = αT(v) = α0_W = 0_W, so αv ∈ Null(T).
- Therefore Null(T) is a subspace of V.

Range(T) is a subspace of W
- Need to check nonempty, closed under addition and scalar multiplication.
  - Nonempty: T(0_V) = 0_W so 0_W ∈ Range(T).
  - Closed under addition: if w1, w2 ∈ Range(T) there exist v1, v2 ∈ V with T(v1)=w1 and T(v2)=w2. Then w1+w2 = T(v1)+T(v2) = T(v1+v2), so w1+w2 ∈ Range(T).
  - Closed under scalar multiplication: if w ∈ Range(T) with w = T(v), then αw = αT(v) = T(αv), so αw ∈ Range(T).
- Therefore Range(T) is a subspace of W.

Concrete examples

1) Matrix map R^3 → R^2
- Let T: R^3 → R^2 given by matrix A = [[1, 2, -1], [0, 1, 3]] so T(x) = A x for x = (x1,x2,x3)^T.
- Solve Null(T): A x = 0 gives
  1) x1 + 2x2 - x3 = 0
  2)      x2 + 3x3 = 0
  From (2): x2 = -3x3. Then (1): x1 + 2(-3x3) - x3 = x1 -7x3 = 0, so x1 = 7x3.
  Let parameter t = x3. Then Null(T) = {(7t, -3t, t) : t ∈ R} = span{(7,-3,1)}.
- Compute Range(T): columns of A span Range(T). Columns are c1=(1,0), c2=(2,1), c3=(-1,3).
  Note c3 = -c1 + 3 c2? Check: -c1 + 3 c2 = -(1,0)+3(2,1) = (-1+6, 0+3) = (5,3) not equal. Find linear dependence: solve α c1 + β c2 + γ c3 = 0. But rank is at most 2; compute that c1 and c2 are independent, so Range(T)=span{(1,0),(2,1)} which is all of R^2 (since these two are independent). Conclude Range(T)=R^2.
  (Alternatively compute row-reduced form of A to see rank 2.)

2) Differentiation on polynomials
- Let V = P3 (polynomials degree ≤ 3) and T: V → P2 given by T(p) = p′.
- Null(T): p′ = 0 means p is constant, so Null(T) = {constant polynomials} = span{1}. It's a 1-dimensional subspace.
- Range(T): derivatives of degree ≤3 polynomials are all polynomials of degree ≤2, so Range(T) = P2. Thus Range(T) is the whole codomain P2.

3) Projection map R^2 → R^2
- Let T(x,y) = (x,0) (projection onto x-axis).
- Null(T): T(x,y) = (0,0) iff x = 0, so Null(T) = {(0,y): y ∈ R} = span{(0,1)}.
- Range(T): all vectors of form (x,0) so Range(T) = {(x,0): x ∈ R} = span{(1,0)}.

Remarks on computation
- To find Null(T) for a matrix map, solve A x = 0 (Gaussian elimination); the solution space is a subspace, typically described by free parameters and basis vectors.
- To find Range(T) for a matrix map, take the column space: Range(T) = span{columns of A}; a basis can be taken from the pivot columns after row reduction.
- For operators like differentiation or evaluation, use the defining formula: Null consists of inputs mapped to zero, Range consists of all possible outputs.

Section 17 — Injective, Surjective, and Invertible Linear Maps

Definitions
- Let V and W be vector spaces over the same field and T : V → W a linear map.
  - T is injective (one-to-one) if T(v1) = T(v2) implies v1 = v2 for all v1, v2 ∈ V.
  - T is surjective (onto) if for every w ∈ W there exists v ∈ V with T(v) = w.
  - T is invertible if there exists a map S : W → V such that S ◦ T = I_V and T ◦ S = I_W. Such an S is called the inverse of T and is denoted T^{-1}.

Characterizations using null space and range
- The null space (kernel) of T is null T = {v ∈ V : T(v) = 0}.  
- The range (image) of T is range T = T(V) = {T(v) : v ∈ V} ⊆ W.

Propositions and proofs

1) Injectivity ⇔ null T = {0}.
Proof:
- (⇒) If T is injective and v ∈ null T, then T(v) = 0 = T(0). By injectivity v = 0, so null T = {0}.
- (⇐) If null T = {0} and T(v1) = T(v2), then T(v1 − v2) = T(v1) − T(v2) = 0, so v1 − v2 ∈ null T. Hence v1 − v2 = 0 and v1 = v2, so T is injective. □

2) Surjectivity ⇔ range T = W.
Proof:
- Immediate from the definitions: T is surjective exactly when every w ∈ W is in T(V), i.e. range T = W. □

3) If T has a (two-sided) inverse S (so S ◦ T = I_V and T ◦ S = I_W), then S is linear and the inverse is unique.
Proof:
- Uniqueness: If S and S' both satisfy S ◦ T = I_V and S' ◦ T = I_V, then for any w ∈ W choose v with T(v) = w (possible if T is surjective). Then S(w) = S(T(v)) = v = S'(T(v)) = S'(w). Thus S = S'.
- Linearity: For w1, w2 ∈ W and scalar α, write w_i = T(v_i) because T ◦ S = I_W implies T is surjective (alternatively assume surjectivity as part of invertibility). Then
  S(w1 + w2) = S(T(v1 + v2)) = v1 + v2 = S(w1) + S(w2),
  S(αw1) = S(T(αv1)) = αv1 = αS(w1).
  So S is linear. □

4) T is invertible ⇔ T is both injective and surjective.
Proof:
- (⇒) If T is invertible with inverse S, then S ◦ T = I_V implies T is injective (because a left inverse forces injectivity), and T ◦ S = I_W implies T is surjective (because a right inverse forces surjectivity).
- (⇐) If T is injective and surjective, define S : W → V as follows: for w ∈ W, choose the unique v ∈ V with T(v) = w (existence by surjectivity, uniqueness by injectivity), and set S(w) = v. This S is well-defined and linear: for w1 = T(v1), w2 = T(v2),
  S(w1 + w2) = S(T(v1) + T(v2)) = S(T(v1 + v2)) = v1 + v2 = S(w1) + S(w2),
  and similarly for scalars. Finally S ◦ T = I_V and T ◦ S = I_W by construction, so S = T^{-1}. □

Corollaries and useful facts
- Existence of a left inverse (S with S ◦ T = I_V) implies T is injective. Existence of a right inverse (S with T ◦ S = I_W) implies T is surjective.
- If a linear map has either a left inverse or a right inverse, that inverse is necessarily linear (when defined on all of W or V as appropriate) and in the presence of both sides they coincide and are unique.
- For finite-dimensional spaces with dim V = dim W, injectivity, surjectivity, and invertibility are all equivalent for linear maps V → W (this follows from rank-nullity and the two characterizations above).

This completes the basic definitions and equivalences relating injective, surjective, and invertible linear maps via null space and range.

Isomorphism — definition
- An isomorphism between vector spaces V and W (over the same field F) is a linear map T: V → W that is bijective. When such a T exists we say V and W are isomorphic and write V ≅ W.

Basic consequences for finite-dimensional spaces

1) Isomorphism preserves dimension
- Proposition. If V and W are finite-dimensional and V ≅ W, then dim V = dim W.
- Proof. Let T: V → W be an isomorphism. If {v1,...,vn} is a basis of V then {T(v1),...,T(vn)} is a basis of W:
  - Linearly independent: if a1T(v1)+...+anT(vn)=0 then T(a1v1+...+anvn)=0, so a1v1+...+anvn=0 (injectivity of T), hence all ai=0.
  - Spanning: for any w in W pick v in V with T(v)=w (surjectivity). Write v = b1v1+...+bnvn; then w = T(v) = b1T(v1)+...+bnT(vn).
  Thus W has a basis of size n, so dim W = n = dim V.

2) Equal finite dimensions imply existence of isomorphism
- Proposition. If V and W are finite-dimensional with dim V = dim W = n, then V ≅ W.
- Proof sketch. Choose bases {v1,...,vn} of V and {w1,...,wn} of W. Define T by T(∑ aivi) = ∑ aiwi. This is linear, clearly bijective (inverse defined by sending wi to vi), so an isomorphism.

3) Basis correspondence characterization
- Proposition. For finite-dimensional V and W, a linear map T: V → W is an isomorphism iff it sends some (equivalently any) basis of V to a basis of W.
- Proof. If T is an isomorphism and {v1,...,vn} is a basis of V then {T(vi)} is a basis of W (argument in (1)). Conversely, if {T(vi)} is a basis of W then T is surjective; since domain and codomain have equal finite dimension, surjectivity implies injectivity (or check injectivity directly from linear independence), so T is bijective.

4) Immediate corollaries used often
- Any n-dimensional vector space over F is isomorphic to F^n (take a basis and map it to the standard basis of F^n).
- For linear maps between finite-dimensional spaces of the same dimension, injective ⇔ surjective ⇔ bijective ⇔ isomorphism.
- Two vector spaces are isomorphic exactly when they have the same dimension (finite-dimensional case).

Example (construction): To build an isomorphism V → W when dim V = dim W = n, pick bases and map basis vectors of V to basis vectors of W coordinatewise. This gives an explicit invertible linear map.

Vector space of polynomials P(F)

Definition
- Fix a field F. A polynomial over F is a formal expression a0 + a1 x + a2 x^2 + ... + an x^n where n is a nonnegative integer and the coefficients ai lie in F. Equivalently, a polynomial is a sequence (a0, a1, a2, ...) with only finitely many nonzero terms.
- Denote by P(F) the set of all such polynomials.

Vector-space structure
- Addition: add polynomials coefficientwise: (a0 + a1 x + ... ) + (b0 + b1 x + ... ) = (a0 + b0) + (a1 + b1) x + ....
- Scalar multiplication: for λ in F, λ(a0 + a1 x + ... ) = (λa0) + (λa1) x + ....
- With these operations P(F) satisfies the vector-space axioms over F (closure, associativity, commutativity of addition, existence of additive identity 0 polynomial, additive inverses, distributivity, etc.). Thus P(F) is a vector space over F.

Degree
- If p(x) = a0 + a1 x + ... + an x^n with an ≠ 0, the degree deg p is n. The zero polynomial is conventionally assigned deg 0 or deg(0) = −∞ depending on convention; the convenient convention when discussing subspaces is to treat the zero polynomial separately as having no well-defined finite degree.
- Degree properties: deg( p + q ) ≤ max(deg p, deg q) and deg(λ p) = deg p for λ ≠ 0.

Standard monomials, spanning, and linear independence
- The standard monomials 1, x, x^2, x^3, ... (where 1 = x^0) are elements of P(F).
- Spanning: Every polynomial p(x) = a0 + a1 x + ... + an x^n is a finite F-linear combination of these monomials: p = a0·1 + a1·x + ... + an·x^n. Hence {1, x, x^2, ...} spans P(F).
- Linear independence: The monomials are linearly independent. If c0·1 + c1·x + ... + cN·x^N = 0 (the zero polynomial), then comparing coefficients gives c0 = c1 = ... = cN = 0. So no nontrivial finite linear relation exists among distinct monomials.
- Basis and dimension: Because the monomials both span and are linearly independent, they form a basis of P(F). Since the basis is infinite, P(F) is an infinite-dimensional vector space.
- Finite-degree subspaces: For each n ≥ 0 define Pn(F) = {p in P(F) : deg p ≤ n}. The set {1, x, ..., x^n} is a basis of Pn(F), so dim Pn(F) = n + 1.

Evaluation map and its linearity

Fix a scalar λ in the field F. Define Evλ: P(F) → F by Evλ(p) = p(λ). (Here P(F) denotes the vector space of polynomials with coefficients in F; the same remarks below apply to the subspace Pn of polynomials of degree ≤ n when that is intended.)

Linearity
For p, q ∈ P(F) and a ∈ F,
Evλ(p + q) = (p + q)(λ) = p(λ) + q(λ) = Evλ(p) + Evλ(q),
Evλ(a p) = (a p)(λ) = a p(λ) = a Evλ(p).
Thus Evλ is a linear map from P(F) to F.

Kernel and range
- Kernel: ker(Evλ) = {p ∈ P(F) : p(λ) = 0}. Equivalently, ker(Evλ) is the ideal of polynomials divisible by (x − λ). In particular every p in ker(Evλ) can be written p(x) = (x − λ)q(x), and for Pn (degree ≤ n) the kernel is precisely {(x − λ)q : q ∈ Pn−1}. So ker(Evλ) consists exactly of the polynomials having λ as a root.
- Range: Evλ is surjective onto F because any scalar c ∈ F is Evλ(constant polynomial c). Hence range(Evλ) = F.

Linear-map viewpoint and consequences
- Codimension and dimension: Because range(Evλ)=F is one-dimensional, ker(Evλ) has codimension 1 in Pn: if dim Pn = n+1 then dim ker(Evλ) = n and rank(Evλ) = 1, consistent with the rank–nullity theorem.
- Roots and factorization: The statement “λ is a root of p” is exactly the statement “p ∈ ker(Evλ)”. The characterization ker(Evλ) = (x − λ)P(F) expresses the familiar factor theorem in linear-algebraic language: having λ as a root means being in the subspace (ideal) generated by (x − λ).
- Quotient and isomorphism: By the First Isomorphism Theorem,
P(F)/ker(Evλ) ≅ range(Evλ) = F.
So modulo the polynomials that vanish at λ, every polynomial is equivalent to a unique scalar (its value at λ).
- Finite-degree counting: For Pn, the kernel being {(x − λ)q : q ∈ Pn−1} shows that evaluating at λ “loses” one degree of freedom: specifying a polynomial of degree ≤ n up to membership in ker(Evλ) is the same as specifying its value at λ.
- Multiplicity perspective: If one is interested in multiplicity m of λ as a root of p, this can be expressed by membership in higher kernels: λ has multiplicity at least m in p iff p lies in the subspace (x − λ)^m P(F). Thus successive powers of the evaluation-related ideals capture higher-order vanishing.

These observations show how a simple evaluation map ties the elementary notion of roots and divisibility of polynomials to standard linear-algebraic ideas of kernel, range, quotient, and dimension.

Section 21 — Division Algorithm and Remainder/Factor Theorems

Division Algorithm for Polynomials (existence and uniqueness)
- Statement. Let p(x) and s(x) be polynomials over a field F, with s(x) ≠ 0. There exist unique polynomials q(x) (the quotient) and r(x) (the remainder) in F[x] such that
  p(x) = q(x) s(x) + r(x)
and either r(x) = 0 or deg r < deg s.

- Existence (sketch). Perform the usual polynomial long division: if deg p < deg s take q = 0, r = p. Otherwise, let a x^m be leading term of p and b x^n leading term of s with m ≥ n; subtract (a/b) x^{m−n} s(x) from p(x) to cancel the leading term. Repeat on the remainder; degrees strictly decrease so the process terminates with a remainder of smaller degree than s.

- Uniqueness (proof). Suppose p = q1 s + r1 = q2 s + r2 with deg r1, deg r2 < deg s. Then (q1 − q2) s = r2 − r1. If q1 ≠ q2 then left side has degree ≥ deg s while right side has degree < deg s, contradiction. Hence q1 = q2 and r1 = r2.

Using the Division Algorithm
- To compute q and r: use polynomial long division or synthetic division (when s(x) is linear x − λ).
- Consequence: for division by a nonzero constant c, q = (1/c) p and r = 0. For division by a monic polynomial s of degree k, deg q = deg p − k (when deg p ≥ k).

Remainder Theorem
- Statement. For any polynomial p(x) and any scalar λ in F, the remainder when p(x) is divided by (x − λ) equals p(λ).

- Derivation. Apply the division algorithm with s(x) = x − λ: p(x) = q(x)(x − λ) + r(x). Since deg r < deg(x − λ) = 1, r is a constant c. Substitute x = λ: p(λ) = q(λ)·0 + c = c. Hence remainder = p(λ).

- Practical use. To find the remainder of p(x) upon division by x − λ, evaluate p(λ) instead of performing full division.

Factor Theorem
- Statement. A scalar λ is a root of p (p(λ) = 0) if and only if (x − λ) is a factor of p(x).

- Proof. From the division algorithm with s(x) = x − λ, p(x) = q(x)(x − λ) + c where c = p(λ). If p(λ) = 0 then c = 0, so p(x) = q(x)(x − λ), meaning x − λ divides p. Conversely, if x − λ divides p then p(x) = (x − λ) q(x) so p(λ) = 0.

- Use. Roots correspond exactly to linear factors. If λ1, …, λm are distinct roots of p and p is nonzero, (x − λ1)…(x − λm) divides p. Multiplicity: if (x − λ)^k divides p but (x − λ)^{k+1} does not, then λ is a root of multiplicity k.

Examples
1) Divide p(x) = 2x^3 + 3x^2 − x + 5 by s(x) = x − 2. Synthetic division or evaluation gives remainder p(2) = 2·8 + 3·4 − 2 + 5 = 16 + 12 − 2 + 5 = 31. So p(x) = q(x)(x − 2) + 31.

2) If p(x) = x^3 − 4x^2 + x + 6, check λ = 1: p(1) = 1 − 4 + 1 + 6 = 4 ≠ 0, so x − 1 is not a factor. For λ = −1: p(−1) = −1 − 4(1) − 1 + 6 = 0, so x + 1 divides p. One can then divide to find the quadratic quotient.

Important consequences to remember
- Division algorithm guarantees both existence and uniqueness of quotient and remainder.
- Remainder theorem lets you replace division by x − λ with evaluation p(λ).
- Factor theorem links zeros of p to linear factors (and multiplicity to powers of (x − λ)) — a fundamental tool for factoring polynomials and counting roots.

Polynomials applied to linear operators (minimal polynomial setup)

- Definition of p(T). Let V be a vector space over field F and T ∈ L(V). For a polynomial p(z) = a0 + a1 z + ... + an z^n ∈ F[z], define the operator p(T) ∈ L(V) by
  p(T) = a0 I + a1 T + a2 T^2 + ... + an T^n,
  where I is the identity operator on V and T^k denotes the k-fold composition of T (with T^0 = I). Thus p(T) acts on v ∈ V by p(T)v = a0 v + a1 T v + ... + an T^n v.

- Homomorphism properties. The map Φ: F[z] → L(V) given by Φ(p) = p(T) is an algebra homomorphism:
  - Linearity: for p,q ∈ F[z] and scalar α ∈ F,
    Φ(p + q) = p(T) + q(T) and Φ(α p) = α p(T).
  - Multiplicativity: Φ(p q) = p(T) q(T) = p(T) ∘ q(T). This holds because composition of powers corresponds to adding exponents: (z^j z^k)(T) = T^{j+k} = T^j ∘ T^k.
  - Identity: Φ(1) = I and Φ(z) = T.
  These facts show Φ respects addition, scalar multiplication, and multiplication, so it is a linear-map algebra homomorphism from the polynomial algebra F[z] into the algebra L(V).

- Annihilating polynomials. A nonzero polynomial p ∈ F[z] is said to annihilate T, or to be an annihilating polynomial for T, if p(T) = 0 (the zero operator). Equivalently, every vector v ∈ V satisfies p(T)v = 0.

- Minimal polynomial. Among all nonzero polynomials that annihilate T, one can consider those of smallest degree. Any nonzero annihilating polynomial of least degree is called a minimal polynomial of T. The minimal polynomial is unique up to multiplication by a nonzero scalar; it is common to choose the unique monic polynomial of least degree that annihilates T and call that the minimal polynomial of T.

Roots (zeros) and multiplicity

- Root (zero). Let F be a field and p(z) a polynomial in F[z]. A ∈ F is called a root (or zero) of p if p(A) = 0.

- Multiplicity. A root A has multiplicity m ≥ 1 if (z − A)^m divides p(z) but (z − A)^(m+1) does not. Equivalently, write p(z) = (z − A)^m q(z) with q(A) ≠ 0; then m is the multiplicity of A. A root with multiplicity 1 is called simple; multiplicity >1 is a repeated root.

Factorization into linear factors

- Over a field F that contains all the roots of p (for example C for complex-coefficient polynomials), any polynomial p of degree n factors as
  p(z) = c (z − r1)(z − r2) ··· (z − rn),
  where c ∈ F is the leading coefficient and r1,…,rn ∈ F are the roots counted with multiplicity. If some root repeats, the corresponding factor appears with that multiplicity. If F does not contain all roots, p may not factor completely into linear factors over F, but it always factors into irreducible factors over F.

Bounding the number of distinct roots by the degree

- Theorem. A nonzero polynomial p(z) ∈ F[z] of degree n has at most n distinct roots in F.

- Proof (division argument). Suppose p has distinct roots A1,…,Ak. For each i, z − Ai divides p(z). Because z − A1, …, z − Ak are pairwise relatively prime, their product (z − A1)·…·(z − Ak) divides p(z). Thus k ≤ deg p = n. (One can make this precise by induction or using the division algorithm: if A is a root, divide p by (z − A) to reduce degree by at least 1, then repeat.)

Consequences and reasoning about repeated roots

- Counting with multiplicity. When one counts roots with multiplicity, the total number of roots of p equals deg p once p is factored completely over a field containing all roots: multiplicities add to the degree.

- Repeated roots and the derivative. If A is a root of multiplicity m ≥ 1 of p, then A is a root of multiplicity m − 1 of p′ (the formal derivative). In particular:
  - A is a repeated root of p (m ≥ 2) if and only if A is a common root of p and p′.
  - Therefore, gcd(p, p′) ≠ 1 exactly when p has a repeated root in an algebraic closure of F.

- Characteristic issues. Over fields of characteristic 0 (e.g., Q, R, C) the derivative test works as above. In characteristic p > 0 there are subtleties: e.g., the polynomial z^p − a has derivative 0, so derivative-based reasoning fails unless one checks separability. A polynomial whose derivative is identically 0 is a polynomial in z^p (so roots can have high multiplicity in a way tied to the field characteristic).

Examples
- p(z) = (z − 2)^3(z + 1) has degree 4, roots 2 (multiplicity 3) and −1 (multiplicity 1); counted with multiplicity there are 4 roots; counted distinctly there are 2 ≤ 4.
- Over R, z^2 + 1 has no real linear factors, but over C it factors as (z − i)(z + i), showing the role of the field containing the roots.

Key takeaways
- Roots are where p vanishes; multiplicity measures how strongly p vanishes there.
- A degree-n nonzero polynomial cannot have more than n distinct roots in a field.
- Over a field that contains all roots, a polynomial factors into linear factors whose multiplicities sum to the degree.
- Repeated roots are detected algebraically by common factors of p and p′ (with cautions in positive characteristic).

Section 24 — Polynomial interpolation: existence and uniqueness

Statement
Let F be a field (e.g. R or C). Fix n distinct points x1, x2, ..., xn in F and prescribed values y1, y2, ..., yn in F. Then

1) Uniqueness: There is at most one polynomial p of degree < n (i.e. deg p ≤ n−1) such that p(xi) = yi for i = 1,...,n.

2) Existence: There exists a polynomial p of degree < n with p(xi) = yi for i = 1,...,n. One explicit choice is given by the Lagrange interpolation polynomial
p(x) = sum_{j=1}^n y_j L_j(x),
where for each j
L_j(x) = ∏_{k ≠ j} (x − x_k) / ∏_{k ≠ j} (x_j − x_k).

Proof of uniqueness
Suppose p and q are two polynomials of degree < n with p(xi) = q(xi) = yi for all i. Then r := p − q is a polynomial of degree < n that vanishes at x1,...,xn. Since the xi are distinct, r has at least n distinct roots. But a nonzero polynomial of degree < n can have at most deg r < n roots, so r must be the zero polynomial. Hence p = q; uniqueness follows.

Construction and proof of existence (Lagrange interpolation)
Define, for each j = 1,...,n,
L_j(x) := ∏_{k ≠ j} (x − x_k) / ∏_{k ≠ j} (x_j − x_k).
Each L_j is a polynomial: the numerator is a polynomial of degree n−1 and the denominator is a nonzero scalar (because the xk are distinct), so L_j has degree ≤ n−1. Note that for i = 1,...,n,
- If i = j, then L_j(x_i) = 1 because the numerator becomes ∏_{k ≠ j} (x_j − x_k) which cancels the denominator.
- If i ≠ j, then L_j(x_i) = 0 because the numerator contains the factor (x_i − x_i) = 0.

Now set
p(x) := sum_{j=1}^n y_j L_j(x).
This p is a linear combination of polynomials of degree ≤ n−1, so deg p ≤ n−1. For each i,
p(x_i) = sum_{j=1}^n y_j L_j(x_i) = y_i·1 + sum_{j ≠ i} y_j·0 = y_i,
so p matches the prescribed values. Thus existence is proved.

Alternative viewpoint (linear-algebraic)
Let P_{n-1} denote the vector space of polynomials over F of degree < n. The evaluation map E: P_{n-1} → F^n defined by E(p) = (p(x1),...,p(xn)) is linear. Uniqueness is equivalent to E being injective; injectivity follows from the argument that a nonzero polynomial in P_{n-1} can have at most n−1 zeros, so if E(p) = 0 then p = 0. Since dim P_{n-1} = n and dim F^n = n, injectivity implies E is an isomorphism, hence surjective; therefore for every (y1,...,yn) ∈ F^n there exists p ∈ P_{n-1} with E(p) = (y1,...,yn). This gives another proof of existence.

Remarks
- The Lagrange formula yields an explicit polynomial of degree at most n−1.  
- If the field F has characteristic p > 0 and n exceeds p, the linear-algebraic dimension argument still applies as long as the xi are distinct (the cardinality n is just a dimension), but care is needed when interpreting "degree < n" in some modular contexts; the proofs above are valid over any field.

Characteristic polynomial — construction and how its roots give eigenvalues

Definition and construction
- For a linear operator T on an n-dimensional vector space V, pick any basis and let A be the n×n matrix representing T in that basis. The characteristic polynomial of T (or of A) is
  p(λ) = det(A − λI),
  where I is the n×n identity matrix and det denotes determinant.
- If T is given directly by a matrix A, you form A − λI and compute its determinant to obtain p(λ), a monic polynomial of degree n.
- The characteristic polynomial is independent of the chosen basis (conjugating A by an invertible change-of-basis matrix does not change det(A − λI)), so its roots are intrinsic to T.

Why the roots are eigenvalues
- A scalar λ is an eigenvalue of T precisely when there exists a nonzero vector v with T(v) = λv.
- In matrix terms with A the matrix of T, this means there is a nonzero vector v with (A − λI)v = 0, i.e. A − λI is singular.
- A square matrix is singular exactly when its determinant is zero. Thus λ is an eigenvalue ⇔ det(A − λI) = 0 ⇔ p(λ) = 0.
- Therefore the eigenvalues of T are exactly the roots of the characteristic polynomial. The multiplicity of a root in p(λ) is its algebraic multiplicity as an eigenvalue.

Worked example (full computation)
Let A = [[2, 1],
         [1, 2]].
We find the characteristic polynomial and eigenvalues, then compute eigenvectors.

1) Form A − λI:
   A − λI = [[2 − λ, 1],
             [1, 2 − λ]].

2) Compute the determinant p(λ) = det(A − λI):
   p(λ) = (2 − λ)(2 − λ) − 1·1
        = (2 − λ)^2 − 1
        = (4 − 4λ + λ^2) − 1
        = λ^2 − 4λ + 3.

3) Factor and find roots:
   λ^2 − 4λ + 3 = (λ − 1)(λ − 3).
   So the characteristic polynomial is p(λ) = λ^2 − 4λ + 3 and its roots are λ = 1 and λ = 3. These are the eigenvalues.

4) Find eigenvectors for each eigenvalue.
   - For λ = 1, solve (A − I)v = 0:
     A − I = [[1, 1],
              [1, 1]].
     The equations are x + y = 0 (both rows give the same equation). Thus y = −x, so eigenvectors are nonzero multiples of [1, −1]^T.
   - For λ = 3, solve (A − 3I)v = 0:
     A − 3I = [[−1, 1],
               [1, −1]].
     The equations are −x + y = 0, so y = x. Eigenvectors are nonzero multiples of [1, 1]^T.

Remarks
- The dimension of the eigenspace corresponding to a root λ (the geometric multiplicity) is at least 1 and at most the algebraic multiplicity of λ in p(λ).
- For n×n matrices, p(λ) has degree n and hence (over C) exactly n roots counting algebraic multiplicity; real matrices may have complex eigenvalues.

Criterion
A linear operator T on an n-dimensional vector space V is diagonalizable precisely when V has a basis consisting entirely of eigenvectors of T.

Equivalently for a matrix A representing T in some basis: A is diagonalizable iff there exists an invertible matrix P and a diagonal matrix D with
P^{-1}AP = D.
In this situation the columns of P form a basis of eigenvectors of A (and hence of T).

How the diagonal matrix arises
Suppose v1,...,vn is a basis of V and each vj is an eigenvector of T with T(vj) = λj vj. Write the coordinate vector of vj relative to this basis as the jth standard basis vector ej. Applying T to the basis vectors and expressing in the same basis gives
T(v1) = λ1 v1 = λ1 e1, ..., T(vn) = λn vn = λn en.
Thus the matrix of T with respect to the basis v1,...,vn has λ1,...,λn on the diagonal and zeros off the diagonal:
[D] = diag(λ1,...,λn).
If A is the matrix of T in some original basis and P is the change-of-basis matrix whose jth column is the coordinate vector of vj in that original basis, then P is invertible and
P^{-1}AP = D,
so A is similar to a diagonal matrix.

Useful consequences (brief)
- A necessary and sufficient practical test: T is diagonalizable iff there exist n linearly independent eigenvectors of T.
- In particular, if T has n distinct eigenvalues then it is diagonalizable, since eigenvectors corresponding to distinct eigenvalues are linearly independent.

Definition (linear operator). Let V be a vector space over a field F and T: V → V a linear map (a linear operator).

Eigenvalue and eigenvector.
- A scalar λ in F is an eigenvalue of T if there exists a nonzero vector v in V such that
  T v = λ v.
- Any nonzero v that satisfies T v = λ v is called an eigenvector of T corresponding to λ.
- Note: v must be nonzero; the zero vector always satisfies T0 = λ0, but it is not an eigenvector.

Eigenspace.
- For a given λ, the eigenspace Eλ is the set of all vectors v in V satisfying T v = λ v. Equivalently,
  Eλ = { v ∈ V : (T − λ I)v = 0 } = Null(T − λ I).
- Eλ is a subspace of V. λ is an eigenvalue exactly when Eλ ≠ {0}.

How to verify the eigenvector equation T v = λ v (general procedure).
1. Compute T v using the definition of T (or multiply the matrix of T by the coordinate vector of v when a basis is fixed).
2. Compute λ v by scalar multiplication.
3. Check whether the two resulting vectors are equal. If they are and v ≠ 0, then v is an eigenvector and λ is the corresponding eigenvalue.

Finding eigenvalues/eigenvectors (standard method).
- Solve (T − λ I)v = 0 for v ≠ 0. Nontrivial solutions exist exactly when det(T − λ I) = 0 (when V is finite-dimensional and a matrix for T is used). The polynomial det(T − λ I) is the characteristic polynomial; its roots are the eigenvalues.

Examples.

1) Matrix example in R^2.
- Let T be given by the matrix A = [[3, 1], [1, 3]] (with respect to the standard basis). Claim: eigenvalues 4 and 2 with eigenvectors proportional to (1, 1) and (1, −1) respectively.
  Verification for λ = 4, v = (1, 1):
  A v = [ [3,1],[1,3] ] [1,1]^T = [4,4]^T = 4 [1,1]^T = 4 v, so v is an eigenvector for eigenvalue 4.
  Verification for λ = 2, w = (1, −1):
  A w = [ [3,1],[1,3] ] [1,−1]^T = [2, −2]^T = 2 [1, −1]^T = 2 w, so w is an eigenvector for eigenvalue 2.

2) Operator on polynomials.
- Let V = P2(F) (polynomials of degree ≤ 2) and T: V → V be differentiation, T(p) = p′. If p is an eigenvector with eigenvalue λ, then p′ = λ p. This ODE implies p must be of the form c e^{λ x}, which is not a polynomial unless λ = 0 and p is constant. So the only eigenvalue is 0 with eigenspace = constant polynomials. Verification: for a constant c, T(c) = 0 = 0·c, so constants are eigenvectors for λ = 0.

Remarks.
- Eigenvectors depend on the field: an operator might have no eigenvalues over R but have eigenvalues over C.
- The eigenspace Eλ equals Null(T − λ I), so standard linear-algebra techniques for nullspaces find all eigenvectors for a given λ.

Eigenspace definition
- For a linear operator T on V and scalar λ, the eigenspace corresponding to λ is
  E_λ = { v ∈ V : T v = λ v }.
  (This set automatically contains 0, so it is the full eigenspace; nonzero elements of E_λ are eigenvectors.)

Eigenspaces are subspaces
- We check the subspace criteria.
  1. 0 ∈ E_λ because T0 = 0 = λ0.
  2. If u, v ∈ E_λ then T(u + v) = T u + T v = λ u + λ v = λ(u + v), so u + v ∈ E_λ.
  3. If v ∈ E_λ and α ∈ F (the field), then T(α v) = α T v = α λ v = λ(α v), so α v ∈ E_λ.
- Hence E_λ is closed under addition and scalar multiplication and contains 0, so E_λ is a subspace of V.

Eigenspaces are invariant under T
- If v ∈ E_λ then T v = λ v ∈ E_λ. Thus T(E_λ) ⊆ E_λ, so E_λ is invariant (T-stable).

Relation to the null space of (T − λI)
- For any v ∈ V, (T − λI)v = 0 exactly when T v = λ v. Therefore
  E_λ = null(T − λI).
- Equivalently, eigenvectors (nonzero) are precisely the nonzero vectors in null(T − λI).

Minimal polynomial and operator structure

Definition and basic facts
- The minimal polynomial m_T(x) of a linear operator T on a finite-dimensional vector space V is the unique monic polynomial of least degree with m_T(T)=0.
- deg m_T ≤ dim V. Every eigenvalue λ of T is a root of m_T. Conversely, every root of m_T is an eigenvalue of T.

How roots relate to eigenvalues
- If m_T(x) factors over the field as
  m_T(x) = (x − λ1)^{e1} ··· (x − λr)^{er},
  then the set {λ1,…,λr} is exactly the spectrum (the set of eigenvalues) of T.
- In particular, the multiplicity ei of (x−λi) in m_T is ≥1 and is determined by T: ei is the smallest exponent e such that (T − λi I)^e annihilates every vector in V.

Diagonalizability criterion
- T is diagonalizable iff m_T splits into distinct linear factors (i.e. every ei = 1):
  T diagonalizable ⇔ m_T(x) = (x − λ1)···(x − λr) with no repeated roots.
  Proof sketch: If m_T has distinct linear factors then by the Chinese remainder/primary decomposition argument V decomposes as a direct sum of kernels of (T−λi I), so T is a direct sum of scalar operators on those eigenspaces (hence diagonalizable). Conversely, if T is diagonalizable then T satisfies the polynomial ∏(x−λi) and minimality forces no repeated factors.

Primary decomposition and constraints on structure
- Primary decomposition: writing m_T as above with powers, V decomposes as a direct sum of T-invariant subspaces
  V = ⊕i V_{λi}, where V_{λi} = ker((T − λi I)^{ei}).
  Each V_{λi} is the primary (generalized eigenspace) subspace for λi, and the restriction T|_{V_{λi}} has minimal polynomial (x−λi)^{ei}.
- Structure constraint: the exponent ei equals the size of the largest Jordan block for eigenvalue λi (over an algebraically closed field). Thus the minimal polynomial records, for each eigenvalue, the maximal size of its Jordan chains — it does not record the number of blocks, only the largest block size.

Immediate consequences and useful deductions
- If m_T has no repeated root then T has no nontrivial generalized eigenvectors (all Jordan blocks are 1×1) — equivalently T is diagonalizable.
- If m_T(x) = (x − λ)^d (a single eigenvalue) then T = λI + N with N nilpotent of index d (N^d = 0 but N^{d−1} ≠ 0). So T is a single Jordan-type nilpotent perturbation of a scalar.
- If m_T factors as a product of k distinct linear factors then T has exactly k distinct eigenvalues; if k = dim V then T has a full set of eigenvectors (diagonalizable).
- Knowing m_T constrains possible Jordan forms: the largest Jordan block for each eigenvalue λi has size ei, and no block for λi can exceed ei. Any Jordan form consistent with these maximal sizes is possible over an algebraically closed field.
- If the field does not contain all roots of m_T, diagonalizability and Jordan form must be considered over an extension; but the minimal polynomial over the base field still detects repeated irreducible factors and the primary decomposition relative to those irreducible factors.

Examples (quick)
- m_T(x) = (x − 2)(x + 1) ⇒ eigenvalues 2 and −1, each with largest Jordan block size 1 ⇒ T diagonalizable with exactly two eigenvalues.
- m_T(x) = (x − 3)^3(x + 2) ⇒ eigenvalues 3 and −2; the largest Jordan block for 3 has size 3, so T is not diagonalizable; restriction to the 3-eigenspace is a 3-step nilpotent plus 3·I.

Practical use in problems
- To test diagonalizability: compute m_T (or show that T satisfies a polynomial with distinct linear factors) — distinct roots ⇔ diagonalizable.
- To bound Jordan block sizes: find the exponent of (x−λ) in m_T — that exponent is exactly the maximal Jordan block size for λ.
- To deduce the number of distinct eigenvalues: factor m_T and count distinct linear factors (over the field).

Summary line
The minimal polynomial encodes exactly which scalars are eigenvalues and, via the multiplicity of each linear factor, gives the maximal size of Jordan blocks for each eigenvalue; it therefore characterizes diagonalizability (distinct linear factors) and constrains the operator’s block structure.

Triangularization and existence of eigenvalues (over C)

Main structural result
- Theorem. If V is a finite-dimensional complex vector space and T: V → V is linear, then there exists a basis of V in which the matrix of T is upper triangular.
- Corollary. Every linear operator on a nonzero complex finite-dimensional space has at least one eigenvalue. In any upper-triangular matrix for T the diagonal entries are eigenvalues of T, so the existence of an upper-triangular form immediately gives an eigenvalue.

Why this holds (proof idea and mechanism)
1) Existence of an eigenvalue (one-dimensional invariant subspace).
- Start with any nonzero vector v ∈ V. Consider the list v, Tv, T^2v, … . Because V is finite-dimensional, these vectors are linearly dependent, so there is a nonzero polynomial p with complex coefficients such that p(T)v = 0.
- Over C every nonconstant polynomial factors into linear factors. So p(z) = (z − λ)q(z) for some λ ∈ C. Then 0 = p(T)v = (T − λI)q(T)v, which implies the nonzero vector w := q(T)v satisfies (T − λI)w = 0. Thus w is a nonzero eigenvector of T with eigenvalue λ. This gives at least one eigenvalue and a 1-dimensional T-invariant subspace span{w}.

2) Building an upper-triangular matrix by induction.
- Base case: If dim V = 1 the statement is trivial.
- Inductive step: Given T on an n-dimensional V with n > 1, use the argument above to find an eigenvector v1 and eigenvalue λ1. Extend v1 to a basis v1, v2, …, vn of V. Because Tv1 = λ1 v1, the matrix of T in this basis has the form
  [ λ1 * * … * ]
  [  0  ? ? … ? ]
  [  0  ? ? … ? ]
  [  …       …  ]
  where the first column has zeros below the top entry (i.e., T maps span{v1} into itself).
- The restriction of T to the (n−1)-dimensional subspace U = span{v2, …, vn} is a linear operator on U. By the induction hypothesis there is a basis of U relative to which this restricted operator has an upper-triangular matrix. Replacing v2, …, vn by that basis and keeping v1 first produces a basis of V in which the full matrix of T is upper triangular (the first row and column come from v1 and the rest is the triangular matrix for T|U).

Consequences and intuition
- Once T is represented by an upper-triangular matrix, the diagonal entries are precisely the eigenvalues (each diagonal entry λi satisfies (T − λi I) has a nontrivial kernel coming from the corresponding coordinate vector).
- This triangular form is the structural decomposition that replaces diagonalization when T need not be diagonalizable: it organizes V into a flag of invariant subspaces 0 = V0 ⊂ V1 ⊂ V2 ⊂ … ⊂ Vn = V with dim Vk = k, and each Vk is T-invariant. The diagonal entries record the eigenvalues that appear along that flag.

Inner product (definition and basic properties)

Let V be a vector space over the field F, where F = R or C. An inner product on V is a function
⟨·,·⟩ : V × V → F
that satisfies the following properties for all u,v,w ∈ V and all scalars α ∈ F:

1. Positivity
   - ⟨v,v⟩ is a real number and ⟨v,v⟩ ≥ 0.

2. Definiteness
   - ⟨v,v⟩ = 0 if and only if v = 0.

3. Linearity in the first slot
   - ⟨u+v, w⟩ = ⟨u,w⟩ + ⟨v,w⟩,
   - ⟨αu, v⟩ = α⟨u,v⟩.

4. Conjugate symmetry
   - ⟨v,w⟩ = overline{⟨w,v⟩} (complex conjugate).

Consequences / specializations:

- Over R (real vector spaces): conjugate symmetry becomes ordinary symmetry, ⟨v,w⟩ = ⟨w,v⟩, and linearity in the first slot together with symmetry implies bilinearity (linear in each slot separately).

- Over C (complex vector spaces): conjugate symmetry implies the inner product is conjugate-linear in the second slot:
   - ⟨v, αw⟩ = overline{α} ⟨v,w⟩,
   - ⟨v, w1 + w2⟩ = ⟨v,w1⟩ + ⟨v,w2⟩ (additivity).
  Thus the usual formulation: linear in the first slot, conjugate-linear in the second slot.

These properties ensure lengths and angles can be defined via ||v|| = sqrt(⟨v,v⟩) and that many geometric and algebraic results follow in inner product spaces.

Norm and Distance Induced by an Inner Product

Definition (norm from an inner product).
Let V be an inner-product space with inner product ⟨·,·⟩. Define the norm (length) of v ∈ V by
‖v‖ := sqrt(⟨v,v⟩).

This definition is well defined because ⟨v,v⟩ ≥ 0 and ⟨v,v⟩ = 0 ⇔ v = 0.

Properties that make ‖·‖ a norm
1. Positive definiteness:
   ‖v‖ ≥ 0 for all v, and ‖v‖ = 0 ⇔ v = 0. (Immediate from properties of the inner product.)

2. Homogeneity:
   For scalar α (real or complex),
   ‖α v‖ = |α| ‖v‖.
   Proof: ⟨α v, α v⟩ = α overline{α} ⟨v,v⟩ = |α|^2 ⟨v,v⟩, so take square roots.

3. Triangle inequality (subadditivity):
   For all u, v ∈ V,
   ‖u + v‖ ≤ ‖u‖ + ‖v‖.
   Proof sketch: expand ‖u+v‖^2 = ‖u‖^2 + 2 Re⟨u,v⟩ + ‖v‖^2 and apply the Cauchy–Schwarz inequality |⟨u,v⟩| ≤ ‖u‖‖v‖ to get
   ‖u+v‖^2 ≤ (‖u‖+‖v‖)^2, then take square roots.

Cauchy–Schwarz inequality (core tool)
For all u, v ∈ V,
|⟨u,v⟩| ≤ ‖u‖ ‖v‖,
with equality iff u and v are linearly dependent (one is a scalar multiple of the other). This inequality is the key ingredient in proving the triangle inequality and many other norm identities.

Metric (distance) induced by the norm
Define d: V × V → [0,∞) by
d(u,v) := ‖u − v‖.
This is a metric because:
- d(u,v) ≥ 0 and d(u,v) = 0 ⇔ u = v (from positive definiteness).
- Symmetry: d(u,v) = ‖u−v‖ = ‖v−u‖ = d(v,u).
- Triangle inequality: d(u,w) = ‖u−w‖ = ‖(u−v)+(v−w)‖ ≤ ‖u−v‖ + ‖v−w‖ = d(u,v) + d(v,w).

Useful identities and inequalities
- Pythagorean theorem (orthogonality):
  If ⟨u,v⟩ = 0, then
  ‖u+v‖^2 = ‖u‖^2 + ‖v‖^2.
- Parallelogram identity:
  For all u, v ∈ V,
  ‖u+v‖^2 + ‖u−v‖^2 = 2‖u‖^2 + 2‖v‖^2.
  (This identity characterizes norms coming from inner products: a norm satisfies the parallelogram law iff it arises from an inner product.)

- Polarization identities (recovering the inner product from the norm)
  Real case (field = R):
  ⟨u,v⟩ = (1/2)(‖u+v‖^2 − ‖u‖^2 − ‖v‖^2).
  Complex case (field = C):
  ⟨u,v⟩ = (1/4) [‖u+v‖^2 − ‖u−v‖^2 + i‖u+iv‖^2 − i‖u−iv‖^2].
  These show the inner product is uniquely determined by the norm.

Equality conditions
- Triangle equality: ‖u+v‖ = ‖u‖ + ‖v‖ iff u and v are positively linearly dependent (v = λ u with λ ≥ 0 in the real case; in the complex case the condition is v = α u with α a nonnegative real multiple of a unimodular scalar that aligns phases).
- Cauchy–Schwarz equality: |⟨u,v⟩| = ‖u‖‖v‖ iff u and v are linearly dependent.

Summary of why this behaves like length/distance
The norm defined by ‖v‖ = sqrt(⟨v,v⟩) is nonnegative, homogeneous, and satisfies the triangle inequality (via Cauchy–Schwarz), so it meets the axioms of a norm. The induced metric d(u,v) = ‖u−v‖ then satisfies the metric axioms. Orthogonality gives a Pythagorean relation, and the parallelogram and polarization identities tightly link the geometry of lengths to the algebra of the inner product.

Orthogonality and orthogonal complements

Definitions
- Two vectors v,w in an inner product space V are orthogonal (written v ⟂ w) if ⟨v,w⟩ = 0.
- A set S ⊆ V is an orthogonal set if every pair of distinct vectors in S is orthogonal: for all x,y ∈ S with x ≠ y, ⟨x,y⟩ = 0. If, in addition, every vector in S has norm 1, S is orthonormal.
- For any subset S ⊆ V, the orthogonal complement S⊥ is
  S⊥ = { v ∈ V : ⟨v, s⟩ = 0 for all s ∈ S }.
  When S is a subspace U, we often write U⊥.

Basic facts and useful structural properties
1. 0 is orthogonal to every vector, so 0 ∈ S⊥ for every S.
2. S⊥ is a subspace of V.
   - Proof sketch: if v,w ∈ S⊥ and α,β ∈ F, then for every s ∈ S,
     ⟨αv+βw, s⟩ = α⟨v,s⟩ + β⟨w,s⟩ = 0, so αv+βw ∈ S⊥.
3. Dependence only on span: S⊥ = (span S)⊥.
   - Reason: any vector orthogonal to S is orthogonal to all linear combinations of S, and conversely being orthogonal to span S implies orthogonality to S.
4. Monotonicity: if S ⊆ T ⊆ V then T⊥ ⊆ S⊥.
   - Reason: more constraints (orthogonality to a larger set) produce a smaller (or equal) orthogonal complement.
5. Intersection with orthogonal complement: if U is a subspace of V then U ∩ U⊥ = {0}.
   - Proof sketch: if v ∈ U ∩ U⊥ then ⟨v,v⟩ = 0, so v = 0.
6. Orthogonal complement of whole/zero subspaces:
   - V⊥ = {0}.
   - {0}⊥ = V.
7. Double orthogonal containement: for any S ⊆ V,
   span S ⊆ (S⊥)⊥.
   - Reason: every vector in S is orthogonal to every vector in S⊥, hence S⊥ annihilates span S, so span S lies in the double orthogonal.
8. Finite-dimensional equality: if V is finite-dimensional and U is a subspace, then (U⊥)⊥ = U.
   - This identifies orthogonal complement as a complement with dimension relation dim U + dim U⊥ = dim V.
9. Orthogonal projection context (used later): when U is a subspace and V is finite-dimensional, every v ∈ V can be uniquely written as v = u + w with u ∈ U and w ∈ U⊥; this decomposition is fundamental to least-squares and projection results.

These properties are the basic toolkit for manipulating orthogonality and orthogonal complements in inner product spaces and are used repeatedly in later results (projections, decompositions, and dimension formulas).

Orthonormal bases and Gram–Schmidt

What “orthonormal” means
- A list (v1, ..., vn) in an inner product space is orthonormal if each vi has norm 1 and distinct vectors are orthogonal: <vi, vj> = 0 for i ≠ j and ||vi|| = 1 for all i.
- An orthonormal basis is an orthonormal list that is also a basis (i.e., it spans the space and is linearly independent).

Why orthonormal bases simplify coordinates
- Coordinate extraction: If (e1, ..., en) is an orthonormal basis and v is any vector, the coordinate of v along ej is simply the inner product <v, ej>. Thus
  v = Σ_{j=1}^n <v, ej> ej.
  No system of linear equations or inversion is needed to find coordinates.
- Norms and Parseval’s identity: ||v||^2 = Σ_{j=1}^n |<v, ej>|^2. This makes computing lengths and checking convergence straightforward.
- Orthogonal decomposition and projections: The orthogonal projection of v onto the span of a subset of the basis is obtained by keeping the corresponding coefficients; projections are computed by inner products, e.g. proj_span{e1,...,ek}(v) = Σ_{j=1}^k <v, ej> ej.
- Linear independence is automatic: any orthonormal list with no zero vectors is linearly independent, so an orthonormal spanning list is a basis.

Gram–Schmidt procedure (algorithm)
Given a linearly independent list (x1, x2, ..., xm) in a finite-dimensional inner product space, Gram–Schmidt produces an orthonormal list (e1, e2, ..., em) with the same span.

Step-by-step:
1. Set w1 = x1. If w1 = 0, the starting list was not linearly independent; otherwise set e1 = w1 / ||w1||.
2. For k = 2, ..., m:
   - Compute wk = xk − Σ_{j=1}^{k-1} <xk, ej> ej. (This subtracts the components of xk in the directions e1,...,e_{k-1}.)
   - If wk = 0, then xk is in the span of the previous xj, so the original list was dependent; otherwise set ek = wk / ||wk||.
3. The resulting (e1, ..., em) is orthonormal and span{e1, ..., ek} = span{x1, ..., xk} for each k.

What Gram–Schmidt guarantees (finite-dimensional case)
- Existence of orthonormal bases: Starting from any basis of a finite-dimensional inner product space, Gram–Schmidt yields an orthonormal basis. Hence every finite-dimensional inner product space has an orthonormal basis.
- Preservation of spans: At each step the span of the first k orthonormal vectors equals the span of the first k original vectors.
- Stability of coordinates: Once an orthonormal basis is obtained, coordinates and projections are computed by inner products as above.
- Uniqueness up to phases/signs: The orthonormal basis produced depends on the order of the original list and on choices of signs/phases when normalizing; otherwise the orthonormal basis for a given ordered input is determined.

Remarks
- Gram–Schmidt is a constructive proof that orthonormal bases exist in finite dimensions and gives explicit formulas for projections and coefficients.
- In infinite-dimensional settings additional care is needed (completeness, convergence), but in the finite-dimensional case the procedure always terminates with an orthonormal basis.

Orthogonal projection onto a subspace; characterization by orthogonality

Definition
- Let V be an inner product space and U a subspace of V. A vector p in U is called an orthogonal projection of v in V onto U if v − p is orthogonal to every vector in U (i.e. v − p ∈ U⊥).
- When such a p exists it is unique; we denote it by proj_U v.

Characterization (orthogonality)
- p = proj_U v if and only if p ∈ U and v − p ⟂ U.
- Uniqueness: if p1, p2 ∈ U both satisfy v − p1 ⟂ U and v − p2 ⟂ U, then p1 − p2 ∈ U ∩ U⊥ = {0}, so p1 = p2.

Best-approximation (least-distance) property
- The orthogonal projection gives the closest vector in U to v. That is, for all u ∈ U,
  ||v − u|| ≥ ||v − proj_U v||,
  with equality iff u = proj_U v.
- Proof (Pythagorean decomposition): for any u ∈ U,
  v − u = (v − proj_U v) + (proj_U v − u),
  where (v − proj_U v) ⟂ (proj_U v − u) because v − proj_U v ⟂ U and proj_U v − u ∈ U.
  Hence ||v − u||^2 = ||v − proj_U v||^2 + ||proj_U v − u||^2 ≥ ||v − proj_U v||^2, proving minimality.

Computing projections with an orthonormal basis
- If {u1, …, um} is an orthonormal basis of the finite-dimensional subspace U, then for any v ∈ V,
  proj_U v = sum_{j=1}^m ⟨v, uj⟩ uj.
  This follows because v − sum ⟨v, uj⟩ uj is orthogonal to each uj, hence to U.
- If the basis {b1, …, bm} of U is not orthonormal, one may:
  - Apply Gram–Schmidt to get an orthonormal basis and use the formula above; or
  - Solve the normal equations: write A = [b1 … bm] (columns), then coefficients c solving A* A c = A* v give proj_U v = A c. In matrix form,
    proj_U v = A (A* A)^{-1} A* v
    (when A* A is invertible, i.e. the bi are linearly independent).

These are the defining properties and principal computational formulas for orthogonal projections and their best-approximation property.

Riesz representation theorem (finite-dimensional)

Theorem. Let V be a finite-dimensional inner-product space over F (R or C) with inner product ⟨·,·⟩. For every linear functional φ ∈ V* there exists a unique vector u ∈ V such that
φ(v) = ⟨v, u⟩ for all v ∈ V.
Hence the map R: V → V* given by R(u) = (v ↦ ⟨v, u⟩) is a bijection (in fact an isomorphism of vector spaces, with the usual caveat about conjugate-linearity over C depending on the inner-product convention).

Proof (finite-dimensional, standard argument).
- Existence: Choose an orthonormal basis {e1,...,en} for V. Write an arbitrary v = ∑ vj ej. Define uj = φ(ej) (scalars). Let u = ∑ uj ej. Then for any v,
⟨v, u⟩ = ⟨∑ vj ej, ∑ uj ej⟩ = ∑ vj uj = ∑ vj φ(ej) = φ(∑ vj ej) = φ(v),
using orthonormality and linearity of φ. Thus such a u exists.
- Uniqueness: If u and u' satisfy φ(v) = ⟨v,u⟩ = ⟨v,u'⟩ for all v, then ⟨v, u - u'⟩ = 0 for all v. Taking v = u - u' gives ||u - u'||^2 = 0, so u = u'.
Therefore each φ corresponds to exactly one u and R is bijective.

Remarks and consequences
- Dependence on the inner product: The vector u representing a given φ depends on the chosen inner product. If the inner product is changed, the same functional φ will, in general, be represented by a different vector. Thus R is not an intrinsic identification of V with V* independent of any extra structure — it is an identification that uses the particular inner product.
- Linearity vs conjugate-linearity: Over R the map R: V → V* defined by u ↦ (v ↦ ⟨v,u⟩) is linear. Over C its linearity properties depend on the convention for the inner product (whether it is linear in the first or second slot). With the common convention that ⟨·,·⟩ is linear in the first argument and conjugate-linear in the second, R is conjugate-linear; with the opposite convention R is linear. Be careful when using this map in proofs: check the convention in use.
- Relation to dual spaces: The theorem gives a concrete isomorphism between V and its algebraic dual V* once an inner product is fixed. Dimensionally this matches the general fact dim V = dim V*, but Riesz supplies a canonical (inner-product-dependent) way to turn a functional into a vector. In other words, while V* is independent of any inner product as a vector space, the natural identification V ≅ V* requires choosing an inner product.
- Use in computations: To find the vector u representing a functional φ, compute φ on an orthonormal basis and form u = ∑ φ(ej) ej. In coordinates relative to an orthonormal basis, φ corresponds to the coordinate vector of u (conjugated if your inner-product convention introduces conjugation).
- Adjoint viewpoint: The Riesz map allows one to identify the adjoint T* of a linear operator T: V → V with the transpose/conjugate-transpose operation on matrices once an orthonormal basis is fixed, because ⟨Tv,w⟩ = ⟨v,T*w⟩ can be rewritten using the identification of functionals with inner products.

Takeaway: In finite dimensions, every linear functional is inner product against a unique vector; this identifies V with V* but only after fixing an inner product — the identification depends on that choice.

Definition and existence
- Let V be a finite-dimensional inner-product space over F (R or C). For a linear operator T: V → V, the adjoint T* is the unique linear operator on V satisfying
  <T v, w> = <v, T* w>  for all v,w in V.
- Existence and uniqueness (sketch): For fixed w, the map v ↦ <T v, w> is a linear functional on V, so by the Riesz representation theorem there is a unique vector T* w such that <T v, w> = <v, T* w> for all v. Doing this for every w defines a linear operator T*; uniqueness follows because if two operators satisfy the identity their values on each w must agree.

Basic properties and short proofs
1) Conjugate-linearity of the adjoint map
- For scalars a,b in F and operators S,T, (aS + bT)* = conjugate(a) S* + conjugate(b) T*.
Proof: For all v,w,
  <v, (aS + bT)* w> = <(aS + bT) v, w> = a<T v, w> + b<S v, w>
                   = a<v, T* w> + b<v, S* w>
                   = <v, conjugate(a) T* w + conjugate(b) S* w>.
Since this holds for all v, we get (aS + bT)* = conjugate(a) T* + conjugate(b) S*. In particular, (aT)* = conjugate(a) T*.

2) Reversal of products: (S T)* = T* S*
Proof: For all v,w,
  <v, (S T)* w> = <S T v, w> = <T v, S* w> = <v, T* S* w>.
Hence (S T)* = T* S*.

3) Involution: (T*)* = T
Proof: For all v,w,
  <T v, w> = <v, T* w> = conjugate(<T* w, v>) = <v, (T*)* w>.
Thus T = (T*)*.

4) Interaction with invertibility
- If T is invertible, then (T^{-1})* = (T*)^{-1}. Proof follows from (T T^{-1})* = (T^{-1})* T* = I and uniqueness of inverses.

Matrix relation in an orthonormal basis
- Let {e1,...,en} be an orthonormal basis of V. Let A be the matrix of T with respect to this basis (so T(ej) = sum_i A_{ij} e_i). Then the matrix of T* in this same orthonormal basis is A* = the conjugate-transpose of A (often denoted Ā^T or A^*): (A*)_{ij} = conjugate(A_{ji}).
Proof: Compute <T e_j, e_i> in two ways. By definition of A, <T e_j, e_i> = <sum_k A_{kj} e_k, e_i> = A_{ij} (orthonormality). On the other hand, using the adjoint identity, <T e_j, e_i> = <e_j, T* e_i> = conjugate(<T* e_i, e_j>) = conjugate((matrix of T*)_{j i}). Equating gives (matrix of T*)_{ji} = conjugate(A_{ij}), so matrix(T*) = conjugate-transpose(A).

Remarks
- Over R the conjugation is trivial, so adjoint corresponds to the transpose in an orthonormal basis.
- The adjoint map T ↦ T* is bijective and conjugate-linear; it reverses products and is an involution.

Normal operators

Definition
- Let V be a finite-dimensional inner-product space (over C; proofs below adapt with minor changes for R when appropriate). An operator T ∈ L(V) is normal if
  T T* = T* T.
Equivalently, T commutes with its adjoint.

Basic consequences
1) Norm equality. For every v ∈ V,
   ||T v|| = ||T* v||.
Proof. ||T v||^2 = <T v, T v> = <T* T v, v> and ||T* v||^2 = <T T* v, v>. If T T* = T* T then the two inner products are equal, hence the norms are equal.

2) Kernel relationships. ker T = ker T* and, more generally, ker T^k = ker (T*)^k for k ≥ 1.
Proof. If T v = 0 then 0 = ||T v|| = ||T* v|| so T* v = 0, hence ker T ⊆ ker T*. The same argument with T and T* interchanged gives the reverse inclusion. The statement for powers follows by applying the same argument to T^k, which is normal whenever T is normal (T^k (T^k)* = T^k (T*)^k = (T*)^k T^k = (T^k)* T^k).

3) Invariance of orthogonal complements. If U ≤ V is T-invariant (i.e. T(U) ⊆ U) and T is normal, then U⊥ is T*-invariant; if U is T-invariant and also T*-invariant then U⊥ is T-invariant.
Proof. If u ∈ U and w ∈ U⊥ then <T* w, u> = <w, T u> = 0, so T* w ∈ U⊥. If U is both T- and T*-invariant then the same argument with T in place of T* shows T(U⊥) ⊆ U⊥.

Orthogonality of eigenvectors
- If T is normal and v and w are eigenvectors of T with eigenvalues λ and μ respectively, and λ ≠ μ, then v ⟂ w.
Proof. Suppose T v = λ v and T w = μ w. Compute
  λ <v, w> = <λ v, w> = <T v, w> = <v, T* w> = <v, \overline{μ} w> = \overline{μ} <v, w>.
Thus (λ − \overline{μ}) <v, w> = 0. Over C, for eigenvalues of T we have μ = \overline{(eigenvalue\ of\ T*)}, and since μ ≠ λ it follows that <v, w> = 0. In particular, eigenvectors belonging to distinct eigenvalues are orthogonal.

Triangularization and diagonalization (spectral theorem for normal operators)
- Every operator T on a complex finite-dimensional inner-product space has an upper-triangular matrix with respect to some orthonormal basis (Schur). If T is normal, that upper-triangular matrix must in fact be diagonal. Consequently, a normal operator is unitarily diagonalizable: there exists an orthonormal basis of V consisting of eigenvectors of T, and T is represented by a diagonal matrix diag(λ1, …, λn) with respect to that basis.
Proof sketch. Triangularize T: choose an orthonormal basis in which T is upper-triangular. Let the diagonal entries be λ1, …, λn. Normality forces the matrix to commute with its conjugate-transpose. Comparing entries shows that all off-diagonal entries must vanish (an easy induction on size: the first column argument shows the first column below the diagonal is zero, etc.), so the upper-triangular matrix is diagonal. That gives an orthonormal eigenbasis, hence unitary diagonalization.

Structural decomposition into invariant orthogonal subspaces
- If T is normal and its distinct eigenvalues are λ1, …, λm, then V decomposes as an orthogonal direct sum of the eigenspaces:
  V = E(λ1) ⊕⊥ E(λ2) ⊕⊥ ··· ⊕⊥ E(λm),
where E(λ) = {v : T v = λ v}. Each E(λj) is invariant under T (indeed, each is an eigenspace) and mutually orthogonal to the others.
- More generally, for any polynomial p, the subspaces ker p(T) and range p(T) are invariant under T and are orthogonal complements when p(T) is normal and has suitable factorization; in particular projections that are polynomials in a normal operator are orthogonal projections.

Adjoint action on eigenspaces
- If T is normal and v is an eigenvector with eigenvalue λ, then T* v = \overline{λ} v. Thus each eigenspace E(λ) is invariant under T* and on that eigenspace T* acts as scalar multiplication by \overline{λ}.

Functional consequences and spectral behavior
- Spectrum and norm. For normal T, the spectral radius equals the operator norm: r(T) = ||T||. In particular, ||T|| = max{|λ| : λ ∈ spectrum(T)}.
Proof sketch. Diagonalization shows ||T|| is the maximum modulus of the diagonal eigenvalues, which is the spectral radius.

- Polynomials and continuous functional calculus. If T is normal and p is a polynomial, then p(T) is normal and its eigenvalues are p(λ) where λ runs over the eigenvalues of T. In the diagonalizing orthonormal basis p(T) is diagonal with entries p(λj).

Summary of structural picture
- A normal operator behaves like a diagonal matrix with respect to an orthonormal basis: its action splits V into mutually orthogonal invariant eigenspaces, its adjoint acts by conjugating eigenvalues, and spectral properties (norm, spectral radius, behavior of polynomials) are read off from the eigenvalues. These structural results are the basis for the further analysis of normal operators and operators that can be reduced to normal form.

Self-adjoint operators (T = T*)

Definition / characterization
- Let V be an inner-product space over F (R or C). The adjoint T* of a linear operator T on V is the unique operator satisfying
  <T v, w> = <v, T* w> for all v,w in V.
- T is self-adjoint if T = T*, i.e. <T v, w> = <v, T w> for all v,w.

Basic consequences and proofs

1) Quadratic form ⟨T v, v⟩ is real
- If T is self-adjoint then for every v in V,
  <T v, v> = <v, T v>.
  But <v, T v> = overline{<T v, v>} (conjugate symmetry of the inner product), so
  <T v, v> = overline{<T v, v>},
  hence <T v, v> is real.

2) Real eigenvalues
- Let v ≠ 0 satisfy T v = λ v. Then
  <T v, v> = λ <v, v>.
  By (1) the left side is real, and <v,v> > 0, so λ must be real.

3) Eigenspaces for distinct eigenvalues are orthogonal
- Let v and w be eigenvectors with eigenvalues λ and μ respectively, with λ ≠ μ. Then
  λ <v, w> = <T v, w> = <v, T w> = <v, μ w> = μ <v, w>.
  Hence (λ − μ) <v, w> = 0, so <v, w> = 0. Thus eigenvectors for distinct eigenvalues are orthogonal; equivalently, eigenspaces corresponding to distinct eigenvalues are orthogonal.

4) Converse: reality of quadratic form implies T is self-adjoint
- Suppose <T v, v> is real for every v in V. We show T = T*. Use polarization. For an inner product linear in the first slot, the polarization identity expresses the inner product in terms of the quadratic form:
  for all x,y,
  <x,y> = 1/4( Q(x+y) − Q(x−y) + i Q(x+i y) − i Q(x−i y) ),
  where Q(z) := <z,z>.
- Apply this to the bilinear form B(u,v) := <T u, v>. Since Q_T(z) := <T z, z> is real by hypothesis, the polarization identity applied to Q_T yields that B(u,v) = <T u, v> satisfies
  <T u, v> = <u, T v> for all u,v.
  Thus T = T*.
- (In words: reality of the quadratic form for all v is equivalent to symmetry of the sesquilinear form (u,v) ↦ <T u, v>, hence T is self-adjoint.)

Remarks
- In finite-dimensional complex inner-product spaces, the facts above are the key steps toward the spectral theorem: a self-adjoint operator has a basis of eigenvectors and is diagonalizable with real eigenvalues (orthonormal eigenbasis can be chosen because eigenspaces for distinct eigenvalues are orthogonal and each eigenspace admits an orthonormal basis).

Spectral theorem for normal operators

Theorem (Spectral theorem, complex case).
Let V be a finite-dimensional inner product space over C, and let T ∈ L(V) be normal (TT* = T*T). Then V has an orthonormal basis consisting of eigenvectors of T. Equivalently, there exists an orthonormal basis of V in which the matrix of T is diagonal; equivalently T is unitarily diagonalizable.

Proof.
By Schur's theorem (or the Schur decomposition) there is an orthonormal basis of V in which the matrix of T is upper triangular. Concretely, choose an orthonormal basis {e1,...,en} so that the matrix of T is upper triangular. Write that upper-triangular matrix as T = (tij) with diagonal entries λ1,...,λn (the eigenvalues of T, listed with multiplicity).

Because T is normal, T*T = TT*. Note that T* is lower triangular with diagonal entries the conjugates λ̄1,...,λ̄n. Compute the (1,1)-entry of T*T and of TT*:

- (T*T)11 = ∑k |t1k|^2 = |t11|^2 + ∑_{k>1} |t1k|^2 = |λ1|^2 + ∑_{k>1} |t1k|^2.
- (TT*)11 = |t11|^2 = |λ1|^2.

Equating, we get ∑_{k>1} |t1k|^2 = 0, hence t1k = 0 for all k > 1. Thus the first row (and so first column above the diagonal) has no nonzero superdiagonal entries. Remove the span of e1 and restrict to the orthogonal complement; the restriction of T to that complement is still normal and upper triangular in the induced orthonormal basis. By induction on dimension all superdiagonal entries vanish, so T is diagonal in the chosen orthonormal basis. Therefore V has an orthonormal basis of eigenvectors of T, and T is unitarily diagonalizable. □

Real case (appropriate decomposition).
Let V be a finite-dimensional real inner product space and T ∈ L(V) normal (TT* = T*T). Over R we cannot always diagonalize by an orthonormal basis because T may have nonreal eigenvalues. However, V has an orthonormal basis relative to which the matrix of T is block-diagonal with blocks of two types:

- 1×1 blocks [α] where α ∈ R is a real eigenvalue,
- 2×2 blocks of the form [ [a, -b], [b, a] ] corresponding to a pair of complex-conjugate eigenvalues a ± bi (b ≠ 0).

Equivalently, by extending scalars to C we get the complex spectral theorem and then return to R: for every complex eigenpair (a + bi, u + iv) (u,v ∈ V viewed over R), the real span of {u,v} is T-invariant and on that 2-dimensional subspace T acts by the indicated 2×2 rotation–scaling matrix. The blocks are orthogonal with respect to the inner product, so the decomposition is orthogonal (i.e., given by an orthonormal basis made of real eigenvectors and orthonormal real bases of these 2-planes).

Remarks: In particular T is orthogonally diagonalizable (over R) if and only if T has a full set of real eigenvalues (equivalently its minimal polynomial splits over R into linear factors), and this happens in particular when T is self-adjoint (see below).

Applications

1) Self-adjoint operators.
If T is self-adjoint (T = T*), then T is normal, so by the spectral theorem (complex case) V has an orthonormal basis of eigenvectors of T. Moreover every eigenvalue of a self-adjoint operator is real: if T v = λv with v ≠ 0, then λ⟨v,v⟩ = ⟨λv,v⟩ = ⟨Tv,v⟩ = ⟨v,Tv⟩̄ = ⟨v,λv⟩̄ = λ̄⟨v,v⟩, hence λ = λ̄. Thus a self-adjoint operator is unitarily diagonalizable with real diagonal entries; over R this means it is orthogonally diagonalizable.

2) Unitary operators.
If U is unitary (U* = U^{-1}), then U is normal, so U is unitarily diagonalizable. Every eigenvalue λ of a unitary operator satisfies |λ| = 1: if Uv = λv and v ≠ 0, then ⟨v,v⟩ = ⟨Uv,Uv⟩ = ⟨λv,λv⟩ = |λ|^2⟨v,v⟩, so |λ| = 1. Thus a unitary operator is unitarily diagonalizable with diagonal entries on the unit circle. Over R a real orthogonal operator (the real analogue of unitary) decomposes into orthogonal 1×1 blocks with entries ±1 and 2×2 rotation blocks [ [cosθ, -sinθ], [sinθ, cosθ] ].

Summary of consequences
- Normal ⇔ unitarily diagonalizable over C.
- Self-adjoint ⇒ diagonalizable by a unitary/orthogonal change of basis with real eigenvalues.
- Unitary ⇒ diagonalizable by a unitary change of basis with eigenvalues of modulus 1.
- Over R, a normal operator decomposes orthogonally into real 1×1 eigenblocks and 2×2 rotation-dilation blocks; symmetric (self-adjoint) operators are exactly those normal operators that are orthogonally diagonalizable.

Positive operators and square roots

Definition
- Let V be a finite-dimensional inner-product space (over R or C). A linear operator T ∈ L(V) is positive (written T ≥ 0) if ⟨Tv,v⟩ ≥ 0 for every v ∈ V.

Basic consequences and properties
1. Positivity implies self-adjointness.
   - Claim: If ⟨Tv,v⟩ ∈ R for all v, then T is self-adjoint. In particular, if T ≥ 0 then T is self-adjoint.
   - Proof: For u,w ∈ V, expand using polarization. Over C, the polarization identities give
     Re⟨Tu,w⟩ = 1/4(⟨T(u+w),u+w⟩ − ⟨T(u−w),u−w⟩),
     Im⟨Tu,w⟩ = 1/4(⟨T(u+iw),u+iw⟩ − ⟨T(u−iw),u−iw⟩).
     If T ≥ 0 then all the inner products on the right are real, so Re⟨Tu,w⟩ = Re⟨u,Tw⟩ and Im⟨Tu,w⟩ = Im⟨u,Tw⟩, hence ⟨Tu,w⟩ = ⟨u,Tw⟩ for all u,w. Thus T = T*, i.e. T is self-adjoint. (Over R the same polarization with fewer terms suffices.)

2. Positivity and eigenvalues.
   - If T ≥ 0 and v is an eigenvector with eigenvalue λ, i.e. Tv = λv and v ≠ 0, then
     λ = ⟨Tv,v⟩/⟨v,v⟩ ≥ 0.
     Thus every eigenvalue of a positive operator is real and ≥ 0.
   - Conversely, if T is self-adjoint and all eigenvalues of T are ≥ 0, then T ≥ 0 (because in an orthonormal eigenbasis v = ∑ αk ek we have ⟨Tv,v⟩ = ∑ λk |αk|^2 ≥ 0).

3. Basic algebraic facts.
   - If T ≥ 0 and c ≥ 0 (real scalar), then cT ≥ 0.
   - If T1 ≥ 0 and T2 ≥ 0 and they commute and are simultaneously diagonalizable (in particular if they are functions of the same self-adjoint operator), then T1 + T2 ≥ 0. More generally, the sum of positive operators is positive: if T1,T2 ≥ 0 then ⟨(T1+T2)v,v⟩ = ⟨T1v,v⟩+⟨T2v,v⟩ ≥ 0.
   - If T ≥ 0 and S is any operator, then S*TS ≥ 0 because ⟨S*TS v,v⟩ = ⟨TS v,TS v⟩ = ‖TSv‖^2 ≥ 0.

Positive square roots: existence and uniqueness
- Theorem (existence and uniqueness of positive square roots). Let T ∈ L(V). There exists a unique operator S ∈ L(V) such that
  (i) S ≥ 0 (S is positive),
  (ii) S^2 = T,
  if and only if T is positive. In that case S is called the positive square root of T and we write S = T^{1/2}.

Proof (construction via the spectral theorem).
1. Reduce to the self-adjoint nonnegative case. If T ≥ 0 then, from above, T is self-adjoint and has a spectral decomposition by the spectral theorem: there exists an orthonormal basis {e1,...,en} of V consisting of eigenvectors of T with real eigenvalues λ1,...,λn. By positivity each λk ≥ 0.

2. Define S on the eigenbasis. Set μk = √λk (choose the nonnegative square root). Define S by S ek = μk ek for each k and extend linearly. Then:
   - S is self-adjoint because it is diagonal in an orthonormal basis with real diagonal entries μk.
   - S is positive since each μk ≥ 0, so for any v = ∑ αk ek,
     ⟨Sv,v⟩ = ∑ μk |αk|^2 ≥ 0.
   - S^2 ek = μk^2 ek = λk ek, so S^2 = T on the basis and hence on all of V.

Thus existence of a positive S with S^2 = T is established.

3. Uniqueness. Suppose R is another operator with R ≥ 0 and R^2 = T. Diagonalize T as above; each ek is an eigenvector of T with eigenvalue λk ≥ 0. Then for each k,
   R^2 ek = T ek = λk ek.
   Because R is self-adjoint, ek can be written in terms of R’s spectral decomposition, but one can argue directly on the one-dimensional invariant subspace span{ek}: R restricts to a self-adjoint operator on that line, so R ek = νk ek for some real νk. Then νk^2 = λk, and since R ≥ 0 we have νk ≥ 0; hence νk = √λk = μk. So R and S agree on every ek, therefore R = S. Thus the positive square root is unique.

Remarks
- The construction is simply taking square roots of eigenvalues in an orthonormal eigenbasis; positivity forces the nonnegative root choice and gives uniqueness.
- This is the finite-dimensional instance of functional calculus for self-adjoint operators: for any real-valued function f defined on the spectrum of a self-adjoint operator T, one can define f(T) by applying f to the eigenvalues in an orthonormal eigenbasis. The positive square root is the special case f(x) = √x on [0,∞).

Unitary operators (and the real orthogonal case)

Definition
- Let V be an inner-product space over F (F = C or R). A linear operator T : V → V is unitary if T*T = TT* = I (equivalently T* = T^{-1}). In the real case we call such operators orthogonal; for matrices this corresponds to A^T A = I.

Basic equivalent characterizations
For T ∈ L(V), the following are equivalent.
1. T is unitary (T*T = I).
2. T is surjective and preserves inner products: for all u,v ∈ V, ⟨Tu, Tv⟩ = ⟨u, v⟩.
3. T preserves norms: for all v ∈ V, ||Tv|| = ||v||.
4. T maps some (hence every) orthonormal basis to an orthonormal basis.
5. T is invertible and T^{-1} = T*.

Proof sketches / remarks
- (1) ⇒ (2): If T*T = I then for all u,v,
  ⟨Tu, Tv⟩ = ⟨u, T*Tv⟩ = ⟨u, v⟩,
  so T preserves inner products. Preservation of inner products implies preservation of norms since ||v||^2 = ⟨v,v⟩.
- (2) ⇒ (3): Immediate by taking v = u.
- (3) ⇒ (4): If {e_i} is an orthonormal basis, then for i≠j,
  ⟨Te_i, Te_j⟩ = 0 (by polarization from norms), and ||Te_i|| = 1, so {Te_i} is orthonormal. Surjectivity follows because an isometry from a finite-dimensional space is injective and hence bijective.
- (4) ⇒ (1): If T sends an orthonormal basis {e_i} to an orthonormal basis {f_i}, then relative to that basis the matrix of T has columns f_i expressed in the e-basis; orthonormality of columns gives T*T = I, hence T is unitary.
- (1) ⇔ (5): If T*T = I then multiplying on the left by T^{-1} (which exists because T is injective on finite-dimensional V) gives T* = T^{-1}. Conversely, if T* = T^{-1} then T*T = I.

Matrix formulation
- If V is finite-dimensional and B = {e_1,...,e_n} is an orthonormal basis, the matrix [T]_B of a unitary operator T satisfies [T]_B^* [T]_B = I (where * denotes conjugate-transpose). Conversely, any matrix U with U^* U = I defines a unitary operator on C^n (or R^n when entries are real, giving an orthogonal matrix).
- Thus unitary operators are exactly those whose matrices relative to orthonormal bases are unitary (orthogonal in the real case).

Consequences
- Unitary operators are isometries and thus preserve lengths, angles, orthogonality, and orthonormality.
- Spectral consequences (brief): eigenvalues of a unitary operator lie on the unit circle in C (in the real/orthogonal case, eigenvalues are ±1 or come in complex-conjugate pairs lying on the unit circle).
- Adjoints and inverses: for a unitary T we have T^{-1} = T*, so taking adjoints swaps inverse and original: (T^{-1})* = (T*)^{-1} = T.

Examples
- Multiplication by a complex scalar of unit modulus on C^n is unitary.
- Permutation matrices and real rotation matrices are orthogonal.

Complex Spectral Theorem & Functional Calculus for Normal Operators

Statement (Complex spectral theorem).
Let V be a finite-dimensional complex inner product space and T ∈ L(V). T is normal (T T* = T* T) if and only if there exists an orthonormal basis of V consisting of eigenvectors of T. Equivalently, with respect to some orthonormal basis T has a diagonal matrix diag(λ1,...,λn). The eigenvalues λi lie in C and the eigenspaces corresponding to distinct eigenvalues are orthogonal.

Spectral decomposition (projection form).
If the distinct eigenvalues of T are μ1,...,μm and Ei = ker(T − μi I) (the eigenspaces), then V = ⊕_{i=1}^m Ei (orthogonal direct sum), and T can be written
T = ∑_{i=1}^m μi Pi,
where Pi is the orthogonal projection onto Ei. The projections Pi satisfy Pi Pj = 0 for i ≠ j, Pi^2 = Pi, Pi* = Pi, and ∑_{i=1}^m Pi = I. This decomposition is unique.

Sketch of how to diagonalize T.
- Find eigenvalues μi of T (roots of the characteristic polynomial).
- For each μi, find an orthonormal basis of Ei (apply Gram–Schmidt inside each eigenspace).
- Put the orthonormal bases of all Ei together; by orthogonality of distinct eigenspaces this is an orthonormal basis of V consisting of eigenvectors, and the matrix of T in that basis is diagonal with entries the corresponding eigenvalues.

Functional calculus for normal operators.
Given a function f defined on the spectrum σ(T) = {μ1,...,μm}, define f(T) by applying f to the eigenvalues in the spectral decomposition:
f(T) := ∑_{i=1}^m f(μi) Pi.
This definition is natural and well defined because the eigenvalue decomposition is unique up to ordering of the terms. Properties:
- If f and g are scalar functions on σ(T) and α, β ∈ C, then (α f + β g)(T) = α f(T) + β g(T).
- Multiplicativity for pointwise product: (fg)(T) = f(T) g(T).
- If f(z) = z^k then f(T) = T^k.
- If f(z) = e^z then e^{T} = ∑ e^{μi} Pi.
- If T is normal then f(T)* = \overline{f}(T) (apply conjugate to values on spectrum).
- If f takes real nonnegative values on σ(T) and T is self-adjoint, then f(T) is positive semidefinite.

How to compute f(T) in practice.
1. Diagonalize T: find an orthonormal eigenbasis v1,...,vn with T vj = λj vj.
2. For any vector x = ∑ c_j vj, f(T)x = ∑ c_j f(λj) vj.
3. Matrix form: if U is the unitary change-of-basis matrix with columns vj, and D = diag(λ1,...,λn), then T = U D U*, and f(T) = U f(D) U* where f(D) = diag(f(λ1),...,f(λn)).

Examples and common applications.
- Powers: T^k = ∑ λ_i^k Pi.
- Exponential: e^T = ∑ e^{λ_i} Pi (used for solving linear ODEs; here finite-dimensional).
- Square root of a positive operator: If T is self-adjoint and all λi ≥ 0, then √T = ∑ √λ_i Pi is the unique positive square root.
- Absolute value: |T| := √(T* T) — for normal T, T* T = T T*, diagonalizes with eigenvalues |λ_i|^2, so |T| = ∑ |λ_i| Pi.
- Polynomial functional calculus: For a polynomial p, p(T) computed by substituting T is equal to ∑ p(λ_i) Pi.
- Spectral mapping theorem (finite-dimensional): σ(f(T)) = f(σ(T)) = {f(λ_i)}.

Remarks.
- Normality is essential: nonnormal matrices need not be diagonalizable by a unitary matrix; the spectral theorem in this form fails.
- The projection decomposition T = ∑ μi Pi encodes both the algebraic structure (eigenvalues) and the geometric structure (orthogonal eigenspaces), and it is the basis for defining any reasonable notion of f(T) that depends only on T and on values of f on σ(T).
- This functional calculus extends (with more work) to continuous functions and to Borel measurable functions in infinite-dimensional settings, but for finite-dimensional complex spaces the finite-sum definition above suffices.

Complexification — passing from a real inner product space to a related complex vector space — is a standard way to study real operators using the richer eigen-structure available over C. The construction and the main facts you need are:

Construction of the complexification
- If V is a real inner product space, define its complexification V_C = {u + i v : u,v ∈ V} with complex-scalar multiplication and addition defined in the obvious way:
  (a+ib)(u+iv) = (au − bv) + i(bu + av).
- Extend the real inner product ⟨·,·⟩ on V uniquely to a complex inner product on V_C by requiring sesquilinearity and that it agree on V. Equivalently, for u1,u2,v1,v2 ∈ V,
  ⟨u1 + i v1, u2 + i v2⟩ = ⟨u1,u2⟩ + ⟨v1,v2⟩ + i(⟨v1,u2⟩ − ⟨u1,v2⟩).
  This makes V_C a complex inner product space and reduces to the original inner product on the real subspace V ⊂ V_C.

Extending operators
- If T : V → V is a real-linear operator, it extends uniquely to a complex-linear operator T_C : V_C → V_C by
  T_C(u + i v) = T u + i T v.
  T_C is C-linear and agrees with T on V. We call T_C the complexification (or scalar extension) of T.

How operator properties behave under complexification
- Preservation of algebraic relations: any polynomial relation p(T)=0 over R remains true for T_C, i.e. p(T_C)=0. In particular, the minimal polynomial of T over C is the factorization of the real minimal polynomial over C.
- Spectral extension: the spectrum of T_C is the set of complex numbers that are eigenvalues of T_C; it equals the roots of the complexified characteristic polynomial. Real eigenvalues of T are eigenvalues of T_C. In general, T might have no real eigenvalues but T_C always has complex eigenvalues (since the characteristic polynomial splits over C).
- Conjugation symmetry: if λ ∈ C is an eigenvalue of T_C with eigenvector w, then the complex-conjugate λ̄ is also an eigenvalue with eigenvector w̄ (complex conjugation of coordinates relative to V). Thus nonreal eigenvalues occur in conjugate pairs. Consequently, nonreal eigenvalues correspond to real T-invariant 2-dimensional subspaces in V (coming from the real and imaginary parts of a complex eigenvector).
- Diagonalizability and Jordan form: T is diagonalizable over C iff T_C is diagonalizable; Jordan structure over C is exactly the Jordan structure of T_C (the real Jordan form can be obtained from this by collecting conjugate blocks).
- Normality and self-adjointness:
  - T is self-adjoint (symmetric) on the real inner product space V iff T_C is self-adjoint on V_C. Proof sketch: the defining inner-product identity ⟨T x,y⟩ = ⟨x,T y⟩ for all real x,y extends by sesquilinearity to all of V_C, so it holds for T_C and conversely.
  - More generally, T is normal on V (i.e. T T* = T* T, where T* is the adjoint on V) iff T_C is normal on V_C. Adjoint commutes with complexification.
  - Orthogonal maps on V complexify to unitary maps on V_C (an orthogonal real operator R satisfies R* = R^-1 on V, and the same relation holds for R_C making it unitary on V_C).
- Spectral consequences:
  - If T is self-adjoint on V, then T_C is self-adjoint on V_C, so all eigenvalues of T_C are real. Hence a real self-adjoint operator already has only real eigenvalues; if V is finite-dimensional and T is self-adjoint, you can find an orthonormal basis of V consisting of real eigenvectors (no need to pass to C). Complexification simply preserves this structure.
  - If T is normal but not self-adjoint, complexification lets you diagonalize T_C by an orthonormal basis of V_C (spectral theorem over C), and the real operator T is represented on V by the real and imaginary parts of those complex eigenvectors; nonreal eigenvalues occur in conjugate pairs and give rise to orthogonal real invariant 2-planes on which T acts like a rotation+scaling.
- Eigenspaces and real structure: if E_λ ⊂ V_C is the eigenspace of T_C for eigenvalue λ, then E_λ̄ = conj(E_λ). The real subspace generated by an eigenvector and its conjugate (if λ ∉ R) is T-invariant and has even real dimension equal to 2 · dim_C E_λ.

Why this is useful
- Many algebraic and spectral questions about a real operator become simpler after complexifying because polynomials split over C and the spectral theorem for normal operators is clean over C. Then one translates the resulting structure back to real invariant subspaces (real eigenvectors or 2D rotation/scaling blocks) using the conjugation symmetry described above.

Key takeaways (short)
- Form V_C = V ⊕ iV, extend inner product and extend T to T_C by C-linearity.
- Self-adjointness, normality, orthogonality/unitarity are preserved under complexification.
- The spectrum of T_C is the complex roots of T’s characteristic polynomial; nonreal eigenvalues come in conjugate pairs and correspond to real 2D invariant subspaces.
- Diagonalization/Jordan form is easiest to analyze over C via T_C, then translated back to real structure using conjugation.

Conjugations and real forms

Definition
- Let V be a complex inner product space. A conjugation on V is a map C: V → V satisfying
  1. C is conjugate-linear: C(αv + βw) = \overline{α} C(v) + \overline{β} C(w) for all α,β ∈ C and v,w ∈ V;
  2. C is an involution: C(C(v)) = v for all v ∈ V;
  3. C is isometric (equivalently, preserves inner products up to conjugation): ⟨C(v), C(w)⟩ = \overline{⟨v,w⟩} for all v,w ∈ V.
- In practice one often drops the explicit isometry requirement when it is clear from context (many authors call any conjugate-linear involution a conjugation), but for inner product considerations the isometry condition is natural and will be used below.

Real form determined by a conjugation
- Given a conjugation C on V, the fixed-point set
  V_R := {v ∈ V : C(v) = v}
  is a real vector subspace of V. We call V_R the real form of V determined by C.
- V_R is a real inner product space with the inner product inherited from V (which is real-valued on V_R because ⟨u,u⟩ = ⟨C(u),C(u)⟩ = \overline{⟨u,u⟩}, so ⟨u,u⟩ ∈ R).
- Decomposition: every v ∈ V decomposes uniquely as v = u + i w with u,w ∈ V_R. Explicitly
  u = (v + C(v))/2,   w = (v − C(v))/(2i).
  Thus V = V_R ⊕ iV_R as a complex vector space; equivalently, V is the complexification of V_R and C acts as "complex conjugation" on this decomposition by C(u + i w) = u − i w.
- Conversely, any real subspace U of V with V = U ⊕ iU (as complex spaces) defines a conjugation: the map C(u + i w) := u − i w is a conjugate-linear involution that fixes U. Hence conjugations on V are in one-to-one correspondence with choices of an underlying real form U satisfying V = U ⊕ iU.

How vectors interact with C
- Fixed vectors: v ∈ V_R iff C(v) = v. Purely imaginary vectors relative to V_R are those of the form i u with u ∈ V_R, and they satisfy C(i u) = − i u.
- Real and imaginary parts: for any v ∈ V, its "real part" Re(v) and "imaginary part" Im(v) relative to C are
  Re(v) = (v + C(v))/2 ∈ V_R,   Im(v) = (v − C(v))/(2i) ∈ V_R,
  so v = Re(v) + i Im(v).
- Inner products: for u,v ∈ V_R the inner product ⟨u,v⟩ is real; more generally ⟨C(u),C(v)⟩ = \overline{⟨u,v⟩}.

How operators interact with C
- Conjugation-by-C: if T: V → V is complex-linear, then the map T^C := C T C is also complex-linear. Indeed for α ∈ C,
  T^C(α v) = C T C(α v) = C T(\overline{α} C(v)) = C(\overline{α} T C(v)) = α C T C(v) = α T^C(v).
- Commutant and real-linear operators:
  - A complex-linear operator A commutes with C (i.e. AC = CA) if and only if A preserves the real form V_R, meaning A(V_R) ⊆ V_R. In that case A restricts to a real-linear operator on V_R, and A is the complex-linear extension of that real operator to V.
  - Conversely, any real-linear operator S: V_R → V_R extends uniquely to a complex-linear operator on V by complex-linearity on V = V_R ⊕ iV_R; this extension commutes with C.
- Compatibility with adjoints: if A is complex-linear, then (C A C)* = C A* C because taking adjoints reverses conjugation in the inner product and C implements conjugation on the space.
- Matrices and coordinates: choosing a real orthonormal basis of V_R yields a complex orthonormal basis of V; with respect to that basis C acts by coordinatewise complex conjugation, and complex-linear operators that commute with C are exactly those with real matrix entries in that basis.

Example (standard conjugation)
- On C^n with the standard inner product, coordinatewise complex conjugation C(z1,...,zn) = (\overline{z1},..., \overline{zn}) is a conjugation. The fixed subspace is R^n ⊂ C^n. Any real matrix (n×n with real entries) defines a complex-linear operator on C^n that commutes with C; conversely, commuting with C forces the matrix to be real.

Summary of key equivalences
- Conjugation C on V ↔ choice of real form V_R with V = V_R ⊕ iV_R.
- A complex-linear operator A preserves that real form (A(V_R) ⊆ V_R) ↔ A commutes with C.
- The decomposition v = Re(v) + i Im(v) and the formulas Re(v) = (v + C(v))/2, Im(v) = (v − C(v))/(2i) give explicit passage between complex vectors and their real-form coordinates.

Polar decomposition

Statement
Let V be a finite-dimensional complex inner-product space and T ∈ L(V). There exists a unitary operator U ∈ L(V) and a positive (self-adjoint, positive semidefinite) operator P ∈ L(V) such that
T = U P.
Moreover one can take P = |T| := (T* T)^{1/2}. If T is invertible then U is unique; in general U is uniquely determined on ran(|T|) and may be chosen arbitrarily unitary on ker(|T|).

Construction and proof
1) Define the positive factor. Set A := T* T. Then A is self-adjoint and positive, so it has a unique positive square root |T| := A^{1/2}. Thus |T| is self-adjoint, positive, and ran(|T|) = ran(A) = ran(T* T).

2) Relate norms. For every x ∈ V,
||T x||^2 = ⟨T x, T x⟩ = ⟨T* T x, x⟩ = ⟨|T|^2 x, x⟩ = |||T| x||^2.
Hence ||T x|| = |||T| x|| for all x. In particular ker(|T|) = ker(T).

3) Define U on ran(|T|). For y in ran(|T|) there exists x with y = |T| x; define
U y := T x.
This is well-defined: if |T| x1 = |T| x2 then |T|(x1−x2)=0 so x1−x2 ∈ ker(|T|)=ker(T), hence T x1 = T x2. Further, by the equality of norms,
||U y|| = ||T x|| = |||T| x|| = ||y||,
so U is an isometry on ran(|T|).

4) Extend U to a unitary. Choose an orthonormal basis of ker(|T|) and an orthonormal complement of ran(|T|); extend U arbitrarily as a unitary map from (ran(|T|))⊥ to ker(T)⊥ (or choose any unitary extension on the orthogonal complement). The resulting U is unitary on V and satisfies U(|T| x) = T x for all x, hence T = U |T|.

Uniqueness remarks
If T is invertible then |T| is invertible, so ran(|T|)=V and the above definition forces U uniquely by U = T |T|^{-1}. If T is not injective, U is only determined on ran(|T|) and can be chosen arbitrarily (unitarily) on the orthogonal complement.

Alternative right-polar form
One can similarly write T = Q V with Q = (T T*)^{1/2} positive and V unitary; this is the “right” polar decomposition. Both forms are useful; the standard choice is T = U |T| with |T| = (T* T)^{1/2}.

Uses and consequences
- Identification of the positive factor: the positive factor in the polar decomposition of T is precisely |T| = (T* T)^{1/2}, the unique positive square root of T* T.
- Norms and singular values: the eigenvalues of |T| are the singular values of T; polar decomposition separates the action of T into a positive scaling (|T|) followed by a unitary rotation (U).
- Computation: if T is diagonalized by a singular value decomposition T = W Σ V*, then |T| = V Σ V* and U = W V*.
- Functional calculus: many spectral properties of T* T transfer to |T|, allowing estimates like ||T|| = |||T||| and spectral bounds derived from |T|.

Example (brief)
If T is invertible then U = T |T|^{-1} and |T| = (T* T)^{1/2}; check U is unitary because
U* U = |T|^{-1} T* T |T|^{-1} = |T|^{-1} |T|^2 |T|^{-1} = I.

This completes the derivation and identification of the positive factor in the polar decomposition T = U |T|.

Singular values and the singular value decomposition (SVD)

Definition via T* T
- Let T: V → W be a linear operator between finite-dimensional complex inner-product spaces. Form the operator T* T on V. This operator is self-adjoint and positive:
  - Self-adjoint: (T* T)* = T* (T*)* = T* T.
  - Positive: for every x in V, ⟨T* T x, x⟩ = ⟨T x, T x⟩ = ‖T x‖^2 ≥ 0.
- Therefore T* T has real, nonnegative eigenvalues and admits an orthonormal basis of eigenvectors (spectral theorem).

Singular values
- The singular values of T are the nonnegative square roots of the eigenvalues of T* T.
  - If T* T v_i = λ_i v_i with λ_i ≥ 0 and {v_i} an orthonormal eigenbasis of V, then the corresponding singular value σ_i is σ_i = √λ_i.
- List the singular values in nonincreasing order σ_1 ≥ σ_2 ≥ ··· ≥ σ_r > 0, where r = rank(T). Any remaining σ_i are zero.

Constructing an SVD
1. Choose an orthonormal eigenbasis {v_1, …, v_n} of V for T* T, arranged so that T* T v_i = σ_i^2 v_i and σ_1 ≥ σ_2 ≥ ··· ≥ σ_n ≥ 0.
2. For each i with σ_i > 0, define u_i = (1/σ_i) T v_i ∈ W. Then:
   - ‖u_i‖ = 1, because ‖T v_i‖ = √⟨T* T v_i, v_i⟩ = σ_i.
   - The vectors {u_i : σ_i > 0} are orthonormal in W. (If i ≠ j with σ_i, σ_j > 0, ⟨u_i, u_j⟩ = (1/(σ_i σ_j)) ⟨T v_i, T v_j⟩ = (1/(σ_i σ_j)) ⟨T* T v_i, v_j⟩ = 0.)
3. Extend {u_i : σ_i > 0} to an orthonormal basis {u_1, …, u_m} of W by adding orthonormal vectors corresponding to the orthogonal complement of the image of T.
4. Then for every x ∈ V,
   T x = ∑_{i=1}^r σ_i ⟨x, v_i⟩ u_i,
   where r = number of positive singular values (rank of T). Equivalently,
   T = ∑_{i=1}^r σ_i u_i ⊗ v_i*,
   meaning T acts by projecting onto v_i, scaling by σ_i, and mapping to u_i.
5. In matrix terms (with orthonormal bases {v_i} of V and {u_i} of W), T has the factorization
   T = U Σ V*,
   where V is the unitary matrix whose columns are v_i, U is the unitary matrix whose columns are u_i, and Σ is the rectangular diagonal matrix with singular values σ_1, …, σ_r on the diagonal and zeros elsewhere.

Consequences and remarks
- Rank and nullspace: rank(T) = number of positive singular values. The nullspace of T is the span of the v_i with σ_i = 0.
- Norms: the operator norm ‖T‖ = σ_1 (largest singular value); the Hilbert–Schmidt (Frobenius) norm satisfies ‖T‖_HS^2 = ∑ σ_i^2.
- Uniqueness: singular values σ_i are uniquely determined (including multiplicities). The choice of orthonormal singular vectors v_i, u_i is unique up to unitary changes within eigenspaces corresponding to repeated singular values.
- Geometric view: SVD diagonalizes T up to unitary changes of basis, expressing T as orthogonal/unitary rotations followed by nonnegative scalings along orthogonal directions, then another rotation.

Unitary Triangularization (Schur Decomposition)

Statement (Schur). Let V be a finite-dimensional complex inner product space and T ∈ L(V). Then there exists an orthonormal basis of V relative to which the matrix of T is upper triangular. Equivalently, there is a unitary operator U (change of orthonormal basis) such that U* T U is upper triangular.

Construction / proof (inductive, producing the unitary change of basis)
1. Base case: If dim V = 1 the statement is trivial.
2. Inductive step: Assume true for all complex inner product spaces of dimension < n, and let dim V = n. Since the field is C, T has at least one eigenvalue λ and an eigenvector v ≠ 0 with T v = λ v.
3. Normalize v: set e1 = v/||v||. Extend {e1} to an orthonormal basis of V (e.g. by Gram–Schmidt). Let W = {e1}⊥, the orthogonal complement of span{e1}. For any w ∈ W consider the inner product ⟨T w, e1⟩; compute
   ⟨T w, e1⟩ = ⟨w, T* e1⟩.
   But by T e1 = λ e1 and linearity we obtain that T maps W into W plus possibly a multiple of e1; more concretely, for any w ∈ W,
   T w = α e1 + w' with w' ∈ W.
   Thus W is invariant under the map S = P_W ∘ T|_W, where P_W is orthogonal projection onto W. In particular S ∈ L(W) and dim W = n − 1.
4. Apply the induction hypothesis to S on W: there exists an orthonormal basis e2, …, en of W in which the matrix of S is upper triangular.
5. Combine e1 with e2, …, en to get an orthonormal basis of V. In this basis the matrix of T takes the block form
   [ λ  * ]
   [ 0  R ]
   where R is the upper triangular matrix of S. Hence the full matrix is upper triangular.

Thus an orthonormal basis {e1, …, en} has been produced; if U is the unitary operator whose columns are these basis vectors (expressed in any prior orthonormal basis), then U* T U is upper triangular.

How to see this as a unitary change of basis. If {u1, …, un} is any orthonormal basis of V and {e1, …, en} is the orthonormal basis produced above, form the unitary matrix U whose jth column is the coordinates of ej relative to {u1, …, un}. Then the matrix of T in the e-basis equals U* [T]_u U, so U* [T]_u U is upper triangular. This is the unitary similarity (change of orthonormal basis) that triangularizes T.

Connection between triangular form and eigenvalues
- If a linear operator has an upper triangular matrix with respect to some basis, then its diagonal entries are eigenvalues. Reason: for an upper triangular n×n matrix A, the characteristic polynomial det(A − tI) equals ∏_{j=1}^n (a_{jj} − t); hence the roots of the characteristic polynomial (the eigenvalues, counted with algebraic multiplicity) are exactly the diagonal entries.
- Conversely, Schur’s theorem shows that for any T on a complex inner product space one can find an orthonormal basis making T upper triangular, so the eigenvalues of T appear on the diagonal of this triangular matrix (in some order).

Remarks and consequences
- The Schur decomposition is a unitary similarity: every complex matrix A is unitarily similar to an upper triangular matrix T = U* A U.
- The diagonal of the Schur form lists the eigenvalues (possibly repeated) of T. The order along the diagonal can be chosen arbitrarily by selecting the order in which eigenvectors (and invariant complements) are picked.
- A normal operator is diagonalizable by a unitary change of basis: if T is normal and triangular in an orthonormal basis, the off-diagonal entries must vanish, so the triangular matrix is in fact diagonal. Thus normality + Schur ⇒ unitary diagonalization.

Short example (2×2 intuition). For a 2-dimensional complex inner product space pick an eigenvector e1 of T and normalize it. Complete to an orthonormal basis {e1, e2}; in this basis T(e1) = λ e1 and T(e2) = α e1 + μ e2. The matrix is
[ λ  α ]
[ 0  μ ],
an upper triangular matrix whose diagonal entries λ, μ are the eigenvalues.

This completes the construction of a unitary change of orthonormal basis that makes T upper triangular and explains why the diagonal entries are exactly the eigenvalues.

Multilinear maps

Definition
- Let V1, V2, …, Vk and W be vector spaces over a field F. A map T : V1 × V2 × ··· × Vk → W is multilinear if for each i = 1,…,k the map is linear in the i-th argument when the other k−1 arguments are held fixed. Concretely, for each i, for all vectors vj ∈ Vj (j ≠ i), and for all u, u′ ∈ Vi and scalars a, b ∈ F,
  T(v1, …, vi−1, a u + b u′, vi+1, …, vk) = a T(v1, …, vi−1, u, vi+1, …, vk) + b T(v1, …, vi−1, u′, vi+1, …, vk).

Basic consequences used later
- Linearity in a single slot. Fix all arguments except the i-th; the resulting map Vi → W, u ↦ T(v1, …, vi−1, u, vi+1, …, vk), is a linear map for each choice of the fixed vectors.
- Pulling scalars out of any slot. For any scalar c ∈ F and any slot i,
  T(v1, …, c vi, …, vk) = c T(v1, …, vi, …, vk).
- Additivity in any slot. For any u, u′ ∈ Vi,
  T(v1, …, vi + vi′, …, vk) = T(v1, …, vi, …, vk) + T(v1, …, vi′, …, vk).
- Vanishing on a zero argument. If any argument is the zero vector, T evaluates to zero:
  If vi = 0 for some i, then T(v1, …, vk) = 0.
- Distributivity across multiple slots (multilinear expansion). If several slots are sums or scalar multiples, expand by applying linearity slot-by-slot (the full value is the sum of terms obtained by distributing each sum and pulling out scalars).
- Composition with linear maps on inputs. If Sj : Uj → Vj are linear maps for j = 1,…,k, then the composed map
  T ∘ (S1 × ··· × Sk) : U1 × ··· × Uk → W, (u1,…,uk) ↦ T(S1(u1),…,Sk(uk))
  is multilinear.
- Postcomposition with a linear map on the output. If R : W → X is linear, then R ◦ T : V1 × … × Vk → X is multilinear.
- Special case: k = 2 gives bilinear maps; the above properties apply with k = 2.

These simple algebraic consequences (linearity in each slot, scalar pull-out, additivity, vanishing with a zero argument, closure under pre- and post-composition with linear maps) are the tools used repeatedly in the chapter to manipulate and build multilinear constructions.

Alternating (skew‑symmetric) multilinear maps

Definition. Let V be a vector space over a field F. A map ω: V^n → F is multilinear if it is linear in each of its n arguments separately. The map ω is called alternating (or skew‑symmetric) if it satisfies the vanishing property
- whenever two arguments agree, ω(v1,…,vn) = 0; equivalently, if vi = vj for some i ≠ j then ω(v1,…,vn) = 0.

Immediate consequences and sign behavior.
- Transposition changes sign. If ω is alternating then swapping two arguments multiplies the value by −1. More precisely, for any i ≠ j and any vectors v1,…,vn,
  ω(…, vi, …, vj, …) = − ω(…, vj, …, vi, …).
  Proof sketch: Let t be a scalar and replace vi by vi + t vj. Linearity in the i‑th slot gives an expression linear in t; alternation forces the coefficient of t^0 and t^1 to behave so that the two one‑term evaluations with vi and vj must be negatives of each other, yielding the sign change for the transposition.
- General permutations. Any permutation σ ∈ Sn acts by permuting the arguments, and because transpositions generate Sn, one gets
  ω(v_{σ(1)},…,v_{σ(n)}) = sgn(σ) · ω(v1,…,vn),
  where sgn(σ) is the sign (±1) of the permutation. Thus alternating maps are completely determined up to sign by how they reorder inputs.

Alternation implies vanishing on dependent lists. If the list v1,…,vn is linearly dependent, then ω(v1,…,vn) = 0. Reason: if some vi is a linear combination of the others, multilinearity reduces the evaluation to a linear combination of evaluations in which two arguments agree; each of those evaluations is zero by alternation.

Why this restriction leads to determinants. The determinant of an n×n matrix can be viewed as a map det: V^n → F where V = F^n and det takes the n column vectors to a scalar. The defining properties usually imposed on det are:
- multilinearity in the columns,
- alternating (so det is 0 when columns are linearly dependent and changes sign when two columns are swapped),
- normalization (det(I) = 1 for the identity matrix).

These three properties force a unique multilinear alternating functional with that normalization; explicitly, det is the unique alternating multilinear map that sends the standard basis tuple to 1. Alternation encodes the crucial geometric and algebraic features of determinants: it makes the determinant detect linear dependence (zero volume), it records orientation via sign changes under column swaps, and combined with multilinearity it yields the usual expansion by permutations (the sum over σ ∈ Sn of sgn(σ) times the product of appropriate entries). Thus requiring multilinearity together with the alternating property is the natural structural restriction that produces the determinant.

Tensor Product and Its Universal Property

Definition (informal). Given vector spaces V1,...,Vk over the same field F, a tensor product is a pair (T, τ) where T is a vector space and τ : V1 × ··· × Vk → T is a multilinear map with the following universal property: for every vector space W and every multilinear map f : V1 × ··· × Vk → W there exists a unique linear map F : T → W such that f = F ◦ τ. We write elements τ(v1,...,vk) as simple tensors v1 ⊗ ··· ⊗ vk and denote T by V1 ⊗ ··· ⊗ Vk.

Universal property (precise). The map τ : V1 × ··· × Vk → V1 ⊗ ··· ⊗ Vk is multilinear, and for each multilinear f : V1 × ··· × Vk → W there is a unique linear map F : V1 ⊗ ··· ⊗ Vk → W with F(v1 ⊗ ··· ⊗ vk) = f(v1,...,vk) for all vi ∈ Vi. This gives a natural bijection
Multilinear(V1 × ··· × Vk, W) ≅ Linear(V1 ⊗ ··· ⊗ Vk, W).

Existence (construction sketch). Construct the tensor product as a quotient of a free vector space:
- Let F be the free vector space with basis consisting of formal symbols [v1,...,vk] for each (v1,...,vk) ∈ V1 × ··· × Vk.
- Let R be the subspace of F generated by all elements enforcing multilinearity:
  * For each i, vi, v'i ∈ Vi and scalars a,b ∈ F,
    [v1,..., a vi + b v'i, ..., vk] − a [v1,...,vi,...,vk] − b [v1,...,v'i,...,vk] ∈ R.
- Define V1 ⊗ ··· ⊗ Vk := F / R and write v1 ⊗ ··· ⊗ vk for the equivalence class of [v1,...,vk].
- The canonical map τ(v1,...,vk) = v1 ⊗ ··· ⊗ vk is multilinear by construction.
- Given any multilinear f : V1 × ··· × Vk → W, there is a well-defined linear map F on F sending [v1,...,vk] to f(v1,...,vk). The relations defining R ensure F(R)=0, so F descends to a unique linear map on F/R satisfying F(v1 ⊗ ··· ⊗ vk)=f(v1,...,vk). This proves existence and the required universal property.

Uniqueness up to unique isomorphism. If (T, τ) and (T', τ') both satisfy the universal property, apply the property twice: there are unique linear maps φ : T → T' with φ ◦ τ = τ' and ψ : T' → T with ψ ◦ τ' = τ. Uniqueness forces ψ ◦ φ = id_T and φ ◦ ψ = id_{T'}, so φ is a canonical isomorphism carrying τ(v1,...,vk) to τ'(v1,...,vk). Thus the tensor product is determined uniquely up to unique isomorphism.

Correspondence between multilinear and linear maps. The universal property gives the bijection explicitly:
- Given multilinear f : V1 × ··· × Vk → W, the corresponding linear map F : V1 ⊗ ··· ⊗ Vk → W is determined by F(v1 ⊗ ··· ⊗ vk) = f(v1,...,vk) and extended linearly.
- Conversely, given a linear map L : V1 ⊗ ··· ⊗ Vk → W, the composition f := L ◦ τ is multilinear and recovers L uniquely because L is determined by its values on simple tensors.

Remarks and consequences
- Simple (pure) tensors are elements of the form v1 ⊗ ··· ⊗ vk. Not every element of the tensor product is simple; general elements are finite linear combinations of simple tensors.
- If each Vi has finite dimension dim Vi = ni, and {e^{(i)}_j} is a basis of Vi, then the simple tensors e^{(1)}_{j1} ⊗ ··· ⊗ e^{(k)}_{jk} form a basis of V1 ⊗ ··· ⊗ Vk. Hence dim(V1 ⊗ ··· ⊗ Vk) = n1·n2·...·nk.
- For k = 2 this recovers the usual V ⊗ W with the bijection Bilinear(V × W, X) ≅ Linear(V ⊗ W, X).

This construction and correspondence are the fundamental reason one can treat multilinear problems as linear ones by passing to the appropriate tensor product.

Exterior power and wedge product

- Exterior power Λ^k V (k-th exterior power)
  - For a vector space V over a field F and integer k ≥ 0, the k-th exterior power Λ^k V is a vector space together with a canonical alternating k-linear map
    v1,...,vk ↦ v1 ∧ ... ∧ vk ∈ Λ^k V
    characterized by the universal property: for every vector space W and every alternating k-linear map A : V^k → W there exists a unique linear map L : Λ^k V → W with A = L ∘ (∧). In other words, alternating k-linear maps from V^k are the same as linear maps out of Λ^k V.
  - Concretely, Λ^k V can be constructed as the quotient of the k-fold tensor power V⊗...⊗V by the subspace generated by tensors that enforce alternating behavior (tensors that become zero when two slots are equal, or equivalently generated by relations v⊗w + w⊗v = 0 and multilinearity). The equivalence class of v1⊗...⊗vk is denoted v1 ∧ ... ∧ vk.
  - If {e1,...,en} is a basis of V, then the wedge products e_{i1} ∧ ... ∧ e_{ik} with i1 < ... < ik form a basis of Λ^k V. Thus dim Λ^k V = C(n,k) when dim V = n.

- Top exterior power Λ^n V
  - When V has finite dimension n, the top exterior power Λ^n V = Λ^{dim V} V is especially important. It has dimension 1. A basis for Λ^n V is any nonzero wedge of n linearly independent vectors, e.g. e1 ∧ ... ∧ en for a basis {e1,...,en}.
  - Because Λ^n V is 1-dimensional, any linear endomorphism of Λ^n V is scalar multiplication by some λ ∈ F. This scalar is exactly the determinant when the endomorphism comes from a linear operator on V (see below).

- Wedge product
  - The wedge product is a bilinear map
    ∧ : Λ^k V × Λ^l V → Λ^{k+l} V
    defined on simple wedges by (v1 ∧ ... ∧ vk) ∧ (w1 ∧ ... ∧ wl) = v1 ∧ ... ∧ vk ∧ w1 ∧ ... ∧ wl and extended bilinearly.
  - Properties:
    - Anticommutativity on simple elements: for α ∈ Λ^k V, β ∈ Λ^l V one has α ∧ β = (−1)^{kl} β ∧ α.
    - Associativity up to the natural identifications of grading: (α ∧ β) ∧ γ = α ∧ (β ∧ γ).
    - The wedge product makes Λ•V = ⊕_k Λ^k V into a graded-anticommutative algebra (the exterior algebra).

- How alternating multilinear maps factor through exterior powers (and connection to determinant)
  - Universal factoring property restated: given any alternating k-linear map A : V^k → W, there exists a unique linear map L : Λ^k V → W such that A(v1,...,vk) = L(v1 ∧ ... ∧ vk) for all v1,...,vk ∈ V. Thus Λ^k V is the universal recipient of alternating k-linear maps.
  - This means one can study alternating forms, multilinear invariants, and objects like volume forms by working with linear maps on Λ^k V rather than directly with k-linear alternating maps on V^k.
  - Determinant as an instance of the factorization through the top exterior power:
    - Let T : V → V be linear and dim V = n. Then T induces a linear map Λ^n T : Λ^n V → Λ^n V defined by
      Λ^n T (v1 ∧ ... ∧ vn) = T(v1) ∧ ... ∧ T(vn).
    - Since Λ^n V is 1-dimensional, Λ^n T acts by multiplication by some scalar λ. Define det(T) := λ. Equivalently, for any basis {e1,...,en}, writing T(ej) = ∑_i a_{ij} e_i, we have
      T(e1 ∧ ... ∧ en) = (det A) (e1 ∧ ... ∧ en),
      where A = (a_{ij}). This recovers the usual determinant and gives an invariant, coordinate-free characterization: the determinant is the scalar by which T scales the top exterior power.
  - The factorization viewpoint clarifies uniqueness and multilinear properties of the determinant: determinant is the unique alternating n-linear map V^n → F that sends a chosen basis to 1 (equivalently, the unique linear functional on Λ^n V sending e1 ∧ ... ∧ en to 1).

Determinant — definition and core properties

Definition (Axler’s preferred approach). Fix an n-dimensional vector space V over a field F and an ordered basis e = (e1,...,en). There is a unique function D: V^n → F with the three properties below:
- Multilinearity: D is linear in each argument separately.
- Alternating: If two arguments are equal then D(...,vi,...,vj,...) = 0; equivalently, D(...,vi,...,vj,...) changes sign when two arguments are swapped.
- Normalization: D(e1,...,en) = 1.

This D is called the determinant form (relative to the chosen ordered basis). For a linear operator T ∈ L(V), the determinant det(T) is defined by the scalar that relates D(Tv1,...,Tvn) to D(v1,...,vn):
D(Tv1,...,Tvn) = det(T) · D(v1,...,vn)
for all v1,...,vn ∈ V. (In particular, taking v1 = e1, ..., vn = en, det(T) = D(Te1,...,Ten).)

Immediate consequences and derivations of key properties

1. Multilinearity of D and linearity of det in columns/rows
- By definition D is multilinear: for each fixed slot j and fixed vectors in the other slots, D is linear in the j-th argument. This implies the usual linearity in columns (or rows) when one represents vectors in coordinates.

2. Alternating property and consequences
- Alternating ⇒ swapping two arguments changes sign:
  If D is alternating then D(...,vi,...,vj,...) = −D(...,vj,...,vi,...).
  Proof: For any pair of positions swap them and note that adding the two expressions gives D with two equal arguments, hence zero.
- If two arguments are equal then D = 0.
- In particular, if the list v1,...,vn is linearly dependent then D(v1,...,vn) = 0 (because one argument is a linear combination of the others, and multilinearity + alternating force zero).

3. Effects of elementary row/column operations (as seen on the list of n vectors)
Let v1,...,vn be the columns (or rows) considered as the n arguments of D.
- Scaling a single argument: Replacing vj by αvj multiplies D by α (by multilinearity).
- Swapping two arguments: Swapping vi and vj multiplies D by −1 (alternating property).
- Adding a scalar multiple of one argument to another: Replacing vj by vj + αvi leaves D unchanged if vi is one of the other arguments, because multilinearity gives D(...,vj+αvi,...) = D(...,vj,...) + αD(...,vi,...) and the second term is zero when vi appears twice (alternating). This is why adding a multiple of one row to another does not change the determinant.

4. Determinant of matrices / normalization and independence of basis
- If one fixes the ordered basis e and identifies linear maps with their matrix relative to e, then det(T) = D(Te1,...,Ten) equals the usual determinant of the matrix of T in that basis.
- The normalization D(e1,...,en) = 1 fixes D uniquely; changing the ordered basis changes the sign/scale of D on tuples of basis vectors accordingly but the scalar det(T) is independent of basis (it transforms compatibly so det is a well-defined invariant of T).

5. Triangular matrices and diagonal entries
- If a linear operator T is represented by an upper (or lower) triangular matrix in the chosen basis, then D(Te1,...,Ten) = (product of diagonal entries) · D(e1,...,en). Thus det(T) equals the product of the diagonal entries. This follows by expanding each Tej = sum_i aij ei and using multilinearity together with the fact that any term that picks a non-diagonal index twice vanishes by alternation; only the product of diagonal coefficients survives.

6. Multiplicativity: det(ST) = det(S) det(T)
- For S, T ∈ L(V) we have, for all v1,...,vn,
  D(S(Tv1),...,S(Tvn)) = det(S) · D(Tv1,...,Tvn) = det(S) det(T) · D(v1,...,vn).
  But the left-hand side is by definition D((ST)v1,...,(ST)vn) = det(ST) · D(v1,...,vn). Comparing scalars gives
  det(ST) = det(S) det(T).
- This shows determinant is a multiplicative map from the algebra of endomorphisms of V to F.

7. More consequences
- det(I) = 1 by normalization.
- det is zero iff the operator is noninvertible: If T is not invertible then Tv1,...,Tvn are linearly dependent, so D(Tv1,...,Tvn)=0 for all v1,...,vn, hence det(T)=0. Conversely, if det(T)=0 then the image of T is contained in a proper subspace, so T is not invertible.
- det(T−1) = det(T)−1 for invertible T (from multiplicativity and det(I)=1).

These properties together capture the core behavior Axler emphasizes: determinant is the unique alternating multilinear scalar function normalized on a basis, it responds predictably to the elementary row/column operations (scaling, swapping, adding multiples), equals the product of diagonal entries for triangular matrices, and is multiplicative with respect to composition of operators.

Determinant as an invertibility/volume criterion

Setup. Fix a finite-dimensional vector space V of dimension n over a field F. Let D be the determinant form on V: the unique alternating n-linear map D : V^n → F such that D(e1,...,en) = 1 for some chosen ordered basis (e1,...,en). For a linear operator T ∈ L(V) define det(T) by
D(Tv1,...,Tvn) = det(T) D(v1,...,vn)
for all v1,...,vn ∈ V. (Existence and uniqueness of such a scalar follows from the fact that composing D with T on each argument gives another alternating n-linear form, and every alternating n-linear form is a scalar multiple of D.)

1) Determinant detects invertibility (det(T) ≠ 0 ⇔ T is invertible).

Proof that invertible ⇒ determinant nonzero.
If T is invertible then T takes any basis (v1,...,vn) of V to another basis (Tv1,...,Tvn). Since D evaluated on a basis is nonzero (alternating n-linear form is nonzero on any basis), D(Tv1,...,Tvn) ≠ 0. By definition D(Tv1,...,Tvn) = det(T) D(v1,...,vn) and D(v1,...,vn) ≠ 0, so det(T) ≠ 0.

Proof that determinant nonzero ⇒ invertible.
Assume det(T) ≠ 0. Suppose for contradiction that T is not injective, so there exists nonzero x ∈ V with Tx = 0. Extend {x} to a basis (x, v2,...,vn). Because D is alternating, any n-tuple with two equal entries gives D = 0; in particular replace the first argument by Tx = 0 and get D(Tx, Tv2,...,Tvn) = D(0, Tv2,...,Tvn) = 0. But D(Tx,...,Tvn) = det(T) D(x, v2,...,vn). Since D(x, v2,...,vn) ≠ 0 (it is the value of D on a basis), we would get det(T) = 0, contradicting the hypothesis. Hence T must be injective, and on a finite-dimensional space injective ⇔ surjective ⇔ invertible. Thus det(T) ≠ 0 implies T is invertible.

Therefore det(T) ≠ 0 exactly when T is invertible.

2) Multiplicativity and behavior on matrices.
If S,T ∈ L(V) then the composite ST satisfies
D(STv1,...,STvn) = det(S) D(Tv1,...,Tvn) = det(S) det(T) D(v1,...,vn),
so det(ST) = det(S) det(T). This is the coordinate-free reason that determinants of matrices multiply.

If one chooses a basis and represents T by a matrix A, then det(T) equals the usual determinant of A. Changing basis multiplies the matrix by invertible change-of-basis matrices on left and right, and multiplicativity plus det(I) = 1 show det is invariant under that conjugation, so det is well-defined for the operator independent of coordinates.

3) Geometric (volume) interpretation.
Interpret D as an oriented volume form: for the chosen basis (e1,...,en) the parallelepiped spanned by e1,...,en is taken to have oriented volume 1. For any n-tuple (v1,...,vn), interpret |D(v1,...,vn)| as the usual (unsigned) n-dimensional volume of the parallelepiped spanned by v1,...,vn. Then for T ∈ L(V) the equation
D(Tv1,...,Tvn) = det(T) D(v1,...,vn)
says T multiplies the oriented volume of every parallelepiped by the scalar det(T). In particular the unsigned volume is multiplied by |det(T)|. Thus det(T) is the signed volume-scaling factor of T.

Remarks tying structure to proofs used later.
- Alternating n-linearity is the structural property that makes D vanish exactly on linearly dependent lists; this underlies the algebraic proof that det(T) = 0 iff T is singular.
- Multiplicativity of determinant follows immediately from composing the action of two maps on each argument of an alternating form; this structural viewpoint avoids coordinate calculations and yields the matrix product determinant formula as a corollary.
- The volume interpretation provides geometric intuition for sign (orientation reversal when det < 0) and for why determinants of elementary operations behave as they do (e.g., shear keeps volume, so det = 1; scaling one basis vector by α scales det by α).

These facts make determinant a fundamental invariant of linear maps: it is an algebraic criterion for invertibility and a geometric measure of how a linear map scales oriented volume.