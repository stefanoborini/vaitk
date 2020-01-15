from vaitk import utils


def test_strformat():
    assert utils.strformat([], 40) == " "*40
    assert (
        utils.strformat([(0, "hello"), (10, "ciao"), (30, "whatever")], 40) ==
        "hello     ciao                whatever  "
    )
    # 01234567890123456789012345678901234567890
    assert (
        utils.strformat([(0, "hello"), (5, "ciao"), (36, "whatever")], 40) ==
        "hellociao                           what")

    # 01234567890123456789012345678901234567890
    assert (
        utils.strformat([(0, "hello"), (3, "ciao"), (36, "whatever")], 40) ==
        "helciao                             what")
    # 01234567890123456789012345678901234567890

    assert (
        utils.strformat([(10, "hello"), (23, "ciao"), (36, "whatever")], 40) ==
        "          hello        ciao         what")
    # 01234567890123456789012345678901234567890

    assert (
        utils.strformat([(10, "hello"), (3, "ciao"), (36, "whatever")], 40) ==
        "   ciao   hello                     what")
    # 01234567890123456789012345678901234567890


def test_clamp():
    assert utils.clamp(30, 0, 50) == 30
    assert utils.clamp(30, 0, 20) == 20
    assert utils.clamp(30, 40, 60) == 40
