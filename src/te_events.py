import te_api as api

from wx.lib.newevent import NewEvent

eOpenFileDirChanged, openFileDirChanged = NewEvent()
api.addToAPI("events", "openFileDirChanged", openFileDirChanged)
