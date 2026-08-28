1. Complex numbers (C)
- Definition/Idea  
  Complex numbers are expressions a + b i with a,b ∈ R and i^2 = −1. Addition and multiplication follow distributivity and associativity; complex conjugation is defined by \overline{a+bi}=a−bi. The real numbers embed in C via a ↦ a+0i. The modulus |z| = √(z\overline{z}) gives a notion of size and distance.
- Key properties/theorems (Axler style)  
  Field axioms hold for C. Conjugation is an automorphism with \overline{zw}=\overline{z}\,\overline{w} and \overline{z+w}=\overline{z}+\overline{w}. Polar form: z = r e^{iθ} with r=|z| and θ arg(z). Nonzero z has inverse 1/z = \overline{z}/|z|^2.
- Small example/check  
  Compute (1+2i)(3−i)=3−i+6i−2i^2=3+5i+2=5+5i. Conjugate check: \overline{1+2i}=1−2i and |1+2i|=√5.
- Common pitfalls  
  Confusing i with an operator; forgetting noncommutativity is not an issue here (C is commutative). Mixing modulus and algebraic operations (e.g., |z+w| ≤ |z|+|w| must be used, not equality). Treating argument as single-valued (it’s multivalued modulo 2π).

2. Field (F) and scalars
- Definition/Idea  
  A field F is a set with two operations + and · satisfying commutative, associative, distributive laws, identities 0 and 1, additive inverses, and multiplicative inverses for nonzero elements. In linear algebra F will be either R or C; vectors are modules over F and scalars mean elements of F.
- Key properties/theorems (Axler style)  
  Fields allow solving linear equations and scalar multiplication in vector spaces. Characteristic 0 for R,C ensures repeated adding 1 never gives 0. Field structure underlies polynomial algebra F[z], important for minimal/characteristic polynomials.
- Small example/check  
  Verify 2·(a+b)=2a+2b for a,b∈F; for F=C check (1+i)^{-1} = (1−i)/2. In proofs, use field axioms when rearranging scalar expressions.
- Common pitfalls  
  Assuming properties that rely on an ordered field (e.g., positivity) when F=C: notions like > are not defined in C. Also avoid using topological/metric facts unless the field has that structure.

3. Lists / tuples and coordinates
- Definition/Idea  
  A list (or tuple) is an ordered finite sequence (v1,…,vn). Coordinate position matters; lists differ from sets. Lists index entries by position 1,…,n and allow linear combinations with ordered coefficients.
- Key properties/theorems (Axler style)  
  Lists give coordinates relative to a basis. Equality of lists requires equality of each coordinate. Permuting entries changes the list. Linear algebra constructions (span, independence) are defined for lists.
- Small example/check  
  The lists (1,2,3) and (3,2,1) in R^3 are distinct. Given basis (e1,e2), the coordinate list of v = 5e1 − e2 is (5,−1).
- Common pitfalls  
  Treating a list as an unordered set (loses ordering needed for matrices). Confusing list length with dimension until a basis is fixed.

4. F^n and coordinatewise operations
- Definition/Idea  
  F^n denotes lists of n scalars (a1,…,an). Addition and scalar multiplication are coordinatewise: (a+b)_j = a_j + b_j, (λa)_j = λ a_j. Standard basis e_j has a 1 in position j and 0 elsewhere.
- Key properties/theorems (Axler style)  
  F^n is an n‑dimensional vector space with basis (e_1,…,e_n). Coordinates relative to that basis are immediate. Linear maps from F^n correspond to n×m matrices acting on coordinate lists.
- Small example/check  
  In R^3, (1,0,2)+(0,3,1)=(1,3,3). Standard basis e_2=(0,1,0). Check linearity: A(αx+βy)=αAx+βAy for matrix A.
- Common pitfalls  
  Forgetting zero vector is (0,…,0). Treating scalars as vectors and vice versa; remember F is distinct from F^n except via embedding.

5. Vector space axioms
- Definition/Idea  
  A vector space V over field F is a set with operations + and scalar multiplication satisfying closure, associativity, commutativity of addition, additive identity 0, additive inverses, distributivity of scalar over vector addition and vice versa, scalar associativity, and 1·v=v.
- Key properties/theorems (Axler style)  
  From axioms derive uniqueness of 0 and additive inverses, 0·v=0, and (−1)v=−v. Subspaces inherit operations. All linear algebra results assume these axioms.
- Small example/check  
  Verify axioms in P(F) (polynomials): check (p+q)(x)=(p(x)+q(x)). For scalar associativity, (αβ)p = α(βp).
- Common pitfalls  
  Assuming multiplication of vectors is defined (it is not unless extra structure). Confusing algebraic properties that require extra structure, e.g., inner products.

6. Examples of vector spaces
- Definition/Idea  
  Important examples: F^n, sequence space F^∞ (all sequences), function space F^S (functions S→F), polynomial space P(F) (all polynomials). Operations are pointwise addition and scalar multiplication.
- Key properties/theorems (Axler style)  
  Many standard results manifest in examples: subspaces like polynomials of degree ≤ n form finite-dimensional spaces; P(F) is infinite-dimensional; evaluation maps are linear; differentiation is a linear operator on P(F).
- Small example/check  
  Check differentiation D: P(F)→P(F) is linear since D(αp+βq)=αp′+βq′. The set of sequences eventually zero is a subspace of F^∞.
- Common pitfalls  
  Forgetting dimension differences: P(F) is infinite-dimensional, so rank–nullity arguments require caution. Also ensure closedness under operations when proposing subspaces.

7. Subspace
- Definition/Idea  
  A subset U⊆V is a subspace if it is nonempty and closed under addition and scalar multiplication. Then U inherits the vector space structure from V.
- Key properties/theorems (Axler style)  
  Equivalent tests: U is a subspace iff 0∈U and for all u,v∈U and λ∈F we have u+v∈U and λu∈U. Intersections of subspaces are subspaces; sums U+W are subspaces.
- Small example/check  
  In R^3, U={ (x,y,0) } is a subspace. Check closure: sum and scalar multiples keep third coordinate 0. Verify 0∈U.
- Common pitfalls  
  Requiring U to be closed under subtraction is unnecessary if scalar multiplication by −1 is allowed. Mistaking arbitrary unions of subspaces for subspaces (not true).

8. Linear combination and span
- Definition/Idea  
  A linear combination of list v_1,…,v_m is ∑_{j} α_j v_j. The span of a list, span(v_1,…,v_m), is the set of all finite linear combinations; it is the smallest subspace containing the list.
- Key properties/theorems (Axler style)  
  Span is a subspace. A list spans V iff span(list)=V. Removing vectors outside the span doesn’t change span. Finite spans give finite-dimensional subspaces.
- Small example/check  
  In R^2, span((1,0),(0,1)) = R^2. Check that (3,4) ∈ span since 3(1,0)+4(0,1)=(3,4).
- Common pitfalls  
  Confusing span with linear combination of a single vector (span{v} is all scalar multiples). Assuming infinite spans produce finite-dimensional spaces without justification.

9. Linear independence / dependence
- Definition/Idea  
  A list (v_1,…,v_m) is linearly independent if the only scalars α_j with ∑ α_j v_j = 0 are all α_j = 0. Otherwise it is dependent; dependence means some vector is a linear combination of others.
- Key properties/theorems (Axler style)  
  Any sublist of a linearly independent list is independent. Adding a vector in the span makes the list dependent. Dependence relates to uniqueness of representation with respect to a basis.
- Small example/check  
  In R^3, (e_1,e_2,e_1+e_2) is dependent; coefficients (1,1,−1) give zero. The list (e_1,e_2,e_3) is independent.
- Common pitfalls  
  Equating independence with nonzero vectors; zero vector in a list makes it dependent. Confusing linear independence with orthogonality.

10. Finite-dimensional vector space
- Definition/Idea  
  V is finite-dimensional if it has a finite spanning list. This allows defining dimension and applying rank–nullity. Many constructive proofs rely on finite-dimensionality.
- Key properties/theorems (Axler style)  
  Finite-dimensional V has a basis of finite length. Subspaces of finite-dimensional spaces are finite-dimensional. Chains of subspaces stabilize by dimension arguments.
- Small example/check  
  P_n(F) (polynomials degree ≤ n) is finite-dimensional with basis 1, z, …, z^n. Verify any polynomial of degree ≤ n is a linear combination of these.
- Common pitfalls  
  Not all vector spaces are finite-dimensional (e.g., P(F), F^∞). Some theorems (rank–nullity) require finite-dimensional domain.

