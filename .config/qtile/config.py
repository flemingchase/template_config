from pathlib import Path
from libqtile import bar, layout, qtile, widget, extension
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import backlight
from my_widgets.caps_num_lock_indicator import MyCapsNumLockIndicator
import re
import os
import shutil

# Shared Qt palette for applications launched by this desktop session.
if (shutil.which("qt6ct") and
        (Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config") /
         "qt6ct/qt6ct.conf").is_file()):
    os.environ["QT_QPA_PLATFORMTHEME"] = "qt6ct"

# Gotham color palette.
colors = {
    "primary": {
        "background": "#0a0f14",
        "foreground": "#98d1ce"
    },
    "normal": {
        "black": "#0a0f14",
        "red": "#c33027",
        "green": "#26a98b",
        "yellow": "#edb54b",
        "blue": "#195465",
        "magenta": "#4e5165",
        "cyan": "#33859d",
        "white": "#98d1ce"
    },
    "bright": {
        "black": "#10151b",
        "red": "#d26939",
        "green": "#081f2d",
        "yellow": "#245361",
        "blue": "#093748",
        "magenta": "#888ba5",
        "cyan": "#599caa",
        "white": "#d3ebe9"
    }
}

mod = "mod4"
terminal = guess_terminal()

def my_func(text):
    for string in [
            "qutebrowser", "zathura", "Zathura",
            "Alacritty", "discord", "Discord",
            "sioyek", "Sioyek", "Firefox", "firefox",
            ]:
        if string in text:
            text = string
    if "pdf" in text:
        last_slash_index = text.rfind('/')
        text = text[last_slash_index + 1: -4]
    return text.lower()

keys = [
    Key(
        [mod, "control"],
        "l",
        lazy.layout.grow_right(),
        desc="Grow window to the right"
        ),

    Key(
        [mod, "control"],
        "h", lazy.layout.grow_left(),
        desc="Grow window to the left"
        ),

    Key(
        [mod, "control"],
        "j",
        lazy.layout.grow_down(),
        desc="Grow window down"
        ),

    Key(
        [mod, "control"],
        "k",
        lazy.layout.grow_up(),
        desc="Grow window up"
        ),

    Key(
        [mod],
        "n",
        lazy.layout.normalize(),
        desc="Reset all window sizes"
        ),

    Key(
        [mod],
        "h",
        lazy.layout.left(),
        desc = "Move focus to left",
        ),

    Key(
        [mod],
        "l",
        lazy.layout.right(),
        desc = "Move focus to right",
        ),

    Key(
        [mod],
        "j",
        lazy.layout.down(),
        desc = "Move focus down",
        ),

    Key(
        [mod],
        "k",
        lazy.layout.up(),
        desc = "Move focus up",
        ),

    Key(
        [mod, "shift"],
        "h",
        lazy.layout.shuffle_left(),
        desc = "Move window to the left",
        ),

    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc = "Move window to the right",
        ),

    Key(
        [mod, "shift"],
        "j",
        lazy.layout.shuffle_down(),
        desc = "Move window down",
        ),

    Key(
        [mod, "shift"],
        "k",
        lazy.layout.shuffle_up(),
        desc = "Move window up",
        ),

    Key(
        [mod, "shift"],
        "n",
        lazy.layout.normalize(),
        desc = "Normalize moved windows",
        ),

    Key(
        [mod, "control"],
        "h",
        lazy.layout.grow_left(),
        desc = "Grow window to the left",
        ),

    Key(
        [mod, "control"],
        "l",
        lazy.layout.grow_right(),
        desc = "Grow window to the right",
        ),

    Key(
        [mod, "control"],
        "j",
        lazy.layout.grow_down(),
        desc ="Grow window down",
        ),

    Key(
        [mod, "control"],
        "k",
        lazy.layout.grow_up(),
        desc = "Grow window up",
        ),

    Key(
        [mod],
        "tab",
        lazy.screen.toggle_group(),
        desc = "Go to last group",
        ),

    #Spawn common programs
    Key(
        [mod, "shift"],
        "BackSpace",
        lazy.spawn("xsel -bc"),
        desc = "Clear clipboard",
        ),

    Key(
        [mod],
        "Return",
        lazy.spawn(terminal),
        desc = "Launch terminal",
        ),

    Key(
        [mod],
        "a",
        lazy.spawn("qutebrowser"),
        desc = "Spawn QuteBrowser",
        ),

    Key(
        [mod],
        "t",
        lazy.spawn([str(Path.home() / ".local/bin/pcmanfm-themed")]),
        desc = "Spawn file manager",
        ),

    Key(
        ['mod4'],
        'space',
        lazy.spawn(
            "rofi -show drun"
        ),
        desc = "Spawn Rofi desktop run"
        ),

    #System Commands
    Key(
        [mod],
        "w",
        lazy.window.kill(),
        desc = "Kill focused window",
        ),

    Key(
        [mod, "control"],
        "r",
        lazy.reload_config(),
        desc = "Reload the config",
        ),

    Key(
        [mod, "control"],
        "q",
        lazy.shutdown(),
        desc = "Shutdown Qtile",
        ),

    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc = "Toggle fullscreen on the focused window",
    ),
]

