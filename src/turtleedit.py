import te_cfg as cfg
import te_widgets as widgets
import te_plugins as plugins

from os.path import join

def main() -> None:
    cfg.loadConfig(join("config", "main.json"))

    widgets.placeWidgets()
    widgets.initializeWidgets()

    plugins.loadPlugins()

    widgets.frame.Show()
    widgets.app.MainLoop()


if __name__ == '__main__':
    main()
