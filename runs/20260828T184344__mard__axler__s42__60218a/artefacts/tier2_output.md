Vector space (definition and examples)

Definition
Let F be a field. A vector space over F is a set V together with two operations:
- vector addition: a map + : V × V → V, written (u, v) ↦ u + v;
- scalar multiplication: a map · : F × V → V, written (a, v) ↦ a v;

such that for all u, v, w in V and all a, b in F the following axioms hold.

Additive axioms
1. (Associativity) u + (v + w) = (u + v) + w.
2. (Commutativity) u + v = v + u.
3. (Additive identity) There exists 0 in V with 0 + v = v for all v in V.
4. (Additive inverse) For each v in V there exists w in V (denoted −v) with v + (−v) = 0.

Scalar multiplication axioms
5. (Compatibility with field multiplication) a(b v) = (ab) v.
6. (Identity scalar) 1 v = v, where 1 is the multiplicative identity in F.
7. (Distributivity over vector addition) a (u + v) = a u + a v.
8. (Distributivity over field addition) (a + b) v = a v + b v.

Remarks
- The additive identity 0 and each additive inverse −v are unique and follow from the axioms.
- When needed we write “V is a vector space over F” or “an F-vector space”.
- When F = R or F = C we commonly speak of real or complex vector spaces.

Standard examples
1. F^n: The set of n-tuples (x1,...,xn) with xi in F, with coordinatewise addition and scalar multiplication. This is the prototypical finite-dimensional vector space.

2. Functions F^S: For any set S, the set of all functions f : S → F with pointwise addition (f+g)(s)=f(s)+g(s) and (a f)(s)=a·f(s). Special cases:
   - F^N = sequences of field elements.
   - C(R) or C([a,b]): continuous real- (or complex-) valued functions on R (or [a,b]).

3. Polynomial space F[x]: The set of all polynomials with coefficients in F, with usual addition and scalar multiplication. Subspaces include polynomials of degree ≤ n.

4. Matrices F^{m×n}: All m×n matrices over F, with entrywise operations. In particular F^{n×n} is a vector space of dimension n^2.

5. Subspaces: Any subset W ⊆ V that contains 0, is closed under addition and scalar multiplication is itself a vector space over F (e.g., the set of solutions to a homogeneous linear system).

6. The zero vector space: {0}, consisting of only the zero vector, is a vector space over any field F.

Common non-examples (and why they fail)
1. The set of integers Z with usual + and scalar multiplication by real numbers: scalar multiplication by arbitrary reals is not defined in Z, so Z is not an R-vector space. (Z is a module over Z but not a vector space over a field like R.)

2. The positive real numbers R_{>0} under usual addition: not closed under additive inverses (no negatives), so additive inverse axiom fails.

3. The set of invertible n×n matrices GL_n(F): closed under multiplication but not under addition (sum of invertible matrices need not be invertible), so not a vector space.

4. The set of polynomials of exactly degree n (not allowing degree < n): not closed under addition (leading coefficients may cancel), so additive closure/inverse fails.

5. Any nonempty set with only a multiplication operation (e.g., (F\{0}, ·)) but no vector addition or scalar multiplication: missing axioms.

6. The empty set: there is no additive identity 0, so it cannot be a vector space.

How to check quickly whether a set with two operations is a vector space
- Verify closure under addition and scalar multiplication.
- Check existence of 0 and additive inverses.
- Check the distributive and compatibility axioms with scalars from F.
- If any of these fail (common failures are missing additive inverses or scalar multiplication not defined for all scalars), it's not a vector space.

This completes the definition and basic catalogue of examples and non-examples.

Linear combinations and span

Definition — linear combination.
Let V be a vector space over a field F, and let v1, …, vn be vectors in V. A vector of the form
    a1 v1 + a2 v2 + … + an vn
with scalars a1, …, an in F is called a linear combination of v1, …, vn. If S ⊆ V is any set, a linear combination of vectors from S means a finite sum a1 s1 + … + an sn with each si ∈ S and ai ∈ F.

Definition — span.
For S ⊆ V, the span of S, denoted span(S) (or span S), is the set of all linear combinations of vectors from S:
    span(S) = { a1 s1 + … + an sn : n ≥ 0, si ∈ S, ai ∈ F }.
By convention the case n = 0 gives the zero combination, so 0 ∈ span(S).

Proposition — span(S) is a subspace containing S.
Proof.
(1) S ⊆ span(S): for any s ∈ S, s = 1·s is a linear combination, so s ∈ span(S).
(2) span(S) is closed under addition and scalar multiplication: if x = ∑_{i=1}^m a_i s_i and y = ∑_{j=1}^n b_j t_j are in span(S) (with all s_i, t_j ∈ S), then x + y = ∑_{i=1}^m a_i s_i + ∑_{j=1}^n b_j t_j is again a finite linear combination of elements of S, hence in span(S). For λ ∈ F, λx = ∑_{i=1}^m (λ a_i) s_i is also a linear combination from S. Thus span(S) is a subspace.
□

Proposition — span(S) is the smallest subspace containing S.
More precisely: span(S) is contained in every subspace of V that contains S; equivalently, span(S) equals the intersection of all subspaces of V that contain S.
Proof.
Let U be any subspace with S ⊆ U. Because U is closed under linear combinations, every finite linear combination of elements of S lies in U, so span(S) ⊆ U. Therefore span(S) is contained in the intersection of all such U. Conversely, span(S) itself is a subspace containing S, so it appears among those U and thus equals that intersection. Hence span(S) is the smallest (by inclusion) subspace of V that contains S.
□

Comments and immediate consequences.
- span(∅) = {0}, since the only linear combination of no vectors is the zero vector.
- A set S spans V (i.e. span(S) = V) precisely when every vector of V is a linear combination of vectors from S; such an S is called a spanning set of V.
- The minimality property of span is often used to construct subspaces generated by given vectors and to reason about dependencies: any subspace that must contain certain vectors necessarily contains their span.

Linear independence and dependence

Definitions
- A list of vectors v1, v2, ..., vn in a vector space V is called linearly independent if the only scalars a1, a2, ..., an for which
  a1 v1 + a2 v2 + ... + an vn = 0
  are a1 = a2 = ... = an = 0. If there exists a choice of scalars not all zero that makes that linear combination equal to 0, the list is called linearly dependent.
- Equivalently, a list is linearly dependent iff some vector in the list can be written as a linear combination of the preceding vectors (more generally: of the other vectors in the list). A single zero vector always makes a list dependent. The empty list is (by convention) linearly independent.

How to use the definitions (practical checklist)
1. Write the equation a1 v1 + ... + an vn = 0.
2. Solve for the scalars a1,...,an (by inspection, comparing coordinates, or forming and row-reducing a matrix whose columns are the vi).
3. If the only solution is the trivial one (all ai = 0), the list is independent. If you find a nontrivial solution, the list is dependent.
4. Short tests:
   - If one of the vi is 0, the list is dependent.
   - If two vi are equal (or scalar multiples of each other), the list is dependent.
   - If you can express any vi as a linear combination of the others, the list is dependent.
   - For n vectors in an n-dimensional space, if the matrix with those vectors as columns has nonzero determinant (or full rank n), the list is independent.

Examples and proofs

Example 1 — dependent by direct relation
Let v1 = (1,0,0), v2 = (0,1,0), v3 = (1,1,0) in R^3.
Observe v3 = v1 + v2. Thus 1·v1 + 1·v2 + (−1)·v3 = 0 with scalars not all zero, so the list is linearly dependent.

Example 2 — independent by solving the defining equation
Let v1 = (1,0,0), v2 = (0,1,0), v3 = (0,0,1) in R^3.
Set a1 v1 + a2 v2 + a3 v3 = 0. Comparing coordinates gives a1 = 0, a2 = 0, a3 = 0. Only the trivial solution exists, so the list is linearly independent.

Example 3 — dependent because determinant is zero
Let v1 = (1,2,3), v2 = (4,5,6), v3 = (7,8,9) in R^3. Put these as columns of a 3×3 matrix. The determinant is 0 (the columns are linearly dependent because the third column is a linear combination of the first two). Concretely, one finds scalars (for example, 1·v1 − 2·v2 + 1·v3 = 0), so the list is linearly dependent.

Example 4 — single vector and the zero vector
- The list (0) is dependent since 1·0 = 0 gives a nontrivial relation.
- Any list containing 0 is dependent.
- Any single nonzero vector (v ≠ 0) is independent: a v = 0 implies a = 0.

Useful equivalent characterization (proof sketch)
If a1 v1 + ... + an vn = 0 and some ai ≠ 0, say ak ≠ 0, then
vk = −(a1/ak) v1 − ... − (a_{k−1}/ak) v_{k−1} − (a_{k+1}/ak) v_{k+1} − ... − (an/ak) vn,
so vk is a linear combination of the other vectors. Thus a nontrivial linear relation ⇔ some vector is a combination of the others. This gives a practical way to show dependence: find one vector expressible in terms of the others.

Summary checklist for proofs
- To prove independence: start from a1 v1 + ... + an vn = 0 and show a1 = ... = an = 0 (coordinate comparison or row reduction).
- To prove dependence: find explicit scalars, not all zero, that produce the zero vector, or show one vector is a linear combination of the others, or exhibit a repeated/zero/scalar-multiple vector.

Bases

Definition
- A list of vectors v1, v2, ..., vn in a vector space V is a basis of V if
  1) the list spans V (every vector in V is a linear combination of the vi), and
  2) the list is linearly independent (no nontrivial linear relation among the vi).
- Equivalently: a basis is a linearly independent spanning list.

Immediate consequence: If (v1,...,vn) is a basis of V, then every vector w in V can be written as
w = a1 v1 + a2 v2 + ... + an vn
for some scalars a1,...,an.

Uniqueness of coordinates
- The coefficients a1,...,an in the representation of w relative to a basis are unique.
- Proof sketch: Suppose w = sum ai vi = sum bi vi. Subtracting gives 0 = sum (ai − bi) vi. Linear independence implies each ai − bi = 0, so ai = bi for all i.

Coordinate vectors
- Given a basis (v1,...,vn), the n-tuple (a1,...,an) of coefficients of w is called the coordinate vector of w relative to that basis. It provides a unique coordinate representation of w.
- Notation: [w]_{(v1,...,vn)} = (a1,...,an).

Characterization by uniqueness
- A list (v1,...,vn) spans V and is linearly independent exactly when every vector in V has a unique expression as a linear combination of the vi. Thus "spanning + independence" ⇔ "every vector has a unique coordinate representation".

Examples
- Standard basis of R^2: e1 = (1,0), e2 = (0,1). Any (x,y) = x e1 + y e2; the coordinates are uniquely (x,y).
- Polynomials of degree ≤ 2: (1, x, x^2) is a basis of P2. Any p(x) = c0 + c1 x + c2 x^2 has unique coefficients (c0,c1,c2).

How to express a vector in a basis (practical method)
- If the basis vectors are written in components (e.g., columns in R^n), set up a linear system whose unknowns are the required coefficients and solve. Uniqueness ensures a single solution when the list is a basis.

Remarks
- A basis is always a list (ordered). Changing the order changes coordinate tuples but not the span or independence.
- In finite-dimensional spaces, bases have the same length (dimension), but the notion above applies to any list that both spans and is independent.

Dimension — the number that measures the size of a vector space — is introduced and made useful through the concept of a basis.

- Intuition: For finite-dimensional spaces, the size of the space should be the number of independent directions it contains. A basis captures exactly those directions: it is a linearly independent list that spans the whole space. Thus the length (number of vectors) of a basis is a natural measure of the space’s size.

- Definition (finite-dimensional intuition): If a vector space has a basis consisting of a finite number of vectors, we call the space finite-dimensional and we want that finite number to be the space’s dimension.

- Why length of a basis works as a definition:
  - A basis both spans and is independent, so its vectors are the minimal set needed to generate every vector in the space without redundancy. Counting them gives a meaningful size.
  - A key theorem (proved later in Axler) shows that any two bases of a finite-dimensional vector space have the same length. That fact justifies defining dimension as “the number of vectors in any basis” — the number is well defined.

- Examples for intuition:
  - R^n: the standard basis has n vectors, so R^n has dimension n. Every basis of R^n will also have n vectors.
  - Pn (polynomials of degree ≤ n): the list 1, x, x^2, …, x^n is a basis of length n+1, so dim Pn = n+1.
  - {0}: the zero vector space has no nonzero vectors; by convention its dimension is 0 (an empty basis).

- How this motivates later results:
  - Coordinates: a basis of length n lets us represent each vector uniquely by an n-tuple of scalars (coordinates). This identification underlies many concrete computations.
  - Subspace relations: comparing dimensions gives constraints (e.g., a subspace of a finite-dimensional space cannot have larger dimension than the whole space).
  - Linear maps: counting dimensions leads directly to fundamental theorems like rank-nullity (dim domain = rank + nullity) and to criteria for injectivity/surjectivity when dimensions match.

In short, for finite-dimensional spaces the length of a basis is the canonical measure of size; proving that all bases have the same length is what makes “dimension” a well-defined and powerful invariant.

Subspaces

Criterion (Subspace Test)
Let V be a vector space over a field F and let W be a subset of V. Then W is a subspace of V (i.e. W is itself a vector space with the same operations) if and only if
1. W is nonempty, and
2. W is closed under addition: for all u, v in W, u + v is in W, and
3. W is closed under scalar multiplication: for all a in F and u in W, a u is in W.

Equivalently, W is a subspace iff W is nonempty and for all a, b in F and u, v in W we have a u + b v in W (closure under all linear combinations of two vectors). Often one checks nonemptiness by noting 0 ∈ W (if 0 ∈ W then nonempty).

Why this works: these conditions ensure the vector-space axioms that involve addition and scalar multiplication hold in W (associativity, distributivity, etc., are inherited from V), and existence of additive identity and inverses follow from closure properties (0 = 0·u ∈ W; −u = (−1)u ∈ W).

Typical examples and verifications

1) Solution sets of homogeneous linear equations (null spaces)
Let T: V → W be a linear map. The null space (kernel)
    ker T = {v ∈ V : T(v) = 0}
is a subspace of V.

Proof: 0 ∈ ker T because T(0) = 0. If u, v ∈ ker T then T(u+v) = T(u)+T(v) = 0+0 = 0, so u+v ∈ ker T. If a ∈ F and u ∈ ker T then T(a u) = a T(u) = a·0 = 0, so a u ∈ ker T. Thus ker T satisfies the subspace test.

Contrast: the solution set of a nonhomogeneous system T(v) = w with w ≠ 0 is generally not a subspace, because it does not contain 0 (unless w = 0) and fails closure under scalar multiplication.

Example: For an m×n matrix A over F, the set {x ∈ F^n : A x = 0} is a subspace of F^n (the null space of A).

2) Coordinate subspaces of F^n
Fix n and consider the standard basis e1,...,en of F^n. For any index set I ⊆ {1,...,n} the coordinate subspace
    W = {x ∈ F^n : x_j = 0 for j ∉ I}
is a subspace. Equivalently, W = span{e_i : i ∈ I}.

Proof: If x,y ∈ W then coordinates outside I remain zero under addition, so x+y ∈ W. If a ∈ F and x ∈ W then scalar multiplication preserves zeros, so a x ∈ W. Hence W is a subspace. It is exactly the span of those standard basis vectors with indices in I, so it is the smallest subspace containing those basis vectors.

Example: In F^3 the set {(x,y,0): x,y ∈ F} is a 2-dimensional subspace spanned by e1 and e2.

3) Span of a set
For any subset S ⊆ V, the span of S,
    span(S) = {linear combinations of finitely many vectors from S},
is a subspace of V and is the smallest subspace containing S.

Proof sketch: span(S) is nonempty (contains 0 as the trivial combination). Sums and scalar multiples of linear combinations are again linear combinations, so span(S) is closed under addition and scalar multiplication. If U is any subspace containing S, then all linear combinations of elements of S lie in U, so span(S) ⊆ U.

4) Function and polynomial examples
- The set P_n of polynomials of degree at most n (with coefficients in F) is a subspace of the vector space of all polynomials: sums and scalar multiples of degree ≤ n polynomials again have degree ≤ n. P_n = span{1, x, x^2, ..., x^n}.
- The set C(R) of continuous real-valued functions on R is a subspace of the vector space of all real-valued functions on R. Sums and scalar multiples of continuous functions are continuous.
- The set of solutions to a homogeneous linear differential equation (e.g. y'' + y = 0) is a subspace of the space of sufficiently differentiable functions because differential operators are linear.

Nonexamples (what to watch for)
- Any subset missing 0 cannot be a subspace. For example, {(x,y) ∈ R^2 : x > 0} is not a subspace.
- An affine set given by A x = b with b ≠ 0 is not a subspace (it is a translate of a subspace but does not contain 0 or is not closed under scalar multiplication).

Quick checklist to test a subset W ⊆ V
- Is 0 ∈ W? If no, W is not a subspace.
- If u, v ∈ W, is u+v always in W?
- If a ∈ F and u ∈ W, is a u always in W?

If the answers are yes, W is a subspace.

Finite-dimensional Subspaces (position 7)

Main facts and how to use them

1) Any subspace of a finite-dimensional space is finite-dimensional.
- Statement: If V is finite-dimensional and W ≤ V, then W is finite-dimensional (or W = {0}).
- Proof idea: Take a basis of V. Any linearly independent list in W is also linearly independent in V, so it cannot exceed dim V in length; therefore W has a finite basis.
- Use: When working inside a finite-dimensional V you may assume all subspaces have finite dimension and apply rank/dimension arguments.

2) Dimension inequality and equality condition.
- Statement: If W ≤ V (both finite-dimensional) then dim W ≤ dim V. Moreover, dim W = dim V ⇔ W = V.
- Reason: Any basis of W is a linearly independent list in V so its length ≤ dim V. If lengths equal, that list is a basis of V as well, so spans V, hence W = V.
- Use: To detect proper subspaces: if you produce dim W = dim V then you’ve shown W = V; if you produce a linearly independent list of length dim V inside V, it is a basis.

3) Extending linearly independent lists to bases.
- Statement: If V is finite-dimensional and v1,...,vk are linearly independent in V, then there exist vectors vk+1,...,vn in V so that v1,...,vn is a basis of V. In particular every linearly independent list can be extended to a basis.
- Proof idea: If the list does not already span V, add a vector from V not in its span and keep going; this process must stop by finiteness (length cannot exceed dim V).
- Use: To build bases containing a prescribed independent set (e.g., find a complement).

4) Reducing spanning lists to bases.
- Statement: If v1,...,vm span V, then some sublist of them is a basis of V (remove redundant vectors until you have a basis).
- Proof idea: Remove any vector that is a linear combination of preceding ones; continuing yields a linearly independent spanning sublist.
- Use: To find a basis inside a given generating set or to compute dimensions from spanning sets.

5) Dimension of sums and intersections (dimension formula).
- Statement: For subspaces U, W ≤ V (finite-dimensional),
  dim(U + W) = dim U + dim W − dim(U ∩ W).
- Proof idea: Choose a basis of U ∩ W, extend it to a basis of U and to a basis of W; combining the extra vectors gives a basis of U + W, count lengths.
- Use: Compute dimensions of sums, determine when the sum is direct, and compute dim(U + W) efficiently.

6) Direct sum characterization.
- Statement: U + W is a direct sum (U ⊕ W) ⇔ U ∩ W = {0} ⇔ dim(U + W) = dim U + dim W.
- Use: To check direct-sum decompositions by checking dimensions.

7) Complements and existence of complements.
- Statement: For any subspace W ≤ V with V finite-dimensional, there exists a subspace U ≤ V such that V = W ⊕ U. Equivalently, every subspace has a complementary subspace.
- Construction: Extend a basis of W to a basis of V; the span of the added vectors is a complement.
- Use: Splitting V into simpler pieces; building projections.

Quick applications/examples

A) Proving a set equals V. Suppose V has dimension n and you find n vectors in a subspace W that are linearly independent. By (2) they form a basis of V, so W = V.

B) Computing dim(U + W). Let dim U = 4, dim W = 3 and dim(U ∩ W) = 2. Then dim(U + W) = 4 + 3 − 2 = 5. In particular U + W is a proper subspace of V if dim V > 5.

C) Building complements. If W has basis {w1,w2} in a 6-dimensional V, extend to a basis {w1,w2,u1,...,u4}. Then span{u1,...,u4} is a 4-dim complement U with V = W ⊕ U.

D) Reducing a spanning list. If you have 7 vectors that span a 5-dimensional V, you can remove dependencies to obtain a basis of 5 vectors.

E) Testing direct sum quickly. If dim U = 3, dim W = 2 and dim(U + W) = 5, then U ∩ W = {0} and V = U ⊕ W (if U + W = V). If instead dim(U + W) = 4, then dim(U ∩ W)=1 and the sum is not direct.

Takeaway checklist (practical rules)
- Any independent list length ≤ dim V; any spanning list length ≥ dim V.
- Independent list of length = dim V ⇒ basis.
- Spanning list of length = dim V ⇒ basis.
- Extend independent lists to bases; reduce spanning lists to bases.
- Use dim(U + W) = dim U + dim W − dim(U ∩ W) to relate sums/intersections.
- Every subspace of a finite-dimensional space has a complement.

Linear independence (finite-dimensional)

- Definition. A list of vectors v1, v2, ..., vk in a vector space V is linearly independent if the only scalars a1, a2, ..., ak in the field F satisfying
  a1 v1 + a2 v2 + ... + ak vk = 0
  are a1 = a2 = ... = ak = 0. If there exist scalars, not all zero, giving the zero combination, the list is linearly dependent.

- Equivalent descriptions (useful tests)
  - No vector in the list can be written as a linear combination of the others.
  - The representation of the zero vector by the list is unique (only the trivial combination).
  - If you view the list as columns of a matrix (after choosing coordinates when V is F^n or after choosing a basis for V), the list is linearly independent iff the column vectors are linearly independent iff the matrix has column rank = number of columns.

- How to verify linear independence in practice
  1. Set up the linear equation a1 v1 + ... + ak vk = 0 and solve for the scalars ai. If the only solution is all ai = 0, the list is independent.
  2. In coordinates: form a matrix whose columns are the coordinate vectors of v1,...,vk. Row-reduce to echelon form. The list is independent iff there is a pivot in every column (equivalently, the rank equals k).
  3. For an abstract V with a known basis, first express v1,...,vk in that basis and apply (2).

Bases (finite-dimensional)

- Definition. A list of vectors v1, v2, ..., vn is a basis of V if
  1) it is linearly independent, and
  2) it spans V (every vector in V is a linear combination of v1,...,vn).
  Equivalently: every vector of V has a unique representation as a linear combination of the basis vectors.

