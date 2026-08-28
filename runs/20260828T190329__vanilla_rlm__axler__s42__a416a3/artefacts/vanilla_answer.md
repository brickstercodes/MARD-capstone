# Study Guide — Linear Algebra Done Right (Axler) — Guided Path for First-Time Learners

Notes: Concepts are ordered so prerequisites appear earlier. Each entry gives a clear definition/intuitive comment, common pitfalls, and a short practice idea. Work through examples by hand and by small matrices/polynomials/vectors to build intuition.

---

## 1. Vector Spaces

### Scalars and the Field F (R or C)
- Definition: F denotes either R or C; its elements are scalars. Many theorems are stated uniformly for both.
- Intuition: Choose F before you build the vector space — changing the field changes scalar multiplication and many results (e.g., existence of eigenvalues).
- Pitfall: A real vector space may be considered as a complex vector space only after complexification.
- Practice: Verify a statement for a general scalar a ∈ F and check it works for both R and C.

### Complex numbers as a field (when F = C)
- Definition: z = a + bi with i^2 = −1; conjugation z̄ = a − bi; |z| = sqrt(a^2 + b^2).
- Intuition: C = R^2 as a real vector space; as a complex space, C is 1-dimensional.
- Pitfall: Inner products over C require conjugation in one slot.
- Practice: Multiply and conjugate some complex numbers; check |zw| = |z||w|.

### Lists, n‑tuples, and F^n
- Definition: A list (x1,...,xn) is an ordered n-tuple. F^n is the set of all n‑tuples with entries in F.
- Intuition: Lists encode coordinates; order matters.
- Pitfall: Distinguish lists from sets — (1,2) ≠ (2,1).
- Practice: Write vectors in C^4 and check coordinatewise operations.

### Vector space axioms; zero vector; additive inverses
- Definition: A vector space V over F is a set with addition V×V→V and scalar multiplication F×V→V satisfying the usual axioms (commutativity, associativity, identity 0, additive inverses, distributivity, scalar associativity, 1·v=v).
- Intuition: Think of F^n as the model example.
- Pitfall: A function with an additive constant is not linear (T(0) ≠ 0).
- Practice: Verify V=F^n satisfies all axioms.

### Operations in coordinates: coordinatewise addition and scalar multiplication
- Definition: (x1,...,xn)+(y1,...,yn)=(x1+y1,...,xn+yn); λ·(x1,...,xn)=(λx1,...,λxn).
- Intuition: Coordinatewise rules let you reduce problems to scalars.
- Practice: Compute examples in R^4 and C^3.

### Subspaces and the Subspace Test
- Definition: U ⊆ V is a subspace if 0 ∈ U and U is closed under addition and scalar multiplication.
- Intuition: A subspace is “a smaller vector space” that shares the same operations.
- Pitfall: A subset closed under addition but not scalar multiplication is not a subspace (e.g., positive real numbers).
- Practice: Test whether {(x,y,z): x+2y+3z=0} is a subspace of F^3.

### Linear combinations, span, and the smallest containing subspace
- Definition: Span of vectors v1,...,vm is all linear combinations a1 v1 + ... + am vm.
- Intuition: Span is the “all you can make” with given ingredients.
- Pitfall: Span of an empty list is {0} (convention).
- Practice: Show standard unit vectors span F^n.

### Sums of subspaces and direct sums
- Definition: U+W = {u+w : u∈U, w∈W}. The sum is direct, U⊕W, if every element has a unique decomposition (equivalently U∩W={0} for two subspaces).
- Intuition: Direct sums split vectors into distinct components from each piece.
- Pitfall: Union is not generally a subspace; use sums instead.
- Practice: For U={(x,0,0)}, W={(0,y,0)} in F^3 compute U+W and check U∩W.

---

## 2. Finite-Dimensional Spaces and Bases

### Finite-dimensional definition and examples
- Definition: V is finite-dimensional if some finite list spans V.
- Intuition: F^n, P_m(F) (polynomials of degree ≤ m) are standard finite-dimensional examples.
- Pitfall: The space of all polynomials P(F) is infinite-dimensional.
- Practice: Exhibit a finite spanning list for F^n and P_m(F).

### Linear independence and dependence
- Definition: v1,...,vm are independent if a1 v1 + ... + am vm = 0 implies all ai = 0; otherwise dependent.
- Intuition: Independent vectors are “nonredundant” directions.
- Pitfall: Presence of the zero vector in a list makes it dependent.
- Practice: Show the standard basis of R^n is independent.

