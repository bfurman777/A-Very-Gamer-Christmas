#!/usr/bin/python3

import sys
import subprocess
import os


while 1:
    try:
        p = subprocess.Popen(sys.argv[1:]) # strip this program name
        p.wait()
        os.system('clear')
        time.sleep(0.1)
    except:
        pass
