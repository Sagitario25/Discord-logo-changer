import os
import subprocess
import shutil
import subprocess
import sys
from packaging import version

def changeEXEicon (originalPath, resultPath, iconPath):
	taskkill ()
	#os.system (f"tool.exe -open \"{originalPath}\" -save \"{resultPath}\" -action addskip -res \"{iconPath}\" -mask ICONGROUP,MAINICON,")
	subprocess.run (["tool.exe", "-open", originalPath, "-save", resultPath, "-action", "addskip", "-res", iconPath, "-mask", "ICONGROUP,MAINICON,"], capture_output = True)
	if os.path.splitext (sys.argv[0])[1] == ".exe":
		input ()

def changeDiscordIcon (iconName, bypass = False):
	if (not iconName.split ('\\')[-1] in getNames()) and (not bypass):
		raise FileNotFoundError ("Provided icon name does not exist")

	paths = getPaths ()

	shutil.copy (iconName + ".ico", paths["ico1"])
	shutil.copy (iconName + ".ico", paths["ico2"])

	counter = 0
	while not os.path.exists (paths["exe"] + ".new"):
		changeEXEicon (paths["exe"], paths["exe"] + ".new", iconName + ".ico")
		if counter > 4:
			raise Exception ("Adding icon failed")
		counter += 1
	os.remove (paths["exe"])
	os.rename (paths["exe"] + ".new", paths["exe"])

	os.remove ("tool.ini")

def getNames ():
	names = []
	for i in os.listdir ("Icons"):
		name = os.path.join ("Icons", i)
		if os.path.isfile (name) and os.path.splitext (i)[1] == ".ico":
			names.append (os.path.splitext (i)[0])
	return names

def callRestore ():
	paths = getPaths ()

	taskkill ()

	os.remove (paths["ico1"])
	os.remove (paths["ico2"])
	os.remove (paths["exe"])

	shutil.copy (os.path.join ("Backup", "app.ico"), paths["ico1"])
	shutil.copy (os.path.join ("Backup", "app.ico"), paths["ico2"])
	shutil.copy (os.path.join ("Backup", "Discord.exe"), paths["exe"])


def callChange (name):
	changeDiscordIcon (os.path.join ("Icons", name))
	print (f"Logo changed to {name}")
	print ("To apply the changes, please restart your computer")

def getPaths ():
	paths = {}
	paths["discord"] = os.path.join (os.getenv ("localappdata"), "Discord")

	while not os.path.exists (paths ["discord"]):
		input ("Discord not installed, install to procced")

	for i in os.listdir (paths["discord"]):
		name = os.path.join (paths["discord"], i)
		newestVer = version.parse ("0.0.0")
		if i[:3] == "app" and os.path.isdir (name):
			try:
				ver = version.parse (os.path.basename (name)[4:])
				if ver > newestVer:
					newestVer = ver
				paths["discordApp"] = name
			except:
				pass
	
	paths["ico1"] = os.path.join (paths["discord"], "app.ico")
	paths["ico2"] = os.path.join (paths["discordApp"], "app.ico")
	paths["exe"] = os.path.join (paths["discordApp"], "Discord.exe")

	while not (os.path.exists (paths["ico1"]) and os.path.exists (paths["ico2"]) and os.path.exists (paths["discordApp"])):
		input (f"Some files are missing in discord folder ({paths['discord']}), fix them or reinstall discord.")

	return paths

def taskkill (name = "discord.exe"):
	#os.system ("taskkill -f -im discord.exe")
	subprocess.run (["taskkill", "-f", "-im", name], capture_output = True)