import gestor
import command

com = command.Interpreter ()

com.addCommand("getNames", gestor.getNames ())