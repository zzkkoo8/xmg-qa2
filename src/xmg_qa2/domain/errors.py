"""Project-owned domain failures."""


class DomainError(Exception):
    """Base class for failures caused by invalid domain operations."""


class InvalidTransition(DomainError):
    """A task status transition violates the lifecycle."""


class StaleStateVersion(DomainError):
    """An operation used an obsolete optimistic-concurrency version."""


class DraftHashMismatch(DomainError):
    """An answer check does not refer to the supplied draft content."""
