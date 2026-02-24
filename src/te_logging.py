from datetime import datetime
import os
import os.path

logsDir: str = "logs"
os.makedirs(logsDir, exist_ok=True)

logFilename: str = datetime.today().strftime("log_%y-%m-%d.txt")
logPath: str = os.path.join(logsDir, logFilename)

def error(msg: str):
    prefix("ERROR", msg)

def prefix(prefix: str, msg: str):
    time: str = datetime.now().strftime("%H-%M-%S")

    with open(logPath, "a", encoding="utf-8") as f:
        f.write(f"({time}) [{prefix}] {msg}")
