import te_logging as log
import te_info as info
import te_api as api

import json
import os.path
from collections import deque
from typing import Literal, overload

jsonT = dict[str, "jsonT"] | list["jsonT"] | str | int | float | bool | None

config: dict[str, jsonT] = {
    "root": {
        "width": 800,
        "height": 600,
        "fullscreen": False
    },

    "insert": {
        "bg": "#000000",
        "fg": "#ffffff",
        "fontSize": 22
    },

    "caret": {
        "color": "#85CB33",
        "width": 3
    }
}

def loadConfig(configPath: str) -> None:
    """
    Tries to open a JSON file located in configDir and if the file exists
    adds/replaces entries in config dictionary
    """
    global config

    if not os.path.exists(configPath):
        log.warn(f"Failed to find config in '{configPath}', using default config")
        return

    try:
        with open(configPath, "r", encoding="utf-8") as configFile:
            userConfig: dict[str, jsonT] = json.load(configFile)

        objectsToRead: deque[
            tuple[
                list[str],        # Parent JSON object (aka dict) key path
                dict[str, jsonT], # Correlated object from JSON file
                dict[str, jsonT]  # Correlated object from config dict
            ]
        ] = deque()

        # Pushing the root JSON object to stack. Path list is empty 
        # because the root object does not have a parent object
        objectsToRead.append(([], userConfig, config))

        # Stack-based tree traversal algorithm 
        while objectsToRead:
            obj = objectsToRead.pop()

            parentObjKeyPath: list[str]       = obj[0]
            objFromJsonFile: dict[str, jsonT] = obj[1]
            objFromConfig: dict[str, jsonT]   = obj[2]

            for key in objFromJsonFile:
                thisKeyPath: list[str] = parentObjKeyPath + [key]
                thisKeyPathFormatted = ".".join(thisKeyPath)
                value = objFromJsonFile[key]

                if key not in objFromConfig:
                    objFromConfig[key] = value
                    continue

                if not isinstance(value, type(objFromConfig[key])):
                    log.warn(f"'{thisKeyPathFormatted}' in user config is not of expected type '{type(objFromConfig[key])}'; using default value")
                    continue

                if isinstance(value, dict):
                    objectsToRead.append((
                        thisKeyPath,
                        objFromJsonFile[key],
                        objFromConfig[key],
                    ))
                else:
                    objFromConfig[key] = objFromJsonFile[key]

        log.info("Finished loading config successfully")
        return
    except json.JSONDecodeError as e:
        log.error(f"Failed to decode JSON config file {configPath}! ({e})")
    except UnicodeDecodeError as e:
        log.error(f"{configPath} is not a valid Unicode file! ({e})")
    except Exception as e:
        if isinstance(e, tuple(info.ioErrors.keys())):
            log.error(info.ioErrors[type(e)].format(configPath) 
                     + f"({e})")
        else:
            raise

    log.info("Finished loading config with errors")
api.addToAPI("cfg", "loadConfig", loadConfig)

@overload
def get[T](
    expectedType: type[T] | tuple[type[T], ...],
    *keys: str,
    throw: Literal[True]
) -> T: ...

@overload
def get[T](
    expectedType: type[T] | tuple[type[T], ...],
    *keys: str,
    throw: Literal[False]
) -> T | None: ...

@overload
def get[T](
    expectedType: type[T] | tuple[type[T], ...],
    *keys: str,
    throw: bool = False
) -> T | None: ...

def get[T](
    expectedType: type[T] | tuple[type[T], ...],
    *keys: str,
    throw: bool = False
) -> T | None:
    """
    Gets a value from user config w/ fallback to default config if no value is 
    found in user config. If no value is found in user and default configs 
    either returns None if throw == False or raises a KeyError.

    Args:
        expectedType <type object or a tuple of type objects)>: expected type

        keys <str, variadic>: key path to value in user config. For example, 
            if you need to get 'footerItems.time.format', then keys is 
            ("footerItems", "time", "format")

    Returns:
        <type of expectedType> if value exists either in user config or 
        default config

        None if throw == False value does not exist both in user and 
        default configs

    Errors:
        KeyError if throw == True and value does not exist both in user 
        and default configs
    """
    keyPath = ".".join(keys)

    value = config

    for key in keys:
        if key not in value:
            errormsg = f"'{key}' of '{keyPath}' is not in config!"
            log.error(errormsg)

            if throw:
                raise KeyError(errormsg)

            return None

        if key != keys[-1] and not isinstance(value, dict):
            errormsg = f"'{key}' of '{keyPath}' in config is not a JSON object!"
            log.error(errormsg)

            if throw:
                raise KeyError(errormsg)

            return None

        value = value[key]
    else:
        if isinstance(value, expectedType):
            return value

        errormsg = f"'{keyPath}' in config is of type '{type(value)}', expected {expectedType}!"
        log.error(errormsg)

        if throw:
            raise KeyError(errormsg)

        return None
api.addToAPI("cfg", "get", get)

if __name__ == "__main__":
    loadConfig(input("Config path: "))
    print(config)

