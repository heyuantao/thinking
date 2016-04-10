import subprocess
import os

def runScriptInBackground():    
    with open(os.devnull, 'w') as devnull:
        subprocess.Popen(['/bin/ping','-c','10','www.baidu.com'],stdout=devnull,stderr=devnull)
        #subprocess.Popen("ls -al /",stdout=devnull,shell=True)