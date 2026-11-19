
@echo off
cd /d "%~dp0"

if not defined GEMINI_API_KEY (
    echo Gemini API key is not set in this window.
    echo Please set your key before starting WanderAI.
    pause
    exit /b 1
)

start "" http://localhost:8501
.venv\Scripts\python.exe -m streamlit run app.py

pause
