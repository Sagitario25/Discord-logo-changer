import os
import subprocess

def changeEXEicon (originalPath, resultPath, iconPath):
	subprocess.run (["ResourceHacker/ResourceHacker.exe", "-open", originalPath, "-save", resultPath, "-action", "addskip", "-res", iconPath, "-mask", "ICONGROUP,MAINICON,"], capture_output = True)