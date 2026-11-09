@echo off
echo ============================================================
echo   Business Plan Generator with Authentication
echo ============================================================
echo.
echo Starting application with login...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the app with login
python main_with_login.py

pause
