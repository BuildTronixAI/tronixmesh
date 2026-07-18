from evals.v1.campaign import run_campaign


def test_eval_v1_campaign_meets_floor():
    report = run_campaign(set_name="v1")
    assert report.total >= 18
    assert report.accuracy >= 0.9
    assert report.silent_forced == 0
    assert report.fp_rate_public <= 0.02
    assert report.fn_rate_boundary <= 0.05
    assert report.meets_floor
