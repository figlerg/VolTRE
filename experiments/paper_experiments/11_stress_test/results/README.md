# Stress Test Figures — Experiment 11

Sampling time versus expression complexity for five VolTRE expressions.
Solid circles connected by a line = all samples succeeded.
Open triangles (not connected) = at least one attempt failed; the Y value is
total wall time divided by successful samples, so it correctly reflects the
cost of obtaining one good sample even when some attempts are rejected or time out.

---

## 11_stress_ex1.pdf — Unbounded Kleene, varying n

**Expression:** $e_1 = (\langle a \rangle_{\leq 1})^*$

Sampling time as a function of word length $n$ (no time bound $T$, so the
sampler must also choose $T$ itself).  Time grows with $n$ up to around
$n = 20$, after which the mpmath precision starts to break down and partial
failures appear.  Shows the baseline cost of the volume polynomial evaluation
for a simple timed Kleene expression.

---

## 11_stress_ex2.pdf — Mixed Kleene + timed subexpression, varying n

**Expression:** $e_2 = a^* \cdot \langle aa \rangle_{\leq 1} \cdot a^*$, fixed $T = 0.5$

Log-scale plot of sampling time vs $n$.  The timed middle factor $\langle aa
\rangle_{\leq 1}$ makes the volume polynomial more complex than $e_1$, and the
cost grows faster.  Failures begin around $n = 22$–25, again driven by
floating-point cancellation in the inclusion-exclusion polynomial at high $n$.

---

## 11_stress_ex3.pdf — Intersection expression, varying T

**Expression:** $e_3 = (\langle aa \rangle_{\leq 1} \cdot a) \cap (a \cdot \langle aa \rangle_{\leq 1})$, fixed $n = 3$

Log-scale plot of effective sampling time vs time budget $T \in (0, 2)$.
Cost is flat and cheap for small $T$, rises steeply as $T \to 2$ because the
intersection volume shrinks and the rejection sampler must try many more
candidates.  Open triangles near $T = 1.9$–$1.95$ indicate that some attempts
hit the 100-rejection budget limit; the displayed time is wall time per
successful sample, correctly showing the continued upward trend.

---

## 11_stress_ex3_volume.pdf — Subexpression volumes and sampling time for ex3

Two-panel figure for $e_3$ at $n = 3$.

- **Top:** Volumes $V(e_A)$ and $V(e_B)$ of the two intersection branches as
  functions of $T$.  Both are symmetric and peak near $T = 1$, going to zero
  at $T = 0$ and $T = 2$.
- **Bottom:** Sampling time (same data as `ex3.pdf`) overlaid on the same
  $T$-axis, showing that cost spikes precisely where the volumes are small and
  the intersection is hardest to hit by rejection.

---

## 11_stress_exb.pdf — Nested Kleene with tight timing, varying n

**Expression:** $e_b = \langle b \rangle^*_{[3,4]} \cdot (\langle a \rangle_{[1,2]} \cdot \langle b \rangle_{[3,4]} \cdot \langle b \rangle^*_{[3,4]})^*$

Sampling time vs $n$ for an expression with narrow timing intervals $[3,4]$
and $[1,2]$ (rather than $[0, T]$).  Cost rises steadily through $n = 9$;
partial failures appear at $n = 10$–$11$ where the tight constraints combined
with high $n$ again push mpmath into cancellation territory.  Demonstrates
that the precision issue is not specific to large $T$ but to high polynomial
degree generally.
