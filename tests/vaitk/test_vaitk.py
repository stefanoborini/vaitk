import vaitk


def test_native_to_vaitk():
    assert vaitk.native_to_vai_key_code(ord('a')) == vaitk.Key.Key_A
    assert (
        vaitk.native_to_vai_key_code(ord('A')) ==
        vaitk.Key.Key_A | vaitk.KeyModifier.ShiftModifier)
    assert vaitk.native_to_vai_key_code(337) is None


def test_is_keycode_printable():
    assert vaitk.isKeyCodePrintable(vaitk.Key.Key_A)
    assert vaitk.isKeyCodePrintable(
        vaitk.Key.Key_A | vaitk.KeyModifier.ShiftModifier
    )
    assert not vaitk.isKeyCodePrintable(vaitk.Key.Key_Escape)


def test_vai_key_code_to_text():
    assert vaitk.vai_key_code_to_text(vaitk.Key.Key_A) == 'a'
    assert vaitk.vai_key_code_to_text(vaitk.Key.Key_Escape) == ''
