#!/usr/bin/env python

## Some necessary imports

from __future__ import print_function
from commands import getoutput
from time import sleep
from os.path import expanduser
import os
import re
from datetime import datetime
import process_lock as pl

###

## Configuration options

script_location = os.path.dirname(os.path.realpath(__file__))

proxy_ssid = ["iiscwlan", "opbwlan"] # Add whatever SSIDs you want to use the proxy for
proxy_set_script = "bash {0}/iisc_proxy_set.sh".format(script_location) # The script you want to run to turn on proxy
proxy_unset_script = "bash {0}/proxy_unset.sh".format(script_location) # The script to turn off proxy
checking_interval = 2 # The checking frequency in seconds.
default_log_file = expanduser("~/.proxy_log") # Where the logging will happen.

ssid_matcher=re.compile("ESSID:\"[\w]*\"") # A regular expression to match to the output of iwconfig.
ssid_slice=slice(7, -1)

## Logs the string to the log file and stdout.
def log_output(string, log_file=default_log_file):
    now = datetime.now()
    timestamped_string = "[{0}:{1}:{2}-{3}/{4}/{5}] {6}".format(now.hour, now.minute, now.second, now.day, now.month, now.year, string)
    file_to_write = open(log_file, "a")
    file_to_write.write(timestamped_string)
    print(timestamped_string, end="")
    file_to_write.close()
###

def set_proxy():
    log_output(str(getoutput(proxy_set_script))+'\n')
    log_output(str(getoutput("cp {0}/proxy_settings_iiscwlan ~/.current_proxy".format(script_location)))+'\n')

def unset_proxy():
    log_output(str(getoutput(proxy_unset_script))+'\n')
    log_output(str(getoutput("cp {0}/proxy_settings_other ~/.current_proxy".format(script_location)))+'\n')

def get_ssid():
    out=getoutput('/sbin/iwconfig')
    result=ssid_matcher.search(out)
    if result:
        return result.string[result.start():result.end()][ssid_slice]
    else:
        return None

def main(interval=2):
    current_ssid=get_ssid()
    if current_ssid and current_ssid in proxy_ssid:
        log_output("Detected proxy network. Trying to set proxy.\n")
        set_proxy()
    else:
        log_output("WiFi off or non-proxy network detected. Trying to unset proxy.\n")
        unset_proxy()

    while True:
        if not current_ssid:
            log_output("WiFi is off. Doing nothing.\n")
        else:
            log_output("WiFi is on. Current ssid is {0}.\n".format(current_ssid))
        sleep(interval)
        new_ssid=get_ssid()
        if new_ssid!=current_ssid:
            if new_ssid and new_ssid in proxy_ssid:
                log_output("Proxy network detected. Trying to set proxy.\n")
                set_proxy()
            else:
                log_output("WiFi off or non-proxy network detected.\n")
                unset_proxy()
        current_ssid=new_ssid

if __name__=="__main__":
    try:
        import psutil
        pid = os.getpid()
        if not pl.process_is_running("proxy_autoconfig", [pid]):
            main(checking_interval)
        else:
            print("Process already running.")
    except ImportError:
        main(checking_interval)
