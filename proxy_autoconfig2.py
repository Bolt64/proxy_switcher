#!/usr/bin/env python

from commands import getoutput
from time import sleep
from os.path import expanduser
import re

proxy_ssid=["iiscwlan", "opbwlan"]
proxy_set_script="./iisc_proxy_set.sh"
proxy_unset_script="./proxy_unset.sh"
checking_interval=2

ssid_matcher=re.compile("ESSID:\"[\w]*\"")
ssid_slice=slice(7, -1)

def get_ssid():
    out=getoutput('/sbin/iwconfig')
    result=ssid_matcher.search(out)
    if result:
        return result.string[result.start():result.end()][ssid_slice]
    else:
        return None

def main(interval=2):
    current_ssid=get_ssid()
    test=open(expanduser("~/.proxy_log"), "a")
    if current_ssid and current_ssid in proxy_ssid:
        test.write("changing to iiscwlan\n")
        test.write(str(getoutput(proxy_set_script))+'\n')
    else:
        test.write("doing nothing\n")
        test.write(str(getoutput(proxy_unset_script))+'\n')
    test.close()

    while True:
        test=open(expanduser("~/.proxy_log"), "a")
        if not current_ssid:
            test.write("Nothing detected\n")
        else:
            test.write(current_ssid + "\n")
        sleep(interval)
        print("blag")
        #test.write("blah\n")
        new_ssid=get_ssid()
        if new_ssid!=current_ssid:
            if new_ssid and new_ssid in proxy_ssid:
                test.write("setting proxy\n")
                test.write(str(getoutput(proxy_set_script))+'\n')
            else:
                test.write("unsetting proxy")
                test.write(str(getoutput(proxy_unset_script))+'\n')
        current_ssid=new_ssid
        test.close()

if __name__=="__main__":
    main(checking_interval)
