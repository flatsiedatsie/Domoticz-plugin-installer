# Plugin that makes it easier to install other plugins. Just insert the URL.
# It checks if the URL in the input field was already installed in a previous round.
"""
<plugin key="python_plugin_installer" name="Python Plugin installer" author="blauwebuis" version="1.0.0" wikilink="http://www.domoticz.com/wiki/plugins/plugin.html" externallink="https://www.domoticz.com/">
	<params>
		<param field="Mode1" label="Plugin URL (ending with .zip)" width="300px" required="false" default=""/>
	</params>
</plugin>
"""

try:
	import Domoticz
except ImportError:
	import fakeDomoticz as Domoticz
	
import shelve
import os
from subprocess import call
import time
import sys
import urllib.request
import zipfile

class BasePlugin:
	def __init__(self):
		return

	def onStart(self):
		#Domoticz.Debugging(1)
		
		self.dirName = os.path.dirname(__file__)
		
		Domoticz.Debug("Plugin folder = " + str(self.dirName))
		
		pluginUrl = str(Parameters["Mode1"])
		Domoticz.Log("Found plugin URL: " + pluginUrl)
		pluginsFolder = self.dirName.rsplit('/', 1)
		Domoticz.Debug("pluginsFolder = " + str(pluginsFolder[0]))
		
		if pluginUrl.startswith("http") and pluginUrl.endswith(".zip"):
			
			databaseFile = self.dirName + "/pythonPluginsInstaller"
			database = shelve.open(databaseFile)
			try:
				lastInstalledPlugin = str(database['lastInstalledPluginUrl'])
				Domoticz.Debug("Previously installed plugin URL: " + str(lastInstalledPlugin))
			except:
				lastInstalledPlugin = ""
				Domoticz.Debug("couldn't find which plugin was last installed")
				database['lastInstalledPluginUrl'] = [""]
			
			if str(lastInstalledPlugin) != pluginUrl:
				Domoticz.Log("INSTALLING NEW PLUGIN")
				
				try:
					zipPath = pluginsFolder[0] + "/plugin.zip"
					urllib.request.urlretrieve(pluginUrl, zipPath)
					try:
						with zipfile.ZipFile(zipPath,"r") as zip_ref:
							zip_ref.extractall()
						database['lastInstalledPluginUrl'] = pluginUrl
					except:
						Domoticz.Error("Unable to extract plugin zip file")

					directories = os.listdir(pluginsFolder[0])
					Domoticz.Log("You now have the following python plugins installed:")
					for directory in directories:
						possibleDirectory = pluginsFolder[0] + "/" + directory
						if os.path.isdir(possibleDirectory):
							Domoticz.Log(directory)
							startCommand = "sudo chmod +x " + pluginsFolder[0] + "/" + directory + "/plugin.py"
							Domoticz.Debug(str(startCommand))
							
							try:
								try:
									call (startCommand, shell=True)
								except:
									cloner = os.popen(startCommand).read()
							except:
								pass
								#Domoticz.Error("Unable to chmod plugin.py file")
				except:
					Domoticz.Error("Unable to install plugin (Check zip file URL?)")
			
			else:
				Domoticz.Log("Plugin already installed.")
		
			database.close()
			
		# Perhaps in the future add a git option here.
		#if pluginUrl.startswith("http") and pluginUrl.endswith(".git"):
		#	Domoticz.Log("git file")
		
		else:
			Domoticz.Error("Not a correct URL. It must start with http and end with .zip")	
		
		return
			
	def onStop(self):
		Domoticz.Log("onStop called")

	def onConnect(self, Connection, Status, Description):
		Domoticz.Log("onConnect called")

	def onMessage(self, Connection, Data):
		Domoticz.Log("onMessage called")

	def onCommand(self, Unit, Command, Level, Hue):
		Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

	def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
		Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

	def onDisconnect(self, Connection):
		Domoticz.Log("onDisconnect called")

	def onHeartbeat(self):
		Domoticz.Log("onHeartbeat called")

global _plugin
_plugin = BasePlugin()

def onStart():
	global _plugin
	_plugin.onStart()

def onStop():
	global _plugin
	_plugin.onStop()

def onConnect(Connection, Status, Description):
	global _plugin
	_plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
	global _plugin
	_plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
	global _plugin
	_plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
	global _plugin
	_plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
	global _plugin
	_plugin.onDisconnect(Connection)

def onHeartbeat():
	global _plugin
	_plugin.onHeartbeat()

	# Generic helper functions
def DumpConfigToLog():
	for x in Parameters:
		if Parameters[x] != "":
			Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
	Domoticz.Debug("Device count: " + str(len(Devices)))
	for x in Devices:
		Domoticz.Debug("Device:		   " + str(x) + " - " + str(Devices[x]))
		Domoticz.Debug("Device ID:	   '" + str(Devices[x].ID) + "'")
		Domoticz.Debug("Device Name:	 '" + Devices[x].Name + "'")
		Domoticz.Debug("Device nValue:	" + str(Devices[x].nValue))
		Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
		Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
	return