- Key finite-dimensional facts (useful shortcuts)
  - If V has dimension n, then any list of n vectors that is linearly independent is automatically a basis.
  - If V has dimension n, then any list of n vectors that spans V is automatically a basis.
  - Any linearly independent list can be extended to a basis; any spanning list can be reduced to a basis by deleting dependent vectors.

- How to verify a basis in practice
  1. Check linear independence (use the methods above).
  2. Check spanning: show that an arbitrary vector w in V can be written as a combination of the list. In coordinates, form a matrix whose columns are the list; the list spans V iff the column space equals V (equivalently, the matrix has rank = dim V).
  3. If you already know dim V = n and your list has length n, you need only check one of the two properties (independence or spanning) — the other follows automatically.

Examples of algorithmic checks
- For vectors in F^n: put vectors as columns in an n×k matrix A.
  - Linear independence ⇔ rank(A) = k.
  - Spanning F^n ⇔ rank(A) = n.
  - Basis of F^n ⇔ k = n and rank(A) = n.
- For vectors in an abstract V with a chosen basis: convert to coordinates and apply the same row-reduction/rank tests.

Remember: basis gives unique coordinates; linear independence prevents redundancy; spanning ensures completeness. These two together characterize bases in finite-dimensional spaces.

Section 9 — Quotient Spaces

- Definition. Let V be a vector space and U a subspace of V. For v in V the coset of v modulo U is
  v + U := { v + u : u ∈ U }.
  The set of all such cosets is denoted V/U and is called the quotient space of V by U.

- Cosets and equivalence. Cosets partition V: v and w lie in the same coset iff v − w ∈ U. Equivalently, v ~ w ⇔ v − w ∈ U is an equivalence relation on V, and V/U is the set of equivalence classes.

- Vector space structure. V/U becomes a vector space with addition and scalar multiplication defined by
  (v + U) + (w + U) := (v + w) + U,
  α·(v + U) := (αv) + U.
  These operations are well defined (independent of the chosen representatives). The zero vector is the coset U = 0 + U, and the additive inverse of v + U is (−v) + U.

- Canonical projection. The map π: V → V/U given by π(v) = v + U is a linear surjection with kernel ker π = U.

- Dimension relation (finite-dimensional case). If V is finite-dimensional and U is a subspace, then V/U is finite-dimensional and
  dim(V/U) = dim V − dim U.
  (This follows from extending a basis of U to a basis of V and taking the images of the extra basis vectors in V/U.)

Span and linear combinations
- Given a vector space V over a field F and a subset S = {v1, v2, …, vk} ⊆ V, a linear combination of vectors from S is any vector of the form a1v1 + a2v2 + … + akvk with scalars a1,…,ak ∈ F.
- The span of S, denoted span(S), is the set of all such linear combinations. It is the smallest subspace of V that contains S.
- S is said to span V (or be a spanning set for V) if span(S) = V; that is, every vector in V can be written as a linear combination of vectors from S.

Representation relative to a chosen basis (coordinates)
- A basis B = {b1, b2, …, bn} of V is a linearly independent set that spans V. Because B spans V, every vector v ∈ V can be written as a linear combination of the basis vectors:
  v = x1 b1 + x2 b2 + … + xn bn
  for some scalars x1,…,xn ∈ F.
- The scalars (x1,…,xn) are the coordinates of v with respect to the basis B. We often write the coordinate vector of v relative to B as [v]_B = (x1, x2, …, xn) ∈ F^n.
- The coordinate map v ↦ [v]_B is a linear map from V to F^n. Because B is a basis, this map is a linear isomorphism (one-to-one and onto).

Uniqueness of representation
- Uniqueness holds exactly when the spanning set is linearly independent (i.e., when it is a basis). More precisely:
  - If B is a basis, then the representation v = x1 b1 + … + xn bn is unique: there is exactly one n-tuple (x1,…,xn) giving v. Proof idea: if two representations exist, subtract them to get a nontrivial linear dependence among the bi, contradicting linear independence.
  - If S spans V but is not linearly independent, representations need not be unique: a vector can have multiple distinct linear combinations of the elements of S producing it.

Useful consequences
- Because coordinate representation relative to a basis is unique, computations in V can be reduced to computations in F^n by working with coordinate vectors.
- Determining whether a set spans V and whether it is linearly independent decides whether it is a basis; only then do coordinate representations exist uniquely.

Sum and direct sum of subspaces

Definition — sum of subspaces.
Let V be a vector space and let U1,...,Um be subspaces of V. The sum U1 + ··· + Um is the set of all finite sums of vectors from the Ui:
U1 + ··· + Um = {u1 + ··· + um : ui ∈ Ui for each i}.
This is a subspace of V.

Definition — direct sum.
The sum U1 + ··· + Um is called a direct sum, written
U1 ⊕ ··· ⊕ Um,
if every vector in U1 + ··· + Um has a unique representation as u1 + ··· + um with ui ∈ Ui.

Equivalent criteria for a direct sum
- Uniqueness criterion (linear independence of the summands): U1 + ··· + Um is direct ⇔ whenever u1 + ··· + um = 0 with ui ∈ Ui, then u1 = ··· = um = 0. (Only the trivial combination gives 0.)

- Intersection criterion (two subspaces): For two subspaces U and W, U ⊕ W ⇔ U ∩ W = {0}. (If U ∩ W = {0} then every v ∈ U + W has a unique decomposition v = u + w.)

- Intersection criterion (general m): U1 ⊕ ··· ⊕ Um ⇔ for each j,
Uj ∩ (sum of the others) = {0}.
Equivalently, no nonzero vector of any Ui can be written as a sum of vectors from the remaining subspaces.

- Dimension criterion: For finite-dimensional subspaces,
dim(U1 + ··· + Um) = dim U1 + ··· + dim Um
if and only if the sum is direct. In the two-subspace case the dimension formula
dim(U + W) = dim U + dim W − dim(U ∩ W)
shows directly that U ⊕ W ⇔ dim(U + W) = dim U + dim W ⇔ dim(U ∩ W) = 0.

Remarks
- When the sum is direct one often writes V = U1 ⊕ ··· ⊕ Um to indicate V = U1 + ··· + Um and the sum is direct (every v ∈ V has a unique decomposition).
- The uniqueness condition is often the most practical test: check that a relation u1 + ··· + um = 0 forces all ui = 0.

Linear map (linear transformation)

Definition
A function T: V → W between vector spaces V and W over the same field F is a linear map (or linear transformation) if for all u, v in V and all scalars a in F,
1) additivity: T(u + v) = T(u) + T(v),
2) homogeneity (scalar multiplication): T(a v) = a T(v).

Equivalently, these two conditions can be combined: for all u, v in V and all scalars a, b in F,
T(a u + b v) = a T(u) + b T(v).

Basic consequences
- T(0) = 0: apply homogeneity with a = 0 or additivity with v = 0.
- T(−v) = −T(v): follows from homogeneity with a = −1.
- T of any finite linear combination is the corresponding linear combination of the images:
  T(∑_{i} a_i v_i) = ∑_{i} a_i T(v_i).

Examples
- Zero map: For any V, W define T(v) = 0 for all v in V. This is linear.
- Identity map: I: V → V with I(v) = v is linear.
- Matrix transformations: If V = F^n and W = F^m, any m×n matrix A defines T(x) = Ax, which is linear.
- Differentiation: For V = space of polynomials (or sufficiently smooth functions), D(f) = f' is linear because (f+g)' = f' + g' and (a f)' = a f'.
- Integration (with fixed limits): For suitable function spaces, the map I(f) = ∫_{a}^{b} f(t) dt is linear.
- Projection and coordinate maps: Given V = U ⊕ W, the projection onto U along W is linear.

Non-examples
- Translation: T(v) = v + w for some fixed nonzero w is not linear because T(0) ≠ 0.
- Squaring on R: S(x) = x^2 from R to R is not linear since S(x+y) ≠ S(x) + S(y) in general.
- Absolute value: A(x) = |x| is not linear (fails additivity and homogeneity for negative scalars).

Determining a linear map from its values on a spanning set/basis
- Spanning set: If S ⊆ V spans V and T: V → W is linear, then T is completely determined by the values {T(s): s ∈ S}. Reason: every v ∈ V can be written as a finite linear combination v = ∑ a_i s_i with s_i ∈ S, and linearity yields T(v) = ∑ a_i T(s_i). Thus specifying T on S (consistently) determines T on all of V.
- Existence and uniqueness from a basis: If B = {v_1,…,v_n} is a basis of V and w_1,…,w_n are arbitrary vectors in W, there exists exactly one linear map T: V → W such that T(v_i) = w_i for each i. Construction: every v ∈ V has a unique coordinate representation v = ∑ a_i v_i; define T(v) = ∑ a_i w_i. Linearity of T is immediate and uniqueness follows because any linear map agreeing on the basis must send coordinates to the same combination of the w_i.

Short proof of uniqueness/existence for a basis:
- Uniqueness: If T and S are linear and T(v_i) = S(v_i) for all basis vectors, then for any v = ∑ a_i v_i,
  T(v) = ∑ a_i T(v_i) = ∑ a_i S(v_i) = S(v).
- Existence: Define T on basis vectors by T(v_i) = w_i and extend linearly to all v via their coordinate sums. This extension is well-defined because representation is unique, and it satisfies the linearity axioms.

Use in practice
- To define a linear map from V to W it suffices to specify images of a basis of V.
- To check linearity of a candidate map, verify additivity and homogeneity (or the combined two-variable condition).
- To show two linear maps agree, it is enough to check they agree on a spanning set (in particular on a basis).

Matrix of a linear map (with respect to bases)

Let V and W be finite-dimensional vector spaces over a field F. Fix ordered bases
- B = (v1, ..., vn) for V,
- C = (w1, ..., wm) for W.

For a linear map T: V → W, each basis vector vj of V has an image T(vj) in W, and T(vj) can be written uniquely as a linear combination of the basis C:
T(vj) = a1j w1 + a2j w2 + ... + amj wm,  for j = 1,...,n.
Collect the scalars aij into an m × n matrix A = [aij], where the j-th column of A is the coordinate column of T(vj) relative to C:
column j = [T(vj)]_C = (a1j, a2j, ..., amj)^T.

A is called the matrix of T with respect to the bases B and C, and it is written A = M(T; C, B) (or sometimes [T]_{C←B}).

Coordinates and action on vectors
Every v ∈ V has coordinates relative to B: v = x1 v1 + ... + xn vn, so [v]_B = (x1, ..., xn)^T. Linearity gives
T(v) = x1 T(v1) + ... + xn T(vn).
Taking coordinates relative to C and using the column description of A yields the matrix equation
[T(v)]_C = A [v]_B.
Thus to compute T(v) one:
1. express v in coordinates relative to B,
2. multiply A by that coordinate column,
3. interpret the resulting column as coordinates relative to C to get T(v).

Composition corresponds to matrix multiplication
Suppose U, V, W have ordered bases D = (u1,...,up), B = (v1,...,vn), C = (w1,...,wm). Let S: U → V and T: V → W. Let
- B_S = M(S; B, D) be the n × p matrix of S (columns are [S(ui)]_B),
- A_T = M(T; C, B) be the m × n matrix of T (columns are [T(vj)]_C).

For the composition T ∘ S: U → W, evaluate (T ∘ S)(ui) = T(S(ui)). The coordinate column of S(ui) relative to B is column i of B_S; applying T to that vector yields a coordinate column equal to A_T times column i of B_S. Therefore the i-th column of the matrix of T ∘ S is A_T times the i-th column of B_S. Hence
M(T ∘ S; C, D) = A_T · B_S,
i.e. the matrix of the composition is the product of the matrices (with the same matching of bases). This matches the rule [T(S(u))]_C = A_T [S(u)]_B = A_T (B_S [u]_D) = (A_T B_S) [u]_D.

Remarks
- The matrix depends on the choice and order of bases B and C; different bases give different matrices, but they represent the same linear map via the relation [T(v)]_C = M(T; C, B)[v]_B.
- The columns of the matrix are exactly the coordinate vectors of the images of the domain basis vectors.

Null space (kernel)

Definition
Let V and W be vector spaces and T : V → W a linear map. The null space (or kernel) of T is
null T = { v ∈ V : T(v) = 0 }.
(It is the set of all vectors in V that T sends to the zero vector of W.)

null T is a subspace
Proof: We show null T is a subspace of V.
- Nonempty: T(0) = 0 by linearity, so 0 ∈ null T.
- Closed under addition: if u,v ∈ null T then T(u+v) = T(u)+T(v) = 0+0 = 0, so u+v ∈ null T.
- Closed under scalar multiplication: if v ∈ null T and α ∈ F then T(αv) = αT(v) = α·0 = 0, so αv ∈ null T.
Therefore null T is a subspace of V.

How to compute / describe null spaces (practical methods and examples)
- Finite-dimensional case given by a matrix: represent T by a matrix A relative to chosen bases. Then null T is the solution space of the homogeneous linear system A x = 0. Compute it by row-reduction and express the solution set in parametric/vector form (a span of basis vectors).
Example 1 (matrix in R^3 → R^2):
Let T: R^3 → R^2 with matrix A = [ [1,2,-1], [0,1,3] ]. Solve A x = 0:
x + 2y − z = 0
    y + 3z = 0  ⇒ y = −3z
Then x = −2y + z = −2(−3z) + z = 7z. So
null T = { z(7, −3, 1) : z ∈ R } = span{(7, −3, 1)}.
- Linear operators on function or polynomial spaces: solve the defining equation T(v)=0 by using the form of elements.
Example 2 (differentiation): Let T : P2 → P1 be differentiation, T(p) = p'. Then null T = { p ∈ P2 : p' = 0 } = { constant polynomials } = span{1}.
- Conceptual description: null T is the set of all inputs that produce the zero output; give a basis/parametrization after solving linear relations among coordinates.

Null space and injectivity
The null space exactly captures injectivity of T:
- If null T = {0} then T is injective.
Proof: Suppose null T = {0} and T(v) = T(w). Then T(v − w) = T(v) − T(w) = 0, so v − w ∈ null T. Hence v − w = 0 and v = w; thus T is injective.
- If T is injective then null T = {0}.
Proof: If v ∈ null T then T(v) = 0 = T(0). By injectivity v = 0. So the only element of null T is 0.
Therefore T is injective ⇔ null T = {0}.

Remarks
- The dimension of null T is the nullity of T (useful in the rank–nullity theorem).
- In practice, finding null T reduces to solving a homogeneous linear system (row reduction) or solving the equation T(v)=0 in the given function/polynomial form.

Range (Image)

Definition
- Let V and W be vector spaces and T: V → W a linear map. The range (also called the image) of T is
  range(T) = { T(v) : v ∈ V } ⊆ W.
  In words: the range is the set of all vectors in W that T actually outputs.

Proof that range(T) is a subspace of W
- Nonempty: T(0_V) = 0_W because T is linear, so 0_W ∈ range(T). Thus range(T) ≠ ∅.
- Closed under addition: take y1, y2 ∈ range(T). Then y1 = T(v1), y2 = T(v2) for some v1, v2 ∈ V. Because T is linear, y1 + y2 = T(v1) + T(v2) = T(v1 + v2) ∈ range(T).
- Closed under scalar multiplication: take y ∈ range(T) with y = T(v) and scalar α. Then αy = αT(v) = T(αv) ∈ range(T).
- Therefore range(T) is a subspace of W.

How to compute or describe the range (examples)
1) Matrix / coordinate example (finite-dimensional, standard bases)
   - If T: R^n → R^m is given by an m×n matrix A, then range(T) = { Ax : x ∈ R^n } is the column space of A, i.e. the span of A's columns. Concretely,
     range(T) = span{ column1(A), column2(A), ..., column_n(A) }.
   - To compute it: form the columns of A, perform column-reduction (or row-reduction while tracking pivot columns) to find a basis of the column space. The pivot columns (from A) give a basis for range(T).

   Example: A = [[1, 2, 1],
                 [0, 1, 1]] as a map T: R^3 → R^2.
   - The columns are v1 = (1,0), v2 = (2,1), v3 = (1,1). range(T) = span{v1, v2, v3}. Observe v3 = v1 + v2 − v1? More simply check linear dependence: v3 = v1 + (0,1) which is v1 plus something; by row/column reduction one finds a basis {v1, v2}, so range(T) is the 2-dimensional subspace of R^2 spanned by (1,0) and (2,1). Here range(T) = R^2, so T is onto.

2) Polynomial-to-polynomial example
   - Let V = P2 (polynomials degree ≤ 2) and T: P2 → P2 defined by T(p) = p'. Then range(T) = { all polynomials of degree ≤ 1 } = P1, because derivatives of degree ≤ 2 polynomials yield exactly degree ≤ 1 polynomials. So range(T) = span{1, x}.

3) Linear functional example
   - Let T: R^3 → R be T(x,y,z) = x + 2y − z. Then range(T) is all real numbers R (because for any real t, pick vector (t,0,0) scaled appropriately), so range(T) = R. Concretely, range(T) = span{1} = R.

Connection to surjectivity
- By definition, T is surjective (onto) iff for every w ∈ W there exists v ∈ V with T(v) = w. Equivalently,
  T is surjective ⇔ range(T) = W.
- Thus checking surjectivity reduces to checking whether the range equals the whole codomain. In finite-dimensional settings with matrices, T: R^n → R^m given by A is surjective iff the columns of A span R^m (equivalently the matrix has rank m, i.e. there is a pivot in every row).

Remarks
- The range is sometimes referred to as Im(T). Its dimension is the rank of T (rank(T) = dim range(T)). The Rank-Nullity Theorem relates rank(T) to nullity(T), but the essential point for surjectivity is rank(T) = dim(W).

Injective (one-to-one)
- Definition: A linear map T: V → W is injective if T(u) = T(v) implies u = v for all u,v ∈ V.
- Null-space criterion: T is injective ⇔ null T = {0}. Equivalently, T(x) = 0 has only the trivial solution x = 0.
- Solution interpretation: If T is injective, any equation T(x) = y has at most one solution (it cannot have two distinct solutions).

Surjective (onto)
- Definition: T: V → W is surjective if for every y ∈ W there exists x ∈ V with T(x) = y.
- Range criterion: T is surjective ⇔ range T = W. Equivalently, for every y ∈ W the equation T(x) = y has at least one solution.

Invertible (bijective with two-sided inverse)
- Definition: T: V → W is invertible if there exists a linear map S: W → V such that S∘T = I_V and T∘S = I_W. The map S is the inverse T^{-1}.
- Equivalences:
  - T is invertible ⇔ T is both injective and surjective (i.e., bijective).
  - T is invertible ⇔ null T = {0} and range T = W.
  - Existence of a left inverse (S with S∘T = I_V) implies T is injective; existence of a right inverse (R with T∘R = I_W) implies T is surjective. If both exist, they coincide and give the two-sided inverse.
- Solution interpretation: T is invertible ⇔ for every y ∈ W the equation T(x) = y has exactly one solution, namely x = T^{-1}(y).

Compact summary of relationships
- Injective ⇔ trivial null space.
- Surjective ⇔ range equals codomain.
- Invertible ⇔ bijective ⇔ both of the above hold; equivalently, T has a linear two-sided inverse; equivalently, every T(x)=y has a unique solution.

Section 17 — Rank–Nullity Theorem

Theorem (Rank–Nullity). Let V and W be vector spaces and T : V → W a linear map with V finite-dimensional. Then
dim V = dim ker T + dim range T.
Equivalently, nullity(T) + rank(T) = dim V.

Proof. Let K = ker T. If K = {0} then start with the empty basis; otherwise choose a basis {v1,...,vk} of K. Extend this basis of K to a basis of V: by finite-dimensionality there exist vectors vk+1,...,vn in V such that B = {v1,...,vk, vk+1,...,vn} is a basis of V.

Apply T to the last n−k basis vectors. We claim that {T(vk+1),...,T(vn)} is a basis of range T.

- Spanning: For any w in range T there exists v in V with T(v) = w. Write v in the basis B as v = a1v1 + ... + akvk + ak+1vk+1 + ... + anvn. Applying T gives
  w = T(v) = ak+1 T(vk+1) + ... + an T(vn),
  because T(v1)=...=T(vk)=0. Thus w is a linear combination of T(vk+1),...,T(vn), so these vectors span range T.

- Linear independence: Suppose c_{k+1} T(v_{k+1}) + ... + c_n T(v_n) = 0. Then T(c_{k+1} v_{k+1} + ... + c_n v_n) = 0, so the vector u = c_{k+1} v_{k+1} + ... + c_n v_n lies in ker T = span{v1,...,vk}. But B is a basis of V, so the representation of u relative to B is unique. Since u has no components in v1,...,vk, uniqueness forces u = 0, hence all c_{k+1},...,c_n = 0. Thus the set {T(vk+1),...,T(vn)} is linearly independent.

Therefore {T(vk+1),...,T(vn)} is a basis of range T, so
dim range T = n − k.
But k = dim ker T and n = dim V, so dim V = dim ker T + dim range T, as claimed. ∎

Corollaries and consequences

1. Nullity zero ⇔ injective:
   ker T = {0} ⇔ dim ker T = 0 ⇔ dim range T = dim V.
   In particular, dim ker T = 0 iff T is injective.

2. Rank equals codomain dimension ⇔ surjective:
   range T = W ⇔ dim range T = dim W.
   If dim range T = dim W then T is surjective; conversely surjectivity implies dim range T = dim W.

3. For maps between equal finite dimensions: If V and W are finite-dimensional with dim V = dim W, then for T : V → W
   T is injective ⇔ T is surjective.
   Proof: From rank–nullity dim V = dim ker T + dim range T. If T is injective then dim ker T = 0, so dim range T = dim V = dim W, hence range T = W and T is surjective. Conversely, if T is surjective then dim range T = dim W = dim V, so dim ker T = 0 and T is injective.

4. Endomorphisms on finite-dimensional spaces: For T : V → V with V finite-dimensional, injective, surjective, and bijective are all equivalent properties.

5. Inequalities and bounds:
   - rank(T) = dim range T ≤ dim W.
   - nullity(T) = dim ker T ≤ dim V.
   - If dim V > dim W then every linear map T : V → W has nontrivial kernel (pigeonhole principle): nullity(T) ≥ dim V − dim W > 0, so no map from a larger to a smaller finite-dimensional space can be injective.

These consequences allow quick dimension-based reasoning about solvability, invertibility, and the structure of linear maps between finite-dimensional spaces.

Vector space of polynomials

Definition
- Let F be a field. Denote by P(F) the set of all polynomials with coefficients in F:
  p(x) = a_0 + a_1 x + a_2 x^2 + ... + a_n x^n, with a_i in F and n ≥ 0.
  With usual polynomial addition and scalar multiplication from F, P(F) is a vector space over F.
- For a nonnegative integer n, denote by P_n(F) the subspace of P(F) consisting of all polynomials of degree at most n:
  P_n(F) = { p in P(F) : deg p ≤ n }.

