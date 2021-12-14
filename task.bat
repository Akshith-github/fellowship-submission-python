@echo off

@REM python3 task.py %1 %2 %3

@REM get the path to current script in variable batpath and append "task.py"
set batpath=%~dp0 
@REM remove the spaces at the end of the path
set batpath=%batpath:~0,-1%
@REM add "task.py" to the path
set pythonfilepath=%batpath%task.py
@REM echo "python3 %batpath% %1 %2 %3"


python3 "%pythonfilepath%" %1 %2 %3