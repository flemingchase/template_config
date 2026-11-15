Standalone application templates
================================

.. note::

   **Vibe-coding disclaimer:** this project was "vibe coded" with OpenAI Codex.
   Review and test the code and configuration before relying on it.

This bundle contains portable copies of the current application configurations
for Alacritty, Zathura, Rofi, Firefox, LibreWolf, Clementine, Sioyek,
PCManFM-Qt, Qtile and qutebrowser, together with the zsh and Vim setup, the Ly login-manager
configuration, and the active Plymouth boot-splash theme. Application colors are
fixed to the Gotham palette, matching the colors selected by ``chthm gotham``:
background ``#0a0f14``, foreground ``#98d1ce``, and its full normal/bright palette.
The copied configurations
have no chthm references, palette environment variables or dependency on a
separate theme-switching program.

The bundle was refreshed from the active settings on 2026-11-14 without
changing the active files. The portability notes below describe the copied settings.

Layout
------

* .config/: application settings, including Qtile's widget and wallpaper.
* .zshrc: shell preferences and functions, with theme integration removed.
* .vimrc and .vim/: Vim settings, custom TeX syntax, plugins and plugin manager.
* .config/qt6ct/: the standalone Gotham palette for Qt 6 applications.
* .config/environment.d/60-qt6ct.conf: selects the Qt 6 palette plugin.
* .local/bin/pcmanfm-themed: an independent launcher selecting the Qt 6 palette.
* .local/share/applications/pcmanfm-qt.desktop: a matching application entry.
* firefox-profile/: stylesheet and preference files for a Firefox profile.
* librewolf-profile/: stylesheet and preference files for a LibreWolf profile.
* etc/ly/config.ini: system-wide Ly login-manager settings (manual restore).
* etc/plymouth/plymouthd.conf: Plymouth daemon settings selecting the bundled theme.
* usr/share/plymouth/themes/arch-boot-dots/: active Plymouth theme, artwork and license.
* install.py: optional restore helper with dry-run support and backups.

Dot-prefixed directories may be hidden by your file manager. Keep them when
copying or archiving this folder.

Use on a fresh Arch installation
--------------------------------

Install your applications and a working desktop session first. This is an
application-configuration bundle, not an operating-system or display-manager
installer. It is prepared for the existing X11-oriented Qtile setup.

You need Python 3.11 or newer to use the restore helper. The helper uses only
Python's standard library and does not download or install packages.

Required applications:

* alacritty, zathura with a PDF plugin, rofi and Firefox and/or LibreWolf.
* clementine, pcmanfm-qt, qtile, qutebrowser and qt6ct.
* sioyek, with the documented interface-color options; the source machine
  uses sioyek-git.
* plymouth for the bundled arch-boot-dots boot-splash theme.

Supporting components:

* Fira Mono, supplied by the ttf-fira-mono package, for the configured fonts.
* A Zathura PDF backend, such as zathura-pdf-mupdf.
* Adwaita icons for PCManFM-Qt's configured fallback icon theme.
* xset for the custom Caps Lock widget. It falls back to an empty indicator
  when the command is missing or unavailable.
* xsel for the existing clipboard-clearing keybinding in Qtile.
* Optional: nvr for Zathura's SyncTeX editor command, file-roller for the file
  manager's archive integration, and lxqt-sudo for its elevated-action command.

Use the repositories or AUR appropriate to your chosen application versions.
The font and PDF-backend names are documented by Arch:
`Fira Mono <https://archlinux.org/packages/extra/any/ttf-fira-mono/>`_ and
`Zathura <https://archlinux.org/packages/extra/x86_64/zathura/>`_.

Close affected applications before restoring files. From this directory,
preview destinations first::

    python3 install.py --dry-run

Then restore the settings for your normal account, without sudo::

    python3 install.py

This copies .config, .local and the shell/Vim dotfiles, uses your HOME and XDG configuration/data
locations, and writes the PCManFM-Qt desktop entry with the correct launcher
path for the destination account. It also resolves the qt6ct color-scheme path
to the destination configuration directory. It preserves existing dotfile symlinks and
creates unique .template-backup-* files before replacing changed files.
Repeated installation skips unchanged files. No applications are restarted.
.zshrc goes to $ZDOTDIR/.zshrc if ZDOTDIR is set; otherwise it goes to ~/.zshrc.
.vimrc and .vim always go under the destination home. With --home, .zshrc also
goes under that home rather than inheriting the current account's ZDOTDIR.

For staging under a different destination home::

    python3 install.py --home /path/to/staging-home --dry-run

