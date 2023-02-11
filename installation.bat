@echo off
cls

set installer_name=pyinstaller

echo Now installing python3.10.9 for 64 bit Windows, please complete the setup process.
curl https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe --ssl-no-revoke -o %installer_name%.exe 
start %installer_name%.exe
echo Now installing pygame-pacman...
git clone https://github.com/atif5/pygame-pacman

echo py -m pip install pygame numpy > play.bat
echo cd pygame-pacman >> play.bat
echo py -m pacman >> play.bat