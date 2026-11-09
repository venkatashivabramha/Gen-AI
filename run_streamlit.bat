@echo off
echo ===============================================
echo   Business Plan Generator - Web Version
echo   Quick Start Script
echo ===============================================
echo.

echo Step 1: Installing dependencies...
pip install streamlit pymongo bcrypt

echo.
echo Step 2: Testing imports...
python test_streamlit.py

echo.
echo ===============================================
echo   NEXT STEPS:
echo ===============================================
echo.
echo 1. Set up MongoDB Atlas (FREE):
echo    https://www.mongodb.com/cloud/atlas
echo.
echo 2. Configure secrets:
echo    Copy .streamlit\secrets.toml.example to .streamlit\secrets.toml
echo    Add your MongoDB URI and API keys
echo.
echo 3. Run the web app:
echo    streamlit run streamlit_app.py
echo.
echo 4. Deploy to Streamlit Cloud:
echo    https://streamlit.io/cloud
echo.
echo For detailed guide, see: STREAMLIT_DEPLOYMENT.md
echo.
pause
