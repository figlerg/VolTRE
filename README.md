# VolTRE
Playground for volume based sampling method for timed regular expressions.



## Meetings

### 23.07


## ?
3 recursions, ambiguity check, etc...

### 16.07
use time generation with breach? alexandre donze
- paper: application for testing, NFM20
- idea: instead of sampling, enumerate points... eg find all the integer points of an expression (enumeration instead of sampling)

### 12.07.
new ideas:
- [x] top level intersection (sampling)
- [ ] top level renaming (sampling)
- [x] need rejection sampling for the sampling of above
  - [x] need matching algo for rejection sampling
- [x] inductive counting of ways of matching a word
- [x] -> can be used for sampling ambiguous expressions (5 sided dice simulation idea)


Update 15.07: 
Let UTRE' be unambiguous TRE without intersection and renaming. TRE' can be ambiguous but also doesn't have intersection and renaming. Then we currently can do this:

|                        | UTRE' | UTRE' + renaming | UTRE' + top level intersection | TRE' |
|------------------------|-------|------------------|--------------------------------| ---- |
| Volume computation     | yes   |  TRE'            | no                             | no   |
| Exact sampling (1shot) | yes   |  TRE'            | no                             | no   |
| Rejection sampling     |       |  TRE'            | yes (for fixed T)              | no   |
| Roulette sampling      |       |  TRE'            | no                             | yes  |


### 25.06. experiments, comp with wordgen

``TAkiller:  < a.<b.<c.<d*>_[0,1]>_[0,2]>_[0,3]>_[0,4]

``Small TAkiller: <a.<b.<d*>_[0,1]>_[0,2]>_[0,3]  

  

- The two tools' results are different for the TAkiller example. 
	- [ ] Benoît will visualize his volume function so we can compare better.
- My tool produces strange jumps at the borders of intervals - the smallest example where this happens was n=4, small TAkiller.
-  (New for Nicolas:) We noticed that both tools couldn't produce a volume for TAkiller with n=3, even though L_3 should have a volume. We will investigate.  
- At the integer points weird things often happen, in both tools.

### 20.06
- we now have better idea of how to fix the moments: we have a formula for $\lambda_1,...,\lambda_m\ \rightarrow \mu_1, ..., \mu_m$ 
- We can also write down the gradient for this mapping -> can do newton or gradient descent
- [ ] implement $\lambda \mapsto \mu$ directly
- [ ] implement $\mu \mapsto \lambda$ via an applicable optimization procedure
- [ ] implement the jacobi matrix for the derivatives of $\frac{d\mu_i} {d\lambda_j}$
- [ ] implement a wrapper function which instead of $\mu_i$ takes as input simply mean and variance $\mu, \sigma$ for usability (this can be inferred directly from the $\mu_i$ values)


### 14.06.
- [ ] compute the blackbox (lambda1, lambda2) -> (mu, sigma)
- [ ] maybe invert it with some sampling/optimization/whatever scheme
- [ ] look at special case lambda2=0, lambda1=-s - compare with benoit
- [ ] find example where TAs are hard for sampling, but TRE easier? 
     10 clocks? ```<<<<<<<<a>_[0,1].b>_[0,2].c>_[0,3].d>_[0,4].e>_[0,5].f>_[0,6].g>_[0,7].h>_[0,8]```, put nested timed restriction

### 11.06.
- [ ] read region paper of alur
- [ ] T sampling with mu, sigma (derivative trick on whiteboard at 11.06.)
- motivation seeking:
  - CASE STUDY: benchmarking: use to create benchmarks (eg test dogans tool, create formulas and check the monitor), quasi unit tester for monitors
  - intersection?
  - nondeterminism? 
    - on the fly determinisation, estimate how the volumes change with increasing values
    - bounded determinism? sampling matches and reweight them acc to how many matches give the same timed words. gives estimations of how big intersections are
    - characterize how much formulas intersect or how different they are
    - refinements?
    - probabilistic theory of contracts, interface theories? pairs of formulas (tres) check refinements, do compositions, but operations are undecidable. maybe estimate with some proba guarantees whether something is the composition of two contracts
    - one of orig motivations was language inclusion. sample in two languages that we want to compare. if word in symmetric difference we have counterexample. otherwise we can say with high confidence that the difference is withing the threshold
    - contract theory: assume guarantee pairs, one refines the other if it has stronger guarantees, weaker conditions
    - lift this idea to 2 player games
  - CASE STUDY: mission time stuff?
  - CASE STUDY: comparing formulas that are similar
  - CASE STUDY: spec mining, LLm , quantitatively compare models
  - CASE STUDY: sample timed word, transform them to have input signals 

### 04.06.2024
- [x] do visual check by plotting in 2d
- [x] compute bernstein region volumes and plot the histogram for the regions
- [x] get polynomials from wordgen and compare with our poly (for an applicable example)