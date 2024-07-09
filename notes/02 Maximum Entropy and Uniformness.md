Here I looked at conrad2004probability and the slides on uniform sampling by Nicolas

## Maximum Entropy and Uniformness
The principle of maximum entropy says: _if we are seeking a probability density function subject to certain constraints (e.g., a given mean or variance), use the density satisfying those constraints that has entropy as large as possible._ __To do what? That sounds like too broad of a statement? Is the uniform distribution so natural that we just know it is the distribution with biggest entropy...__

The principle is partially motivated by the principle of insufficient reason: _If we want to assign probabilities to an event, and see no reason for one outcome to occur more often than any other, then the events are assigned equal probabilities._

Intuitively: when looking for a sampler, we can also rephrase the question to look for a density function for timed words. Without any context except the target mean, we must __maximize entropy__  for a pdf that is as uniform as possible: One where the entropy (measure of uncertainity) is as big as possible.

### Entropy
#### Entropy of continuous pdf
Since timed languages are (at least partially) continuous (timing delays on a continuum make up the words), we need to use something like the continuous definition for the entropy of a pdf $p$:
$$
h(p) = - \int_{I} p(x) \log p(x) \, dx
$$

High entropy means less information, low entropy more information. Thus, max entropy means minimum information, which we want to capture in our pdf. __TODO look at the definitions in information theory. where does the log come from again? isn't it weird that it also pops up in continuous stuff?__

#### Integrals over words
Nicolas defined an integral in terms of languages as follows:
$$
\int_{L_n} f(w)dw = \sum_{a_1 \dots a_n \in \sum^n} \int_{t_1,\dots,t_n \in \mathbb{R}} f(t_1a_1\dots t_n a_n)dt_1 \dots dt_n
$$
Intuitively, this measures the typical volume of sets of valid time-delay-tuples for each discrete word. 

#### Entropy of timed language pdf
Now we fuse these two notions to lift the entropy to timed languages: Let $p(w)$ be a pdf on timed words. Then the entropy of $p$ is:
$$
H(p) = -\int_{L_n}p(w) \log{p(w)}~ dw = 
- \sum_{a_1 \dots a_n \in \sum^n} \int_{t_1,\dots,t_n \in \mathbb{R}} 
p(t_1a_1\dots t_n a_n) \cdot \log ~ p (t_1a_1\dots t_n a_n)
dt_1 \dots dt_n
$$

### Formulation of optimization problem
So in the words above, we want a pdf $p(w)$ which maximizes the entropy, so the optimization problem 
$$
\max_{p...\text{pdf}} H(p) \quad s.t. \quad \int_{L_n} \theta(w) \, p(w) \, dw = \mu.

$$
Here we have a constraint on the mean of the word length.

(Note that this is slightly simplified from Nicola's formulation, here I specialized it to the case where just the constraint on the expected value is given.)

### Solution of optimization problem

#### Lagrange multipliers WHAT I DO HERE IS HORRIBLE, CHECK THE 2023 SAMPLING PAPER!
This is often done with Lagrange multipliers (the book conrad2004probability says it is slightly incorrect or there is some caveat, but for now I try to do it like this).

First the general [Lagrangean](https://en.wikipedia.org/wiki/Lagrange_multiplier) when we want to optimize $f(x)$ under constraints $g(x) = 0$ is written like this:
$$
\mathcal L (x,\lambda) = f(x) + \langle \lambda, g(x) \rangle
$$

In our case we have only one Lagrange multiplier, because the only constraint is $g(x) =  \int_{L_n} \theta(w) \, p(w) \, dw - \mu = 0$. So our specific Lagrangean is this:

$$
\begin{align}
\mathcal L (p,\lambda) &= 
H(p) + \lambda \cdot \left(\int_{L_n} \theta(w) \, p(w) dw - \mu \right) =\\
&- \sum_{a_1 \dots a_n \in \sum^n} \int_{t_1,\dots,t_n \in \mathbb{R}} 
p(t_1a_1\dots t_n a_n) \cdot \log ~ p (t_1a_1\dots t_n a_n)
dt_1 \dots dt_n \\
&+ \lambda \cdot \left(\int_{L_n} \theta(w) \, p(w) dw - \mu \right)
\end{align}
$$
and we find (candidates of) local maxima by setting all partial derivatives to 0.

Now I am not sure this whole thing works, since $p$ is a function. But Let us try anyways and see whether we arrive at Nicolas' characterisation. Compute the "points" where both derivatives are 0:
$$
\begin{align}
\frac{d\mathcal L}{dp} &= 
- \sum_{a_1 \dots a_n \in \sum^n} \int_{t_1,\dots,t_n \in \mathbb{R}} 
\log p(t_1a_1\dots t_n a_n) + 1~
dt_1 \dots dt_n 
+
\lambda \int_{L_n} \theta(w) dw
=
0
\\
\frac{d\mathcal L}{d\lambda} &= H(p) + \int_{L_n} \theta(w) \, p(w) dw - \mu
= 0
\end{align}
$$
For $\frac{d\mathcal L}{dp}$ I plugged $p \log p'$ into WolframAlpha... __This is very unlike me, I treat it like an engineer and simply assume that switching the limits works. I pulled the differential inside and pray that I can differentiate like this.__



#### Maximum entropy pdf form
The form of the maximum entropy density (for arbitrary soft constraints $f_($) is 
$$
p^*(w) = \exp \left(\lambda_0 + \sum_{i=1}^m \lambda_i f_i(\theta(w))\right)
$$

So in our case where we have only one constraint (on the mean), we end up with this form:

$$
p^*(w) = \exp (\lambda_0 + \lambda_1 \theta(w)) = c \exp(\lambda_1 \theta(w))
$$

#### Transfer to integral over reals