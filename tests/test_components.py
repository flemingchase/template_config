import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import install


class ComponentSelectionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.home = self.root / 'home'
        self.bundle = Path(install.__file__).resolve().parent

    def plan(self, **options):
        return install.plan(self.bundle, self.home, self.home / '.config',
                            self.home / '.local/share', **options)

    def test_core_restore_owns_only_requested_application_files(self):
        components = {'zsh', 'vim', 'qtile', 'alacritty', 'qutebrowser'}
        writes = self.plan(components=components)
        paths = {path.relative_to(self.home) for path, _, _ in writes}
        for expected in ('.zshrc', '.vimrc', '.vim/autoload/plug.vim',
                         '.config/qtile/config.py', '.config/qtile/wallpaper.jpg',
                         '.config/alacritty/alacritty.toml',
                         '.config/qutebrowser/config.py', '.config/qutebrowser/blank.html'):
            self.assertIn(Path(expected), paths)
        allowed = (Path('.vim'), Path('.config/qtile'), Path('.config/alacritty'),
                   Path('.config/qutebrowser'))
        for path in paths:
            self.assertTrue(path in (Path('.zshrc'), Path('.vimrc')) or
                            any(path.is_relative_to(prefix) for prefix in allowed), path)
        self.assertFalse(self.home.exists())

    def test_file_manager_and_qt_palette_can_be_selected_separately(self):
        files = {path.relative_to(self.home) for path, _, _ in self.plan(components={'pcmanfm-qt'})}
        self.assertIn(Path('.local/bin/pcmanfm-themed'), files)
        self.assertIn(Path('.local/share/applications/pcmanfm-qt.desktop'), files)
        self.assertTrue(any(path.is_relative_to('.config/pcmanfm-qt') for path in files))
        self.assertFalse(any(path.is_relative_to('.config/qt6ct') for path in files))
        palette = {path.relative_to(self.home) for path, _, _ in self.plan(components={'qt6ct'})}
        self.assertIn(Path('.config/environment.d/60-qt6ct.conf'), palette)
        self.assertIn(Path('.config/qt6ct/colors/gotham.conf'), palette)
        self.assertNotIn(Path('.local/bin/pcmanfm-themed'), palette)

    def test_only_selected_browser_profile_is_validated_and_modified(self):
        firefox = self.root / 'firefox'
        firefox.mkdir()
        # An unrelated browser's missing directory must not affect Firefox-only restoration.
        writes = self.plan(components={'firefox'}, firefox_profile=firefox,
                           librewolf_profile=self.root / 'missing-librewolf')
        self.assertEqual({path.relative_to(firefox).as_posix() for path, _, _ in writes},
                         {'user.js', 'chrome/userChrome.css', 'chrome/userContent.css'})
        self.assertEqual(self.plan(components={'firefox'}), [])
        self.assertFalse(self.home.exists())

    def test_unknown_components_fail_before_any_writes(self):
        for names in ('zsh,unknown', 'zsh,', ''):
            with self.subTest(names=names), contextlib.redirect_stderr(io.StringIO()) as error:
                result = install.main(['--home', str(self.home), '--components', names])
            self.assertEqual(result, 1)
            self.assertIn('component', error.getvalue())
            self.assertFalse(self.home.exists())
        with self.assertRaisesRegex(ValueError, 'Unknown template components'):
            self.plan(components={'unknown'})

    def test_repeated_cli_selection_preserves_unselected_existing_files(self):
        unrelated = self.home / '.config/sioyek/prefs_user.config'
        unrelated.parent.mkdir(parents=True)
        unrelated.write_text('personal Sioyek settings\n')
        with contextlib.redirect_stdout(io.StringIO()) as output:
            result = install.main(['--home', str(self.home), '--components', 'zsh',
                                   '--components', 'alacritty,qutebrowser'])
        self.assertEqual(result, 0)
        self.assertTrue((self.home / '.zshrc').is_file())
        self.assertTrue((self.home / '.config/alacritty/alacritty.toml').is_file())
        self.assertTrue((self.home / '.config/qutebrowser/blank.html').is_file())
        self.assertEqual(unrelated.read_text(), 'personal Sioyek settings\n')
        self.assertFalse((self.home / '.vimrc').exists())
        self.assertNotIn('Vim plugins:', output.getvalue())
        self.assertNotIn('Firefox overlay', output.getvalue())

    def test_listing_components_has_no_restore_side_effects(self):
        with patch.object(install, 'save') as save, contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(install.main(['--list-components', '--home', str(self.home)]), 0)
        self.assertEqual(set(output.getvalue().splitlines()), install.COMPONENTS)
        self.assertNotIn('ly', install.COMPONENTS)
        self.assertNotIn('plymouth', install.COMPONENTS)
        save.assert_not_called()
        self.assertFalse(self.home.exists())


if __name__ == '__main__':
    unittest.main()
