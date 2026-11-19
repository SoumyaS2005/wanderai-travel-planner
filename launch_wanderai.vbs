
Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")

projectFolder = FSO.GetParentFolderName(WScript.ScriptFullName)
pythonPath = projectFolder & "\.venv\Scripts\pythonw.exe"
appPath = projectFolder & "\.venv\Scripts\streamlit.exe"

WshShell.CurrentDirectory = projectFolder

If Not FSO.FileExists(pythonPath) Then
    MsgBox "Python launcher not found. Check your .venv folder.", 16, "WanderAI"
    WScript.Quit
End If

If Not FSO.FileExists(appPath) Then
    MsgBox "Streamlit was not found. Check your project environment.", 16, "WanderAI"
    WScript.Quit
End If

WshShell.Run """" & pythonPath & """ -m streamlit run """ & projectFolder & "\app.py""", 0, False

WScript.Sleep 2500
WshShell.Run "http://localhost:8501", 1, False
