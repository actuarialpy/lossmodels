"""Tests for the (a, b, 1) frequency class (added in 0.5.0).

Closed-form means/variances are taken from Loss Models Appendix B.3. The base
(a, b, 0) models use the library's probability parameterization; the Klugman beta
relates by beta = (1 - p) / p for the geometric / negative binomial.
"""

from math import exp, log

import numpy as np
import pytest

from lossmodels.frequency import (
    Binomial,
    Geometric,
    Logarithmic,
    NegativeBinomial,
    Poisson,
    ZeroModified,
    ZeroTruncated,
)


def _pmf_sum(model, K=5000):
    return float(model.pmf(np.arange(0, K)).sum())


# ---------------------------------------------------------------- ZeroTruncated
def test_zt_poisson_pmf_zero_and_sum():
    zt = ZeroTruncated(Poisson(2.0))
    assert float(zt.pmf(0)) == 0.0
    assert np.isclose(_pmf_sum(zt), 1.0, atol=1e-9)


def test_zt_poisson_mean_variance():
    lam = 2.0
    zt = ZeroTruncated(Poisson(lam))
    mean = lam / (1 - exp(-lam))
    var = lam * (1 - (lam + 1) * exp(-lam)) / (1 - exp(-lam)) ** 2
    assert np.isclose(zt.mean(), mean, rtol=1e-9)
    assert np.isclose(zt.variance(), var, rtol=1e-9)


def test_zt_geometric_mean_variance():
    p = 0.25
    beta = (1 - p) / p
    zt = ZeroTruncated(Geometric(p))
    assert np.isclose(zt.mean(), 1 + beta, rtol=1e-9)
    assert np.isclose(zt.variance(), beta * (1 + beta), rtol=1e-9)


def test_zt_binomial_mean():
    n, q = 5, 0.3
    zt = ZeroTruncated(Binomial(n, q))
    assert np.isclose(zt.mean(), n * q / (1 - (1 - q) ** n), rtol=1e-9)
    assert np.isclose(_pmf_sum(zt), 1.0, atol=1e-9)


def test_zt_negbinomial_mean():
    r, p = 3.0, 1 / 3.0
    beta = (1 - p) / p
    zt = ZeroTruncated(NegativeBinomial(r, p))
    assert np.isclose(zt.mean(), r * beta / (1 - (1 + beta) ** (-r)), rtol=1e-9)


def test_zt_cdf_monotone_and_limit():
    zt = ZeroTruncated(Poisson(2.0))
    c = zt.cdf(np.arange(0, 40))
    assert float(zt.cdf(0)) == 0.0
    assert np.all(np.diff(c) >= -1e-12)
    assert c[-1] > 0.999


def test_zt_sample():
    np.random.seed(11)
    zt = ZeroTruncated(Poisson(2.0))
    s = zt.sample(20000)
    assert s.shape == (20000,)
    assert np.all(s >= 1)  # zero is impossible
    assert np.isclose(s.mean(), zt.mean(), rtol=0.05)


def test_zt_scalar_vs_array():
    zt = ZeroTruncated(Poisson(2.0))
    arr = zt.pmf(np.array([1, 2, 3]))
    assert isinstance(arr, np.ndarray) and arr.shape == (3,)
    assert np.isclose(float(zt.pmf(2)), arr[1], rtol=1e-12)


def test_zt_rejects_degenerate_base():
    class AllZero:
        def pmf(self, k):
            return 1.0 if np.all(k == 0) else 0.0

        def cdf(self, k):
            return 1.0

        def mean(self):
            return 0.0

        def variance(self):
            return 0.0

        def sample(self, size=1):
            return np.zeros(size)

    with pytest.raises(ValueError):
        ZeroTruncated(AllZero())


# ----------------------------------------------------------------- Logarithmic
def test_logarithmic_pmf_zero_and_sum():
    log_d = Logarithmic(3.0)
    assert float(log_d.pmf(0)) == 0.0
    assert np.isclose(_pmf_sum(log_d), 1.0, atol=1e-9)


def test_logarithmic_mean_variance():
    beta = 3.0
    c = log(1 + beta)
    log_d = Logarithmic(beta)
    assert np.isclose(log_d.mean(), beta / c, rtol=1e-12)
    assert np.isclose(log_d.variance(), beta * (1 + beta - beta / c) / c, rtol=1e-12)


def test_logarithmic_pmf_values():
    beta = 3.0
    c = log(1 + beta)
    r = beta / (1 + beta)
    log_d = Logarithmic(beta)
    for k in (1, 2, 5):
        assert np.isclose(float(log_d.pmf(k)), r**k / (k * c), rtol=1e-12)


def test_logarithmic_sample():
    np.random.seed(3)
    log_d = Logarithmic(3.0)
    s = log_d.sample(50000)
    assert np.all(s >= 1)
    assert np.isclose(s.mean(), log_d.mean(), rtol=0.05)


def test_logarithmic_rejects_bad_beta():
    with pytest.raises(ValueError):
        Logarithmic(0.0)
    with pytest.raises(ValueError):
        Logarithmic(-1.0)


# ---------------------------------------------------------------- ZeroModified
def _zt_moments(base):
    p0 = float(base.pmf(0))
    ztm = base.mean() / (1 - p0)
    ztv = (base.variance() + base.mean() ** 2) / (1 - p0) - ztm**2
    return ztm, ztv


def test_zm_pmf_zero_and_sum():
    zm = ZeroModified(Poisson(2.0), 0.4)
    assert np.isclose(float(zm.pmf(0)), 0.4)
    assert np.isclose(_pmf_sum(zm), 1.0, atol=1e-9)


def test_zm_mean_variance():
    p0m = 0.4
    base = Poisson(2.0)
    zm = ZeroModified(base, p0m)
    ztm, ztv = _zt_moments(base)
    assert np.isclose(zm.mean(), (1 - p0m) * ztm, rtol=1e-12)
    assert np.isclose(
        zm.variance(), (1 - p0m) * ztv + p0m * (1 - p0m) * ztm**2, rtol=1e-12
    )


def test_zm_reduces_to_truncated_when_p0_zero():
    base = Poisson(2.0)
    zm = ZeroModified(base, 0.0)
    zt = ZeroTruncated(base)
    assert np.isclose(zm.mean(), zt.mean(), rtol=1e-12)
    assert np.isclose(float(zm.pmf(3)), float(zt.pmf(3)), rtol=1e-12)


def test_zm_cdf_monotone_and_limit():
    zm = ZeroModified(Poisson(2.0), 0.4)
    c = zm.cdf(np.arange(0, 40))
    assert np.isclose(c[0], 0.4)  # cdf(0) = p0_modified
    assert np.all(np.diff(c) >= -1e-12)
    assert c[-1] > 0.999


def test_zm_sample():
    np.random.seed(5)
    zm = ZeroModified(Poisson(2.0), 0.4)
    s = zm.sample(30000)
    assert s.shape == (30000,)
    assert np.all(s >= 0)
    assert np.isclose((s == 0).mean(), 0.4, atol=0.02)  # ~p0_modified zeros
    assert np.isclose(s.mean(), zm.mean(), rtol=0.06)


def test_zm_rejects_bad_p0():
    with pytest.raises(ValueError):
        ZeroModified(Poisson(2.0), 1.0)
    with pytest.raises(ValueError):
        ZeroModified(Poisson(2.0), -0.1)
