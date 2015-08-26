#!/usr/bin/env python

from __future__ import print_function
from commands import getoutput
from time import sleep
from os.path import expanduser
import os
import re

script_location = os.path.dirname(os.path.realpath(__file__))

proxy_ssid = ["iiscwlan", "opbwlan"]
proxy_set_script = "bash {0}/iisc_proxy_set.sh".format(script_location)
proxy_unset_script = "bash {0}/proxy_unset.sh".format(script_location)
checking_interval = 2
default_log_file = expanduser("~/.proxy_log")

ssid_matcher=re.compile("ESSID:\"[\w]*\"")
ssid_slice=slice(7, -1)

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

def log_output(string, log_file=default_log_file):
    file_to_write = open(log_file, "a")
    file_to_write.write(string)
    print(string, end="")
    file_to_write.close()

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
    main(checking_interval)
