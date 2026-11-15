user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);

// Prefer native dark website themes; websites retain control of their palette.
user_pref("browser.display.document_color_use", 1);
user_pref("layout.css.prefers-color-scheme.content-override", 0);

// Current portable browser layout; native toolbar buttons and spacers only.
user_pref("sidebar.visibility", "hide-on-close");
user_pref("sidebar.main.tools", "history,passwords");
user_pref("browser.uiCustomization.state", "{\"placements\":{\"widget-overflow-fixed-list\":[],\"unified-extensions-area\":[],\"nav-bar\":[\"back-button\",\"forward-button\",\"stop-reload-button\",\"customizableui-special-spring1\",\"vertical-spacer\",\"urlbar-container\",\"customizableui-special-spring2\",\"downloads-button\",\"fxa-toolbar-menu-button\",\"reset-pbm-toolbar-button\",\"fire-button\",\"unified-extensions-button\"],\"toolbar-menubar\":[\"menubar-items\"],\"TabsToolbar\":[\"tabbrowser-tabs\",\"new-tab-button\",\"customizableui-special-spring3\",\"alltabs-button\",\"smartwindow-group-tabs-button\",\"ai-window-toggle\"],\"vertical-tabs\":[],\"PersonalToolbar\":[\"personal-bookmarks\"]},\"seen\":[\"reset-pbm-toolbar-button\",\"developer-button\",\"screenshot-button\"],\"dirtyAreaCache\":[\"nav-bar\",\"TabsToolbar\",\"vertical-tabs\",\"toolbar-menubar\",\"PersonalToolbar\"],\"currentVersion\":28,\"newElementCount\":4}");
