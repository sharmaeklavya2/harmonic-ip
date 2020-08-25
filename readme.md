## Harmonic IP

A python program that finds optimal solutions to the harmonic integer program.

## The harmonic integer program

The harmonic function `f` parametrized by `k` and `μ` is defined as

```python
def f(x):
    if x <= 1/k:
        return μ * x
    else:
        for j in range(1, k):
            if 1/(j+1) < x <= 1/j:
                return 1/j
```

Such a function finds applications in packing problems.
See, for example, the article
'[A simple on-line bin-packing algorithm](https://dl.acm.org/doi/pdf/10.1145/3828.3833)'
by C. C. Lee and D. T. Lee (1985) in Journal of the ACM,
which first introduced the harmonic function for `μ = k/(k-1)`.

Let `IP(k, μ)` be the integer program on a sequence `z` of `k-1` variables,
where we want to maximize `sum([z[j] * (1/(j+1) - μ/(j+2)) for j in range(k-1)])`
under the constraint that `sum([z[j]/(j+1) for j in range(k-1)]) < 1`.
Call it the harmonic integer program.

Given a set `X` of numbers such that `sum(X) ≤ 1`,
we would like to find the least upper bound (LUB) on `sum([f(x) for x in X])`.
It can be proved that this LUB is the same as the optimal value of `IP(k, μ)`.

## Using the scripts

There is a `O(4^k)`-time brute-force algorithm for
finding all feasible solutions to `IP(k, μ)`.
The program `compute.py` takes `k` and `μ` as command-line arguments
and outputs the optimal value of `IP(k, μ)`.
`k` must be an integer and `μ` must be a fraction expressed in the form `numerator/denominator`.
Rational-number arithmetic is used for computation,
so there are no floating-point errors due to rounding.

A simple example invocation:
```
$ ./compute.py 5 5/4
41/24 = 1.7083333333333333
```
Run `./compute.py --help` to see all available command-line options.

The program `print-table.py` takes two command-line arguments,
the first is an integer called `kmax`, and the second is either `csv` or `tex`.
`print-table.py` outputs the optimal value of `IP(k, μ)` for all `k ≤ kmax`
and some important values of `μ`, and the output is formatted as a table (either CSV or TeX).

Example invocations:
```
$ ./print-table.py 4 csv
k,lee,capr,eku
2,2,null,4
3,7/4,3,19/10
4,31/18,2,115/66
$ ./print-table.py 4 tex
\begin{tabular}{|c|r|r|r|}
\hline \diagbox{$k$}{$\mu$} & $k/(k-1)$ & $k/(k-2)$ & $k^2/(k^2-k-1)$ \\
\hline $2$ & $2$ & -- & $4$ \\
\hline $3$ & $\sfrac{7}{4} = \texttt{1.75000000}$ & $3$ & $\sfrac{19}{10} = \texttt{1.90000000}$ \\
\hline $4$ & $\sfrac{31}{18} = \texttt{1.72222222}$ & $2$ & $\sfrac{115}{66} = \texttt{1.74242424}$ \\
\hline \end{tabular}
```
Run `./print-table.py --help` to see all available command-line options.
