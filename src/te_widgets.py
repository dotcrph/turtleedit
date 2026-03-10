import te_api as api
import te_cfg as cfg
import te_logging as log
import te_info as info

import wx
import wx.stc
import sys
import os
import os.path

app = wx.App(False)
api.addToAPI("widgets", "app", app)

frame = wx.Frame(None, title = info.appNameVersion.v)
api.addToAPI("widgets", "frame", frame)

panel = wx.Panel(frame)
api.addToAPI("widgets", "panel", panel)

grid = wx.GridBagSizer(vgap = 0, hgap = 0)
api.addToAPI("widgets", "grid", grid)

insert = wx.stc.StyledTextCtrl(panel, style = wx.TE_MULTILINE)
api.addToAPI("widgets", "insert", insert)

def initializeWidgets() -> None:
    initializeRoot()
    initializeIcon("turtleicon.ico")
    initializeInsert()
    initializeCaret()

    insert.StyleClearAll()
    insert.Refresh()

    frame.ShowFullScreen(cfg.get(bool, "root", "fullscreen", throw = True))
api.addToAPI("widgets", "initializeWidgets", initializeWidgets)

def initializeRoot() -> None:
    frame.SetSize(cfg.get(int, "root", "width", throw = True), 
                  cfg.get(int, "root", "height", throw = True))
api.addToAPI("widgets", "initializeRoot", initializeRoot)

def initializeIcon(iconPath: str) -> None:
    # This is needed because pyinstaller extracts all of the bundled assets 
    # in a temporary folder and you cannot retrieve them in a normal way
    iconPathFull: str = os.path.join(sys._MEIPASS, iconPath)                  \
                        if hasattr(sys, "_MEIPASS")                           \
                        else os.path.join(os.getcwd(), iconPath)

    if not os.path.isfile(iconPathFull):
        log.error(f"Failed to find icon at '{iconPathFull}'!")
        return

    icon = wx.Icon(iconPathFull, wx.BITMAP_TYPE_ANY)
    frame.SetIcon(icon)
api.addToAPI("widgets", "initializeIcon", initializeIcon)

def initializeInsert() -> None:
    fontFromCFG: str | None = cfg.get(str, "insert", "font")
    font: str = fontFromCFG if fontFromCFG else ""

    # Hide default margin
    insert.SetMarginWidth(1, 0)

    insert.StyleSetBackground(
        wx.stc.STC_STYLE_DEFAULT, 
        wx.Colour(cfg.get(str, "insert", "bg", throw = True))
    )

    insert.StyleSetForeground(
        wx.stc.STC_STYLE_DEFAULT, 
        wx.Colour(cfg.get(str, "insert", "fg", throw = True))
    )

    insert.StyleSetFont(
        wx.stc.STC_STYLE_DEFAULT, 
        wx.Font(
            pointSize = cfg.get(int, "insert", "fontSize", throw = True),
            family = wx.FONTFAMILY_TELETYPE,
            style = wx.FONTSTYLE_NORMAL,
            weight = wx.FONTWEIGHT_NORMAL,
            underline = False,
            faceName = font
        )
    )
api.addToAPI("widgets", "initializeInsert", initializeInsert)

def initializeCaret() -> None:
    insert.SetCaretForeground(
        wx.Colour(cfg.get(str, "caret", "color", throw = True))
    )

    insert.SetCaretWidth(
        cfg.get(int, "caret", "width", throw = True)
    )
api.addToAPI("widgets", "initializeCaret", initializeCaret)

def setTitle(title: str = "") -> None:
    if (not title):
        frame.SetTitle(info.appName.v)
    else:
        frame.SetTitle(f"{info.appName.v} - {title}")
api.addToAPI("widgets", "setTitle", setTitle)

def placeWidgets() -> None:
    grid.Add(insert, (0, 0), span = (1, 1), flag = wx.EXPAND | wx.ALL)
    grid.AddGrowableCol(0)
    grid.AddGrowableRow(0)
    panel.SetSizerAndFit(grid)
    panel.Layout()

