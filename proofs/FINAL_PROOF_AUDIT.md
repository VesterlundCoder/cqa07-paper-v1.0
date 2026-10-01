# CQA07: Final Adversarial Proof Audit

This audit attempts to falsify each lemma/theorem in `RIGOROUS_PROOFS.md`. Each item must reach status PASS before entering the manuscript.

---

## Lemma 1: Single-Copy Compatibility

### STATEMENT
$S \subseteq \{01, 10, 11\}$ is compatible iff $|S| \leq 2$.

### DEPENDENCIES
- Task definition (virtual outputs, winning predicate)

### POSSIBLE FAILURE MODES
1. The ⊕1 contradiction proof has an algebraic error.
2. A 2-element subset is actually incompatible (no valid $f, g$ exist).
3. The quantifier order allows a loophole (e.g., $g$ depends on $x^A$).

### COUNTEREXAMPLE SEARCH
- For $S = \{01, 10\}$: explicit construction found: $f = (1,1)$, $g = (1,1)$. Verified: $\tilde{y}^A = (1,1,1)$, $\tilde{y}^B = (1,1,0)$. For $I(x^A) \in \{1,2\}$, $I(x^B) \in \{1,2,3\}$: $b_{I(x^A)} = 1 = a_{I(x^B)}$. ✓
- For $S = \{01, 11\}$: by symmetry (swap roles of indices 1 and 3 in the virtual output), same construction works.
- For $S = \{10, 11\}$: by symmetry, same construction works.
- For $S = \{01, 10, 11\}$: the matrix contradiction $M_{33} = M_{13} \oplus M_{23}$ (row) vs $M_{33} = M_{31} \oplus M_{32} \oplus 1$ (column) gives $0 = 1$. ✓

### MACHINE CHECK
Exhaustive verification for $n=1$ (65536 strategy pairs) confirms $S_1(0) = 15/16$, meaning no 3-element set is compatible.

### STATUS: PASS

---

## Lemma 2: Factorization (Necessity)

### STATEMENT
$M$ compatible $\Rightarrow$ $\pi_i(M)$ single-copy compatible for all $i$.

### DEPENDENCIES
- Lemma 1

### POSSIBLE FAILURE MODES
1. Alice's output in coordinate $i$ depends on the full $X_A$, not just $X_A[i]$, so the projection argument fails.
2. The "fix other coordinates to easy" trick doesn't work because the protocol might use cross-coordinate information.

### COUNTEREXAMPLE SEARCH
The proof fixes $X_B$ with all coordinates except $i$ set to 00 (easy). This forces coordinate $i$ to be the only non-trivial one. The key insight is:

For each $j \in \{1,2,3\}$, pick $X_A^{(j)} \in M$ with $I(X_A^{(j)}[i]) = j$. The protocol must win for ALL $X_B$, including the one with $X_B[\ell] = 00$ for $\ell \neq i$ and $I(X_B[i]) = k$.

In this case, all coordinates $\ell \neq i$ auto-win, so only coordinate $i$ matters. The constraint becomes:
$$\tilde{y}^B_{I(X_A[i])}(X_B) = \tilde{y}^A_{k}(X_A)$$

The left side is fixed (depends on $X_B$, which is fixed up to $k$). So $\tilde{y}^A_k(X_A)$ must be the same for all $X_A \in M$ with $I(X_A[i]) = j$.

This means: for each $j$, the virtual output in coordinate $i$ is the same for all $X_A \in M$ with $I(X_A[i]) = j$. Call it $(a_1^{(j)}, a_2^{(j)}, a_3^{(j)})$.

Then $b_j^{(k)} = a_k^{(j)}$ for all $j, k$, giving the same matrix contradiction as Lemma 1 if all three $j$-values appear.

**Potential issue:** What if $M$ contains no element with $I(X_A[i]) = j$ for some $j$? Then $|\pi_i(M) \cap \{1,2,3\}| \leq 2$, which is already compatible. The argument only needs to handle the case where all three appear, and in that case it produces a contradiction.

