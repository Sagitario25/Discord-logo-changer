import os
import subprocess
import shutil

def changeEXEicon (originalPath, resultPath, iconPath):
	subprocess.run (["tool.exe", "-open", originalPath, "-save", resultPath, "-action", "addskip", "-res", iconPath, "-mask", "ICONGROUP,MAINICON,"], capture_output = True)

def changeDiscordIcon (iconName, bypass = False):
	if (not iconName.split ('\\') [-1] in getNames()) and (not bypass):
		raise FileNotFoundError ("Provided icon name does not exist")

	paths = getPaths ()

	shutil.copy (iconName + ".ico", paths ["ico1"])
	shutil.copy (iconName + ".ico", paths ["ico2"])
	changeEXEicon (paths ["exe"], paths ["exe"], iconName + ".ico")

	os.remove ("tool.ini")

def getNames ():
	names = []
	for i in os.listdir ("Icons"):
		name = os.path.join ("Icons", i)
		if os.path.isfile (name) and os.path.splitext (i) [1] == ".ico":
			names.append (os.path.splitext (i) [0])
	return names

def callRestore ():
	changeDiscordIcon ("app", True)

def callChange (name):
	changeDiscordIcon (os.path.join ("Icons", name))

def getPaths ():
	paths = {}
	paths ["discord"] = os.path.join (os.getenv ("localappdata"), "Discord")

	for i in os.listdir (paths ["discord"]):
		name = os.path.join (paths ["discord"], i)
		if i [:3] == "app" and os.path.isdir (name):
			paths ["discordApp"] = name
	
	paths ["ico1"] = os.path.join (paths ["discord"], "app.ico")
	paths ["ico2"] = os.path.join (paths ["discordApp"], "app.ico")
	paths ["exe"] = os.path.join (paths ["discordApp"], "Discord.exe")

	return paths