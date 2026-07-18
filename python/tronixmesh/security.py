"""Phase B security floor checks — fail closed; no silent bypass."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .coordinate import MeshCoordinate
from .envelope import ContextEnvelope
from .flags import FeatureFlags


@dataclass(frozen=True)
class SecurityFinding:
    code: str
    ok: bool
    detail: str


def check_cross_cell(source: MeshCoordinate, destination: MeshCoordinate) -> SecurityFinding:
    if source.middle_cell() != destination.middle_cell():
        return SecurityFinding(
            "S1_CROSS_CELL",
            False,
            "cross-middle-cell handoff denied in Phase B",
        )
    return SecurityFinding("S1_CROSS_CELL", True, "same middle cell")


def check_signature_floor(
    envelope: ContextEnvelope,
    *,
    flags: FeatureFlags,
    public_key: Optional[bytes] = None,
) -> SecurityFinding:
    if not flags.verify_signatures:
        return SecurityFinding("S2_SIGNATURE", True, "verify_signatures off — skipped")
    if public_key is None:
        return SecurityFinding("S2_SIGNATURE", False, "verify on but no public key")
    if not envelope.verify(public_key):
        return SecurityFinding("S2_SIGNATURE", False, "invalid envelope signature (F10)")
    return SecurityFinding("S2_SIGNATURE", True, "signature valid")


def check_no_model_authority(worker_output: dict) -> SecurityFinding:
    """Workers must not claim authority fields."""
    banned = {"grant_id", "authority", "decision_token", "authorize"}
    keys = set(worker_output.keys())
    hit = keys & banned
    if hit:
        return SecurityFinding(
            "S3_MODEL_AUTHORITY",
            False,
            f"worker output claimed authority fields: {sorted(hit)}",
        )
    return SecurityFinding("S3_MODEL_AUTHORITY", True, "no authority fields in worker output")


def security_floor_report(
    *,
    source: MeshCoordinate,
    destination: MeshCoordinate,
    envelope: Optional[ContextEnvelope] = None,
    flags: Optional[FeatureFlags] = None,
    public_key: Optional[bytes] = None,
    worker_output: Optional[dict] = None,
) -> list[SecurityFinding]:
    findings = [check_cross_cell(source, destination)]
    if envelope is not None:
        findings.append(
            check_signature_floor(envelope, flags=flags or FeatureFlags(), public_key=public_key)
        )
    if worker_output is not None:
        findings.append(check_no_model_authority(worker_output))
    return findings
