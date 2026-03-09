import wx
import wx.stc

te = None

status: wx.StatusBar = wx.StatusBar()
caretLastPos: int = 0

def init(teRef) -> None:
    global te
    te = teRef

    setup()

def setup() -> None:
    FIELDS: int = 3

    status.Create(te.widgets.frame, style = 0)
    status.SetFieldsCount(FIELDS)
    status.SetStatusWidths([120, -1, 100])

    te.widgets.frame.SetStatusBar(status)

    status.SetStatusText(te.info.appNameVersion.v, 0)

    status.SetStatusText(te.io.openFileDir.v, 1)
    te.widgets.frame.Bind(
        te.events.openFileDirChanged,
        onOpenFileDirChanged
    )

    status.SetStatusText("0, 0", 2)
    te.widgets.frame.Bind(wx.stc.EVT_STC_UPDATEUI, onInsertUpdated)

def onOpenFileDirChanged(event: wx.Event) -> None:
    status.SetStatusText(event.newDir, 1)
    event.Skip()

def onInsertUpdated(event: wx.Event) -> None:
    global caretLastPos

    caretNewPos: int = te.widgets.insert.GetCurrentPos()

    if caretNewPos == caretLastPos:
        event.Skip()
        return

    caretLastPos = caretNewPos

    line: int = te.widgets.insert.LineFromPosition(caretNewPos)
    col: int = te.widgets.insert.GetColumn(caretNewPos)

    status.SetStatusText(f"{line}, {col}", 2)
    event.Skip()
