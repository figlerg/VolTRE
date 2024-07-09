
Let $\varphi \in TRE_u$ be a timed regular expression in some fragment $TRE_u$ which is unambiguous on its operations (we do not know whether we can define this syntactically, but it is necessary for words to be unambiguous).

## Basics

### Definition: Unambiguous
I think this is a property of an expression? Something like
$$e_1 + e_2 \text{ is unambiguous} \Leftrightarrow L(e_1) \cap L(e_2) = \emptyset$$
but to me this is not a general definition.

A bit of confusion is added because ambiguity also pops up in grammars: Here it means that we get a unique syntax tree while parsing an expression. I do not think that the two concepts are related.

### Some examples
#### $\varphi_1 = a \cup a^*$
 is likely ambiguous. It also makes sense to exclude this from the inductive volume computation, since

$$
V_1^{\varphi_1}(T) = V_1^a (T) + V_1^{a^*}(T) = 2
$$
obviously counts the word $Ta$ twice.

#### $\varphi_2 = a^* \cdot a^*$
can also never differentiate between the two subexpressions, so blindly evaluating the rule for concatenation likely counts some words multiple times. 

### Ideas to get around this
- If we had access to the $\cap$, then we could do the thing with union? Namely $V_1^{\varphi_1}(T) = V_1^a (T) + V_1^{a^*}(T) - V_1^{a \cap a^*}(T)$

If these are actually volumes, this should work. But Nicolas excluded intersection, why again?

- Simply exclude them, like Nicolas said. But to me it seems unlikely that we can do this syntactically? Is unambiguity decidable or do we just have to assume that they are or work with obvious example? 


## Volumes
### Original Version
Ideally we want a Volume function $V_n: TRE_u \rightarrow \mathbb{R}_+\cup \infty$. 
I think what Nicolas is trying to say in the slides is that as an intermediate volume we measure the volume of a _slice_, so basically the volume given that we know the duration:
$$
V_n^\varphi (T) = \text {...given by the inductive rules}
$$
![[Pasted image 20240320172403.png]]

Nicolas gives the following integral of a function on the duration, over a language:
![[Pasted image 20240320173001.png]]


If we set $f(T) = 1$ we can calculate the overall volume of $L_n$ by integrating over all $T$.

$$
V_n(\varphi)= \int_{L_n} 1 dw = \int_0^\infty V_n^L(T) dT
$$
In that last step, $V_n^L$ is the $n-1$ dimensional volume for fixed T.

### My Version
I can sort of see the idea above (except for the stuff with the form of the distribution due to the max entropy distribution). __HOWEVER__ the logic of the base definitions escape me a little: 
- Why start with the definition of integrals over languages? This all smells like measure theory, would we not need to start from the volume definitions? 
- I have a draft based on Lebesgue measures, which looks like it is the exact same as Nicola's version in practice. (handwritten notes)
- Also, the hole thing needs to be simplified.