With --home, configuration and data go under that home's .config and
.local/share rather than inheriting the current account's XDG overrides.
The helper does not set up Qtile as a login session or configure audio,
networking, shell preferences, file associations or system services.

Firefox and LibreWolf profile overlays
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start each browser you want to configure once on the new installation so it
creates a profile. Find its Profile Directory on about:support, then close the
browser. Restore Firefox with its existing directory selected::

    python3 install.py --firefox-profile /path/to/actual/firefox/profile --dry-run
    python3 install.py --firefox-profile /path/to/actual/firefox/profile

Restore LibreWolf with its own existing directory selected::

    python3 install.py --librewolf-profile /path/to/actual/librewolf/profile --dry-run
    python3 install.py --librewolf-profile /path/to/actual/librewolf/profile

The options can be combined to configure both browsers in one run. Each adds
``chrome/userChrome.css``, ``chrome/userContent.css`` and ``user.js`` to only
the selected profile, with backups. They do not copy the source machine's
profile identifiers, cookies, passwords, browsing history, extensions or
accounts.

Both browser templates use Gotham: ``#0a0f14`` for
the background and ``#98d1ce`` for the foreground. Horizontal tabs are square,
gapless boxes with one-pixel foreground borders. Their 18-pixel minimum height
is half of Firefox 160's current 36-pixel default; the label line height and
close/audio controls are reduced with it so they do not force the tabs taller.
Custom browser stylesheets are enabled. The Settings page
(``about:preferences``) also uses that background and foreground for its
canvas, cards, dialogs, inputs and text instead of Firefox's or LibreWolf's
built-in dark gray surfaces. Browser context menus and popup panels use the
same palette for their surfaces, text, icons, borders and separators. Hovered
or keyboard-active menu rows invert the foreground and background pair. Tabs,
address and search fields, toolbar buttons, panels, menu rows, Settings cards,
dialogs, inputs and buttons all use square zero-radius corners. The toolbar
address/search field, its autocomplete and search-engine result rows, and the
search field on ``about:newtab`` and ``about:home`` all use the fixed palette;
selected or hovered results invert that foreground/background pair.

Each overlay also includes its current native toolbar button and spacer
arrangement, sidebar tool order and hide-on-close behavior. Firefox uses
125% interface scaling, a 20px default proportional text size, and a sparse
New Tab page with its logo, search, shortcuts, stories and widgets hidden.
LibreWolf retains its own scaling and text-size defaults. Extension-specific
buttons and machine-specific window dimensions are omitted from the overlays.
These preferences are applied from ``user.js`` on startup; to retain later
manual toolbar rearrangements, remove its ``browser.uiCustomization.state``
entry after the first launch.

Both Firefox and LibreWolf disable website color overrides and advertise a dark website preference;
websites choose whether to use their own dark palette. Site-defined colors, icons,
backgrounds and animations are preserved. The content stylesheet only applies
to browser-owned Settings, Home and New Tab pages; it contains no website rules
or per-site exceptions. Current Gecko uses standard document colors with forced
colors off, so it does not apply arbitrary theme hex colors to websites.

Fingerprint resistance is unchanged. LibreWolf can substitute standardized
colors for custom defaults under its privacy protections; this bundle accepts
that behavior instead of forcing a website palette.

Without the corresponding profile option, the helper skips that browser's
overlay and tells you so. Profile locations are installation-specific; see
`Mozilla's profile documentation <https://support.mozilla.org/en-US/kb/profiles-where-firefox-stores-user-data>`_.

qutebrowser website appearance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

qutebrowser advertises a dark website preference and disables automatic
recoloring. Websites retain their own styles. No website stylesheet or per-site
exception is installed. The native white fallback background is preserved:
qutebrowser has no matching default text-color option, so forcing a dark
fallback would make unstyled black text unreadable.

The local ``.config/qutebrowser/blank.html`` page uses the fixed Gotham
palette and is selected for empty new tabs and startup. Keep that file beside
``config.py`` when copying manually. The path is resolved relative to the
configuration directory. Browser interface colors remain themed. Restart
qutebrowser after restoring.

The layout matches the current qutebrowser setup: tabs stay at the top, the
bottom status bar appears only in modes that need it, and tab progress
indicators are hidden. Tab titles show the host, pinned tabs show their index,
and default page zoom is 125%. Fira Mono at 22pt, centered tab labels, tab
padding, hidden window decorations and the transparent window are retained.

Manual copying
~~~~~~~~~~~~~~

You can copy any application subdirectory under .config into your own
configuration directory. Alacritty's main config imports the included
standalone theme.toml by a relative path. Keep those two files together.

