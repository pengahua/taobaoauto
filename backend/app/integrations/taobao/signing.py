import hashlib


def sign_top_request(params: dict[str, object], app_secret: str) -> str:
    """Create TOP MD5 signature.

    TOP's common signature style sorts parameter names, concatenates key/value
    pairs between app_secret on both sides, then applies MD5 uppercase.
    Binary uploads and multipart signing are intentionally out of MVP scope.
    """
    filtered = {
        key: value
        for key, value in params.items()
        if value is not None and key != "sign"
    }
    canonical = "".join(f"{key}{filtered[key]}" for key in sorted(filtered))
    payload = f"{app_secret}{canonical}{app_secret}".encode("utf-8")
    return hashlib.md5(payload).hexdigest().upper()


def attach_signature(params: dict[str, object], app_secret: str) -> dict[str, object]:
    signed = dict(params)
    signed["sign"] = sign_top_request(signed, app_secret)
    return signed

