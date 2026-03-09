import os
from time import time

# In seconds
maxAllowedLifetime: float = 259200 # 3 days

def cleanup(te) -> None:
    paths: list[str] = [os.path.join(te.log.logsDir.v, e) 
                        for e in os.listdir(te.log.logsDir.v)]
    
    for path in paths:
        if not os.path.isfile(path):
            continue

        # NOTE: On Unix(-like) getctime is not actually the time when the file 
        # was created, it is the time when the metadata was last changed. This 
        # is not really important but may explain some strange behaviour
        secsSinceCreation: float = time() - os.path.getctime(path)

        if (secsSinceCreation <= maxAllowedLifetime):
            continue

        te.log.prefix("Log Cleaner", f"Removing file {path}")
        os.remove(path)