Copy the entire Qtile folder, including my_widgets/ and wallpaper.jpg.
The wallpaper is resolved relative to config.py and is optional if removed.

Qt 6 applications use the bundled qt6ct Gotham palette. The restore helper
sets its absolute color-scheme path for the destination account. If copying
manually, select the installed ``qt6ct/colors/gotham.conf`` file in qt6ct so
``color_scheme_path`` points to that file. The template's relative path is a
portable placeholder for the restore helper.

The included environment.d entry, Qtile setup and zsh setup select qt6ct.
Start a new desktop session after restoring so applications inherit
``QT_QPA_PLATFORMTHEME=qt6ct``. The PCManFM-Qt launcher also selects it directly.
Its desktop entry is adjusted by the restore helper so it does not depend on
~/.local/bin being in the desktop session's PATH. When copying manually,
add ~/.local/bin to the session's PATH or adjust the desktop entry's Exec path.

Copy Firefox's or LibreWolf's overlay files into the corresponding actual
profile, not simply into a generic configuration directory. Each application's
files can also be restored individually; using the helper is the shortest way
to handle all destinations.

Ly login manager
----------------

The bundle includes an exact copy of /etc/ly/config.ini under etc/ly/config.ini.
The user-level install.py helper does not install system-wide files. After
installing Ly on the destination machine, back up its configuration and copy
this file manually from the bundle directory::

    sudo cp -a /etc/ly/config.ini /etc/ly/config.ini.template-backup-$(date +%Y%m%d-%H%M%S)
    sudo install -m 644 etc/ly/config.ini /etc/ly/config.ini

The backup command assumes Ly has already created /etc/ly/config.ini. This
copies only the configuration; it does not enable or restart the login manager.
The referenced setup.sh, startup.sh, custom-sessions and example.dur resources
are not included. Review those paths and the configured X11/session commands
for the destination machine. Optional brightness shortcuts use brightnessctl.

Plymouth boot splash
--------------------

The bundle includes the active ``arch-boot-dots`` theme, including its script,
logo, animation frames and GPL-2.0-only license. It also includes the current
``/etc/plymouth/plymouthd.conf``, which selects that theme. These system files
are not installed by the user-level ``install.py`` helper.

After installing Plymouth on the destination Arch system, restore the theme
from the bundle directory::

    sudo install -d /usr/share/plymouth/themes/arch-boot-dots
    sudo cp -a usr/share/plymouth/themes/arch-boot-dots/. /usr/share/plymouth/themes/arch-boot-dots/
    sudo install -d /etc/plymouth
    sudo install -m 644 etc/plymouth/plymouthd.conf /etc/plymouth/plymouthd.conf
    sudo plymouth-set-default-theme -R arch-boot-dots

The source system's mkinitcpio configuration places the ``plymouth`` hook
after ``udev`` and before ``autodetect``. Ensure the destination initramfs has
the Plymouth hook and the kernel command line contains ``splash``. The final
command selects the theme and rebuilds the initramfs; boot-loader and kernel
command-line configuration remain machine-specific and are not included.

Shell and Vim
-------------

The copied .zshrc keeps your aliases, prompt, history settings, file selector,
color display and screenshot functions. The theme-changer function and its
source block are absent. Its completion configuration uses the destination
home instead of the original account's absolute path. The existing ~/.local/bin
PATH entry is retained.

Use zsh for this shell configuration; restoring .zshrc does not change your
login shell. Optional commands used by functions or aliases include fzf,
scrot, dropbox-cli, rbenv and virtualenvwrapper. Those commands are needed only
for their associated features; guarded environment-manager setup stays guarded.
No history file is copied.

The .vim directory includes your custom TeX syntax and snapshots of VimTeX,
vim-airline, vim-airline-themes and UltiSnips. A local autoload/plug.vim is
included because the source setup used a system-wide vim-plug installation.
No plugin download is needed to load these bundled copies. Plugin licenses
are retained; Git metadata, bytecode, swap files and netrw browsing history
are omitted.

Use a Vim build with Python 3 support for UltiSnips. The configured clipboard
integration also requires a suitable Vim build/provider and clipboard tool.
VimTeX's compilation/viewing features need an appropriate TeX installation,
latexmk and Zathura. These external programs are not included in the bundle.

The bundled plugins are source snapshots rather than Git checkouts. To switch
to plugin-manager updates later, keep a backup of .vim/plugged, move that
snapshot directory aside, then use :PlugInstall with Git and network access.
Your plugin declarations remain in .vimrc. Review any local plugin edits
before replacing the snapshots.

What was preserved and omitted
------------------------------

