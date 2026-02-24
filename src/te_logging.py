from datetime import datetime
import os
import os.path

logsDir: str = "logs"
os.makedirs(logsDir, exist_ok=True)

logFilename: str = datetime.now().strftime("log_%y-%m-%d_%H-%M-%S.txt")
logPath: str = os.path.join(logsDir, logFilename)

lastLogMessage = ""

def error(msg: str):
    prefix("ERROR", msg)

def info(msg: str):
    prefix("Info", msg)

def prefix(prefix: str, msg: str):
    global lastLogMessage
    lastLogMessage = f"[{prefix}] {msg}"

    time: str = datetime.now().strftime("%H:%M:%S")
    with open(logPath, "a", encoding="utf-8") as f:
        f.write(f"({time}) " + lastLogMessage + "\n")
