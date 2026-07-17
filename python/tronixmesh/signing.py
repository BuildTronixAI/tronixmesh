"""Signature helpers — Ed25519 intended first algorithm; opaque layout (ADR-0004)."""

from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat


ALGORITHM_ED25519 = "ed25519"
ALGORITHM_HMAC_SHA256 = "hmac-sha256"


@dataclass(frozen=True)
class SigningKey:
    key_id: str
    algorithm_id: str
    private_key_bytes: bytes


def generate_ed25519_key(key_id: str) -> tuple[SigningKey, bytes]:
    """Return (signing key, raw 32-byte public key)."""
    priv = Ed25519PrivateKey.generate()
    pub = priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    return (
        SigningKey(
            key_id=key_id,
            algorithm_id=ALGORITHM_ED25519,
            private_key_bytes=priv.private_bytes_raw(),
        ),
        pub,
    )


def sign_bytes(key: SigningKey, message: bytes) -> bytes:
    if key.algorithm_id == ALGORITHM_ED25519:
        priv = Ed25519PrivateKey.from_private_bytes(key.private_key_bytes)
        return priv.sign(message)
    if key.algorithm_id == ALGORITHM_HMAC_SHA256:
        return hmac.new(key.private_key_bytes, message, hashlib.sha256).digest()
    raise ValueError(f"unsupported algorithm_id: {key.algorithm_id}")


def verify_bytes(
    *,
    algorithm_id: str,
    public_key_bytes: bytes,
    message: bytes,
    signature: bytes,
) -> bool:
    if algorithm_id == ALGORITHM_ED25519:
        try:
            pub = Ed25519PublicKey.from_public_bytes(public_key_bytes)
            pub.verify(signature, message)
            return True
        except (InvalidSignature, ValueError):
            return False
    if algorithm_id == ALGORITHM_HMAC_SHA256:
        expected = hmac.new(public_key_bytes, message, hashlib.sha256).digest()
        return hmac.compare_digest(expected, signature)
    return False
