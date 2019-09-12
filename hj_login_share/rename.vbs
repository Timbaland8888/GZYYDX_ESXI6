Set oShell=CreateObject("Shell.Application")
oShell.NameSpace("u:\").Self.Name=WScript.Arguments(0)