11. Basis and unique representation
- Definition/Idea  
  A basis is a linearly independent list that spans V. Every vector has a unique representation as a linear combination of basis vectors; coordinate maps relative to a basis give isomorphism V ≅ F^n.
- Key properties/theorems (Axler style)  
  Bases allow coordinate extraction: coordinates are unique. If (v_1,…,v_n) is a basis, then dim V = n. Change of basis is captured by invertible matrices.
- Small example/check  
  For P_2(F), basis (1, z, z^2). Express p(z)=3+2z−z^2 uniquely as 3·1 + 2·z + (−1)·z^2.
- Common pitfalls  
  Thinking any spanning list is a basis—span alone insufficient without independence. Confusing basis order—coordinate vectors depend on order.

12. Linear dependence lemma (reduction)
- Definition/Idea  
  If a list is linearly dependent, some vector equals a linear combination of previous ones (after reordering), so it can be removed without changing the span. This is the dependence lemma used to build bases.
- Key properties/theorems (Axler style)  
  The lemma lets one reduce a spanning list to a basis by deleting redundant vectors. It underpins the proof that any spanning list contains a basis.
- Small example/check  
  In R^3, list (e_1, e_2, e_1+e_2) is dependent; remove e_1+e_2 and span remains same as (e_1,e_2).
- Common pitfalls  
  Removing the “wrong” vector without checking earlier positions; ensure the dependence relation is arranged so the vector to delete lies in span of preceding ones.

13. Comparison of lengths (independent ≤ spanning)
- Definition/Idea  
  In a finite-dimensional V, any linearly independent list has length ≤ any spanning list. This yields bounds on possible sizes of independent sets and spanning sets.
- Key properties/theorems (Axler style)  
  Proof uses the dependence lemma: appending independent vectors to a spanning list forces dependence. Immediate consequences: size of basis is fixed; independent list longer than a spanning list impossible.
- Small example/check  
  In R^3 any independent list has ≤3 vectors. If you have four vectors in R^3 they must be dependent.
- Common pitfalls  
  Applying this inequality in infinite-dimensional spaces where lengths may not compare; forgetting finite-dimensional assumption.

14. Extending to a basis
- Definition/Idea  
  Any linearly independent list in a finite-dimensional V can be extended to a basis by adjoining vectors from V until the span equals V. This constructs bases containing given independent vectors.
- Key properties/theorems (Axler style)  
  Algorithmic proof: start with independent list and add vectors not in its span until spanning. This uses comparison of lengths to guarantee termination.
- Small example/check  
  In R^3, start with e_1; add e_2 and e_3 to get basis (e_1,e_2,e_3). For a nonstandard independent vector (1,1,0), adjoint e_3 and another to span R^3.
- Common pitfalls  
  Assuming extension is unique—many choices exist. Forgetting to check each added vector preserves independence.

15. Direct sum and sum of subspaces
- Definition/Idea  
  For subspaces V_1,…,V_m, the sum V_1+⋯+V_m = {v_1+⋯+v_m}. The sum is direct, denoted ⊕, if every vector has a unique representation as such a sum. For two subspaces U⊕W ⇔ U∩W={0} and V = U+W.
- Key properties/theorems (Axler style)  
  Direct sums give decompositions and facilitate block representations of linear maps. If V=U⊕W then dim V = dim U + dim W.
- Small example/check  
  In R^2, let U = span(e_1), W=span(e_2). Then R^2 = U⊕W and each (x,y) = x e_1 + y e_2 uniquely.
- Common pitfalls  
  Misidentifying sums as direct when intersection nontrivial. For more than two summands uniqueness requires trivial overlapping between all combinations.

16. Complementary subspace / decomposition V = U ⊕ W
- Definition/Idea  
  Given U⊆V finite-dimensional, a complementary subspace W satisfies V=U⊕W. One constructs W by extending a basis of U to a basis of V and letting W be the span of added vectors.
- Key properties/theorems (Axler style)  
  Complement exists for finite-dimensional subspaces. Complement is not unique. Projections and decompositions follow from choice of complement.
- Small example/check  
  In R^3 with U=span(e_1,e_2), extend to basis (e_1,e_2,e_3) and set W=span(e_3). Then V=U⊕W.
- Common pitfalls  
  Assuming a canonical complement; choice depends on extension. Infinite-dimensional complements require Zorn’s lemma in general.

17. Length invariance and dimension
- Definition/Idea  
  All bases of a finite-dimensional vector space V have the same length; this length is defined as dim V. Dimension is a fundamental invariant of V.
- Key properties/theorems (Axler style)  
  Use comparison of lengths to show any two bases have equal length. Dimension behaves well under direct sums: dim(U⊕W)=dim U+dim W.
- Small example/check  
  R^3 has dim 3 regardless of basis chosen; (e_1+e_2, e_2+e_3, e_3) is also a basis of length 3.
- Common pitfalls  
  Confusing dimension with cardinality of arbitrary generating sets (must be bases). Thinking dimension is defined only for F^n—it's general.

18. Dimension inequalities and basis tests
- Definition/Idea  
  For U⊆V finite-dimensional, dim U ≤ dim V. A list of length dim V is a basis iff it is independent or iff it spans. These give practical tests for basishood.
- Key properties/theorems (Axler style)  
  If an independent list has length dim V, it spans. If a spanning list has length dim V, it is independent. These are used to test bases without checking both properties.
- Small example/check  
  In R^3, any independent list of 3 vectors is a basis; any spanning list of 3 vectors is a basis. So if three vectors are independent, they automatically span R^3.
- Common pitfalls  
  Applying the tests when dimension is unknown. Using these in infinite-dimensional spaces is invalid.

19. Dimension formula for sums: dim(V1+V2)
- Definition/Idea  
  For subspaces V_1, V_2 of finite-dimensional V: dim(V_1+V_2) = dim V_1 + dim V_2 − dim(V_1∩V_2). This quantifies overlap.
- Key properties/theorems (Axler style)  
  The formula follows by choosing basis of intersection and extending to bases of V_1 and V_2. It tests direct sum: V_1+V_2 is direct iff dim(V_1+V_2)=dim V_1+dim V_2.
- Small example/check  
  In R^3, let V_1=span(e_1,e_2), V_2=span(e_2,e_3). Then dim(V_1∩V_2)=1, so dim(V_1+V_2)=2+2−1=3.
- Common pitfalls  
  Forgetting finite-dimensional requirement. Miscomputing intersection dimension without basis.

20. Product spaces and identification with direct sums
- Definition/Idea  
  External product V_1×⋯×V_m has coordinatewise operations. When each V_j is a subspace of V and the sum is direct, the internal direct sum is isomorphic to the product via Γ(v_1,…,v_m)=v_1+⋯+v_m.
- Key properties/theorems (Axler style)  
  V_1×V_2 is a vector space with dim equal to sum of dims. Γ is linear and bijective iff V = V_1⊕⋯⊕V_m. This identification explains block constructions.
- Small example/check  
  R^2 × R^3 ≅ R^5. If V=U⊕W then map (u,w)↦u+w is an isomorphism V≈U×W.
- Common pitfalls  
  Confusing product with direct sum when infinite index sets are involved (direct sum uses finite support).

21. Quotient spaces and cosets (V / U)
- Definition/Idea  
  For subspace U⊆V, coset v+U={v+u: u∈U}. The set of cosets V/U forms a vector space with (v+U)+(w+U)=(v+w)+U and scalar multiplication λ(v+U)=(λv)+U. The quotient map π: V→V/U sends v↦v+U with null π = U.
- Key properties/theorems (Axler style)  
  V/U has dimension dim V − dim U (finite-dimensional). Cosets partition V; operations are well-defined because U is a subspace.
- Small example/check  
  In R^2 with U=span(e_1), cosets are horizontal lines; V/U ≅ R with π(x,y)=y coordinate in appropriate identification.
- Common pitfalls  
  Treating representatives as unique—coset elements differ by vectors in U. Forgetting to check well-definedness when defining maps on quotient.

22. Induced map V/(null T) → range T (First Isomorphism)
- Definition/Idea  
  For T∈ℒ(V,W), define \widehat{T}: V/null T → range T by \widehat{T}(v + null T) = T v. This map is linear and injective; thus V/null T ≅ range T.
- Key properties/theorems (Axler style)  
  First Isomorphism Theorem: V/null T ≅ range T. Consequences: dim V = dim null T + dim range T (rank–nullity). This provides canonical reduction of T to an injective map.
- Small example/check  
  For T: R^2→R with T(x,y)=x, null T=span((0,1)), V/null T ≅ R, and \widehat{T} is an isomorphism onto range R.
- Common pitfalls  
  Forgetting the map is well-defined (must check T(v)=T(w) when v+null T = w+null T). Confusing domain and quotient.

