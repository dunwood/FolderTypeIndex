@echo off
cd /d "%~dp0"
start "" pyw -3 folder_type_index.pyw
if errorlevel 1 start "" pythonw folder_type_index.pyw
