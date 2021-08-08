class Interpreter:
	def __init__ (self):
		self.commands = {}
		#Predefined commands
		self.addCommand ("listCommands", self.listCommands)
		
	def call (self, raw_command):
		if type (raw_command) != type (""): raise TypeError ("Input has to be a string")#Only string inputs
		self.raw = delSpaces (raw_command)#Interiorize the command
		self.getArgs ()
		self.callCommand ()
			
	def getArgs (self):
		self.args = []
		self.raw += " fakeArg"#Add fake arg
		while True:
			#When there is only 1 arg left, an error will occur and fake arg wont be added
			try:
				self.arg, self.raw = getArg (self.raw)#Take next arg
				self.args.append (self.arg)#Append new arg to the list
				self.raw = delSpaces (self.raw)#Clean remanents
			except:
				break
	
	def callCommand (self):
		self.command = None
		try:
			self.command = self.commands [self.args [0]]#Asign the command
			try:
				self.returned = self.command (*self.args[1:])#Call the command and pass the arguments
				if type (self.returned) == type (None):
					pass
				elif type (self.returned) == type ([]):
					for i in self.returned: print (i)
				else:
					print (self.returned)
			except Exception as inst:
				print (inst)
		except Exception as inst:
			print (inst)
			print ("Usually this is caused because you didnt import that command")

	def addCommand (self, name, function):
		self.commands [name] = function#Add comand to the list

	def listCommands (self):
		return [(i, self.commands [i]) for i in self.commands]


def getArg (string):
	if string [0] == '"':#If the next arg is between "
		arg = string [1:string [1:].index ('"') + 1]
		return arg, string [len (arg) + 2:]
	else:#If the next arg isn't between "
		arg = string [:string [:].index (' ')]
		return arg, string [len (arg):]

def delSpaces (string):#Delete spaces on both sides of a string
	string = delStart (string)#Clean beggining
	string = delStart (string [::-1])#Cleaning the beggining fo the reverse, aka: the end
	return string[::-1]#Return and reverse again

def delStart (string):#Deletes spaces on the beggining of a string
	for i in range (len (string)):#Iterate the input
		if not string [i] == " ":#If its not a space,
			return string [i:]#return whats left