Application layout preferences, Qtile keybindings and browser interface
settings are preserved, with the portability fixes described here and Gotham
colors applied through the same mappings as the theme switcher. Qt 6
applications share the bundled qt6ct palette. Sioyek's PDF recoloring remains
unchanged; Zathura retains its enabled recoloring with Gotham page colors.
Ly, Plymouth artwork and Vim's separate theme settings are outside the theme
switcher's application targets and retain their existing configuration.

Personal history, databases, recent-file lists, caches, bytecode, old backups,
unused palette helpers and downloaded theme collections are omitted.
Clementine's library paths, playback/window state, remote-control credentials
and cached song information are omitted. qutebrowser's global auto-config
preferences are retained, while site-specific permissions are reset.

Large font and bar settings match the source setup. You may want to adjust
sizes on displays with different resolution or scaling. App upgrades can
change option names or browser stylesheet behavior; this bundle records the
configuration checked against the installed versions, not a guarantee for
all future releases.

Checks performed during original preparation
--------------------------------------------

* Parsed the TOML, INI and Python files.
* Loaded Qtile's configuration with the included custom widget and wallpaper.
* Loaded qutebrowser's config.py and global autoconfig through its installed
  configuration API, including validation of option names and values.
* Checked the absence of theme-program references and old personal paths in
  the configuration, launcher and Firefox overlay files.
* Checked zsh syntax and startup from a temporary destination home with no
  theme function defined. Loaded the Vim settings and all four plugin paths
  with Python 3 support. The remote_startserver call was disabled only in the
  temporary test copy because this environment blocks local server listeners;
  the bundled .vimrc remains identical to the source.
* Tested restore dry runs, backups, repeated installation, symlink preservation,
  Firefox overlay copying, desktop-entry validation and launcher arguments in
  a temporary destination home. Active settings were not used as destinations.

GUI startup, rendering and hardware behavior still need checking on the new
machine. Rofi, Zathura, Sioyek, Clementine and Firefox were not started for
interactive visual verification during preparation.

Refresh notes (2026-11-14)
--------------------------

* Set application palettes to Gotham, including both Firefox and LibreWolf
  overlays, qutebrowser, Qtile, Alacritty, Rofi, Zathura, Sioyek and Clementine.
  The files remain standalone and do not require a theme-switching program.
* Added the Gotham qt6ct palette and portable installation path handling.
  PCManFM-Qt now uses that shared palette in place of its old stylesheet.
* Alacritty now uses 0.8 opacity. Qtile includes the current six workspaces,
  grow/normalize shortcuts, bar settings, and bundled JWST wallpaper in fill mode.
* Updated zsh's Git aliases, default editor and delayed screenshot function.
* Updated Vim's relative numbers, wrapping/concealment, split mappings, prose
  column exceptions, VimTeX options and airline theme. Refreshed the installed
  plugin snapshots; retained UltiSnips because .vimrc still declares it even
  though it is absent from the active plugin directory.
* Updated Clementine's appearance, search, library view, playlist, moodbar,
  sleep-inhibition and other portable preferences. Account credentials, library
  paths, history and playback/window session state remain excluded. The audio
  output retains automatic device selection for portability.
* Retained the PCManFM-Qt launcher name and destination-independent paths.
  qutebrowser uses a bundled local blank page with the Gotham palette.
* Retained the widget's existing missing-command/error handling. Corrected the
  source Qtile reader-workspace match to use regex alternation, and omitted its
  misspelled, unsupported center_algined widget option.
* Added the active ``arch-boot-dots`` Plymouth theme and daemon setting. The
  theme's source files and license are preserved exactly.

Refresh validation: parsed Python, TOML, INI and YAML files; checked shell and
Vim loading, loaded Qtile and qutebrowser configurations, and exercised restore
installation, repeat runs, backups and Firefox copying in a temporary home.
No active settings were used as installation destinations. Desktop rendering
and hardware behavior were not tested during this refresh.

License
-------

Original template scripts, documentation and configuration material are
released under the Zero-Clause BSD license; see ``LICENSE``. Bundled plugins,
the wallpaper and the Plymouth theme retain their upstream terms; see
``THIRD_PARTY_LICENSES.md``.

Useful upstream references
--------------------------

* `Alacritty configuration and relative imports <https://alacritty.org/config-alacritty.html>`_
* `qutebrowser config.py and autoconfig <https://qutebrowser.org/doc/help/configuring.html>`_
* `Sioyek interface-color settings <https://sioyek-documentation.readthedocs.io/en/latest/configuration.html>`_
* `Desktop entry command syntax <https://specifications.freedesktop.org/desktop-entry/latest/exec-variables.html>`_
