import pytest

from tronixmesh.coordinate import MeshCoordinate


def test_parse_and_canonical():
    c = MeshCoordinate.parse(
        "L2R.Buildtronix.Engineering.research.public.balanced.text.long"
    )
    assert c.function == "research"
    assert c.sensitivity == "public"
    assert str(c) == "L2R.Buildtronix.Engineering.research.public.balanced.text.long"


def test_invalid_segment_count():
    with pytest.raises(ValueError):
        MeshCoordinate.parse("L2R.Buildtronix.Engineering.research")


def test_sensitivity_increase():
    pub = MeshCoordinate.parse(
        "L2R.Buildtronix.Engineering.research.public.balanced.text.long"
    )
    conf = MeshCoordinate.parse(
        "L2R.Buildtronix.Engineering.structure.confidential.frontier.text.medium"
    )
    assert pub.is_sensitivity_increase(conf)
    assert not conf.is_sensitivity_increase(pub)