### Basis: spanning + independence; coordinate uniqueness
- Definition: A basis is a list that both spans and is linearly independent. Coordinates relative to a basis are unique.
- Intuition: A basis gives the minimum “ingredients” to construct any vector.
- Pitfall: Order matters in a basis as a list when defining coordinate columns, though dimension and span do not.
- Practice: Verify a given pair of vectors in F^2 forms a basis by checking linear independence and span.

### Existence and extension/reduction principles
- Theorems: Every spanning list contains a basis (remove redundant vectors). Every independent list extends to a basis (adjoin vectors).
- Intuition: You can trim or complete lists to a basis.
- Practice: Reduce a spanning list in R^2 to a basis.

### Dimension and invariance of basis size
- Definition: dim V = number of vectors in any basis.
- Consequences: Any independent list has length ≤ any spanning list; in an n-dim space, any independent list of length n or any spanning list of length n is a basis.
- Pitfall: Beware mixing “dimension” with “number of nonzero coordinates” — dimension is basis length.
- Practice: Use dimension arguments to show no 4 independent vectors in R^3.

### Direct-sum complements
- Fact: If U ⊆ V and V finite-dimensional, extend a basis of U to a basis of V; the span of added vectors is a complementary subspace W with V = U ⊕ W.
- Practice: For a plane U in R^3, find W so R^3 = U ⊕ W.

### Dimension formula for subspace sums
- Formula: dim(U+W) = dim U + dim W − dim(U∩W).
- Practice: Compute dim of sum of two planes in R^3 that intersect in a line.

---

## 3. Linear Maps and Matrices

### Linear maps, L(V,W), and operators
- Definition: T: V → W is linear if T(u+v)=Tu+Tv and T(λv)=λ(Tv). Operators are maps V→V.
- Intuition: Linear maps preserve vector space structure.
- Pitfall: Nonlinear parts (constants, products) break linearity.
- Practice: Check linearity of differentiation operator on polynomials, and of affine maps on R.

### Examples and determining maps by basis images
- Fact: A linear map is determined uniquely by its values on a basis: given basis {v_k} of V and arbitrary {w_k} in W, there is a unique T with T(v_k)=w_k.
- Practice: Construct T from basis images and verify uniqueness.

### Nullspace (kernel), range (image), and subspace properties
- Definition: null T = {v: T v = 0}, range T = {T v : v ∈ V}; both are subspaces.
- Practice: For a matrix A, compute null(A) and range(A) and verify closure properties.

### Injectivity/surjectivity and characterization
- Facts: T is injective iff null T = {0}. T is surjective iff range T = W.
- Practice: Test injectivity/surjectivity of small matrices and relate to rank.

### Rank–nullity (fundamental theorem)
- Theorem: For finite-dimensional V, dim V = dim null T + dim range T.
- Consequences: If dim V > dim W there is no injective map V→W; if dim V < dim W no surjective map V→W.
- Practice: Given nullity, deduce rank and vice versa.

### Matrices: representation, matrix multiplication, and composition
- Definition: Fix bases; the matrix of T has columns equal to coordinates of T(v_k). Composition of linear maps corresponds to matrix multiplication.
- Practice: Compute matrices of simple maps and verify M(S∘T) = M(S) M(T).

### Column picture, rank, and transpose
- Insight: Multiplying A by a column vector gives a linear combination of A’s columns; column rank = row rank = rank(A).
- Practice: Compute independent columns and check row rank equals column rank.

### Invertible maps, isomorphisms, and equivalences
- Fact: T invertible ⇔ there exists S with ST = TS = I. For finite-dimensional V and W with equal dimension, injectivity ⇔ surjectivity ⇔ invertibility.
- Practice: For 2×2 matrices, test invertibility (det ≠ 0) and find inverses.

### Change of basis and similarity
- Fact: Matrix of the same operator in a different basis are similar: A' = C^{-1} A C. The change-of-basis matrix C is invertible.
- Pitfall: Similarity preserves eigenvalues but not individual entries.
- Practice: Compute similarity transforms for a simple basis change.

### Dual space, dual basis, and dual map
- Definition: V' = L(V, F). Given basis {v_k}, the dual basis {φ_k} satisfies φ_j(v_k)=δ_{jk}. For T:V→W, dual map T': W'→V' defined by T'(φ) = φ ∘ T.
- Intuition: Duals are “coordinate pickers”; dual map reverses arrows.
- Practice: Write coordinate functionals for F^3 and compute T' for a matrix T (matrix becomes transpose in coordinate representation).

