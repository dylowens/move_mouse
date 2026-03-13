import ctypes
import unittest
from ctypes import wintypes

import mouse_jiggler


class EnsureWintypesAliasesTests(unittest.TestCase):
    def test_missing_hcursor_alias_is_restored(self):
        had_hcursor = hasattr(wintypes, "HCURSOR")
        original_hcursor = getattr(wintypes, "HCURSOR", None)
        try:
            if had_hcursor:
                delattr(wintypes, "HCURSOR")

            mouse_jiggler._ensure_wintypes_aliases()

            self.assertTrue(hasattr(wintypes, "HCURSOR"))
            self.assertIs(wintypes.HCURSOR, ctypes.c_void_p)
        finally:
            if hasattr(wintypes, "HCURSOR"):
                delattr(wintypes, "HCURSOR")
            if had_hcursor:
                setattr(wintypes, "HCURSOR", original_hcursor)

    def test_tray_text_reflects_running_state(self):
        app = mouse_jiggler.MouseJigglerTrayApp()
        self.assertEqual(app._tray_text(), "Mouse Jiggler (Stopped)")
        app.running = True
        self.assertEqual(app._tray_text(), "Mouse Jiggler (Running)")


if __name__ == "__main__":
    unittest.main()
