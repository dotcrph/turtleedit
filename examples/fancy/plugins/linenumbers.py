import wx
import wx.stc
import os
import os.path

def init(te) -> None:
    configDir: str = os.path.join(os.getcwd(), os.pardir, "config", 
                                  "linenumbers.json")
    te.cfg.loadConfig(configDir)

    te.widgets.insert.SetMarginType(0, wx.stc.STC_MARGIN_NUMBER)
    te.widgets.insert.SetMarginWidth(0, 50)

    te.widgets.insert.StyleSetBackground(
        wx.stc.STC_STYLE_LINENUMBER, 
        wx.Colour(te.cfg.get(str, "linenumbers", "bg"))
    )

    te.widgets.insert.StyleSetForeground(
        wx.stc.STC_STYLE_LINENUMBER, 
        wx.Colour(te.cfg.get(str, "linenumbers", "fg"))
    )

    te.widgets.insert.Refresh()
