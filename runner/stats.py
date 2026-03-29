"""Bootstrap confidence intervals and significance tests. No scipy dependency."""

import random

# Fixed seed for reproducible reports
_RNG = random.Random(42)


def bootstrap_ci(values: list[float], n_resamples: int = 2000, ci: float = 0.95) -> tuple[float, float] | None:
    """Compute bootstrap confidence interval for the mean.

    Returns (low, high) or None if insufficient data.
    """
    if len(values) < 3 or n_resamples <= 0:
        return None

    alpha = (1 - ci) / 2
    means = []
    for _ in range(n_resamples):
        sample = _RNG.choices(values, k=len(values))
        means.append(sum(sample) / len(sample))

    means.sort()
    low_idx = int(alpha * n_resamples)
    high_idx = int((1 - alpha) * n_resamples) - 1
    return (means[low_idx], means[high_idx])


def bootstrap_diff_test(a: list[float], b: list[float], n_resamples: int = 5000) -> float | None:
    """Two-sample bootstrap test for difference of means.

    Returns p-value (two-sided) or None if insufficient data.
    Tests H0: mean(a) == mean(b).
    """
    if len(a) < 3 or len(b) < 3 or n_resamples <= 0:
        return None

    observed_diff = abs(sum(a) / len(a) - sum(b) / len(b))

    # Pool under H0
    pooled = a + b
    pool_mean = sum(pooled) / len(pooled)
    a_centered = [x - sum(a) / len(a) + pool_mean for x in a]
    b_centered = [x - sum(b) / len(b) + pool_mean for x in b]

    count = 0
    for _ in range(n_resamples):
        sa = _RNG.choices(a_centered, k=len(a))
        sb = _RNG.choices(b_centered, k=len(b))
        diff = abs(sum(sa) / len(sa) - sum(sb) / len(sb))
        if diff >= observed_diff:
            count += 1

    return count / n_resamples
