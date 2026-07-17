from tronixmesh.provenance import ProvenanceStore


def test_hash_chain_integrity():
    store = ProvenanceStore(":memory:")
    store.append(task_id="t1", event_type="START", payload={"n": 1})
    store.append(task_id="t1", event_type="HANDOFF", payload={"n": 2})
    store.append(task_id="t2", event_type="START", payload={"n": 3})
    assert store.verify_chain()
    events = store.all_events()
    assert events[0].prev_hash == ProvenanceStore.GENESIS
    assert events[1].prev_hash == events[0].entry_hash


def test_tamper_detected():
    store = ProvenanceStore(":memory:")
    store.append(task_id="t1", event_type="START", payload={})
    events = store.all_events()
    # Simulate tampering by reconstructing with wrong payload
    bad = events[0]
    from tronixmesh.provenance import ProvenanceEvent

    tampered = ProvenanceEvent(
        seq=bad.seq,
        task_id=bad.task_id,
        event_type=bad.event_type,
        payload={"evil": True},
        prev_hash=bad.prev_hash,
        entry_hash=bad.entry_hash,
        created_at=bad.created_at,
    )
    assert not store.verify_chain([tampered])
