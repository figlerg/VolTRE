## Method

Let $e_1,e_2$ be TRE. We want a probabilistic procedure to test whether $L(e_1) \subset L(e_2)$.

Think of the procedure: Sample $w \in L(e_1)$ and check whether $w \in L_2$. 
- If  $w \notin L_2$, we know the inclusion does not hold.
- If $w \in L_2$, we repeat and are a little more confident that $L(e_1) \subset L(e_2)$

## Probabilities
So what does "a little more confident" from above mean? We would like to quantify how sure we are about the inclusions after $n$ iterations. Say that both expressions are bounded.

Assume there is an intersection $L(e_1) \cap L(e_2)^C \neq \varnothing$. We probably can't do anything about the case  $V(L(e_1) \cap L(e_2)^c) = 0$, for example cases where only the boundary of $e_1$ is outside and the integrals collapse (or similar).

So let us say further that $V(L(e_1) \cap L(e_2)^c) = v \neq 0$, so the set of counter examples to the inclusion has a volume $v$. 

### Version 1
Each time we sample we have a probability $p = \frac{v}{V(e_1)}$ to find a counterexample. The probability of having found no counterexample (even though there is one) at try $n$ is $(1-p)^n$. If $v=0$ we have probability $1$. 

$$P_\varphi(X=n) = 
\begin{cases} 
	\left(1-\frac{v}{V(e_1)}\right)^n & v > 0 \\
	1 & v = 0
\end{cases}
$$
Another way of saying this is that for high $n$, $\left(1-\frac{v}{V(e_1)}\right)^n \rightarrow 0$. However, we can't say how likely it is that we are right since we a-priori have no clue how big $v$ is.

### Version 2

Instead maybe the chance to find the counterexample after exactly n+1 tries?:
$$P_\varphi(Y=n+1) = 
\begin{cases} 
	\left(1-\frac{v}{V(e_1)}\right)^n * \frac{v}{V(e_1)} & v > 0 \\
	0 & v = 0
\end{cases}
$$





