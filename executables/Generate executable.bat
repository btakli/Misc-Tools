@ECHO off

ECHO [42m~~~~~~~~Generating EXEs~~~~~~[0m
ECHO [42m~~~~Generating EXE for GUI version~~~~[0m
pyinstaller --onefile "../source code/MasterTool (GUI).spec"
move /y ".\dist\MasterTool (GUI).exe" .\

ECHO [42m~~~~Generating EXE for CLI version~~~~[0m
pyinstaller --onefile "../source code/MasterTool.spec"
move /y ".\dist\MasterTool.exe" .\

ECHO [42m~~~~Done!~~~~[0m
PAUSE

