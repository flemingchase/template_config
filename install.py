#!/usr/bin/env python3
"""Restore application templates, with backups and optional browser overlays."""
import argparse
from datetime import datetime
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
import uuid


# Component paths are relative to this repository. System-wide Ly and Plymouth
# assets are deliberately absent: the user-level restore never installs them.
COMPONENT_PATHS = {
    'zsh': ('.zshrc',),
    'vim': ('.vimrc', '.vim'),
    'qtile': ('.config/qtile',),
    'alacritty': ('.config/alacritty',),
    'qutebrowser': ('.config/qutebrowser',),
    'rofi': ('.config/rofi',),
    'zathura': ('.config/zathura',),
    'clementine': ('.config/Clementine',),
    'sioyek': ('.config/sioyek',),
    'pcmanfm-qt': ('.config/pcmanfm-qt', '.local/bin/pcmanfm-themed',
                   '.local/share/applications/pcmanfm-qt.desktop'),
    'qt6ct': ('.config/qt6ct', '.config/environment.d/60-qt6ct.conf'),
    'firefox': ('firefox-profile',),
    'librewolf': ('librewolf-profile',),
}
COMPONENTS = frozenset(COMPONENT_PATHS)


def selected_components(components):
    """Validate a selection; None preserves the traditional full restore."""
    if components is None:
        return None
    if isinstance(components, str):
        components = components.split(',')
    selected = frozenset(components)
    unknown = selected - COMPONENTS
    if unknown:
        raise ValueError('Unknown template components: ' + ', '.join(sorted(unknown)))
    return selected


def component_selected(relative, components):
    if components is None:
        return True
    return any(relative.is_relative_to(Path(prefix))
               for component in components for prefix in COMPONENT_PATHS[component])


def desktop_argument(value):
    value = str(value).replace('%', '%%')
    for char in ('\\', '"', '`', '$'):
        value = value.replace(char, '\\' + char)
    # Desktop entry string escaping precedes argument unquoting.
    return '"' + value.replace('\\', '\\\\') + '"'


