import te_api as api

from datetime import datetime
import os
import os.path

logsDir: str = "logs"
os.makedirs(logsDir, exist_ok=True)
api.addToAPI("log", logsDir)

logFilename: str = datetime.now().strftime("log_%y-%m-%d_%H-%M-%S.txt")
api.addToAPI("log", logFilename)

logPath: str = os.path.join(logsDir, logFilename)
api.addToAPI("log", logPath)

lastLogMessage = ""
api.addToAPI("log", lastLogMessage)

def error(msg: str):
    prefix("ERROR", msg)
api.addToAPI("log", error)

def warn(msg: str):
    prefix("WARNING", msg)
api.addToAPI("log", warn)

def info(msg: str):
    prefix("Info", msg)
api.addToAPI("log", info)

def prefix(prefix: str, msg: str):
    global lastLogMessage
    lastLogMessage = f"[{prefix}] {msg}"

    time: str = datetime.now().strftime("%H:%M:%S")

    logMsgWithTime: str = f"({time}) {lastLogMessage}"

    print(logMsgWithTime)
    with open(logPath, "a", encoding="utf-8") as f:
        f.write(logMsgWithTime + "\n")
api.addToAPI("log", prefix)