Degree conventions (useful for vector-space reasoning)
- For a nonzero polynomial p, deg p is the largest exponent with a nonzero coefficient.
- Convention: deg 0 = −∞ (or declare deg 0 < k for every integer k). This convention makes the following inequalities valid uniformly:
  deg(p + q) ≤ max(deg p, deg q) and deg(α p) = deg p for α ≠ 0.
  It also avoids special cases when reasoning about spans and dependence.

Vector-space structure and basic consequences
- Addition and scalar multiplication are the usual coefficient-wise operations:
  (p+q)(x) = p(x) + q(x); (α p)(x) = α · p(x).
  These operations preserve degrees according to the degree rules above.
- P(F) is infinite-dimensional: for each n, the finite set {1, x, x^2, ..., x^n} lies in P(F) and can be extended arbitrarily, so no finite basis spans all of P(F).
- Each P_n(F) is finite-dimensional with dimension n+1. A standard basis is {1, x, x^2, ..., x^n}.

Spans, linear independence, and bases in polynomial spaces
- Spanning P_n(F):
  The set {1, x, x^2, ..., x^n} spans P_n(F) because any p in P_n(F) can be written uniquely as a_0 + a_1 x + ... + a_n x^n.
- Linear independence of monomials:
  The monomials 1, x, x^2, ..., x^n are linearly independent. Proof sketch: if c_0 + c_1 x + ... + c_n x^n = 0 polynomial (all coefficients zero), then each c_i = 0; hence no nontrivial linear combination is zero.
- Dimension:
  Because {1, x, ..., x^n} is a linearly independent spanning set of P_n(F), dim P_n(F) = n+1.
- Consequence (size and dependence):
  Any set of more than n+1 polynomials in P_n(F) is linearly dependent (dimension bound). Conversely, any linearly independent set in P_n(F) has at most n+1 elements.
- Uniqueness of coordinates:
  Given the basis {1, x, ..., x^n}, each p in P_n(F) has a unique coordinate vector (a_0, a_1, ..., a_n) in F^{n+1}. The linear map p ↦ (a_0, ..., a_n) is an isomorphism P_n(F) ≅ F^{n+1}.

Using vector-space operations to reason about polynomial questions
- Testing whether a polynomial q lies in span{p_1, ..., p_k}:
  Form the linear combination α_1 p_1 + ... + α_k p_k and equate coefficients with q. This yields a linear system for α_i; solvability determines membership.
- Checking linear independence:
  To test if {p_1, ..., p_k} is independent, solve α_1 p_1 + ... + α_k p_k = 0. Equating coefficients produces a homogeneous linear system; only trivial solution implies independence.
- Degree arguments for dependence:
  If p_1, ..., p_m are nonzero polynomials with strictly increasing degrees and m > n+1 in P_n(F) then they cannot all lie in P_n(F). More usefully, if you have more than n+1 polynomials of degree ≤ n, they are dependent because their coordinate vectors in basis {1,...,x^n} form more than n+1 vectors in F^{n+1}.
- Constructing a basis from a spanning set:
  Use Gaussian-elimination-style operations on coefficient matrices (or remove polynomials that are linear combinations of earlier ones) to extract a basis from any spanning set of P_n(F).
- Evaluation maps are linear:
  For a fixed a in F, the map Ev_a : P(F) → F defined by Ev_a(p) = p(a) is linear. Kernels of evaluation maps are subspaces (e.g., all polynomials with root at a). For P_n(F), the kernel of Ev_a has codimension 1 when n ≥ 0 (unless restricting to the zero space).

Examples and common arguments
- Example (expressing as span): To show x^3 + 2x + 1 is in span{1, x, x^2, x^3}, write it directly as 1·1 + 2·x + 0·x^2 + 1·x^3.
- Example (dependence by dimension): Any four polynomials of degree ≤ 2 are linearly dependent because dim P_2(F) = 3.
- Example (independence using evaluation): The polynomials 1, x−a, (x−a)^2, ..., (x−a)^n are a basis of P_n(F) (they are independent because the matrix relating them to 1,x,...,x^n is invertible; equivalently binomial expansion gives a triangular change-of-basis with nonzero diagonal).
- Example (uniqueness of zero polynomial): If a polynomial of degree ≤ n has n+1 distinct roots in F, it must be the zero polynomial. Reason: a nonzero polynomial of degree ≤ n has at most n roots; therefore a polynomial with n+1 roots is zero, hence all coefficients zero. Vector-space viewpoint: evaluation at those n+1 points gives a linear map P_n(F) → F^{n+1}; if the image of a polynomial is the zero vector but the evaluation map is injective, the polynomial must be zero (injectivity follows because a nonzero polynomial of degree ≤ n cannot vanish at all n+1 distinct points).

Key takeaways
- P(F) is a vector space; P_n(F) is the (n+1)-dimensional subspace of polynomials of degree ≤ n.
- The standard monomials {1, x, ..., x^n} form a basis for P_n(F); dimension arguments about spans and independence reduce to coefficient linear algebra in that basis.
- Degree conventions (especially deg 0 = −∞) streamline many inequalities and proofs involving sums and scalar multiples.

Evaluation maps and interpolation

Definitions and basic facts
- Let F be a field and let P denote the vector space of all polynomials with coefficients in F. For each a in F define the evaluation map ev_a : P → F by ev_a(p) = p(a). Each ev_a is a linear functional on P (i.e., an element of the dual space P*), because for p,q in P and scalars α,β we have ev_a(αp+βq) = αp(a)+βq(a).

- For any n ≥ 0 write P_n for the subspace of polynomials of degree at most n. Then ev_a restricts to a linear functional on P_n.

Interpolation via a linear map to coordinate space
- Fix distinct points a_0, a_1, …, a_n in F. Define the linear map
  T : P_n → F^{n+1},     T(p) = (p(a_0), p(a_1), …, p(a_n)).
  T is linear because each coordinate is the linear functional ev_{a_j}.

Existence and uniqueness of interpolating polynomials
- Theorem (Existence and uniqueness). For any list of values b_0, b_1, …, b_n in F there exists exactly one polynomial p in P_n such that p(a_j) = b_j for j = 0,…,n.

  Proof. dim P_n = n+1 and dim F^{n+1} = n+1. It suffices to show T is injective (then it is bijective and every right-hand side (b_0,…,b_n) has a unique preimage). Suppose p ∈ P_n satisfies T(p) = 0, i.e. p(a_j) = 0 for j = 0,…,n. Then p has n+1 distinct roots but deg p ≤ n, so p must be the zero polynomial. Hence ker T = {0}, so T is injective and therefore bijective. This proves existence and uniqueness.

Lagrange basis and explicit construction
- As a consequence of bijectivity, the coordinate vectors e_0 = (1,0,…,0), …, e_n = (0,…,0,1) in F^{n+1} have unique preimages l_0, …, l_n in P_n with T(l_j) = e_j. Thus l_j(a_k) = δ_{jk}. The polynomials l_j form a basis of P_n (the Lagrange basis), and the interpolating polynomial for values b_0,…,b_n is
  p = b_0 l_0 + b_1 l_1 + … + b_n l_n.
  One convenient explicit formula for l_j is
  l_j(x) = ∏_{k ≠ j} (x − a_k) / ∏_{k ≠ j} (a_j − a_k),
  which clearly satisfies l_j(a_k) = δ_{jk}.

Linear-independence statement for evaluation functionals
- Corollary. The evaluation functionals ev_{a_0}, ev_{a_1}, …, ev_{a_n} (restricted to P_n) are linearly independent elements of the dual space P_n*.

  Proof. If c_0 ev_{a_0} + … + c_n ev_{a_n} = 0 as a functional, then for every p ∈ P_n we have c_0 p(a_0) + … + c_n p(a_n) = 0. Evaluate this identity on the Lagrange basis polynomials l_j: doing so gives c_j = 0 for each j. Hence the functionals are independent.

Remarks
- The linear-algebra proof emphasizes dimension and kernel arguments rather than formula manipulation. It gives both existence/uniqueness and a constructive method (via inverses or the Lagrange basis) to produce the interpolating polynomial.
- The argument fails if two of the nodes a_j coincide (evaluation functionals are then linearly dependent), or if one seeks interpolation with degree strictly less than n when n+1 values are prescribed.

Section 20 — Polynomial Division Algorithm and Useful Algebraic Identities

Statement of the Division Algorithm
- Let F be a field and let f, g be polynomials in F[x] with g ≠ 0. Then there exist unique polynomials q, r in F[x] such that
  f(x) = q(x) g(x) + r(x),
  with either r = 0 or deg r < deg g.
- Existence: perform the usual long division (or synthetic division when g is linear) by repeatedly canceling the leading term of the current dividend using the leading term of g; the process terminates because degrees strictly decrease.
- Uniqueness: if f = q1 g + r1 = q2 g + r2 with deg r1, deg r2 < deg g, subtract to get (q1 − q2)g = r2 − r1. If q1 ≠ q2 then deg((q1 − q2)g) ≥ deg g > deg(r2 − r1), contradiction. Thus q1 = q2 and r1 = r2.

Immediate consequences and useful facts
- Degree inequalities: deg f = deg q + deg g when r = 0 and q ≠ 0; otherwise deg f ≥ deg q + deg g.
- Remainder is zero iff g divides f in F[x].
- Remainder Theorem: If g(x) = x − a (a in F), then the remainder r is the constant f(a). So f(x) = q(x)(x − a) + f(a). Immediate corollary:
  - Factor Theorem: x − a divides f iff f(a) = 0. Thus linear factors correspond exactly to roots in F.
- Repeated (higher-multiplicity) factors: x − a is a factor of multiplicity m of f iff f(a) = f′(a) = … = f^(m−1)(a) = 0 but f^(m)(a) ≠ 0.

Algebraic identities used frequently
- Difference of powers:
  x^n − y^n = (x − y)(x^{n−1} + x^{n−2}y + … + xy^{n−2} + y^{n−1}).
  In particular, taking y = 1 gives x^n − 1 = (x − 1)(x^{n−1} + x^{n−2} + … + 1).
- Sum of powers (for odd n):
  x^n + y^n = (x + y)(x^{n−1} − x^{n−2}y + … − xy^{n−2} + y^{n−1}) when n is odd.
- Difference of squares:
  x^2 − y^2 = (x − y)(x + y).
- Cyclotomic-style factorization (useful when working over fields containing roots of unity): x^{n} − 1 factors as a product of cyclotomic polynomials; more concretely, for any divisor d of n, x^d − 1 divides x^n − 1.
- Binomial factorization identity (useful for manipulating shifted polynomials):
  For integer n ≥ 1, (x + a)^n − a^n = (sum_{k=1}^n binom(n,k) a^{n−k} x^k) — shows (x) divides that expression, and powers of x divide successive derivatives.

How to use the division algorithm in practice
- Reducing degree: To analyze f relative to g, compute q and r. Questions about values, roots, or divisibility often reduce to studying the smaller-degree r.
- Constructing minimal polynomials: If v is a vector (or element) and p ∈ F[x] satisfies p(v) = 0, then the monic polynomial of least degree that annihilates v (the minimal polynomial) divides every polynomial that annihilates v. This follows by dividing any annihilating polynomial by the minimal polynomial and using uniqueness of the remainder: the remainder must be zero because it would be a smaller-degree annihilator otherwise.
- Proving irreducibility or factor structure: Using the division algorithm and identities like x^n − 1 factorization, one can show certain factors must appear or cannot appear in a polynomial factorization over F. For example, if f(a) = 0 then (x − a) is a factor; if f(ω) = 0 for a primitive n-th root of unity ω, then minimal polynomials of roots of unity divide f.

Examples (short, illustrative)
1) Remainder when dividing by x − a:
   Using the division algorithm, f(x) = q(x)(x − a) + r, deg r < 1 so r is constant. Evaluating at x = a yields r = f(a). Therefore remainder = f(a).

2) Using x^n − 1 factorization:
   Suppose f(x) ∈ F[x] and f(1) = f′(1) = … = f^{(m−1)}(1) = 0. Then (x − 1)^m divides f(x). Proof sketch: Write f as f(x) = (x − 1) g1(x) + r1 with deg r1 < 1; r1 = f(1) = 0 so x − 1 divides f. Repeat with derivatives or use Taylor expansion in F[x] to get higher powers.

3) Minimal polynomial divisibility:
   Let T be a linear operator on a finite-dimensional vector space over F and let m_T be its minimal polynomial. If p(T) = 0, divide p by m_T: p = q m_T + r with deg r < deg m_T. Then r(T) = p(T) − q(T)m_T = 0, so r is an annihilating polynomial of smaller degree. By minimality r = 0, hence m_T divides p.

Notes on computation
- Synthetic division: For linear divisors x − a, use synthetic division to quickly get q and f(a) as remainder.
- When dividing by higher-degree g, perform polynomial long division, tracking leading coefficients. Over a field, inversion of leading coefficient is allowed and required in the step that cancels the current highest-degree term.

Applications toward later factorization and minimal-polynomial arguments
- To show a polynomial p factors in a particular way, show that potential linear (or irreducible) factors are forced by evaluation or by algebraic identities, then repeatedly divide to remove those factors.
- To prove minimality or uniqueness of a minimal polynomial, use division to reduce any candidate polynomial to a remainder of smaller degree; minimality forces that remainder to be zero, giving divisibility.
- To deduce multiplicity of roots or to lift a root to a higher power factor (e.g., showing (x − a)^k divides f), use repeated division or derivative tests as in the example above.

Summary of the toolbox you should keep in mind
- Division algorithm (existence + uniqueness).
- Remainder and Factor Theorems.
- Difference/sum of powers identities.
- Repeated-division and derivative tests for multiplicity.
- Division-based argument that minimal polynomials divide any annihilating polynomial.

This section gives the core algebraic apparatus used repeatedly to manipulate polynomials, remove factors, and set up arguments about divisibility and minimal polynomials. Use the division algorithm first to reduce problems to smaller-degree remainders, then apply the identities above to recognize or force particular factors.

Polynomials Applied to Linear Operators

Definition
- Let V be a vector space over a field F and T ∈ L(V). For a polynomial p(z) = a0 + a1 z + ··· + an z^n ∈ F[z] define the operator p(T) ∈ L(V) by
  p(T) = a0 I + a1 T + ··· + an T^n,
  where I is the identity on V and T^k means T composed with itself k times (T^0 = I).
- This is called evaluating the polynomial p at the operator T.

Basic algebraic properties
- Linearity in the polynomial:
  (p + q)(T) = p(T) + q(T), and (αp)(T) = α p(T) for α ∈ F.
- Multiplicativity:
  (p q)(T) = p(T) q(T).
  Proof sketch: expand pq as a sum of monomials and use distributivity; monomial zk corresponds to T^k and composition of monomials corresponds to product of powers of T.
- Compatibility with powers and constants:
  1(T) = I, z(T) = T, and z^k(T) = T^k.
- Commutation with T:
  For every polynomial p, p(T) commutes with T (because each T^k commutes with T), and hence all polynomials in T pairwise commute: p(T) q(T) = q(T) p(T).

Action on eigenvectors
- If v ≠ 0 is an eigenvector of T with eigenvalue λ (T v = λ v), then for any polynomial p,
  p(T) v = p(λ) v.
  In particular, if p(λ) = 0 then p(T) v = 0.
- Consequence: knowledge of p(λ) gives immediate information about p(T) on the eigenspace corresponding to λ.

Annihilating polynomials
- A polynomial p ∈ F[z] is called an annihilating polynomial for T if p(T) = 0 (the zero operator).
- If p is an annihilating polynomial and p = r s (factorization in F[z]), then r(T) s(T) = 0. This yields algebraic relations between factors evaluated at T.
- If v is any eigenvector with eigenvalue λ and p is annihilating, then p(λ) = 0. Thus the eigenvalues of T must be roots of every annihilating polynomial.
- In finite-dimensional V there always exist nonzero annihilating polynomials (for example the characteristic polynomial; this is the Cayley–Hamilton statement, proved later). The existence implies the set {I, T, T^2, ...} is linearly dependent.

Elementary consequences and uses
- If p(T) = q(T) then (p − q)(T) = 0, so p − q is an annihilating polynomial. Thus polynomials that differ by an annihilating polynomial give the same operator when evaluated at T.
- If p(T) is invertible, then 0 is not a root of p when restricted to T’s spectrum (more precisely, p(λ) ≠ 0 for every eigenvalue λ), because otherwise p(T) would kill the corresponding eigenvector.
- Factorization insight: if p(T) = 0 and p factors into distinct linear factors (over the field), then T satisfies a product of commuting operators equal to zero; this is a stepping stone toward decompositions of V into T-invariant subspaces.

Summary (what this gives us for eigenvalue study)
- Defining p(T) allows us to translate polynomial algebra into operator algebra.
- Evaluating polynomials at T preserves sums, scalar multiples, and products, and maps roots of polynomials to annihilation of corresponding eigenspaces.
- Annihilating polynomials connect algebraic factorization of polynomials to invariant subspaces and eigenvalues; they are the bridge to minimal polynomials, the characteristic polynomial, and structural results about T.

Roots, Multiplicity, and Factorization

Definitions and basic connection
- Root (zero): For a polynomial p ∈ F[x], a ∈ F is a root of p if p(a) = 0.
- Linear factor: x − a is called a linear factor corresponding to the root a.
- Factor Theorem (basic form): a ∈ F is a root of p if and only if x − a divides p. Equivalently, p(x) = (x − a)q(x) for some q ∈ F[x].

Proof idea: Use polynomial long division (or the division algorithm). Evaluating p at x = a gives p(a) = (a − a)q(a) + r = r, so p(a) = 0 iff the remainder r = 0, i.e. x − a divides p.

Multiplicity
- Multiplicity (order) of a root a: The multiplicity m ≥ 1 of a as a root of p is the largest integer m such that (x − a)^m divides p. In other words, p(x) = (x − a)^m r(x) with r(a) ≠ 0.
- A root of multiplicity 1 is called a simple root; multiplicity ≥ 2 is a repeated root.

Equivalent characterizations:
- p(a) = p′(a) = ··· = p^{(m−1)}(a) = 0 but p^{(m)}(a) ≠ 0 (when char(F) = 0 or when derivatives make sense in the field).
- The exponent of (x − a) in the complete factorization of p gives the multiplicity.

Consequences about number of roots
- Nonzero polynomial of degree n has at most n roots in F (counted without multiplicity).
Proof sketch: If a1, …, ak are distinct roots, then (x − a1) ··· (x − ak) divides p. That product has degree k, so k ≤ deg p.
- If you count multiplicities, the sum of multiplicities of all roots (in any extension field where p splits) equals deg p.
- If a polynomial of degree n has more than n distinct points where it evaluates to the same value as another polynomial of degree ≤ n, then the polynomials are equal. In particular, if two polynomials of degree ≤ n agree at n + 1 distinct points, they are identical.

Factorization structure
- Complete factorization over F (when possible): If p ∈ F[x] has roots a1, …, ak in F with multiplicities m1, …, mk and leading coefficient c ≠ 0, then
  p(x) = c · ∏_{j=1}^k (x − a_j)^{m_j} · s(x),
where s(x) is a polynomial with no roots in F (s may be 1 if p splits completely in F).
- Over an algebraically closed field (e.g., C), every nonzero polynomial of degree n factors as
  p(x) = c · ∏_{j=1}^n (x − b_j),
where the b_j are the roots counted with multiplicity.

Uses and applications
- Control of roots: The degree of a polynomial bounds how many zeros it can have. This is a key tool for proving uniqueness statements and for solving problems where a polynomial is shown to vanish at many points.
- Detecting the zero polynomial: If a polynomial vanishes on infinitely many elements of F, then it must be the zero polynomial (this follows because a nonzero polynomial has finitely many roots).
- Manipulating multiplicities: If p has a root a of multiplicity m, then small perturbations of coefficients can reduce multiplicity but cannot create more total multiplicity than the degree permits.
- Comparing polynomials: If p − q has degree ≤ n and has n + 1 distinct zeros, then p − q is the zero polynomial, so p = q.

Examples
- p(x) = (x − 2)^3(x + 1) has root 2 with multiplicity 3 and root −1 with multiplicity 1; deg p = 4 and there are at most 4 roots counted with multiplicity (here exactly 4).
- q(x) = x^2 + 1 over R has no real roots, so it cannot be written as a product of real linear factors; over C it factors as (x + i)(x − i).

Key points to remember
- Roots correspond exactly to linear factors.
- Multiplicity is the exponent of a linear factor in the factorization.
- Degree bounds the total number of roots (distinct ≤ degree; with multiplicity sum = degree when fully split).
- These facts let you deduce uniqueness and vanishing results that are widely used in polynomial arguments.

Characteristic polynomial

Let V be an n-dimensional vector space and T: V → V a linear operator. Choose any ordered basis of V and let A be the matrix of T with respect to that basis. The characteristic polynomial of T (or of A) is the polynomial
p_T(λ) = det(λI − A).
Equivalently, when one works abstractly without a matrix, write p_T(λ) = det(λI_V − T). This is a polynomial of degree n whose leading coefficient is 1 (monic).

Algebraic multiplicity

If λ0 is a root of p_T(λ), its algebraic multiplicity is the multiplicity of λ0 as a root of p_T. Concretely, if p_T(λ) factors (over the field) as
p_T(λ) = (λ − λ0)^m q(λ)
with q(λ0) ≠ 0, then the algebraic multiplicity of λ0 is m.

Connection between roots of the characteristic polynomial and eigenvalues

A scalar λ0 is an eigenvalue of T if and only if p_T(λ0) = 0. Proof sketch: λ0 is an eigenvalue ⇔ λ0I − T is not invertible ⇔ det(λ0I − T) = 0 ⇔ p_T(λ0) = 0. Thus the eigenvalues of T are exactly the roots of its characteristic polynomial; each eigenvalue appears among the roots with algebraic multiplicity equal to its multiplicity as a root of p_T.

(For later use: if V is n-dimensional, p_T has degree n, so the sum of algebraic multiplicities of all eigenvalues counted with multiplicity equals n.)

Diagonalization and Eigenbasis Criteria

Definition and equivalence
- An operator T on a finite-dimensional vector space V (or an n×n matrix) is diagonalizable if there exists a basis of V consisting entirely of eigenvectors of T. Equivalently, T is similar to a diagonal matrix: there exists an invertible P and a diagonal D with T = PDP⁻¹, where the diagonal entries of D are eigenvalues of T (with repetition according to how many basis eigenvectors have that eigenvalue).

Criteria for diagonalizability
1. Existence of n independent eigenvectors
   - T is diagonalizable ⇐⇒ V has a basis of n linearly independent eigenvectors of T.
   - In particular, if the eigenvectors corresponding to all eigenvalues span V, T is diagonalizable.

