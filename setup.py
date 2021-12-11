#Modules
import gestor

#Packages
import sys
import shutil
import os


if os.path.exists ("Discord Logo Changer"):#Remove previous build
	shutil.rmtree ("Discord Logo Changer")

os.system ('pyinstaller --noconfirm --onefile --windowed --icon "D:/Informatica/Python/Discord/app.ico" --name "Discord Logo Changer"  "D:/Informatica/Python/Discord/main.py"')

shutil.rmtree ("build")
os.remove ("Discord Logo Changer.spec")

shutil.copy ("tool.exe", "dist/tool.exe")#Copy resource hacker
shutil.copy ("app.ico", "dist/app.ico")#Copy resource hacker
shutil.copytree (gestor.iconsPath, os.path.join ("dist", gestor.iconsPath))#Copy default icons
shutil.copytree (gestor.fontsPath, os.path.join ("dist", gestor.fontsPath))#Copy default icons

os.rename ("dist", "Discord Logo Changer")