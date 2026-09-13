from uuid import uuid4

from xmg_qa2.infrastructure.checkpoint.postgres import PostgresCheckpointAdapter
from xmg_qa2.runtime.execution_service import ReconciliationAction, reconcile_operation

DATABASE_URL = "postgresql://xmg_qa2:xmg_qa2@localhost:5432/xmg_qa2"


def test_real_langgraph_postgres_checkpoint_setup_and_marker_roundtrip() -> None:
    adapter = PostgresCheckpointAdapter(DATABASE_URL)
    adapter.setup()
    run_id = str(uuid4())
    adapter.record_operation(run_id, "operation-1")
    assert adapter.operation(run_id) == "operation-1"


def test_business_commit_ahead_advances_checkpoint() -> None:
    assert reconcile_operation(checkpoint_operation_id="previous", business_operation_id="committed", operation_is_safe_to_repeat=True) is ReconciliationAction.ADVANCE_CHECKPOINT


def test_checkpoint_only_effect_is_not_business_truth() -> None:
    assert reconcile_operation(checkpoint_operation_id="checkpoint-only", business_operation_id=None, operation_is_safe_to_repeat=True) is ReconciliationAction.RERUN_SAFE_OPERATION
    assert reconcile_operation(checkpoint_operation_id="checkpoint-only", business_operation_id=None, operation_is_safe_to_repeat=False) is ReconciliationAction.PAUSE_UNSAFE_OPERATION