2. Geometric vs algebraic multiplicity
   - For each eigenvalue λ, let g(λ) = dim eigenspace E(λ) (geometric multiplicity) and a(λ) = multiplicity of λ as a root of the characteristic polynomial (algebraic multiplicity).
   - Necessary and sufficient condition: T is diagonalizable ⇐⇒ for every eigenvalue λ, g(λ) = a(λ).
   - In words: each eigenspace has dimension equal to the eigenvalue’s algebraic multiplicity, so the eigenspaces together give a direct-sum decomposition of V.

3. Distinct eigenvalues
   - If T has n distinct eigenvalues (so the characteristic polynomial has n distinct roots), then T is diagonalizable. (Distinct eigenvalues guarantee eigenvectors are linearly independent.)

4. Minimal polynomial condition
   - T is diagonalizable ⇐⇒ the minimal polynomial of T has no repeated factors (i.e., is a product of distinct linear factors).
   - Equivalently: the minimal polynomial is square-free.

5. Direct-sum of eigenspaces
   - T is diagonalizable ⇐⇒ V = ⊕_{λ} E(λ). That is, the sum of eigenspaces is direct and equals the whole space.

Using these criteria
- To check diagonalizability in practice:
  1. Find eigenvalues by solving det(T−λI)=0.
  2. For each eigenvalue λ, compute a(λ) from the characteristic polynomial and g(λ) = dim ker(T−λI).
  3. If g(λ)=a(λ) for every λ, T is diagonalizable. If any g(λ)<a(λ), T is not diagonalizable.
  4. If you find n distinct eigenvalues, you can stop — T is diagonalizable.

How diagonalization simplifies powers and polynomials
- Suppose T = PDP⁻¹ with D = diag(λ1,...,λn). Then:
  - Powers: T^k = P D^k P⁻¹, and D^k = diag(λ1^k,...,λn^k). Thus computing T^k reduces to taking powers of the diagonal entries.
  - Polynomials: For any polynomial p(z), p(T) = P p(D) P⁻¹, and p(D) = diag(p(λ1),...,p(λn)). So p(T) acts like applying p to each eigenvalue on the corresponding eigenvector.
  - In particular, if v is an eigenvector with Tv = λv, then p(T)v = p(λ)v.

Projection (spectral) decomposition
- If T is diagonalizable with distinct eigenvalues λ1,...,λm and corresponding eigenspace projections P1,...,Pm (summing to I and PiPj = 0 for i≠j), then
  - T = λ1 P1 + λ2 P2 + ... + λm Pm,
  - and for any polynomial p, p(T) = p(λ1) P1 + ... + p(λm) Pm.
- This form makes functional calculus immediate: powers, exponentials (via series), and other polynomials of T are linear combinations of the projections with coefficients p(λj).

Examples of use
- Compute T^100 quickly: diagonalize T = PDP⁻¹, then T^100 = P diag(λ1^100,...,λn^100) P⁻¹.
- Solve recurrence/polynomial equations in T: if p(T)=0 and T is diagonalizable, then p(λ)=0 for every eigenvalue λ; conversely, knowledge of p on eigenvalues determines p(T).

Takeaway
- Diagonalizability is equivalent to having a full eigenbasis or, algebraically, to matching geometric and algebraic multiplicities (or a square-free minimal polynomial). Once diagonalized, manipulating powers and polynomials of an operator reduces to simple scalar computations on the eigenvalues.

Eigenspace and geometric multiplicity

Definition. Let V be a vector space over a field F and T: V → V a linear operator. For an eigenvalue λ of T, the eigenspace corresponding to λ is
E(λ) = {v in V : T(v) = λ v}.
Equivalently, E(λ) = {v in V : (T − λ I)(v) = 0}.

Eigenspace as a subspace. Because E(λ) = ker(T − λ I), it is a subspace of V. Explicitly:
- 0 ∈ E(λ) since T(0) = 0 = λ·0.
- If v, w ∈ E(λ), then T(v + w) = T(v) + T(w) = λ v + λ w = λ (v + w), so v + w ∈ E(λ).
- If v ∈ E(λ) and α ∈ F, then T(α v) = α T(v) = α λ v = λ (α v), so α v ∈ E(λ).
Thus E(λ) is closed under addition and scalar multiplication and contains 0, hence is a subspace; this is exactly the null space of the linear map T − λ I.

Geometric multiplicity. The geometric multiplicity of the eigenvalue λ is defined to be the dimension of its eigenspace:
geom mult(λ) := dim E(λ) = dim ker(T − λ I).
Remarks: since λ is an eigenvalue, E(λ) contains a nonzero vector, so geom mult(λ) ≥ 1. The geometric multiplicity measures how many linearly independent eigenvectors correspond to λ (i.e., the maximum size of a linearly independent set of eigenvectors for λ).

Definition
- Let V be a vector space over a field F and T: V → V a linear operator. A scalar λ in F is an eigenvalue of T if there exists a nonzero vector v in V such that T(v) = λv. Any nonzero v with T(v) = λv is called an eigenvector of T corresponding to λ.
- Equivalently, λ is an eigenvalue iff the operator (T − λI) is not injective (has nontrivial kernel), i.e. ker(T − λI) ≠ {0}. The eigenspace for λ is E_λ = {v ∈ V : T(v) = λv} = ker(T − λI).

The eigenvalue equation
- The equation T v = λ v is the defining relation. It says that v is stretched (or flipped, scaled, or left unchanged) by T by the scalar factor λ, and the direction of v is preserved (v and T v are collinear).
- To find eigenvalues/eigenvectors one typically rewrites this as (T − λI)v = 0. Nonzero solutions v exist exactly when the linear map (T − λI) is singular, which (for finite-dimensional V represented by an n×n matrix A with respect to some basis) is equivalent to det(A − λI) = 0. The polynomial p(λ) = det(A − λI) is the characteristic polynomial; its roots are the eigenvalues. For each eigenvalue λ, the eigenvectors are the nonzero vectors in the nullspace of A − λI.

Concrete examples

1) Simple diagonal/triangular matrix
- Let A = [[2, 1], [0, 3]] acting on R^2. Compute A − λI = [[2 − λ, 1], [0, 3 − λ]]. The determinant is (2 − λ)(3 − λ) − 0 = (2 − λ)(3 − λ). So the characteristic polynomial is (2 − λ)(3 − λ). Roots: λ = 2 and λ = 3 are the eigenvalues.
- For λ = 2: solve (A − 2I)v = 0 → [[0, 1], [0, 1]] [x; y] = 0. This gives y = 0, x free. Eigenspace E_2 = span{[1; 0]}. Any nonzero multiple of [1;0] is an eigenvector with eigenvalue 2.
- For λ = 3: solve (A − 3I)v = 0 → [[−1, 1], [0, 0]] [x; y] = 0. This gives −x + y = 0, so y = x. E_3 = span{[1; 1]}. Any nonzero multiple of [1;1] is an eigenvector with eigenvalue 3.

2) A 2×2 matrix with nontrivial characteristic polynomial
- Let B = [[4, 2], [1, 3]]. Compute characteristic polynomial: det(B − λI) = det([[4 − λ, 2], [1, 3 − λ]]) = (4 − λ)(3 − λ) − 2·1 = λ^2 − 7λ + 10 = (λ − 5)(λ − 2). Eigenvalues: λ = 5 and λ = 2.
- For λ = 5: B − 5I = [[−1, 2], [1, −2]]. Solve (B − 5I)[x; y] = 0 → −x + 2y = 0 so x = 2y. E_5 = span{[2; 1]}.
- For λ = 2: B − 2I = [[2, 2], [1, 1]]. Solve 2x + 2y = 0 so x = −y. E_2 = span{[−1; 1]}.

3) An operator with no real eigenvalues (geometric intuition)
- Consider the rotation matrix R = [[0, −1], [1, 0]] on R^2 (rotation by 90°). Its characteristic polynomial is det(R − λI) = det([−λ, −1], [1, −λ]) = λ^2 + 1. Over R this has no roots, so R has no real eigenvalues and no real eigenvectors. Over C the eigenvalues are λ = i and λ = −i, with corresponding complex eigenvectors.
- This illustrates that existence of eigenvalues depends on the field: a real operator may have no real eigenvalues but have complex eigenvalues.

4) A linear operator on a polynomial space
- Let T: P2 → P2 be differentiation T(p) = p'. For polynomials of degree ≤2, write p(t) = a + bt + ct^2. Then T(p) = b + 2ct.
- Solve T(p) = λ p. If λ ≠ 0, comparing degrees shows the left side has degree ≤1 while λ p has degree up to 2, so the only possibility is c = 0 and then b = λ b and a = λ a. For λ ≠ 1, this forces a = b = 0, but then p = 0, not allowed. Checking possibilities shows the only eigenvalue is λ = 0 with eigenspace the constant polynomials (since T(constant) = 0). So E_0 = span{1}. This shows some operators have only 0 as an eigenvalue on a given space.

Procedure summary
- For a linear operator T on a finite-dimensional vector space with matrix A:
  1. Form the characteristic polynomial p(λ) = det(A − λI).
  2. Find its roots λ (the eigenvalues).
  3. For each eigenvalue λ, solve (A − λI)v = 0 to find the eigenspace and pick nonzero vectors as eigenvectors.
- If working in an infinite-dimensional space or with operators not represented by finite matrices, use the equation (T − λI)v = 0 and analyze kernels directly.

Key points
- Eigenvectors must be nonzero; λ = 0 can be an eigenvalue (then eigenvectors lie in ker T).
- The eigenspace for a given λ is a subspace; if its dimension equals the multiplicity of λ in the characteristic polynomial and the operator has a full set of eigenvectors, the operator is diagonalizable.
- Existence of eigenvalues can depend on the field (real vs complex).

Definition
- Let V be a vector space and T: V → V a linear operator. A subspace U ⊆ V is called invariant under T (or T-invariant) if T(U) ⊆ U; equivalently, for every u ∈ U we have Tu ∈ U.

Basic facts and simple examples
- The trivial subspaces {0} and V are always invariant.
- If v ≠ 0 is an eigenvector of T with eigenvalue λ, then span{v} is T-invariant because T(cv) = cλv ∈ span{v}.
- More generally, an eigenspace E(λ) = {v ∈ V : Tv = λv} is T-invariant: if x ∈ E(λ) then Tx = λx ∈ E(λ).

Restriction of an operator to an invariant subspace
- If U is T-invariant then the restriction T|_U : U → U is a well-defined linear operator. We call T|_U the restriction of T to U.
- Any eigenvalue of T|_U is an eigenvalue of T (because an eigenvector for T|_U is an eigenvector for T).
- Thus invariant subspaces give smaller-dimensional operators whose eigenvalues contribute to the eigenvalues of T.

Using invariant subspaces to reduce eigenvalue problems
- If U is T-invariant, choose a basis of V that begins with a basis of U and then extends to a basis of V. With respect to that basis the matrix of T has the block form
  [ A  * ]
  [ 0  B ]
  where A is the matrix of T|_U (an dim U × dim U block), B represents the action of T on a complementary subspace, and the zero block is a consequence of U being invariant.
- From this block upper-triangular form one obtains the factorization of characteristic polynomials:
  det(zI_V − T) = det(zI_U − T|_U) · det(zI_{V/U} − T̄),
  where T̄ is the induced operator on a choice of complementary subspace (or on the quotient V/U). In particular, the eigenvalues of T are the union (with algebraic multiplicity) of the eigenvalues of T|_U and of the induced operator on the complement/quotient.
- Practically: to find eigenvalues of T you may
  1) find a nontrivial invariant subspace U (for example, spanned by known eigenvectors or other structure),
  2) compute eigenvalues of the smaller operator T|_U,
  3) compute eigenvalues of the induced operator on V/U (or on a chosen complement),
  4) combine the results.

How quotients enter
- If U is invariant then T induces a well-defined operator T̄ : V/U → V/U by T̄(v + U) = Tv + U. The eigenvalues of T̄ are the eigenvalues of T that are not accounted for by T|_U (counting multiplicities as in the characteristic polynomial factorization above). Working on V/U is often convenient when one wants to “mod out” a known invariant subspace.

Remarks and consequences
- Eigenvectors give the simplest nontrivial invariant subspaces (1-dimensional). Finding a single eigenvector reduces the problem by one dimension via restriction to its span and consideration of the quotient.
- If one can decompose V as a direct sum of invariant subspaces V = U1 ⊕ ··· ⊕ Uk, then T has a block-diagonal form relative to that decomposition and the eigenvalue problem reduces to the eigenvalue problems for each block (each T|_{Ui}).
- Over C, existence of at least one eigenvalue (and hence a 1-dimensional invariant subspace) is guaranteed for operators on finite-dimensional nonzero spaces; this is the basic mechanism enabling inductive arguments on dimension.

Short example
- Suppose T has an eigenvector v with eigenvalue λ. Let U = span{v}. Then T|_U is multiplication by λ, so λ is an eigenvalue of T|_U and hence of T. To find the remaining eigenvalues, work with T̄ on V/U (dimension reduced by 1); compute its characteristic polynomial and combine with (z − λ) coming from U.

This is the key idea: invariant subspaces let you restrict or pass to quotients, turning an n-dimensional eigenvalue problem into smaller-dimensional ones that are easier to solve.

Triangular Matrices and Eigenvalues

Basic fact
- If T is represented by an upper-triangular matrix A = (aij) with respect to some basis, then the eigenvalues of T are exactly the entries on the diagonal of A (counted with algebraic multiplicity).
Why: For any scalar λ, A − λI is also upper-triangular with diagonal entries a11 − λ, a22 − λ, …, ann − λ. The determinant of an upper-triangular matrix equals the product of its diagonal entries, so
det(A − λI) = ∏_{j=1}^n (ajj − λ).
Thus the characteristic polynomial factors as ∏(ajj − λ), and its roots are precisely the diagonal entries ajj. Equivalently, λ is an eigenvalue iff det(A − λI) = 0, which occurs exactly when some ajj = λ.

Consequences and useful observations
- Reading eigenvalues: When you have an upper-triangular matrix, you can read off all eigenvalues immediately from the diagonal (including multiplicities).
- Similar matrices: If B = P^{-1}AP, then A and B have the same eigenvalues. So if an operator has any upper-triangular matrix representation, the diagonal entries of that triangular matrix give the eigenvalues of the operator.
- Algebraic multiplicity: The number of times a scalar λ appears on the diagonal of an upper-triangular representation equals the algebraic multiplicity of λ (the multiplicity of λ as a root of the characteristic polynomial).
- Geometric information is not fully determined by the diagonal alone: multiplicity on the diagonal gives algebraic multiplicity, but eigenvector dimensions (geometric multiplicity) require more structure.

Triangularization and existence results
- Triangularization principle (finite-dimensional, over an algebraically closed field such as C): Every linear operator on a finite-dimensional vector space has an upper-triangular matrix with respect to some basis. Axler’s approach builds this by induction using the existence of at least one eigenvalue and choosing a basis starting with an eigenvector, then restricting to the quotient/subspace to continue.
- How triangularization helps prove existence results:
  - Existence of eigenvalues over C: If you can triangularize an operator, its diagonal entries (which are entries of the triangular matrix) are eigenvalues. In fact, Axler uses the contrapositive: show operators on complex vector spaces always have at least one eigenvalue, then inductively produce a basis giving an upper-triangular matrix.
  - Counting eigenvalues with multiplicity: Once triangularized, the characteristic polynomial is the product of linear factors (λ − ajj), so over C the polynomial splits completely and the eigenvalues with algebraic multiplicity are explicit.
  - Invariant subspaces: The triangular form itself exhibits a flag of invariant subspaces: if A is upper-triangular with respect to basis v1, …, vn, then span{v1, …, vk} is invariant for each k. This flag is the device used in induction proofs and in constructing invariant subspaces corresponding to blocks of eigenvalues.

Examples of use
- To prove that a linear operator on a complex finite-dimensional space has at least one eigenvalue: pick a nonzero vector v, consider the space spanned by {v, Tv, T^2v, …}. If that sequence is linearly dependent, a polynomial p of degree ≥1 annihilates v; factor p over C to obtain a linear factor giving an eigenvalue. From that eigenvalue you start the triangularization induction.
- To compute the characteristic polynomial quickly: triangular form reduces determinant computation to multiplying diagonal entries (A − λI), making eigenvalue computation straightforward.

Caveats
- Over fields that are not algebraically closed (e.g., R), an operator need not be triangularizable over that field; triangularization may require extending scalars to an algebraic closure (e.g., passing to C). Over R one can often get real canonical forms with 2×2 blocks for complex conjugate pairs instead of full triangularization.
- Triangular matrices reveal algebraic multiplicities directly but do not by themselves give the dimensions of eigenspaces (geometric multiplicities) except to show that geometric multiplicity ≤ algebraic multiplicity.

Summary (one-line): Upper-triangular representations make eigenvalues immediately visible on the diagonal and triangularization (available over algebraically closed fields) is the key tool for proving existence, counting, and basic structural facts about eigenvalues.

Section 29 — Inner Product

Definition
- An inner product on a real or complex vector space V is a function ⟨·,·⟩ : V × V → F (where F = R or C) satisfying, for all u,v,w ∈ V and all scalars α ∈ F:
  1. Conjugate-linearity in the first argument and linearity in the second argument (Axler uses the convention linear in the second argument):
     - ⟨u, v + w⟩ = ⟨u, v⟩ + ⟨u, w⟩
     - ⟨u, αv⟩ = α⟨u, v⟩
     - ⟨αu, v⟩ = overline{α} ⟨u, v⟩
  2. Conjugate symmetry:
     - ⟨v, u⟩ = overline{⟨u, v⟩}
     (In the real case this reduces to ⟨v,u⟩ = ⟨u,v⟩.)
  3. Positive-definiteness:
     - ⟨v, v⟩ ≥ 0 for all v, and ⟨v, v⟩ = 0 iff v = 0.

Remarks on Axler's convention: Many authors take linearity in the first argument and conjugate-linearity in the second. Here we follow Axler: linear in the second argument, conjugate-linear in the first.

Examples and verifications

1) Standard dot product on R^n
- Definition: For x = (x1,...,xn), y = (y1,...,yn) ∈ R^n, define ⟨x,y⟩ = ∑_{i=1}^n xi yi.
- Linearity in second argument:
  ⟨x, y+z⟩ = ∑ xi(yi+zi) = ∑ xi yi + ∑ xi zi = ⟨x,y⟩ + ⟨x,z⟩.
  ⟨x, αy⟩ = ∑ xi (α yi) = α ∑ xi yi = α ⟨x,y⟩.
- Conjugate-linearity in first argument: over R conjugation is trivial, so ⟨αx, y⟩ = α⟨x,y⟩ (which matches since α is real).
- Symmetry: ⟨y,x⟩ = ∑ yi xi = ∑ xi yi = ⟨x,y⟩.
- Positive-definiteness: ⟨x,x⟩ = ∑ xi^2 ≥ 0; equals 0 iff all xi = 0, i.e. x = 0.

2) Standard inner product on C^n
- Definition: For z = (z1,...,zn), w = (w1,...,wn) ∈ C^n, define ⟨z,w⟩ = ∑_{i=1}^n overline{zi} wi.
- Linearity in second argument:
  ⟨z, w+u⟩ = ∑ overline{zi}(wi+ui) = ∑ overline{zi} wi + ∑ overline{zi} ui = ⟨z,w⟩ + ⟨z,u⟩.
  ⟨z, αw⟩ = ∑ overline{zi} (α wi) = α ∑ overline{zi} wi = α ⟨z,w⟩.
- Conjugate-linearity in first argument:
  ⟨αz, w⟩ = ∑ overline{α zi} wi = overline{α} ∑ overline{zi} wi = overline{α} ⟨z,w⟩.
- Conjugate symmetry:
  ⟨w,z⟩ = ∑ overline{wi} zi = overline{∑ overline{zi} wi} = overline{⟨z,w⟩}.
- Positive-definiteness:
  ⟨z,z⟩ = ∑ overline{zi} zi = ∑ |zi|^2 ≥ 0, and equals 0 iff all zi = 0.

3) L^2 inner product for continuous functions on [a,b]
- Space: V = C([a,b]) (or more generally L^2[a,b]).
- Definition: ⟨f,g⟩ = ∫_a^b overline{f(t)} g(t) dt.
- Linearity in second argument and conjugate-linearity in first follow from linearity properties of the integral:
  ⟨f, g + h⟩ = ∫ overline{f}(g+h) = ∫ overline{f} g + ∫ overline{f} h = ⟨f,g⟩ + ⟨f,h⟩, etc.
  ⟨αf, g⟩ = ∫ overline{α f} g = overline{α} ∫ overline{f} g = overline{α} ⟨f,g⟩.
- Conjugate symmetry: ⟨g,f⟩ = ∫ overline{g} f = overline{∫ overline{f} g} = overline{⟨f,g⟩}.
- Positive-definiteness: ⟨f,f⟩ = ∫ |f(t)|^2 dt ≥ 0; equals 0 iff f = 0 almost everywhere (in L^2 setting) or f ≡ 0 for continuous functions.

4) Inner product on polynomial space via coefficient pairing
- Space: V = P_n (polynomials of degree ≤ n) with real or complex coefficients.
- Definition: For p(x) = ∑_{k=0}^n ak x^k and q(x) = ∑_{k=0}^n bk x^k, set ⟨p,q⟩ = ∑_{k=0}^n overline{ak} bk.
- This is just the C^ (n+1) inner product on coefficient vectors, so all axioms follow as in example 2. Positive-definiteness holds because ⟨p,p⟩ = ∑ |ak|^2, zero iff all ak = 0 (p = 0).

Notes on checking axioms
- When verifying linearity/conjugate-linearity be explicit which argument is linear. Follow Axler: linear in the second argument.
- Conjugate symmetry implies ⟨v,v⟩ is always real; combined with positive-definiteness it gives a norm via ‖v‖ = sqrt(⟨v,v⟩).
- Many examples are built from the standard C^n inner product by coordinate identification or by integrals that mimic the coordinate sum.

End of section.

Linear functionals as inner products (finite-dimensional Riesz representation)

Statement (Riesz representation, finite-dimensional). Let V be a finite-dimensional inner-product space (Axler’s convention: inner product linear in the first argument, conjugate-linear in the second). For every linear functional φ ∈ V* there exists a unique vector y ∈ V such that
φ(x) = ⟨x, y⟩ for all x ∈ V.
We call y the Riesz representation of φ.

Proof sketch (constructive). Pick an orthonormal basis {e1,...,en} of V. Write an arbitrary x = ∑i ⟨x, ei⟩ ei. Define
y = ∑i overline{φ(ei)} ei.
Then for any x
⟨x, y⟩ = ⟨∑i ⟨x, ei⟩ ei, ∑j overline{φ(ej)} ej⟩ = ∑i ⟨x, ei⟩ φ(ei) = φ(∑i ⟨x, ei⟩ ei) = φ(x),
so φ(x) = ⟨x,y⟩. Uniqueness follows because if ⟨x,y⟩ = ⟨x,y'⟩ for all x then ⟨x,y−y'⟩ = 0 for all x, so y − y' = 0.