23. Linear map (definition and examples)
- Definition/Idea  
  A map T: V→W is linear if T(u+v)=T u+T v and T(λv)=λ T v for all u,v∈V, λ∈F. Standard examples: zero map, identity, differentiation D on P(F), and matrix maps from F^n to F^m.
- Key properties/theorems (Axler style)  
  Linear maps preserve linear structure; images of subspaces are subspaces; preimages of subspaces are subspaces. Composition of linear maps is linear.
- Small example/check  
  Check D: P_2→P_1, D(az^2+bz+c)=2az+b is linear. Matrix A acting on coordinate vectors is linear: A(αx+βy)=αAx+βAy.
- Common pitfalls  
  Testing linearity only on basis elements may be insufficient unless the map is defined by images on a basis; also confusing multiplicative maps with linear maps.

24. ℒ(V,W) as a vector space; algebra of linear maps
- Definition/Idea  
  ℒ(V,W) is the set of linear maps V→W; it is a vector space under pointwise addition and scalar multiplication. When V=W, ℒ(V) has an algebra structure with composition as multiplication.
- Key properties/theorems (Axler style)  
  dim ℒ(V,W) = (dim V)(dim W) for finite-dimensional spaces. Composition is associative; identity map I ∈ ℒ(V) acts as multiplicative identity.
- Small example/check  
  For V=W=R^2, ℒ(V) corresponds to 2×2 matrices. Sum of two linear maps corresponds to sum of matrices.
- Common pitfalls  
  Treating ℒ(V,W) as function space without linearity—only linear maps belong. Composition order matters (noncommutative in general).

25. Null space and injectivity
- Definition/Idea  
  null T = {v∈V : T v = 0} is a subspace of V. T is injective iff null T = {0}. Null space measures failure of injectivity.
- Key properties/theorems (Axler style)  
  Null T is invariant under scalar multiplication and addition. If null T = {0} and V finite-dimensional, dim range T = dim V (by rank–nullity) so T is surjective iff codomain dimension matches.
- Small example/check  
  For T: R^2→R with T(x,y)=x, null T=span((0,1)) so not injective. Check T(0,1)=0.
- Common pitfalls  
  Confusing null T with preimage of singleton other than 0. Overlooking that null T is basis-dependent but subspace property is intrinsic.

26. Range and surjectivity
- Definition/Idea  
  range T = {T v : v∈V} is a subspace of codomain W. T is surjective iff range T = W. Range measures what outputs T can produce.
- Key properties/theorems (Axler style)  
  Range is invariant under linear combinations. For finite-dimensional V, dim range T ≤ dim W and rank–nullity ties range dimension to nullity.
- Small example/check  
  For matrix A = [[1,0],[0,0]] mapping R^2→R^2, range A = span(e_1); not surjective because e_2 not in range.
- Common pitfalls  
  Assuming surjectivity from injectivity without equal dimensions. Miscomputing range by only looking at images of a few vectors.

27. Fundamental theorem of linear maps (rank–nullity)
- Definition/Idea  
  For finite-dimensional V and T∈ℒ(V,W), dim V = dim null T + dim range T. This is the rank–nullity theorem (Axler’s Fundamental Theorem).
- Key properties/theorems (Axler style)  
  Immediate corollaries: if null T = {0} then dim range T = dim V; if dim V > dim W then T cannot be injective; if dim V < dim W then T cannot be surjective.
- Small example/check  
  For T: R^3→R^2, rank–nullity implies nullity ≥ 1 since dim V =3 and dim range ≤2. Example: projection onto first two coordinates has nullity 1.
- Common pitfalls  
  Applying rank–nullity to infinite-dimensional V without modification. Forgetting to compute dimensions correctly.

28. Linear map determined by images of a basis
- Definition/Idea  
  Given a basis (v_1,…,v_n) of V and arbitrary vectors w_1,…,w_n in W, there is a unique linear map T: V→W with T v_j = w_j for each j. This constructs linear maps from basis images.
- Key properties/theorems (Axler style)  
  Uniqueness follows from linearity and unique representation; existence by defining T on basis and extending linearly. This is fundamental for matrix representation.
- Small example/check  
  For V=R^2 with basis (e_1,e_2) and choose w_1=(1,0), w_2=(0,2), then T(x,y)=x(1,0)+y(0,2) = (x,2y).
- Common pitfalls  
  Attempting to define T by images of a dependent list—must use a basis (independent spanning list).

29. Matrices of linear maps & matrix operations
- Definition/Idea  
  Relative to bases, a linear map T: V→W is represented by a matrix whose j-th column is the coordinate list of T(v_j) where (v_j) is a basis of V and (w_i) is a basis of W. Matrix operations mirror linear map operations.
- Key properties/theorems (Axler style)  
  ℳ(S+T)=ℳ(S)+ℳ(T), ℳ(λT)=λℳ(T), and ℳ(S∘T)=ℳ(S)ℳ(T) when bases are appropriately chosen. Matrix multiplication corresponds to composition; columns represent images of basis vectors.
- Small example/check  
  For T: R^2→R^2 with T(x,y)=(x+2y,3x+y), matrix in standard basis is [[1,2],[3,1]]. Check T(e_2) column is (2,1).
- Common pitfalls  
  Mixing up row-major/column-major conventions; Axler uses column vectors and column representation. Forgetting to align domain/codomain bases when composing.

30. Matrix multiplication and change of basis (similarity)
- Definition/Idea  
  Matrix multiplication corresponds to composition of linear maps. Changing basis transforms matrix A to B by similarity: B = C^{-1} A C where C is the change-of-basis matrix from old to new basis.
- Key properties/theorems (Axler style)  
  Similar matrices represent the same linear operator under different bases; invariants under similarity include determinant, trace, eigenvalues, minimal and characteristic polynomials.
- Small example/check  
  In R^2 rotate basis by C; compute new matrix B = C^{-1}AC. If A=I, then B=I regardless of C.
- Common pitfalls  
  Using wrong order for C and C^{-1}; forgetting that similarity requires same linear operator, not just two arbitrary matrices.

31. Rank; column and row ranks and factorization
- Definition/Idea  
  Rank of a matrix (or map) is dimension of its column space (or range). Column rank equals row rank. Low-rank matrices admit factorizations A = C R with C having independent columns and R having independent rows.
- Key properties/theorems (Axler style)  
  Column rank = row rank (rank theorem). Factorization yields A = [columns basis]·[coordinate matrix], making rank transparent. Rank is invariant under multiplication by invertible matrices.
- Small example/check  
  A = [[1,2],[2,4]] has rank 1 since second column is twice first. Factor as A = [ [1],[2] ]·[1,2].
- Common pitfalls  
  Mistaking nullity with rank. Assuming rank equals number of nonzero entries; it's about linear independence of columns/rows.

32. Invertible linear maps and isomorphisms
- Definition/Idea  
  T∈ℒ(V,W) is invertible if there exists S with S∘T=I_V and T∘S=I_W. For finite-dimensional spaces of same dimension, invertibility ⇔ bijectivity ⇔ matrix is invertible.
- Key properties/theorems (Axler style)  
  Inverse is unique and linear. Two finite-dimensional vector spaces are isomorphic iff they have same dimension. Invertibility preserved under similarity; det ≠ 0 characterizes invertibility.
- Small example/check  
  Matrix [[1,0],[0,2]] is invertible with inverse [[1,0],[0,1/2]]. For T(x,y)=(x,2y), inverse T^{-1}(u,v)=(u,v/2).
- Common pitfalls  
  Forgetting domain/codomain must match to speak of inverse. For infinite-dimensional spaces invertibility is subtler.

33. Determinant via alternating n-forms (placeholder/bridge)
- Definition/Idea  
  The determinant can be defined as the scalar by which T acts on the 1‑dimensional space of alternating n‑linear forms (top forms): for ω an alternating n‑form, (T·ω)(v_1,…,v_n)=ω(Tv_1,…,Tv_n) = (det T) ω(v_1,…,v_n).
- Key properties/theorems (Axler style)  
  This yields multiplicativity det(ST)=det S · det T and characterizes invertibility: det T ≠ 0 ⇔ T invertible. It aligns with Leibniz formula and volume scaling.
- Small example/check  
  For diagonal matrix diag(d_1,…,d_n), det = ∏ d_j since columns scale basis top form by each diagonal entry.
- Common pitfalls  
  Confusing determinant sign conventions; ensure alternating forms orientation consistent. For complex fields, determinant is complex-valued.

