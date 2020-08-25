#!/usr/bin/env python3
"""Computes the optimal solution to the harmonic integer program
for a given value of k and mu."""

import argparse
from harmonic import frac_str, solve_ips
from fractions import Fraction


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('k', type=int)
    parser.add_argument('mu', type=Fraction)
    parser.add_argument('-d', '--debug', action='store_true', default=False)
    args = parser.parse_args()
    if args.k <= 0:
        raise ValueError('k should be >= 1')
    if args.mu < 0:
        raise ValueError('mu should be >= 0')
    best_score = solve_ips(args.k, [args.mu], args.debug)[0]
    print(best_score, '=', frac_str(best_score, use_float=True))


if __name__ == '__main__':
    main()
