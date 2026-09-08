"""Built-in passive checks."""

from .base import Check
from .excessive_surface import ExcessiveSurfaceCheck
from .injection_susceptible_description import InjectionSusceptibleDescriptionCheck
from .overprivileged_tool import OverprivilegedToolCheck
from .secret_exposure import SecretExposureCheck
from .unscoped_remote_exposure import UnscopedRemoteExposureCheck
from .weak_input_validation import WeakInputValidationCheck

DEFAULT_CHECKS: tuple[Check, ...] = (
    OverprivilegedToolCheck(),
    InjectionSusceptibleDescriptionCheck(),
    WeakInputValidationCheck(),
    SecretExposureCheck(),
    UnscopedRemoteExposureCheck(),
    ExcessiveSurfaceCheck(),
)

__all__ = ["DEFAULT_CHECKS", "Check"]