groups = [
    Group(
        "1",
        label = "term",
        matches = [],
        ),

    Group(
        "2",
        label = "web",
        matches = [Match(wm_class=re.compile(r"^(qutebrowser)$"))],
        ),

    Group(
        "3",
        label = "read",
        matches = [Match(wm_class=re.compile(r"^(Zathura|sioyek)$"))],
        ),

    Group(
        "4",
        label = "music",
        matches = [Match(wm_class=re.compile(r"^(clementine)$"))],
        ),

    Group(
        "5",
        label = "files",
        matches = [Match(wm_class=re.compile(r"^(pcmanfm-qt)$"))],
        ),

    Group(
        "6",
        label = "misc",
        matches = [],
        ),
]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc = f"Switch to group {i.name}",
            ),

            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc = f"Switch to & move focused window to group {i.name}",
            ),
        ]
    )

layouts = [
    layout.Bsp(
        border_focus = colors["primary"]["foreground"],
        border_normal = colors["primary"]["background"],
        border_width = 2,
        grow_amount = 2,
        margin_on_single = [0, 0, 0, 0,],
        margin = [0, 0, 0, 0,],
        ratio = 1.7,
        ),
]

widget_defaults = dict(
    font = "Fira Mono",
    fontsize = 30,
    padding = 6,
    background = colors["primary"]["background"],
    foreground = colors["primary"]["foreground"]
)

extension_defaults = widget_defaults.copy()
wallpaper_path = Path(__file__).resolve().parent / "wallpaper.jpg"
logo = str(wallpaper_path) if wallpaper_path.is_file() else None

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    disable_drag = True,
                    active = colors["primary"]["foreground"],
                    hide_unused = False,
                    use_mouse_wheel = False,
                    highlight_method = "line",
                    highlight_color = [colors["primary"]["background"], colors["primary"]["background"]],
                    inactive = colors["primary"]["foreground"],
                    this_current_screen_border = colors["primary"]["foreground"],
                    toggle = False,
                    ),

                widget.Sep(
                    line_width = 1,
                    size_percent = 90,
                    ),

                widget.WindowName(
                    format = '{name}',
                    fmt = '<b>{}</b>',
                    parse_text = my_func,
                    ),

                widget.Spacer(),

                MyCapsNumLockIndicator(
                    update_interval =0.5,
                    ),

                widget.Sep(
                    line_width = 1,
                    size_percent = 90
                    ),

                widget.Clock(
                    format ="<b>%b %d %H:%M</b>"
                    ),
            ],
            35,
            margin = [0,0,0,0,],
            opacity = 1.0,
            border_width = 5,
            border_color = colors["primary"]["background"],
        ),
        background = colors["primary"]["background"],
        wallpaper = logo,
        wallpaper_mode = "fill",
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start = lazy.window.get_position()
        ),

    Drag(
        [mod],
        "Button3",
        lazy.window.set_size_floating(),
        start = lazy.window.get_size()
        ),

    Click(
        [mod],
        "Button2",
        lazy.window.bring_to_front()
        ),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False

floating_layout = layout.Floating(
    float_rules = [
        *layout.Floating.default_float_rules,

        Match(
            wm_class = "confirmreset"
            ),

        Match(
            wm_class = "makebranch"
            ),

        Match(
            wm_class = "maketag"
            ),

        Match(
            wm_class = "ssh-askpass"
            ),

        Match(
            title = "branchdialog"
            ),

        Match(
            title = "pinentry"
            ),
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24
idle_inhibitors = []
wmname = "LG3D"
