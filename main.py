import gestor
import command
import os
import shutil
import sys

installed = gestor.discordInstalled ()
try:
	gestor.getPaths ()
	installed = installed and True
except:
	installed = False

if installed:
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

def commandline ():
	com = command.Interpreter ()

	com.addCommand("getNames", gestor.getNames, "Prints all the names of available icons\nPlace icons in .ico format in \"Icons\" folder to add more\nI recomend using the integrated icon converter (image2ico) to make the icons")
	com.addCommand("restore", gestor.callRestore, "Restores the icon back to the original\nThe original is the icon that was in use when this program was executed for first time")
	com.addCommand("change", gestor.callChange, "Changes Discord logo for the specified one\nPlace the name of the icon separated by an space\nIf the name has spaces in it it must be writed between quotation marks \"\"\nTo get possible names use getNames")
	com.addCommand("repair", gestor.callRepair, "Changing the icon or restoring may cause some errors on Discord\nThis will try to repair them, it is not very advanced\nReinstalling Discord is endorsed if this does not work")
	com.addCommand("image2ico", gestor.callImage2ico, "Converts any image into an ico,\nthen the ico can be set to be the Discord icon.\nThe name of the icon is the name of the image")

	print ('Type "listCommands" to see a list of all available commands')
	print ('Type "help" before any command to get help')

	while True:
		try:
			com.call (input ("--- "))
			print ()
		except Exception as e:
			print (e)

if len (sys.argv) > 1:
	if sys.argv[1] == "terminal":
		if not installed:
			print ("Discord is not installed, isn't detected or there are some files missing, there will not be any restrictions, but errors will occur.\n")
		commandline ()

import interface
interface.installed = interface.toButtonStatus (installed)
interface.mainMenu ()