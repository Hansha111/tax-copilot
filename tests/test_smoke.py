def test_package_imports():
    import gstcopilot
    from gstcopilot import config

    assert gstcopilot.__version__
    assert config.DRC01C_PCT_THRESHOLD == 20
    assert config.DRC01C_AMOUNT_THRESHOLD == 2_500_000
