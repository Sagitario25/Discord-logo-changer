import tkinter

def constructCanvas (canvas, contents):
	for i in contents:
		print (i ["text"])
		if   i ["type"] == "Label":
			tkinter.Label (canvas, text = i["text"]).pack (fill = tkinter.BOTH, expand = True)
		elif i ["type"] == "Button":
			tkinter.Button (canvas, text = i ["text"], command = i ["command"]).pack (fill = tkinter.BOTH, expand = True)

def mainMenu ():
	window = tkinter.Tk ()
	canvas = tkinter.Canvas (window)

	conts = [
		{"type" : "Button", "text" : "Change Logo", "command" : canvas.destroy},
		{"type" : "Button", "text" : "Restore default", "command" : canvas.destroy},
		{"type" : "Button", "text" : "Convert images to icons", "command" : canvas.destroy},
		{"type" : "Button", "text" : "Help", "command" : canvas.destroy}
	]
	constructCanvas(canvas, conts)

	canvas.pack (fill = tkinter.BOTH, expand = True)
	window.mainloop ()