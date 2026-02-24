import te_io as io
import te_logging as log

import json
from os.path import exists
from typing import Any

configDir = "data/config.json"
userConfig: dict[str, Any] = dict()
defaultConfig = {
    "root": {
        "width": 1600,
        "height": 900,
        "fullscreen": False
    },

    "insert": {
        "bgColor": "#000000",
        "fgColor": "#ffffff",
        "relief": "flat",
        "font": "Consolas",
        "fontSize": 16
    },

    "caret": {
        "color": "#85CB33",
        "width": 3
    },

    "lineNumbers": {
        "position": "left",
        "bgColor": "#000000",
        "fgColor": "#3d3d3d",
        "relief": "flat"
    },

    "footer": {
        "enabled": True,
        "bgColor": "#85CB33",
        "fgColor": "#000000",
        "relief": "flat",
        "font": "Consolas",
        "fontSize": 16,
        "items": ["position", "time", "filename", "log", "appinfo"],
        "separator": " | "
    },

    "footerItems" : {
        "time": {
            "format": "%A %x %X"
        }
    }
}

appVersion = "turtleEdit 2.0.0"

def setupConfig():
    global config

    if exists(configDir):
        readConfig()
    else:
        createConfigFile()

def readConfig() -> None:
    global userConfig

    try:
        with open(configDir, "r", encoding="utf-8") as configFile:
            userConfig = json.load(configFile)
    except json.JSONDecodeError as e:
        log.error(f"Failed to encode JSON config file {configDir}! ({e})")
    except Exception as e:
        if isinstance(e, tuple(io.ioErrors.keys())):
            log.error(io.ioErrors[type(e)].format(configDir) 
                     + f"({e})")
            return
        else:
            raise

def createConfigFile() -> None:
    with open(configDir, "w", encoding="utf-8") as configFile:
        json.dump(defaultConfig, configFile, indent=4)

def get(expectedType: type, *keys: str) -> Any | None:
    keyPath = ".".join(keys)

    key = ""
    value = None

    for key in keys:
        if key in userConfig:
            value = userConfig[key]
            continue

        if key in defaultConfig:
            value = defaultConfig[key]
            continue
        
        log.error(f"Could not find config key {key} in {keyPath}")
        return None

    if (not isinstance(value, expectedType)):
        log.error(f"Value {keyPath} is of type {type(value)}, expected {expectedType}")
        return None

    return value

if __name__ == "__main__":
    setupConfig()
    print(userConfig)
