@echo off
chcp 65001 >nul
echo ====================================
echo   Sistema de Adega - Trocar Tema
echo ====================================
echo.
echo Tema atual configurado no arquivo .streamlit\config.toml
echo.
echo Escolha uma opção:
echo.
echo [1] Ativar Tema ESCURO
echo [2] Ativar Tema CLARO
echo [3] Sair
echo.
set /p opcao="Digite 1, 2 ou 3: "

if "%opcao%"=="1" goto dark
if "%opcao%"=="2" goto light
if "%opcao%"=="3" goto end

echo Opção inválida!
goto end

:dark
echo.
echo Ativando tema ESCURO...
copy /Y ".streamlit\config_dark.toml" ".streamlit\config.toml" >nul
echo ✓ Tema ESCURO ativado!
echo.
echo IMPORTANTE: Feche e reabra o navegador (ou pressione Ctrl+F5)
echo para aplicar o novo tema.
goto end

:light
echo.
echo Ativando tema CLARO...
copy /Y ".streamlit\config_light_backup.toml" ".streamlit\config.toml" >nul
echo ✓ Tema CLARO ativado!
echo.
echo IMPORTANTE: Feche e reabra o navegador (ou pressione Ctrl+F5)
echo para aplicar o novo tema.
goto end

:end
echo.
pause
