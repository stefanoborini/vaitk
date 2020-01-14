import vaitk
from vaitk import keys
from vaitk.keys import (
    native_to_vai_key_code,
    is_key_code_printable,
    KeyModifier,
    vai_key_code_to_text)


def test_native_to_vaitk():
    assert native_to_vai_key_code(ord('a')) == keys.Key.Key_A
    assert (
            native_to_vai_key_code(ord('A')) ==
            keys.Key.Key_A | KeyModifier.ShiftModifier)
    assert native_to_vai_key_code(337) is None


def test_is_keycode_printable():
    assert is_key_code_printable(keys.Key.Key_A)
    assert is_key_code_printable(
        keys.Key.Key_A | KeyModifier.ShiftModifier
    )
    assert not is_key_code_printable(vaitk.keys.Key.Key_Escape)


def test_vai_key_code_to_text():
    assert vai_key_code_to_text(vaitk.keys.Key.Key_A) == 'a'
    assert vai_key_code_to_text(vaitk.keys.Key.Key_Escape) == ''
