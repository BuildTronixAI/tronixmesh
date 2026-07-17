"""Proof-native Context Envelope with ADR-0004 signature-agnostic block."""

from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Optional

from .coordinate import MeshCoordinate
from .signing import ALGORITHM_ED25519, SigningKey, sign_bytes, verify_bytes


SIGNATURE_VERSION = 1


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass
class SignatureBlock:
    """ADR-0004 frozen signature fields — algorithm-pluggable opaque blob."""

    signature_version: int = SIGNATURE_VERSION
    algorithm_id: str = ALGORITHM_ED25519
    key_id: str = ""
    signed_at: str = ""
    content_hash: str = ""
    signature: str = ""  # base64 opaque blob
    proof_extension: Optional[dict[str, Any]] = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> SignatureBlock:
        return cls(
            signature_version=int(data.get("signature_version", SIGNATURE_VERSION)),
            algorithm_id=str(data.get("algorithm_id", "")),
            key_id=str(data.get("key_id", "")),
            signed_at=str(data.get("signed_at", "")),
            content_hash=str(data.get("content_hash", "")),
            signature=str(data.get("signature", "")),
            proof_extension=data.get("proof_extension"),
        )


@dataclass
class ContextEnvelope:
    """
    Co-traveling package: payload + routing + authority + provenance refs + proof-native fields.

    Schema is proof-native even when verification is feature-flagged off.
    """

    envelope_id: str
    task_id: str
    schema_version: str = "1"
    source: Optional[MeshCoordinate] = None
    destination: Optional[MeshCoordinate] = None
    payload: dict[str, Any] = field(default_factory=dict)
    authority_refs: list[str] = field(default_factory=list)
    provenance_ref: Optional[str] = None
    governance_ref: Optional[str] = None
    proof_id: Optional[str] = None
    witness_coordinates: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=_utc_now)
    signature: SignatureBlock = field(default_factory=SignatureBlock)

    def canonical_bytes(self) -> bytes:
        """Canonical form for hashing/signing — excludes the signature block itself."""
        body = {
            "envelope_id": self.envelope_id,
            "task_id": self.task_id,
            "schema_version": self.schema_version,
            "source": self.source.canonical() if self.source else None,
            "destination": self.destination.canonical() if self.destination else None,
            "payload": self.payload,
            "authority_refs": self.authority_refs,
            "provenance_ref": self.provenance_ref,
            "governance_ref": self.governance_ref,
            "proof_id": self.proof_id,
            "witness_coordinates": self.witness_coordinates,
            "tags": self.tags,
            "created_at": self.created_at,
        }
        return json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
            "utf-8"
        )

    def content_hash(self) -> str:
        return hashlib.sha256(self.canonical_bytes()).hexdigest()

    def sign(self, key: SigningKey) -> None:
        canonical = self.canonical_bytes()
        digest = hashlib.sha256(canonical).hexdigest()
        sig = sign_bytes(key, canonical)
        self.signature = SignatureBlock(
            signature_version=SIGNATURE_VERSION,
            algorithm_id=key.algorithm_id,
            key_id=key.key_id,
            signed_at=_utc_now(),
            content_hash=digest,
            signature=base64.b64encode(sig).decode("ascii"),
            proof_extension=self.signature.proof_extension,
        )

    def verify(self, public_key_bytes: bytes) -> bool:
        if not self.signature.signature or not self.signature.content_hash:
            return False
        canonical = self.canonical_bytes()
        digest = hashlib.sha256(canonical).hexdigest()
        if digest != self.signature.content_hash:
            return False
        try:
            sig = base64.b64decode(self.signature.signature.encode("ascii"))
        except Exception:
            return False
        return verify_bytes(
            algorithm_id=self.signature.algorithm_id,
            public_key_bytes=public_key_bytes,
            message=canonical,
            signature=sig,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "envelope_id": self.envelope_id,
            "task_id": self.task_id,
            "schema_version": self.schema_version,
            "source": self.source.canonical() if self.source else None,
            "destination": self.destination.canonical() if self.destination else None,
            "payload": self.payload,
            "authority_refs": self.authority_refs,
            "provenance_ref": self.provenance_ref,
            "governance_ref": self.governance_ref,
            "proof_id": self.proof_id,
            "witness_coordinates": self.witness_coordinates,
            "tags": self.tags,
            "created_at": self.created_at,
            "signature": self.signature.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ContextEnvelope:
        src = data.get("source")
        dst = data.get("destination")
        return cls(
            envelope_id=str(data["envelope_id"]),
            task_id=str(data["task_id"]),
            schema_version=str(data.get("schema_version", "1")),
            source=MeshCoordinate.parse(src) if src else None,
            destination=MeshCoordinate.parse(dst) if dst else None,
            payload=dict(data.get("payload") or {}),
            authority_refs=list(data.get("authority_refs") or []),
            provenance_ref=data.get("provenance_ref"),
            governance_ref=data.get("governance_ref"),
            proof_id=data.get("proof_id"),
            witness_coordinates=list(data.get("witness_coordinates") or []),
            tags=list(data.get("tags") or []),
            created_at=str(data.get("created_at") or _utc_now()),
            signature=SignatureBlock.from_dict(data.get("signature") or {}),
        )

    def required_proof_fields_present(self) -> bool:
        """M7: proof-native fields present (populated or explicitly null-versioned)."""
        sig = self.signature
        return (
            self.schema_version is not None
            and sig.signature_version is not None
            and isinstance(sig.algorithm_id, str)
            and isinstance(sig.key_id, str)
            and isinstance(sig.content_hash, str)
            and isinstance(sig.signature, str)
            # proof_extension may be None explicitly
            and "proof_extension" in sig.to_dict()
        )
