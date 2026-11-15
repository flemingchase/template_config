import contextlib
import io
from pathlib import Path
import tempfile
import unittest

import install


class BrowserOverlayTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.bundle = Path(install.__file__).resolve().parent
        self.home = self.root / "home"
        self.firefox = self.root / "firefox-profile"
        self.librewolf = self.root / "librewolf-profile"
        self.firefox.mkdir()
        self.librewolf.mkdir()

    def test_both_browser_overlays_are_planned_independently(self):
        writes = install.plan(
            self.bundle, self.home, self.home / ".config",
            self.home / ".local/share", firefox_profile=self.firefox,
            librewolf_profile=self.librewolf, zshdir=self.home)
        planned = {path: (content, mode) for path, content, mode in writes}
        for profile, overlay in ((self.firefox, "firefox-profile"),
                                 (self.librewolf, "librewolf-profile")):
            for relative in (Path("user.js"), Path("chrome/userChrome.css"),
                             Path("chrome/userContent.css")):
                destination = profile / relative
                self.assertIn(destination, planned)
                self.assertEqual(planned[destination][0],
                                 (self.bundle / overlay / relative).read_bytes())
                self.assertEqual(planned[destination][1], 0o600)

    def test_templates_share_current_defaults_and_square_tabs(self):
        firefox_css = (self.bundle / "firefox-profile/chrome/userChrome.css").read_text()
        librewolf_css = (self.bundle / "librewolf-profile/chrome/userChrome.css").read_text()
        firefox_content = (self.bundle / "firefox-profile/chrome/userContent.css").read_text()
        librewolf_content = (self.bundle / "librewolf-profile/chrome/userContent.css").read_text()
        firefox_prefs = (self.bundle / "firefox-profile/user.js").read_text()
        librewolf_prefs = (self.bundle / "librewolf-profile/user.js").read_text()
        self.assertEqual(firefox_css, librewolf_css)
        self.assertTrue(firefox_content.startswith(librewolf_content))
        self.assertEqual(firefox_prefs.split('// Current portable browser layout;')[0],
                         librewolf_prefs.split('// Current portable browser layout;')[0])
        self.assertIn("--palette-background: #0a0f14", firefox_css)
        self.assertIn("--palette-foreground: #98d1ce", firefox_css)
        self.assertIn("--tab-border-radius: 0px", firefox_css)
        self.assertIn("--tab-min-height: 18px", firefox_css)
        self.assertIn("--tab-content-button-size: 16px", firefox_css)
        self.assertIn("--tab-content-button-padding: 2px", firefox_css)
        self.assertIn("--tab-label-line-height: 1.2", firefox_css)
        self.assertIn("border-radius: 0 !important", firefox_css)
        self.assertIn("--panel-background-color: #0a0f14", firefox_css)
        self.assertIn("--panel-text-color: #98d1ce", firefox_css)
        self.assertIn("menupopup::part(content)", firefox_css)
        self.assertIn(":is(menu, menuitem):is([_moz-menuactive], :hover):not([disabled])",
                      firefox_css)
        self.assertIn("background-color: var(--palette-foreground)", firefox_css)
        self.assertIn("color: var(--palette-background)", firefox_css)
        self.assertIn("menuseparator::before", firefox_css)
        self.assertIn("--border-radius-circle: 0px", firefox_css)
        self.assertIn("--toolbarbutton-border-radius: 0px", firefox_css)
        self.assertIn("--urlbar-border-radius: 0px", firefox_css)
        self.assertIn("--panel-menuitem-border-radius: 0px", firefox_css)
        self.assertIn("--toolbar-field-background-color-focus: #0a0f14",
                      firefox_css)
        self.assertIn("--toolbar-field-text-color-focus: #98d1ce",
                      firefox_css)
        self.assertIn("--urlbarview-background-color-selected: #98d1ce",
                      firefox_css)
        self.assertIn("--urlbarview-text-color-selected: #0a0f14",
                      firefox_css)
        self.assertIn("#PopupSearchAutoComplete::part(content)", firefox_css)
        self.assertIn(".searchbar-engine-one-off-item", firefox_css)
        self.assertIn('@-moz-document url-prefix("about:preferences")',
                      firefox_content)
        self.assertIn("--background-color-canvas: var(--palette-background)",
                      firefox_content)
        self.assertIn("--text-color: var(--palette-foreground)",
                      firefox_content)
        self.assertIn("--card-border-radius: 0px", firefox_content)
        self.assertIn("--input-border-radius: 0px", firefox_content)
        self.assertIn('@-moz-document url("about:newtab"), url("about:home")',
                      firefox_content)
        self.assertIn("--newtab-background-color: var(--palette-background)",
                      firefox_content)
        self.assertIn("--newtab-text-primary-color: var(--palette-foreground)",
                      firefox_content)
        self.assertIn("content-search-handoff-ui", firefox_content)
        self.assertIn("--content-search-handoff-ui-background-color: var(--palette-background)",
                      firefox_content)
        self.assertIn('browser.display.document_color_use", 1', firefox_prefs)
        self.assertNotIn('browser.display.background_color', firefox_prefs + librewolf_prefs)
        self.assertNotIn('browser.display.foreground_color', firefox_prefs + librewolf_prefs)
        self.assertNotIn('layout.css.always_underline_links', firefox_prefs)
        self.assertIn('browser.display.document_color_use", 1', librewolf_prefs)
        self.assertIn('layout.css.prefers-color-scheme.content-override", 0', librewolf_prefs)
        self.assertNotIn('forced-color', firefox_content + librewolf_content)
        self.assertNotIn('privacy.resistFingerprinting', firefox_prefs + librewolf_prefs)

    def test_cli_accepts_both_profile_entries(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = install.main([
                "--home", str(self.home), "--dry-run",
                "--firefox-profile", str(self.firefox),
                "--librewolf-profile", str(self.librewolf),
            ])
        self.assertEqual(result, 0)
        preview = output.getvalue()
        self.assertIn(str(self.firefox / "chrome/userChrome.css"), preview)
        self.assertIn(str(self.librewolf / "chrome/userChrome.css"), preview)
        self.assertNotIn("overlay was not selected", preview)
        self.assertFalse(self.home.exists())

    def test_cli_installs_both_overlays_with_private_permissions(self):
        arguments = [
            "--home", str(self.home),
            "--firefox-profile", str(self.firefox),
            "--librewolf-profile", str(self.librewolf),
        ]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(install.main(arguments), 0)
            self.assertEqual(install.main(arguments), 0)
        for profile, overlay in ((self.firefox, "firefox-profile"),
                                 (self.librewolf, "librewolf-profile")):
            for relative in (Path("user.js"), Path("chrome/userChrome.css"),
                             Path("chrome/userContent.css")):
                destination = profile / relative
                self.assertEqual(destination.read_bytes(),
                                 (self.bundle / overlay / relative).read_bytes())
                self.assertEqual(destination.stat().st_mode & 0o777, 0o600)
                self.assertEqual(list(destination.parent.glob(
                    destination.name + ".template-backup-*")), [])

    def test_missing_librewolf_profile_fails_before_writes(self):
        missing = self.root / "missing"
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            result = install.main([
                "--home", str(self.home),
                "--librewolf-profile", str(missing),
            ])
        self.assertEqual(result, 1)
        self.assertIn("LibreWolf profile must already exist", error.getvalue())
        self.assertFalse(self.home.exists())


if __name__ == "__main__":
    unittest.main()
