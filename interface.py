#Modules
import gestor
import engine

#Packages
import functools
import os
import subprocess
import shutil

installed = "disabled"



###Menus###
def mainMenu (lastWindow = None):
	if lastWindow == None:
		window = engine.createWindow ()
	else:
		window = engine.newWindow (lastWindow)

	conts = [
		{"type" : "Button", "text" : "Change Logo", "state" : installed, "command" : lambda: chooseIcon (window)},
		{"type" : "Button", "text" : "Repair discord", "command" : repair},
		{"type" : "Button", "text" : "Restore default", "state" : engine.toButtonStatus (gestor.checkBackup () and engine.buttonStatusToBool (installed)), "command" : restore},
		{"type" : "Button", "text" : "Convert images to icons", "command" : lambda: image2ico (window)},
		{"type" : "Button", "text" : "Help", "command" : window.destroy},
		{"type" : "Button", "text" : "Open icon folder", "command" : lambda: os.startfile ("Icons")},
		{"type" : "Label", "text" : ""},
		{"type" : "Button", "text" : "Exit", "command" : window.destroy}
	]
	engine.constructCanvas (window, conts)

	if not installed == "normal":
		engine.tkinter.messagebox.showwarning (title = "Discord not installed", message = "Discord is not installed, some options are now disabled")

	window.mainloop ()

def chooseIcon (lastWindow):
	window = engine.newWindow(lastWindow)

	conts = [
		{"type" : "Label", "text" : "Choose your icon"}
	]
	for i in gestor.getNames ():
		conts.append ({"type" : "Canvas", "contents" : [
			{"type" : "Button", "text" : i, "side" : engine.tkinter.LEFT, "expand" : True, "command" : functools.partial (changeIcon, i)},
			{"type" : "Button", "text" : "Preview", "side" : engine.tkinter.LEFT, "expand" : False, "command" : functools.partial (engine.previewImage, os.path.join ("Icons", i + ".ico"))}
			]})
	conts.append ({"type" : "Label", "text" : ""})
	conts.append ({"type" : "Button", "text" : "Back to main menu", "command" : lambda: mainMenu (window)})

	engine.constructCanvas (window, conts)

	window.mainloop ()

def image2ico (lastWindow, selected = []):
	def manageSelection ():
		newImages = selectImages (selected)
		image2ico (lastWindow, newImages)
	def conversionEnded (images, undone):
		engine.tkinter.messagebox.showinfo (title = "Conversion ended", message = f"The conversion has ended.\n{len (undone)} out of {len (images)} have failed.")
		if len (undone) == 0:
			mainMenu (lastWindow)
		else:
			if engine.tkinter.messagebox.askyesno (title = "Next action", message = "Show only onsuccesful images?"):
				image2ico (lastWindow, undone)
			else:
				mainMenu (lastWindow)

	window = engine.newWindow (lastWindow)

	if len (selected) == 0:
		conts = [
			{"type" : "Label", "text" : "There are no images selected"},
			{"type" : "Button", "text" : "Select images", "command" : manageSelection},
		]
	else:
		conts = []
		for i in selected:
			conts.append ({"type" : "Canvas", "contents" : [
				{"type" : "Label", "text" : i[0], "side" : engine.tkinter.LEFT, "expand" : True},
				{"type" : "Button", "text" : "Preview", "side" : engine.tkinter.LEFT, "expand" : False, "command" : functools.partial (engine.previewImage, i[1])}
			]})
		conts.append ({"type" : "Button", "text" : "Select more images", "command" : manageSelection})
		conts.append ({"type" : "Button", "text" : "Deselect last image", "command" : lambda: image2ico (lastWindow, selected[:-1])})
	conts.append ({"type" : "Button", "text" : "Convert", "state" : engine.toButtonStatus (not len (selected) == 0), "command" :  lambda: conversionEnded (selected, convert (selected)) if engine.tkinter.messagebox.askyesno (title = "Confirmation", message = "The conversion is going to start, are you sure?") else print ()})
	conts.append ({"type" : "Label", "text" : ""})
	conts.append ({"type" : "Button", "text" : "Back to main menu", "command" : lambda: mainMenu (window)})

	engine.constructCanvas (window, conts)

	window.mainloop ()

def selectImages (toAppend = []):
	filetypes = [
		("All image format", ".png"),
		("All image format", ".jpg"),
		("All image format", ".jpeg"),
		("All image format", ".ico")
	]

	if not os.path.exists ("Cache"):
			os.mkdir ("Cache")
	for i in engine.tkinter.filedialog.askopenfilenames (filetypes = filetypes, title = "Select images"):
		originalName = os.path.basename (i)
		pathImage = os.path.join ("Cache", str (len (toAppend)))
		objectiveName = os.path.splitext (originalName)[0] + ".ico"
		shutil.copy (i, pathImage)
		toAppend.append ((originalName, pathImage, objectiveName))

	return toAppend

###Actions###
def changeIcon (name):
	def action ():
		if engine.tkinter.messagebox.askokcancel (title = "Warning", message = "To complete the action discord is going to close, are you sure?"):
			gestor.callChange (name)
	warnWindow = functools.partial (engine.tkinter.messagebox.askokcancel, "Confirm logo change", f"Discord icon is going to be change to \"{name}\", are you sure?\nTo preview use previous menu.")

	engine.warnedAction (warnWindow, action)

def repair ():
	def action ():
		results = gestor.callRepair ()
		resultWindow = engine.newWindow (engine.tkinter.Tk ())
		resultWindow.title ("Repair results")
		conts = []

		for i in results:
			conts.append ({"type" : "Label", "text" : i})

		conts.append ({"type" : "Label", "text" : ""})
		conts.append ({"type" : "Button", "text" : "Back to main menu", "command" : resultWindow.destroy})

		engine.constructCanvas (resultWindow, conts)

	if installed == "disabled":
		engine.tkinter.messagebox.showwarning ("Warning", "Discord is not disabled, some errors may occur.")
	engine.warnedAction (action)

def restore ():
	engine.warnedAction (gestor.callRestore)

def convert (images):
	undone = []
	for i in images:
		path = os.path.join ("Icons", i[2])
		if os.path.exists (path):
			answer = engine.tkinter.messagebox.askyesnocancel ("Warning", f"There is already a icon named {i[2]}, do you want to overwrite it?\nPress cancel to skip.")
			if answer == True:
				gestor.callImage2ico (i[1], i[2])
			elif answer == False:
				while True:
					path = engine.tkinter.filedialog.asksaveasfilename (filetypes = [("Icon image", ".ico")], initialdir = os.path.join (os.getcwd (), "Icons"), initialfile = i[0])
					abspath = os.path.abspath ("Icons")
					if os.path.normpath (path [:len (abspath)]) == os.path.normpath (abspath) and os.path.splitext (path)[1] == ".ico":
						gestor.callImage2ico (i[1], os.path.splitext (os.path.basename (path))[0] + ".ico")
						break
					elif path == "":
						undone.append (i)
						break
					else:
						engine.tkinter.messagebox.showerror ("Invalid path", "The path you have choosen is not valid, it has to be in the Icons directory.")
			elif answer == None:
				undone.append (i)
		else:
			gestor.callImage2ico (i[1], i[2])
	return undone