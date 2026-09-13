"""Project-owned domain failures."""


class DomainError(Exception):
    """Base class for failures caused by invalid domain operations."""


class InvalidTransition(DomainError):
    """A task status transition violates the lifecycle."""


class StaleStateVersion(DomainError):
    """An operation used an obsolete optimistic-concurrency version."""


class DraftHashMismatch(DomainError):
    """An answer check does not refer to the supplied draft content."""


class ProviderError(Exception):
    """Base class for project-owned provider failures."""


class ProviderUnavailable(ProviderError):
    pass


class ProviderRateLimited(ProviderError):
    pass


class ProviderTimeout(ProviderError):
    pass


class ProviderMalformedResponse(ProviderError):
    pass


class ProviderAuthorizationFailed(ProviderError):
    pass


class CapabilityNotFound(ProviderError):
    pass


class CapabilityDisabled(ProviderError):
    pass


class CapabilitySchemaMismatch(ProviderError):
    pass


class PolicyDenied(ProviderError):
    pass
