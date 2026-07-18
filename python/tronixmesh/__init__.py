"""Tronix Mesh Phase B runtime primitives."""

from .coordinate import MeshCoordinate
from .envelope import ContextEnvelope, SignatureBlock
from .flags import FeatureFlags
from .governance import GovernanceState, may_execute, transition
from .memory import CellMemoryStore
from .provenance import ProvenanceStore, ProvenanceEvent
from .router import RulesRouter
from .runner import IdempotentStepRunner

__version__ = "0.2.0"

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
    "CellMemoryStore",
    "RulesRouter",
    "IdempotentStepRunner",
    "__version__",
]
