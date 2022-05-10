@ECHO off

ECHO ~~~~~~~~Generating EXEs~~~~~~

ECHO ~~~~Generating EXE for GUI version~~~~
pyinstaller --onefile "../source code/MasterTool (GUI).spec"
move /y ".\dist\MasterTool (GUI).exe" .\

ECHO ~Generating EXE for CLI version~
pyinstaller --onefile "../source code/MasterTool.spec"
move /y ".\dist\MasterTool.exe" .\

