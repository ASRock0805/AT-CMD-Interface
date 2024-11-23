@ECHO OFF

TITLE Start AT Interface

REM This batch script starts the AT Command Interface Python application.
REM It checks for the Python installation and then executes the 'at_cmd_interface.py' file.
REM Author: Starke Wang

REM Check if Python is installed and in the PATH.
python --version > NUL 2>&1
IF %ERRORLEVEL% == 0 (
  REM If Python is found, check if the script exists.
  IF EXIST "at_cmd_interface.py" (
    REM Execute the Python script.
    python "at_cmd_interface.py"
  ) ELSE (
    ECHO Error: Python script 'at_cmd_interface.py' not found.
  )
) ELSE (
  ECHO Error: Python installation not found. 
  ECHO Please install Python and ensure it is added to your PATH environment variable.
)

PAUSE