import te_api as api

appName: str = "turtleEdit"
api.addToAPI("info", appName)

appVersion: str = "2.0.0"
api.addToAPI("info", appVersion)

appNameVersion: str = f"{appName} {appVersion}"
api.addToAPI("info", appNameVersion)

ioErrors = {
    FileNotFoundError: "Failed to find \"{filename}\"!",
    PermissionError: "Not enough permissions to perform operations on \"{filename}\"!",
    IsADirectoryError: "\"{filename}\" is a directory, expected file!",
    OSError: "Something went wrong while operating on \"{filename}\"!",
}

