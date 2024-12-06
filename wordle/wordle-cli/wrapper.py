
import subprocess
import os

while 1:
    try:
        p = subprocess.Popen(["python3", "wordle.py"])
        p.wait()
        os.system('clear')
        time.sleep(0.1)
    except:
        pass