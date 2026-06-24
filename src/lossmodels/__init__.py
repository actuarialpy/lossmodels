"""lossmodels: actuarial loss distributions, aggregate modeling, and fit diagnostics.

The full public API is surfaced here for convenience, so common entry points are
available directly as ``lossmodels.Lognormal``, ``lossmodels.fit_best_severity``,
``lossmodels.goodness_of_fit``, etc. Submodule imports
(``from lossmodels.severity import Lognormal``) continue to work unchanged.
"""

__version__ = "0.5.0"

from .severity import (
    SeverityModel,
    Exponential,
    Gamma,
    Lognormal,
    Pareto,
    SplicedSeverity,
    Weibull,
    # FAM / ASTAM continuous inventory (0.5.0)
    Burr,
    InverseBurr,
    GeneralizedPareto,
    ParetoII,
    InversePareto,
    Loglogistic,
    Paralogistic,
    InverseParalogistic,
    InverseGamma,
    InverseWeibull,
    InverseExponential,
    InverseGaussian,
    LogT,
    SingleParameterPareto,
    Beta,
    GeneralizedBeta,
)
from .frequency import (
    FrequencyModel,
    Binomial,
    Geometric,
    NegativeBinomial,
    Poisson,
    # (a, b, 1) class (0.5.0)
    ZeroTruncated,
    ZeroModified,
    Logarithmic,
)
from .aggregate import CollectiveRiskModel
from .empirical import EmpiricalSeverity, EmpiricalFrequency
from .estimation import (
    fit_exponential,
    fit_gamma,
    fit_lognormal,
    fit_pareto,
    fit_poisson,
    fit_weibull,
    fit_negbinomial,
    fit_mle,
    fit_best_severity,
    fit_best_frequency,
    log_likelihood,
    aic,
    bic,
    ks_statistic,
    anderson_darling,
    cramer_von_mises,
    tail_quantile_table,
    goodness_of_fit,
)

__all__ = [
    "__version__",
    "SeverityModel", "Exponential", "Gamma", "Lognormal", "Pareto",
    "SplicedSeverity", "Weibull",
    "Burr", "InverseBurr", "GeneralizedPareto", "ParetoII", "InversePareto",
    "Loglogistic", "Paralogistic", "InverseParalogistic",
    "InverseGamma", "InverseWeibull", "InverseExponential",
    "InverseGaussian", "LogT", "SingleParameterPareto",
    "Beta", "GeneralizedBeta",
    "FrequencyModel", "Binomial", "Geometric", "NegativeBinomial", "Poisson",
    "ZeroTruncated", "ZeroModified", "Logarithmic",
    "CollectiveRiskModel", "EmpiricalSeverity", "EmpiricalFrequency",
    "fit_exponential", "fit_gamma", "fit_lognormal", "fit_pareto", "fit_poisson",
    "fit_weibull", "fit_negbinomial", "fit_mle",
    "fit_best_severity", "fit_best_frequency",
    "log_likelihood", "aic", "bic",
    "ks_statistic", "anderson_darling", "cramer_von_mises",
    "tail_quantile_table", "goodness_of_fit",
]