def qsettings_string(value):
    """Quote a path for Qt's INI reader without expanding special characters."""
    return ('"' + str(value).replace('\\', '\\\\').replace('"', '\\"')
            .replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t') + '"')


def plan(bundle, home, config, data, firefox_profile=None, zshdir=None,
         librewolf_profile=None, components=None):
    components = selected_components(components)
    writes = []
    for relative, destination in (('.config', config), ('.local/bin', home / '.local/bin'),
                                  ('.local/share', data), ('.vim', home / '.vim')):
        source = bundle / relative
        for filename in sorted(source.rglob('*')):
            if not component_selected(filename.relative_to(bundle), components):
                continue
            if relative == '.vim' and filename.relative_to(source).parts[0] == 'plugged':
                continue
            if not filename.is_file() or any(part in ('__pycache__', '.git') for part in filename.parts) or filename.suffix in ('.pyc', '.pyo'):
                continue
            content = filename.read_bytes()
            target = destination / filename.relative_to(source)
            if filename.name == 'pcmanfm-qt.desktop':
                command = desktop_argument(home / '.local/bin/pcmanfm-themed')
                content = content.replace(b'Exec=pcmanfm-themed %U', f'Exec={command} %U'.encode())
            if relative == '.config' and filename.relative_to(source) == Path('qt6ct/qt6ct.conf'):
                palette = qsettings_string((config / 'qt6ct/colors/gotham.conf').absolute())
                content = content.replace(b'color_scheme_path="colors/gotham.conf"',
                                          f'color_scheme_path={palette}'.encode())
            writes.append((target, content, stat.S_IMODE(filename.stat().st_mode)))
    for name, destination in (('.vimrc', home / '.vimrc'), ('.zshrc', (zshdir or home) / '.zshrc')):
        filename = bundle / name
        if component_selected(Path(name), components) and filename.is_file():
            writes.append((destination, filename.read_bytes(), stat.S_IMODE(filename.stat().st_mode)))
    for application, profile, overlay_name in (
            ('Firefox', firefox_profile, 'firefox-profile'),
            ('LibreWolf', librewolf_profile, 'librewolf-profile')):
        if profile is None or not component_selected(Path(overlay_name), components):
            continue
        if not profile.is_dir():
            raise ValueError(
                f'{application} profile must already exist. Start {application} once, '
                'then choose its profile directory.')
        overlay = bundle / overlay_name
        for filename in sorted(overlay.rglob('*')):
            if filename.is_file():
                writes.append((profile / filename.relative_to(overlay),
                               filename.read_bytes(), 0o600))
    resolved = [filename.resolve() for filename, _, _ in writes]
    if len(resolved) != len(set(resolved)):
        raise ValueError('Two template destinations resolve to the same file.')
    if any(filename.is_relative_to(bundle.resolve()) for filename in resolved):
        raise ValueError('Choose a destination outside the template bundle.')
    return writes


def save(filename, content, mode):
    filename = filename.resolve()
    if filename.exists() and filename.read_bytes() == content:
        return False
    filename.parent.mkdir(parents=True, exist_ok=True)
    if filename.exists():
        suffix = datetime.now().strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:8]
        backup = filename.with_name(filename.name + '.template-backup-' + suffix)
        shutil.copy2(filename, backup)
        mode = stat.S_IMODE(filename.stat().st_mode)
        print(f'Backup: {backup}')
    if filename.name == 'pcmanfm-themed':
        mode |= 0o100  # An existing wrapper must remain executable after replacement.
    fd, temporary = tempfile.mkstemp(prefix='.template-', dir=filename.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
            os.fchmod(stream.fileno(), mode)
        os.replace(temporary, filename)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true', help='Show destination paths without writing files')
    parser.add_argument('--home', type=Path, help='Alternate destination home; uses its .config and .local/share')
    parser.add_argument('--firefox-profile', type=Path, help='Existing destination Firefox profile directory')
    parser.add_argument('--librewolf-profile', type=Path, help='Existing destination LibreWolf profile directory')
    parser.add_argument('--components', action='append', metavar='NAME[,NAME...]',
                        help='Restore only these components; repeat to add more (default: all)')
    parser.add_argument('--list-components', action='store_true', help='List available user-level components and exit')
    args = parser.parse_args(argv)
    try:
        components = None
        if args.components is not None:
            names = [name.strip() for group in args.components for name in group.split(',')]
            if not all(names):
                raise ValueError('--components requires nonempty component names')
            components = selected_components(names)
        if args.list_components:
            print('\n'.join(sorted(COMPONENTS)))
            return 0
        home = args.home.expanduser().absolute() if args.home else Path.home()
        config = home / '.config' if args.home else Path(os.environ.get('XDG_CONFIG_HOME') or home / '.config').expanduser()
        data = home / '.local/share' if args.home else Path(os.environ.get('XDG_DATA_HOME') or home / '.local/share').expanduser()
        firefox_profile = args.firefox_profile.expanduser().absolute() if args.firefox_profile else None
        librewolf_profile = args.librewolf_profile.expanduser().absolute() if args.librewolf_profile else None
        bundle = Path(__file__).resolve().parent
        zshdir = home if args.home else Path(os.environ.get('ZDOTDIR') or home).expanduser()
        writes = plan(bundle, home, config, data, firefox_profile=firefox_profile,
                      librewolf_profile=librewolf_profile, zshdir=zshdir, components=components)
        changed = 0
        for filename, content, mode in writes:
            if args.dry_run:
                print(f'Would copy: {filename}')
            elif save(filename, content, mode):
                print(f'Installed: {filename}')
                changed += 1
        if not args.dry_run:
            print(f'Updated {changed} files. No applications were restarted.')
            if components is None or 'vim' in components:
                print('Vim plugins: open Vim as the destination user and run :PlugInstall (requires Git and internet access).')
        if firefox_profile is None and (components is None or 'firefox' in components):
            print('Firefox overlay was not selected; rerun with --firefox-profile PATH after Firefox creates a profile.')
        if librewolf_profile is None and (components is None or 'librewolf' in components):
            print('LibreWolf overlay was not selected; rerun with --librewolf-profile PATH after LibreWolf creates a profile.')
        return 0
    except (OSError, ValueError) as error:
        print(f'Template restore failed: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
