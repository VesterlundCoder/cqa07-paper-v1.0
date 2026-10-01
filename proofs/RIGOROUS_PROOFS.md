# CQA07: Rigorous Theorem Proofs

## Notation and Task Definition

### Single-Copy Task

**Inputs:**
- Alice receives $x^A \in \{00, 01, 10, 11\}$
- Bob receives $x^B \in \{00, 01, 10, 11\}$

**Index function:** $I(x) = 2x_1 + x_2 \in \{0, 1, 2, 3\}$

**Outputs:**
- Alice produces $y^A = (y_1^A, y_2^A) \in \{0,1\}^2$
- Bob produces $y^B = (y_1^B, y_2^B) \in \{0,1\}^2$

**Virtual outputs (3 components each):**
- Alice: $\tilde{y}^A = (y_1^A, y_2^A, y_1^A \oplus y_2^A \oplus 1)$
- Bob: $\tilde{y}^B = (y_1^B, y_2^B, y_1^B \oplus y_2^B)$

**Winning predicate:**

$$W(x^A, x^B, y^A, y^B) = \begin{cases} 1 & \text{if } I(x^A) = 0 \text{ or } I(x^B) = 0 \\ 1 & \text{if } \tilde{y}^B_{I(x^A)} = \tilde{y}^A_{I(x^B)} \\ 0 & \text{otherwise} \end{cases}$$

where $\tilde{y}^A_j, \tilde{y}^B_j$ denote the $j$-th components (1-indexed, $j \in \{1,2,3\}$).

**Hard inputs:** Inputs with $I(x) \in \{1,2,3\}$ (i.e., $x \in \{01, 10, 11\}$).
**Easy inputs:** Inputs with $I(x) = 0$ (i.e., $x = 00$). These auto-win.

### n-Fold Parallel Task

For $n$ independent copies:
- $X_A = (x_1^A, \ldots, x_n^A) \in \{00,01,10,11\}^n$
- $X_B = (x_1^B, \ldots, x_n^B) \in \{00,01,10,11\}^n$
- $Y_A = (y_1^A, \ldots, y_n^A)$, $Y_B = (y_1^B, \ldots, y_n^B)$

**Global winning predicate:**

$$W_n(X_A, X_B, Y_A, Y_B) = \bigwedge_{i=1}^{n} W(x_i^A, x_i^B, y_i^A, y_i^B)$$

### Communication Model

A deterministic one-way protocol with $B$ bits:
- **Encoder:** $e: \{00,01,10,11\}^n \to \{0,1\}^B$
- **Alice output:** $f: \{00,01,10,11\}^n \to (\{0,1\}^2)^n$
- **Bob output:** $g: \{00,01,10,11\}^n \times \{0,1\}^B \to (\{0,1\}^2)^n$

**Success probability (uniform over inputs):**

$$S_n(B) = \max_{e,f,g} \Pr_{X_A, X_B}[W_n(X_A, X_B, f(X_A), g(X_B, e(X_A))) = 1]$$

**Communication complexity:**

$$B^*(n, q) = \min\{B : S_n(B) \geq q\}$$

---

## Lemma 1: Single-Copy Compatibility

### Definition

A set $S \subseteq \{01, 10, 11\}$ of hard Alice inputs is **compatible** if there exist functions $f: S \to \{0,1\}^2$ and $g: \{00,01,10,11\} \to \{0,1\}^2$ such that:

$$\forall x^A \in S, \quad \forall x^B \in \{00,01,10,11\}: \quad W(x^A, x^B, f(x^A), g(x^B)) = 1$$

**Quantifier order:** $\exists f, \exists g \quad \forall x^A \in S \quad \forall x^B: \quad W = 1$.

Note: Alice's output $f(x^A)$ depends only on $x^A$ (not $x^B$). Bob's output $g(x^B)$ depends only on $x^B$ (there is no message in the single-copy case; the message is the compatibility class label).

### Statement

**Lemma 1.** $S \subseteq \{01, 10, 11\}$ is compatible if and only if $|S| \leq 2$.

### Proof

**(⟸) Any 2-element subset is compatible.**

