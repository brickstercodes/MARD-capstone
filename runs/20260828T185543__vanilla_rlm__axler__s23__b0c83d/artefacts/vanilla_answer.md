1. Vector spaces

1.1 Notation: list of vectors
Definition/statement:
- A “list” of vectors means an ordered finite sequence, often written (v1, v2, ..., vm) or v1, v2, …, vm. Lists may have repeated vectors and order matters for some arguments (e.g., matrices of linear maps relative to a basis).

Intuition:
- Think of a list as a finite ordered batch of vectors you will combine, test for independence, or use as a candidate basis.

Example:
- ( (1,0), (0,1) ) is a list in R^2. The list ( (1,0), (1,0) ) is allowed but has repetition.

Pitfalls/checks:
- Don’t confuse “list” with “set”: sets ignore order and multiplicity. Many theorems assume lists are finite. If a result refers to “length of a list,” count repeats.

1.2 Vector space / field of scalars
Definition/statement:
- A vector space V over a field F is a set with addition and scalar multiplication satisfying the usual axioms (associativity, commutativity of addition, distributivity, existence of additive identity 0 and additive inverses, multiplicative identity acting correctly, etc.). The field F supplies scalars.

Intuition:
- Vectors are objects you can add and scale. The field F determines what scalars you may use (e.g., R or C).

Example:
- R^n is a vector space over R. The set of polynomials with real coefficients is a vector space over R.

Pitfalls/checks:
- Ensure scalar operations come from a field (commonly R or C). Mixed-scalar arithmetic (treating V as over R vs over C) changes properties (e.g., complex structure matters).

1.3 Subspace (definition) and basic tests for subspaces
Definition/statement:
- A subset U ⊆ V is a subspace if it is itself a vector space under the same operations. Equivalently, U is nonempty and closed under vector addition and scalar multiplication.

Intuition:
- Subspaces are “linear pieces” of V that you can treat like smaller vector spaces.

Example:
- In R^3, the set {(x,y,0)} is a subspace. The set {(x,y,1)} is not (no zero vector).

Pitfalls/checks:
- Check that 0 ∈ U. Don’t forget closure under scalars for all scalars in F (not just integers). A nonempty set closed under linear combinations of two elements is a good quick test for subspace.

1.4 Linear combination
Definition/statement:
- A linear combination of vectors v1,...,vm is any vector of the form a1 v1 + ... + am vm with scalars a1,...,am ∈ F.

Intuition:
- Linear combinations are how you build new vectors from old ones using scaling and addition.

Example:
- In R^2, (2,3) is 2*(1,1) + 1*(0,1).

Pitfalls/checks:
- Distinguish finite linear combinations (lists) from infinite sums (not allowed unless topology given). Coefficients matter: trivial combination has all coefficients zero.

1.5 Span
Definition/statement:
- span(v1,...,vm) is the set of all linear combinations of the list v1,...,vm. It is a subspace of V.

Intuition:
- The span is everything you can reach using the given vectors with scalars — the “linear span” or linear hull.

Example:
- span((1,0),(0,1)) = R^2. span((1,1)) is the line {t(1,1)}.

Pitfalls/checks:
- If span equals V, the list spans V. If a vector is outside the span, no linear combination of the given vectors produces it.

1.6 Span is the smallest containing subspace
Definition/statement:
- span(S) is the intersection of all subspaces containing S; equivalently, it is the smallest subspace that contains S.

Intuition:
- Span collects all needed linear combinations but nothing extra.

Example:
- For S = {(1,0)} in R^2, span(S) is the x-axis; any subspace containing (1,0) must contain that entire axis.

Pitfalls/checks:
- To show a subspace W equals span(S), show S ⊆ W and that W is contained in every subspace containing S (or just show W is a subspace containing S and compare dimensions).

1.7 Sum of subspaces
Definition/statement:
- For subspaces U and W, U + W = {u + w : u ∈ U, w ∈ W}. This is a subspace containing both U and W.

Intuition:
- U + W is the smallest subspace containing U ∪ W — all linear combinations of elements from U and W.

Example:
- In R^2, let U = x-axis and W = y-axis; then U + W = R^2.

Pitfalls/checks:
- U + W is not the same as the union U ∪ W unless one subspace contains the other.

1.8 Intersection of subspaces (finite and arbitrary)
Definition/statement:
- The intersection ∩α Uα of any collection of subspaces is a subspace (possibly {0}). Finite intersection is a special case.

Intuition:
- Intersection keeps only vectors common to all subspaces.

Example:
- In R^2, intersection of x-axis and y-axis is {0}.

Pitfalls/checks:
- Intersection could be trivial even if individual subspaces are large. Intersection of infinitely many subspaces can be small.

1.9 Union of subspaces: necessary and sufficient conditions
Definition/statement:
- The union U ∪ W of subspaces is a subspace iff one subspace is contained in the other. For more than two subspaces, the union is rarely a subspace.

Intuition:
- A union need not be closed under addition: adding one vector from U and one from W might not lie in either.

Example:
- In R^2, union of x-axis and y-axis is not a subspace (sum of (1,0) and (0,1) is (1,1) not in union). If W = U, union is U.

Pitfalls/checks:
- Test union closure: pick vectors from different summands — if their sum fails to lie in the union, union is not a subspace.

1.10 Product (Cartesian product) of vector spaces
Definition/statement:
- V × W consists of pairs (v,w) with componentwise addition and scalar multiplication; V × W is a vector space over the same field.

Intuition:
- Think of ordered pairs as concatenated vectors — coordinates live in different factors.

Example:
- R^2 × R^3 ≅ R^5; operations act coordinatewise.

Pitfalls/checks:
- Dimension adds: dim(V × W) = dim V + dim W when finite-dimensional.

1.11 Direct sum (V1 ⊕ ⋯ ⊕ Vm) and direct-sum notation
Definition/statement:
- The direct sum V1 ⊕ ⋯ ⊕ Vm denotes the internal sum when every element of the sum V1 + ⋯ + Vm has a unique decomposition as v1 + ⋯ + vm with vi ∈ Vi. Equivalently, the sum is the whole space and summands intersect appropriately.

Intuition:
- Direct sum is like putting vector spaces side by side so coordinates are uniquely determined per summand.

Example:
- R^2 = x-axis ⊕ y-axis. Each vector (x,y) = (x,0) + (0,y) uniquely.

Pitfalls/checks:
- Uniqueness is crucial: if uniqueness fails, it’s a sum but not a direct sum.

1.12 Uniqueness characterization of direct sum (zero-representation test)
Definition/statement:
- V = V1 ⊕ ⋯ ⊕ Vm iff the only way to write 0 as v1 + ⋯ + vm with vi ∈ Vi is all vi = 0. This is the zero-representation test for uniqueness.

Intuition:
- If nontrivial combination gives 0, decompositions are not unique.

Example:
- For x-axis and y-axis in R^2, only (0,0) = (0,0)+(0,0).

Pitfalls/checks:
- Use this test to verify directness: check that no nonzero combination from different summands sums to zero.

1.13 Two-subspace direct-sum criterion (U + W direct ⇔ U ∩ W = {0})
Definition/statement:
- For two subspaces U and W, U ⊕ W is equivalent to U + W = V and U ∩ W = {0}. For internal direct sum of only those two, uniqueness ⇔ intersection trivial.

Intuition:
- No overlap means coordinates from each subspace are determined independently.

Example:
- In R^3, span{(1,0,0)} ⊕ span{(0,1,0)} ⊕ span{(0,0,1)} (three coordinate axes pairwise intersections are {0} and sum is whole space).

Pitfalls/checks:
- For two subspaces, trivial intersection suffices. For more than two summands, pairwise trivial intersections alone are not enough (see next item).

1.14 Warning: pairwise zero intersections insufficient for >2 summands
Definition/statement:
- For three or more subspaces, pairwise intersections being {0} does not guarantee their sum is a direct sum; there can be nontrivial representations of 0 using vectors from different summands.

Intuition:
- Overlaps among triples can create cancellation even if pairwise intersections are trivial.

Example:
- In R^2, let V1 = span{(1,0)}, V2 = span{(1,1)}, V3 = span{(0,1)}. Pairwise intersections are {0} but V1 + V2 + V3 is not a direct sum because (1,0) + (0,1) = (1,1).

Pitfalls/checks:
- For m > 2, use the zero-representation test: check that only trivial combination gives zero.

1.15 Decompositions into multiple direct-sum summands and complements
Definition/statement:
- Given a subspace U of finite-dimensional V, there exists a complementary subspace W such that V = U ⊕ W. More generally, V can be decomposed as a direct sum of multiple summands when appropriate.

Intuition:
- Complement picks “the rest” of the space so every vector splits uniquely into a U-part and a W-part.

Example:
- In R^3, U = span{(1,0,0)} has many complements, e.g., W = span{(0,1,0),(0,0,1)}.

Pitfalls/checks:
- Complement is not unique. To find one, extend a basis of U to a basis of V; remaining basis vectors span a complement.

1.16 Examples: coordinate-axis direct-sum decomposition (F^n) and even/odd decomposition
Definition/statement:
- Coordinate axes decomposition: F^n = span(e1) ⊕ ··· ⊕ span(en). Even/odd decomposition: space of functions or polynomials can split into even and odd parts, giving a direct sum.

Intuition:
- Coordinates isolate each dimension; parity splits functions into symmetric and antisymmetric parts.

Example:
- Any vector in R^3 = (x,y,z) decomposes uniquely as (x,0,0)+(0,y,0)+(0,0,z). For polynomials, any p(x) = p_even(x) + p_odd(x).

Pitfalls/checks:
- When forming sums, check uniqueness of components; using standard basis often simplifies checks.

2. Finite-dimensional spaces

2.1 Finite-dimensional vector space (definition) and examples
Definition/statement:
- V is finite-dimensional if it has a finite spanning list. The smallest length of a spanning list equals the dimension if a basis exists; otherwise infinite-dimensional.

Intuition:
- Finite-dimensional means you can describe every vector using finitely many coordinates.

Example:
- R^n, P_m(F) (polynomials of degree ≤ m) are finite-dimensional.

Pitfalls/checks:
- Existence of a finite spanning list is the test. Some familiar spaces (all polynomials) are infinite-dimensional.

2.2 Polynomial spaces P(F) and P_m(F)
Definition/statement:
- P(F) is the vector space of all polynomials with coefficients in F. P_m(F) is the subspace of polynomials of degree ≤ m.

Intuition:
- P_m(F) behaves like F^{m+1} via coefficient vectors.

Example:
- Basis for P_2(R) is {1, x, x^2}. dim P_m(F) = m+1.

Pitfalls/checks:
- Beware: P(F) (all polynomials) is infinite-dimensional. Degree conventions and zero polynomial handling matter.

2.3 Infinite-dimensional vector spaces (examples)
Definition/statement:
- Spaces without finite spanning lists are infinite-dimensional.

Intuition:
- You cannot capture all elements with finitely many parameters.

Example:
- P(R), the space of all polynomials, and the space of all sequences of real numbers.

Pitfalls/checks:
- A subspace of infinite-dimensional may be finite-dimensional or infinite; check whether a finite spanning list exists.

2.4 Linear independence (definition)
Definition/statement:
- A list v1,...,vm is linearly independent if the only scalars a1,...,am with a1 v1 + ... + am vm = 0 are all zeros.

Intuition:
- No vector in the list can be made from the others.

Example:
- ( (1,0), (0,1) ) in R^2 is independent. ( (1,0), (2,0) ) is dependent.

