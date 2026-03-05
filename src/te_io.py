import te_api as api
import te_widgets as widgets
import te_info as info
import te_logging as log

import wx
import wx.stc

openFileDir: str = ""
api.addToAPI("io", openFileDir)

lastOpenDir: str = ""
api.addToAPI("io", lastOpenDir)

lastSaveAsDir: str = ""
api.addToAPI("io", lastSaveAsDir)

fileWildcard: str = "All files|*.*"
api.addToAPI("io", fileWildcard)

def openFile(_ = None) -> bool:
    global lastOpenDir, openFileDir

    if not confirmDirty(widgets.insert):
        return False

    fileDialog = wx.FileDialog(
        widgets.frame,
        message = "Open file",
        defaultDir = lastOpenDir,
        defaultFile = "",
        wildcard = fileWildcard,
        style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_SHOW_HIDDEN 
    )

    if fileDialog.ShowModal() != wx.ID_OK:
        return False

    openDir: str = fileDialog.GetPath()
    log.info(f"Opening file '{openDir}'")

    try:
        with open(openDir, "r+", encoding="utf-8") as file:
            fileContent: str = file.read()
    except Exception as e:
        if type(e) not in info.ioErrors.keys():
            raise

        log.error(info.ioErrors[type(e)].format(openDir) 
                 + f"({e})")
        return False

    widgets.insert.SetValue(fileContent)
    widgets.insert.SetSavePoint()

    widgets.setTitle(openDir)
    lastOpenDir = openDir
    openFileDir = openDir

    fileDialog.Destroy()
    return True
api.addToAPI("io", openFile)

def saveAsFile(_ = None) -> bool:
    global lastSaveAsDir, openFileDir

    fileDialog = wx.FileDialog(
        widgets.frame,
        message = "Save file as",
        defaultDir = lastSaveAsDir,
        defaultFile = "",
        wildcard = fileWildcard,
        style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT | wx.FD_SHOW_HIDDEN
    )

    if fileDialog.ShowModal() != wx.ID_OK:
        return False

    saveAsDir: str = fileDialog.GetPath()
    log.info(f"Saving file '{openFileDir}' as '{saveAsDir}'")

    try:
        widgets.insert.SaveFile(saveAsDir)
    except Exception as e:
        if type(e) not in info.ioErrors.keys():
            raise

        log.error(info.ioErrors[type(e)].format(openDir) 
                 + f"({e})")
        return False

    widgets.insert.SetSavePoint()

    widgets.setTitle(saveAsDir)
    lastSaveAsDir = saveAsDir
    openFileDir = saveAsDir

    fileDialog.Destroy()

    return True
api.addToAPI("io", saveAsFile)

def saveFile(_ = None) -> bool:
    global openFileDir

    if not openFileDir:
        return saveAsFile()

    log.info(f"Saving file '{openFileDir}'")

    try:
        widgets.insert.SaveFile(openFileDir)
    except Exception as e:
        if type(e) not in info.ioErrors.keys():
            raise

        log.error(info.ioErrors[type(e)].format(openDir) 
                 + f"({e})")
        return False

    widgets.insert.SetSavePoint()

    return True
api.addToAPI("io", saveFile)

def newFile(_ = None) -> bool:
    global openFileDir

    if not confirmDirty(widgets.insert):
        return False

    widgets.insert.ClearAll()
    openFileDir = ""

    return True
api.addToAPI("io", newFile)

def quitWithSave(_ = None) -> bool:
    if not confirmDirty(widgets.insert):
        return False

    widgets.frame.Close()
    return True
api.addToAPI("io", quitWithSave)

def confirmDirty(widget: wx.stc.StyledTextCtrl) -> bool:
    if not widget.GetModify():
        return True

    confirmationDialog = wx.MessageDialog(
        widgets.panel, 
        "Your file has unsaved changes. Do you want to continue?", 
        "Confirm", 
        wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
    )

    res: int = confirmationDialog.ShowModal()
    confirmationDialog.Destroy()

    return False if res != wx.ID_YES else True
api.addToAPI("io", confirmDirty)

