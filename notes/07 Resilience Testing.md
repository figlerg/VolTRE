## General Idea
Let $S$ be a discrete event model describing the manufacturing processes of computer chips. Frame it as a resilience problem: Given such a model (e.g. for the chip manufacturing), how resilient is it towards special outside factor events, such as covid19 or the canal thing. As input signals describe something like $\langle a\rangle. (\langle b.c\rangle_{[1,2]}*)$
with
- $a \dots$ outbreak of a pandemic
- $b \dots$ lockdown procedures (which impact some part of the production process).
- $c\dots$ end of any lockdown procedures

The storage decays in some form (chips are used, bought etc.). Event $b$ worsens production parameters, event $c$ fixes them again.

As outcome we observe the produced units, e.g. by monitoring an STL formula for when the capacity drops under some threshold. Something like "The supply for computer chips should never drop below threshold $x$". 
### An example of a specific model
_"Discrete Event Simulation as a Robust Supporting Tool for Smart Manufacturing":_
![[Pasted image 20240909172330.png]]
