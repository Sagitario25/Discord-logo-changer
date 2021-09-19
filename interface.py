import tkinter
import tkinter.messagebox
import gestor
import functools
import os
import subprocess

def createWindow ():
	window = tkinter.Tk ()
	window.minsize (200, 0)
	window.iconbitmap ("app.ico")
	window.title ("Discord Logo Changer")
	window.resizable (width = True, height = False)
	return window

def newWindow (window):
	resetWindow (window)
	return window

def resetWindow (window):
	for i in window.winfo_children ():
		i.destroy ()

def constructCanvas (canvas, contents):
	contents = defaultContents (contents)
	for i in contents:
		if   i["type"] == "Label":
			tkinter.Label (canvas, text = i["text"]).pack (fill = i["fill"], expand = i["expand"], side = i["side"])
		elif i["type"] == "Button":
			tkinter.Button (canvas, text = i["text"], command = i["command"], state = i["state"]).pack (fill = i["fill"], expand = i["expand"], side = i["side"])
		elif i["type"] == "Canvas":
			newCanvas = tkinter.Canvas (canvas)
			constructCanvas (newCanvas, i["contents"])
			newCanvas.pack (fill = tkinter.BOTH, expand = True)

def defaultContents (conts):
	for i in conts:
		keys = [j for j in i]
		if not "fill" in keys:
			i["fill"] = tkinter.BOTH
		if not "expand" in keys:
			i["expand"] = True
		if not "side" in keys:
			i["side"] = tkinter.TOP
		if not "state" in keys:
			i["state"] = "normal"

	return conts

def warnedAction (warnWindow, action):
	confirm = warnWindow ()
	if confirm:
		try:
			action ()
		except Exception as e:
			tkinter.messagebox.showerror (title = "Error", message = f"The next error ocurred while completing the action\n{e}")
	else:
		tkinter.messagebox.showinfo (title = "Action cancelled", message = "The change was cancelled, going back to menu.")

installed = "disabled"
def toButtonStatus (boolean):
	if boolean:
		return "normal"
	else:
		return "disabled"

def buttonStatusToBool (buttonStatus):
	if buttonStatus == "normal":
		return True
	elif buttonStatus == "disabled":
		return False
	else:
		return None

def mainMenu (lastWindow = None):
	if lastWindow == None:
		window = createWindow ()
	else:
		window = newWindow (lastWindow)

	conts = [
		{"type" : "Button", "text" : "Change Logo", "state" : installed, "command" : lambda: chooseIcon (window)},
		{"type" : "Button", "text" : "Repair discord", "state" : toButtonStatus (gestor.checkBackup () and buttonStatusToBool (installed)), "command" : repair},
		{"type" : "Button", "text" : "Restore default", "state" : toButtonStatus (gestor.checkBackup () and buttonStatusToBool (installed)), "command" : restore},
		{"type" : "Button", "text" : "Convert images to icons", "command" : lambda: resetWindow (window)},
		{"type" : "Button", "text" : "Help", "command" : window.destroy},
		{"type" : "Label", "text" : ""},
		{"type" : "Button", "text" : "Exit", "command" : window.destroy}
	]
	constructCanvas (window, conts)

	if not installed == "normal":
		tkinter.messagebox.showwarning (title = "Discord not installed", message = "Discord is not installed, some options are now disabled")

	window.mainloop ()

def chooseIcon (lastWindow):
	window = newWindow(lastWindow)

	conts = [
		{"type" : "Label", "text" : "Choose your icon"}
	]
	for i in gestor.getNames ():
		conts.append ({"type" : "Canvas", "contents" : [
			{"type" : "Button", "text" : i, "side" : tkinter.LEFT, "expand" : True, "command" : functools.partial (changeIcon, i)},
			{"type" : "Button", "text" : "Preview", "side" : tkinter.LEFT, "expand" : False, "command" : functools.partial (subprocess.run, [os.path.join (os.getenv ("windir"), "System32", "mspaint.exe"), os.path.join ("Icons", i + ".ico")])}
			]})
	conts.append ({"type" : "Label", "text" : ""})
	conts.append ({"type" : "Button", "text" : "Back to main menu", "command" : lambda: mainMenu (window)})

	constructCanvas (window, conts)

	window.mainloop ()

def changeIcon (name):
	def action ():
		if tkinter.messagebox.askokcancel (title = "Warning", message = "To complete the action discord is going to close, are you sure?"):
			gestor.callChange (name)
	warnWindow = functools.partial (tkinter.messagebox.askokcancel, "Confirm logo change", f"Discord icon is going to be change to \"{name}\", are you sure?\nTo preview use previous menu.")

	warnedAction (warnWindow, action)

def repair ():
	def action ():
		results = gestor.callRepair ()
		resultWindow = newWindow (tkinter.Tk ())
		resultWindow.title ("Repair results")
		conts = []

		for i in results:
			conts.append ({"type" : "Label", "text" : i})

		conts.append ({"type" : "Label", "text" : ""})
		conts.append ({"type" : "Button", "text" : "Back to main menu", "command" : resultWindow.destroy})

		constructCanvas (resultWindow, conts)
	warnWindow = functools.partial (tkinter.messagebox.askokcancel, "Warning", "To complete the action discord is going to close, are you sure?")

	warnedAction (warnWindow, action)

def restore ():
	warnWindow = functools.partial (tkinter.messagebox.askokcancel, "Warning", "To complete the action discord is going to close, are you sure?")

	warnedAction (warnWindow, gestor.callRestore)