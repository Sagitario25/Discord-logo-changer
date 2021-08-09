import gestor
import command
import os
import shutil

if not os.path.exists (os.path.join ("backup", "app.ico")):
	shutil.copy (os.path.join (os.getenv ("localappdata"), "Discord", "app.ico"), os.path.join ("backup", "app.ico"))
	print ("Backed up discord icon")

if not os.path.exists (os.path.join ("backup", "Discord.exe")):
	discord = os.path.join (os.getenv ("localappdata"), "Discord")
	for i in os.listdir (discord):
		name = os.path.join (discord, i)
		if i [:3] == "app" and os.path.isdir (name):
			discordApp = name

	shutil.copy (os.path.join (discordApp, "Discord.exe"), os.path.join ("backup", "Discord.exe"))
	print ("Backed up discord executable")

com = command.Interpreter ()

com.addCommand("getNames", gestor.getNames)
com.addCommand("restore", gestor.callRestore)
com.addCommand("change", gestor.callChange)

while True:
	com.call (input ("--- "))