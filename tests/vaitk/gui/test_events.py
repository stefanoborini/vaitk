'''
import pytest

from vaitk.gui import KeyEvent
from vaitk.keys import Key, KeyModifier


def test_key_event():
    ev = KeyEvent.from_native_key_code(20)

    assert ev.key == Key.Key_T
    assert ev.modifiers == KeyModifier.ControlModifier


def test_raises_for_unknown_key():
    with pytest.raises(ValueError):
        KeyEvent.from_native_key_code(-2)
'''
