#!/usr/bin/env python3
"""Computes the optimal solution to the harmonic integer program
for several values of k and mu and outputs these values as a table."""

import sys
import argparse
from harmonic import frac_str, solve_ips
from fractions import Fraction
from typing import Optional, Sequence, TextIO


def tex_str(x: Optional[Fraction], float_only: bool) -> str:
    if x is None:
        return '--'
    else:
        if x.denominator == 1:
            return '$' + str(x.numerator) + '$'
        elif float_only:
            return '\\texttt{%.8f}' % (float(x),)
        else:
            return '$\\sfrac{%s}{%s} = \\texttt{%.8f}$' % (x.numerator, x.denominator, float(x))


def get_mu(label: str, k: int) -> Optional[Fraction]:
    if label == 'one':
        return Fraction(1)
    elif label == 'lee':
        return Fraction(k, k - 1) if k >= 2 else None
    elif label == 'eku':
        return Fraction(k * k, k * k - k - 1) if k >= 2 else None
    elif label == 'capr':
        return Fraction(k, k - 2) if k >= 3 else None
    else:
        raise ValueError('get_mu: invalid value of label')


TEX_LABELS = {
    'one': '$1$',
    'lee': '$k/(k-1)$',
    'capr': '$k/(k-2)$',
    'eku': '$k^2/(k^2-k-1)$',
}


def print_table(ks: Sequence[int], labels: Sequence[str], format: str,
        use_float: bool, file: TextIO, debug: bool) -> None:
    if format == 'csv':
        print('k,' + ','.join(labels), file=file)
        for k in ks:
            mus = [get_mu(label, k) for label in labels]
            line = solve_ips(k, mus, debug)
            print(','.join([str(k)] + [frac_str(x, use_float) for x in line]), file=file)
    elif format == 'tex':
        print('\\begin{tabular}{|c|%s}' % ('r|' * len(labels)), file=file)
        print('\\hline \\diagbox{$k$}{$\\mu$} & '
            + ' & '.join([TEX_LABELS[x] for x in labels]) + ' \\\\', file=file)  # noqa
        for k in ks:
            mus = [get_mu(label, k) for label in labels]
            line = solve_ips(k, mus, debug)
            print('\\hline ${}$ & '.format(k)
                + ' & '.join([tex_str(x, use_float) for x in line])  # noqa
                + ' \\\\', file=file)  # noqa
        print('\\hline \\end{tabular}', file=file)
    else:
        raise NotImplementedError('format {}'.format(repr(format)))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kmax', type=int)
    parser.add_argument('fmt', choices=('csv', 'tex'))
    parser.add_argument('--use-float', action='store_true', default=False,
        help='show floats in CSV and only show floats in TeX')
    parser.add_argument('-d', '--debug', action='store_true', default=False)
    args = parser.parse_args()
    if args.kmax <= 0:
        raise ValueError('kmax should be >= 1')
    print_table(range(2, args.kmax + 1), ['lee', 'capr', 'eku'],
        args.fmt, args.use_float, sys.stdout, args.debug)


if __name__ == '__main__':
    main()