### Quotient spaces and induced maps
- Definition: For U⊆V, V/U consists of cosets v+U. The quotient map π: V→V/U has kernel U; dim V/U = dim V − dim U.
- Fact: T induces ˜T: V/null T → range T which is an isomorphism.
- Practice: Describe R^2 / x-axis and compute π. Build induced ˜T for a simple T.

### Trace and basic properties
- Definition: tr(T) is the sum of diagonal entries of any matrix of T (basis independent). tr(AB) = tr(BA); trace is linear.
- Application: No linear operators S,T satisfy ST − TS = I on finite-dimensional spaces (trace argument).
- Practice: Compute trace for some matrices and verify invariance under similarity.

---

## 4. Polynomials

### Polynomial vector spaces and degree
- Definition: P(F) is space of polynomials; P_m(F) = degree ≤ m, with basis {1, z, ..., z^m}.
- Pitfall: Zero polynomial is special (degree convention −∞).
- Practice: Show dim P_m(F) = m+1.

### Division algorithm and factor theorem
- Theorems: For p and nonzero s, there exist unique q,r with p = s q + r and deg r < deg s. If p(λ)=0 then (z−λ) divides p.
- Practice: Divide polynomials and factor out linear factors using known roots.

### Zeros, uniqueness of coefficients, and interpolation
- Fact: A nonzero polynomial of degree m has at most m zeros; hence coefficients representation is unique. Given m+1 distinct points, there is a unique degree ≤ m polynomial interpolating them.
- Practice: Solve a small interpolation problem (quadratic through 3 points).

### Complex analysis facts: Fundamental Theorem of Algebra (FTA)
- Statement: Every nonconstant complex polynomial has a complex root; consequently, polynomials over C factor completely into linear factors.
- Consequence: Over R, nonreal roots occur in conjugate pairs; real polynomials factor into linear and irreducible quadratics.
- Practice: Factor z^3 − 1 over C and factor x^4 + 1 over R into quadratics.

---

## 5. Eigenvalues and Eigenvectors

### Operators, invariant subspaces, eigenvalues/eigenvectors
- Definition: For T: V→V, λ is an eigenvalue if there exists nonzero v with T v = λ v; eigenspace E(λ) = null(T − λ I).
- Intuition: Eigenvectors are directions preserved up to scaling by T; eigenspaces are invariant subspaces.
- Pitfall: Over R some operators (rotations) have no real eigenvalues — move to C when needed.
- Practice: Find eigenpairs of simple diagonal and rotation matrices.

### Characterizations and computations
- Fact: λ is eigenvalue ⇔ T − λ I not invertible ⇔ det(T − λ I) = 0 (characteristic polynomial).
- Practice: Solve det(A − λ I) = 0 for small matrices to find eigenvalues and eigenvectors.

### Powers and polynomials in T; minimal polynomial
- Definition: p(T) defined by polynomial p. The minimal polynomial m_T is the unique monic polynomial of least degree with m_T(T) = 0 (degree ≤ dim V).
- Facts: Eigenvalues are roots of m_T; q(T)=0 iff q divisible by m_T.
- Practice: Find m_T for a simple companion matrix or small Jordan block.

### Triangularization and eigenvalues on the diagonal
- Fact: Over C, every operator is triangularizable: there exists a basis making its matrix upper-triangular; diagonal entries are eigenvalues.
- Consequence: Every complex operator has at least one eigenvalue; odd-dimensional real spaces always have a real eigenvalue.
- Practice: Triangularize a 3×3 complex matrix by finding an eigenvector and restricting.

### Diagonalizability and criteria
- Definition: T is diagonalizable if V has a basis of eigenvectors (equivalently direct sum of eigenspaces).
- Criterion: T diagonalizable ⇔ minimal polynomial splits into distinct linear factors (no repeated roots).
- Practice: Check diagonalizability for matrices with repeated eigenvalues by computing eigenspace dimensions.

### Commuting operators and simultaneous diagonalization/triangularization
- Fact: Commuting diagonalizable operators can be simultaneously diagonalized; commuting operators over C can be simultaneously triangularized, which helps analyze S+T and ST on eigenvalues.
- Practice: Given commuting matrices, attempt joint diagonalization or triangularization.