34. Eigenvalues, eigenvectors, and invariant subspaces
- Definition/Idea  
  λ∈F is an eigenvalue of T∈ℒ(V) if ∃ nonzero v with T v = λ v; such v is an eigenvector. An invariant subspace U satisfies T(U)⊆U; eigenspaces E(λ,T) are 1‑dimensional invariant subspaces when λ distinct.
- Key properties/theorems (Axler style)  
  Eigenvalues correspond to zeros of characteristic polynomial; eigenvectors for distinct eigenvalues are linearly independent. Invariant subspaces reduce operator complexity.
- Small example/check  
  For T represented by [[2,0],[0,3]], eigenvalues 2 and 3 with eigenvectors e_1 and e_2. Check T e_1 = 2 e_1.
- Common pitfalls  
  Assuming every operator has eigenvalues over R (need C in general). Confusing eigenvectors with arbitrary invariant vectors.

35. Polynomials of operators and evaluation p(T)
- Definition/Idea  
  For polynomial p(z)=∑ a_j z^j define p(T)=∑ a_j T^j ∈ ℒ(V). This functional calculus allows building operators from polynomials.
- Key properties/theorems (Axler style)  
  p(T)q(T)=(pq)(T). If v is eigenvector with T v = λ v then p(T) v = p(λ) v. Polynomials that annihilate T lead to the minimal polynomial.
- Small example/check  
  For T with T^2 = T, p(z)=z^2 − z gives p(T)=0. Check p(T) v = 0 for all v.
- Common pitfalls  
  Treating formal polynomial evaluation as substitution of scalar—operator composition order matters but for polynomials in a single operator it's straightforward.

36. Complex polynomials: factor theorem and FTA
- Definition/Idea  
  Over C, every nonconstant polynomial factors into linear factors (Fundamental Theorem of Algebra). Division algorithm and factor theorem let one decompose polynomials and locate roots.
- Key properties/theorems (Axler style)  
  For p∈C[z], p(z) = c∏ (z−λ_j) with multiplicities. Over R, nonreal roots occur in conjugate pairs yielding real quadratic irreducible factors.
- Small example/check  
  z^2+1 factors over C as (z−i)(z+i). Use synthetic division to divide polynomials.
- Common pitfalls  
  Forgetting multiplicity of roots and its effect on minimal/characteristic polynomials. Overlooking complex conjugation when working over R.

37. Minimal polynomial
- Definition/Idea  
  The minimal polynomial m_T(z) is the monic polynomial of least degree with m_T(T)=0. It divides every polynomial that annihilates T and captures algebraic properties of T.
- Key properties/theorems (Axler style)  
  m_T divides characteristic polynomial χ_T. The minimal polynomial’s linear factors and multiplicities control triangularizability and Jordan blocks. Eigenvalues are roots of m_T.
- Small example/check  
  If T is diagonalizable with eigenvalues 2 and 3, m_T(z)=(z−2)(z−3). If T satisfies (T−I)^2=0 but not (T−I)=0, then m_T(z)=(z−1)^2.
- Common pitfalls  
  Confusing minimal polynomial with characteristic polynomial; minimal polynomial has smaller or equal degree and need not equal χ_T.

38. Eigenvalues as zeros of minimal polynomial; multiplicity relations
- Definition/Idea  
  Eigenvalues of T are precisely roots of m_T. The minimal polynomial encodes necessary multiplicities for each eigenvalue corresponding to the size of largest Jordan block.
- Key properties/theorems (Axler style)  
  If p(T)=0 then m_T divides p. Distinct linear factors in m_T ⇔ T diagonalizable. Multiplicity in χ_T relates to algebraic multiplicity; size in m_T relates to maximal Jordan block size.
- Small example/check  
  For T with Jordan blocks of sizes 2 and 1 at λ=1, m_T(z)=(z−1)^2 while χ_T(z)=(z−1)^3.
- Common pitfalls  
  Believing algebraic multiplicity equals geometric multiplicity—only equal exactly when diagonalizable. Confusing multiplicities in m_T and χ_T.

39. Upper‑triangular matrices and invariant flags
- Definition/Idea  
  A linear operator has an upper-triangular matrix relative to a basis if there exists a flag (nested sequence) {0}=V_0⊂V_1⊂⋯⊂V_n=V of invariant subspaces with dim V_k = k. Triangular matrices ease reading eigenvalues on diagonal.
- Key properties/theorems (Axler style)  
  An operator is triangularizable iff there exists such an invariant flag. Diagonal entries of an upper-triangular matrix are eigenvalues; triangularization reduces many proofs to 1D steps.
- Small example/check  
  Matrix [[2,1],[0,3]] is upper-triangular; invariant flag: span(e_1)⊂span(e_1,e_2). Diagonal entries 2 and 3 are eigenvalues.
- Common pitfalls  
  Assuming triangular entries imply diagonalizability—triangularizable does not imply diagonalizable. Over R some operators may not be triangularizable if polynomial doesn’t split.

40. Triangularization criterion (splitting of minimal polynomial) and Schur's theorem
- Definition/Idea  
  T is triangularizable over F iff its minimal polynomial splits over F into linear factors. Over C, by Schur's theorem, every operator on finite-dimensional inner-product space has an upper-triangular matrix with respect to an orthonormal basis; in particular every operator is triangularizable.
- Key properties/theorems (Axler style)  
  Schur gives unitary (orthonormal) triangularization: there exists an orthonormal basis making matrix upper-triangular (over C). Triangularization simplifies spectrum and invariant-subspace arguments.
- Small example/check  
  For any complex 2×2 matrix A, Schur provides unitary U with U* A U upper-triangular. For A=[[0,−1],[1,0]] (rotation by 90°), over C we get triangularization.
- Common pitfalls  
  Over R Schur need not apply; real matrices may require complexification. Confusing triangularization with diagonalization.

41. Diagonalizable operators and eigenspace direct-sum criterion
- Definition/Idea  
  T is diagonalizable if there exists a basis of eigenvectors; equivalently V = ⊕_{λ} E(λ,T) (direct sum of eigenspaces). Diagonalizability simplifies powers and functional calculus.
- Key properties/theorems (Axler style)  
  T diagonalizable ⇔ minimal polynomial splits into distinct linear factors. Eigenvectors for distinct eigenvalues are independent; algebraic and geometric multiplicities must align.
- Small example/check  
  T with matrix [[2,0],[0,3]] is diagonalizable; eigenbasis (e_1,e_2). If A=[[1,1],[0,1]] (Jordan block) is not diagonalizable.
- Common pitfalls  
  Interpreting diagonalizable only in C; some real operators diagonalizable over C but not over R if complex eigenvalues present.

42. Gershgorin discs and eigenvalue localization
- Definition/Idea  
  Gershgorin discs for matrix A have centers a_{jj} and radii R_j = ∑_{k≠j} |a_{jk}|. Every eigenvalue lies in at least one of these discs; used to bound spectra and infer invertibility.
- Key properties/theorems (Axler style)  
  Gershgorin’s theorem: spectrum ⊆ ∪ D(a_{jj},R_j). If a disc is disjoint from others, it contains exactly one eigenvalue (counting multiplicity).
- Small example/check  
  For A = [[4,0.5],[0.1,3]], discs D(4,0.5) and D(3,0.1) contain eigenvalues near 4 and 3 respectively.
- Common pitfalls  
  Discs give inclusion, not exact locations. Radii use row sums (or column sums) consistently.

43. Commuting operators and simultaneous triangularization/diagonalization
- Definition/Idea  
  If operators commute, they preserve each other's eigenspaces. A commuting family of operators that is triangularizable can often be simultaneously triangularized; commuting diagonalizable operators are simultaneously diagonalizable under suitable hypotheses.
- Key properties/theorems (Axler style)  
  Over C, any commuting family of operators on finite-dimensional V can be simultaneously triangularized. If operators are diagonalizable and commute, there exists a basis of common eigenvectors (simultaneous diagonalization).
- Small example/check  
  Diagonal matrices commute and are simultaneously diagonalizable with standard basis. Two commuting 2×2 rotations by same axis are simultaneously diagonalizable only over C.
- Common pitfalls  
  Commutativity is essential; noncommuting diagonalizable operators need not be simultaneously diagonalizable. Simultaneous diagonalization may fail without diagonalizability.

44. Sequence of null spaces null T^k and stabilization
- Definition/Idea  
  For T∈ℒ(V), consider chain null T ⊆ null T^2 ⊆ … . In finite-dimensional V this chain stabilizes: there exists m with null T^m = null T^{m+1} = … . Stabilization is used to define generalized eigenspaces.
- Key properties/theorems (Axler style)  
  Dimensions of null T^k are nondecreasing and bounded by dim V, hence eventually constant. Once stabilized, T maps the stabilized space into itself nilpotently.
