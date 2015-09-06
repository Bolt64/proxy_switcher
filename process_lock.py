#!/usr/bin/env python

import psutil

def list_processes(pids_to_exclude=[]):
    processes = [psutil.Process(pid) for pid in psutil.pids() if not pid in pids_to_exclude]
    return [i for i in [" ".join(process.cmdline()) for process in processes] if i!=""]

def look_for_processes(name, process_names):
    return filter(lambda x: name in x, process_names)

def process_is_running(name, pids_to_exclude=[]):
    procces_names = list_processes(pids_to_exclude)
    if look_for_processes(name, procces_names):
        return True
    else:
        return False

if __name__=="__main__":
    from sys import argv
    from os import getpid
    pid = getpid()
    print(process_is_running(argv[-1], [pid]))
