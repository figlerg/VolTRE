# VolTRE
Playground for volume based sampling method for timed regular expressions.


## Meetings
### 11.06.
- [ ] read region paper of alur
- [ ] T sampling with mu, sigma (derivative trick on whiteboard at 11.06.)
- [ ] motivation seeking:
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
- [ ] get polynomials from wordgen and compare with our poly (for an applicable example)