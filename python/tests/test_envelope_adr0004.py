from tronixmesh.coordinate import MeshCoordinate
from tronixmesh.envelope import ContextEnvelope, SignatureBlock
from tronixmesh.signing import generate_ed25519_key


def test_signature_block_fields_frozen():
    block = SignatureBlock()
    data = block.to_dict()
    for key in (
        "signature_version",
        "algorithm_id",
        "key_id",
        "signed_at",
        "content_hash",
        "signature",
        "proof_extension",
    ):
        assert key in data


def test_sign_and_verify_ed25519():
    key, pub = generate_ed25519_key("key-pilot-001")
    env = ContextEnvelope(
        envelope_id="env-1",
        task_id="task-1",
        source=MeshCoordinate.parse(
            "L2R.Buildtronix.Engineering.research.public.balanced.text.long"
        ),
        destination=MeshCoordinate.parse(
            "L2R.Buildtronix.Engineering.structure.confidential.frontier.text.medium"
        ),
        payload={"summary": "procore public posture"},
    )
    env.signature.proof_extension = None
    env.sign(key)
    assert env.signature.algorithm_id == "ed25519"
    assert env.signature.content_hash
    assert env.signature.signature
    assert env.verify(pub)
    assert env.required_proof_fields_present()


def test_tamper_fails_verify():
    key, pub = generate_ed25519_key("key-pilot-002")
    env = ContextEnvelope(envelope_id="env-2", task_id="task-2", payload={"a": 1})
    env.sign(key)
    env.payload["a"] = 2
    assert not env.verify(pub)