Pitfalls/checks:
- Order not important for independence but length is. If any vector equals a linear combination of earlier ones, the whole list is dependent.

2.5 Linear dependence (definition)
Definition/statement:
- A list is linearly dependent if there exists a nontrivial linear combination equal to 0 (some scalar not zero).

Intuition:
- There is redundancy in the list.

Example:
- ( (1,0), (1,1), (0,1) ) is dependent because (1,0) + (0,1) − (1,1) = 0.

Pitfalls/checks:
- If list contains the zero vector, it is automatically dependent.

2.6 Simple criteria/examples for small lists
Definition/statement:
- For a 1-list, independent iff nonzero. For a 2-list v,w: independent iff w is not a scalar multiple of v.

Intuition:
- In low dimensions, dependence is easy to check geometrically.

Example:
- In R^2, two non-collinear vectors are independent.

Pitfalls/checks:
- For more vectors, use row-reduction/coefficient tests or the linear dependence lemma.

2.7 Linear Dependence Lemma
Definition/statement:
- If a list v1,...,vm is linearly dependent, then some vi is a linear combination of preceding vectors. Removing such vi yields a spanning list for the same span.

Intuition:
- You can eliminate redundant vectors from the list without shrinking the span.

Example:
- From (v1,v2,v3) dependent, maybe v2 = a v1 + b v3; one of them can be removed.

Pitfalls/checks:
- The lemma is used to trim spanning lists to bases; track order so “preceding” is meaningful.

2.8 Bound: length of any independent list ≤ length of any spanning list
Definition/statement:
- In a finite-dimensional V, every independent list has length ≤ every spanning list. In particular, any two bases have the same length.

Intuition:
- You cannot have more independent vectors than there are degrees of freedom in any spanning system.

Example:
- In R^3, no independent list of length 4 exists.

Pitfalls/checks:
- Use this to show basis lengths equal. It follows from repeatedly extending an independent list or trimming a spanning list.

2.9 Consequences: impossibility of overly long independent lists / short spanning lists
Definition/statement:
- If an independent list exceeds dim V, impossible. If a spanning list has fewer elements than dim V, impossible.

Intuition:
- Dimension gives tight limits on independent/spanning list lengths.

Example:
- In P_2(R) (dim 3), any spanning list must have ≥ 3 vectors.

Pitfalls/checks:
- Use dimension counts to rule out possibilities; always check if finite-dimensionality holds.

2.10 Subspaces of finite-dimensional spaces are finite-dimensional
Definition/statement:
- Any subspace U of finite-dimensional V is finite-dimensional, with dim U ≤ dim V.

Intuition:
- A subspace cannot have more degrees of freedom than the ambient space.

Example:
- A line in R^3 has dimension 1.

Pitfalls/checks:
- A subspace spanned by a finite number of vectors is clearly finite-dimensional; prove for general subspaces using bases.

2.11 Basis (definition)
Definition/statement:
- A basis is a linearly independent list that spans V. Equivalently, a maximal independent list or a minimal spanning list.

Intuition:
- Basis gives coordinates uniquely for every vector.

Example:
- Standard basis of R^n: e1,...,en.

Pitfalls/checks:
- Both independence and spanning are required. A spanning list with dependence is not a basis; an independent nonspanning list is not a basis.

2.12 Criterion for basis: unique representation
Definition/statement:
- A list is a basis iff every vector in V can be written uniquely as a linear combination of list vectors.

Intuition:
- Basis vectors serve as independent coordinates: coefficients are the coordinates.

Example:
- In R^2 with basis ( (1,1),(1,-1) ), coefficients are unique.

Pitfalls/checks:
- Uniqueness implies independence; existence implies spanning.

2.13 Every spanning list contains a basis
Definition/statement:
- From any spanning list, one can remove redundant vectors successively (using Linear Dependence Lemma) to obtain a basis.

Intuition:
- Trim a spanning list down to a minimal spanning set which is a basis.

Example:
- From (e1,e2,e1+e2) in R^2, drop e1+e2 to get basis (e1,e2).

Pitfalls/checks:
- Order can affect which vectors remain; result always gives some basis.

2.14 Existence of a basis for every finite-dimensional space
Definition/statement:
- Every finite-dimensional vector space has a basis; start from any finite spanning list and extract a basis.

Intuition:
- Finite spanning implies you can find a minimal spanning set that is independent.

Example:
- For P_2(R), {1,x,x^2} is a basis.

Pitfalls/checks:
- For infinite-dimensional spaces, bases need Zorn's lemma in general; for finite-dimensional, constructive methods suffice.

2.15 Every independent list extends to a basis
Definition/statement:
- Any independent list in a finite-dimensional V can be extended by adding vectors until it becomes a basis.

Intuition:
- Independent vectors form part of a coordinate system; keep adding independent vectors until spanning is achieved.

Example:
- In R^3, start with (1,0,0); add (0,1,0) and (0,0,1) to form a basis.

Pitfalls/checks:
- Make sure added vectors stay independent; extension stops when spanning is achieved.

2.16 Complement/subspace giving a direct-sum decomposition V = U ⊕ W
Definition/statement:
- For a subspace U of finite-dimensional V, there exists W with V = U ⊕ W. One constructs W by extending a basis of U to a basis of V and taking span of the added vectors.

Intuition:
- The extra basis vectors span the complement.

Example:
- U = span{(1,0,0)} in R^3; extend with (0,1,0),(0,0,1) to get W.

Pitfalls/checks:
- Complement not unique. To verify direct sum, check U ∩ W = {0} and U + W = V.

2.17 Invariance of basis length
Definition/statement:
- Any two bases of a finite-dimensional vector space have the same length (cardinality). This common length is the dimension.

Intuition:
- Dimension is well-defined and measures degrees of freedom.

Example:
- R^3 has any basis of length 3.

Pitfalls/checks:
- Proof uses the bound that independent lists ≤ spanning lists applied in both directions.

2.18 Dimension (definition)
Definition/statement:
- dim V is the number of vectors in any basis of V (for finite-dimensional V).

Intuition:
- Dimension counts independent coordinates needed to describe vectors.

Example:
- dim P_2(R) = 3.

Pitfalls/checks:
- For infinite-dimensional, dimension is infinite; many results assume finite dimension.

2.19 Basic dimension facts (dim F^n, dim P_m(F), dim inequalities)
Definition/statement:
- dim F^n = n. dim P_m(F) = m+1. If U ≤ V then dim U ≤ dim V; if equality holds then U = V.

Intuition:
- Dimensions add or compare as expected.

Example:
- If U is a plane in R^3, dim U = 2 ≤ 3.

Pitfalls/checks:
- Use dimension comparisons to decide possibility of injections/surjections between spaces.

2.20 Dimension of a sum: dim(V1 + V2) = dim V1 + dim V2 − dim(V1 ∩ V2)
Definition/statement:
- For subspaces V1,V2 of finite-dimensional V, the formula above holds.

Intuition:
- Count dimensions in each subspace but avoid double-counting their intersection.

Example:
- Two lines in R^3 that meet only at 0: dim sum = 1 + 1 − 0 = 2 (a plane).

Pitfalls/checks:
- Use to compute dimension of sums and to detect direct sums (intersection 0 gives dim sum = dim V1 + dim V2).

3. Linear maps

3.1 Linear map (linear transformation) T : V → W
Definition/statement:
- T is linear if T(u+v) = T(u)+T(v) and T(αv)=αT(v) for all u,v ∈ V and α ∈ F.

Intuition:
- Linear maps respect vector space structure; they are “coordinate-free” matrices.

Example:
- Differentiation D: P_2(R) → P_1(R) with D(p)=p' is linear.

Pitfalls/checks:
- Test both additivity and homogeneity. Many problems injectively use linearity of scalar multiplication.

3.2 Notation L(V,W) and L(V)
Definition/statement:
- L(V,W) denotes the vector space of all linear maps V → W. L(V) denotes L(V,V), linear operators on V.

Intuition:
- Linear maps themselves form a vector space with pointwise operations.

Example:
- L(R^2, R^3) is the space of 3×2 real matrices.

Pitfalls/checks:
- Composition is not the vector-space operation; composition is multiplication-like and not commutative generally.

3.3 Linear map determined by values on a basis (existence & uniqueness)
Definition/statement:
- Given a basis v1,...,vn of V and arbitrary w1,...,wn in W, there is a unique linear map T with T(vi)=wi for each i.

Intuition:
- Define T on basis and extend linearly.

Example:
- Define T on standard basis e1,e2 by T(e1)=(1,0), T(e2)=(0,1) to get identity on R^2.

Pitfalls/checks:
- Ensure images wi are chosen freely; linearity then defines T everywhere.

3.4 Algebraic operations on L(V,W) (addition, scalar multiplication)
Definition/statement:
- (S+T)(v) = S(v) + T(v), (αT)(v) = α T(v). With these operations L(V,W) is a vector space.

Intuition:
- Combine linear maps pointwise like vectors.

Example:
- Sum of two matrices represents sum of linear maps.

Pitfalls/checks:
- Composition is not the same as addition; keep operations distinct.

3.5 Composition (product) of linear maps and algebraic properties
Definition/statement:
- If T ∈ L(U,V) and S ∈ L(V,W), then ST ∈ L(U,W) defined by (ST)(u) = S(T(u)). Composition is associative and distributes over addition in appropriate ways.

Intuition:
- Composition corresponds to matrix multiplication; apply one map then the next.

Example:
- Rotating then scaling a vector equals composition of rotation and scaling operators.

Pitfalls/checks:
- Noncommutativity: ST ≠ TS in general. Track domain and codomain types.

3.6 Null space / kernel of a linear map
Definition/statement:
- null T = {v ∈ V : T(v) = 0}; it is a subspace of V.

Intuition:
- Null space measures how T collapses directions to zero.

Example:
- For differentiation D: P_2 → P_1, null D = constant polynomials.

Pitfalls/checks:
- Null space being {0} characterizes injectivity for linear maps.

3.7 Null space is a subspace
Definition/statement:
- null T is closed under sums and scalar multiplication and contains 0.

Intuition:
- Kernel gathers all vectors mapped to zero — closure follows from linearity.

Example:
- As above, constant polynomials are closed under addition and scalars.

Pitfalls/checks:
- Don’t forget to include 0 when checking subspace criteria.

3.8 Injective ⇔ null T = {0}
Definition/statement:
- T is injective iff its null space is {0}. For linear maps, if T(v)=0 only for v=0, then T is one-to-one.

Intuition:
- No two different vectors map to the same image iff only trivial kernel.

Example:
- Inclusion map from subspace to V is injective and has trivial kernel.

Pitfalls/checks:
- For linear maps, injectivity reduces to a linear-algebraic property of kernel.

3.9 Range / image of a linear map
Definition/statement:
- range T = {T(v) : v ∈ V} ⊆ W; range is a subspace of W.

Intuition:
- Range is the set of outputs achievable by T.

Example:
- For differentiation D: P_2 → P_1, range D = P_1 (all linear polynomials).

Pitfalls/checks:
- Surjectivity is the property range T = W.

3.10 Range is a subspace; surjective ⇔ range = W
Definition/statement:
- Range is closed under addition and scalar multiplication. Surjectivity means every w ∈ W is T(v) for some v.

Intuition:
- Range gives column space in matrix terms.

Example:
- The projection onto x-axis has range equal to x-axis subspace.

Pitfalls/checks:
- Use dimension test (rank) to test surjectivity in finite dimensions.

