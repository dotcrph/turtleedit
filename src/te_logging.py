import te_api as api

from datetime import datetime
import os
import os.path

logsDir: api.Mutable[str] = api.Mutable(os.path.join(os.getcwd(), "logs"))
api.addToAPI("log", "logsDir", logsDir)

logFilename: api.Mutable[str]                                                 \
    = api.Mutable(datetime.now().strftime("log_%y-%m-%d_%H-%M-%S.txt"))
api.addToAPI("log", "logFilename", logFilename)

logPath: api.Mutable[str] = api.Mutable(os.path.join(logsDir.v, logFilename.v))
api.addToAPI("log", "logPath", logPath)

lastLogMessage: api.Mutable[str] = api.Mutable("")
api.addToAPI("log", "lastLogMessage", lastLogMessage)

os.makedirs(logsDir.v, exist_ok=True)

def error(msg: str):
    prefix("ERROR", msg)
api.addToAPI("log", "error", error)

def warn(msg: str):
    prefix("WARNING", msg)
api.addToAPI("log", "warn", warn)

def info(msg: str):
    prefix("Info", msg)
api.addToAPI("log", "info", info)

def prefix(prefix: str, msg: str):
    global lastLogMessage
    lastLogMessage.v = f"[{prefix}] {msg}"

    time: str = datetime.now().strftime("%H:%M:%S")

    logMsgWithTime: str = f"({time}) {lastLogMessage.v}"

    print(logMsgWithTime)
    with open(logPath.v, "a", encoding="utf-8") as f:
        f.write(logMsgWithTime + "\n")
api.addToAPI("log", "prefix", prefix)
