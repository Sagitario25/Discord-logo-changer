import os
import subprocess
import shutil
import subprocess
import sys
import filecmp
import packaging.version
import PIL.Image

def changeEXEicon (originalPath, resultPath, iconPath):
	taskkill ()
	#os.system (f"tool.exe -open \"{originalPath}\" -save \"{resultPath}\" -action addskip -res \"{iconPath}\" -mask ICONGROUP,MAINICON,")
	subprocess.run (["tool.exe", "-open", originalPath, "-save", resultPath, "-action", "addskip", "-res", iconPath, "-mask", "ICONGROUP,MAINICON,"], capture_output = True)
	if os.path.splitext (sys.argv[0])[1] == ".exe":
		input ()

def changeDiscordIcon (iconName, bypass = False, tries = 1):
	if (not iconName.split ('\\')[-1] in getNames()) and (not bypass):
		raise FileNotFoundError ("Provided icon name does not exist")

	paths = getPaths ()

	shutil.copy (iconName + ".ico", paths["ico1"])
	shutil.copy (iconName + ".ico", paths["ico2"])

	counter = 0

	if not os.path.exists ("Cache"):
		os.mkdir ("Cache")
	paths["cached"] = os.path.join ("Cache", "Discord.exe")
	shutil.copyfile (paths["exe"], paths["cached"])

	while not filecmp.cmp (paths["exe"], paths["cached"]):
		changeEXEicon (paths["exe"], paths["exe"], iconName + ".ico")
		filecmp.clear_cache ()
		if counter > tries:
			raise Exception ("Adding icon failed")
		counter += 1

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

def callRepair ():
	paths = getPaths (False)

	return repair ([os.path.join ("Backup", "app.ico"), os.path.join ("Backup", "app.ico"), os.path.join ("Backup", "Discord.exe")],
	[paths["ico1"], paths["ico2"], paths["exe"]],
	["Icon 1", "Icon 2", "Discord's executable"])

def callImage2ico (paths, names = []):
	if not type (paths) == type ([]):
		paths = [paths]
	if not type (names) == type ([]):
		names = [names]
	for i in range (len (paths)):
		try:
			name = names[i]
		except:
			name, _ = os.path.splitext (os.path.basename (paths [i]))
			name += ".ico"
		image2ico (paths[i], os.path.join ("Icons", name))

def getPaths (checkFiles = True):
	paths = {}
	paths["discord"] = os.path.join (os.getenv ("localappdata"), "Discord")

	if not os.path.exists (paths ["discord"]):
		raise Exception ("Discord not installed, install to procced")

	for i in os.listdir (paths["discord"]):
		name = os.path.join (paths["discord"], i)
		newestVer = packaging.version.parse ("0.0.0")
		if i[:3] == "app" and os.path.isdir (name):
			try:
				ver = packaging.version.parse (os.path.basename (name)[4:])
				if ver > newestVer:
					newestVer = ver
				paths["discordApp"] = name
			except:
				pass
	
	if not "discordApp" in [i for i in paths]:
		shutil.rmtree (paths["discord"])
		return getPaths ()
	
	paths["ico1"] = os.path.join (paths["discord"], "app.ico")
	paths["ico2"] = os.path.join (paths["discordApp"], "app.ico")
	paths["exe"] = os.path.join (paths["discordApp"], "Discord.exe")
	
	if not os.path.exists (paths["discordApp"]):
		raise FileNotFoundError ("Discord is not installed")
	if not (os.path.exists (paths["ico1"]) and os.path.exists (paths["ico2"]) and os.path.exists (paths ["exe"])) and checkFiles:
		raise FileNotFoundError (f"Some files are missing in discord folder ({paths['discord']}), fix them or reinstall discord.")

	return paths

def repair (backupPaths, originalPaths, names):
	changes = []
	def repairFile (backupPath, originalPath, name):
		if not os.path.exists (originalPath):
			try:
				shutil.copy (backupPath, originalPath)
				changes.append (f"{name} repaired")
			except Exception as e:
				changes.append (f"{name} rapair failed")
		else:
			changes.append (f"{name} OK")

	for i in range (len (backupPaths)):
		repairFile (backupPaths[i], originalPaths[i], names[i])

	return changes

def image2ico (objective, result):
	def squareProportion (img):
		img = img.convert ("RGBA")
		side = max (img.width, img.height)
		square = PIL.Image.new ("RGBA", (side, side), (0, 0, 0, 0))

		x, y = startingCoords ((img.width, img.height))
		for i in range (0, img.width):
			for j in range (0, img.height):
				pixel = img.getpixel ((i, j))
				square.putpixel ((x + i, y + j), pixel)

		return square

	def startingCoords (res):
		smallSide = int ((max (res) - min (res)) / 2)
		indexBigSide = [i for i in res].index (max (res))

		coordList = [0, 0]
		coordList[indexBigSide] = 0
		coordList[1 - indexBigSide] = smallSide

		return tuple (coordList)

	img = PIL.Image.open (objective)
	img = squareProportion (img)
	img.save (result, format = "ICO", sizes = [(i, i) for i in [16, 32, 48, 256]])

def discordInstalled ():
	discordPath = os.path.join (os.getenv ("localappdata"), "Discord")
	if not os.path.exists (discordPath):
		return False
	for i in os.listdir (discordPath):
		name = os.path.join (discordPath, i)
		if i[:3] == "app" and os.path.isdir (name):
			return True
	return False

def checkBackup ():
	if not os.path.exists ("Backup"):
		return False

	return os.path.exists (os.path.join ("Backup", "app.ico")) and os.path.exists (os.path.join ("Backup", "Discord.exe"))

def taskkill (name = "discord.exe"):
	#os.system ("taskkill -f -im discord.exe")
	subprocess.run (["taskkill", "-f", "-im", name], capture_output = True)