3.11 Fundamental Theorem of Linear Maps (Rank–Nullity)
Definition/statement:
- If V is finite-dimensional and T ∈ L(V,W), then dim V = dim null T + dim range T. dim range T is called rank, dim null T is nullity.

Intuition:
- Degrees of freedom split into those lost to kernel and those mapped injectively into output.

Example:
- For 3-dim V and T with 1D kernel, rank = 2.

Pitfalls/checks:
- Use to deduce impossibility of certain dimensions for kernel/range. Requires finite-dimensional V.

3.12 Dimension-based consequences for (non)injectivity and (non)surjectivity
Definition/statement:
- If dim V > dim W, no injective map V → W exists. If dim V < dim W, no surjective map V → W exists. For equal finite dims, injective ⇔ surjective ⇔ bijective.

Intuition:
- Map cannot increase or decrease dimension without consequences.

Example:
- No injective linear map R^3 → R^2 exists.

Pitfalls/checks:
- Always verify finite dimensionality when applying these criteria.

3.13 Matrix of a linear map relative to bases (M(T))
Definition/statement:
- Given ordered bases of V and W, the matrix M(T) has columns that are coordinate vectors of T applied to basis elements of V relative to basis of W.

Intuition:
- Matrix encodes how T acts on coordinates: multiply coordinate column of v by M(T) to get coordinates of T(v).

Example:
- If T(e1)=2e1+e2 and T(e2)=e1, then matrix [[2,1],[1,0]] relative to basis {e1,e2}.

Pitfalls/checks:
- Be consistent with ordering of bases and whether columns correspond to domain basis vectors.

3.14 Matrix addition and scalar multiplication; L(V,W) ≅ F^{m,n}
Definition/statement:
- L(V,W) is isomorphic to the space of m×n matrices when dim W = m and dim V = n. Matrix addition and scalar multiplication correspond to linear-map operations.

Intuition:
- Linear maps and matrices are interchangeable once bases chosen.

Example:
- L(R^2,R^3) corresponds to 3×2 real matrices.

Pitfalls/checks:
- Isomorphism depends on chosen bases; different bases give different matrix representations.

3.15 Matrix multiplication and its relation to composition
Definition/statement:
- If matrices A and B represent S and T in compatible bases, then the matrix of S∘T is the product of matrices: M(S∘T)=M(S) M(T).

Intuition:
- Composition corresponds to successive linear transformations; multiplication composes their actions.

Example:
- Rotations then scalings correspond to multiplication of rotation and scaling matrices.

Pitfalls/checks:
- Watch order: apply T first, then S corresponds to M(S) M(T).

3.16 Action on coordinate columns: M(T v) = M(T) M(v)
Definition/statement:
- Coordinates of T(v) equal matrix M(T) times coordinate column of v (with consistent bases).

Intuition:
- Matrix acts on coordinate vector to produce coordinates of image.

Example:
- If v has coordinates [x;y] and M(T) = [[1,2],[0,1]], then coordinates of T(v) are [[1,2],[0,1]] [x;y].

Pitfalls/checks:
- Ensure the coordinate column is with respect to the domain basis and output relative to codomain basis.

3.17 Column/row viewpoints and column–row factorization
Definition/statement:
- Columns of M(T) are images of basis vectors expressed in codomain basis. M can be seen as sum of outer products of column vectors and standard basis functionals (column-row factorization).

Intuition:
- Think of building the map by specifying where basis vectors go (columns). Row perspective connects to functionals giving coefficients.

Example:
- A 2×2 matrix can be written as column1*[1,0]^T + column2*[0,1]^T in column-row senses.

Pitfalls/checks:
- Column rank and row rank may be computed via column/row spaces; keep track of which dimension they live in.

3.18 Column rank, row rank and equality = rank
Definition/statement:
- Column rank = dim column space; row rank = dim row space; they are equal and equal to rank of the linear map.

Intuition:
- Independent columns determine how many independent outputs exist; rows reflect independent linear constraints.

Example:
- A 3×2 matrix of rank 2 has two independent columns and two independent rows (in appropriate senses).

Pitfalls/checks:
- Use row-reduction to compute rank; row operations change rows but preserve row space up to equivalence.

3.19 Invertible linear map and inverse (T^{-1}); bijectivity ⇔ invertibility
Definition/statement:
- An operator T: V→V is invertible if there exists S with ST = TS = I. For linear maps between equal-dimension finite spaces, invertible ⇔ bijective.

Intuition:
- Invertible linear maps reorder/scale but don’t collapse information.

Example:
- 2×2 matrix with nonzero determinant is invertible.

Pitfalls/checks:
- Check both left- and right-inverses in infinite-dimensional contexts; in finite-dimensional case bijectivity suffices.

3.20 Isomorphism and dimension criterion for isomorphism
Definition/statement:
- Isomorphism is a bijective linear map. Two finite-dimensional vector spaces are isomorphic iff they have equal finite dimension.

Intuition:
- Isomorphic spaces are “the same” vector-space-wise, just with different labels on basis.

Example:
- P_2(R) ≅ R^3.

Pitfalls/checks:
- Existence of an isomorphism depends solely on dimension in finite-dimensional case.

3.21 Identity matrix, matrix inverse, similarity / change-of-basis (A = C^{-1} B C)
Definition/statement:
- Identity operator I has matrix equal to identity matrix. If A is matrix of T in one basis and B in another, they are similar: A = C^{-1} B C where C is change-of-basis matrix.

Intuition:
- Similar matrices represent the same linear operator in different coordinates.

Example:
- Diagonalization is similarity to a diagonal matrix.

Pitfalls/checks:
- Similarity preserves characteristic polynomial, determinant, trace, and eigenvalues but not entries.

3.22 Direct-sum criterion via the product-to-sum map Γ
Definition/statement:
- Given subspaces V1,...,Vm, the map Γ: V1 × ... × Vm → V defined by Γ(v1,...,vm)=v1+...+vm is linear. Γ is injective iff the sum is direct; Γ is surjective iff sum equals V. Thus V is direct sum of Vi iff Γ is an isomorphism.

Intuition:
- Product-to-sum map encodes decomposition and uniqueness.

Example:
- For V=R^2, taking V1 = x-axis, V2 = y-axis, Γ is bijective.

Pitfalls/checks:
- Use Γ to test directness by checking kernel (only zero tuple) and image.

3.23 Quotient space V/U (cosets) and quotient map π : V → V/U
Definition/statement:
- V/U is the set of cosets v + U with vector space operations (well-defined). The quotient map π sends v to v+U and is linear with kernel U.

Intuition:
- Quotient collapses U to 0, treating vectors equal modulo U.

Example:
- R^2 / x-axis is isomorphic to y-axis; cosets are horizontal lines.

Pitfalls/checks:
- Ensure operations on cosets are well-defined: independence of representative follows from U being a subspace.

3.24 Dimension formula dim(V/U) = dim V − dim U
Definition/statement:
- For finite-dimensional V and subspace U, dim(V/U) = dim V − dim U.

Intuition:
- Collapsing U removes dim U degrees of freedom.

Example:
- dim(R^3 / plane) = 3 − 2 = 1.

Pitfalls/checks:
- Requires finite dimensionality.

3.25 Induced map ˜T : V/(null T) → W and isomorphism onto range T
Definition/statement:
- For T: V→W, there is a well-defined injective linear map ˜T from V/null T to range T given by ˜T(v + null T) = T(v). This map is an isomorphism onto range T.

Intuition:
- Factor out the kernel so map becomes injective; gives an isomorphism between quotient and image.

Example:
- For differentiation D on P_2, quotient by constants maps to P_1 isomorphically.

Pitfalls/checks:
- Well-definedness requires equivalent representatives map to same image; that holds precisely because difference lies in null T.

3.26 Linear functional and dual space V′ = L(V, F)
Definition/statement:
- Linear functionals are linear maps V→F. The dual space V′ is the space of all such functionals.

Intuition:
- Functionals assign scalars to vectors linearly; they are the “row” viewpoint.

Example:
- In R^n, linear functionals correspond to row vectors acting on column vectors by dot product.

Pitfalls/checks:
- Dual depends on base field. For infinite-dimensional V, dual can be much larger.

3.27 Dimension of the dual: dim V′ = dim V (finite-dimensional case)
Definition/statement:
- If dim V = n finite, then dim V′ = n.

Intuition:
- Dual has same number of degrees of freedom as original space.

Example:
- R^3 dual also has dimension 3.

Pitfalls/checks:
- Not necessarily true for infinite-dimensional spaces (dual may be larger).

3.28 Dual basis
Definition/statement:
- Given a basis v1,...,vn of V, the dual basis φ1,...,φn in V′ is defined by φi(vj)=δij (Kronecker delta).

Intuition:
- Dual basis extracts coordinates: φi(v) gives i-th coordinate relative to the basis.

Example:
- For standard basis in R^n, dual basis is coordinate functionals.

Pitfalls/checks:
- Dual basis depends on chosen ordering of basis.

3.29 Dual map T′ : W′ → V′ and algebraic properties
Definition/statement:
- For T: V→W, the dual (transpose) T′ maps φ ∈ W′ to φ∘T ∈ V′. T′ is linear and reverses composition: (ST)′ = T′ S′.

Intuition:
- Dual map pulls functionals back along T.

Example:
- If T is a matrix A, T′ corresponds to A^t acting on row vectors.

Pitfalls/checks:
- Direction reverses: domain/codomain swap roles.

3.30 Annihilator U^0 of a subset U ⊆ V and basic properties
Definition/statement:
- U^0 = {φ ∈ V′ : φ(u) = 0 for all u ∈ U}. It is a subspace of V′.

Intuition:
- Annihilator consists of functionals that vanish on U.

Example:
- In R^3, annihilator of x-y plane consists of multiples of a normal vector’s functional.

Pitfalls/checks:
- Dimension relations: dim U + dim U^0 = dim V for finite-dimensional V.

3.31 Relationships between T and T′ (null/range/annihilator relations)
Definition/statement:
- Useful identities: null T′ = (range T)^0 (annihilator of range T) and range T′ = (null T)^0 (annihilator of null T).

Intuition:
- Dual maps translate kernel/range info into annihilators.

Example:
- If T is surjective, range T = W, then null T′ = {0} so T′ injective.

Pitfalls/checks:
- These relations hold in finite dimensions; use them to infer injectivity/surjectivity of duals.

3.32 Matrix of the dual map is the transpose: M(T′) = M(T)^t
Definition/statement:
- With respect to dual bases, the matrix of T′ is the transpose of the matrix of T.

Intuition:
- Dual map corresponds to transposing action from columns to rows.

Example:
- If M(T) = [[a,b],[c,d]], then M(T′) = [[a,c],[b,d]].

Pitfalls/checks:
- Bases must be appropriately paired with their duals.

