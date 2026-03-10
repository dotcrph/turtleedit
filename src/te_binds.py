import te_widgets as widgets
import te_io as io
import te_api as api

import wx

binds: list[wx.AcceleratorEntry] = []
api.addToAPI("binds", "binds", binds)

def initializeEventHandlers() -> None:
    # On frame resize
    widgets.frame.Bind(wx.EVT_SIZE, onFrameResize)

def initializeBinds() -> None:
    # Quit
    binds.append(wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('Q'), wx.ID_EXIT))
    widgets.frame.Bind(wx.EVT_MENU, onQuit, id = wx.ID_EXIT)

    # New
    binds.append(wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('N'), wx.ID_NEW))
    widgets.frame.Bind(wx.EVT_MENU, io.newFile, id = wx.ID_NEW)

    # Open
    binds.append(wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('O'), wx.ID_OPEN))
    widgets.frame.Bind(wx.EVT_MENU, io.openFile, id = wx.ID_OPEN)

    # Save
    binds.append(wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('S'), wx.ID_SAVE))
    widgets.frame.Bind(wx.EVT_MENU, io.saveFile, id = wx.ID_SAVE)

    # Save as
    binds.append(wx.AcceleratorEntry(wx.ACCEL_CTRL | wx.ACCEL_SHIFT, 
                                     ord('S'), wx.ID_SAVEAS))
    widgets.frame.Bind(wx.EVT_MENU, io.saveAsFile, id = wx.ID_SAVEAS)

    reloadBinds()

def reloadBinds() -> None:
    acceleratorTable = wx.AcceleratorTable(binds)
    widgets.frame.SetAcceleratorTable(acceleratorTable)
api.addToAPI("binds", "reloadBinds", reloadBinds)

def onQuit(_: wx.CommandEvent) -> None:
    if io.quitWithSave():
        widgets.insert.Destroy()

def onFrameResize(event: wx.Event) -> None:
    # This is needed because STC draws horizontal 
    # scrollbar based on a cached width

    # BUG: The horizontal scrollbar disappears after resizing, 
    #      even if the text is longer than the STC width
    widgets.insert.SetScrollWidth(1)
    event.Skip()