Immediate consequences and how to compute/characterize functionals

- Formula from values on an orthonormal basis. If φ is known on an orthonormal basis {ei}, then the representing vector is
  y = ∑i overline{φ(ei)} ei,
  and for any x = ∑i ⟨x, ei⟩ ei,
  φ(x) = ∑i ⟨x, ei⟩ φ(ei).

- If {v1,...,vn} is a (not necessarily orthonormal) basis, write x and y in that basis and use the Gram matrix G with entries Gij = ⟨vi, vj⟩. Given the values φ(vj) = cj, the coordinates a of y in the basis satisfy Ga = overline{c} (conjugation depends on the inner-product convention), so solve a = G^{-1} overline{c} to obtain y and then φ(x) = ⟨x,y⟩.

- Norm equality. The operator norm of φ equals the norm of its representing vector:
  ||φ|| = ||y||,
  attained at any x with ||x|| = 1 and x parallel to y. (In particular, φ = 0 iff y = 0.)

- Kernel and orthogonality. ker φ = {x : φ(x) = 0} equals the orthogonal complement y⊥. Thus ker φ is an (n−1)-dimensional hyperplane when φ ≠ 0.

- Adjoint viewpoint. Identifying V and V* via φ ↔ y with φ(x)=⟨x,y⟩ is an isometric conjugate-linear isomorphism (conjugate-linear because of the usual dual pairing conventions). This identification makes many statements about functionals easiest to handle by working with the corresponding vectors.

Examples of practical use

- To extend a linear functional specified on a basis to all of V: find an orthonormal basis containing those basis vectors (or compute Gram matrix), compute the representing y as above, then evaluate φ(x) = ⟨x,y⟩.

- To test whether two functionals φ and ψ are equal: form their representing vectors yφ and yψ; φ = ψ iff yφ = yψ.

- To compute ||φ||: compute the representing y and take its norm.

These are the finite-dimensional Riesz representation facts used throughout inner-product theory: every linear functional is “inner product with a fixed vector,” unique representation, norm equality, and kernel = orthogonal complement.

Norm and Distance (from an Inner Product)

Definition and basic properties
- If V is an inner-product space with inner product <·,·>, define the norm (length) of v in V by
  ||v|| := sqrt(<v,v>).
  This is well-defined because <v,v> ≥ 0 and <v,v> = 0 iff v = 0.
- Define the distance between u and v by
  d(u,v) := ||u − v||.
  This makes (V,d) a metric space once the norm axioms are established.

Proof that ||·|| satisfies the norm axioms
1. Positive definiteness: ||v|| ≥ 0 for all v, and ||v|| = 0 ⇔ v = 0, because <v,v> ≥ 0 and equals 0 only for v = 0.
2. Homogeneity: for scalar α and vector v,
   ||α v|| = sqrt(<α v, α v>) = sqrt(ᾱ α <v,v>) = |α| ||v||.
3. Triangle inequality: shown below using Cauchy–Schwarz.

Cauchy–Schwarz inequality
- Statement: For all v,w in V,
  |<v,w>| ≤ ||v|| · ||w||,
  with equality iff v and w are linearly dependent (one is a scalar multiple of the other).

- Proof: If w = 0 the inequality is trivial. Assume w ≠ 0 and consider the scalar-valued function of t in R (or C)
  f(t) := ||v − t w||^2 = <v − t w, v − t w> ≥ 0 for all t.
  Expand:
  f(t) = <v,v> − t <v,w> − t̄ <w,v> + |t|^2 <w,w>.
  Choose t = <w,v> / <w,w> (if scalars are complex use that choice; for real scalars choose t = <v,w>/<w,w>) so that the linear terms cancel optimally. Substituting yields
  0 ≤ f(t) = ||v||^2 − |<v,w>|^2 / ||w||^2.
  Rearranging gives |<v,w>|^2 ≤ ||v||^2 ||w||^2, hence Cauchy–Schwarz.

- Equality case: f(t) = 0 for that t iff v − t w = 0, i.e. v is a scalar multiple of w.

Triangle inequality (via Cauchy–Schwarz)
- For u,w in V,
  ||u + w||^2 = <u + w, u + w> = ||u||^2 + 2 Re <u,w> + ||w||^2
  ≤ ||u||^2 + 2 |<u,w>| + ||w||^2
  ≤ ||u||^2 + 2 ||u|| ||w|| + ||w||^2 = (||u|| + ||w||)^2,
  using Cauchy–Schwarz in the middle step. Taking square roots gives
  ||u + w|| ≤ ||u|| + ||w||.
- From homogeneity and the triangle inequality one gets the metric properties of d(u,v) = ||u − v||, in particular symmetry and the triangle inequality for distances:
  d(u,w) ≤ d(u,v) + d(v,w).

Parallelogram law and polarization
- Parallelogram law: for all v,w,
  ||v + w||^2 + ||v − w||^2 = 2(||v||^2 + ||w||^2).
  Proof: expand both squares and add; cross terms cancel.
- Polarization identity (recovers inner product from norm): when needed,
  In the real case: <v,w> = (1/4)(||v + w||^2 − ||v − w||^2).
  In the complex case: <v,w> = (1/4) ∑_{k=0}^3 i^k ||v + i^k w||^2.
  These show that an inner product is determined by the norm satisfying the parallelogram law.

Typical estimates and uses
- Upper bound on inner products: |<v,w>| ≤ ||v|| ||w||. Use to bound projection coefficients and to control bilinear forms coming from the inner product.
- Distance estimate: For any vectors u,v,w,
  | ||u|| − ||v|| | ≤ ||u − v|| (reverse triangle inequality), obtained from
  ||u|| = ||(u − v) + v|| ≤ ||u − v|| + ||v||, and swap u,v.
- Norm of a sum/subtraction bounds:
  ||u ± v|| ≤ ||u|| + ||v||, and hence ||u|| − ||v|| ≤ ||u ± v|| ≤ ||u|| + ||v|| as appropriate.
- Projection estimate: If proj_w(v) = (<v,w>/<w,w>) w then
  ||proj_w(v)|| ≤ ||v||, immediate from Cauchy–Schwarz.

Worked quick example
- Given v,w with ||v|| = 3, ||w|| = 4, bound |<v,w>| and ||v + w||:
  |<v,w>| ≤ 3·4 = 12.
  ||v + w|| ≤ 3 + 4 = 7; also ||v + w||^2 = 3^2 + 4^2 + 2 Re <v,w> so it lies between |3−4| = 1 and 7.

Concluding remarks
- The norm induced by an inner product gives a geometrical notion of length and distance compatible with the algebraic structure of V.
- Cauchy–Schwarz and the triangle inequality are the primary tools for estimating lengths, inner products, and distances in inner-product spaces.

Orthogonality — definition and basic facts
- Let V be an inner product space with inner product ⟨·,·⟩. Two vectors v,w ∈ V are orthogonal, written v ⟂ w, iff ⟨v,w⟩ = 0.
- For a subset S ⊆ V define the orthogonal complement
  S⊥ = { v ∈ V : ⟨v,s⟩ = 0 for all s ∈ S }.
  S⊥ is always a subspace of V.
- In particular, for a subspace U ≤ V, U⊥ is the set of all vectors orthogonal to every vector of U.

Elementary consequences (useful facts)
- U ∩ U⊥ = {0}. (If v is in both, ⟨v,v⟩ = 0 so v = 0.)
- If S ⊆ T then T⊥ ⊆ S⊥. In particular, (span S)⊥ = S⊥.
- (U + W)⊥ = U⊥ ∩ W⊥ for subspaces U,W.
- In finite-dimensional V one also has (U ∩ W)⊥ = U⊥ + W⊥.

Computing orthogonal complements (practical methods)
- Basis method: If U = span{u1,…,uk}, then a vector v = (unknown) is in U⊥ iff ⟨v, ui⟩ = 0 for i = 1..k. This yields a homogeneous linear system for the coordinates of v; its solution space is U⊥.
- Matrix/kernel method: Fix an orthonormal basis or any basis and represent the ui as columns of a matrix A (each column is coordinates of a ui). Then U = column space(A), and U⊥ = {x : A* x = 0}, i.e. U⊥ = nullspace(A*), where A* is the conjugate-transpose (transpose for real spaces). So U⊥ is the kernel of A*.
- Orthonormal basis simplifies computations: If {e1,…,en} is orthonormal and U = span{e1,…,ek}, then U⊥ = span{ek+1,…,en}. For an arbitrary set, apply Gram–Schmidt to produce an orthonormal basis containing an orthonormal basis of U, then read off U⊥.

Finite-dimensional dimension and closure properties
- If V is finite-dimensional and U ≤ V then
  dim U + dim(U⊥) = dim V.
  Equivalently, (U⊥)⊥ = U.
  (Both follow from rank-nullity applied to the matrix A* above.)
- Consequences:
  - U = {0} ⇔ U⊥ = V, and U = V ⇔ U⊥ = {0}.
  - If U ⊆ W then W⊥ ⊆ U⊥, and dim W − dim U = dim(U⊥) − dim(W⊥).
- For subspaces U,W ≤ V (finite-dimensional):
  - (U + W)⊥ = U⊥ ∩ W⊥.
  - (U ∩ W)⊥ = U⊥ + W⊥.
  - Taking orthogonal complements reverses inclusions and exchanges sums and intersections.

Examples
1) Single vector: If v ≠ 0 in R^n with the standard inner product, then span{v}⊥ is the (n−1)-dimensional hyperplane of all x with x·v = 0. Solve v^T x = 0 to get an explicit basis.
2) Two vectors: Let u1,u2 ∈ R^3. To find span{u1,u2}⊥ set up the 2 × 3 matrix A whose rows are u1^T,u2^T (or columns if you prefer) and solve A x = 0. The solution is a 1-dimensional space (if u1,u2 are independent), giving an explicit orthogonal vector.
3) Using Gram–Schmidt: Given arbitrary vectors spanning U, orthonormalize them to get e1,…,ek. Extend to an orthonormal basis e1,…,en of V. Then U⊥ = span{ek+1,…,en} immediately.

Why (U⊥)⊥ = U in finite dimensions (sketch)
- Let A have columns a1,…,ak spanning U. Then U⊥ = ker(A*). Applying the same construction to U⊥, (U⊥)⊥ = ker((A*)*) = ker(A)⊥? More directly: rank(A) + nullity(A*) = n and nullity(A*) = dim(U⊥), so dim((U⊥)⊥) = n − dim(U⊥) = dim U. Since U ⊆ (U⊥)⊥ and dimensions agree, equality holds.

Takeaways (how to use these in problems)
- To test orthogonality always evaluate the inner product.
- To compute an orthogonal complement, write linear equations ⟨x,ui⟩ = 0 for a basis {ui} of the subspace, or compute nullspace of the conjugate-transpose of the matrix of basis vectors.
- In finite-dimensional problems use dim U + dim U⊥ = dim V and (U⊥)⊥ = U to convert between subspaces and their complements and to count dimensions.

Orthonormal Bases and Gram–Schmidt

Definition and basic facts
- A list (e1, ..., en) in an inner-product space V is orthonormal if each ei has norm 1 and they are mutually orthogonal: <ei, ej> = 0 for i ≠ j.
- An orthonormal list of length n that spans V (dim V = n) is an orthonormal basis.
- Key consequences for an orthonormal basis (e1, ..., en):
  - Coordinates: For any v in V,
    v = sum_{i=1}^n <v, ei> ei.
    So the coordinate (i-th) of v relative to this basis is <v, ei>.
  - Inner products: For u, v in V,
    <u, v> = sum_{i=1}^n <u, ei> conj(<v, ei>).
    In particular, if the field is real, <u,v> = sum_i <u,ei><v,ei>.
  - Norms / Parseval: ||v||^2 = sum_{i=1}^n |<v, ei>|^2.
  - Orthogonal projection onto span{e1,...,ek} is sum_{i=1}^k <v, ei> ei.

Gram–Schmidt process (constructing an orthonormal list from a linearly independent list)
Given a linearly independent list (v1, ..., vn) in an inner-product space V, Gram–Schmidt produces an orthonormal list (e1, ..., en) with span{v1,...,vk} = span{e1,...,ek} for each k.

Algorithm (constructive steps):
1. Set u1 = v1. Define e1 = u1 / ||u1||.
2. For k = 2,...,n:
   - Compute the k-th orthogonal component
     uk = vk - sum_{j=1}^{k-1} <vk, ej> ej.
     (This subtracts the projection of vk onto the previously produced orthonormal vectors.)
   - If uk = 0 then vk was in the span of previous vectors; the original list was not independent.
   - Otherwise set ek = uk / ||uk||.

Remarks:
- Each uk is orthogonal to e1,...,e_{k-1} by construction, so ek are mutually orthonormal.
- The process yields an orthonormal basis when starting from a basis.

Example 1 — Gram–Schmidt in R^3 (standard real inner product)
Start with v1 = (1,1,0), v2 = (1,0,1), v3 = (0,1,1).
1. u1 = v1 = (1,1,0), e1 = u1 / ||u1|| = (1,1,0)/√2.
2. Compute projection of v2 onto e1: <v2,e1> = (1+0)/√2 = 1/√2.
   u2 = v2 - <v2,e1> e1 = (1,0,1) - (1/√2)*(1,1,0)/√2 = (1,0,1) - (1/2)(1,1,0) = (1/2, -1/2, 1).
   ||u2|| = √((1/2)^2 + (-1/2)^2 + 1^2) = √(1/4+1/4+1)=√(3/2).
   e2 = u2 / ||u2||.
3. For v3 compute <v3,e1>, <v3,e2>, subtract projections to get u3 and normalize to get e3.
(You can carry out arithmetic to get explicit ei.)

Using orthonormal bases to compute coordinates and simplify inner products
- Coordinates: Once you have an orthonormal basis (e1,...,en), computing coordinates of any v reduces to inner products c_i = <v, ei>. No need to solve linear systems.
- Inner products: To compute <u,v>, compute coordinates c_i = <u,ei>, d_i = <v,ei>, then <u,v> = sum_i c_i conj(d_i). This often reduces a complicated inner-product computation to a few scalar multiplications and sums.
- Norms: ||v|| = √(sum |<v,ei>|^2).

Example 2 — Computing inner product via orthonormal basis
Let e1, e2 be orthonormal in some inner-product space. If u = 3 e1 + 2 e2 and v = e1 - 4 e2, then
<u,v> = (3)(1) + (2)(-4) = 3 - 8 = -5
(using real scalars; with complex scalars take conjugates appropriately).

Practical tips
- When working in R^n with the standard inner product, Gram–Schmidt is numerical-friendly but can suffer loss of orthogonality numerically; use modified Gram–Schmidt in computations for better stability.
- If you only need projection onto a subspace, you can compute the orthonormal basis for that subspace and use the projection formula; you do not need a full basis for V.
- Orthonormal bases diagonalize the Gram matrix: if B is matrix whose columns are basis vectors, then with an orthonormal basis the Gram matrix is the identity and coordinate computations are simplest.

Summary of formulas to remember
- e_k = (vk - sum_{j<k} <vk, ej> ej) / ||vk - sum_{j<k} <vk, ej> ej||  (Gram–Schmidt step)
- Coordinates: v = sum_i <v, ei> ei
- Inner product: <u,v> = sum_i <u, ei> conj(<v, ei>)
- Norm: ||v||^2 = sum_i |<v, ei>|^2

End of section.

Orthogonal projection and best approximation

Definition
- Let V be a subspace of an inner product space W and let x ∈ W. An orthogonal projection of x onto V is the vector p ∈ V such that x − p is orthogonal to every vector in V:
  for all v ∈ V, ⟨x − p, v⟩ = 0.
- When such p exists (and in finite-dimensional inner-product spaces it does), it is unique and denoted proj_V x.

Computing proj_V x
1. If V has an orthonormal basis {u1,...,uk}:
   proj_V x = Σ_{i=1}^k ⟨x, ui⟩ ui.
   (This is the simplest formula: take inner products with the orthonormal basis and sum.)

2. If V is spanned by a linearly independent (not orthonormal) set {v1,...,vk}, form the Gram matrix G with Gij = ⟨vi, vj⟩ and the vector b with bj = ⟨x, vj⟩. Solve the normal equations G c = b for coefficients c = (c1,...,ck). Then
   proj_V x = Σ_{i=1}^k ci vi.
   (Equivalently, if A is the linear map with columns v1,...,vk, then proj_V x = A (A^* A)^{-1} A^* x.)

Properties used in computation
- Normal equations come from the orthogonality condition: for each j, ⟨x − Σ ci vi, vj⟩ = 0.
- If you prefer, convert {v1,...,vk} to an orthonormal basis of V via Gram–Schmidt and apply formula (1).

Best-approximation (closest vector) property
- For any x ∈ W, proj_V x is the unique vector in V closest to x: for every v ∈ V,
  ||x − proj_V x|| ≤ ||x − v||,
  with equality only when v = proj_V x.
- Equivalent geometric/pythagorean statement: for p = proj_V x and any v ∈ V,
  ||x − v||^2 = ||x − p||^2 + ||p − v||^2.
  In particular, ||x − p|| is the minimal distance from x to V.

Short example
- Project x = (2,0) onto the subspace V = span{(1,1)} in R^2 with the standard inner product. Orthonormalize u = (1,1)/√2. Then
  proj_V x = ⟨(2,0), u⟩ u = ( (2·1 + 0·1)/√2 ) u = (2/√2)·(1/√2)(1,1) = (1,1).

Summary checklist for finding proj_V x
- If you can, get an orthonormal basis of V and use proj_V x = Σ ⟨x, ui⟩ ui.
- Otherwise set up and solve the normal equations G c = b (Gram matrix approach).
- The result is the unique closest vector in V to x; use the Pythagorean relation to compute distances.

Section 35 — Adjoint Operator

Definition
- Let V be an inner product space over F (R or C). For a linear operator T : V → V, an operator T* : V → V is called an adjoint of T if for every v, w ∈ V,
  <T v, w> = <v, T* w>.
- In finite-dimensional inner product spaces the adjoint always exists and is unique.

How to compute an adjoint (using the defining identity)
- Use the identity <T v, w> = <v, T* w> as an equation in v (for fixed w). To find T* w you find the vector that yields the same inner product with every v as <T v, w> does.
- Practical recipe in coordinates: if {e_i} is an orthonormal basis and [T] is the matrix of T in that basis, then the matrix of T* in that basis is the conjugate-transpose [T]* = [T]̅^T (i.e., the Hermitian transpose). Thus compute T* by taking the conjugate-transpose of the matrix of T relative to an orthonormal basis.
- Example (quick): If V = C^n with standard inner product and T has matrix A, then T*(x) = A* x where A* = Ȧ^T.

Basic properties (derived from the defining identity)
1. Linearity (conjugate-linearity in scalars):
   - (aT + bS)* = \overline{a} T* + \overline{b} S* for a, b ∈ F and linear operators S, T. Proof: compute <(aT + bS) v, w> and move scalars to the other side using conjugation of scalars in the inner product.
2. Composition reversal:
   - (ST)* = T* S*. Proof: for all v, w,
     <ST v, w> = <T v, S* w> = <v, T* S* w>,
     so by uniqueness of adjoint, (ST)* = T* S*.
3. Involution:
   - (T*)* = T. Proof: apply definition twice and use uniqueness.
4. Scalar adjoint:
   - If λ ∈ F, then (λ I)* = \overline{λ} I.

Relations between kernels and ranges
- Orthogonality relations (finite-dimensional setting as in Axler):
  - ker(T*) = (range T)⊥.
    Proof: w ∈ ker(T*) ⇔ T* w = 0 ⇔ for all v, <T v, w> = <v, T* w> = 0 ⇔ w is orthogonal to every vector in range(T).
  - range(T*) = (ker T)⊥.
    Proof: x ∈ range(T*) ⇔ x = T* y for some y ⇔ for every z ∈ ker T, <x, z> = <T* y, z> = <y, T z> = 0, so x ⟂ ker T. Conversely, if x ⟂ ker T, dimension-counting (or orthogonal decomposition) gives x ∈ range(T*). In finite dimensions this yields range(T*) = (ker T)⊥.
- Consequences:
  - rank(T) = rank(T*). (Because dim(range T) = dim(range T*) = dim(V) − dim(ker T) = dim(V) − dim(ker T*).)
  - T is injective ⇔ range(T*) is dense/full etc.; in finite dimensions T injective ⇔ range(T*) = V.

Norm and adjoint (brief)
- For operators on finite-dimensional inner product spaces, ||T|| = ||T*|| and ||T* T|| = ||T||^2; these follow from properties of the adjoint and the definition of operator norm.

Summary of key identities to use repeatedly
- <T v, w> = <v, T* w> (definition)
- (ST)* = T* S*
- (aT + bS)* = \overline{a} T* + \overline{b} S*
- (T*)* = T
- ker(T*) = (range T)⊥, range(T*) = (ker T)⊥

Use the defining identity to compute adjoints in examples and to derive the properties above; in coordinates pick an orthonormal basis so the adjoint is just conjugate-transpose of the matrix.

Normal operators

Definition
- Let V be an inner-product space (over R or C) and T : V → V linear. T is normal if T T* = T* T, where T* is the adjoint of T. Equivalently, T is normal iff ||T v|| = ||T* v|| for every v in V (this follows from ||T v||^2 = ⟨T v, T v⟩ = ⟨T* T v, v⟩ = ⟨T T* v, v⟩ = ||T* v||^2 when T T* = T* T).

Basic structural properties and proofs

1) Eigenvectors of a normal operator give eigenvectors of the adjoint (conjugate eigenvalues).
- Claim: If T is normal and T v = λ v (v ≠ 0), then T* v = λ̄ v.
- Proof: (T − λ I) v = 0. The operator N := T − λ I is normal (because T and λ I commute and T normal ⇒ T − λ I normal). For a normal operator N we have ||N v|| = ||N* v|| for all v, hence ker N = ker N*. Thus 0 = N v implies 0 = N* v = (T* − λ̄ I) v, so T* v = λ̄ v. □

2) Eigenspaces corresponding to distinct eigenvalues are orthogonal.
- Statement: If T is normal, and T v = λ v, T w = μ w with λ ≠ μ, then ⟨v, w⟩ = 0.
- Proof: Since (T − λ I) v = 0 we have 0 = ⟨(T − λ I) v, w⟩ = ⟨v, (T − λ I)* w⟩. But (T − λ I)* = T* − λ̄ I and by (1) T* w = μ̄ w, so
  0 = ⟨v, (μ̄ − λ̄) w⟩ = (μ̄ − λ̄) ⟨v, w⟩.
  Because μ̄ − λ̄ ≠ 0, it follows that ⟨v, w⟩ = 0. □

