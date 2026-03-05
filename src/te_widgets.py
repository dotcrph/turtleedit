import te_api as api
import te_cfg as cfg
import te_logging as log
import te_info as info

import wx
import wx.stc
from os.path import isfile

app = wx.App(False)
api.addToAPI("widgets", app)

frame = wx.Frame(None, title = info.appNameVersion.v)
api.addToAPI("widgets", frame)

panel = wx.Panel(frame)
api.addToAPI("widgets", panel)

grid = wx.GridBagSizer(vgap = 0, hgap = 0)
api.addToAPI("widgets", grid)

insert = wx.stc.StyledTextCtrl(panel, style = wx.TE_MULTILINE)
api.addToAPI("widgets", insert)

def initializeWidgets() -> None:
    initializeRoot()
    initializeIcon("turtleIcon.ico")
    initializeInsert()
    initializeCaret()

    frame.ShowFullScreen(cfg.get(bool, "root", "fullscreen", throw = True))
api.addToAPI("widgets", initializeWidgets)

def initializeRoot() -> None:
    frame.SetSize(cfg.get(int, "root", "width", throw = True), 
                  cfg.get(int, "root", "height", throw = True))
api.addToAPI("widgets", initializeRoot)

def initializeIcon(iconPath: str) -> None:
    if not isfile(iconPath):
        log.error(f"Failed to find icon at '{iconPath}'!")
        return

    icon = wx.Icon(iconPath, wx.BITMAP_TYPE_ANY)
    frame.SetIcon(icon)
api.addToAPI("widgets", initializeIcon)

def initializeInsert() -> None:
    insert.StyleClearAll()

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
        )
    )

    insert.Refresh()
api.addToAPI("widgets", initializeInsert)

def initializeCaret() -> None:
    insert.SetCaretForeground(
        wx.Colour(cfg.get(str, "caret", "color", throw = True))
    )

    insert.SetCaretWidth(
        cfg.get(int, "caret", "width", throw = True)
    )
api.addToAPI("widgets", initializeCaret)

def setTitle(title: str = "") -> None:
    if (not title):
        frame.SetTitle(info.appName.v)
    else:
        frame.SetTitle(f"{info.appName.v} - {title}")
api.addToAPI("widgets", setTitle)

def placeWidgets() -> None:
    grid.Add(insert, (0, 0), span = (1, 1), flag = wx.EXPAND | wx.ALL)
    grid.AddGrowableCol(0)
    grid.AddGrowableRow(0)
    panel.SetSizerAndFit(grid)
    panel.Layout()