- Small example/check  
  For a nilpotent Jordan block J with J^n=0, null J^k grows until k=n when it equals whole space.
- Common pitfalls  
  Assuming stabilization occurs in one step; need to check up to dimension V. Infinite-dimensional spaces may not stabilize.

45. Generalized eigenvectors and generalized eigenspaces G(λ,T)
- Definition/Idea  
  A generalized eigenvector for eigenvalue λ satisfies (T−λI)^k v = 0 for some k≥1. The generalized eigenspace G(λ,T)=null (T−λI)^n (for dim V = n) collects all generalized eigenvectors associated to λ.
- Key properties/theorems (Axler style)  
  G(λ,T) is invariant and finite-dimensional; restriction (T−λI)|_{G(λ,T)} is nilpotent. Generalized eigenspaces corresponding to distinct eigenvalues intersect trivially.
- Small example/check  
  For Jordan block J_λ of size 3, G(λ,J)=span of chain vectors v, (T−λI)v, (T−λI)^2 v giving whole 3‑dimensional block.
- Common pitfalls  
  Confusing generalized eigenvectors with eigenvectors (generalized ones include chains). Using wrong exponent—should go up to n for dim V.

46. Nilpotent operators and Jordan nilpotent blocks
- Definition/Idea  
  N∈ℒ(V) is nilpotent if N^m=0 for some m. Jordan nilpotent blocks are strictly upper-shift matrices with zeros on diagonal and ones on superdiagonal representing nilpotent action in a suitable basis.
- Key properties/theorems (Axler style)  
  Minimal polynomial of nilpotent N is z^m for some m. Nilpotent operators decompose into direct sum of Jordan nilpotent blocks; sizes correspond to chain lengths.
- Small example/check  
  N = [[0,1,0],[0,0,1],[0,0,0]] satisfies N^3=0 but N^2≠0. Its minimal polynomial is z^3.
- Common pitfalls  
  Mistaking nilpotency order for dimension; minimal m may be less than dim V. Confusing nilpotent with zero operator.

47. Generalized eigenspace decomposition (over C)
- Definition/Idea  
  Over C, V decomposes as direct sum of generalized eigenspaces: V = ⊕_{k} G(λ_k,T) where λ_k run over distinct eigenvalues. On each G(λ_k,T), T−λ_k I is nilpotent.
- Key properties/theorems (Axler style)  
  Decomposition is canonical; restriction to each generalized eigenspace reduces study of T to nilpotent parts. This decomposition underlies Jordan canonical form.
- Small example/check  
  For T with eigenvalues 1 and 2, split V into G(1,T)⊕G(2,T). Check T maps each summand to itself.
- Common pitfalls  
  Over R this decomposition may require complexification if eigenvalues are nonreal. Ensure eigenvalues considered are over algebraic closure.

48. Jordan basis and Jordan canonical form
- Definition/Idea  
  A Jordan basis organizes generalized eigenvectors into chains producing block-diagonal Jordan form: blocks J_λ with λ on diagonal and 1’s on superdiagonal. Jordan form classifies complex operators up to similarity.
- Key properties/theorems (Axler style)  
  The sizes and multiplicities of Jordan blocks are invariants of similarity. Jordan form gives explicit structure: characteristic polynomial and minimal polynomial deduced from block sizes.
- Small example/check  
  Matrix with Jordan blocks J_2(2) (2×2 block at λ=2) and J_1(3) is block-diagonal with [[2,1],[0,2]] and [3].
- Common pitfalls  
  Assuming Jordan form is always diagonalizable; only when all block sizes are 1. Computing Jordan form requires algebraic and geometric multiplicities.

49. Characteristic polynomial and Cayley–Hamilton theorem
- Definition/Idea  
  Characteristic polynomial χ_T(z) = det(zI − T) is a degree-n polynomial whose roots are eigenvalues (with algebraic multiplicity). Cayley–Hamilton: χ_T(T) = 0 (operator annihilates its characteristic polynomial).
- Key properties/theorems (Axler style)  
  deg χ_T = dim V. Coefficients relate to trace and determinant (up to sign). Cayley–Hamilton used to express higher powers of T in lower-degree polynomials.
- Small example/check  
  For 2×2 A, χ_A(z)=z^2 − (tr A) z + det A. Verify Cayley–Hamilton by direct substitution into matrix polynomial.
- Common pitfalls  
  Confusing characteristic and minimal polynomials. Using Cayley–Hamilton without ensuring polynomial acts on the same space (must substitute operator T).

50. Trace of an operator and spectral relations
- Definition/Idea  
  tr T is the sum of diagonal entries of any matrix representing T; it is basis-independent. For operator T, tr T equals sum of eigenvalues counting algebraic multiplicity (over algebraic closure).
- Key properties/theorems (Axler style)  
  Linearity: tr(S+T)=tr S + tr T. Cyclic property: tr(ST)=tr(TS). Coefficients of characteristic polynomial satisfy relations; determinant equals product of eigenvalues.
- Small example/check  
  For A=[[2,1],[0,3]], tr A = 5 and eigenvalues 2,3 sum to 5. Check tr(AB)=tr(BA) numerically for small matrices.
- Common pitfalls  
  Forgetting dependence on algebraic multiplicity. Using trace to infer eigenvalues without full spectral info.

51. Bilinear forms and quadratic forms
- Definition/Idea  
  A bilinear form β: V×V→F is linear in each slot. A quadratic form q(v)=β(v,v) arises from β (when symmetric). Bilinear forms are represented by matrices relative to bases.
- Key properties/theorems (Axler style)  
  Symmetric part S=(β+β^T)/2 determines q via polarization: β_sym(u,v)= (q(u+v)−q(u)−q(v))/2. Change of basis transforms matrix by congruence.
- Small example/check  
  On R^2, β((x,y),(u,v))=xu+2yv is bilinear; matrix relative to standard basis is [[1,0],[0,2]]. Quadratic form q(x,y)=x^2+2y^2.
- Common pitfalls  
  Over C bilinearity vs sesquilinearity matters for inner products. Not every quadratic form determines a unique bilinear form over fields of characteristic 2.

52. Symmetric and alternating bilinear forms; decomposition
- Definition/Idea  
  Any bilinear form β decomposes uniquely as symmetric part β_sym and alternating part β_alt where β_sym(u,v)= (β(u,v)+β(v,u))/2 and β_alt=(β−β^T)/2. Alternating forms satisfy β(v,v)=0.
- Key properties/theorems (Axler style)  
  Symmetric forms correspond to symmetric matrices; alternating forms correspond to skew-symmetric matrices. Alternating forms vanish on dependent lists and have special properties in even/odd dimensions.
- Small example/check  
  β with matrix [[0,1],[-1,0]] is alternating: β(v,v)=0 for all v. Symmetric example: [[2,1],[1,3]] gives β_sym.
- Common pitfalls  
  Over C, skew-Hermitian differs from alternating. For characteristic ≠2 use the 1/2 formulas; characteristic 2 needs care.

53. Diagonalization of symmetric forms (real orthogonal diagonalization)
- Definition/Idea  
  Real symmetric matrices (or symmetric bilinear forms over R) can be diagonalized by an orthogonal change of basis: A = Q^T D Q with Q orthogonal and D diagonal. This leads to signature and definiteness classification.
