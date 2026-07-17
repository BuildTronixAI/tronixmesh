"""Tronix Mesh Phase B runtime primitives."""

from .coordinate import MeshCoordinate
from .envelope import ContextEnvelope, SignatureBlock
from .flags import FeatureFlags
from .governance import GovernanceState, may_execute, transition
from .provenance import ProvenanceStore, ProvenanceEvent

__version__ = "0.1.0"

__all__ = [
    "MeshCoordinate",
    "ContextEnvelope",
    "SignatureBlock",
    "FeatureFlags",
    "GovernanceState",
    "may_execute",
    "transition",
    "ProvenanceStore",
    "ProvenanceEvent",
    "__version__",
]
