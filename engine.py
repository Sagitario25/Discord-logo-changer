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
	objects = []
	for i in contents:
		keys = [j for j in i]
		
		if i["type"] == "Label":
			if "text" in keys:
				objects.append (tkinter.Label (canvas, text = i["text"]))
			elif "image" in keys:
				objects.append (tkinter.Label (canvas, image = i["image"], border = False))
			objects[-1].pack (fill = i["fill"], expand = i["expand"], side = i["side"])
		elif i["type"] == "Button":
			objects.append (tkinter.Button (canvas, text = i["text"], command = i["command"], state = i["state"]))
			objects[-1].pack (fill = i["fill"], expand = i["expand"], side = i["side"])
		elif i["type"] == "Canvas":
			newCanvas = tkinter.Canvas (canvas)
			objects.append (constructCanvas (newCanvas, i["contents"]))
			newCanvas.pack (fill = tkinter.BOTH, expand = True)
	prettyTkinter ().applyStyles (objects)
	return objects

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
	window.minsize (size[0], size[1])
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

class prettyTkinter:
	def __init__(self, labelStyle = {}, buttonStyle = {}):
		self.labelStyle = labelStyle
		self.buttonStyle = buttonStyle

	def sustituteLabelStyle (self, labelStyle):
		self.labelStyle = labelStyle
	def sustituteButtonStyle (self, buttonStyle):
		self.buttonStyle = buttonStyle

	def applyStyles (self, objects):
		for i in objects:
			if type (i) == type ([]):
				self.applyStyles (i)
			elif type (i) == type (tkinter.Label ()):
				i.master.update_idletasks ()
				self.text = i.cget ("text")
				self.size = (i.winfo_width (), i.winfo_height ())
			elif type (i) == type (tkinter.Button ()):
				pass#Process buttons