## AD
Imagine an automated vehicle and three events $a,b,c$ which describe the following discrete scenarios: 
- $a \dots$ overtake maneuver
- $b \dots$ high speed 
- $c \dots$ lane switch
- $d \dots$ brake maneuver
- $e \dots$ tire problem
- $f \dots$ sensor sees obstacle
- $g \dots$ view deteriorates

We define some safety property and write a scenario description in form of a TRE:
$\langle c.f\rangle _{[0,1]}$ would mean that shortly after initiating the lane switch an obstacle is recognized.

__BUT:__ We can't really run any AD driving stack?

__PS: Somehow these feel especially unnatural?__

## Resilience Testing

Extracted to document: "07 Resilience Testing".


## General View of above examples
In both cases I am trying to make a case for injecting some events. I think this could be done in any model, but I don't quite see how to motivate using TRE as input specification.


## Timed sequence charts? AD