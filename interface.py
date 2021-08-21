import tkinter

window = tkinter.Tk ()
canvas = tkinter.Canvas (window)

def constructCanvas (canvas, contents):
	for i in contents:
		print (i ["text"])
		if   i ["type"] == "Label":
			tkinter.Label (canvas, text = i["text"]).pack (fill = tkinter.BOTH, expand = True)
		elif i ["type"] == "Button":
			tkinter.Button (canvas, text = i ["text"], command = i ["command"]).pack (fill = tkinter.BOTH, expand = True)

def resetCanvas (canvas):
	canvas.destroy ()
	canvas = tkinter.Canvas (window)

def mainMenu ():
	conts = [
		{"type" : "Button", "text" : "Change Logo", "command" : canvas.destroy},
		{"type" : "Button", "text" : "Restore default", "command" : canvas.destroy},
		{"type" : "Button", "text" : "Convert images to icons", "command" : lambda: resetCanvas (canvas)},
		{"type" : "Button", "text" : "Help", "command" : canvas.destroy}
	]
	constructCanvas(canvas, conts)

	canvas.pack (fill = tkinter.BOTH, expand = True)
	window.mainloop ()