**Potential issue:** What if $X_A^{(j)}$ and $X_A^{(j')}$ have different values in other coordinates, and this affects $f(X_A)[i]$? The proof shows that $\tilde{y}^A_k(X_A)$ must be the same for all $X_A$ with the same $I(X_A[i]) = j$, regardless of other coordinates. This is because the constraint $b_j^{(k)} = \tilde{y}^A_k(X_A)$ must hold for the fixed $X_B$, and $b_j^{(k)}$ is a single value.

### MACHINE CHECK
Computational verification for $n=2,3,4$ confirms that compatible classes have $|\pi_i(M)| \leq 2$ for all $i$.

### STATUS: PASS

---

## Lemma 2: Factorization (Sufficiency)

### STATEMENT
$\pi_i(M)$ single-copy compatible for all $i$ $\Rightarrow$ $M$ compatible.

### DEPENDENCIES
- Lemma 1

### POSSIBLE FAILURE MODES
1. **Cross-coordinate consistency conflict:** Alice's global output $f(X_A)$ must work for all $X_B$ simultaneously. If $f_i(X_A[i])$ is chosen per-coordinate, there might be a conflict.
2. **Bob's decoder depends on the message, not just the coordinate:** In the full protocol, Bob receives one message for all coordinates. The sufficiency proof must show that a single Bob decoder works for all coordinates.
3. **The single-copy $g_i$ depends on the class $\pi_i(M)$, which may differ across coordinates:** Different coordinates may have different projections, requiring different Bob decoders.

### COUNTEREXAMPLE SEARCH

**Addressing failure mode 1:** The global winning predicate is $W_n = \bigwedge_i W_i$. Each $W_i$ depends only on coordinate $i$'s inputs and outputs. Alice's output $f(X_A) = (f_1(X_A[1]), \ldots, f_n(X_A[n]))$ is a concatenation of per-coordinate outputs. Bob's output $g(X_B) = (g_1(X_B[1]), \ldots, g_n(X_B[n]))$ is also a concatenation. Since $W_i$ depends only on $(X_A[i], X_B[i], f_i(X_A[i]), g_i(X_B[i]))$, and each $W_i = 1$ by single-copy compatibility, we get $W_n = 1$.

There is no cross-coordinate constraint because the winning predicate is a product (conjunction). This is the key structural property.

**Addressing failure mode 2:** In the compatibility definition, Bob's decoder $g$ does NOT depend on the message — it's a single function for the entire class $M$. In the full protocol, Bob receives a message identifying the class, and then uses the class-specific decoder. The sufficiency proof constructs ONE decoder $g = (g_1, \ldots, g_n)$ for the entire class $M$. This is valid because:
- Each $g_i$ is the single-copy decoder for $\pi_i(M)$
- $g(X_B) = (g_1(X_B[1]), \ldots, g_n(X_B[n]))$ is well-defined
- For any $X_A \in M$ and any $X_B$, each coordinate $i$ wins by single-copy compatibility

**Addressing failure mode 3:** The single-copy $g_i$ depends on $\pi_i(M)$, which is determined by the class $M$. Since $M$ is fixed, each $\pi_i(M)$ is fixed, and each $g_i$ is fixed. The concatenation $g = (g_1, \ldots, g_n)$ is a single function. In the full protocol, the message identifies $M$, so Bob knows which $g_i$ to use for each coordinate.

**Important subtlety:** In the full protocol, different message classes $M$ and $M'$ may have different projections $\pi_i(M) \neq \pi_i(M')$, requiring different $g_i$. This is fine — the message tells Bob which class he's in, so he knows which $g_i$ to use.

**Another subtlety:** What if $X_A[i] \in \pi_i(M)$ but $X_A[i] \notin \pi_i(M')$ for some other class $M'$? This doesn't matter because Alice sends the message identifying which class $X_A$ belongs to. The encoder $e$ maps $X_A$ to a class $M$ containing $X_A$, and Bob uses the decoder for $M$.

### MACHINE CHECK
Computational verification for $n=2,3,4$ confirms that protocols constructed from the covering number achieve $S = 1.0$.

### STATUS: PASS

---

## Lemma 3: From Compatibility to Binary Subcubes

### STATEMENT
Maximal compatible sets correspond to binary subcubes $A_1 \times \cdots \times A_n$ with $|A_i| = 2$.

### DEPENDENCIES
- Lemma 1, Lemma 2

### POSSIBLE FAILURE MODES
1. A compatible set might not be a full binary subcube (it could be a proper subset).
2. Enlarging a compatible set to a full binary subcube might break compatibility.

### COUNTEREXAMPLE SEARCH

**Addressing failure mode 1:** A compatible set $M$ has $|\pi_i(M)| \leq 2$ for each $i$. So $M \subseteq A_1 \times \cdots \times A_n$ where $A_i = \pi_i(M)$. If $M$ is a proper subset, it's still compatible, but it's not maximal. The covering problem minimizes the number of classes, so we want maximal classes.

**Addressing failure mode 2:** If we enlarge $M$ to $A_1 \times \cdots \times A_n$, the projections don't change ($\pi_i(A_1 \times \cdots \times A_n) = A_i = \pi_i(M)$). So the enlarged set is still compatible by Lemma 2. ✓

**Key point for the covering equivalence:** The covering problem asks for the minimum number of binary subcubes whose union covers $\{0,1,2\}^n$. Each binary subcube is a maximal compatible set. The minimum number of compatible classes equals the minimum number of binary subcubes covering $\{0,1,2\}^n$.

But wait: could a non-maximal compatible set be part of a more efficient cover? No — if $M \subsetneq A_1 \times \cdots \times A_n$, replacing $M$ with $A_1 \times \cdots \times A_n$ in the cover only covers more elements, never fewer. So optimal covers use maximal compatible sets (full binary subcubes).

### MACHINE CHECK
Computational verification confirms that optimal covers use full binary subcubes.

### STATUS: PASS

---

## Theorem 1: Main Communication Theorem

### STATEMENT
$B^*(n, 1) = \lceil \log_2 f(n, 3) \rceil$

### DEPENDENCIES
- Lemma 1, Lemma 2, Lemma 3

### POSSIBLE FAILURE MODES
1. **Encoding non-power-of-two classes:** If $f(n,3)$ is not a power of 2, can we encode $m = f(n,3)$ classes with $\lceil \log_2 m \rceil$ bits?
2. **Lower bound gap:** The lower bound says $2^B \geq f(n,3)$, but maybe some classes can share a message?
3. **Upper bound gap:** The upper bound uses $\lceil \log_2 m \rceil$ bits, but maybe fewer bits suffice with a cleverer encoding?

### COUNTEREXAMPLE SEARCH

**Addressing failure mode 1:** With $B = \lceil \log_2 m \rceil$ bits, we can represent $2^B \geq m$ distinct messages. We assign one message per class, using only $m$ of the $2^B$ available messages. This is valid — unused messages are simply never sent. ✓

**Addressing failure mode 2:** Each message class must be compatible (by definition of perfect success). The classes must cover all hard inputs (otherwise some input has no winning strategy). By Lemma 3, each class is contained in a binary subcube. So the classes form a binary subcube cover, requiring at least $f(n,3)$ classes. Since each class needs a distinct message, $2^B \geq f(n,3)$. ✓

**Addressing failure mode 3:** The upper bound is constructive: assign one message per class in an optimal cover. Alice sends the class index. This uses exactly $\lceil \log_2 m \rceil$ bits. Could we do better? The lower bound shows $B \geq \lceil \log_2 f(n,3) \rceil$, so no. ✓

**Subtle issue:** Could two classes share a message if they are "compatible with each other"? No — a message class is a set of Alice inputs that share the same message. If two covering sets $C_j$ and $C_k$ share a message, then the message class is $C_j \cup C_k$, which must be compatible. But $C_j \cup C_k$ might not be compatible (its projections might have size > 2). So in general, each covering set needs its own message. ✓

**Another subtle issue:** What about easy inputs ($I(x^A) = 0$ in some coordinate)? These auto-win, so they can be in any class. They don't affect the covering problem. The covering problem is over hard inputs $\{01,10,11\}^n \cong \{0,1,2\}^n$. ✓

### MACHINE CHECK
Computational verification for $n=1,2,3,4$ confirms $B^*(n,1) = \lceil \log_2 f(n,3) \rceil$ with $f(n,3) = 2,3,5,8$.

### STATUS: PASS

---

## Corollary 1: Asymptotic Communication Rate

### STATEMENT
$B^*(n,1) = n \log_2(3/2) + O(1)$, so $\lim B^*/n = \log_2(3/2)$.

### DEPENDENCIES
- Theorem 1
- Kuang & Wang (2026): $f(n) = (C_3 + o(1))(3/2)^n$

### POSSIBLE FAILURE MODES
1. The $o(1)$ term in $f(n) = (C_3 + o(1))(3/2)^n$ might not be $O(1)$ after taking $\log_2$.
2. The ceiling function might introduce a non-$O(1)$ error.

### COUNTEREXAMPLE SEARCH

**Addressing failure mode 1:** $\log_2((C_3 + o(1))(3/2)^n) = n \log_2(3/2) + \log_2(C_3 + o(1))$. Since $C_3 \in (1.62227, 2]$, $\log_2(C_3 + o(1))$ is bounded (between $\log_2(1.62227) \approx 0.699$ and $\log_2(2) = 1$). So $\log_2(C_3 + o(1)) = O(1)$. ✓

**Addressing failure mode 2:** $\lceil x + O(1) \rceil = x + O(1)$ (the ceiling adds at most 1). So $B^* = n \log_2(3/2) + O(1)$. ✓

### STATUS: PASS

---

## Corollary 2: Communication Compression

### STATEMENT
$B^*(n,1) < n \cdot B^*(1,1)$ for $n \geq 4$, asymptotically $B^*/n \to \log_2(3/2) \approx 0.585$.

### DEPENDENCIES
- Corollary 1
- Finite-size table

### POSSIBLE FAILURE MODES
1. The finite-size values might be wrong.
2. The asymptotic limit might not be $< 1$.

### COUNTEREXAMPLE SEARCH
- $B^*(1,1) = 1$, so $n \cdot B^*(1,1) = n$.
- $B^*(4,1) = 3 < 4$. ✓
- $\log_2(3/2) \approx 0.585 < 1$. ✓

### STATUS: PASS

---

## Corollary 3: Shared Randomness Does Not Help

### STATEMENT
$B^*_{\text{shared-random}}(n, 1) = B^*_{\text{deterministic}}(n, 1)$

### DEPENDENCIES
- Definition of perfect success (worst-case over inputs)

### POSSIBLE FAILURE MODES
1. The success criterion might be distributional (average over inputs), not worst-case.
2. The quantifier order might allow a loophole.

### COUNTEREXAMPLE SEARCH

**Addressing failure mode 1:** The success probability $S_n(B)$ is defined as $\max_{e,f,g} \Pr_{X_A, X_B}[W_n = 1]$, which is an average over uniformly random inputs. For $S = 1$, this means $W_n = 1$ for ALL input pairs (since $W_n \in \{0,1\}$ and the average is 1 only if all values are 1). So perfect success IS worst-case. ✓

**Addressing failure mode 2:** For shared randomness with seed $R$:
$$S = \mathbb{E}_R[\Pr_{X_A, X_B}[W_n = 1 | R]] = \Pr_{X_A, X_B, R}[W_n = 1]$$

For $S = 1$: $\Pr[W_n = 1] = 1$, which means $W_n = 1$ for all $(X_A, X_B, R)$ with positive probability. So for each $r$ with $\Pr[R = r] > 0$, the deterministic protocol $(e_r, f_r, g_r)$ achieves $W_n = 1$ for all $(X_A, X_B)$. ✓

**Important note:** This argument works because $W_n \in \{0, 1\}$ (binary). If the score were a real-valued quantity, averaging could allow some seeds to fail. But for perfect success ($S = 1$), every seed must succeed on every input.

### STATUS: PASS

---

## Audit of $S_n(0) = (15/16)^n$ Claim

### STATEMENT
The no-communication classical score for $n$ copies is $S_n(0) = (15/16)^n$.

### DEPENDENCIES
- $S_1(0) = 15/16$ (exhaustively verified)
- Multiplicativity under parallel repetition

### POSSIBLE FAILURE MODES
1. **Parallel repetition is nontrivial:** For nonlocal games, $\omega(G^{\otimes n}) \neq \omega(G)^n$ in general. Correlated strategies across copies could improve the score.
2. **The Zhao-Deng task is not a standard nonlocal game:** It has a specific structure that might or might not allow correlation benefits.

### COUNTEREXAMPLE SEARCH

The claim $S_n(0) = (15/16)^n$ assumes that the optimal no-communication strategy for $n$ copies is the product of optimal single-copy strategies. This is NOT automatic.

**Upper bound (product strategy achieves):** $S_n(0) \geq (15/16)^n$ by using the optimal single-copy strategy independently for each copy. ✓

**Lower bound (no strategy can exceed):** This requires showing that no correlated strategy can exceed $(15/16)^n$. This is a parallel repetition theorem for this specific task.

**Status:** The multiplicativity is NOT proven. The claim should be weakened to:
$$S_n(0) \geq (15/16)^n$$
with equality computationally verified for small $n$.

**Recommendation:** Move to appendix as a computational observation, not a theorem. The main communication theorem does NOT depend on this claim.

### STATUS: FAIL — Claim must be weakened to $S_n(0) \geq (15/16)^n$ with computational verification for small $n$.

---

## Summary

| Item | Status |
|------|--------|
| Lemma 1 (single-copy compatibility) | PASS |
| Lemma 2 necessity | PASS |
| Lemma 2 sufficiency | PASS |
| Lemma 3 (binary subcubes) | PASS |
| Theorem 1 (main theorem) | PASS |
| Corollary 1 (asymptotic rate) | PASS |
| Corollary 2 (compression) | PASS |
| Corollary 3 (shared randomness) | PASS |
| $S_n(0) = (15/16)^n$ | FAIL — weaken to $\geq$ with computational verification |

**All lemmas and theorems required for the main paper PASS the audit.** The only failing item is the secondary $S_n(0)$ claim, which is not needed for the main theorem and should be moved to the appendix.
