from tronixmesh.authority import BootstrapGrant, MinimalAuthorityModule
from tronixmesh.channel import ChannelRuleEngine
from tronixmesh.flags import FeatureFlags
from tronixmesh.handoff import HandoffService
from tronixmesh.provenance import ProvenanceStore
from tronixmesh.registry import CoordinateRegistry
from tronixmesh.signing import generate_ed25519_key


RESEARCH = "L2R.Buildtronix.Engineering.research.public.balanced.text.long"
STRUCTURE = "L2R.Buildtronix.Engineering.structure.confidential.frontier.text.medium"
REVIEW = "L2R.Buildtronix.Engineering.review.confidential.frontier.text.long"


def _service(*, verify: bool = False) -> HandoffService:
    reg = CoordinateRegistry()
    reg.register(STRUCTURE, "agent://structure")
    reg.register(REVIEW, "agent://review")
    auth = MinimalAuthorityModule()
    auth.add_grant(
        BootstrapGrant(
            grant_id="grant-pub-to-conf",
            source_function="research",
            dest_function="structure",
            allow_sensitivity_increase=True,
        )
    )
    return HandoffService(
        registry=reg,
        channels=ChannelRuleEngine(),
        authority=auth,
        provenance=ProvenanceStore(":memory:"),
        flags=FeatureFlags(verify_signatures=verify),
    )


def test_sensitivity_increase_handoff_with_authority():
    svc = _service(verify=True)
    key, pub = generate_ed25519_key("pilot-key")
    result = svc.handoff(
        task_id="task-ci-1",
        source=RESEARCH,
        destination=STRUCTURE,
        payload={"competitor": "Procore"},
        signing_key=key,
        verify_public_key=pub,
    )
    assert result.ok
    assert result.grant_id == "grant-pub-to-conf"
    assert result.envelope is not None
    assert "sensitivity-elevated" in result.envelope.tags
    assert svc.provenance.verify_chain()


def test_sensitivity_increase_denied_without_grant():
    reg = CoordinateRegistry()
    reg.register(STRUCTURE, "agent://structure")
    svc = HandoffService(
        registry=reg,
        channels=ChannelRuleEngine(),
        authority=MinimalAuthorityModule(),
        provenance=ProvenanceStore(":memory:"),
    )
    result = svc.handoff(
        task_id="task-ci-2",
        source=RESEARCH,
        destination=STRUCTURE,
        payload={},
    )
    assert not result.ok
    assert "authority" in result.reason


def test_unroutable():
    svc = _service()
    result = svc.handoff(
        task_id="task-ci-3",
        source=STRUCTURE,
        destination="L2R.Buildtronix.Engineering.unknown.confidential.frontier.text.long",
        payload={},
    )
    assert not result.ok
    assert result.reason.startswith("UNROUTABLE")


def test_same_sensitivity_structure_to_review():
    svc = _service()
    result = svc.handoff(
        task_id="task-ci-4",
        source=STRUCTURE,
        destination=REVIEW,
        payload={"analysis": "..."},
    )
    assert result.ok
    assert result.grant_id is None