### Applications: computing powers and recurrences
- Use: If T is diagonalizable, T^n easily computed in eigenbasis; used to solve linear recurrences (e.g., Fibonacci via matrix diagonalization).
- Practice: Diagonalize the Fibonacci matrix and derive Binet’s formula.

### Gershgorin disks (eigenvalue localization)
- Statement: Each eigenvalue of A lies in at least one Gershgorin disk centered at A_jj with radius sum of off-diagonal absolute values in that row.
- Use: Quick bounds and eigenvalue approximations.
- Practice: Compute Gershgorin disks for a sample matrix and locate eigenvalues approximately.

---

## 6. Inner Product Spaces

### Inner product and induced norm
- Definition: Inner product ⟨u,v⟩ is positive-definite, conjugate-symmetric, linear in one slot; norm ||v|| = sqrt(⟨v,v⟩).
- Intuition: Generalizes dot product to abstract spaces; gives angles, lengths.
- Pitfall: Over C, use conjugation in one slot when writing inner products.
- Practice: Verify ⟨f,g⟩ = ∫_{-1}^1 f g is an inner product on continuous real functions.

### Orthogonality, Pythagorean theorem, and orthogonal complements
- Definitions: u ⟂ v if ⟨u,v⟩ = 0. For subspace U, U^⊥ = {v: ⟨v,u⟩ = 0 ∀u∈U}. In finite dimensions V = U ⊕ U^⊥.
- Practice: Find orthogonal complement of span{(1,1,0)} in R^3.

### Projection and best approximation
- Fact: Every v decomposes uniquely v = u + w with u∈U and w∈U^⊥; u is the orthogonal projection P_U v and is the unique best approximation in U (minimizes ||v − u||).
- Practice: Project (3,1,2) onto span of (1,2,2).

### Orthonormal bases, Gram–Schmidt, and Parseval/Bessel
- Fact: Orthonormal basis: vectors of unit norm, mutually orthogonal; coefficients are inner products. Gram–Schmidt converts independent lists into orthonormal ones. Parseval: ||v||^2 = Σ |⟨v,e_k⟩|^2 for orthonormal basis.
- Practice: Apply Gram–Schmidt to {1,x,x^2} with inner product ∫_{−1}^1 p q.

### Riesz representation theorem (finite-dimensional)
- Statement: Every linear functional φ on an inner product space V can be written φ(v) = ⟨v,w⟩ for a unique w ∈ V.
- Use: Identifies V with its dual V' in the inner-product setting.
- Practice: Given φ(p)=∫ p(t) cos(πt) dt on P_2, find q with φ(p)=⟨p,q⟩.

### Pseudoinverse and least-squares (Moore–Penrose)
- Idea: For T: V→W, define T^† by inverting T on (null T)^⊥ and mapping W onto minimal-norm preimages; T^† gives minimal-norm solutions and best approximations (least-squares).
- Practice: Solve an overdetermined system Ax≈b by computing x = A^† b (via SVD or normal equations).

---

## 7. Operators on Inner Product Spaces (Spectral Theory & Matrix Factorizations)

### Adjoint operator T*
- Definition: T*: W→V satisfies ⟨T v, w⟩ = ⟨v, T* w⟩ for all v,w. In orthonormal bases, matrix of T* is the conjugate transpose (A* = Ā^T).
- Pitfall: Adjoint depends on the inner product; different bases that are not orthonormal change the relation to conjugate transpose.
- Practice: Compute T* for small matrices using standard inner product.

### Properties: self-adjoint, normal, and unitary operators
- Definitions:
  - Self‑adjoint (Hermitian): T = T* (matrix = conjugate transpose).
  - Normal: T T* = T* T.
  - Unitary (complex) / orthogonal (real): T* = T^{-1}; preserves norms/inner products.
- Facts:
  - Self-adjoint ⇒ eigenvalues real, diagonalizable with orthonormal eigenbasis.
  - Normal ⇔ unitarily diagonalizable (complex spectral theorem).
  - Eigenvectors for distinct eigenvalues of a normal operator are orthogonal.
- Practice: For given matrices, test self-adjointness, normality, or unitarity.

### Positive operators and square roots
- Definition: T positive if T = T* and ⟨T v, v⟩ ≥ 0 ∀ v. Every positive T has a unique positive square root √T.
- Practice: Diagonalize a symmetric positive matrix and take square roots of diagonal entries.

