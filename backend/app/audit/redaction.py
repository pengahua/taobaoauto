MASK = "***"


def redact_sensitive(value: str | None, visible_suffix: int = 4) -> str | None:
    if value is None:
        return None
    if len(value) <= visible_suffix:
        return MASK
    return f"{MASK}{value[-visible_suffix:]}"


def redact_payload(payload: dict) -> dict:
    sensitive_keys = {"phone", "mobile", "address", "token", "secret", "session_key"}
    return {
        key: MASK if key.lower() in sensitive_keys else value
        for key, value in payload.items()
    }

