def test_coverage():
    import coverage
    cov = coverage.Coverage()
    cov.load()
    percent = cov.report()
    assert percent >= 90, f"Coverage is {percent}%, must be ≥90%"
