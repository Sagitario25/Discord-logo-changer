import os
import subprocess

def changeEXEicon (originalPath, resultPath, iconPath):
	subprocess.run (["ResourceHacker/ResourceHacker.exe", "-open", originalPath, "-save", resultPath, "-action", "addskip", "-res", iconPath, "-mask", "ICONGROUP,MAINICON,"], capture_output = True)

def changeDiscordIcon (iconName):
	discord = os.path.join (os.getenv ("localappdata"), "Discord")
	for i in os.listdir (discord):
		name = os.path.join (discord, i)
		if i [:3] == "app" and os.path.isdir (name):
			discordApp = name

	ico1 = os.path.join (discord, "app.ico")
	ico2 = os.path.join (discordApp, "app.ico")
	exe = os.path.join (discordApp, "Discord.exe")