import os
import subprocess

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# pid2name = dict()

# run this every 114 logs or can not find pid->name
def updatePs():
    pid2name = dict()
    with os.popen("adb shell ps -o PID -o NAME",'r') as f:
        lines = f.read()
        for line in lines.split("\n"):
            pid = line[0:5]
            name = line[6:]
            pid2name[pid] = name
        return pid2name

def logdog():
    p = subprocess.Popen(
            args="adb logcat",
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False)
    
    with p:
        prevHeader = ""
        pid2name = {}
        for line in p.stdout:
            thisline = line.decode("utf-8", errors='ignore')
            date = thisline[0:5]
            time = thisline[6:18]
            pid = thisline[19:24]
            tid = thisline[25:30]
            lvl = thisline[31:32]
            if(thisline[0:33] == prevHeader):
                if(pid in pid2name):
                    thisline = ' '*(33 + len(pid2name[pid])) + " > " + thisline[33:]
                else:
                    thisline = ' '*(33 + 8) + " > " + thisline[33:]

            else:
                prevHeader = thisline[0:33]
                if(pid not in pid2name):
                    pid2name = updatePs()
                if(pid in pid2name):
                    thisline = thisline[0:33] + pid2name[pid] + " > " + thisline[33:]
                else:
                    thisline = thisline[0:33] + "Unknown" + " > " + thisline[33:]


            # print(date, "|", time, "|", pid, "|", tid, "|", lvl, "|", )

            if(  lvl.upper() == "E" ):
                print(bcolors.FAIL + thisline + bcolors.ENDC, end='')
            elif(lvl.upper() == "W" ):
                print(bcolors.WARNING + thisline + bcolors.ENDC, end='')
            elif(lvl.upper() == "D" ):
                print(bcolors.ENDC + thisline + bcolors.ENDC, end='')
            elif(lvl.upper() == "L" ):
                print(bcolors.OKCYAN + thisline + bcolors.ENDC, end='')
            elif(lvl.upper() == "I" ):
                print(bcolors.BOLD + thisline + bcolors.ENDC, end='')
            else:
                print(thisline, end='')


if __name__ == "__main__":
    logdog()