### QR factorization and isometries
- Fact: Any full-rank matrix A factors as A = Q R with Q having orthonormal columns (isometry) and R upper-triangular with positive diagonal. Gram–Schmidt produces Q.
- Use: Solve linear systems by back-substitution: Ax = b → R x = Q* b.
- Practice: Compute QR for a 3×2 matrix.

### T* T, singular values, and SVD
- Facts:
  - T* T is self-adjoint and positive; its eigenvalues are nonnegative.
  - Singular values s_k are sqrt(eigenvalues of T* T) arranged decreasingly.
  - SVD: T v = Σ_{k=1}^m s_k ⟨v, e_k⟩ f_k with orthonormal {e_k} in V and {f_k} in W.
  - A = B D C* is the matrix form: B,C have orthonormal columns and D diagonal with positive singular values.
- Uses: Compute operator norm (largest singular value), pseudoinverse (invert nonzero s_k), best low-rank approximations (truncate SVD).
- Practice: Compute SVD for a 2×2 or 3×2 matrix: find eigenvectors of A* A, build singular vectors, and verify decomposition.

### Operator norm and related properties
- Definition: ||T|| = max_{||v||≤1} ||T v|| = largest singular value.
- Properties: ||T*|| = ||T||, ||S T|| ≤ ||S|| ||T||, triangle inequality holds.
- Practice: Compute ||A|| via largest singular value from A* A.

### Polar decomposition
- Statement: T = U √(T* T), where U is unitary on the range of T and √(T* T) is positive. Separates rotation (unitary) and stretch (positive).
- Practice: For an invertible 2×2 matrix compute √(T* T) and then U = T (√(T* T))^{-1}.

### Cholesky factorization and positive definite matrices
- Fact: A positive definite matrix B factors as B = R* R (unique R upper-triangular with positive diagonal).
- Practice: Compute Cholesky factor for a 3×3 positive definite matrix.

### Geometric interpretation: mapping unit ball to ellipsoid
- Insight: T maps the unit ball to an ellipsoid whose principal axes are singular vectors scaled by singular values; volume scales by product of singular values (|det T|).
- Practice: For a 2×2 invertible matrix, draw how unit disk maps to ellipse via SVD.

---

## 8. Complex Operators and Jordan Canonical Form

### Increasing kernels and stabilization
- Fact: null T ⊆ null T^2 ⊆ ...; in finite dimensions the chain stabilizes at or before power n = dim V.
- Practice: Compute nullspaces for powers of a small matrix and note when they stabilize.

### Generalized eigenvectors and generalized eigenspaces
- Definitions: v is a generalized eigenvector for λ if (T−λ I)^k v = 0 for some k. G(λ,T) = {v: (T−λ I)^k v = 0 for some k} is the generalized eigenspace.
- Facts: Over C, V decomposes as ⊕_λ G(λ,T); each restriction (T−λI) on G(λ,T) is nilpotent.
- Practice: For an upper-triangular matrix, compute G(λ,T) as null((T−λI)^n).

### Nilpotent operators and Jordan chains
- Definition: T nilpotent if T^m = 0 for some m. Nilpotent operators have only eigenvalue 0 and admit Jordan chains.
- Fact: Every nilpotent operator has a Jordan basis of chains; its matrix can be put into blocks with 1s on the superdiagonal (strictly upper-triangular).
- Practice: For differentiation on P_m, identify nilpotency index and produce Jordan chains.

### Jordan normal form
- Theorem: Over C every operator has a Jordan basis and hence a Jordan canonical form — block-diagonal with Jordan blocks J_k(λ).
- Intuition: Jordan blocks encode minimal polynomial and sizes of generalized-eigenvector chains; geometric multiplicity = eigenspace dimension, algebraic multiplicity = size sum of Jordan blocks for that eigenvalue.
- Practice: Given a 3×3 matrix with single eigenvalue λ and minimal polynomial (z−λ)^2, compute a possible Jordan form (one 2×2 block and one 1×1 block).

### Characteristic and minimal polynomials; Cayley–Hamilton
- Definitions: Characteristic polynomial q_T(z) = det(z I − T). Cayley–Hamilton: q_T(T) = 0.
- Relation: Minimal polynomial divides characteristic polynomial. Trace equals sum of eigenvalues (with multiplicity); determinant equals product of eigenvalues.
- Practice: For a 2×2 matrix compute characteristic polynomial, check Cayley–Hamilton by substitution, and compare det with product of eigenvalues.

