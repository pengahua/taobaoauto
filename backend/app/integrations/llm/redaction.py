import re


PHONE_RE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
ORDER_RE = re.compile(r"(?<!\d)\d{12,20}(?!\d)")


def redact_text(text: str) -> str:
    text = PHONE_RE.sub("1**********", text)
    text = ORDER_RE.sub("[ORDER_ID]", text)
    return text


def redact_facts(facts: dict[str, str]) -> dict[str, str]:
    sensitive_keys = {"phone", "mobile", "address", "receiver", "receiver_name"}
    redacted: dict[str, str] = {}
    for key, value in facts.items():
        if key.lower() in sensitive_keys:
            redacted[key] = "[REDACTED]"
        else:
            redacted[key] = redact_text(str(value))
    return redacted

