import te_api as api
import te_logging as log
import te_io as io

from os.path import isfile, join

initFilename = "init.py"
initDir = join("plugins", initFilename)

def loadPlugins() -> None:
    if not isfile(initDir):
        log.warn(f"Failed to find '{initDir}', ignoring")
        return

    try:
        with open(initDir, 'r', encoding='utf-8') as initFile:
            initFileAsString = initFile.read()
    except Exception as e:
        if isinstance(e, tuple(io.ioErrors.keys())):
            log.error(io.ioErrors[type(e)].format(initDir) 
                     + f"({e})")
            return
        else:
            raise

    log.info("Loading plugins...")

    initCompiled = compile(initFileAsString, initFilename, 'exec')
    exec(initCompiled, api.apiGlobals)
    
    log.info("Successfully loaded plugins!")
