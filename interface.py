import tkinter
import gestor
import functools
import os
import subprocess

def newWindow ():
	window = tkinter.Tk ()
	window.minsize (200, 0)
	return window

def constructCanvas (canvas, contents, side = tkinter.TOP):
	for i in contents:
		if   i ["type"] == "Label":
			tkinter.Label (canvas, text = i["text"]).pack (fill = tkinter.BOTH, expand = True, side = side)
		elif i ["type"] == "Button":
			tkinter.Button (canvas, text = i ["text"], command = i ["command"]).pack (fill = tkinter.BOTH, expand = True, side = side)
		elif i ["type"] == "Canvas":
			newCanvas = tkinter.Canvas (canvas)
			constructCanvas (newCanvas, i ["contents"], side = tkinter.LEFT)
			newCanvas.pack (fill = tkinter.BOTH, expand = True)

def mainMenu (lastWindow = None):
	if lastWindow != None:
		lastWindow.destroy ()
	window = newWindow ()

	conts = [
		{"type" : "Button", "text" : "Change Logo", "command" : lambda: chooseIcon (window)},
		{"type" : "Button", "text" : "Restore default", "command" : window.destroy},
		{"type" : "Button", "text" : "Convert images to icons", "command" : lambda: resetCanvas (canvas)},
		{"type" : "Button", "text" : "Help", "command" : window.destroy}
	]
	constructCanvas (window, conts)
	
	window.mainloop ()

def chooseIcon (lastWindow):
	lastWindow.destroy ()
	window = newWindow()

	conts = [
		{"type" : "Label", "text" : "Choose your icon"}
	]
	for i in gestor.getNames ():
		conts.append ({"type" : "Canvas", "contents" : [
			{"type" : "Button", "text" : i, "command" : functools.partial (changeIcon, i)},
			{"type" : "Button", "text" : "Preview", "command" : functools.partial (subprocess.run, [os.path.join (os.getenv ("windir"), "System32", "mspaint.exe"), os.path.join ("Icons", i + ".ico")])}
			]})
	conts.append ({"type" : "Label", "text" : ""})
	conts.append ({"type" : "Button", "text" : "Back to main menu", "command" : lambda: mainMenu (window)})

	constructCanvas (window, conts)

	window.mainloop ()

def changeIcon (name):
	pass
	#gestor.callChange (name)