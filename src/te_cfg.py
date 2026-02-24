import te_io as io
import te_logging as log

import json
import os.path
from typing import Any

configDir = "data"
configFilename = "config.json"
configPath = os.path.join(configDir, configFilename)

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

    if os.path.exists(configPath):
        readConfig()
    else:
        createConfigFile()

def readConfig() -> None:
    global userConfig

    try:
        with open(configPath, "r", encoding="utf-8") as configFile:
            userConfig = json.load(configFile)
    except json.JSONDecodeError as e:
        log.error(f"Failed to encode JSON config file {configPath}! ({e})")
    except Exception as e:
        if isinstance(e, tuple(io.ioErrors.keys())):
            log.error(io.ioErrors[type(e)].format(configDir) 
                     + f"({e})")
            return
        else:
            raise

def createConfigFile() -> None:
    os.makedirs(configDir, exist_ok=True)

    with open(configPath, "w", encoding="utf-8") as configFile:
        json.dump(defaultConfig, configFile, indent=4)

    log.info(f"Created {configPath}")

def get(expectedType: type, *keys: str) -> Any:
    keyPath = ".".join(keys)

    # Check user config
    value = userConfig

    for key in keys:
        if key not in value:
            break

        if (key != keys[-1] and not isinstance(value, dict)):
            log.error(f"Value {key} in {keyPath} in user config is not a dictionary!")
            return None

        value = value[key]
    else:
        if (isinstance(value, expectedType)):
            return value

    # Check default config
    value = defaultConfig

    for key in keys:
        if key not in value:
            break

        if (key != keys[-1] and not isinstance(value, dict)):
            log.error(f"Value {key} in {keyPath} in default config is not a dictionary!")
            return None

        value = value[key]
    else:
        if (not isinstance(value, expectedType)):
            log.error(f"Value {keyPath} in user config file is of type {type(value)}, expected {expectedType}")
            return None

        return value

    log.error(f"Could not find {key} in {keyPath} in config!")
    return None


if __name__ == "__main__":
    setupConfig()
    print(userConfig)
