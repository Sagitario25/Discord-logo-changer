import gestor
import command
import os
import shutil

paths = gestor.getPaths ()

if not os.path.exists ("Backup"):
	os.mkdir ("Backup")

if not os.path.exists ("Icons"):
	os.mkdir ("Icons")

if not os.path.exists (os.path.join ("backup", "app.ico")):
	shutil.copy (paths ["ico1"], os.path.join ("backup", "app.ico"))
	print ("Backed up discord icon")

if not os.path.exists (os.path.join ("backup", "Discord.exe")):
	shutil.copy (paths ["exe"], os.path.join ("backup", "Discord.exe"))
	print ("Backed up discord executable")

com = command.Interpreter ()

com.addCommand("getNames", gestor.getNames, "Prints all the names of available icons\nPlace icons in .ico format in \"Icons\" folder to add more\nI recomend the next page for converting images to icons\nhttps://image.online-convert.com/convert-to-ico")
com.addCommand("restore", gestor.callRestore, "Restores the icon back to the original\nThe original is the icon that was in use when this program was executed for first time")
com.addCommand("change", gestor.callChange, "Changes Discord logo for the specified one\nPlace the name of the icon separated by an space\nIf the name has spaces in it it must be writed between quotation marks \"\"\nTo get possible names use getNames")

print ('Type "listCommands" to see a list of all available commands')
print ('Type "help" before any command to get help')

while True:
	com.call (input ("--- "))
	print ()