There are three 2-element subsets: $\{01, 10\}$, $\{01, 11\}$, $\{10, 11\}$.

For each, we exhibit explicit $f$ and $g$:

**Case $S = \{01, 10\}$ (I-values 1 and 2):**

Alice outputs $f(01) = (0, 0)$, $f(10) = (0, 0)$.
- Alice virtual: $\tilde{y}^A(01) = (0, 0, 1)$, $\tilde{y}^A(10) = (0, 0, 1)$.

Bob outputs $g(x^B) = (0, 0)$ for all $x^B$.
- Bob virtual: $\tilde{y}^B = (0, 0, 0)$.

Check: For $x^A \in \{01, 10\}$ and $x^B$ hard:
- If $I(x^B) = 1$: need $\tilde{y}^B_{I(x^A)} = \tilde{y}^A_1 = 0$. Since $\tilde{y}^B_1 = 0$ and $\tilde{y}^B_2 = 0$, this holds for $I(x^A) \in \{1,2\}$.
- If $I(x^B) = 2$: need $\tilde{y}^B_{I(x^A)} = \tilde{y}^A_2 = 0$. Same.
- If $I(x^B) = 3$: need $\tilde{y}^B_{I(x^A)} = \tilde{y}^A_3 = 1$. But $\tilde{y}^B_1 = 0, \tilde{y}^B_2 = 0$, so need $I(x^A) = 3$. But $I(x^A) \in \{1,2\}$, so $\tilde{y}^B_{I(x^A)} \in \{0, 0\} \neq 1$.

**This fails!** Let me redo this more carefully.

Actually, the compatibility is more subtle. Let me reconsider.

For $S = \{01, 10\}$, we need $f$ and $g$ such that for all $x^A \in S$ and all $x^B$:

$$\tilde{y}^B_{I(x^A)} = \tilde{y}^A_{I(x^B)}$$

where $I(x^A) \in \{1, 2\}$ and $I(x^B) \in \{0, 1, 2, 3\}$.

For $I(x^B) = 0$ (easy): auto-win. ✓

For $I(x^B) \in \{1, 2, 3\}$ (hard):
- Need $\tilde{y}^B_{I(x^A)} = \tilde{y}^A_{I(x^B)}$ for $I(x^A) \in \{1, 2\}$.

Let $\tilde{y}^A = (a_1, a_2, a_3)$ where $a_3 = a_1 \oplus a_2 \oplus 1$.
Let $\tilde{y}^B = (b_1, b_2, b_3)$ where $b_3 = b_1 \oplus b_2$.

Constraints (for $I(x^B) = 1$): $b_{I(x^A)} = a_1$ for $I(x^A) \in \{1, 2\}$, i.e., $b_1 = a_1$ and $b_2 = a_1$.
Constraints (for $I(x^B) = 2$): $b_{I(x^A)} = a_2$ for $I(x^A) \in \{1, 2\}$, i.e., $b_1 = a_2$ and $b_2 = a_2$.
Constraints (for $I(x^B) = 3$): $b_{I(x^A)} = a_3$ for $I(x^A) \in \{1, 2\}$, i.e., $b_1 = a_3$ and $b_2 = a_3$.

From $I(x^B) = 1$: $b_1 = a_1, b_2 = a_1$.
From $I(x^B) = 2$: $b_1 = a_2, b_2 = a_2$.

So $a_1 = b_1 = a_2 = b_2$. Let $a_1 = a_2 = c$.

From $I(x^B) = 3$: $b_1 = a_3 = a_1 \oplus a_2 \oplus 1 = c \oplus c \oplus 1 = 1$.
So $b_1 = 1$, but $b_1 = c$, so $c = 1$.

Then $a_1 = a_2 = 1$, $a_3 = 1 \oplus 1 \oplus 1 = 1$.
$b_1 = b_2 = 1$, $b_3 = 1 \oplus 1 = 0$.

Check: $b_{I(x^A)} = 1$ for $I(x^A) \in \{1,2\}$, and $a_{I(x^B)} = 1$ for $I(x^B) \in \{1,2\}$, $a_3 = 1$.

So $b_{I(x^A)} = 1 = a_{I(x^B)}$ for all $I(x^B) \in \{1,2,3\}$. ✓

