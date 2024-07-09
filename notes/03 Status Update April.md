## State of the Art
There is a paper by Nicolas on __fixed-length uniform sampling of _deterministic timed automata___ (Barbot and Basset, “Max-Entropy Sampling for Deterministic Timed Automata Under Linear Duration Constraints.”). Here, they lay much of the groundwork on computing volumes. The volumes are then used to weight the edges in a certain way and also indicate how to sample the delays [_not quite sure how this works yet_].

We want to use similar methods to __unambiguous timed regular expressions without intersection__, for which no algorithm exists yet. 

## Base idea
We give an inductive way to compute the volumes of expressions. The end goal is an algorithm which generates these volumes and lets us sample timed words as uniformly as possible.

### Notation
- $\theta(w)$ is the duration of timed word $w$.
- $l(w)$ is the length of $w$. 
- $\mathcal L(\varphi)$ is the language of expression $\varphi$.
- If the expression $\varphi$ is clear from context, we use $L$ for $\mathcal L(\varphi)$ and $L_n=\{w \in \mathcal L (\varphi) ~|~ l(w) = n\}$, so the language of $n$-letter words. 
- For $f : L_n \rightarrow \mathbb R$ we define $\int_{L_n} f~dw = \sum_{(w_1\dots w_n)\in \Sigma^n} \int_{t_1\dots t_n \in \mathbb R^n} \mathbb 1_{(t_1w_1\dots t_nw_n)\in L_n} dt_1\dots dt_n$. Essentially this is an integral over all words and all delays which make up the language.
- $V_n^\varphi$ is the volume of the language $L_n = \{w \in \mathcal L (\varphi) ~|~ l(w) = n\}$.
- As a special case of $f$ above we can pick $f(w) = 1$. This is the same as the volume of an expression $V_n^\varphi = \int_{L_n} 1 ~dw$. This means that for every discrete word in the language we sum up the standard (Lebesgue) volume of applicable delays.
- $V_n^\varphi(T)$ is the $(n-1)$-dimensional volume of a _slice_, meaning for a given duration $T$. 


### Setup
Let $\varphi$ be an unambiguous TRE without intersection. Let $n \in \mathbb N$ and $\mu \in \mathbb R^+$. We want to generate samples as uniformly as possible with the given mean duration $\mu$, meaning that the following constraint must hold for the sampling distribution $p$:
$$\int_{L_n} p(w) \theta(w) = \mu$$

### Maximum Entropy
The principle of maximum entropy tells us, that without any knowledge about  the distribution we should maximize entropy (basically assume the least amount of knowledge). We lift the definition of entropy to timed languages like this: 
$$
H(p) = -\int_{L_n}p(w) \log{p(w)}~ dw = 
- \sum_{a_1 \dots a_n \in \sum^n} \int_{t_1,\dots,t_n \in \mathbb{R}} 
p(t_1a_1\dots t_n a_n) \cdot \log ~ p (t_1a_1\dots t_n a_n)
dt_1 \dots dt_n
$$

(For reference, the entropy of a continuous PDF is $h(p) = - \int_{I} p(x) \log p(x) \, dx$.)

The PDF we are looking for must therefore maximize entropy while satisfying the constraint on the mean duration, which is an optimization problem:

$$
\max_{p...\text{pdf}} H(p) \quad s.t. \quad \int_{L_n} \theta(w) \, p(w) \, dw = \mu.
$$

In Nicolas' paper it is proved that 
1) it is always better to sample on a _slice_: given some duration $T$, we must assign the same density to all words $w$ with $\theta(w)=T$. Thus, the maximum entropy solution will be of form $p^* = \tilde p^* \circ \theta$  with some $\tilde p^* : \mathbb R \rightarrow \mathbb R$. In other words, we can transform the integral above to an integral over reals and look for solutions $p^*(T)$ instead.
2) the solution of the maximum entropy problem is of the form
$$
p^*(T) = \frac {e^{-sT}} {\mathcal L (V_n^\varphi(T))(s)}
$$
for some $s\in \mathbb R$ (if such a PDF exists). The normalization term in the denominator is the Laplace transform of the volume function in terms of $T$.

Roughly speaking, we have a correspondence $\mu \leftrightarrow s$ here, i.e. by tuning $s$ we can change the mean duration. Note that for clarity, I only included the special case for the mean duration here - the actual theorem is more general and can handle multiple, more general soft constraints. [_I am unsure about this, but I think $s$ can be found using the reverse Laplace transform?_]

### Computation of Volumes
Above we heard that instead of directly computing the volumes, we can instead compute volumes in slices and integrate:
$$
V_n(\varphi) = \int_{L_n} 1 dw = \int_0^\infty V_n^\varphi (T)~dT.
$$

This helps us, because it is easier to compute the volume of slices. Here are inductive rules for the computation of volumes as a function of a fixed duration $T$:

$$
V_n^\varphi (T) = \text {...given by the inductive rules}
$$
![[Pasted image 20240320172403.png]]

We have a an idea for a theorem which roughly says: __Slice volumes are piecewise polynomials in terms of $T$. These polynomials are of the form__
$$
V_n^\varphi = \sum_{I \in \mathcal J}^n \mathbb 1_I(T)\cdot p_I(T),
$$
where $\mathcal J$ is a finite set of intervals and $p_I$ is a polynomial. The volume polynomials
- can be computed relatively easily,
- have degree $\leq n$,
- consist of $\mathcal O (cn)$ pieces, where $c$ is a constant that depends linearly on the biggest constant in the time constraints of the expression.

This lets us compute volumes in a table, which in turn tells us what the PDF is.


### Sampling Algorithm

Recall that we know that the optimal PDF is uniform on a slice. This means we can split the sampling in two steps (assuming we calculated the right $s$):
1) Sample the duration $T$ according to the PDF $p^*(T) = \frac {e^{-sT}} {\mathcal L (V_n^\varphi(T))(s)}$. This just means sampling $u \sim \mathcal U(0,1)$ and finding the corresponding value in the CDF. (inverse sampling method)
 2) Sample in $L_n^\varphi (T)$. This can be done recursively, so by computing the volumes of subexpressions and picking each subexpression with the probability expressed as a fraction of volumes. [_The details I have yet to figure out._] The Subexpression that is picked will be the recurred on. 

