import tkinter

def newWindow ():
	window = tkinter.Tk ()
	return window

def constructCanvas (canvas, contents):
	for i in contents:
		if   i ["type"] == "Label":
			tkinter.Label (canvas, text = i["text"]).pack (fill = tkinter.BOTH, expand = True)
		elif i ["type"] == "Button":
			tkinter.Button (canvas, text = i ["text"], command = i ["command"]).pack (fill = tkinter.BOTH, expand = True)

def mainMenu ():
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
	constructCanvas (window, conts)