So $f(01) = (1, 1)$, $f(10) = (1, 1)$, $g(x^B) = (1, 1)$ for all $x^B$.

Alice virtual: $(1, 1, 1 \oplus 1 \oplus 1) = (1, 1, 1)$.
Bob virtual: $(1, 1, 1 \oplus 1) = (1, 1, 0)$.

Check: $b_{I(x^A)} = 1$ for $I(x^A) \in \{1,2\}$. $a_{I(x^B)} = 1$ for $I(x^B) \in \{1,2\}$, $a_3 = 1$. All match. ✓

The other 2-element subsets work similarly (by symmetry of the ⊕1 structure). ✓

**(⟹) The full set $\{01, 10, 11\}$ is incompatible.**

Suppose for contradiction that $f$ and $g$ exist for $S = \{01, 10, 11\}$.

Let $\tilde{y}^A(x^A) = (a_1(x^A), a_2(x^A), a_1(x^A) \oplus a_2(x^A) \oplus 1)$.
Let $\tilde{y}^B(x^B) = (b_1(x^B), b_2(x^B), b_1(x^B) \oplus b_2(x^B))$.

For $I(x^A) = j$ and $I(x^B) = k$ (both in $\{1,2,3\}$):

$$b_j(x^B) = a_k(x^A) \quad \text{whenever } I(x^A) = j, I(x^B) = k$$

