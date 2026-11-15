import contextlib
import importlib.util
import io
import os
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch

import install


class QtPaletteTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.bundle = Path(install.__file__).resolve().parent

    def test_restore_resolves_palette_under_destination_config(self):
        home = self.root / 'destination home'
        config = self.root / 'custom config "quotes",semicolon;back\\slash\nline\rtab\tend'
        writes = install.plan(self.bundle, home, config, home / '.local/share')
        planned = {path: (content, mode) for path, content, mode in writes}
        settings = config / 'qt6ct/qt6ct.conf'
        palette = config / 'qt6ct/colors/gotham.conf'
        self.assertIn(palette, planned)
        self.assertIn(config / 'environment.d/60-qt6ct.conf', planned)
        self.assertNotIn(config / 'pcmanfm-qt/theme.qss', planned)
        text = planned[settings][0].decode()
        self.assertIn('color_scheme_path="' + str(self.root) +
                      '/custom config \\"quotes\\",semicolon;back\\\\slash\\nline\\rtab\\tend/qt6ct/colors/gotham.conf"', text)
        self.assertNotIn(str(self.bundle), text)
        self.assertIn('custom_palette=true', text)
        self.assertIn('style=Fusion', text)
        with contextlib.redirect_stdout(io.StringIO()):
            for target in (settings, palette):
                self.assertTrue(install.save(target, *planned[target]))
                self.assertFalse(install.save(target, *planned[target]))
        if importlib.util.find_spec('PyQt6') is not None:
            from PyQt6.QtCore import QSettings
            loaded = QSettings(str(settings), QSettings.Format.IniFormat)
            self.assertEqual(loaded.value('Appearance/color_scheme_path'), str(palette))
            self.assertEqual(loaded.status(), QSettings.Status.NoError)

    def test_pcmanfm_launcher_uses_native_palette_and_preserves_arguments(self):
        launcher = self.bundle / '.local/bin/pcmanfm-themed'
        arguments = ['folder with spaces', 'file:///tmp/one%20two']
        with patch.dict(os.environ, {'QT_QPA_PLATFORMTHEME': 'other'}), \
             patch('shutil.which', return_value='/usr/bin/pcmanfm-qt'), \
             patch('os.execv') as execute, \
             patch('sys.argv', [str(launcher), *arguments]):
            runpy.run_path(str(launcher), run_name='__main__')
            self.assertEqual(os.environ['QT_QPA_PLATFORMTHEME'], 'qt6ct')
            execute.assert_called_once_with('/usr/bin/pcmanfm-qt',
                                            ['/usr/bin/pcmanfm-qt', *arguments])


if __name__ == '__main__':
    unittest.main()
