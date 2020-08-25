import sys
from fractions import Fraction
from typing import Any, Iterable, Optional, Sequence, Tuple


def debug_print(*args: Any, **kwargs: Any) -> None:
    print(*args, file=sys.stderr, **kwargs)


def list_str(x: Sequence[Any]) -> str:
    return '[' + ', '.join([str(y) for y in x]) + ']'


def frac_str(x: Optional[Fraction], use_float: bool) -> str:
    if use_float:
        return '{:.8f}'.format(float(x)) if x is not None else 'null'
    else:
        return str(x) if x is not None else 'null'


def feasible_sols(k: int, i: int, s: Fraction) -> Iterable[Tuple[int, ...]]:
    # debug_print('feasible_sols(k={}, i={}, s={})'.format(k, i, s))
    if i <= 0:
        raise ValueError('i should be >= 1')
    if i > k:
        raise ValueError('i should be <= k')
    if s >= 1:
        raise ValueError('s should be < 1')
    if i == k:
        yield ()
    else:
        yi_up = ((1 - s) * (i + 1)).__ceil__()
        for yi in range(yi_up):
            s2 = s + Fraction(yi, i + 1)
            for sol in feasible_sols(k, i + 1, s2):
                yield (yi,) + sol


def eval_sol(sol: Sequence[int], k: int, mu: Fraction) -> Fraction:
    if len(sol) != k - 1:
        raise ValueError('len(sol) != k-1')
    s = mu
    for j in range(1, k):
        s += sol[j - 1] * (Fraction(1, j) - Fraction(mu, j + 1))
    return s


SeqOFrac = Sequence[Optional[Fraction]]


def solve_ips(k: int, mus: SeqOFrac, debug: bool) -> SeqOFrac:
    if debug:
        debug_print('calling solve_ips(k={}, mus={})'.format(k, list_str(mus)))
    count = 0
    best_sols = [(0,) * (k - 1) for mu in mus]
    best_scores = [mu for mu in mus]
    for sol in feasible_sols(k, 1, Fraction(0)):
        count += 1
        for (imu, mu) in enumerate(mus):
            if mu is not None:
                score = eval_sol(sol, k, mu)
                # debug_print(sol, score)
                if score > best_scores[imu]:  # type: ignore # best_score[imu] will not be None
                    best_sols[imu], best_scores[imu] = sol, score
                    # debug_print(sol, score, float(score))
    if debug:
        debug_print('k={}:'.format(k), count, 'solutions found')
        for (imu, mu) in enumerate(mus):
            debug_print('k={}: mu={}, sol={}, score={}={}'.format(
                k, mu, best_sols[imu], frac_str(best_scores[imu], use_float=False),
                frac_str(best_scores[imu], use_float=True)))
    return best_scores
