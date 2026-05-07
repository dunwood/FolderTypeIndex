@echo off
cd /d "%~dp0"
py -3 folder_type_index.py
if errorlevel 1 python folder_type_index.py
pause