- Key properties/theorems (Axler style)  
  Spectral theorem for real symmetric matrices yields orthonormal eigenbasis and real eigenvalues. Sylvester’s law of inertia: signature (#positive, #negative) invariant under congruence.
- Small example/check  
  A = [[2,1],[1,2]] has eigenvalues 3 and 1 with orthonormal eigenvectors; diagonalize by orthogonal Q.
- Common pitfalls  
  Confusing similarity diagonalization with congruence; symmetric matrices diagonalize orthogonally (congruence) rather than via arbitrary similarity.

54. Alternating m-linear forms and top forms
- Definition/Idea  
  An alternating m-linear form ω: V^m→F changes sign when swapping two arguments and vanishes on dependent lists. On an n-dimensional space, alternating n-forms (top forms) form a 1‑dimensional space.
- Key properties/theorems (Axler style)  
  Alternating forms detect linear independence: ω(v_1,…,v_n) ≠ 0 iff v_1,…,v_n is a basis. The top forms transform by determinant under change of basis.
- Small example/check  
  In R^2, ω((x_1,x_2),(y_1,y_2)) = x_1 y_2 − x_2 y_1 is alternating and nonzero for basis pairs.
- Common pitfalls  
  Assuming alternating forms are symmetric; they are antisymmetric. Counting dimensions: number of alternating m-forms is C(n,m), but top forms (m=n) give 1-dimensional space.

55. Determinant of a matrix (Leibniz formula and properties)
- Definition/Idea  
  Determinant det A is a scalar defined by the Leibniz sum over permutations or equivalently by action on top alternating forms. It is multiplicative det(AB)=det A det B and zero iff A singular.
- Key properties/theorems (Axler style)  
  Determinant changes sign upon swapping columns, scales linearly in each column, and equals volume-scaling factor. Triangular matrices have determinant product of diagonal entries.
- Small example/check  
  For A=[[a,b],[c,d]], det A = ad−bc. For upper-triangular [[2,1],[0,3]], det=6.
- Common pitfalls  
  Computational errors in signs from permutations. Confusing determinant with permanent (no signs).

56. Hadamard and Vandermonde determinants (inequalities and formulas)
- Definition/Idea  
  Hadamard’s inequality: |det A| ≤ ∏_{j} ‖col_j‖ with equality iff columns orthogonal up to scaling. Vandermonde determinant gives closed form det [x_i^{j−1}] = ∏_{i<j} (x_j − x_i).
- Key properties/theorems (Axler style)  
  Hadamard bounds volume in terms of column lengths; Vandermonde shows determinant zero iff repeated x_i. These are useful in polynomial interpolation and conditioning.
- Small example/check  
  For 2×2 Vandermonde with x_1,x_2, determinant = x_2 − x_1. For orthonormal columns, Hadamard equality gives |det|=1.
- Common pitfalls  
  Applying Hadamard without column orthogonality check. Using Vandermonde over fields where subtraction may vanish.

57. Multilinear maps and tensor product V ⊗ W
- Definition/Idea  
  Tensor product V⊗W is the linear space generated by formal symbols v⊗w subject to bilinearity relations; it linearizes bilinear maps via a universal property: bilinear maps V×W→X correspond uniquely to linear maps V⊗W→X.
- Key properties/theorems (Axler style)  
  Simple tensors span V⊗W; if bases {e_j} and {f_k} then {e_j⊗f_k} is a basis for V⊗W, giving dim V⊗W = dim V · dim W. Tensor product behaves functorially.
- Small example/check  
  For V=W=R^2 with standard bases, basis of V⊗W has four elements e_1⊗f_1, e_1⊗f_2, e_2⊗f_1, e_2⊗f_2. Map bilinear β→ linearization on tensor.
- Common pitfalls  
  Believing every tensor is simple v⊗w—general tensors are sums of simple tensors. Confusing tensor product with direct product.

58. Inner product and norm
- Definition/Idea  
  Inner product ⟨·,·⟩ is a positive-definite bilinear form (sesquilinear conjugate-linear in first or second slot over C) giving norm ‖v‖=√⟨v,v⟩. It induces geometry: angles, orthogonality, projections.
- Key properties/theorems (Axler style)  
  Cauchy–Schwarz: |⟨u,v⟩| ≤ ‖u‖‖v‖. Triangle inequality: ‖u+v‖≤‖u‖+‖v‖. Inner products allow orthonormal bases and Riesz representation.
- Small example/check  
  Standard inner product on C^n: ⟨x,y⟩ = ∑ \overline{x_j} y_j. Check ⟨e_i,e_j⟩ = δ_{ij}.
- Common pitfalls  
  Over C, forgetting conjugation in inner product leads to contradictions (e.g., positivity fails). Confusing bilinear and sesquilinear conventions.

59. Orthonormal lists and orthonormal basis
- Definition/Idea  
  An orthonormal list consists of unit vectors mutually orthogonal. An orthonormal basis is an orthonormal list that spans V; coordinates are simple: v = ∑ ⟨v,e_k⟩ e_k.
- Key properties/theorems (Axler style)  
  Orthonormal bases simplify computations: matrix of linear functional and adjoint are conjugate-transposes. Existence guaranteed in finite-dimensional inner-product spaces via Gram–Schmidt.
- Small example/check  
  In R^2, {(1/√2)(1,1),(1/√2)(1,−1)} is orthonormal. Compute coordinates of (1,0) by inner products.
- Common pitfalls  
  Assuming orthogonality implies spanning (need completeness/basis). Confusing orthonormal with orthogonal (which need not have unit length).

60. Gram–Schmidt orthonormalization
- Definition/Idea  
  Gram–Schmidt converts a linearly independent list into an orthonormal list with the same span by orthogonalizing and normalizing sequentially. It constructs orthonormal bases in finite-dimensional spaces.
- Key properties/theorems (Axler style)  
  Process yields orthonormal list (e_1,…,e_n) with span preserved. Numerically sensitive but conceptually straightforward. Used to produce QR factorizations.
- Small example/check  
  Starting with (1,1) and (1,0) in R^2: subtract projection to orthogonalize and normalize to get orthonormal pair.
- Common pitfalls  
  Applying Gram–Schmidt to dependent lists yields division by zero; must start with independent lists and be careful about numerical instability.

61. Bessel’s inequality and Parseval’s identity
- Definition/Idea  
  For orthonormal list (e_k), Bessel: ∑ |⟨v,e_k⟩|^2 ≤ ‖v‖^2. If the list is an orthonormal basis, equality holds (Parseval): ‖v‖^2 = ∑ |⟨v,e_k⟩|^2, and v = ∑ ⟨v,e_k⟩ e_k.
- Key properties/theorems (Axler style)  
  Bessel gives projection error bounds. Parseval expresses energy conservation in orthonormal expansions and underlies Fourier analysis and SVD components.
- Small example/check  
  For v=(1,0) and orthonormal basis e_1=(1/√2)(1,1), e_2=(1/√2)(1,−1), compute coefficients and verify Bessel and Parseval.
- Common pitfalls  
  Applying Parseval when basis is incomplete. Miscomputing inner products in complex spaces without conjugation.

62. Orthogonal complement U^⊥ and direct-sum decomposition V = U ⊕ U^⊥
- Definition/Idea  
  U^⊥ = {v∈V : ⟨v,u⟩=0 ∀u∈U} is a subspace. For finite-dimensional inner-product spaces, V = U ⊕ U^⊥ when U is finite-dimensional; dim relations hold and (U^⊥)^⊥ = U.
- Key properties/theorems (Axler style)  
  dim U + dim U^⊥ = dim V. Orthogonal complements allow projection and decomposition. Double orthogonal identity holds in finite-dimensions.
- Small example/check  
  In R^3, U=span(e_1,e_2) has U^⊥ = span(e_3). Then any v decomposes uniquely as u + w with u∈U, w∈U^⊥.
- Common pitfalls  
  For infinite-dimensional spaces, closure issues arise (topology needed). Assuming U∩U^⊥={0} without checking finite-dimensionality may mislead.

63. Orthogonal projection P_U and best approximation
- Definition/Idea  
  P_U: V→U is the orthogonal projection mapping v to its U-component in V=U⊕U^⊥. It is linear, idempotent (P_U^2=P_U), with range U and null U^⊥. P_U v is the unique best approximation to v from U minimizing ‖v−u‖.
- Key properties/theorems (Axler style)  
  If (e_k) is orthonormal basis of U, P_U v = ∑ ⟨v,e_k⟩ e_k. Projection is self-adjoint: P_U^* = P_U. Best approximation property follows from orthogonality of error.
- Small example/check  
  Project v=(1,2,3) onto U=span(e_1,e_2) in R^3 by dropping third coordinate: P_U v = (1,2,0).
- Common pitfalls  
  Confusing orthogonal projection with arbitrary linear projection; only orthogonal ones minimize norm. Using non-orthonormal bases complicates formulas.

64. Riesz representation theorem and dual identification
- Definition/Idea  
  In finite-dimensional inner-product space V, every linear functional φ ∈ V′ can be written φ(u)=⟨u,v⟩ for a unique v∈V. This identifies V with its dual V′ via the Riesz map.
- Key properties/theorems (Axler style)  
  The map v↦φ_v where φ_v(u)=⟨u,v⟩ is an isomorphism V ≅ V′. Norms on functionals correspond to norms of representing vectors.
- Small example/check  
  For V=R^2 with standard inner product, the functional φ(x,y)=2x+3y corresponds to v=(2,3).
- Common pitfalls  
  Treating Riesz as valid without an inner product—requires inner-product structure. Over C be mindful of conjugate-linearity convention.

65. Adjoints T* and basic properties
- Definition/Idea  
  For T∈ℒ(V,W) between inner-product spaces, the adjoint T*∈ℒ(W,V) is defined by ⟨T v,w⟩ = ⟨v,T* w⟩ for all v,w. It generalizes conjugate-transpose of matrices in orthonormal bases.
- Key properties/theorems (Axler style)  
  (ST)* = T* S*, (T*)* = T, and (λT)* = \overline{λ} T*. In orthonormal bases, matrix of T* is conjugate-transpose: ℳ(T*) = ℳ(T)^*.
- Small example/check  
  For T: C^2→C^2 with matrix [[1,2],[3,4]] in orthonormal basis, T* matrix is conjugate transpose [[1̄,3̄],[2̄,4̄]] (here all real so transpose).
- Common pitfalls  
  Mixing up adjoint and inverse; T* exists for all bounded linear maps in finite dimensions but is not inverse unless T unitary. Conjugation matters over C.

66. Self‑adjoint (Hermitian) operators and properties
- Definition/Idea  
  T is self-adjoint (Hermitian) if T* = T. Self-adjoint operators generalize real symmetric matrices; they have real eigenvalues and orthogonal eigenvectors for distinct eigenvalues.
- Key properties/theorems (Axler style)  
  Eigenvalues are real; eigenspaces for distinct eigenvalues are orthogonal; spectral theorem applies: self-adjoint operators are orthogonally diagonalizable (over R: real symmetric).
- Small example/check  
  Matrix [[2,1],[1,3]] is symmetric and hence self-adjoint; eigenvalues are real (computed as roots of z^2−5z+5).
- Common pitfalls  
  Assuming self-adjoint implies positive—need check ⟨T v,v⟩≥0 for positivity. Over C verify Hermitian condition with conjugation.

67. Normal operators
- Definition/Idea  
  T is normal if TT* = T*T. Normal operators include self-adjoint, unitary, and normal matrices; they are diagonalizable by a unitary matrix over C.
- Key properties/theorems (Axler style)  
  For normal T, ‖T v‖ = ‖T* v‖ for all v. Spectral theorem: normal ⇔ there exists an orthonormal basis of eigenvectors (over C). Commuting with adjoint characterizes normality.
- Small example/check  
  A unitary matrix U satisfies U U* = I = U* U, hence normal. Rotation matrix in R^2 (real orthogonal) is normal.
- Common pitfalls  
  Normal does not imply diagonalizable over R if eigenvalues are complex; normal requires matching multiplicity behavior.

68. Spectral theorem (real and complex)
- Definition/Idea  
  Over C: T normal ⇔ there exists an orthonormal eigenbasis; T is unitarily diagonalizable. Over R: self-adjoint ⇔ orthogonally diagonalizable. Spectral theorem enables functional calculus for normal/self-adjoint operators.
- Key properties/theorems (Axler style)  
  Decompose T = Σ λ_j P_j where P_j are orthogonal projections onto eigenspaces. Functions of T can be defined by applying function to eigenvalues on each eigenspace.
- Small example/check  
  For self-adjoint A with eigenpairs (λ_j,e_j), write A = ∑ λ_j ⟨·,e_j⟩ e_j. Compute √A by taking square roots of λ_j ≥ 0.
- Common pitfalls  
  Over R, require self-adjointness for orthogonal diagonalization; normality alone might not suffice for real orthogonal diagonalization.

69. Positive and positive-definite operators/matrices
- Definition/Idea  
  T is positive if ⟨T v,v⟩ ≥ 0 for all v; positive-definite if strict >0 for v≠0. On self-adjoint operators, positivity ⇔ eigenvalues nonnegative.
- Key properties/theorems (Axler style)  
  Positive operators are self-adjoint. They admit factorizations T = R* R and have unique positive square roots. Positive-definite matrices are invertible.
- Small example/check  
  A = [[2,0],[0,3]] is positive-definite; ⟨A v,v⟩ = 2x^2+3y^2 >0 for v≠0.
- Common pitfalls  
  Confusing positive with entry-wise positivity. Positivity depends on inner product and operator, not just matrix entries.

70. Square root of a positive operator
- Definition/Idea  
  For positive T there exists unique positive √T with (√T)^2 = T. Construct via spectral theorem by taking nonnegative square roots of eigenvalues in an orthonormal eigenbasis.
- Key properties/theorems (Axler style)  
  √T commutes with T and is polynomially bounded in finite-dimensions. Uniqueness follows from positivity and functional calculus.
- Small example/check  
  For diag(4,9), √T = diag(2,3). Verify (√T)^2 = diag(4,9)=T.
- Common pitfalls  
  Assuming square roots exist for nonpositive self-adjoints; negative eigenvalues prevent real square roots.

71. Isometries and unitary (orthogonal) operators
- Definition/Idea  
  An isometry S preserves norms: ‖S v‖ = ‖v‖. A unitary (orthogonal in R) operator satisfies S* S = I (equivalently S^{-1} = S*). Columns of unitary matrices form orthonormal bases.
- Key properties/theorems (Axler style)  
  Unitary operators preserve inner products: ⟨S u, S v⟩=⟨u,v⟩. Unitaries are normal and diagonalizable on C when spectrum available. Determinant of unitary has modulus 1.
- Small example/check  
  Rotation matrix in R^2 is orthogonal with determinant 1 and preserves norms. Verify S* S = I for given S.
- Common pitfalls  
  Confusing isometry with surjectivity; an isometry between spaces of same finite dimension is unitary (bijective), but in general one must check surjectivity.

72. QR factorization
- Definition/Idea  
  Any matrix A with linearly independent columns factors as A = Q R where Q has orthonormal columns (Q^* Q = I) and R is upper-triangular with positive diagonal entries. Construct via Gram–Schmidt.
- Key properties/theorems (Axler style)  
  QR is unique under positivity convention on R diagonals. Useful for solving least-squares and computing orthonormal bases from column spaces.
- Small example/check  
  For A = [ (1,1,0)^T, (1,0,1)^T ], apply Gram–Schmidt to columns to form Q and compute R by Q^* A.
- Common pitfalls  
  Columns must be independent for full QR; otherwise use reduced QR or pivoting. Normalization sign choices affect uniqueness.

73. Cholesky factorization
- Definition/Idea  
  For positive-definite Hermitian B, there exists unique upper-triangular R with positive diagonal such that B = R* R (or lower-triangular L with B = L L*). This is Cholesky factorization.
- Key properties/theorems (Axler style)  
  Useful for solving symmetric positive-definite systems efficiently and for numerical stability. Existence relies on positivity.
- Small example/check  
  For B = [[4,2],[2,3]], compute R such that R* R = B; solution gives R ≈ [[2,1],[0,1]].
- Common pitfalls  
  B must be positive-definite; otherwise Cholesky fails (pivoting or modifications required). Numerical rounding can break positive-definiteness.

74. T* T, singular values and SVD
- Definition/Idea  
  For T∈ℒ(V,W), T* T is positive on V. Singular values s_k are √(eigenvalues of T* T). SVD expresses T as T = Σ s_k ⟨·, e_k⟩ f_k with orthonormal e_k in V and f_k in W.
- Key properties/theorems (Axler style)  
  SVD exists for any finite-dimensional operator; singular values are nonnegative, ordered s_1≥s_2≥... The rank equals number of nonzero singular values.
- Small example/check  
  For A=[[3,0],[0,4]], singular values are 4 and 3 (ordering). SVD coincides with diagonalization in this orthonormal setting.
- Common pitfalls  
  Confusing singular values with eigenvalues of T; they are eigenvalues of T* T, hence always nonnegative. SVD involves two orthonormal bases.

75. Adjoint and pseudoinverse via SVD; Moore–Penrose pseudoinverse
- Definition/Idea  
  Using SVD T = Σ s_k ⟨·, e_k⟩ f_k, the adjoint T* = Σ s_k ⟨·, f_k⟩ e_k. Moore–Penrose pseudoinverse T† = Σ (1/s_k) ⟨·, f_k⟩ e_k inverting nonzero singular values.
- Key properties/theorems (Axler style)  
  T† yields least-squares least-norm solutions. Properties: T T† is orthogonal projection onto range T; T† T projects onto (null T)^⊥. T† is unique satisfying Moore–Penrose equations.
- Small example/check  
  For diagonal A=[[3,0],[0,0]], pseudoinverse is [[1/3,0],[0,0]]. Check A A† projects onto first coordinate.
- Common pitfalls  
  Inverting zero singular values must be avoided. Pseudoinverse depends on SVD; numerically computing small singular values is delicate.

76. Operator norm and best low-rank approximations (Eckart–Young)
- Definition/Idea  
  Operator norm ‖T‖ = max_{‖v‖≤1} ‖T v‖ equals largest singular value s_1. Truncated SVD yields best rank-k approximations in operator norm; error equals s_{k+1}.
- Key properties/theorems (Axler style)  
  Eckart–Young theorem: best approximation of rank ≤ k to T in operator norm is obtained by keeping top k singular values and corresponding singular vectors.
- Small example/check  
  For T with singular values 5,3,1, best rank-1 approximation has error 3 in operator norm. Compute truncated SVD and verify.
- Common pitfalls  
  Using Frobenius-norm optimality interchangeably; operator norm and Frobenius norm have different optimal truncated approximations (SVD optimal in both but errors differ).

77. Polar decomposition
- Definition/Idea  
  Any T∈ℒ(V,W) factors as T = S √(T* T) where √(T* T) is positive and S is partial isometry/unitary on range appropriate subspace. Analogue of polar form r e^{iθ}.
- Key properties/theorems (Axler style)  
  √(T* T) is positive; S is unique on (null T)^⊥ and maps eigenvectors of √(T* T) to corresponding images under T. Polar decomposition useful in numerical and conceptual analysis.
- Small example/check  
  For invertible A, S = A (A* A)^{-1/2} is unitary and A = S √(A* A). For diagonal positive A, S is identity.
- Common pitfalls  
  For noninvertible T, S need not be unitary on whole space, only partial isometry. Confusing polar S with unitary in general.

78. Ellipsoids, parallelepipeds and volume scaling via singular values
- Definition/Idea  
  T maps unit ball to ellipsoid whose principal semi-axes lengths are singular values s_k. Volume scaling factor equals product ∏ s_k, which equals |det T| when T is square.
- Key properties/theorems (Axler style)  
  Singular values describe geometric distortion; determinant equals signed product of eigenvalues but absolute value equals product of singular values (volume scaling).
- Small example/check  
  For diag(3,2), unit circle maps to ellipse with axes 3 and 2; area scales by 6 which equals |det|.
- Common pitfalls  
  Confusing singular values with eigenvalues (signs and complex values). Volume scaling uses absolute determinant; sign gives orientation.

79. Pseudoinverse properties and least-squares interpretation
- Definition/Idea  
  T† gives minimal-norm solution among all least-squares minimizers. Properties: T T† = P_{range T}, T† T = P_{(null T)^⊥}. For given w, v = T† w minimizes ‖T v − w‖ and among minimizers has least norm.
- Key properties/theorems (Axler style)  
  Pseudoinverse yields orthogonal projection behavior and satisfies Moore–Penrose equations uniquely. Useful in solving inconsistent linear systems by best approximation.
- Small example/check  
  For overdetermined A with full column rank, least-squares solution x = (A* A)^{-1} A* b equals A† b. Check residual orthogonality A*(Ax−b)=0.
- Common pitfalls  
  Using pseudoinverse in ill-conditioned contexts without regularization. Confusing Moore–Penrose pseudoinverse with left/right inverses in nonsquare cases.

80. Nilpotent Jordan chains and generalized Jordan structure
- Definition/Idea  
  Jordan chains are sequences v, (T−λI)v, (T−λI)^2 v, … forming generalized eigenvector chains that produce Jordan blocks. Nilpotent part within each generalized eigenspace is organized by chain lengths.
- Key properties/theorems (Axler style)  
  Chains generate G(λ,T) and block sizes deduced from chain lengths. Structure theorem: operator decomposes into direct sum of Jordan blocks corresponding to chains.
- Small example/check  
  For nilpotent N with chains length 3 and 2, Jordan blocks are sizes 3 and 2 yielding N in block-diagonal Jordan nilpotent form.
- Common pitfalls  
  Miscounting chain lengths and thereby Jordan block sizes. Overlooking multiplicity interactions across eigenvalues.

81. Square roots of invertible operators over C
- Definition/Idea  
  Over C every invertible operator T has a square root S with S^2 = T. Construct via Jordan form: on each Jordan block write block as λ(I+N) with N nilpotent and use binomial series (polynomial) to take square root.
- Key properties/theorems (Axler style)  
  Existence follows since scalar square roots exist in C and nilpotent parts allow polynomial square roots. Uniqueness fails in general (multiple choices of branch for each eigenvalue).
- Small example/check  
  For diagonalizable invertible A with eigenvalues λ_j, choose square roots μ_j and define S with μ_j on diagonal. For Jordan blocks, adjust with polynomial in N.
- Common pitfalls  
  Over R some invertible matrices have no real square root. Branch choices for square roots of eigenvalues yield multiple square roots.

82. Bilinear functionals space B(V,W) and matrix congruence
- Definition/Idea  
  B(V,W) is space of bilinear maps V×W→F of dimension (dim V)(dim W). Matrices of bilinear forms change by congruence: for change-of-basis C, new matrix B' = C^T B C (or conjugate-transpose in complex case).
- Key properties/theorems (Axler style)  
  Congruence classifies bilinear forms up to change of basis (Sylvester law for symmetric forms). Dimension counting matches matrix size expectations.
- Small example/check  
  For V=R^2 and bilinear β with matrix [[1,0],[0,1]], under basis change C, compute congruent B' = C^T C.
- Common pitfalls  
  Confusing similarity (A↦C^{-1}AC) with congruence (A↦C^T A C). Use correct transform for bilinear forms.

83. Alternating n‑forms detect bases; determinant via alternation
- Definition/Idea  
  A top alternating n-form ω evaluates nonzero exactly on oriented bases; the determinant of linear map T is the scalar by which T acts on ω: ω(Tv_1,…,Tv_n) = (det T) ω(v_1,…,v_n). This gives an invariant definition of determinant.
- Key properties/theorems (Axler style)  
  Determinant multiplicativity and invertibility criterion follow. Alternating forms vanish on dependent lists, so ω nonzero on a list ⇔ they form a basis.
- Small example/check  
  For standard ω(e_1,…,e_n)=1, compute ω(T e_1,…,T e_n)=det T. For 2×2 check ω((a,c),(b,d))=ad−bc.
- Common pitfalls  
  Orientation matters: sign convention for ω affects determinant sign. Over complex fields orientation is subtler but determinant defined via alternating tensor.

84. Tensor products of multiple spaces and inner products on tensors
- Definition/Idea  
  Extend tensor product to multiple factors V_1⊗⋯⊗V_m with basis tensors from bases of each factor. If factors have inner products, define inner product on simple tensors by ⟨⊗ v_j, ⊗ w_j⟩ = ∏ ⟨v_j,w_j⟩ and extend linearly.
- Key properties/theorems (Axler style)  
  Multilinear universal property holds. Inner product on tensor products makes basis tensors orthonormal when factors’ bases are orthonormal. Dimensional multiplicativity holds.
- Small example/check  
  For V⊗V with orthonormal basis e_i, e_j, simple tensors e_i⊗e_j are orthonormal. Verify inner product multiplicativity on simple tensors.
- Common pitfalls  
  Believing inner product defined this way makes all tensors simple; general tensors are linear combinations. Keeping track of conjugation in complex case is essential.

85. Alternating multilinear forms and determinant formulas (Leibniz & permutation)
- Definition/Idea  
  Alternating n-linear forms can be expanded by permutations (Leibniz formula): ω(v_1,…,v_n) = ∑_{σ∈S_n} sgn(σ) ∏ entries when ω is determinant form. This underlies determinant permutation formula.
- Key properties/theorems (Axler style)  
  Expand determinants and alternating forms via permutations; multiplicativity of determinant derives from properties of alternating forms. Permutation sign encodes antisymmetry.
- Small example/check  
  For 3×3 determinant, expand along permutations; verify simple numeric example to match computed determinant.
- Common pitfalls  
  Miscounting permutations or dealing incorrectly with repeated vectors (which make alternating form zero).

86. Final synthesis: operator classification and functional calculus
- Definition/Idea  
  Bring together triangularization, diagonalization, Jordan form, SVD, polar decomposition, and Cayley–Hamilton to analyze and compute functions of operators. Use spectral decompositions where possible; use Jordan form for precise algebraic structure; use SVD/polar for geometry and numerics.
- Key properties/theorems (Axler style)  
  Functional calculus: for diagonalizable T, f(T)=Σ f(λ_j) P_j. Cayley–Hamilton gives polynomial relations. SVD gives best approximations and pseudoinverse. Jordan form classifies similarity classes over C.
- Small example/check  
  Compute e^{T} for diagonalizable T by exponentiating eigenvalues; for T with Jordan blocks, use Jordan exponential formula involving polynomials times e^{λ}. Use SVD to approximate ill-conditioned T.
- Common pitfalls  
  Applying diagonal-based functional calculus to non-diagonalizable operators without Jordan analysis. Overlooking numerical instability when switching between factorizations; choose spectral methods for theory and SVD/polar for numerics.