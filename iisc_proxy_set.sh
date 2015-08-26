#!/bin/bash

HTTP_PROXY_HOST=proxy.iisc.ernet.in
HTTPS_PROXY_HOST=proxy.iisc.ernet.in
FTP_PROXY_HOST=proxy.iisc.ernet.in
PROXY_PORT=3128

gsettings set org.gnome.system.proxy mode manual
gsettings set org.gnome.system.proxy.http host "$HTTP_PROXY_HOST"
gsettings set org.gnome.system.proxy.http port "$PROXY_PORT"
gsettings set org.gnome.system.proxy.https host "$HTTPS_PROXY_HOST"
gsettings set org.gnome.system.proxy.https port "$PROXY_PORT"
gsettings set org.gnome.system.proxy.ftp host "$FTP_PROXY_HOST"
gsettings set org.gnome.system.proxy.ftp port "$PROXY_PORT"

cp /home/bolt/Code/configs/proxy_settings_iiscwlan /home/bolt/.current_proxy
