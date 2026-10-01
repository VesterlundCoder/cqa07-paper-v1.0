# CQA07: Parallel Repetition Audit for S_n(0)

## Question

Does $S_n(0) = (15/16)^n$ hold, or can correlated no-communication strategies across $n$ copies improve on the product strategy?

## Background

The claim $S_n(0) = (15/16)^n$ assumes multiplicativity of the no-communication optimum under parallel repetition. For general nonlocal games, parallel repetition is nontrivial: $\omega(G^{\otimes n}) \neq \omega(G)^n$ in general, and correlated strategies can sometimes improve the score.

## What is proven

### Lower bound (product strategy)

The product of optimal single-copy strategies achieves:
$$S_n(0) \geq (15/16)^n$$

This is trivially true: use the optimal single-copy strategy independently for each copy. Each copy wins with probability $15/16$, so the product wins with probability $(15/16)^n$.

### Upper bound (multiplicativity)

**NOT PROVEN.** Showing $S_n(0) \leq (15/16)^n$ requires proving that no correlated strategy can exceed the product score. This is a parallel repetition theorem for this specific task.

## Why this is hard

For general nonlocal games, parallel repetition theorems (Raz, Holenstein, etc.) show that the score decreases exponentially, but not necessarily with the exact base $\omega(G)$. The exact multiplicativity $\omega(G^{\otimes n}) = \omega(G)^n$ holds for some games but not all.

The Zhao-Deng task has a specific structure:
- The winning predicate is a product of per-copy predicates.
- The no-communication constraint means Alice and Bob each produce outputs without communication.
- But Alice and Bob CAN correlate their outputs across copies (using shared randomness or deterministic correlation).

A correlated strategy might, for example, sacrifice one copy to gain information that helps another copy. However, since there is no communication and no post-selection, it's unclear how this would help.

## Computational evidence

For $n = 1$: $S_1(0) = 15/16$ (exhaustively verified, 65536 strategy pairs).
For $n = 2, 3, 4$: computational verification confirms $S_n(0) = (15/16)^n$ (exhaustive or near-exhaustive search).

## Decision

**The multiplicativity claim is NOT proven as a theorem.** It is computationally verified for small $n$.

**Action:** Weaken the claim in the manuscript to:
$$S_n(0) \geq (15/16)^n$$
with equality computationally verified for $n \leq 4$.

This claim is NOT needed for the main communication theorem (Theorem 1), which only depends on the zero-error ($S = 1$) case. The $S_n(0)$ claim is a secondary observation about the no-communication baseline.

## Zhao-Deng context

Zhao-Deng themselves only claim that the no-communication score decreases as $2^{-\Omega(n)}$, not that it equals $(15/16)^n$ exactly. Our weaker claim $S_n(0) \geq (15/16)^n$ is consistent with their bound (since $(15/16)^n = 2^{-n \log_2(16/15)} \approx 2^{-0.093n}$, which is $2^{-\Omega(n)}$).

## Recommendation

Move the $S_n(0)$ discussion to the appendix as a computational observation. State:
- $S_1(0) = 15/16$ (proven by exhaustive search).
- $S_n(0) \geq (15/16)^n$ (product strategy lower bound).
- Equality computationally verified for $n \leq 4$.
- General multiplicativity is an open question (not needed for the main theorem).

This avoids a reviewer vulnerability while preserving the computational evidence.
