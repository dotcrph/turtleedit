import te_api as api

appName: api.Mutable[str] = api.Mutable("turtleEdit")
api.addToAPI("info", appName)

appVersion: api.Mutable[str] = api.Mutable("2.0.0")
api.addToAPI("info", appVersion)

appNameVersion: api.Mutable[str] = api.Mutable(f"{appName.v} {appVersion.v}")
api.addToAPI("info", appNameVersion)

ioErrors = {
    FileNotFoundError: "Failed to find \"{filename}\"!",
    PermissionError: "Not enough permissions to perform operations on \"{filename}\"!",
    IsADirectoryError: "\"{filename}\" is a directory, expected file!",
    OSError: "Something went wrong while operating on \"{filename}\"!",
}
api.addToAPI("info", ioErrors)

