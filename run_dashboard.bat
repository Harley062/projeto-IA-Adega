@echo off
echo.
echo ========================================
echo   Sistema de Analise - Adega
echo   Iniciando Dashboard Web...
echo ========================================
echo.

REM Ativar ambiente virtual
call venv\Scripts\activate.bat

REM Iniciar Streamlit
streamlit run app.py

pause
