import gestor
import functools
import os
import subprocess
import engine
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
		{"type" : "Button", "text" : "Repair discord", "state" : engine.toButtonStatus (gestor.checkBackup () and engine.buttonStatusToBool (installed)), "command" : repair},
		{"type" : "Button", "text" : "Restore default", "state" : engine.toButtonStatus (gestor.checkBackup () and engine.buttonStatusToBool (installed)), "command" : restore},
		{"type" : "Button", "text" : "Convert images to icons", "command" : lambda: image2ico (window)},
		{"type" : "Button", "text" : "Help", "command" : window.destroy},
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
			{"type" : "Button", "text" : "Preview", "side" : engine.tkinter.LEFT, "expand" : False, "command" : functools.partial (subprocess.run, [os.path.join (os.getenv ("windir"), "System32", "mspaint.exe"), os.path.join ("Icons", i + ".ico")])}
			]})
	conts.append ({"type" : "Label", "text" : ""})
	conts.append ({"type" : "Button", "text" : "Back to main menu", "command" : lambda: mainMenu (window)})

	engine.constructCanvas (window, conts)

	window.mainloop ()

def image2ico (lastWindow, selected = []):
	window = engine.newWindow (lastWindow)

	if len (selected) == 0:
		conts = [
			{"type" : "Label", "text" : "There are no images selected"},
			{"type" : "Button", "text" : "Select images", "command" : lambda: selectImages (window)},
		]
	else:
		conts = []
		for i in selected:
			conts.append ({"type" : "Canvas", "contents" : [
				{"type" : "Label", "text" : i[0], "side" : engine.tkinter.LEFT, "expand" : True},
				{"type" : "Button", "text" : "Preview", "side" : engine.tkinter.LEFT, "expand" : False, "command" : functools.partial (subprocess.run, [os.path.join (os.getenv ("windir"), "System32", "mspaint.exe"), i[1]])}
			]})
		conts.append ({"type" : "Button", "text" : "Select more images", "command" : lambda: selectImages (window, selected)})

	conts.append ({"type" : "Button", "text" : "Convert", "state" : engine.toButtonStatus (not len (selected) == 0), "command" : lambda: convert (selected)})
	conts.append ({"type" : "Label", "text" : ""})
	conts.append ({"type" : "Button", "text" : "Back to main menu", "command" : lambda: mainMenu (window)})

	engine.constructCanvas (window, conts)

	window.mainloop ()

def selectImages (lastWindow, toAppend = []):
	filetypes = [
		("All image format", ".png"),
		("All image format", ".jpg"),
		("All image format", ".jpeg"),
		("All image format", ".ico")
	]
	for i in engine.tkinter.filedialog.askopenfilenames (parent = lastWindow, filetypes = filetypes, title = "Select images"):
		if not os.path.exists ("Cache"):
			os.mkdir ("Cache")
		pathImage = os.path.join ("Cache", os.path.basename (i))
		shutil.copy (i, pathImage)
		toAppend.append (((os.path.basename (pathImage), pathImage)))

	image2ico (lastWindow, toAppend)

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
	warnWindow = functools.partial (engine.tkinter.messagebox.askokcancel, "Warning", "To complete the action discord is going to close, are you sure?")

	engine.warnedAction (warnWindow, action)

def restore ():
	warnWindow = functools.partial (engine.tkinter.messagebox.askokcancel, "Warning", "To complete the action discord is going to close, are you sure?")

	engine.warnedAction (warnWindow, gestor.callRestore)

def convert (images):
	pass