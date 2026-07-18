from evals.v0.harness import run_eval_v0


def test_eval_v0_meets_floor():
    report = run_eval_v0()
    assert report.total >= 10
    assert report.accuracy >= 0.9
    assert report.silent_forced == 0
    assert report.fp == 0
    assert report.fn == 0
