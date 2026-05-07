Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
folder = fso.GetParentFolderName(WScript.ScriptFullName)
shell.CurrentDirectory = folder
cmd = "cmd /c ""cd /d """"" & folder & """"" && (pyw -3 folder_type_index.pyw || pythonw folder_type_index.pyw || python folder_type_index.py)"""
shell.Run cmd, 0, False
