import subprocess
import os

def hashValuer(path):
    cwd = os.getcwd().replace('\\','/')
    if (cwd != path):
        command = f'powershell -ExecutionPolicy ByPass -File Hash_values.ps1 -path "{path}"'
        subprocess.run(command)
    else:
        print('It is not possible to get the hash of the same directory from which the script is run.')
