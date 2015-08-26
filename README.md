# ProxyAutoSwitcher v0.01

## About ProxyAutoSwitcher (PAS)
PAS switches you proxies for you based on your WiFi ssid. It's useful when your
university network uses a proxy and you are tired of constantly manually
switching between turning on proxy and turning it off.

## Platform
In principle, it should work on any recent GNOME based linux distro, though it
has only been tested on Ubuntu and Debian.

## Installation
Add this line to your bashrc
```
source $HOME/.current_proxy
```

Make the script executable by using chmod
```
chmod +x proxy_autoconfig.py
```

Add it to the startup applications list.
