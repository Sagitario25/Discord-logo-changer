#Packages
import sys
import shutil
import os

sys.argv.append ("py2exe")#Auto call py2exe

if os.path.exists ("dist"):#Remove previous build
	shutil.rmtree ("dist")

os.system ('pyinstaller --noconfirm --onefile --windowed --icon "D:/Informatica/Python/Discord/app.ico" --name "Discord Logo Changer"  "D:/Informatica/Python/Discord/main.py"')

shutil.rmtree ("build")
os.remove ("Discord Logo Changer.spec")

shutil.copy ("tool.exe", "dist/tool.exe")#Copy resource hacker
shutil.copy ("app.ico", "dist/app.ico")#Copy resource hacker
shutil.copytree ("Icons", "dist/Icons")#Copy default icons