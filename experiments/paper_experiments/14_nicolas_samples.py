"""
50 uniform samples of eex2 = a*.<a*>_[1,2]  for  n=2, T=2.3.
Saves to nicolas_samples.csv (delay1, symbol1, delay2, symbol2, ...).
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from parse.quickparse import quickparse
from sample.sample import sample
from sample.TimedWord import TimedWord

N          = 2
T          = 2.3
NR_SAMPLES = 50
OUT        = os.path.join(os.path.dirname(__file__), '14_nicolas_samples.csv')

phi = quickparse('a*.<a*>_[1,2]', string=True)

words = []
for i in range(NR_SAMPLES):
    w, _ = sample(phi, n=N, T=T, feedback=True)
    words.append(w)
    print(f"  {i+1:2d}: {w}")

TimedWord.list_to_csv(words, OUT)
print(f"\nSaved {NR_SAMPLES} samples to {OUT}")