3) Unitary/orthonormal diagonalizability in the finite-dimensional complex case (spectral theorem for normal operators).
- Statement: If V is finite-dimensional over C and T : V → V is normal, then there exists an orthonormal basis of V consisting of eigenvectors of T; equivalently, T is unitarily diagonalizable (there is a unitary U with U* T U diagonal).
- Proof (standard Schur-based argument): By Schur’s theorem, for any linear T on a finite-dimensional complex inner-product space there is an orthonormal basis in which T has upper-triangular matrix R (with eigenvalues on the diagonal). Write R = [r_{ij}]. If T is normal, R must be normal as well (unitary similarity preserves normality). For an upper-triangular matrix R, normality forces all entries above the diagonal to vanish: compute R R* and R* R and compare the (1,2) (or any off-diagonal) entries — the off-diagonal entries of R R* and R* R involve the strictly upper-triangular part; equality forces those strictly upper-triangular entries to be 0. Thus R is diagonal. Hence T is diagonal with respect to an orthonormal basis, i.e., there is an orthonormal eigenbasis. □

Consequences and remarks
- Over C, normal ⇒ diagonalizable by a unitary change of basis; over R one gets an orthogonal block-diagonal form consisting of 1×1 real-eigenvalue blocks and 2×2 rotation/complex-conjugate-eigenvalue blocks.
- Self-adjoint (Hermitian), unitary, and normal commuting normal operators are all examples of normal operators; for self-adjoint T the eigenvalues are real and the previous proofs simplify (T* = T implies immediately ⟨Tv, w⟩ = ⟨v, Tw⟩).
- The orthogonality of distinct eigenspaces is often used to build an orthonormal eigenbasis: pick an orthonormal basis in each eigenspace and combine them (direct sum is orthogonal by (2)).

This collection of properties (definition, adjoint eigenvalue correspondence, orthogonality of distinct eigenspaces, and unitary diagonalizability in the finite-dimensional complex case) captures the primary structural facts about normal operators used throughout operator theory on inner-product spaces.

Orthogonal projections

Definition and geometric characterization
- Let V be an inner-product space and W a subspace. The orthogonal projection of v ∈ V onto W is the unique vector w ∈ W such that v − w ∈ W⊥. Equivalently, w is the unique point of W closest to v (minimizes ||v − x|| over x ∈ W).
- Existence/uniqueness (finite-dimensional case): If V is finite-dimensional, then V = W ⊕ W⊥, so every v decomposes uniquely as v = w + w⊥ with w ∈ W, w⊥ ∈ W⊥; that w is the orthogonal projection of v onto W. This establishes existence and uniqueness of the orthogonal projection map P_W : V → W given by P_W(v) = w.

Formula in an orthonormal basis
- If {u1,…,uk} is an orthonormal basis of W, then for every v ∈ V
  P_W(v) = ∑_{j=1}^k ⟨v, uj⟩ uj.
- Proof sketch: write w = ∑ α_j uj. The condition v − w ∈ W⊥ is equivalent to ⟨v − w, uj⟩ = 0 for all j, so ⟨v, uj⟩ = ⟨w, uj⟩ = α_j, hence α_j = ⟨v, uj⟩ and the formula follows.
- Matrix form: relative to an orthonormal basis of V in which the first k vectors span W, the matrix of P_W is block diagonal with an identity I_k in the W-block and 0 in the W⊥-block.

Operator-theoretic characterization
- P_W is linear and satisfies P_W^2 = P_W (idempotent). Also P_W* = P_W (self-adjoint). Thus P_W is a self-adjoint idempotent.
- Conversely, any linear operator P on a (finite-dimensional) inner-product space with P^2 = P and P* = P is the orthogonal projection onto Range(P). Proof sketch: Range(P) and Null(P) are orthogonal complements when P is self-adjoint idempotent; for any v, Pv ∈ Range(P) and v − Pv ∈ Null(P) = Range(P)⊥, so Pv is the orthogonal projection of v onto Range(P).

Relations between operator properties and subspaces
- Range(P_W) = W and Null(P_W) = W⊥.
- P_W is the identity on W and zero on W⊥. In particular, for w ∈ W, P_W(w) = w; for z ∈ W⊥, P_W(z) = 0.
- Uniqueness of the operator: there is exactly one linear operator P with Range(P) = W, Null(P) = W⊥ and P^2 = P; that operator is the orthogonal projection P_W.

Notes on computation (alternative viewpoint)
- If {u1,…,uk} is not orthonormal but forms a basis of W and A is the matrix whose columns are the uj relative to some orthonormal basis of V, then the orthogonal projection matrix onto W (in that orthonormal coordinate system) can be written as A(A* A)^{-1}A*. When the columns are orthonormal, A* A = I_k and this reduces to A A* and matches the sum-of-outer-products formula ∑ uj uj*.

Key consequences to remember
- Orthogonal projection gives the orthogonal decomposition V = W ⊕ W⊥.
- Orthogonal projections are precisely the self-adjoint idempotent operators.
- In an orthonormal basis of W, projection coefficients are inner products ⟨v, uj⟩.

Self-Adjoint Operators (T = T*)

Definition
- An operator T on an inner-product space V is self-adjoint if T* = T, i.e. for all u,v in V, <Tu,v> = <u,Tv>.
- In a real inner-product space this is the same as T being symmetric (<Tu,v> = <u,Tv>), and in a matrix representation with respect to an orthonormal basis it means the matrix is Hermitian (conjugate-transpose equals itself).

Characterizations
- T is self-adjoint ⇔ for every v in V, <Tv,v> is real.
  Proof sketch: If T = T*, then <Tv,v> = <v,Tv> = conj(<Tv,v>), so it is real. Conversely, if <Tv,v> is real for all v then by the polarization identity (which recovers inner products from the quadratic form v ↦ <Tv,v>) one gets <Tu,v> = <u,Tv> for all u,v, hence T = T*.
- In an orthonormal basis, T is self-adjoint ⇔ its matrix is Hermitian (entries satisfy a_{ij} = conj(a_{ji})).

Basic consequences
- Real eigenvalues: If Tv = λv with v ≠ 0 and T = T*, then λ is real.
  Proof: λ<v,v> = <λv,v> = <Tv,v> = <v,Tv> = <v,λv> = conj(λ)<v,v>. Since <v,v> ≠ 0, λ = conj(λ), so λ ∈ R.
- Orthogonality of eigenvectors from distinct eigenvalues: If Tv = λv and Tw = μw with λ ≠ μ, then <v,w> = 0.
  Proof: λ<v,w> = <Tv,w> = <v,Tw> = <v,μw> = μ̄<v,w>. Because eigenvalues are real, μ̄ = μ, so (λ−μ)<v,w> = 0 and hence <v,w> = 0.
- Diagonalizability with an orthonormal eigenbasis (Spectral Theorem, finite-dimensional): Every self-adjoint operator on a finite-dimensional inner-product space has an orthonormal basis of eigenvectors; equivalently, it is diagonalizable by a unitary (or orthogonal, in the real case) change of basis and its eigenvalues are real.
- Norm equals spectral radius: For a self-adjoint T, ||T|| = max{|λ| : λ an eigenvalue of T} (the operator norm equals the largest absolute eigenvalue).
- Rayleigh quotient: The scalar <Tv,v>/<v,v> (for v ≠ 0) is always real for self-adjoint T. Extremal values of this Rayleigh quotient are eigenvalues; in particular, the maximum (minimum) is the largest (smallest) eigenvalue and is attained at an eigenvector.

Remarks and useful facts
- Positive (semi)definiteness: If <Tv,v> ≥ 0 for all v then T is called positive semidefinite; if strict > 0 for v ≠ 0 it is positive definite. Such operators are self-adjoint.
- Spectral decomposition: For a self-adjoint T on a real or complex finite-dimensional space, one can write T = sum_i λ_i P_i where {P_i} are orthogonal projections onto the eigenspaces (they are mutually orthogonal and sum to the identity).
- Stability under polynomials: If T = T* and p is a real-coefficient polynomial, then p(T) is self-adjoint and its eigenvalues are p(λ_i).

Key takeaways
- Self-adjointness is the operator-version of “symmetric/Hermitian,” and it forces real eigenvalues and orthogonality between eigenvectors from distinct eigenvalues.
- In finite dimensions, self-adjoint operators admit an orthonormal eigenbasis and hence a particularly simple spectral structure useful for computations and variational characterizations.

Spectral Theorem (finite-dimensional — self-adjoint / normal)

Statement
- Let V be a finite-dimensional inner-product space over F (F = R or C).  
  - If T ∈ L(V) is self-adjoint (T = T*), then V has an orthonormal basis of eigenvectors of T. All eigenvalues of T are real. Equivalently, there exists an orthonormal basis of V relative to which the matrix of T is diagonal with real entries.
  - If F = C and T ∈ L(V) is normal (T*T = TT*), then V has an orthonormal basis of eigenvectors of T. Equivalently, T is unitarily diagonalizable: there exists an orthonormal basis of V in which T is diagonal (eigenvalues need not be real).
- Operator decomposition (same form for both cases): Suppose distinct eigenvalues of T are λ1,...,λk and E_j = ker(T − λj I) are the eigenspaces. Let P_j be the orthogonal projection onto E_j. Then
  - V = E1 ⊕ ··· ⊕ Ek (orthogonal direct sum),
  - T = λ1 P1 + ··· + λk Pk.
  The P_j are mutually orthogonal projections satisfying P_i P_j = 0 (i ≠ j), P_1 + ··· + P_k = I.

How to apply (recipe)
1. Compute eigenvalues λ of T by solving det(T − λI) = 0 (or find spectrum).
2. For each eigenvalue λ, find its eigenspace E = ker(T − λI).
3. On each eigenspace E, choose an orthonormal basis (use Gram–Schmidt if needed). Eigenvectors belonging to different eigenvalues are already orthogonal.
4. Concatenate these orthonormal bases to get an orthonormal eigenbasis of V.
5. The matrix of T relative to this orthonormal basis is diagonal with the eigenvalues on the diagonal (each eigenvalue repeated according to geometric multiplicity).
6. Form orthogonal projections P_j onto each eigenspace E_j (if {u_{j,m}} is an orthonormal basis for E_j, then P_j x = sum_m ⟨x,u_{j,m}⟩ u_{j,m}). Then T = ∑_j λ_j P_j.
7. Use the decomposition for computations: powers, exponentials, polynomials, or functional calculus give f(T) = ∑_j f(λ_j) P_j.

Short example (illustrative outline)
- Given a normal/self-adjoint T on V:
  1. Find eigenvalues λ1, λ2.
  2. Find orthonormal eigenvectors u1 ∈ E1, u2 ∈ E2.
  3. Then {u1,u2} is an orthonormal eigenbasis and T = λ1 P_{u1} + λ2 P_{u2}, where P_{ui} x = ⟨x,ui⟩ ui.
  4. For instance, T^n = λ1^n P_{u1} + λ2^n P_{u2}, and exp(T) = e^{λ1} P_{u1} + e^{λ2} P_{u2}.

Key consequences to remember
- Normal/self-adjoint operators are diagonalizable by an orthonormal change of basis.
- Eigenvectors for distinct eigenvalues are orthogonal.
- Self-adjoint ⇒ eigenvalues real.
- The spectral decomposition T = ∑ λ_j P_j gives an efficient route to functions of T and to understanding T’s action on V.

Section 40 — Positive Operators and Square Roots

Definition
- A linear operator T on an inner product space V (finite-dimensional, over R or C) is called positive (notation: T ≥ 0) if T is self-adjoint and
  ⟨T v, v⟩ ≥ 0 for all v ∈ V.
  (Equivalently one may define positivity by the quadratic form condition ⟨T v, v⟩ ≥ 0 and this implies self-adjointness in the finite-dimensional setting; see Proposition 1 below.)

Basic properties
1. Self-adjointness.
   - If ⟨T v, v⟩ ∈ R for all v and ⟨T v, v⟩ ≥ 0 for all v, then T is self-adjoint. Proof: for all u,v, use polarization identity to express ⟨T u, v⟩ in terms of values of the quadratic form; since those are real, symmetry follows.

2. Nonnegative eigenvalues.
   - If T is positive and T x = λ x with x ≠ 0, then λ ∈ R (since T is self-adjoint) and λ = ⟨T x, x⟩/⟨x,x⟩ ≥ 0. Thus all eigenvalues of a positive operator are ≥ 0.

3. Closure under nonnegative linear combinations.
   - If A and B are positive and α, β ≥ 0 scalars, then αA + βB is positive: it is self-adjoint and ⟨(αA+βB)v,v⟩ = α⟨Av,v⟩ + β⟨Bv,v⟩ ≥ 0.

4. Ordering and square roots via factorization.
   - A linear operator T is positive iff there exists some operator S such that T = S* S. Proof: If T = S* S then T is self-adjoint and ⟨T v, v⟩ = ⟨S v, S v⟩ = ∥S v∥^2 ≥ 0. Conversely, if T ≥ 0, one can construct S as the positive square root (below) so that T = S* S.

Spectral construction of the positive square root (finite-dimensional)
- The existence and uniqueness of the positive square root relies on diagonalizing T.

Theorem (Existence and uniqueness of positive square root).
Let V be finite-dimensional and T: V → V a positive operator. Then there exists a unique positive operator S such that S^2 = T. We call S the positive square root of T and write S = T^{1/2}.

Proof (existence).
- Diagonalize T using the spectral theorem for self-adjoint operators: there is an orthonormal basis {e1,...,en} of V consisting of eigenvectors of T with real eigenvalues λ1,...,λn. Since T ≥ 0, each λj ≥ 0.
- Define S on the basis by S ej = sqrt(λj) ej and extend linearly. Then S is self-adjoint (diagonal in the same orthonormal basis with real entries) and for each j, S^2 ej = (sqrt(λj))^2 ej = λj ej, hence S^2 = T. Also for any v = Σ cj ej,
  ⟨S v, v⟩ = Σ |cj|^2 sqrt(λj) ≥ 0,
  so S is positive.

Proof (uniqueness).
- Suppose R is another positive operator with R^2 = T. Diagonalize T as above and let Vλ be the eigenspace for eigenvalue λ ≥ 0. On each Vλ, both S and R are self-adjoint operators whose squares equal λ I on Vλ, so their eigenvalues on Vλ must be ±sqrt(λ). Positivity forces their eigenvalues to be nonnegative, hence on Vλ both S and R act as sqrt(λ) times the identity. Therefore S = R on each eigenspace, so S = R globally.

Corollary (factorization).
- For a positive T, T = B* B where B = T^{1/2}. Conversely, any operator of the form B* B is positive.

Consequences and useful facts
- Polynomial/functional calculus: if p is a polynomial nonnegative on the spectrum of T, then p(T) is positive. In particular, the map T ↦ T^{1/2} can be obtained by applying the scalar function t ↦ sqrt(t) to the spectral decomposition of T.
- Norm relation: ∥T^{1/2}∥^2 = ∥T∥ when T ≥ 0, because the operator norm equals the largest eigenvalue and taking square roots behaves accordingly.
- Monotonicity: If 0 ≤ A ≤ B (meaning B − A is positive), then A^{1/2} ≤ B^{1/2}. (This follows from the spectral picture: on a common eigenbasis for commuting positive operators or by functional calculus more generally; in finite dimensions one proves monotonicity by diagonalizing in a basis that simultaneously reduces the pair after appropriate arguments.)

Example
- If T is represented by a positive semidefinite matrix (symmetric/Hermitian with nonnegative eigenvalues), compute T^{1/2} by diagonalizing T = U diag(λ1,...,λn) U* and setting T^{1/2} = U diag(sqrt(λ1),...,sqrt(λn)) U*.

Summary of how to construct T^{1/2} in practice
1. Compute an orthonormal eigenbasis of T and the eigenvalues λj ≥ 0.
2. Form the diagonal matrix with entries sqrt(λj).
3. Conjugate back by the orthonormal eigenvectors to obtain T^{1/2}.

This completes the development of positive operators and their unique positive square roots in finite-dimensional inner product spaces.

Concept: Eigenvalues/Eigenvectors over Complex Vector Spaces

Key facts that become available over the complex field
- Every nonconstant complex polynomial splits into linear factors (Fundamental Theorem of Algebra). Consequently, any polynomial with complex coefficients factors as a product of (z − λ) powers.
- For T a linear operator on a finite-dimensional complex vector space V:
  - T has at least one eigenvalue (equivalently, V has a nonzero 1-dimensional T-invariant subspace).
  - The characteristic polynomial χ_T(z) and the minimal polynomial m_T(z) both split completely into linear factors over C:
    χ_T(z) = ∏_{j=1}^k (z − λ_j)^{a_j},   m_T(z) = ∏_{j=1}^k (z − λ_j)^{b_j},
    where the λ_j are the distinct eigenvalues of T and 1 ≤ b_j ≤ a_j for each j.
  - The eigenvalues of T are exactly the roots of χ_T and of m_T.
  - The algebraic multiplicity of an eigenvalue λ (its exponent a_j in χ_T) is at least its geometric multiplicity (dim ker(T − λI)).
  - T is invertible ⇔ 0 is not an eigenvalue ⇔ 0 is not a root of χ_T (or m_T).
- Consequences for structure and classification:
  - T is diagonalizable ⇔ m_T has no repeated factors (i.e., m_T is a product of distinct linear factors) ⇔ for every eigenvalue λ, geometric multiplicity = algebraic multiplicity.
  - The space V decomposes as a direct sum of generalized eigenspaces:
    V = ⊕_{j=1}^k G(λ_j), where G(λ) = {v : (T − λI)^N v = 0 for some N}.
  - For any polynomial p, the spectrum satisfies σ(p(T)) = p(σ(T)): eigenvalues of p(T) are p(λ) for λ an eigenvalue of T (spectral mapping for polynomials).

How to use these facts (typical applications)
1. Existence of eigenvectors.
   - Given T on a nonzero complex V, pick any vector v. The subspace span{v, Tv, T^2v, ...} is finite-dimensional, so T acting on it satisfies a nontrivial polynomial relation. That annihilating polynomial splits over C, so one of its linear factors yields an eigenvalue and eigenvector for T. Thus every such T has an eigenvalue.

2. Relating characteristic and minimal polynomials to eigenstructure.
   - Since m_T splits into linear factors, its roots are eigenvalues; the highest exponent of (z − λ) in m_T equals the size of the largest Jordan block (or equivalently the index of nilpotency of (T − λI) on the generalized eigenspace). The exponent in χ_T gives the total size (algebraic multiplicity).
   - Use m_T to test diagonalizability: compute m_T; if it has no repeated linear factors, T is diagonalizable.

3. Triangularization and decomposition.
   - Over C one can choose a basis that puts T into upper-triangular form (Schur or constructive triangularization). The diagonal entries are eigenvalues (repetition allowed). From the split form of χ_T one can further refine structure into generalized eigenspaces (Jordan form exists over C).

4. Practical tests and consequences.
   - Invertibility test: check if 0 is a root of χ_T or m_T.
   - Spectral computations: if p is a polynomial, eigenvalues of p(T) are p(λ). In particular, if λ is an eigenvalue of T, then λ^n is an eigenvalue of T^n.
   - If T has distinct eigenvalues (all algebraic multiplicities 1), then T is automatically diagonalizable (because m_T is product of distinct linear factors).
   - If an operator satisfies a polynomial equation p(T) = 0 with p splitting and having distinct roots, then V splits into a direct sum of the kernels of the individual factors of p(T) (use Chinese remainder / primary decomposition).

Short proofs / reasoning sketches
- Existence of an eigenvalue: take a nonzero v, consider the finite-dimensional subspace spanned by {v, Tv, T^2v, …}. T satisfies some nonzero polynomial on that subspace; factor that polynomial over C and pick a linear factor (z − λ); its corresponding factor applied to a nonzero vector yields an eigenvector for λ.
- Eigenvalues ↔ roots of χ_T, m_T: by definition an eigenvalue λ means T − λI is not injective, so det(T − λI) = 0, making λ a root of χ_T; minimal polynomial annihilates T, so m_T(T) = 0, hence m_T(λ) = 0 for any eigenvalue λ; conversely, every root of m_T must be an eigenvalue because (T − λI) is not invertible on V.

Takeaway
Working over C gives the powerful advantage that all polynomials split into linear factors. That guarantees existence of eigenvalues, full factorization of characteristic and minimal polynomials, a decomposition into generalized eigenspaces, and strong, checkable criteria for diagonalizability and other structural properties of linear operators.

Generalized eigenspaces and Jordan chains

Definition — generalized eigenspace.
Let V be a finite-dimensional complex vector space and T ∈ L(V). For λ ∈ C and k ≥ 1, set
  K_k(λ) = ker((T − λI)^k).
The generalized eigenspace for λ is
  G(λ) = ⋃_{k≥1} K_k(λ).
Because V is finite-dimensional the ascending chain K_1(λ) ⊆ K_2(λ) ⊆ ··· stabilizes: there exists m such that K_m(λ) = K_{m+1}(λ) = ···, and G(λ) = K_m(λ). Equivalently,
  G(λ) = ker((T − λI)^m)
for m large enough.

Remarks and basic properties
- K_1(λ) = ker(T − λI) is the ordinary eigenspace of λ. In general K_k(λ) consists of vectors whose images under (T − λI)^k are zero; such vectors are called generalized eigenvectors of order ≤ k.
- Each G(λ) is T-invariant because (T − λI) commutes with T and powers of (T − λI) map kernels into kernels.
- If λ ≠ μ then G(λ) ∩ G(μ) = {0}. Consequently, V decomposes as a direct sum of generalized eigenspaces:
    V = ⊕_{λ distinct} G(λ).
  (This decomposition follows from the primary decomposition theorem; on a complex space the minimal polynomial splits and the generalized eigenspaces for distinct roots are complementary invariant subspaces.)
- dim G(λ) equals the algebraic multiplicity of λ (the exponent of (z − λ) in the characteristic polynomial).

Jordan chains
A Jordan chain (or generalized eigenchain) for λ is a sequence of nonzero vectors v_1, v_2, ..., v_k in V satisfying
  (T − λI) v_1 = 0,
  (T − λI) v_2 = v_1,
  (T − λI) v_3 = v_2,
  ...
  (T − λI) v_k = v_{k−1}.
Equivalently, v_k ∈ K_k(λ) but v_k ∉ K_{k−1}(λ); the length of the chain is k and v_k is called a generalized eigenvector of rank k. The vectors v_1, ..., v_k are linearly independent, and the subspace they span is invariant under T.