### Square roots and Jordan-form consequences
- Facts: I + nilpotent has a polynomial square root; any invertible complex operator has a square root obtained blockwise on generalized eigenspaces.
- Practice: Build a square root for a Jordan block with eigenvalue λ ≠ 0 using the nilpotent decomposition.

---

## 9. Multilinear Algebra, Determinants, and Tensors

### Bilinear and multilinear forms
- Definitions:
  - Bilinear form β: V×V → F linear in each slot.
  - m‑linear form: β: V^m → F linear in each argument.
- Intuition: Bilinear forms generalize dot products but need not be symmetric or positive.
- Practice: Given A, define β(x,y)=x^T A y; check bilinearity.

### Symmetric and alternating forms; decomposition
- Definitions: Symmetric: β(u,w)=β(w,u). Alternating: β(v,v)=0 (equivalently β(u,w)=−β(w,u)).
- Decomposition: Any bilinear form decomposes uniquely into symmetric + alternating parts: β = (β+β^T)/2 + (β−β^T)/2.
- Practice: For a given matrix A compute symmetric and alternating parts.

### Quadratic forms and diagonalization (principal axes)
- Fact: A quadratic form q(v) = β(v,v) corresponds to a unique symmetric form β and can be diagonalized (principal axes). Over R you can choose orthonormal diagonalization to identify signature.
- Practice: Diagonalize a quadratic form and classify it by positive/negative terms.

### Alternating n‑forms and determinant (basis-free)
- Facts:
  - On an n-dimensional space, alternating n-forms are 1-dimensional: any nonzero one is a scalar multiple of any other.
  - An alternating n-form is nonzero on a list exactly when the list is a basis.
  - Determinant: define det T by α(Tv1,...,Tvn) = (det T) α(v1,...,vn) for α an alternating n-form.
- Practice: Using the permutation expansion, compute determinant via α on basis images.

### Determinant properties and Leibniz expansion
- Facts:
  - Leibniz formula: det A = Σ_{σ∈S_n} sign(σ) Π_i A_{σ(i),i}.
  - Multiplicativity: det(ST) = det S · det T. Invertible iff det ≠ 0.
  - Row operations effect determinant predictably (swap → sign change; scale row → scale det; add multiple → no change).
- Practice: Compute determinant by row-reduction and track operation effects; verify det(AB) = det A det B.

### Volume, Hadamard’s inequality
- Fact: |det A| ≤ Π ||column_k||; equality iff columns orthogonal. Determinant geometrically equals signed volume scaling factor.
- Practice: Compare |det A| to product of column norms for a random 3×3 matrix.

### Tensor product V ⊗ W
- Definition (concrete view): V ⊗ W is the vector space spanned by formal simple tensors v ⊗ w, bilinear in each factor; bases {e_j⊗f_k} form a basis when {e_j},{f_k} are bases of V,W. dim(V⊗W)=dim V·dim W.
- Universal property: Bilinear maps V×W→U correspond uniquely to linear maps V⊗W→U.
- Inner product on tensor product: ⟨v⊗w, u⊗x⟩ = ⟨v,u⟩ ⟨w,x⟩; orthonormal bases produce orthonormal tensor bases.
- Practice: For V=R^2 and W=R^3 compute basis of V⊗W and represent a simple tensor as a matrix of rank 1.

---

## How to Practice and Study Effectively

- Work examples with small dimensions (n = 1,2,3). Many abstract statements are clarified by 2×2 or 3×3 matrices.
- Alternate between conceptual proofs and computational practice: prove a theorem once, then compute several instances.
- For spectral and SVD topics, compute A* A and eigenvectors numerically to build geometric intuition about singular vectors and ellipsoids.
- Use Gram–Schmidt to convert random independent lists into orthonormal bases; compare coordinates before and after.
- For Jordan theory, follow an operator with a single eigenvalue through construction of generalized eigenvectors and explicit Jordan blocks.
- Keep a one-page cheat-sheet of definitions (nullspace, range, eigenspace, minimal polynomial, characteristic polynomial, adjoint, SVD, etc.) and refer to it when solving problems.

---

This guide groups and orders the key ideas of Axler’s Linear Algebra Done Right so you can progress logically: build from fields and vector space axioms, through bases and dimension, to linear maps and matrices, then polynomials and eigenstructure, then inner-product geometry and operator theory, on to complex-operator canonical forms, and finish with multilinear algebra and determinants. Use the practice suggestions to internalize concepts and link the computational and theoretical viewpoints.