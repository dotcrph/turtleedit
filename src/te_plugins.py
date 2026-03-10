import te_api as api
import te_logging as log
import te_info as info

from sys import path
from os import getcwd, chdir
from os.path import isfile, join

# NOTE: I am intentionally not wrapping vars below in Mutable

pluginsDir = "plugins"
api.addToAPI("plugins", "pluginsDir", pluginsDir)

initFilename = "init.py"
api.addToAPI("plugins", "initFilename", initFilename)

initDir = join(pluginsDir, initFilename)
api.addToAPI("plugins", "initDir", initDir)

def loadPlugins() -> None:
    if not isfile(initDir):
        log.warn(f"Failed to find '{initDir}', ignoring")
        return

    try:
        with open(initDir, 'r', encoding='utf-8') as initFile:
            initFileAsString = initFile.read()
    except Exception as e:
        if isinstance(e, tuple(info.ioErrors.keys())):
            log.error(info.ioErrors[type(e)].format(initDir) 
                     + f"({e})")
            return
        else:
            raise

    log.info("Loading plugins...")
    initCompiled = compile(initFileAsString, initFilename, 'exec')

    originalDir = getcwd()
    pluginsFullDir = join(originalDir, pluginsDir)

    log.info(f"Executing '{initFilename}' from '{pluginsFullDir}'")
    chdir(pluginsFullDir)
    
    if (pluginsFullDir not in path):
        path.append(pluginsFullDir)

    exec(initCompiled, api.apiGlobals)

    path.remove(pluginsFullDir)

    chdir(originalDir)
    log.info(f"Changed working directory back to '{originalDir}'")

    log.info("Successfully loaded plugins!")