Building invariant subspaces from kernels
- Quotient viewpoint and chain construction. For each k ≥ 1 consider the successive quotients Q_k = K_k(λ)/K_{k−1}(λ) (with K_0(λ) := {0}). Choosing a basis for each quotient lifts to a set of vectors in K_k(λ) whose images under successive applications of (T − λI) produce Jordan chains. Concretely: pick w in K_k(λ) whose coset represents a nonzero element of Q_k; then w, (T − λI)w, (T − λI)^2 w, ..., (T − λI)^{k−1} w form a chain of length k.
- Decomposition of G(λ) into chain subspaces. One can choose a collection of Jordan chains for λ such that their chain-subspaces (spans of each chain) are linearly independent and their direct sum equals G(λ). Each chain-subspace corresponds to a Jordan block in the Jordan normal form of T restricted to G(λ).
- Nilpotent reduction. On G(λ) the operator N := T − λI is nilpotent. Understanding N (via its Jordan chains) completely describes the action of T on G(λ): T = λI + N, and the sizes of the Jordan chains are exactly the sizes of the Jordan blocks of N (and hence of T) for eigenvalue λ.

Structure beyond diagonalization
- Diagonalizability criterion. T is diagonalizable iff for every eigenvalue λ we have G(λ) = K_1(λ); equivalently, (T − λI) acts as 0 on G(λ) (N = 0), so every Jordan chain has length 1.
- Jordan form interpretation. The decomposition V = ⊕ G(λ) together with a chain decomposition of each G(λ) yields a basis in which the matrix of T is in Jordan normal form: block-diagonal with Jordan blocks J_k(λ) (size k blocks coming from chains of length k).
- Relation to minimal polynomial. The minimal polynomial of T is ∏_λ (z − λ)^{m_λ}, where m_λ is the maximal length of a Jordan chain for λ (equivalently the smallest k with K_k(λ) = K_{k+1}(λ)). Thus generalized eigenspaces and chains determine the exponents in the minimal polynomial.

Takeaway
Generalized eigenspaces K_k(λ) provide a graded way to capture vectors eventually annihilated by powers of (T − λI). Jordan chains are concrete generators of these kernels: chains give invariant subspaces (each chain span) and, when assembled across all λ, produce the full invariant direct-sum decomposition and the Jordan canonical form—describing the structure of T beyond the diagonalizable case.

Jordan canonical form (over C)

Statement (existence and uniqueness up to block order)
- Theorem (Jordan Canonical Form). Let V be a finite-dimensional complex vector space and T: V → V a linear operator. There exists a basis of V with respect to which the matrix of T is block-diagonal, with each block a Jordan block Jk(λ) (a k×k matrix with λ on the diagonal, 1’s on the superdiagonal, 0’s elsewhere). This matrix is called a Jordan matrix for T. The Jordan matrix is unique up to the order in which the Jordan blocks appear.

Key objects and relationships
- Eigenvalue λ:
  - Algebraic multiplicity aλ: the multiplicity of λ as a root of the characteristic polynomial. In the Jordan form it equals the sum of the sizes of all Jordan blocks for λ.
  - Geometric multiplicity gλ: dim ker(T − λI) (the eigenspace dimension). In the Jordan form it equals the number of Jordan blocks for λ.
  - Size of largest Jordan block for λ = the smallest s such that (T − λI)^s annihilates the whole generalized eigenspace for λ. Equivalently, it is the exponent of (z − λ) in the minimal polynomial of T.

- Generalized eigenspace for λ:
  - Vλ := {v ∈ V : (T − λI)^m v = 0 for some m ≥ 1} = ⋃_{k≥1} ker((T − λI)^k).
  - V decomposes as a direct sum of generalized eigenspaces: V = ⊕λ Vλ (one summand per distinct eigenvalue).
  - Each generalized eigenspace Vλ is T-invariant, and the Jordan blocks for λ are determined entirely by the structure of T|Vλ.

How Jordan blocks are read from kernels of powers
- For a fixed eigenvalue λ, set Nk := ker((T − λI)^k). Then the sequence of dimensions dim Nk is nondecreasing and stabilizes at aλ for sufficiently large k.
- The number of Jordan blocks for λ equals dim N1 = gλ.
- More generally, the number of Jordan blocks of size at least k equals dim Nk − dim N{k−1} (with N0 := {0}).
- From these differences one recovers the full partition of aλ into block sizes: let bk := number of blocks of size exactly k. Then for each k ≥ 1,
  - number of blocks of size ≥ k = Σ_{j≥k} bj = dim Nk − dim N{k−1},
  - and therefore bj = (dim Nk − dim N{k−1}) − (dim N{k+1} − dim Nk) = 2 dim Nk − dim N{k−1} − dim N{k+1}.
  Practically one computes the sequence dim N1, dim N2, ... until stabilization and reads off block counts.

Practical computation / procedure
1. For each eigenvalue λ:
   a. Compute aλ (algebraic multiplicity) from the characteristic polynomial.
   b. Compute gλ = dim ker(T − λI).
   c. For k = 1, 2, ... compute dim ker((T − λI)^k) until it reaches aλ.
2. Use dim Nk to determine how many Jordan blocks have size ≥ k via dim Nk − dim N{k−1}.
3. Recover the sizes of the Jordan blocks (their multiset) for λ from these counts.
4. Combine the blocks for all eigenvalues; permute blocks arbitrarily to get a Jordan matrix. The result is unique up to block order.

Consequences and checks
- The algebraic multiplicity for λ equals the total of block sizes for λ; the geometric multiplicity equals the number of blocks for λ.
- The exponent of (z − λ) in the minimal polynomial is the size of the largest Jordan block for λ.
- If for every λ we have gλ = aλ then T is diagonalizable (all Jordan blocks are 1×1).
- The Jordan form is canonical in the sense that the partition of aλ into block sizes (for each λ) is uniquely determined by T; only the ordering of blocks is arbitrary.

Section 44 — Minimal Polynomial and Cyclic Decomposition

Definitions and basic facts
- Minimal polynomial. For a linear operator T on a finite-dimensional complex vector space V, the minimal polynomial m_T(x) is the unique monic polynomial of least degree such that m_T(T) = 0. Equivalently, m_T is the monic generator of the ideal {p ∈ C[x] : p(T) = 0}.

- Relationship with characteristic polynomial. m_T divides the characteristic polynomial χ_T, and they have the same distinct linear factors (because over C every eigenvalue λ gives a factor (x − λ) in χ_T, and if λ is an eigenvalue then x − λ divides m_T).

- Cayley–Hamilton. χ_T(T) = 0, so m_T exists and deg m_T ≤ dim V.

How the minimal polynomial encodes Jordan block sizes
- For each eigenvalue λ of T, write the Jordan canonical form of T as a direct sum of Jordan blocks J_k(λ) of various sizes k. For fixed λ, let s_λ be the size of the largest Jordan block with eigenvalue λ. Then the factor of m_T corresponding to λ is (x − λ)^{s_λ}. Thus
  m_T(x) = ∏_{λ} (x − λ)^{s_λ},
where the product runs over the distinct eigenvalues of T.

- Consequence. The exponent of (x − λ) in m_T equals the index of nilpotency of T − λI on the generalized eigenspace for λ: it is the smallest r with (T − λI)^r vanishing on that generalized eigenspace.

Proof idea. On a single Jordan block J_k(λ), (J_k(λ) − λI)^k = 0 but the (k−1)st power is nonzero; therefore the minimal polynomial of that block is (x − λ)^k. For a direct sum of blocks for the same λ, the minimal polynomial is (x − λ)^{max block size}. Combining different eigenvalues multiplies the factors because the corresponding primary components are invariant and pairwise coprime polynomials annihilate those components.

Cyclic subspaces and cyclic (companion) operators
- Cyclic vector and cyclic subspace. A vector v ∈ V is cyclic for T if the cyclic subspace Z(v) = span{v, T v, T^2 v, …} equals V. The restriction of T to a cyclic subspace Z(v) is represented, with respect to the basis {v, T v, …, T^{n-1} v} (where n = dim Z(v)), by the companion matrix of the monic polynomial p_v(x) of degree n that annihilates v: p_v(T)v = 0. That polynomial p_v is the minimal polynomial of T|_{Z(v)} and is called the cyclic (or companion) polynomial for v.

- Companion matrix. The companion matrix of p(x) = x^n + a_{n-1}x^{n-1} + … + a_0 is the n×n matrix that, in the basis above, has the shift form with last row (−a_0, −a_1, …, −a_{n-1}). A linear operator is similar to a companion matrix exactly when it has a cyclic vector (i.e., V is a single cyclic subspace).

Cyclic decomposition theorem (primary/cyclic form)
- Statement (existence). Any linear operator T on a finite-dimensional complex vector space V decomposes V as a direct sum of cyclic T-invariant subspaces:
  V = Z(v_1) ⊕ Z(v_2) ⊕ … ⊕ Z(v_r),
where each Z(v_i) is cyclic with annihilating polynomial p_i(x) (monic), and p_1 divides p_2 divides … divides p_r. Moreover, the product p_1 p_2 … p_r equals the characteristic polynomial χ_T, and p_r = m_T (the minimal polynomial).

- Uniqueness (up to order). The invariant factors p_i (the cyclic annihilators) are uniquely determined by T. They are sometimes called the invariant factor decomposition; their degrees are the sizes of the companion blocks in the rational canonical form. Over C, this gives a canonical decomposition that refines Jordan form.

How to derive structural results and classification up to similarity
- From invariant factors to Jordan form. Each invariant factor p_i factors over C into linear factors (x − λ)^{e_{i,λ}}. Grouping those factors for a fixed eigenvalue λ across the invariant factors yields the sizes of Jordan blocks for λ: the exponents e_{i,λ} record how the largest Jordan block sizes grow. Concretely, the multiplicity and sizes of Jordan blocks for each λ can be read off from the factorization of the invariant factors.

- Minimal polynomial identifies largest block sizes. As above, the exponent of (x − λ) in m_T is the size of the largest Jordan block for eigenvalue λ. Thus m_T provides sharp upper bounds on Jordan block sizes and, together with χ_T (which records total algebraic multiplicities), determines the full Jordan partition for each λ.

- Classification up to similarity. Two operators T and S are similar iff they have the same list of invariant factors (equivalently the same rational canonical form). Over C, this is equivalent to having the same Jordan canonical form — that is, the same eigenvalues with the same Jordan block sizes. The minimal polynomial and characteristic polynomial together determine the invariant factors uniquely: the invariant factors are the monic polynomials whose product is χ_T and whose largest is m_T, with the divisibility chain as above.

Examples and usage
- Single Jordan block. If T is a single Jordan block J_n(λ), then m_T(x) = (x − λ)^n and T is cyclic (any vector with nonzero component in the top generalized eigenspace is cyclic). The companion matrix of (x − λ)^n is similar to J_n(λ).

- Diagonalizable case. If T is diagonalizable, all Jordan blocks are size 1, so m_T(x) = ∏_λ (x − λ). Thus m_T has no repeated factors, and a cyclic decomposition exists with all invariant factors linear.

- Determining Jordan structure from m_T and χ_T. Given χ_T(x) and m_T(x), one proceeds eigenvalue-by-eigenvalue. For a fixed λ, if χ_T has (x − λ)^a and m_T has (x − λ)^s with s ≤ a, then the Jordan blocks for λ are partitions of a with largest part s. The invariant factors provide the refinement needed to pin down multiplicities; if some ambiguity remains from χ_T and m_T alone, compute the sizes of kernels of (T − λI)^k for k = 1,2,… to resolve block counts: dim ker(T − λI)^k increments tell you how many Jordan blocks have size ≥ k.

Practical method for decomposing V
- Find eigenvalues and compute m_T and χ_T (or directly compute nullities of powers of (T − λI)).
- For each λ, compute dimensions d_k(λ) = dim ker(T − λI)^k for k = 1,2,…; the differences d_k − d_{k−1} equal the number of Jordan blocks of size at least k. From these you recover the Jordan partition.
- Construct cyclic vectors for each invariant factor to produce an explicit direct-sum decomposition into companion-block invariant subspaces, yielding a rational (and over C, Jordan) canonical form.

Key takeaways
- The minimal polynomial records the largest Jordan block size for each eigenvalue.
- Cyclic subspaces lead to the invariant factor decomposition (cyclic decomposition) of V, which uniquely classifies T up to similarity.
- Combining m_T and χ_T (or the sequence of nullities of (T − λI)^k) yields the full Jordan structure and thereby the similarity class of T.

Primary decomposition (decomposition into generalized eigenspaces)

Let V be a finite-dimensional complex vector space and T ∈ L(V). Over C the characteristic (hence minimal) polynomial of T splits, so T has finitely many distinct eigenvalues λ1,…,λk. For each eigenvalue λ define the generalized eigenspace
G(λ) := ker((T − λI)^N),
where N = dim V (any exponent ≥ the index of λ will do). Equivalently G(λ) is the set of all v for which (T − λI)^m v = 0 for some m ≥ 1.

The primary decomposition theorem
1. V = G(λ1) ⊕ ··· ⊕ G(λk).
2. Each G(λi) is T-invariant.
3. The restriction Ti := T|G(λi) has λi as its only eigenvalue, and the minimal polynomial of T is the least common multiple of the minimal polynomials of the Ti (in particular each minimal polynomial is a power of (x − λi)).

Proof (sketch).
- Let m1,…,mk be the multiplicities of λ1,…,λk in the minimal polynomial pT(x) of T, so pT(x) = ∏i (x − λi)^{mi}. Set pi(x) := (x − λi)^{mi}. The pi are pairwise relatively prime polynomials.
- By the polynomial functional calculus there exist polynomials ai(x) with ∑i ai(x) pi(x) = 1 (Bézout). Apply this identity to T:
  I = ∑i ai(T) pi(T).
  Because pi(T) annihilates G(λi)⊥? More directly: pi(T) annihilates any vector in G(λi), and ai(T)pi(T) is a projection-like operator onto the complementary part. From I = ∑i ai(T)pi(T) we get that every v ∈ V is a sum of vectors in the kernels ker pi(T) = G(λi), so V = G(λ1) + ··· + G(λk).
- To see the sum is direct, note that the polynomials pi are relatively prime. If v ∈ ∩i G(λi), then pi(T)v = 0 for all i, so pT(T)v = 0, but pT(T) = 0 identically, which alone does not contradict anything. A cleaner direct-sum argument uses the Bézout identity: choose i and write 1 = ai pi + bi with bi divisible by pj for j ≠ i, then apply to v in the intersection to deduce v = 0. Thus the intersection of any distinct subset of the G(λi) is {0}. Hence the sum is direct.
- Each G(λi) is invariant because (T − λiI) maps ker((T − λiI)^N) into itself. Restricting T to G(λi) shows the only eigenvalue that restriction can have is λi: if μ ≠ λi and (T − μI)w = 0 with w ∈ G(λi), then (T − λiI)^N w = 0 and combining these two relations forces w = 0.
- Finally, because each Ti has minimal polynomial a power of (x − λi), the minimal polynomial of T is the lcm of those powers, which is exactly pT.

Consequences and usage
- Reduction to single-eigenvalue blocks: any problem about T (computing powers, exponentials, solving (T − aI)-equations, invariant-subspace questions, matrix representation) can be handled on each G(λi) separately and then combined, because V decomposes as a direct sum of T-invariant subspaces. In any basis adapted to this decomposition the matrix of T is block diagonal, each block corresponding to Ti and having only the single eigenvalue λi.
- Projection operators: the polynomials qi(x) = ai(x) pi(x) from the Bézout identity satisfy qi(T) is the projection of V onto G(λi) along the direct sum of the other generalized eigenspaces. These qi(T) are pairwise orthogonal idempotents (qi(T)qj(T) = 0 for i ≠ j, ∑i qi(T) = I).
- Minimal and characteristic polynomials: the characteristic polynomial factors compatibly as ∏i (x − λi)^{dim G(λi)}, and the minimal polynomial is the lcm of the minimal polynomials of the Ti (hence an ∏i (x − λi)^{mi}).

In practice, to study T you therefore:
- split V into the generalized eigenspaces G(λi),
- solve the problem on each G(λi) (where T − λiI is nilpotent),
- combine the results using the direct-sum decomposition and the polynomial projections qi(T).

Theorem (Upper-triangularization over C)
Let V be a finite-dimensional complex vector space and T ∈ L(V). Then there exists a basis of V with respect to which the matrix of T is upper triangular.

Proof (induction on dim V)
Base n = 1 is trivial. Assume the statement holds for all complex vector spaces of dimension < n and let dim V = n.
1. Since the field is C, T has at least one eigenvalue λ and a nonzero eigenvector v1 with T v1 = λ v1.
2. Consider the quotient space V / span{v1}. The linear map T induces a linear map T̄ on V / span{v1} by T̄( x + span{v1} ) = T x + span{v1}. dim(V / span{v1}) = n − 1, so by the induction hypothesis there is a basis of V / span{v1} whose matrix for T̄ is upper triangular.
3. Lift that basis of the quotient to representatives v2, …, vn in V so that the cosets v2 + span{v1}, …, vn + span{v1} form the chosen basis of V / span{v1}. Then {v1, v2, …, vn} is a basis of V.
4. In this basis the first column of the matrix of T has λ in the (1,1) entry and zeros below it (because T v1 = λ v1), and the action of T on the span of v2,…,vn reduces modulo span{v1} to the upper-triangular matrix of T̄. Combining these facts yields an upper-triangular matrix for T on V.

Thus by induction an upper-triangular matrix for T exists.

How to construct/use such a basis to read spectral data
- Construction recipe:
  - Find an eigenvalue λ1 and a corresponding eigenvector v1.
  - Form the quotient V / span{v1} and find an eigenvector of the induced map there (or continue inductively); lift representatives to get v2, …, vn so that {v1, …, vn} is a basis.
  - In practice one often finds a chain of eigenvectors and extends to a full basis, or repeatedly chooses eigenvectors in successive quotients; this yields an ordered basis giving an upper-triangular matrix.
- Reading spectral data from the diagonal:
  - If A is the matrix of T in an upper-triangular basis, then the diagonal entries a11, a22, …, ann are eigenvalues of T (not necessarily distinct). Each diagonal entry equals the eigenvalue of the corresponding 1×1 quotient action used in the construction.
  - The characteristic polynomial factors as det(tI − A) = (t − a11)(t − a22)···(t − ann). Hence the eigenvalues of T (with algebraic multiplicities) are exactly the diagonal entries of any upper-triangular matrix representation.
  - Trace and determinant: tr T = sum_i aii and det T = ∏_i aii.
  - Geometric multiplicities are not read directly from the diagonal alone, but the diagonal gives the algebraic multiplicities; comparing algebraic and geometric multiplicities requires examining eigenvectors (nullspaces of T − λI).
- Consequences:
  - Over C every operator has a full chain of (generalized) eigenvalues on the diagonal; this is the first step toward Schur or Jordan forms.
  - Any invariant spectral polynomial computations (determinant, trace, characteristic polynomial) can be read off immediately from an upper-triangular matrix.

Multilinear maps — definition and basic consequences

Definition
- Let V1, ..., Vk and W be vector spaces over the same field F. A map
  T : V1 × ... × Vk → W
  is multilinear (or k-linear) if T is linear in each argument separately: for each j (1 ≤ j ≤ k) and for all fixed vectors in the other slots, the map v ↦ T(v1,...,vj,...,vk) is a linear map Vj → W.
- Special cases:
  - k = 1: multilinear = linear.
  - k = 2: bilinear.
  - If V1 = ... = Vk = V, we often speak of k-linear maps on V^k.

Basic examples
- Product of linear functionals: If φ1,...,φk are linear maps Vi → F (functionals when Vi = V), then
  (v1,...,vk) ↦ φ1(v1) · ... · φk(vk)
  is multilinear V1 × ... × Vk → F.
- Composition with a linear map in one slot: if T is multilinear and L: U → Vi is linear, then (v1,...,vi-1,u,vi+1,...,vk) ↦ T(v1,...,L(u),...,vk) is multilinear.
- Matrix bilinear form: For fixed m×n matrix A and vectors x ∈ F^n, y ∈ F^m, the map (x,y) ↦ y^T A x is bilinear F^n × F^m → F.
- Determinant as an n-linear map: For an n-dimensional vector space V, det is an alternating n-linear map det: V^n → F once a basis identification is fixed (see the later treatment of alternating forms).

Space of multilinear maps
- Denote by L(V1,...,Vk; W) the vector space of all multilinear maps from V1 × ... × Vk to W. Pointwise addition and scalar multiplication make this a vector space.
- If W is finite-dimensional and each Vi is finite-dimensional, then L(V1,...,Vk; W) is finite-dimensional.

How multilinearity interacts with bases and coordinates
- Determination by basis values. Let Ei = {e_i1,...,e_ini} be a basis of Vi (dim Vi = ni), and let T ∈ L(V1,...,Vk; W). For any tuple (v1,...,vk) write each vj in coordinates relative to Ej:
  vj = sum_{a=1}^{nj} α_{a}^{(j)} e_{aj}.
  Multilinearity implies the expansion
  T(v1,...,vk) = sum_{a1=1}^{n1} ... sum_{ak=1}^{nk}
                  (α_{a1}^{(1)} · ... · α_{ak}^{(k)}) T(e_{a1}^{(1)}, ..., e_{ak}^{(k)}).
  Thus T is completely determined by its values on the product of the bases E1 × ... × Ek.
- Coordinates and dimension count. Taking W = F, the scalar-valued multilinear maps are determined by the n1·n2·...·nk numbers T(e_{a1}^{(1)},...,e_{ak}^{(k)}). Therefore
  dim L(V1,...,Vk; F) = n1 · n2 · ... · nk.
  For general finite-dimensional W with dim W = m, one gets dim L(V1,...,Vk; W) = m · n1 · ... · nk.
- Expansion formula (componentwise): If W has a basis {w1,...,wm} and T(e_{a1}^{(1)},...,e_{ak}^{(k)}) = sum_{t=1}^m c_{a1,...,ak}^{(t)} wt, then for arbitrary inputs the same coefficient sums (with coordinate products) give the coordinates of T(v1,...,vk) in that basis of W.

Constructions and linear algebra operations
- Fixing arguments (partial evaluation). Fix all slots of a multilinear map T except the j-th; the resulting map is linear in the j-th slot. This gives linear maps from Vi to W (or to L of the remaining slots) and is how we build and reason about multilinear maps inductively.
- Tensor product viewpoint (preview). Pure tensors φ1 ⊗ ... ⊗ φk (with φj ∈ Vj*) act on (v1,...,vk) by φ1(v1)...φk(vk); linear combinations of pure tensors produce all multilinear forms and give an isomorphic description of L(V1,...,Vk; F) as (V1* ⊗ ... ⊗ Vk*).
- Pullback by linear maps. If T ∈ L(V1,...,Vk; W) and for each j we have linear Sj : Uj → Vj, then T ∘ (S1,...,Sk) ∈ L(U1,...,Uk; W). In coordinates, the values on basis tuples transform by multiplying coordinate matrices of the Sj in each slot.

