#Packages
import tkinter
import tkinter.messagebox
import tkinter.filedialog
import PIL.Image
import PIL.ImageTk

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
		keys = [j for j in i]
		if   i["type"] == "Label":
			if "text" in keys:
				tkinter.Label (canvas, text = i["text"]).pack (fill = i["fill"], expand = i["expand"], side = i["side"])
			elif "image" in keys:
				tkinter.Label (canvas, image = i["image"]).pack (fill = i["fill"], expand = i["expand"], side = i["side"])
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

def warnedAction (action, warnWindow = lambda: tkinter.messagebox.askokcancel ("Warning", "To complete the action discord is going to close, are you sure?")):
	confirm = warnWindow ()
	if confirm:
		try:
			action ()
		except Exception as e:
			tkinter.messagebox.showerror (title = "Error", message = f"The next error ocurred while completing the action\n{e}")
	else:
		tkinter.messagebox.showinfo (title = "Action cancelled", message = "The change was cancelled, going back to menu.")

def previewImage (path, size = (256, 256)):
	window = createWindow ()#Start window
	window.resizable (width = False, height = False)
	window.title ("Preview")#Modify this to change the title
	rawimg = PIL.Image.open(path)#Open image path

	if size != (256, 256):#If a specific resolution has been requested
		rawimg = rawimg.resize (size)#Change the image resolution

	img = PIL.ImageTk.PhotoImage(rawimg, master = window)#Adapt the image to tkinter
	data = [{"type" : "Label", "image" : img}]
	constructCanvas (window, data)

	window.mainloop ()

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