3.33 Double dual and canonical embedding Λ : V → V''
Definition/statement:
- V'' = (V')' is the double dual. There is a canonical linear map Λ: V → V'' given by Λ(v)(φ) = φ(v). For finite-dimensional V, Λ is an isomorphism.

Intuition:
- Elements of V can be identified with evaluation functionals on V′.

Example:
- In finite-dimensional R^n, canonical embedding is identification with double dual; coordinates match.

Pitfalls/checks:
- For infinite-dimensional V, Λ need not be surjective (V not isomorphic to V'').

3.34 Duals of inclusions and quotients: natural isomorphisms V'/U^0 ≅ U' and (V/U)' ≅ U^0
Definition/statement:
- For U ≤ V finite-dimensional, the dual of the quotient (V/U)' is naturally isomorphic to U^0, and V'/U^0 is isomorphic to U'.

Intuition:
- Dualizing interacts with restriction and quotient: duals of quotient spaces identify with annihilators.

Example:
- If U is a line in R^3, (R^3/U)' ≅ U^0, a 2D space of functionals vanishing on U.

Pitfalls/checks:
- Keep track of naturalness: these are canonical isomorphisms, not dependent on arbitrary choices.

4. Polynomials

4.1 Polynomial vector space P(F)
Definition/statement:
- P(F) is the vector space of polynomials with coefficients in F; addition and scalar multiplication are coefficientwise.

Intuition:
- Polynomials form a familiar algebraic structure with vector-space properties.

Example:
- p(x)=2 + 3x + x^2 ∈ P(R).

Pitfalls/checks:
- Distinguish P(F) (all polynomials) from P_m(F) (bounded degree).

4.2 Polynomial (definition) and degree conventions (including deg 0 = −∞)
Definition/statement:
- Degree deg p is the highest power with nonzero coefficient; the zero polynomial is often assigned deg 0 = −∞ to make degree rules consistent (e.g., deg( p+q ) ≤ max(deg p, deg q) unconditionally).

Intuition:
- Degree measures polynomial complexity; treat zero specially to preserve inequality rules.

Example:
- deg(x^2+1) = 2; deg 0 = −∞.

Pitfalls/checks:
- Remember this convention if using degree inequalities; some texts use deg 0 = −∞ for convenience.

4.3 Evaluation of polynomials; zeros / roots
Definition/statement:
- For a ∈ F, p(a) is evaluation at a. A zero/root is a where p(a)=0.

Intuition:
- Roots are where the polynomial crosses zero; evaluation is a linear operation in coefficients.

Example:
- p(x)=x^2−1 has zeros at x=1,−1.

Pitfalls/checks:
- Over fields, factorization behavior depends on whether field is algebraically closed (e.g., C).

4.4 Factor theorem (root ⇔ linear factor)
Definition/statement:
- a is a root of p iff (x−a) divides p (i.e., p(x) = (x−a) q(x)).

Intuition:
- Finding roots corresponds to factoring out linear factors.

Example:
- Since p(1)=0 for p(x)=x^2−1, we can write p(x)=(x−1)(x+1).

Pitfalls/checks:
- Use polynomial division to find quotient and remainder; remainder zero indicates divisibility.

4.5 Bound on number of zeros (deg m ⇒ at most m zeros)
Definition/statement:
- Nonzero polynomial of degree ≤ m has at most m distinct zeros in a field.

Intuition:
- Each linear factor accounts for at most one distinct root; multiplicity ignores distinctness.

Example:
- x^2 has at most 2 roots (but only one distinct root at 0).

Pitfalls/checks:
- Over infinite fields this holds; over finite fields polynomials can vanish at many points but degree bound still holds for distinct roots.

4.6 Division algorithm for polynomials (existence/uniqueness of quotient & remainder)
Definition/statement:
- Given p and nonzero s with deg s ≤ deg p, there exist unique q and r with p = s q + r and deg r < deg s (or r = 0).

Intuition:
- Polynomial division mirrors integer division: quotient + remainder.

Example:
- Divide x^3 by x−1 to get quotient x^2 + x + 1 and remainder 1 (actually for this example remainder 1, but p(1)=? check). Standard algorithm applies.

Pitfalls/checks:
- Keep track of degrees; remainder degree must be strictly less than divisor degree.

4.7 De Moivre and k-th roots in C (complex preliminaries)
Definition/statement:
- Complex numbers in polar form re^{iθ} have k-th roots r^{1/k} e^{i(θ+2π j)/k} for j=0,...,k−1 (De Moivre’s root-generalization).

Intuition:
- Roots in C come in k distinct equally spaced arguments on the circle.

Example:
- Square roots of 1 are 1 and −1.

Pitfalls/checks:
- For r=0, root is 0 only. Angles modulo 2π produce duplicates if not careful.

4.8 Fundamental Theorem of Algebra (every nonconstant poly over C has a root)
Definition/statement:
- Every nonconstant polynomial with complex coefficients has at least one complex root.

Intuition:
- C is algebraically closed: polynomials factor fully into linear factors over C.

Example:
- x^2 + 1 has roots i and −i in C.

Pitfalls/checks:
- Fails over R for some polynomials; but holds over C.

4.9 Complete factorization over C into linear factors
Definition/statement:
- Any polynomial p(z) ∈ C[z] of degree n factors as c (z − λ1) ··· (z − λn) for scalars λi ∈ C (counted with multiplicity).

Intuition:
- Roots (with multiplicity) fully determine polynomial up to scalar factor.

Example:
- x^3 − 1 = (x − 1)(x − ω)(x − ω^2) with ω primitive cube root of unity.

Pitfalls/checks:
- Include multiplicity; constant factor c must equal leading coefficient.

4.10 Conjugate-pair property for real-coefficient polynomials
Definition/statement:
- Nonreal roots of real polynomials occur in conjugate pairs: if a+bi is a root, so is a−bi.

Intuition:
- Complex conjugation preserves real coefficients so roots come in pairs.

Example:
- x^2 + 1 has i and −i as roots.

Pitfalls/checks:
- Multiplicities also match for conjugate pairs.

4.11 Factorization over R into linear and irreducible quadratic factors
Definition/statement:
- Every real-coefficient polynomial factors as product of real linear factors and irreducible quadratics (with negative discriminant).

Intuition:
- Over R you can only break polynomials down to quadratics or linears.

Example:
- x^4 + 1 factors as two quadratics over R.

Pitfalls/checks:
- Irreducible quadratics correspond to complex conjugate root pairs.

5. Eigen

5.1 Operator (T ∈ L(V))
Definition/statement:
- An operator is a linear map from a vector space to itself: T: V → V.

Intuition:
- Operators are endomorphisms (matrices act on same space).

Example:
- Matrix multiplication by a fixed matrix A is an operator on F^n.

Pitfalls/checks:
- Many spectral results require operator domain and codomain to coincide.

5.2 Invariant subspace
Definition/statement:
- U ≤ V is invariant under T if T(U) ⊆ U.

Intuition:
- T maps the subspace into itself; you can study T by restriction.

Example:
- For diagonal matrices, coordinate axes are invariant.

Pitfalls/checks:
- Check closure under T for all vectors in U, not just generators.

5.3 One-dimensional invariant subspaces ⇔ T v = λ v (motivation)
Definition/statement:
- A one-dimensional invariant subspace is spanned by some nonzero v with T(v) ∈ span(v) ⇒ T(v) = λ v, i.e., eigenvector/eigenvalue.

Intuition:
- On a line, T acts by scaling.

Example:
- For T(x,y) = (x,0), span{(1,0)} is invariant and (1,0) is an eigenvector with λ=1.

Pitfalls/checks:
- Existence of 1D invariant subspaces depends on field (over C they always exist when operator has a root of characteristic polynomial).

5.4 Eigenvalue (definition)
Definition/statement:
- λ ∈ F is an eigenvalue of T if there exists nonzero v with T(v) = λ v.

Intuition:
- Eigenvalues are scalars by which T scales some nonzero directions.

Example:
- For diagonal matrix diag(2,3), eigenvalues are 2 and 3.

Pitfalls/checks:
- Eigenvalue requires nonzero eigenvector. 0 can be an eigenvalue if T not injective.

5.5 Eigenvector (definition) and eigenspace E(λ,T) = null(T − λ I)
Definition/statement:
- Eigenvectors are nonzero solutions to (T − λ I)v = 0. Eigenspace includes zero and is a subspace equal to null(T−λ I).

Intuition:
- Eigenspace collects all vectors scaled by λ.

Example:
- For T=2I on R^2, E(2,T)=R^2.

Pitfalls/checks:
- Eigenspace dimension (geometric multiplicity) can be >1; multiplicity distinctions important.

5.6 Equivalent finite-dimensional characterizations: λ eigenvalue ⇔ T − λ I not invertible / not injective / not surjective
Definition/statement:
- For finite-dimensional V, λ is an eigenvalue iff T − λ I is not invertible, equivalently not injective, equivalently not surjective.

Intuition:
- Eigenvalue means operator fails to be invertible at that shift.

Example:
- If det(T−λI)=0, λ is eigenvalue.

Pitfalls/checks:
- Determinant criteria only work in finite dimensions.

5.7 Linear independence of eigenvectors corresponding to distinct eigenvalues
Definition/statement:
- Eigenvectors corresponding to distinct eigenvalues are linearly independent.

Intuition:
- Different scaling factors prevent linear dependence.

Example:
- For diag(1,2,3), eigenvectors e1,e2,e3 are independent.

Pitfalls/checks:
- This fact does not imply all eigenvectors are independent if eigenvalues repeat; multiplicity issues arise.

5.8 Upper bound on the number of distinct eigenvalues (≤ dim V)
Definition/statement:
- An n-dimensional space can have at most n distinct eigenvalues (distinct eigenvectors are independent).

Intuition:
- Each distinct eigenvalue provides at least one independent direction.

Example:
- A 3×3 matrix cannot have 4 distinct eigenvalues.

Pitfalls/checks:
- Field matters: over R some complex eigenvalues may not count as eigenvalues in R.

5.9 Powers of an operator T^m
Definition/statement:
- T^m denotes m-fold composition of T with itself; T^0 = I.

Intuition:
- Repeated application of T; spectral properties propagate in predictable ways.

Example:
- If T(v)=λ v, then T^m(v) = λ^m v.

Pitfalls/checks:
- For negative powers, invertibility of T required.

5.10 Polynomials applied to operators p(T) and multiplicative properties
Definition/statement:
- Given p(z)=a0 + a1 z + ... + ak z^k, define p(T) = a0 I + a1 T + ... + ak T^k. p(T) respects algebraic operations: (p+q)(T)=p(T)+q(T), (pq)(T)=p(T) q(T).

Intuition:
- Operators can be plugged into polynomials like numbers; algebra transfers.

Example:
- For T, (T−I)(T+I)=T^2 − I equals composition p(T).

Pitfalls/checks:
- Noncommutativity between operators matters only when combining different operators; polynomials in a single operator are well-defined.

5.11 Null space and range of p(T) are T-invariant
Definition/statement:
- For any polynomial p, null p(T) and range p(T) are invariant under T.

Intuition:
- Applying T maps p(T)-null vectors to other p(T)-null vectors because p(T) and T commute.

Example:
- If v ∈ null(T−λI), then T(v) = λ v ∈ same eigenspace.

Pitfalls/checks:
- Use invariance when decomposing spaces into invariant pieces.

5.12 Existence of eigenvalues over C (FTA applied to operators)
Definition/statement:
- Over C, characteristic polynomial has a complex root, so every operator on nonzero finite-dimensional complex vector space has at least one eigenvalue.

Intuition:
- C being algebraically closed ensures existence of 1D invariant subspaces for operators.

Example:
- Any complex 2×2 matrix has at least one complex eigenvalue.

Pitfalls/checks:
- Over R this may fail (e.g., rotation by 90 degrees in R^2 has no real eigenvalues).

5.13 Monic polynomial and minimal-polynomial existence/uniqueness and degree bound
Definition/statement:
- A polynomial p is monic if leading coefficient is 1. There exists a unique monic minimal polynomial for T: the monic polynomial of smallest degree such that m(T)=0. Its degree ≤ dim V.

Intuition:
- Minimal polynomial captures the simplest algebraic relation satisfied by T.

Example:
- For diagonalizable T with eigenvalues λ1,...,λk, minimal polynomial is product of distinct (z − λi).

Pitfalls/checks:
- Minimal polynomial divides any polynomial q with q(T)=0.

5.14 Minimal polynomial (definition) and basic properties
Definition/statement:
- Minimal polynomial m(z) is the monic polynomial of least degree with m(T)=0. It is unique and divides any polynomial annihilating T.

Intuition:
- Encodes essential algebraic structure of T (including eigenvalues and sizes of Jordan blocks).

Example:
- For nilpotent N with N^k=0 but N^{k−1}≠0, minimal polynomial is z^k.

Pitfalls/checks:
- Minimal polynomial degree ≤ n and shares roots with characteristic polynomial.

5.15 Zeros of the minimal polynomial = eigenvalues
Definition/statement:
- The roots of the minimal polynomial are exactly the eigenvalues of T.

Intuition:
- If (T − λ I) were invertible, then (z−λ) wouldn’t divide minimal polynomial.

Example:
- If m(z) = (z−2)(z−3)^2, eigenvalues are 2 and 3.

Pitfalls/checks:
- Multiplicities in minimal polynomial reflect size of largest Jordan block for that eigenvalue.

5.16 Characterization: q(T) = 0 ⇔ q is a multiple of the minimal polynomial
Definition/statement:
- For monic minimal polynomial m, any polynomial q satisfies q(T)=0 iff m divides q.

Intuition:
- Minimal polynomial generates the ideal of polynomials that annihilate T.

Example:
- If m(z) = z^2, any polynomial divisible by z^2 annihilates T.

Pitfalls/checks:
- Use division algorithm to test whether q(T)=0 given m.

5.17 Minimal polynomial of restrictions / quotients and relation to T
Definition/statement:
- The minimal polynomial of T restricted to an invariant subspace divides the minimal polynomial of T. For induced maps on quotients, minimal polynomial divides the minimal polynomial of T as well.

Intuition:
- Sub-operators satisfy simpler algebraic relations.

Example:
- Restricting T to a 1D eigenspace yields minimal polynomial z−λ.

Pitfalls/checks:
- Be mindful of invariance; restriction only defined on T-invariant subspaces.

5.18 Minimal-polynomial criterion for triangularizability and diagonalizability
Definition/statement:
- T is triangularizable if minimal polynomial splits into linear factors over the field. T is diagonalizable iff minimal polynomial splits into distinct linear factors (product of distinct (z−λ)).

Intuition:
- Multiple roots in minimal polynomial signal Jordan blocks larger than 1, obstructing diagonalizability.

Example:
- A matrix with minimal polynomial (z−1)^2 is not diagonalizable.

Pitfalls/checks:
- Triangularization requires algebraic closure (over C always possible); diagonalization is stricter.

5.19 Triangularization over C (every operator is triangularizable)
Definition/statement:
- Over C, every operator on finite-dimensional space has an upper-triangular matrix with respect to some orthonormal basis (Schur triangularization or by choosing chains of invariant subspaces).

Intuition:
- Use existence of eigenvalue to build flag of invariant subspaces and produce triangular form.

Example:
- Any complex 3×3 matrix is similar to an upper-triangular matrix.

Pitfalls/checks:
- Triangularization does not imply diagonalization; diagonal entries are eigenvalues.

5.20 Diagonalizable operator (definition) and equivalent conditions (basis of eigenvectors; direct sum of eigenspaces)
Definition/statement:
- T is diagonalizable if there is a basis of V consisting of eigenvectors of T. Equivalently, V = ⊕ E(λ_i) (direct sum of eigenspaces) and dim sum equals dim V.

Intuition:
- T acts by scaling each coordinate — simplest possible operator.

Example:
- Distinct eigenvalues with enough eigenvectors yield diagonalization.

Pitfalls/checks:
- Geometric multiplicity (dim eigenspace) must equal algebraic multiplicity for each eigenvalue for a matrix to be diagonalizable.

5.21 Sufficient condition for diagonalizability: dim V distinct eigenvalues
Definition/statement:
- If T has n = dim V distinct eigenvalues, then eigenvectors form a basis and T is diagonalizable.

Intuition:
- Distinct eigenvalues guarantee independent eigenvectors.

Example:
- A 3×3 with eigenvalues 1,2,3 is diagonalizable.

Pitfalls/checks:
- Distinctness is sufficient but not necessary (some repeated eigenvalues may allow diagonalization).

5.22 Minimal-polynomial criterion for diagonalizability (product of distinct linear factors)
Definition/statement:
- T is diagonalizable iff its minimal polynomial has no repeated factors (i.e., is product of distinct linear factors).

Intuition:
- No repeated root means no Jordan blocks beyond size 1.

Example:
- Minimal polynomial (z−2)(z−3) implies diagonalizable.

Pitfalls/checks:
- Verify minimal polynomial correctly; characteristic polynomial could have repeated roots even if minimal polynomial does not.

5.23 Restriction preserves diagonalizability
Definition/statement:
- If T is diagonalizable and U is T-invariant, then T|_U is diagonalizable.

Intuition:
- Restrict to invariant coordinates; eigenvectors restricted remain eigenvectors.

Example:
- Projecting a diagonal operator onto a coordinate plane gives diagonal operator.

Pitfalls/checks:
- Invariance is essential; restrict to non-invariant subspaces is not meaningful.

6. Inner product spaces

6.1 Complex numbers review: real/imaginary parts, conjugate, modulus
Definition/statement:
- For z = a+bi, Re z = a, Im z = b, conjugate z̄ = a − bi, modulus |z| = sqrt(a^2 + b^2).

Intuition:
- Conjugation flips imaginary sign; modulus gives distance from origin.

Example:
- For z = 3 + 4i, z̄ = 3 − 4i, |z| = 5.

Pitfalls/checks:
- Use conjugation when moving scalars in inner products (sesquilinearity in complex case).

6.2 Inner product (abstract definition) and inner-product space
Definition/statement:
- An inner product ⟨·,·⟩ on V (over R or C) is positive-definite, conjugate-symmetric (⟨u,v⟩ = overline{⟨v,u⟩}), and linear in first or second slot depending on convention; Axler uses linear in first and conjugate-linear in second or vice versa — be consistent. Inner-product space is vector space with inner product.

Intuition:
- Inner product generalizes dot product: provides notion of length and angle.

Example:
- On R^n, ⟨x,y⟩ = x⋅y. On C^n, ⟨x,y⟩ = Σ xi ȳi (conjugate on second slot).

Pitfalls/checks:
- Be careful of convention (which slot is linear). Axler typically uses linear in first, conjugate-linear in second; adopt one and stick to it.

6.3 Norm induced by an inner product; basic properties of the norm
Definition/statement:
- Norm ‖v‖ = sqrt(⟨v,v⟩) is induced from inner product. Norm properties: positive-definite, homogeneous, triangle inequality (proved from inner product).

Intuition:
- Norm measures vector length; inner product gives squared norm.

Example:
- For x=(3,4), ‖x‖ = 5.

Pitfalls/checks:
- Norm derived from inner product satisfies parallelogram law; not every norm comes from an inner product.

6.4 Orthogonality and Pythagorean theorem
Definition/statement:
- v and w are orthogonal if ⟨v,w⟩ = 0. If v ⟂ w, then ‖v + w‖^2 = ‖v‖^2 + ‖w‖^2 (Pythagorean theorem).

Intuition:
- Orthogonality generalizes perpendicularity.

Example:
- In R^2, (1,0) ⟂ (0,1) and norms add as squares.

Pitfalls/checks:
- Orthogonality implies independence if one vector is nonzero.

6.5 Orthogonal decomposition / projection onto a one-dimensional span
Definition/statement:
- For nonzero u, any v decomposes uniquely as v = w + α u where w ⟂ u and α = ⟨v,u⟩/⟨u,u⟩. The projection onto span{u} is given by proj_u(v) = (⟨v,u⟩/⟨u,u⟩) u.

Intuition:
- Decompose v into component along u and component perpendicular to u.

Example:
- Project (1,1) onto (1,0): gives (1,0).

Pitfalls/checks:
- Division by ⟨u,u⟩ requires u ≠ 0.

6.6 Cauchy–Schwarz inequality
Definition/statement:
- |⟨v,w⟩| ≤ ‖v‖ ‖w‖ with equality iff v and w are linearly dependent.

Intuition:
- Correlation between vectors bounded by product of lengths.

Example:
- For v=(1,0), w=(1,1), |⟨v,w⟩|=1 ≤ sqrt(1)*sqrt(2)=√2.

Pitfalls/checks:
- Use to derive triangle inequality and other norm inequalities.

6.7 Triangle inequality and parallelogram law
Definition/statement:
- Triangle: ‖v+w‖ ≤ ‖v‖ + ‖w‖. Parallelogram law: ‖v+w‖^2 + ‖v−w‖^2 = 2(‖v‖^2 + ‖w‖^2).

Intuition:
- Norm behaves like length in Euclidean geometry.

Example:
- For v,w unit orthogonal vectors, ‖v+w‖ = √2 ≤ 2.

Pitfalls/checks:
- Parallelogram identity characterizes inner-product-derived norms (Jordan–von Neumann theorem).

6.8 Orthonormal list and properties (norms of combinations, linear independence)
Definition/statement:
- An orthonormal list is a list of vectors each of norm 1 and pairwise orthogonal. Any orthonormal list is linearly independent. Norms of linear combinations: ‖Σ ai vi‖^2 = Σ |ai|^2.

Intuition:
- Orthonormal sets are ideal bases: coefficients are simply inner products.

Example:
- Standard basis in R^n is orthonormal.

Pitfalls/checks:
- Orthonormality simplifies computations; verify both unit norm and mutual orthogonality.

6.9 Bessel’s inequality
Definition/statement:
- For orthonormal list {e1,...,ek} and any v, Σ_{i=1}^k |⟨v,ei⟩|^2 ≤ ‖v‖^2.

Intuition:
- Projections onto orthonormal directions capture at most the full energy of the vector.

Example:
- For v in R^3 and two orthonormal directions, squared projection sum ≤ ‖v‖^2.

Pitfalls/checks:
- Equality holds if and only if v lies in the span of the orthonormal list.

6.10 Orthonormal basis and Parseval’s identity / coordinate expansions
Definition/statement:
- An orthonormal basis is an orthonormal list that spans V. For such a basis {ei}, v = Σ ⟨v,ei⟩ ei and ‖v‖^2 = Σ |⟨v,ei⟩|^2 (Parseval).

Intuition:
- Coordinates are inner products; energy decomposes into orthogonal components.

Example:
- Fourier series are infinite-dimensional analog of this (when orthonormal basis infinite).

Pitfalls/checks:
- For finite bases, expansion is finite and exact. For infinite settings, completeness matters.

6.11 Gram–Schmidt procedure
Definition/statement:
- Starting from a linearly independent list, Gram–Schmidt orthonormalizes it by successive orthogonal projections to produce an orthonormal list with the same span.

Intuition:
- Convert any basis into an orthonormal one while preserving span.

Example:
- Turn (1,1),(1,0) into orthonormal vectors in R^2 via Gram–Schmidt.

Pitfalls/checks:
- Watch for numerical instability in computations; ensure nonzero divisors; works only when original list independent.

6.12 Existence and extension of orthonormal bases
Definition/statement:
- Any finite-dimensional inner-product space has an orthonormal basis. Any orthonormal list can be extended to an orthonormal basis.

Intuition:
- Use Gram–Schmidt to build orthonormal bases from bases or extend orthonormal lists.

Example:
- Start with one unit vector and extend to basis in R^n.

Pitfalls/checks:
- For infinite dimensions extension requires Zorn-like arguments and completeness issues.

6.13 Orthogonal complement U^⊥ and basic properties
Definition/statement:
- U^⊥ = {v ∈ V : ⟨v,u⟩ = 0 for all u ∈ U}; it is a subspace. For finite-dimensional V, dim U + dim U^⊥ = dim V.

Intuition:
- U^⊥ collects directions orthogonal to U.

Example:
- For U = x-axis in R^2, U^⊥ = y-axis.

Pitfalls/checks:
- U ∩ U^⊥ = {0} usually (unless U = {0}). In infinite-dimensional spaces, closure matters for topological complements.

6.14 Direct-sum decomposition V = U ⊕ U^⊥ (finite-dimensional)
Definition/statement:
- In finite-dimensional inner-product spaces, V = U ⊕ U^⊥: every v uniquely splits as u + w with u ∈ U, w ∈ U^⊥.

Intuition:
- Project onto U and orthogonal leftover gives unique decomposition.

Example:
- Decompose (x,y) into x-axis + y-axis components.

Pitfalls/checks:
- Finite dimensionality ensures U + U^⊥ = V. In infinite dimensions closure of U may be needed.

6.15 Orthogonal projection P_U and its properties
Definition/statement:
- P_U: V→U maps v to its U-component in the orthogonal decomposition. P_U is linear, self-adjoint (P_U* = P_U), idempotent (P_U^2 = P_U), and has norm ≤ 1.

Intuition:
- Projection is best approximation of v by elements of U.

Example:
- Projection onto x-axis maps (x,y) to (x,0).

Pitfalls/checks:
- Projection depends on inner product. Projection onto non-orthogonal complements is more complicated.

6.16 Riesz representation theorem (finite-dimensional)
Definition/statement:
- For finite-dimensional inner-product V, every linear functional φ ∈ V′ can be written as φ(v) = ⟨v,u⟩ for a unique u ∈ V. This gives an isomorphism between V and V′.

Intuition:
- Functionals correspond to inner products with a unique representing vector.

Example:
- In R^n with dot product, φ(x)=a⋅x corresponds to u=a.

Pitfalls/checks:
- This is finite-dimensional version; in infinite dimensions completeness matters for Hilbert spaces.

6.17 Best-approximation and least-squares via orthogonal projection
Definition/statement:
- The orthogonal projection P_U(v) is the unique u ∈ U minimizing ‖v−u‖. This is the least-squares solution when solving inconsistent linear systems.

Intuition:
- Projecting gives the best approximation by U.

Example:
- Fitting a line to data via normal equations corresponds to projecting onto span of basis functions.

Pitfalls/checks:
- Solve normal equations (A^* A x = A^* b) with care for conditioning.

6.18 Pseudoinverse motivation via restriction to (null T)^⊥
Definition/statement:
- For T: V→W, restricting T to (null T)^⊥ makes it injective; one can form a left-inverse on the range, leading to pseudoinverse ideas in least-squares contexts.

Intuition:
- Remove null directions then invert on remaining part for best-approximation solutions.

Example:
- Moore–Penrose pseudoinverse gives least-squares solution to A x = b.

Pitfalls/checks:
- Pseudoinverse gives unique minimum-norm solution but requires understanding of nullspace and orthogonality.

7. Operators on inner product spaces

7.1 Adjoint (T*) and computation techniques
Definition/statement:
- For T: V→V on inner-product space, T* is operator satisfying ⟨T v, w⟩ = ⟨v, T* w⟩ for all v,w ∈ V. With orthonormal bases, matrix of T* is conjugate transpose of matrix of T.

Intuition:
- Adjoint transfers action from one slot of the inner product to the other.

Example:
- For matrix A representing T in orthonormal basis, T* has matrix A* = (Ā)^t.

Pitfalls/checks:
- Adjoint depends on inner product; ensure using orthonormal basis for matrix formulas.

7.2 Algebraic properties of adjoint and matrix conjugate-transpose (A*)
Definition/statement:
- (S+T)* = S* + T*, (αT)* = overline{α} T*, (ST)* = T* S*, and (T*)* = T, etc. Matrix conjugate-transpose shares these properties.

Intuition:
- Adjoint reverses order in products and conjugates scalars.

Example:
- (AB)* = B* A* for matrices.

Pitfalls/checks:
- Keep conjugation of scalars in mind in complex case.

7.3 Nullspace / range relationships: null T* = (range T)^⊥, range T* = (null T)^⊥
Definition/statement:
- In inner-product spaces, null T* equals orthogonal complement of range T; range T* equals orthogonal complement of null T.

Intuition:
- Adjoint connects kernel and image via orthogonality.

Example:
- For matrix A, left nullspace corresponds to orthogonal complement of column space.

Pitfalls/checks:
- Useful for solving least-squares and normal equations.

7.4 Self-adjoint operators (T = T*) and basic consequences (⟨T v,v⟩ ∈ R, real eigenvalues)
Definition/statement:
- T is self-adjoint if T = T*. Then ⟨T v, v⟩ is real for all v, and eigenvalues are real.

Intuition:
- Self-adjoint operators generalize symmetric matrices with real spectral properties.

Example:
- Real symmetric matrix represents self-adjoint operator under standard inner product.

Pitfalls/checks:
- Self-adjointness depends on inner product; check in complex case appropriately (Hermitian matrices).

7.5 Normal operators (T T* = T* T) and equivalent characterizations
Definition/statement:
- T is normal iff T commutes with its adjoint. Equivalent: T and T* are simultaneously diagonalizable by a unitary if T is normal and diagonalizable; more precisely, T is unitarily diagonalizable iff normal and minimal polynomial splits into distinct linear factors in C, etc.

Intuition:
- Normal operators behave nicely: have orthonormal bases of eigenvectors if diagonalizable.

Example:
- Unitary and self-adjoint operators are normal.

Pitfalls/checks:
- Normal does not imply diagonalizable over reals; over C, normal ⇒ unitarily diagonalizable.

7.6 Real/imaginary decomposition for normal operators (complex case)
Definition/statement:
- Any complex operator T can be decomposed as T = A + iB with A and B self-adjoint; if T is normal, A and B commute.

Intuition:
- Separate Hermitian and skew-Hermitian parts to analyze spectral properties.

Example:
- For any matrix A, A = (A + A*)/2 + (A − A*)/2.

Pitfalls/checks:
- Commutator issues: A and B commuting helps triangularization/diagonalization.

7.7 Schur’s theorem: orthonormal upper-triangularization; existence over C
Definition/statement:
- For complex inner-product spaces, every operator has an orthonormal basis in which its matrix is upper-triangular (Schur decomposition). Diagonal entries are eigenvalues.

Intuition:
- Triangular form achieved via orthonormal change of basis; stepping by picking eigenvectors and extending orthogonally.

Example:
- Any 3×3 complex matrix is unitarily similar to an upper-triangular matrix.

Pitfalls/checks:
- Schur gives triangularization, not diagonalization; further normality needed for unitary diagonalization.

7.8 Spectral theorem (real): orthogonal diagonalization for self-adjoint operators
Definition/statement:
- A real self-adjoint operator on finite-dimensional inner-product space has an orthonormal basis of eigenvectors and is orthogonally diagonalizable with real eigenvalues.

Intuition:
- Self-adjoint operators are “perfectly” diagonalizable with orthonormal eigenbasis.

Example:
- Real symmetric matrices are orthogonally diagonalizable: A = Q D Q^t with Q orthogonal.

Pitfalls/checks:
- Over C this is Hermitian ⇒ unitary diagonalizable; over R ensure eigenvalues are real.

7.9 Spectral theorem (complex): unitary diagonalization for normal operators
Definition/statement:
- A complex normal operator has an orthonormal basis of eigenvectors and is unitarily diagonalizable.

Intuition:
- Normal operators generalize Hermitian or unitary ones and admit diagonalization by a unitary matrix.

Example:
- Unitary matrices are normal and diagonalizable by a unitary if eigenvalues distinct or appropriate.

Pitfalls/checks:
- Normality is necessary and sufficient for unitary diagonalization in complex finite-dimensional setting.

7.10 Positive operators and equivalent characterizations
Definition/statement:
- T is positive if T is self-adjoint and ⟨T v, v⟩ ≥ 0 for all v. Equivalent: T = S* S for some S, and spectrum lies in [0,∞).

Intuition:
- Positive operators are like positive-definite matrices but allow zero eigenvalues.

Example:
- T = A^* A is positive.

Pitfalls/checks:
- Positive does not imply invertible; strictly positive (⟨T v,v⟩ > 0 for v≠0) implies invertibility.

7.11 Square root of a positive operator (existence and uniqueness)
Definition/statement:
- Every positive operator T has a unique positive square root S with S^2 = T and S positive.

Intuition:
- Generalizes matrix square root for PSD matrices.

Example:
- For positive definite matrix A, there is unique positive definite B with B^2 = A.

Pitfalls/checks:
- Square root chosen must be positive; other (nonpositive) square roots may exist for some operators.

7.12 Isometries and unitary operators (definitions and matrix characterizations)
Definition/statement:
- An isometry S satisfies ‖S v‖ = ‖v‖ for all v. On finite-dimensional inner-product spaces, isometries are exactly unitary (complex) or orthogonal (real) operators; their matrices satisfy S* S = I.

Intuition:
- Isometries preserve lengths and inner products.

Example:
- Rotation matrix in R^2 is orthogonal and an isometry.

Pitfalls/checks:
- Determinant of orthogonal matrix is ±1. Unitaires preserve inner product and are invertible with inverse S*.

7.13 Eigenvalue location for unitary operators (|λ| = 1)
Definition/statement:
- If U is unitary, all eigenvalues λ satisfy |λ| = 1 (lie on unit circle in C).

Intuition:
- Unit-preserving scaling only possible by complex phases.

Example:
- Rotation by θ has eigenvalues e^{iθ} (in complexified sense).

Pitfalls/checks:
- Real orthogonal matrices might have complex eigenvalues on unit circle when considered over C.

7.14 QR factorization and Cholesky factorization
Definition/statement:
- Any full-rank matrix A can be factored as A = Q R with Q orthonormal columns and R upper-triangular (QR). For positive definite A, Cholesky gives A = L L* with lower-triangular L.

Intuition:
- QR is orthonormalization of column space; Cholesky is square-root decomposition for positive definite matrices.

Example:
- Apply Gram–Schmidt to columns of A to produce Q and R.

Pitfalls/checks:
- QR requires column independence for square invertible R. Cholesky requires positive definiteness.

7.15 T* T, positive operator and definition of singular values
Definition/statement:
- For T: V→W, T* T is positive operator on V. Singular values of T are square roots of eigenvalues of T* T (nonnegative).

Intuition:
- Singular values measure how much T stretches orthogonal directions.

Example:
- For diagonal matrix diag(3,2), singular values 3 and 2 (absolute values).

Pitfalls/checks:
- Singular values are always ≥ 0; multiplicity issues reflect dimensions.

7.16 Singular value decomposition (SVD) for linear maps and matrices
Definition/statement:
- Any matrix A (or linear map) can be factored as A = U Σ V* where U and V are unitary (orthogonal in real case) and Σ is diagonal with nonnegative entries (singular values) placed in descending order, possibly padded with zeros.

Intuition:
- SVD decomposes map into rotation → scaling along orthogonal axes → rotation.

Example:
- A 2×2 matrix with full SVD yields orthonormal bases of domain and codomain that show action as scaling by singular values.

Pitfalls/checks:
- SVD exists for all matrices (no diagonalizability requirement). Beware ordering and zero padding.

7.17 Expressions for adjoint and pseudoinverse from SVD
Definition/statement:
- From A = U Σ V*, A* = V Σ U*. Moore–Penrose pseudoinverse A^+ = V Σ^+ U* where Σ^+ inverts nonzero singular values and leaves zeros.

Intuition:
- SVD gives constructive formulas for pseudoinverse and adjoint.

Example:
- For rank-deficient matrices, pseudoinverse gives least-squares solution.

Pitfalls/checks:
- Use singular values above numerical tolerance to invert; small singular values cause instability.

7.18 Operator norm and relation to largest singular value
Definition/statement:
- Operator norm ‖T‖ = sup_{‖v‖=1} ‖T v‖ equals largest singular value σ_max(T).

Intuition:
- Maximal stretching factor of T is its biggest singular value.

Example:
- For diagonal scaling diag(5,2), operator norm is 5.

Pitfalls/checks:
- Norm depends on chosen inner product; equivalently, matrix norm subordinate to vector norm.

7.19 Norm properties (‖T‖ = ‖T*‖) and best low-rank approximation (Eckart–Young)
Definition/statement:
- ‖T‖ = ‖T*‖ = σ_max. Eckart–Young theorem: truncating SVD gives best low-rank approximation in operator or Frobenius norm.

Intuition:
- Largest singular values capture most of operator’s action; dropping small ones yields best approximation of specified rank.

Example:
- Best rank-one approximation is σ1 u1 v1*.

Pitfalls/checks:
- Best approximation is with respect to orthogonally invariant norms like operator and Frobenius norm.

7.20 Polar decomposition T = S √(T* T)
Definition/statement:
- Any T can be written as T = U P where P = √(T* T) is positive and U is partial isometry/unitary on range of P; in full-rank square case U is unitary.

Intuition:
- Separate T into a positive symmetric stretch and a unitary rotation.

Example:
- For invertible A, A = Q H with Q unitary and H positive definite.

Pitfalls/checks:
- For non-invertible T, U defined only on closure of range; in finite dimensions this is fine but must be careful with rank-deficiency.

7.21 Geometric consequences (images of balls, ellipsoids, volume scaling preview)
Definition/statement:
- T maps unit ball into an ellipsoid whose semi-axes lengths are singular values. Determinant magnitude equals product of singular values (volume scaling).

Intuition:
- SVD describes geometric deformation: rotation → scaling → rotation.

Example:
- A maps unit circle to ellipse with axes lengths σ1,σ2.

Pitfalls/checks:
- Determinant sign relates to orientation; absolute determinant equals volume scaling factor.

8. Operators on complex vector spaces

8.1 Sequence of null spaces of powers and stabilization
Definition/statement:
- For T on finite-dimensional V, null(T) ⊆ null(T^2) ⊆ ... and this ascending chain stabilizes: null(T^k) = null(T^{k+1}) for large enough k (≤ dim V).

Intuition:
- Repeated kernels grow until they stop; nilpotent behavior captured by stabilization index.

Example:
- For nilpotent N with N^3 = 0, null(N) ⊂ null(N^2) ⊂ null(N^3)=V.

Pitfalls/checks:
- Stabilization index ≤ dim V. Check powers until rank no longer changes.

8.2 Direct-sum decomposition V = null(T^n) ⊕ range(T^n)
Definition/statement:
- For sufficiently large n (≥ index of stabilization), V decomposes as direct sum of null(T^n) and range(T^n).

Intuition:
- High power of T splits space into generalized null part and range part cleanly.

Example:
- For Jordan decompositions, take n equal to size of largest Jordan block for eigenvalue 0.

Pitfalls/checks:
- Requires choosing n large enough; formula follows from rank-nullity stabilization.

8.3 Generalized eigenvector (definition) and finiteness bound on the order
Definition/statement:
- A generalized eigenvector of order k for eigenvalue λ satisfies (T − λ I)^k v = 0. Orders bounded by dim V.

Intuition:
- Generalized eigenvectors lie in chains that culminate in true eigenvectors.

Example:
- If (T−λI)^2 v = 0 but (T−λI) v ≠ 0, v is generalized eigenvector of order 2.

Pitfalls/checks:
- Generalized eigenvectors include ordinary eigenvectors (k=1). Choose minimal k for chain.

8.4 Generalized eigenspace G(λ,T) and description via a fixed power
Definition/statement:
- G(λ,T) = ∪_{k≥1} null( (T − λ I)^k ) = null( (T − λ I)^m ) for m large enough (stabilization). It is T-invariant.

Intuition:
- G(λ,T) collects all vectors eventually sent to zero by shifting T−λI enough times.

Example:
- For Jordan block of size r, generalized eigenspace has dimension r for that block.

Pitfalls/checks:
- Stabilization exponent m ≤ dim V; G(λ,T) includes all generalized eigenvectors.

8.5 Existence of a basis of generalized eigenvectors over C
Definition/statement:
- Over C, V has a basis consisting of generalized eigenvectors of T (Jordan canonical theory). Equivalently, T is block upper-triangular with Jordan blocks.

Intuition:
- You can always decompose V into primary components and within each build Jordan chains.

Example:
- A 3×3 matrix with one eigenvalue λ and Jordan blocks of sizes 2 and 1 yields basis of generalized eigenvectors.

Pitfalls/checks:
- Existence relies on algebraic closure (C). Over R, generalized eigenvectors may require passing to C.

8.6 Linear independence properties of generalized eigenvectors for distinct eigenvalues
Definition/statement:
- Generalized eigenvectors corresponding to distinct eigenvalues are linearly independent; generalized eigenspaces for distinct eigenvalues intersect trivially.

Intuition:
- Different eigenvalues separate structure so chains do not mix.

Example:
- Chains for λ=1 and λ=2 span independent subspaces.

Pitfalls/checks:
- Use this to build direct-sum decomposition into generalized eigenspaces.

8.7 Nilpotent operators: definition, examples, and bounds
Definition/statement:
- N is nilpotent if N^k = 0 for some k. The minimal such k ≤ dim V. Nilpotents have only 0 eigenvalue.

Intuition:
- Nilpotent operators “eventually kill” every vector.

Example:
- Strictly upper-triangular matrix is nilpotent.

Pitfalls/checks:
- Nilpotency implies trace 0 and determinant 0.

8.8 Characterizations of nilpotency (minimal polynomial = z^m; strictly upper-triangular form)
Definition/statement:
- N nilpotent ⇔ minimal polynomial is z^m for some m. Equivalent: N is similar to strictly upper-triangular matrix with zeros on diagonal.

Intuition:
- Nilpotent operators are Jordan blocks with eigenvalue 0 only.

Example:
- 3×3 Jordan block with zeros on diagonal has N^3=0.

Pitfalls/checks:
- Check minimal polynomial and powers to determine nilpotency index.

8.9 Generalized eigenspace (primary) decomposition: V = ⊕ G(λ_k,T)
Definition/statement:
- V decomposes into direct sum of generalized eigenspaces corresponding to distinct eigenvalues λ_k (primary decomposition).

Intuition:
- T acts independently on each primary component; reduce study to each eigenvalue separately.

Example:
- For matrix with eigenvalues 1 and 2, V = G(1) ⊕ G(2).

Pitfalls/checks:
- Multiplicities add up: sum of dimensions of generalized eigenspaces = dim V.

8.10 Multiplicity (algebraic multiplicity) = dim G(λ,T) and sum of multiplicities = dim V
Definition/statement:
- Algebraic multiplicity of eigenvalue λ equals dimension of its generalized eigenspace G(λ,T); the sum over eigenvalues equals dim V.

Intuition:
- Generalized eigenspace dimension counts how many coordinates are associated with λ.

Example:
- If characteristic polynomial has (z−λ)^3 factor, then dim G(λ,T)=3.

Pitfalls/checks:
- Algebraic multiplicity can differ from geometric multiplicity (dim eigenspace).

8.11 Block-diagonalization with upper-triangular blocks (one block per eigenvalue)
Definition/statement:
- T is similar to block-diagonal matrix where each block is upper-triangular with eigenvalue λ_i repeated on diagonal (Jordan form refinement).

Intuition:
- Separate operator into blocks that each handle one eigenvalue.

Example:
- Blocks for λ=1 of sizes 2 and 1 produce a block-diagonal matrix with two Jordan blocks for λ=1.

Pitfalls/checks:
- Blocks correspond to primary decomposition; sizes and number reflect structure of minimal polynomial.

8.12 Jordan chains, Jordan basis and Jordan canonical form (existence over C)
Definition/statement:
- Jordan chain is sequence v, (T−λI)v, ..., forming a chain of generalized eigenvectors producing Jordan block. A Jordan basis produces Jordan canonical form: block-diagonal with Jordan blocks (each block has λ on diagonal and 1’s on superdiagonal).

Intuition:
- Jordan form makes nilpotent part explicit and classifies linear operators up to similarity over C.

Example:
- A Jordan block J_r(λ) of size r has λ on diagonal and ones above diagonal.

Pitfalls/checks:
- Jordan form requires algebraically closed field (C). Jordan blocks sizes determined by structure of (T−λI)^k kernels.

8.13 Square roots for invertible operators over C (I + nilpotent square-root construction)
Definition/statement:
- Any invertible operator over C with no negative complication admits a square root; decomposition into diagonalizable and nilpotent parts can be used to construct square roots for invertible operators via functional calculus and series when dealing with I+N where N nilpotent.

Intuition:
- Use Jordan decomposition: for invertible operator expressible as S (I+N) with S diagonalizable positive then take roots block-wise.

Example:
- For matrix with eigenvalues not zero, one can define principal square root via Jordan blocks when no nonpositive issues arise.

Pitfalls/checks:
- Care needed for non-diagonalizable parts; nilpotent series converge finitely because N nilpotent.

9. Multilinear / determinants

9.1 Bilinear forms and examples
Definition/statement:
- A bilinear form B: V × V → F is linear in each argument separately. Over complex fields one often studies sesquilinear (conjugate-linear in one argument) forms; here treat bilinear as stated.

Intuition:
- Generalizes dot product without positivity or symmetry assumptions.

Example:
- B(u,v) = u^t A v for matrix A gives a bilinear form.

Pitfalls/checks:
- Distinguish bilinear vs sesquilinear (inner products are conjugate-linear in one slot in complex case).

9.2 Space of bilinear forms V(2) and matrix of a bilinear form
Definition/statement:
- Set of bilinear forms is a vector space. Given basis, any bilinear form corresponds to a matrix B with entries B(ei,ej). Changing basis transforms matrix via congruence.

Intuition:
- Bilinear forms correspond to matrices relative to chosen basis; algebraic operations correspond to matrix operations.

Example:
- Standard dot product corresponds to identity matrix.

Pitfalls/checks:
- Matrix representation depends on basis ordering; forms can be symmetric or skew-symmetric.

9.3 Change-of-basis formula for bilinear forms (A = C^t B C)
Definition/statement:
- Under basis change with change-of-basis matrix C, matrix of bilinear form transforms as A = C^t B C (congruence), where B is old matrix and A is new.

Intuition:
- Congruence captures how quadratic forms change under variable substitution.

Example:
- Diagonalization of quadratic forms uses congruence transformations.

Pitfalls/checks:
- This differs from similarity (A = C^{-1} B C) used for linear operators.

9.4 Symmetric bilinear forms and symmetric matrices; diagonalizability
Definition/statement:
- Bilinear form is symmetric if B(u,v)=B(v,u). Over fields not of char 2, symmetric forms have symmetric matrices and can often be diagonalized by congruence (Sylvester’s law of inertia over R yields signature).

Intuition:
- Symmetric forms generalize quadratic forms; diagonalization simplifies their study.

Example:
- Quadratic form x^2 + y^2 − z^2 corresponds to diagonal matrix diag(1,1,−1).

Pitfalls/checks:
- Over R, signature (numbers of positive/negative squares) is invariant under congruence. Over general fields, diagonalization properties vary.

9.5 Alternating bilinear forms and properties (vanishing on dependent lists)
Definition/statement:
- Alternating bilinear form B satisfies B(v,v)=0 for all v; equivalently B(u,v) = −B(v,u) and B(v,v)=0. Alternating forms vanish on linearly dependent lists in certain degrees.

Intuition:
- Alternating forms generalize determinants and areas; they detect oriented volume.

Example:
- Area form in R^2 given by determinant is alternating.

Pitfalls/checks:
- Over fields of characteristic 2, antisymmetry and alternating notions coincide differently; watch characteristic.

9.6 Multilinear (m-linear) forms and alternating m-forms; permutation sign behavior
Definition/statement:
- An m-linear form is multilinear in m arguments. An alternating m-form changes sign according to permutation parity: ω(v_{σ(1)},...,v_{σ(m)}) = sign(σ) ω(v1,...,vm).

Intuition:
- Alternating forms vanish when arguments are linearly dependent and pick up sign changes under swapping.

Example:
- Determinant as an n-linear alternating form on an n-dimensional space.

Pitfalls/checks:
- Linearity and alternation implies vanishing when two arguments equal.

9.7 Top-degree alternating forms: formula over permutations and dim = 1
Definition/statement:
- On n-dimensional V, the space of alternating n-forms is one-dimensional. Any such form is a scalar multiple of a chosen volume form; its value on a basis determines it.

Intuition:
- Up to scale there is a unique n-form measuring oriented volume.

Example:
- Determinant is basis form; any n-form ω determined by ω(e1,...,en).

Pitfalls/checks:
- This is basis-free: maps that act on top forms produce scalars (determinant).

9.8 Action of operators on top-degree alternating forms (pullback α_T)
Definition/statement:
- Given T ∈ L(V), define α_T(ω)(v1,...,vn) = ω(T v1, ..., T vn). α_T acts linearly on top-degree alternating forms and corresponds to scaling by det(T) on the one-dimensional top space.

Intuition:
- Operator stretches/compresses oriented volumes by determinant.

Example:
- For A scaling by 2 in each coordinate in R^n, α_A multiplies ω by 2^n.

Pitfalls/checks:
- α_T is multiplicative in T: α_{ST} = α_S α_T.

9.9 Determinant of an operator (basis-free) via action on top-degree alternating forms
Definition/statement:
- Determinant det T is defined by α_T(ω) = (det T) ω for any nonzero top-degree alternating form ω. This gives basis-free determinant.

Intuition:
- Determinant measures volume scaling factor of T.

Example:
- det on diagonal matrix diag(d1,...,dn) equals product d1···dn.

Pitfalls/checks:
- Determinant depends on field and orientation conventions; multiplicative: det(ST)=det S det T.

9.10 Determinant of a matrix and Leibniz (permutation-sum) formula
Definition/statement:
- Determinant of matrix A is Σ_{σ ∈ S_n} sign(σ) a_{1σ(1)}... a_{nσ(n)} (Leibniz formula).

Intuition:
- Determinant sums over all permutations, each weighted by sign, reflecting oriented volume combinatorics.

Example:
- 2×2 determinant ad − bc.

Pitfalls/checks:
- Computation by Leibniz is factorial in cost; use expansion or row operations for practicality.

9.11 Determinant of triangular matrices and multiplicativity: det(ST) = det S · det T
Definition/statement:
- Determinant of triangular matrix equals product of diagonal entries. Determinant is multiplicative: det(ST) = det S det T.

Intuition:
- Triangular gives immediate determinant; multiplicativity follows from action on top forms or matrix algebra.

Example:
- For upper-triangular diag(2,3,4), det = 24.

Pitfalls/checks:
- Multiplicativity can be used to deduce det inverse = 1/det if invertible.

9.12 Invertibility ⇔ nonzero determinant; det(T^{-1}) = 1 / det T
Definition/statement:
- T invertible iff det T ≠ 0; and det(T^{-1}) = (det T)^{-1}.

Intuition:
- Nonzero volume scaling implies invertibility.

Example:
- Matrix with determinant 0 cannot be invertible.

Pitfalls/checks:
- For singular matrices det = 0, nullspace nontrivial.

9.13 Determinant and eigenvalues: det = product of eigenvalues (over C)
Definition/statement:
- For operator on n-dim space over C, determinant equals product of eigenvalues counted with algebraic multiplicity.

Intuition:
- Diagonalizable case immediate; triangularization gives same product on diagonal.

Example:
- For matrix with eigenvalues 2,3,−1, det = −6.

Pitfalls/checks:
- Holds over algebraically closed fields when counting multiplicity (characteristic polynomial roots). Over reals some eigenvalues complex, product still equals determinant via complexification.

9.14 Characteristic polynomial p_T(z) = det(z I − T) and its properties (degree n, zeros = eigenvalues)
Definition/statement:
- Characteristic polynomial p_T(z) is degree n polynomial whose roots are eigenvalues. p_T has leading coefficient 1 (monic).

Intuition:
- Characteristic polynomial bundles spectral information algebraically.

Example:
- For 2×2 matrix [[a,b],[c,d]], p(z) = (z−a)(z−d) − bc.

Pitfalls/checks:
- Cayley–Hamilton theorem connects characteristic polynomial back to operator.

9.15 Cayley–Hamilton theorem: q(T) = 0 for the characteristic polynomial q
Definition/statement:
- Every operator satisfies its characteristic polynomial: p_T(T) = 0.

Intuition:
- Characteristic polynomial annihilates the operator; useful for expressing powers of T in lower degree basis.

Example:
- For 2×2, T^2 expressed in terms of T and I using coefficients from characteristic polynomial.

Pitfalls/checks:
- Use Cayley–Hamilton to reduce polynomials in T modulo characteristic polynomial.

9.16 Trace: definition, basis-independence, and relation to eigenvalues and characteristic polynomial coefficient
Definition/statement:
- Trace of operator is sum of diagonal entries of any matrix representing it; independent of basis. It equals sum of eigenvalues (with multiplicity) and is negative of coefficient of z^{n−1} in characteristic polynomial up to sign convention.

Intuition:
- Trace measures total sum of scalings along diagonalizable directions.

Example:
- For matrix [[a,b],[c,d]], tr = a + d.

Pitfalls/checks:
- Trace is linear and cyclic: tr(AB)=tr(BA).

9.17 Trace cyclicity tr(AB) = tr(BA) and linearity
Definition/statement:
- Trace is linear and satisfies tr(AB) = tr(BA) for compatible matrices. More generally tr(ABC)=tr(CAB) etc.

Intuition:
- Cyclic property useful in proofs and invariants.

Example:
- tr([[0,1],[0,0]] [[0,0],[1,0]]) = tr([[1,0],[0,0]]) = 1 equals tr product reversed.

Pitfalls/checks:
- Cyclicity does not allow arbitrary permutation except cyclic shifts.

9.18 Determinant behaviours under row/column operations; det A^t = det A; det of adjoint/dual
Definition/statement:
- Elementary row operations affect determinant: swapping rows multiplies det by −1, scaling a row multiplies det by scalar, adding multiple of one row to another leaves det unchanged. det(A^t) = det A. Determinant of adjoint/dual relates via det(T^*) = overline{det(T)} in complex case.

Intuition:
- Row operations track how volume changes.

Example:
- Row swap of matrix with det 2 gives det −2.

Pitfalls/checks:
- When computing determinant via row-reduction, record multipliers and swaps to adjust determinant.

9.19 Hadamard’s inequality and Vandermonde determinant
Definition/statement:
- Hadamard: Absolute determinant ≤ product of norms of column vectors, with equality when columns orthogonal. Vandermonde determinant gives det of matrix with geometric progression powers as product of differences ∏_{i<j} (x_j − x_i).

Intuition:
- Hadamard bounds volume by product of column lengths. Vandermonde formula quantifies determinant of power matrices.

Example:
- For 2×2 columns u,v, |det[u v]| ≤ ‖u‖ ‖v‖.

Pitfalls/checks:
- Hadamard equality case requires orthogonality; Vandermonde zero when two xi equal.

9.20 Tensor product V ⊗ W: definition, elementary tensors, basis {e_j ⊗ f_k}, and universal property
Definition/statement:
- Tensor product V ⊗ W is vector space generated by formal symbols v ⊗ w subject to bilinearity relations. Elementary tensors v⊗w span it; if {e_j} and {f_k} are bases then {e_j ⊗ f_k} is basis of V⊗W. Universal property: bilinear maps V × W → X correspond uniquely to linear maps V ⊗ W → X.

Intuition:
- Tensor product encodes bilinear combinations as linear objects.

Example:
- For F^m ⊗ F^n ≅ F^{mn} with elementary tensors forming standard basis.

Pitfalls/checks:
- Not every element is simple tensor (elementary); general element is sum of simple tensors.

9.21 Identification F^m ⊗ F^n ≅ F^{m×n} and rank-one tensors
Definition/statement:
- Under identification, elementary tensor u⊗v corresponds to matrix u v^t (outer product), which is rank-one. Sum of such outer products yields arbitrary matrices.

Intuition:
- Tensor product and matrix spaces coincide; rank-one tensors generate whole space.

Example:
- (1,0)^T ⊗ (0,1)^T corresponds to matrix with 1 at (1,2) and zeros elsewhere.

Pitfalls/checks:
- Matrix rank equals minimal number of elementary tensors needed to express matrix; computing tensor rank can be difficult in general.

9.22 Inner product on tensor products and extensions to multiple tensor factors
Definition/statement:
- If V and W have inner products, define ⟨v1⊗w1, v2⊗w2⟩ = ⟨v1,v2⟩ ⟨w1,w2⟩ and extend bilinearly; gives inner product on V⊗W.

Intuition:
- Inner product on tensor product behaves multiplicatively on elementary tensors.

Example:
- For standard inner products on R^m and R^n, the induced inner product on matrices is Frobenius inner product ⟨A,B⟩ = tr(A^t B).

Pitfalls/checks:
- Ensure bilinearity and positive-definiteness extend properly; use orthonormal bases to simplify.

9.23 Volume scaling by linear maps: |det T| and volume (product of singular values connection)
Definition/statement:
- |det T| gives volume-scaling factor of T on n-dimensional parallelepipeds. Also |det T| = product of singular values of T (since singular values give principal stretchings).

Intuition:
- Determinant magnitude tells how volumes (Lebesgue measure) change under linear map.

Example:
- 2×2 matrix with singular values 3 and 2 scales area by 6.

Pitfalls/checks:
- Sign of determinant indicates orientation preservation or reversal; absolute value gives pure scaling.

End of guide.