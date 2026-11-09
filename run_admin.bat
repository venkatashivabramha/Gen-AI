@echo off
echo ========================================
echo   Business Plan Generator - ADMIN
echo ========================================
echo.

REM Activate virtual environment
call .\venv\Scripts\activate.bat

REM Run admin dashboard
python admin_dashboard.py

pause
