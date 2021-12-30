#Packages
import tkinter
import tkinter.messagebox
import tkinter.filedialog
import PIL.Image
import PIL.ImageTk
import PIL.ImageDraw
import PIL.ImageFont

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
				objects.append (DefaultWidgets.Label.text (canvas, text = i["text"]))
			elif "image" in keys:
				objects.append (DefaultWidgets.Label.image (canvas, image = i["image"]))
			objects[-1].pack (fill = i["fill"], expand = i["expand"], side = i["side"])
		elif i["type"] == "Button":
			objects.append (DefaultWidgets.Button.text (canvas, text = i["text"], command = i["command"], state = i["state"]))
			objects[-1].pack (fill = i["fill"], expand = i["expand"], side = i["side"])
		elif i["type"] == "Canvas":
			newCanvas = tkinter.Canvas (canvas)
			objects.append (constructCanvas (newCanvas, i["contents"]))
			newCanvas.pack (fill = tkinter.BOTH, expand = True)

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

class DefaultWidgets:
	class Label:
		def text (canvas, text):
			return tkinter.Label (canvas, text = text)
		def image (canvas, image):
			return tkinter.Label (canvas, image = image, border = False)
	class Button:
		def text (canvas, text, command, state):
			return tkinter.Button (canvas, text = text, command = command, state = state)
		def image ():
			pass

class prettyTkinter:
	def __init__(self, labelStyle = {}, buttonStyle = {}):
		self.labelStyle = labelStyle
		self.buttonStyle = buttonStyle

	def sustituteLabelStyle (self, labelStyle):
		self.labelStyle = labelStyle
	def sustituteButtonStyle (self, buttonStyle):
		self.buttonStyle = buttonStyle

	def createImage (self, canvas, text, textColor, imgSize, color, fontName, fontSize):
		self.image = PIL.Image.new (mode = "RGB", size = imgSize, color = color)
		self.draw = PIL.ImageDraw.Draw (self.image)
		self.font = PIL.ImageFont.truetype (font = fontName, size = fontSize)
		self.textsize = self.draw.textsize (text, self.font)
		self.draw.text (((imgSize[0] - self.textsize[0]) / 2, (imgSize[1] - self.textsize[1]) / 2), text, textColor, self.font)
		return PIL.ImageTk.PhotoImage (self.image, master = canvas)

	def applyStyles (self, canvas, objects):
		self.contents = []
		for i in objects:
			if type (i) == type ([]):
				self.applyStyles (canvas, i)
			elif type (i) == type (tkinter.Label ()):
				i.master.update_idletasks ()
				self.text = i.cget ("text")
				self.size = (i.winfo_width (), i.winfo_height ())

				self.img = self.createImage (canvas, self.text, self.labelStyle["textColor"], self.size, self.labelStyle["backgroundColor"], self.labelStyle["font"], self.labelStyle["fontSize"])
				self.contents.append ({"type" : "Label", "image" : self.img})
			elif type (i) == type (tkinter.Button ()):
				i.master.update_idletasks ()
				self.text = i.cget ("text")
				self.size = (i.winfo_width (), i.winfo_height ())
		constructCanvas (canvas, self.contents)