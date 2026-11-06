@echo off
echo ========================================
echo   Business Plan Generator
echo   Starting Application...
echo ========================================
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo Virtual environment not found, using system Python
)

echo.
echo Starting Business Plan Generator...
echo.

REM Run the application
python src/main.py

pause
