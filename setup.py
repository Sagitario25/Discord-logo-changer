from distutils.core import setup
import py2exe
import sys
import shutil
import os

sys.argv.append ("py2exe")#Auto call py2exe

if os.path.exists ("dist"):#Remove previous build
	shutil.rmtree ("dist")

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    console = [{
		"script" : "main.py",
		"icon_resources" : [(0, "app.ico")]
	}],
    zipfile = None,
)

shutil.copy ("tool.exe", "dist/tool.exe")#Copy resource hacker
shutil.copytree ("Icons", "dist/Icons")#Copy default icons
os.rename ("dist/main.exe", "dist/Discord Logo Changer.exe")#Rename executable