Alternating and symmetric multilinear maps (brief)
- Alternating multilinear map: T is alternating if T(v1,...,vk) = 0 whenever two arguments are equal. Equivalently, swapping two arguments changes sign (for fields of characteristic ≠ 2, the sign rule characterizes alternation). For k = n = dim V, alternating n-linear scalar-valued forms are determined (up to scalars) by their value on any ordered basis; this is the structural fact behind the determinant.
- Symmetric multilinear map: T invariant under permutations of the arguments.

Uniqueness and reconstruction
- Given bases of the domain spaces and a basis of W, prescribing arbitrary values at the basis tuples uniquely extends (by the multilinear expansion) to a multilinear map on the whole product. This is the practical tool used repeatedly: to define a multilinear map, it suffices to specify its values on the finitely many basis-tuple inputs.

Key formula to remember
- If e_{aj}^{(j)} are the basis vectors of Vj and vj = sum_a α_{a}^{(j)} e_{aj}^{(j)}, then for T ∈ L(V1,...,Vk; W),
  T(v1,...,vk) = sum_{a1,...,ak} (α_{a1}^{(1)} · ... · α_{ak}^{(k)}) T(e_{a1}^{(1)},...,e_{ak}^{(k)}).

This section sets up the language and basic manipulations of multilinear maps: how to build them, how to compute with coordinates, and how special properties like alternation restrict their values on basis tuples (a fact exploited in the theory of determinants).

Alternating multilinear forms and the exterior algebra

Definitions and first properties
- Let V be a finite-dimensional vector space over field F. A k-multilinear form on V is a multilinear map ω: V^k → F. It is alternating if ω(v1,...,vk) = 0 whenever two arguments are equal. Equivalently, ω changes sign under any transposition of two arguments:
  ω(..., vi,..., vj, ...) = −ω(..., vj,..., vi, ...).
- Consequences:
  - Alternation implies total skew-symmetry: swapping any two entries multiplies the value by −1, so for a permutation σ of {1,...,k},
    ω(v_{σ(1)},...,v_{σ(k)}) = sgn(σ) ω(v1,...,vk).
  - An alternating k-form vanishes on any k-tuple that is linearly dependent (because some coordinate repeated in a dependence can be used to show cancellation).
- Notation: The space of alternating k-forms (k-covectors) on V is denoted Λ^k(V*). By convention Λ^0(V*) = F and Λ^1(V*) = V*.

Wedge product and construction of exterior powers
- The wedge product is the bilinear product
  ∧ : Λ^k(V*) × Λ^l(V*) → Λ^{k+l}(V*),
  designed to combine alternating forms into higher-degree alternating forms.
- Construction (standard one): for φ ∈ Λ^k(V*), ψ ∈ Λ^l(V*), form the (k+l)-multilinear map φ ⊗ ψ given by
  (φ ⊗ ψ)(v1,...,v_{k+l}) = φ(v1,...,vk) · ψ(v_{k+1},...,v_{k+l}).
  Then alternate it to make it skew-symmetric:
  φ ∧ ψ := Alt(φ ⊗ ψ) = 1/(k! l!) ∑_{σ∈S_{k+l}} sgn(σ) (φ ⊗ ψ)∘σ,
  equivalently φ ∧ ψ = (k+l)!/(k! l!) Alt(φ ⊗ ψ) in the convention that Alt averages with 1/(k+l)!.
- Key algebraic properties of ∧:
  - Bilinearity in each argument.
  - Graded anticommutativity: for φ ∈ Λ^k(V*), ψ ∈ Λ^l(V*),
    φ ∧ ψ = (−1)^{kl} ψ ∧ φ.
  - Associativity: (φ ∧ ψ) ∧ θ = φ ∧ (ψ ∧ θ) (so we drop parentheses).
  - If φ and ψ have overlapping dependence (e.g. they involve the same 1-form factor), exterior product can be zero; in particular φ∧φ = 0 for odd-degree φ.
- Basis and dimension:
  - If {e1,...,en} is a basis of V and {e^1,...,e^n} the dual basis of V*, then the wedge products e^{i1} ∧ ... ∧ e^{ik} with i1 < ... < ik form a basis of Λ^k(V*). Thus dim Λ^k(V*) = C(n,k).
- Exterior powers of V:
  - One can dually define Λ^k(V) (kth exterior power of V) as the vector space generated by formal wedges v1 ∧ ... ∧ vk subject to multilinearity and alternating relations (v∧v = 0, and anticommutation under swaps). Λ^k(V) is dual to Λ^k(V*) when V is finite-dimensional.

Functoriality and induced maps
- Any linear map T: V → W induces linear maps on exterior powers:
  - On forms: T^*: Λ^k(W*) → Λ^k(V*) by (T^*φ)(v1,...,vk) = φ(Tv1,...,Tvk).
  - On vectors: Λ^k(T): Λ^k(V) → Λ^k(W) by Λ^k(T)(v1 ∧ ... ∧ vk) = Tv1 ∧ ... ∧ Tvk.
- These induced maps respect the wedge product (they are algebra homomorphisms in the graded sense) and compose compatibly: Λ^k(S∘T) = Λ^k(S) ∘ Λ^k(T).

Top exterior power, determinants, and oriented volume
- If dim V = n, the top exterior power Λ^n(V*) is 1-dimensional. Choose a nonzero top form ω ∈ Λ^n(V*). For any ordered n-tuple (v1,...,vn) define the scalar ω(v1,...,vn). Because Λ^n(V*) is 1-dimensional, any linear operator T: V → V acts on Λ^n(V*) by scalar multiplication:
  Λ^n(T): Λ^n(V*) → Λ^n(V*), Λ^n(T)(ω) = (det T) ω,
  and this scalar is the determinant det T. That is, det T is the unique scalar such that
  ω(Tv1,...,Tvn) = (det T) ω(v1,...,vn) for all v1,...,vn.
- This gives determinant coordinate-free characterizations and the usual properties follow immediately:
  - det(S∘T) = det S · det T (functoriality on top exterior power).
  - det I = 1, det is multilinear in columns when expressed in a basis, and det changes sign under swapping two columns (because of alternation).
- Oriented volume:
  - Fix a top form ω and normalize it (choose ω so that ω(e1,...,en) = 1 for some basis). Then |ω(v1,...,vn)| is the volume of the parallelepiped spanned by v1,...,vn relative to that orientation and unit choice. The sign of ω(v1,...,vn) encodes orientation: positive means the ordered basis (v1,...,vn) is positively oriented relative to ω.
  - Under a linear transformation T, volumes scale by |det T| and orientations by sgn(det T).

Sketch of proofs of the crucial facts
- Alternation implies skew-symmetry: a transposition τ can be written in terms of swapping two equal entries in a family of evaluations; multilinearity forces the sign change.
- Basis of Λ^k(V*): any alternating k-form is determined by its values on basis k-tuples; alternation forces zero when indices repeat and sign changes under permutation, so independent values correspond exactly to choices on strictly increasing index k-tuples.
- Wedge product produces an alternating form: alternating the tensor product yields a skew-symmetric (k+l)-form; the combinatorial factor ensures that for decomposable inputs (simple wedges) the wedge matches the expected antisymmetrized product.
- Determinant from top exterior power: since Λ^n(V*) is 1-dim, any linear endomorphism acts by multiplication by some scalar; define det T to be that scalar. Checking the usual column-multilinearity and sign rules is immediate from the behavior of Λ^n(T) on decomposable wedges.

Takeaway (operational rules)
- To check a k-form is alternating, it suffices to check it vanishes when two arguments are equal or that it changes sign on a single transposition.
- Compute wedge products by antisymmetrizing tensor products; for decomposable 1-forms α1,...,αk and β1,...,βl,
  (α1 ∧ ... ∧ αk) ∧ (β1 ∧ ... ∧ βl) = α1 ∧ ... ∧ αk ∧ β1 ∧ ... ∧ βl,
  up to the sign rules when reordering factors.
- Determinant = scalar by which a linear map scales the top exterior power; oriented volume = value of a chosen top form on an ordered basis of vectors.

This completes the treatment of alternating forms, the wedge product, exterior powers, and their role in defining determinant and oriented volume.

Section: Determinant via alternating multilinear forms

Setup. Let V be an n-dimensional vector space over a field F and fix an ordered basis b = (b1,...,bn). Write L(V) for the space of linear maps V → V. Let Alt(V) denote the vector space of n-multilinear alternating maps V^n → F. (Alternating means the value changes sign under a transposition of two arguments, equivalently any repeated argument gives 0; multilinear means linear in each argument separately.)

Existence and uniqueness of a normalization. It is a standard fact (proof omitted here) that dim Alt(V) = 1. Hence there is a unique φ ∈ Alt(V) such that φ(b1,...,bn) = 1. Call this φ the normalized alternating form with respect to the basis b.

Definition (determinant of a linear map). For T ∈ L(V) define
det(T) := φ(Tb1, ..., Tbn),
where φ is the normalized alternating form determined by the chosen basis b.

This gives a well-defined scalar in F. Because Alt(V) is 1-dimensional and φ was normalized on the basis, det(T) does not depend on any choice other than the ordered basis b used to normalize φ; changing the normalization basis changes φ by its value on the new basis, and the resulting definition changes accordingly (this is the usual coordinate dependence of the matrix determinant).

Core properties

1) Multilinearity and alternating behavior in columns (or rows).
Consider T as determined by its action on basis vectors. If we view the arguments of φ as the columns of the matrix of T in the basis b, φ is multilinear in each column and alternating in the columns. Thus for fixed T, det(T) is multilinear in the columns of the matrix of T and changes sign if any two columns are swapped; and if two columns are equal then det(T)=0. These properties follow immediately from φ being multilinear and alternating.

2) Effect of elementary column operations (equivalently row operations after transposition).
Because det(T) is multilinear and alternating in the columns:

- Scaling a single column by α ∈ F scales det(T) by α.
- Adding α times one column to another leaves det(T) unchanged (multilinearity + alternating implies linear dependence of the increment does not change the alternating value).
- Swapping two columns multiplies det(T) by −1.
- If columns are linearly dependent then det(T)=0 (alternating implies zero whenever arguments are linearly dependent).

These are direct consequences of multilinearity and the alternating property.

3) Multiplicativity: det(ST) = det(S) · det(T).
Let S,T ∈ L(V). Fix the normalized φ. Consider the alternating n-form ψ defined by
ψ(v1,...,vn) := φ(Sv1, ..., Svn).
Since composition of a multilinear alternating form with a linear map in each argument produces another alternating multilinear form, ψ ∈ Alt(V). Because Alt(V) is 1-dimensional, ψ must be a scalar multiple of φ: there exists α ∈ F with ψ = αφ. Evaluating both sides on the ordered basis b gives
α = ψ(b1,...,bn) = φ(Sb1,...,Sbn) = det(S).
Thus φ(STv1,...,STvn) = ψ(Tv1,...,Tvn) = det(S) · φ(Tv1,...,Tvn).
Evaluating at v1=b1,...,vn=bn gives
det(ST) = det(S) · det(T).
So determinant is multiplicative under composition.

4) Determinant of the identity and determinant of inverses.
Applying multiplicativity with S = I gives det(I) = 1 (since φ(Ib1,...,Ibn) = φ(b1,...,bn) = 1). If T is invertible then 1 = det(I) = det(TT^{-1}) = det(T)det(T^{-1}), so det(T^{-1}) = det(T)^{-1}. Thus det(T) ≠ 0 for invertible T.

5) Determinant detects invertibility.
If T is not injective then Tb1,...,Tbn are linearly dependent, so det(T) = φ(Tb1,...,Tbn) = 0 by the alternating property. Conversely, if det(T) = 0 then φ(Tb1,...,Tbn) = 0, hence the n-tuple Tb1,...,Tbn is linearly dependent, so T fails to be surjective and hence is not invertible (on a finite-dimensional space injective ⇔ surjective ⇔ invertible). Therefore T is invertible ⇔ det(T) ≠ 0.

Remarks tying to matrices. With respect to the chosen ordered basis b, T corresponds to an n×n matrix M. The scalar det(T) defined above equals the usual determinant of M (the unique alternating multilinear function of the columns normalized to be 1 on the identity matrix). The properties above translate to the familiar row/column operations and multiplicativity det(AB)=det(A)det(B) for matrices.

Summary of key consequences
- Determinant is the unique alternating multilinear scalar-valued function on n vectors normalized to 1 on the basis.
- It is multilinear in columns (or rows), alternating (repeats give 0, swaps change sign).
- Elementary column/row operations have the usual effect on determinant (scale, add multiple, swap).
- Multiplicative: det(ST)=det(S)det(T).
- A linear map (or matrix) is invertible iff its determinant is nonzero.

Change of basis, orientation, and volume interpretation

- Determinant as a volume-scaling factor
  - For a linear map T: V → V on an n-dimensional real vector space, det(T) measures how T scales n-dimensional volume. Concretely, if you take the parallelepiped spanned by n vectors v1,...,vn, its oriented volume is given (relative to some chosen ordered basis) by the determinant of the matrix whose columns are the coordinates of the vi. Applying T sends that parallelepiped to the one spanned by T(v1),...,T(vn), and the oriented volume is multiplied by det(T):
    Vol_oriented(T(v1),...,T(vn)) = det(T) · Vol_oriented(v1,...,vn).
  - In particular, the image of the unit cube has oriented volume det(T); its absolute value |det(T)| is the ordinary (unsigned) volume scale factor and det(T) < 0 indicates an orientation reversal.

- Determinant and change of basis
  - The determinant of a linear operator is intrinsic to the operator, independent of the choice of basis. If A is the matrix of T in one ordered basis and A' is the matrix of T in another ordered basis, then A' = P^{-1} A P for some invertible change-of-basis matrix P, and
    det(A') = det(P^{-1} A P) = det(P^{-1}) det(A) det(P) = det(A).
    So det(T) is well defined as a scalar attached to T, not to any particular matrix representation.
  - However, if you fix a multilinear alternating n-form (a "volume form") ω and change the ordered basis used to evaluate ω, the numerical value of ω on the new basis is multiplied by det(P). If e1,...,en is an ordered basis and e' = Pe (i.e., e'i = sum_j P_{ji} ej), then
    ω(e'1,...,e'n) = det(P) · ω(e1,...,en).
    This is the transformation rule for n-forms under basis change.

- Orientation
  - Orientation partitions ordered bases into two classes: two ordered bases are equivalent (same orientation) exactly when the transition matrix between them has positive determinant. That common-sense “handedness” is captured algebraically by det.
  - A nonzero alternating n-form (a volume form) picks one of these two classes as “positive”: those ordered bases on which the form takes a positive value. Multiplying the form by −1 swaps the two orientations.
  - Thus det(T) > 0 means T preserves orientation (it sends a positively oriented basis to a positively oriented one), det(T) < 0 means T reverses orientation.

- Geometric consequences and examples
  - Composition: determinants multiply under composition, so successive linear maps scale volume by the product of their dets. This is why the Jacobian determinant appears in change-of-variables formulas for integrals.
  - Invertibility: T is invertible ⇔ det(T) ≠ 0; geometrically, a zero determinant means T collapses some n-volume to zero (the image has lower dimension).
  - Example in R^2: a matrix diag(a,b) scales areas by ab; a shear with matrix [[1,s],[0,1]] has det 1 and preserves area but changes shape; a reflection has determinant −1 and reverses orientation while preserving area magnitude.

- Summary picture
  - The determinant gives the signed scale factor by which an n-dimensional linear map multiplies oriented n-volumes; it is basis-independent for linear maps but controls how coordinates and volume forms change under basis transformations. Orientation is the sign (positive/negative) information carried by determinants, distinguishing the two possible “handedness” choices for ordered bases.

Determinant, characteristic polynomial, and eigenvalues (finite-dimensional)

- Characteristic polynomial. For a linear operator T on an n-dimensional vector space V over a field F, the characteristic polynomial is
  p_T(λ) = det(λI − T).
  (Some authors use det(T − λI); these differ by a factor (−1)^n.) p_T(λ) is a monic polynomial of degree n whose roots (in an algebraic closure of F) are exactly the eigenvalues of T, with algebraic multiplicities.

- Eigenvalues as roots. λ0 is an eigenvalue of T ⇔ p_T(λ0) = 0. Thus every eigenvalue appears as a root of p_T, and conversely every root of p_T (counted with multiplicity) is an eigenvalue.

- Determinant as product of eigenvalues. Over an algebraically closed field (or after extending scalars), if the eigenvalues of T (counting algebraic multiplicity) are λ1, …, λn, then
  det T = λ1 · λ2 · … · λn.
  Equivalently, if p_T(λ) = λ^n + a_{n−1} λ^{n−1} + … + a_1 λ + a_0, then a_0 = (−1)^n det T when using p_T(λ) = det(λI − T). Thus the constant term of the characteristic polynomial (up to sign) equals det T.

- Short justification. Choose a basis in which the matrix of T is upper triangular (this exists over an algebraically closed field by the Schur triangularization or, more elementarily, by induction using eigenvectors). The diagonal entries are the eigenvalues (with multiplicity), and the determinant equals the product of the diagonal entries, giving the product formula. Because similarity preserves eigenvalues and determinant, the relation holds for any matrix representation.

- Consequences and interactions with spectral results
  - Invertibility: T is invertible ⇔ det T ≠ 0 ⇔ 0 is not an eigenvalue of T. If 0 is an eigenvalue then it appears among λ1,…,λn, so the product is zero.
  - Multiplicity bookkeeping: The algebraic multiplicities of eigenvalues sum to n, and the product of eigenvalues counting algebraic multiplicity yields det T. Geometric multiplicity (dimension of eigenspaces) does not affect the determinant beyond how it relates to algebraic multiplicity.
  - Diagonalizable case: If T is diagonalizable with diagonal entries its eigenvalues, the determinant is immediately the product of those diagonal entries. If T is not diagonalizable, triangularization still gives the same product formula.
  - Similarity invariance: det(T) and p_T(λ) are invariant under similarity; thus the product-of-eigenvalues relation is a similarity-invariant spectral statement.

- Practical notes
  - When working over a field that is not algebraically closed, interpret “product of eigenvalues” by passing to an algebraic closure or by saying “product of roots of p_T counted with multiplicity.”
  - For computational uses, det(T − λI) expands to a polynomial whose coefficients encode symmetric polynomials in the eigenvalues; in particular the trace equals the sum of eigenvalues (coefficient of λ^{n−1} with sign) and the determinant equals the product (constant term with sign).

This ties the determinant, the characteristic polynomial, and the spectrum together: the characteristic polynomial encodes the eigenvalues, and its constant term (up to sign) is the determinant, so the determinant equals the product of eigenvalues counted with algebraic multiplicity.

Section: Tensor Products and the Universal Property

Goal. Given vector spaces V1, ..., Vn over the same field F, we want a vector space T and a multilinear map τ : V1 × ··· × Vn → T with the property that every multilinear map φ : V1 × ··· × Vn → W into any vector space W factors uniquely through τ by a linear map L : T → W. Equivalently, T is the object that "represents" the functor sending W to the space of multilinear maps into W. We call such a T a tensor product of V1, …, Vn and write T = V1 ⊗ ··· ⊗ Vn.

Concrete construction. Let M be the free vector space (over F) having as a basis the set of formal symbols [v1, ..., vn] for all tuples (v1, ..., vn) ∈ V1 × ··· × Vn. Concretely, elements of M are finite linear combinations ∑ αi [vi1, ..., vin]. Let R be the subspace of M spanned by all elements enforcing multilinearity:
- For each j (1 ≤ j ≤ n), for all v1, …, vj, vj' ∈ Vj and scalar a ∈ F,
  - [v1, …, vj + vj', …, vn] − [v1, …, vj, …, vn] − [v1, …, vj', …, vn] ∈ R,
  - [v1, …, a vj, …, vn] − a [v1, …, vj, …, vn] ∈ R.
Define the tensor product space as the quotient
  T := M / R,
and denote the coset of [v1, …, vn] in T by v1 ⊗ ··· ⊗ vn. By construction the map
  τ : V1 × ··· × Vn → T,  (v1, …, vn) ↦ v1 ⊗ ··· ⊗ vn
is multilinear (the relations in R force additivity and homogeneity in each slot).

Universal property (existence). Let W be any vector space and let φ : V1 × ··· × Vn → W be a multilinear map. Define Φ0 on the basis symbols by Φ0([v1, …, vn]) := φ(v1, …, vn) and extend linearly to a linear map Φ : M → W. Because φ is multilinear, every generator of R is sent to 0, so R ⊆ ker Φ. Hence Φ descends to a well-defined linear map L : T → W with L(v1 ⊗ ··· ⊗ vn) = φ(v1, …, vn). Thus φ = L ◦ τ. This shows every multilinear map factors through τ.

Uniqueness part of universal property. Suppose T' is another vector space and τ' : V1 × ··· × Vn → T' is multilinear and has the property that every multilinear φ factors uniquely through τ'. Take φ = τ : there exists a linear map F : T' → T with F ◦ τ' = τ. Similarly, there exists G : T → T' with G ◦ τ = τ'. Then G ◦ F and F ◦ G are linear maps from T' to T' and from T to T respectively that, when postcomposed with τ' or τ, give τ' or τ. By uniqueness of factorization these composites must be the identities on T' and T, so F and G are inverse isomorphisms. Hence any two tensor products are uniquely isomorphic in the evident way; the tensor product is determined up to unique isomorphism by the universal property.

Correspondence between multilinear maps and linear maps out of the tensor product. The construction above gives a natural bijection between
  Lin(T, W) and Multilin(V1 × ··· × Vn; W),
where Lin(T, W) denotes the space of linear maps T → W and Multilin(…; W) denotes the space of n-multilinear maps into W. Explicitly:
- Given a linear map L : T → W define φ := L ◦ τ; then φ is multilinear.
- Given a multilinear φ : V1 × ··· × Vn → W the universal property provides a unique linear map L : T → W with φ = L ◦ τ.

These assignments are linear in W (i.e., they identify the vector space Multilin(V1 × ··· × Vn; W) with Lin(T, W)), and they are natural in W: for a linear map S : W → W' postcomposition with S commutes with the correspondence.

Remarks and immediate consequences.
- Symbols v1 ⊗ ··· ⊗ vn span T (by definition), and relations in R enforce multilinearity. In particular, if some vj = 0 then v1 ⊗ ··· ⊗ vn = 0.
- When n = 2 we write V ⊗ W for V1 ⊗ V2; the same universal property characterizes the bilinear-to-linear correspondence: Bilin(V × W; X) ≅ Lin(V ⊗ W, X).
- The universal property is the defining feature: any construction that provides a space T and multilinear τ with the stated factoring property yields a tensor product isomorphic (uniquely) to the quotient construction given above.

This completes the construction of the tensor product as the representing object for multilinear maps and the proof that multilinear maps from V1 × ··· × Vn to any W correspond exactly to linear maps from V1 ⊗ ··· ⊗ Vn to W.