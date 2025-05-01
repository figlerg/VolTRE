import argparse
import os
import random
import cProfile
import pstats
import numpy as np
import matplotlib.pyplot as plt
import warnings
from misc.rename import rename
from parse.quickparse import quickparse
from sample.sample import sample
from sample.sample import DurationSamplerMode
from volume.slice_volume import slice_volume  # Assumes this is where it's defined

# ========================
# Command-line Arguments
# ========================
parser = argparse.ArgumentParser(description="Parse a TRE file and generate samples.")
parser.add_argument('-p', '--path', type=str, required=True, help='Path to the .tre file.')
parser.add_argument('-n', '--length', type=int, required=True, help='Fixed length (number of events) of sampled words.')
parser.add_argument('-T', '--duration', type=float, default=None, help='Fixed total duration (optional).')
parser.add_argument('--mode', type=str, choices=['vanilla', 'max_entropy'], default='vanilla', help='Sampling mode. Default is vanilla.')
parser.add_argument('--budget', type=int, default=500, help='Budget for rejection sampling (default: 500).')
parser.add_argument('--nr_samples', type=int, default=None, help='Number of samples to generate.')
parser.add_argument('--verbose', action='store_true', help='Enable verbose mode with profiling.')
parser.add_argument('--seed', type=int, default=None, help='Random seed (optional).')
parser.add_argument('-v', '--visualize', action='store_true', help='Visualize the slice volume function.')
parser.add_argument('--total_volume', action='store_true', help='Print the total volume of the slice.')
args = parser.parse_args()

# ========================
# Setup and Parsing
# ========================
if args.seed is not None:
    random.seed(args.seed)
    np.random.seed(args.seed)

ctx = quickparse(args.path)
print("Parsed Expression:")
print(ctx.getText())

# Apply renamings if necessary
ctx_tmp = rename(ctx)
if ctx.getText() != ctx_tmp.getText():
    ctx = ctx_tmp
    print("Applied renaming. New Expression:")
    print(ctx.getText())

# ========================
# Experiment Logic
# ========================

def experiment():
    mode = DurationSamplerMode.VANILLA if args.mode == 'vanilla' else DurationSamplerMode.MAX_ENT

    if args.verbose:
        print("Computing slice volume...")
    try:
        vol = slice_volume(ctx, args.length)
        if args.visualize:
            vol.plot()
        if args.total_volume:
            total_vol = vol.total_volume()
            print(f"Total volume: {total_vol}")
        if args.verbose:
            print("Slice volume computation completed.")
            vol.fancy_print()
            print("This volume assumes the expression is unambiguous and has no top-level intersection. Intersection errors will be caught, but ambiguity cannot be detected here. If the expression is ambiguous, the computed volume may be incorrect. Check the sampling rejection feedback: zero rejections imply unambiguous expression.")
            print("Sampling will work anyways, as it uses our smart rejection sampling in case of ambiguity.")
    except Exception as e:
        vol = None
        if args.verbose:
            print(f"Slice volume computation failed or not applicable: {e}")

    if args.nr_samples is None:
        if args.visualize or args.total_volume:
            return  # Only visualization or volume requested
        else:
            raise ValueError("--nr_samples must be specified unless using --visualize or --total_volume only.")

    if args.verbose:
        print("Starting sampling...")

    for _ in range(args.nr_samples):
        w = sample(ctx, n=args.length, T=args.duration, mode=mode, budget=args.budget)
        print(w)

    plt.show()

# ========================
# Profiling Setup
# ========================
pr = cProfile.Profile()  # just to shut up my linter

if args.verbose:
    print("Profiling enabled...")
    pr.enable()

experiment()

if args.verbose:
    pr.disable()
    profile_file = "main.prof"
    pr.dump_stats(profile_file)
    print(f"Profiling data saved to {profile_file}")
    p = pstats.Stats(profile_file)
    p.strip_dirs().sort_stats('cumulative').print_stats(10)

# ========================
# Internal Flags
# ========================
# top=True is handled inside sample(), hidden from CLI
# TODO: Add --feedback option to CLI in the future
