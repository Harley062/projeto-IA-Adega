@echo off
cls
echo.
echo ========================================
echo   SISTEMA DE ANALISE DA ADEGA
echo   Versao 1.0 - Pronto para Producao
echo ========================================
echo.
echo Verificando ambiente...
echo.

REM Verificar se o ambiente virtual existe
if not exist "venv\" (
    echo ERRO: Ambiente virtual nao encontrado!
    echo.
    echo Execute primeiro:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Ativar ambiente virtual
echo [1/3] Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Verificar se os dados existem
if not exist "data\Cliente.csv" (
    echo.
    echo AVISO: Arquivos de dados nao encontrados na pasta 'data\'
    echo O sistema vai iniciar, mas voce precisara processar os dados.
    echo.
    timeout /t 3 >nul
)

REM Criar pastas de output se não existirem
echo [2/3] Preparando diretorios de saida...
if not exist "output" mkdir output
if not exist "output\models" mkdir output\models
if not exist "output\plots" mkdir output\plots
if not exist "output\reports" mkdir output\reports
if not exist "logs" mkdir logs

REM Iniciar dashboard
echo [3/3] Iniciando dashboard web...
echo.
echo ========================================
echo   Dashboard disponivel em:
echo   http://localhost:8501
echo ========================================
echo.
echo Pressione Ctrl+C para encerrar
echo.

streamlit run app.py

pause
