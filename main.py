import gestor
import command

com = command.Interpreter ()

com.addCommand("getNames", gestor.getNames)
com.addCommand("restore", gestor.callRestore)
com.addCommand("change", gestor.callChange)