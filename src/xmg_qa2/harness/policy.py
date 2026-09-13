"""Local mandatory safety policy evaluated before provider invocation."""

from xmg_qa2.domain.capability import CapabilityEffect
from xmg_qa2.harness.contracts.policy import PolicyDecision, PolicyRequest


class DenyFirstPolicy:
    async def authorize(self, request: PolicyRequest) -> PolicyDecision:
        descriptor = request.descriptor
        if not descriptor.enabled:
            return self._deny("CAPABILITY_DISABLED", "Capability is disabled")
        if descriptor.effect is CapabilityEffect.WRITE:
            return self._deny("WRITE_NOT_ALLOWED", "Customer-target writes are prohibited")
        if descriptor.effect is CapabilityEffect.UNKNOWN:
            return self._deny("UNKNOWN_EFFECT", "Unknown capability effects are prohibited")

        metadata = descriptor.metadata
        allowed_cases = metadata.get("allowed_case_ids")
        if isinstance(allowed_cases, (list, tuple, set)) and request.context.case_id not in allowed_cases:
            return self._deny("CASE_SCOPE_DENIED", "Case is outside capability scope")
        allowed_principals = metadata.get("allowed_principal_ids")
        if (
            isinstance(allowed_principals, (list, tuple, set))
            and request.context.principal_id not in allowed_principals
        ):
            return self._deny("PRINCIPAL_DENIED", "Principal is outside capability scope")
        if request.arguments.get("schema_hash") not in (None, descriptor.schema_hash):
            return self._deny("SCHEMA_MISMATCH", "Request schema does not match capability")
        if request.arguments.get("external_data_export") and not metadata.get(
            "allow_external_data_export", False
        ):
            return self._deny("DATA_EXPORT_DENIED", "External data export is prohibited")
        return PolicyDecision(True, "ALLOWED", "Capability invocation allowed")

    @staticmethod
    def _deny(reason_code: str, safe_reason: str) -> PolicyDecision:
        return PolicyDecision(False, reason_code, safe_reason)
