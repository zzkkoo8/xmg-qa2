from xmg_qa2.observability.logging import redact


def test_secrets_and_hidden_reasoning_are_redacted_recursively() -> None:
    secret = "super-secret-value"
    cleaned = redact(
        {
            "password": secret,
            "nested": {"authorization": f"Bearer {secret}"},
            "chain_of_thought": secret,
            "safe": "ok",
        }
    )
    assert secret not in repr(cleaned)
    assert cleaned["safe"] == "ok"
