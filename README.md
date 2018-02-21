# Domoticz-plugin-installer
A python plugin that makes it really easy to install other python plugins

Just paste in the URL into this plugin's input field, and it will do the rest.

- It downloads the zip file URL you provide, unpacks that file into a new plugin directory, and finally CHMOD's the plugin.py file.
- The URL you provide is processed when you press "update" on the plugin, or when Domoticz boots.
- It checks to see that it hasn't already processed the current URL (and that it's a valid URL).

## Installing
Follow the standard plugin installation instructions. It may be the last time that you have to follow them :-)

https://www.domoticz.com/wiki/Using_Python_plugins