Since $f$ depends only on $x^A$ and $g$ depends only on $x^B$:
- $a_k$ depends only on $x^A$ with $I(x^A) = k$ (but there's only one such $x^A$ for each $k$).
- $b_j$ depends only on $x^B$ with $I(x^B) = j$... wait, $b_j$ is the $j$-th component of $\tilde{y}^B(x^B)$, which depends on $x^B$.

Actually, $b_j$ is a function of $x^B$, not of $I(x^B)$ alone. But the constraint must hold for ALL $x^B$ with $I(x^B) = k$.

Let me be more precise. For $x^A$ with $I(x^A) = j$ and $x^B$ with $I(x^B) = k$:

$$\tilde{y}^B_j(x^B) = \tilde{y}^A_k(x^A)$$

The left side depends on $x^B$ (through $g$), the right side depends on $x^A$ (through $f$). Since this must hold for ALL $x^A$ with $I(x^A) = j$ and ALL $x^B$ with $I(x^B) = k$:

- $\tilde{y}^A_k(x^A)$ must be the same for all $x^A$ with $I(x^A) = j$ (but there's only one such $x^A$ for each $j$, so this is automatic).
- $\tilde{y}^B_j(x^B)$ must be the same for all $x^B$ with $I(x^B) = k$ (but there's only one such $x^B$ for each $k$, so this is automatic).

So the constraint is: for each $(j, k) \in \{1,2,3\}^2$:

$$b_j^{(k)} := \tilde{y}^B_j(x^B \text{ with } I(x^B) = k) = \tilde{y}^A_k(x^A \text{ with } I(x^A) = j) =: a_k^{(j)}$$

Since the left depends on $k$ and the right depends on $j$, and they must be equal, we need:

$$b_j^{(k)} = a_k^{(j)} \quad \forall j, k \in \{1,2,3\}$$

This means: for each pair $(j,k)$, $b_j^{(k)} = a_k^{(j)}$. But $b_j^{(k)}$ depends on $k$ (which Bob input) and $a_k^{(j)}$ depends on $j$ (which Alice input). For these to be equal for all $(j,k)$, we need a matrix $M_{jk} = b_j^{(k)} = a_k^{(j)}$ that is simultaneously:
- A function of $k$ for each fixed $j$ (Bob's $j$-th component when Bob has input $k$)
- A function of $j$ for each fixed $k$ (Alice's $k$-th component when Alice has input $j$)

This is just saying $M_{jk}$ is well-defined. The constraints are:

For each $j \in \{1,2,3\}$ (Alice input with $I = j$):
- $a_1^{(j)}, a_2^{(j)}, a_3^{(j)}$ with $a_3^{(j)} = a_1^{(j)} \oplus a_2^{(j)} \oplus 1$

For each $k \in \{1,2,3\}$ (Bob input with $I = k$):
- $b_1^{(k)}, b_2^{(k)}, b_3^{(k)}$ with $b_3^{(k)} = b_1^{(k)} \oplus b_2^{(k)}$

And $M_{jk} = a_k^{(j)} = b_j^{(k)}$ for all $j, k$.

From the Alice constraint: $M_{j3} = a_3^{(j)} = a_1^{(j)} \oplus a_2^{(j)} \oplus 1 = M_{j1} \oplus M_{j2} \oplus 1$.

From the Bob constraint: $M_{3k} = b_3^{(k)} = b_1^{(k)} \oplus b_2^{(k)} = M_{1k} \oplus M_{2k}$.

So:
- Row 3: $M_{3k} = M_{1k} \oplus M_{2k}$ for all $k$
- Column 3: $M_{j3} = M_{j1} \oplus M_{j2} \oplus 1$ for all $j$

In particular, for $j = 3, k = 3$:
- From row 3: $M_{33} = M_{13} \oplus M_{23}$
- From column 3: $M_{33} = M_{31} \oplus M_{32} \oplus 1$

From row 3, $k = 1$: $M_{31} = M_{11} \oplus M_{21}$
From row 3, $k = 2$: $M_{32} = M_{12} \oplus M_{22}$

So $M_{31} \oplus M_{32} = M_{11} \oplus M_{21} \oplus M_{12} \oplus M_{22}$.

From column 3, $j = 1$: $M_{13} = M_{11} \oplus M_{12} \oplus 1$
From column 3, $j = 2$: $M_{23} = M_{21} \oplus M_{22} \oplus 1$

So $M_{13} \oplus M_{23} = M_{11} \oplus M_{12} \oplus 1 \oplus M_{21} \oplus M_{22} \oplus 1 = M_{11} \oplus M_{21} \oplus M_{12} \oplus M_{22}$.

Therefore:
- From row 3: $M_{33} = M_{13} \oplus M_{23} = M_{11} \oplus M_{21} \oplus M_{12} \oplus M_{22}$
- From column 3: $M_{33} = M_{31} \oplus M_{32} \oplus 1 = M_{11} \oplus M_{21} \oplus M_{12} \oplus M_{22} \oplus 1$

These give:
$$M_{11} \oplus M_{21} \oplus M_{12} \oplus M_{22} = M_{11} \oplus M_{21} \oplus M_{12} \oplus M_{22} \oplus 1$$

This is a contradiction ($0 = 1$). $\square$

---

## Lemma 2: Factorization (Necessity and Sufficiency)

### Definition (n-fold compatibility)

A set $M \subseteq \{00, 01, 10, 11\}^n$ of Alice inputs is **compatible** if there exist functions:
- $f: M \to (\{0,1\}^2)^n$ (Alice output)
- $g: \{00,01,10,11\}^n \to (\{0,1\}^2)^n$ (Bob output, no message dependence in the compatibility definition — the message is the class label)

such that:

$$\exists f, \exists g \quad \forall X_A \in M \quad \forall X_B \in \{00,01,10,11\}^n: \quad W_n(X_A, X_B, f(X_A), g(X_B)) = 1$$

**Important:** In the protocol, Bob receives a message $m$ identifying the class. The function $g$ can depend on $m$ (different classes get different Bob decoders). In the compatibility definition, we fix one class $M$ and its decoder $g_M$. The full protocol uses one $g_M$ per class.

### Projection

For $M \subseteq \{00,01,10,11\}^n$ and coordinate $i \in \{1, \ldots, n\}$:

$$\pi_i(M) = \{x_i^A \in \{00,01,10,11\} : \exists X_A \in M \text{ with } X_A[i] = x_i^A\}$$

### Statement

**Lemma 2.** $M$ is compatible if and only if $\pi_i(M)$ is single-copy compatible for every $i \in \{1, \ldots, n\}$.

### Proof of Necessity (⟹)

Assume $M$ is compatible with functions $f$ and $g$.

Fix coordinate $i$. We must show $\pi_i(M)$ is single-copy compatible.

**Construct single-copy functions $f_i$ and $g_i$:**

For $x_i^A \in \pi_i(M)$: Choose any $X_A \in M$ with $X_A[i] = x_i^A$ and define:
$$f_i(x_i^A) = f(X_A)[i]$$

We must show this is well-defined (independent of the choice of $X_A$). Suppose $X_A, X_A' \in M$ with $X_A[i] = X_A'[i] = x_i^A$. We need $f(X_A)[i] = f(X_A')[i]$.

Hmm, this is not obvious. The function $f$ might assign different outputs to $X_A$ and $X_A'$ in coordinate $i$ even though they have the same $i$-th input.

**This is the key subtlety.** Let me reconsider.

Actually, the necessity direction doesn't require $f_i$ to be well-defined in this way. Instead, we should use a different approach.

**Alternative approach:** Fix all coordinates except $i$ to some fixed values. Then the restriction of the protocol to coordinate $i$ gives a single-copy protocol.

More precisely: Fix $X_A^{-i} = (x_1^A, \ldots, x_{i-1}^A, x_{i+1}^A, \ldots, x_n^A)$ to some fixed values, and fix $X_B^{-i}$ similarly.

Define $M_i = \{x_i^A : (x_1^A, \ldots, x_i^A, \ldots, x_n^A) \in M \text{ with the fixed } X_A^{-i}\}$.

Wait, this gives a subset of $\pi_i(M)$, not all of $\pi_i(M)$.

**Better approach:** We need to show that $\pi_i(M) \cap \{01,10,11\}$ has size $\leq 2$ (by Lemma 1).

Suppose for contradiction that $|\pi_i(M) \cap \{01,10,11\}| = 3$, i.e., all three hard values appear in coordinate $i$ of some elements of $M$.

For each $j \in \{1,2,3\}$, there exists $X_A^{(j)} \in M$ with $I(X_A^{(j)}[i]) = j$.

Now, the global protocol must win for all $X_B$. In particular, fix $X_B$ such that $I(X_B[i]) = k$ for some $k \in \{1,2,3\}$, and all other coordinates are easy (00).

For $X_A^{(j)}$ and this $X_B$:
- All coordinates except $i$ auto-win (since $X_B[\ell] = 00$ for $\ell \neq i$).
- Coordinate $i$ must win: $W(x_i^A, x_i^B, y_i^A, y_i^B) = 1$ where $I(x_i^A) = j, I(x_i^B) = k$.

So for each $j \in \{1,2,3\}$ and $k \in \{1,2,3\}$:
$$\tilde{y}^B_{j}(x_i^B) = \tilde{y}^A_{k}(x_i^A) \quad \text{where } I(x_i^A) = j, I(x_i^B) = k$$

But $\tilde{y}^A_k$ depends on $X_A^{(j)}$ (through $f$), and $\tilde{y}^B_j$ depends on $x_i^B$ (through $g$). Since $X_A^{(j)}$ may differ in other coordinates, $f(X_A^{(j)})[i]$ could differ for different $j$.

Wait, but we're looking at coordinate $i$ only. The output $f(X_A)[i] = (y_{i,1}^A, y_{i,2}^A)$ depends on the full $X_A$, not just $X_A[i]$.

**This is the real subtlety.** Alice's output in coordinate $i$ can depend on ALL her inputs, not just coordinate $i$.

So the necessity argument needs to be more careful.

**Corrected approach:** We use the fact that the protocol must work for ALL $X_B$, including those that are easy in all coordinates except $i$.

Fix $X_B$ with $X_B[\ell] = 00$ for all $\ell \neq i$ and $I(X_B[i]) = k \in \{1,2,3\}$.

For $X_A \in M$, all coordinates $\ell \neq i$ auto-win (since $X_B[\ell] = 00$). So we only need coordinate $i$ to win:

$$\tilde{y}^B_{I(X_A[i])}(X_B) = \tilde{y}^A_{k}(X_A) \quad \text{(the } i\text{-th coordinate outputs)}$$

where $\tilde{y}^B$ and $\tilde{y}^A$ are the virtual outputs in coordinate $i$.

Now, $\tilde{y}^B_{I(X_A[i])}(X_B)$ is the $I(X_A[i])$-th component of Bob's virtual output in coordinate $i$, which depends on $g(X_B)[i]$. Since $X_B$ is fixed (with only coordinate $i$ varying through $k$), $g(X_B)[i]$ is fixed. So $\tilde{y}^B_j$ is a fixed value for each $j$.

And $\tilde{y}^A_k(X_A)$ is the $k$-th component of Alice's virtual output in coordinate $i$, which depends on $f(X_A)[i]$, which depends on the full $X_A$.

So for each $X_A \in M$ with $I(X_A[i]) = j$:
$$\tilde{y}^B_j = \tilde{y}^A_k(X_A)$$

The left side is fixed (depends only on $X_B$, which is fixed). So $\tilde{y}^A_k(X_A)$ must be the same for all $X_A \in M$ with $I(X_A[i]) = j$.

Now, varying $k$ (the Bob input in coordinate $i$), we get:
- For $k = 1$: $\tilde{y}^A_1(X_A) = b_j^{(1)}$ for all $X_A$ with $I(X_A[i]) = j$.
- For $k = 2$: $\tilde{y}^A_2(X_A) = b_j^{(2)}$ for all $X_A$ with $I(X_A[i]) = j$.
- For $k = 3$: $\tilde{y}^A_3(X_A) = b_j^{(3)}$ for all $X_A$ with $I(X_A[i]) = j$.

So for each $j$, the virtual output $\tilde{y}^A(X_A)$ in coordinate $i$ is the SAME for all $X_A \in M$ with $I(X_A[i]) = j$. Call this $(a_1^{(j)}, a_2^{(j)}, a_3^{(j)})$.

And we have: $b_j^{(k)} = a_k^{(j)}$ for all $j, k \in \{1,2,3\}$.

With Alice's constraint: $a_3^{(j)} = a_1^{(j)} \oplus a_2^{(j)} \oplus 1$.
With Bob's constraint: $b_3^{(k)} = b_1^{(k)} \oplus b_2^{(k)}$.

This is exactly the same system as in Lemma 1, and if $|\{j : j \in \pi_i(M)\}| = 3$, we get the same contradiction.

Therefore $|\pi_i(M) \cap \{01,10,11\}| \leq 2$, which means $\pi_i(M)$ is single-copy compatible by Lemma 1. $\square$

### Proof of Sufficiency (⟸)

Assume $\pi_i(M)$ is single-copy compatible for every $i \in \{1, \ldots, n\}$.

By Lemma 1, for each $i$, $|\pi_i(M) \cap \{01,10,11\}| \leq 2$.

**Construct global functions $f$ and $g$:**

For each coordinate $i$, since $\pi_i(M)$ is single-copy compatible, there exist single-copy functions $f_i: \pi_i(M) \to \{0,1\}^2$ and $g_i: \{00,01,10,11\} \to \{0,1\}^2$ such that:

$$\forall x_i^A \in \pi_i(M), \quad \forall x_i^B \in \{00,01,10,11\}: \quad W(x_i^A, x_i^B, f_i(x_i^A), g_i(x_i^B)) = 1$$

**Key point:** The single-copy compatibility of $\pi_i(M)$ means there exist $f_i$ and $g_i$ where:
- $f_i(x_i^A)$ depends only on $x_i^A$ (the $i$-th coordinate of Alice's input)
- $g_i(x_i^B)$ depends only on $x_i^B$ (the $i$-th coordinate of Bob's input)
- The winning condition holds for ALL $x_i^B$ simultaneously

**Define global functions:**

$$f(X_A) = (f_1(X_A[1]), f_2(X_A[2]), \ldots, f_n(X_A[n]))$$
$$g(X_B) = (g_1(X_B[1]), g_2(X_B[2]), \ldots, g_n(X_B[n]))$$

**Verify the protocol wins:**

For any $X_A \in M$ and any $X_B \in \{00,01,10,11\}^n$:

$$W_n(X_A, X_B, f(X_A), g(X_B)) = \bigwedge_{i=1}^{n} W(X_A[i], X_B[i], f_i(X_A[i]), g_i(X_B[i]))$$

For each coordinate $i$:
- $X_A[i] \in \pi_i(M)$ (by definition of projection)
- $X_B[i] \in \{00,01,10,11\}$ (any Bob input)
- By single-copy compatibility: $W(X_A[i], X_B[i], f_i(X_A[i]), g_i(X_B[i])) = 1$

Therefore $W_n = \bigwedge_{i=1}^n 1 = 1$. ✓

**Why there is no cross-coordinate consistency conflict:**

The global winning predicate is a conjunction: $W_n = \bigwedge_i W_i$. Each $W_i$ depends only on $(X_A[i], X_B[i], Y_A[i], Y_B[i])$. The global output is a concatenation: $Y_A = (Y_A[1], \ldots, Y_A[n])$, $Y_B = (Y_B[1], \ldots, Y_B[n])$.

Since each $W_i$ depends only on coordinate $i$'s inputs and outputs, and we choose each coordinate's output independently using the single-copy compatible strategy for that coordinate, there is no cross-coordinate constraint. The conjunction is satisfied if and only if each conjunct is satisfied, and each conjunct is satisfied by the single-copy strategy.

**Explicitly:** Alice's output in coordinate $i$ is $f_i(X_A[i])$, which depends only on $X_A[i]$. Bob's output in coordinate $i$ is $g_i(X_B[i])$, which depends only on $X_B[i]$. These are the same functions that achieve single-copy compatibility for $\pi_i(M)$. Since $X_A[i] \in \pi_i(M)$, the single-copy winning condition applies. $\square$

---

## Lemma 3: From Compatibility to Binary Subcubes

### Statement

A maximal compatible set $M \subseteq \{01,10,11\}^n$ (considering only hard inputs) corresponds to a binary subcube $A_1 \times \cdots \times A_n$ where $A_i \subseteq \{1,2,3\}$ with $|A_i| = 2$ for each $i$.

### Proof

By Lemma 2, $M$ is compatible iff $\pi_i(M)$ is single-copy compatible for each $i$. By Lemma 1, $\pi_i(M) \subseteq \{1,2,3\}$ with $|\pi_i(M)| \leq 2$.

A maximal compatible set has $|\pi_i(M)| = 2$ for each $i$ (otherwise we could add more elements).

So $M \subseteq A_1 \times \cdots \times A_n$ where $A_i = \pi_i(M)$ with $|A_i| = 2$.

**Enlargement:** If $M \subsetneq A_1 \times \cdots \times A_n$, we can enlarge $M$ to the full binary subcube $A_1 \times \cdots \times A_n$ and it remains compatible (the projections don't change). So maximal compatible sets are full binary subcubes.

**Conversely:** Any binary subcube $A_1 \times \cdots \times A_n$ with $|A_i| = 2$ is compatible (each projection has size 2, which is compatible by Lemma 1). $\square$

---

## Theorem 1: Main Communication Theorem

### Statement

$$B^*(n, 1) = \left\lceil \log_2 f(n, 3) \right\rceil = \left\lceil \log_2 \gamma_t(K_3^{\times n}) \right\rceil$$

where $f(n, 3)$ is the minimum number of binary subcubes covering $\{0,1,2\}^n$, equivalently $\gamma_t(K_3^{\times n})$.

### Proof

**Lower bound:** A $B$-bit protocol has at most $2^B$ message classes. Each class must be compatible (by definition of perfect success). By Lemma 3, each compatible class is contained in a binary subcube. The classes must cover all hard inputs $\{01,10,11\}^n$, which (after relabeling) is $\{0,1,2\}^n$. So the classes form a binary subcube cover, requiring at least $f(n, 3)$ classes. Therefore $2^B \geq f(n, 3)$, giving $B \geq \lceil \log_2 f(n, 3) \rceil$.

**Upper bound:** Let $\{C_1, \ldots, C_m\}$ be an optimal binary subcube cover with $m = f(n, 3)$. Assign one message label $j \in \{1, \ldots, m\}$ to each $C_j$. Alice, on input $X_A$, finds any $C_j$ containing $X_A$ and sends $j$ (using $\lceil \log_2 m \rceil$ bits). By Lemma 3, $C_j$ is compatible, so Alice and Bob use the corresponding perfect strategy. Perfect success is achieved. So $B^*(n,1) \leq \lceil \log_2 f(n, 3) \rceil$.

**Combining:** $B^*(n, 1) = \lceil \log_2 f(n, 3) \rceil$. $\square$

---

## Corollary 1: Asymptotic Communication Rate

### Statement

$$B^*(n, 1) = n \log_2(3/2) + O(1)$$

and therefore:

$$\lim_{n \to \infty} \frac{B^*(n, 1)}{n} = \log_2(3/2) \approx 0.5849625$$

### Proof

By Theorem 1, $B^*(n,1) = \lceil \log_2 f(n, 3) \rceil$.

By Kuang & Wang (2026, Theorem 1.2): $f(n) = (C_3 + o(1))(3/2)^n$ where $1.62227 < C_3 \leq 2$.

Therefore:
$$B^*(n,1) = \lceil \log_2((C_3 + o(1))(3/2)^n) \rceil = \lceil n \log_2(3/2) + \log_2(C_3 + o(1)) \rceil$$

Since $\log_2(C_3 + o(1)) = O(1)$ (as $C_3$ is bounded):

$$B^*(n,1) = n \log_2(3/2) + O(1)$$

and:

$$\lim_{n \to \infty} \frac{B^*(n,1)}{n} = \log_2(3/2)$$

**Attribution:** The covering asymptotic $f(n) = (C_3 + o(1))(3/2)^n$ is due to Kuang & Wang (2026). Our contribution is the exact reduction $B^* = \lceil \log_2 f(n,3) \rceil$, which translates this into the communication rate. $\square$

---

## Corollary 2: Communication Compression

### Statement

$B^*(n, 1) < n \cdot B^*(1, 1)$ for $n \in \{4, 5, 6, 7, 8\}$, and asymptotically:

$$\frac{B^*(n, 1)}{n \cdot B^*(1, 1)} \to \log_2(3/2) \approx 0.585$$

### Proof

$B^*(1, 1) = 1$. From the finite-size table:

| $n$ | $B^*(n,1)$ | $n \cdot B^*(1,1)$ | Compression? |
|-----|-------------|---------------------|--------------|
| 4 | 3 | 4 | YES |
| 5 | 4 | 5 | YES |
| 6 | 5 | 6 | YES |
| 7 | 5 | 7 | YES |
| 8 | 6 | 8 | YES |

Asymptotically, by Corollary 1:

$$\frac{B^*(n,1)}{n} \to \log_2(3/2) \approx 0.585 < 1 = B^*(1,1)$$

So communication is compressed to ~58.5% of one bit per subtask. $\square$

---

## Corollary 3: Shared Randomness Does Not Help

### Statement

$$B^*_{\text{shared-random}}(n, 1) = B^*_{\text{deterministic}}(n, 1)$$

### Proof

A shared-randomness protocol with $B$ bits consists of functions $e_r, f_r, g_r$ for each random seed $r$ in the support. The success probability is:

$$S = \mathbb{E}_r \left[ \Pr_{X_A, X_B}[W_n(X_A, X_B, f_r(X_A), g_r(X_B, e_r(X_A))) = 1] \right]$$

For $S = 1$ (perfect success), we need:

$$\forall X_A, X_B: \quad \mathbb{E}_r[W_n(X_A, X_B, f_r(X_A), g_r(X_B, e_r(X_A)))] = 1$$

Since $W_n \in \{0, 1\}$, this requires:

$$\forall X_A, X_B, \quad \forall r \text{ with } \Pr[R = r] > 0: \quad W_n(X_A, X_B, f_r(X_A), g_r(X_B, e_r(X_A))) = 1$$

So every seed $r$ in the support induces a deterministic perfect protocol. Fix any such $r$. This gives a deterministic protocol with $B$ bits achieving perfect success.

Therefore $B^*_{\text{shared-random}}(n, 1) \geq B^*_{\text{deterministic}}(n, 1)$. The reverse inequality is trivial (deterministic is a special case of shared-randomness). $\square$

**Note:** This argument works because the success criterion is worst-case over inputs (perfect success requires winning on ALL inputs). If the success criterion were distributional (average over inputs), the argument would need adaptation.
