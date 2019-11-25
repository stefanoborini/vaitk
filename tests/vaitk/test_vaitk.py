import unittest
import vaitk


class TestVaiTk(unittest.TestCase):
    def testNativeToVaiKeyCode(self):
        self.assertEqual(vaitk.native_to_vai_key_code(ord('a')),
                         vaitk.Key.Key_A)
        self.assertEqual(vaitk.native_to_vai_key_code(ord('A')),
                         vaitk.Key.Key_A | vaitk.KeyModifier.ShiftModifier)
        self.assertEqual(vaitk.native_to_vai_key_code(337), None)

    def testIsKeyCodePrintable(self):
        self.assertTrue(vaitk.isKeyCodePrintable(vaitk.Key.Key_A))
        self.assertTrue(vaitk.isKeyCodePrintable(
            vaitk.Key.Key_A | vaitk.KeyModifier.ShiftModifier))
        self.assertFalse(vaitk.isKeyCodePrintable(vaitk.Key.Key_Escape))

    def testVaiKeyCodeToText(self):
        self.assertEqual(vaitk.vai_key_code_to_text(vaitk.Key.Key_A), 'a')
        self.assertEqual(vaitk.vai_key_code_to_text(vaitk.Key.Key_Escape), '')


if __name__ == '__main__':
    unittest.main()
