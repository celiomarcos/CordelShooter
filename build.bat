@echo off
REM ===================================================================
REM  Cordel Shooter - Script de build para Windows
REM  Gera o executavel (.exe), copia os assets e cria o ZIP de entrega.
REM  Requisitos: Python 3.10+ instalado e no PATH.
REM  Uso: clique duas vezes neste arquivo ou rode "build.bat" no CMD.
REM ===================================================================
setlocal
cd /d "%~dp0"

echo.
echo [1/6] Criando ambiente virtual...
if not exist ".venv" (
    python -m venv .venv
)
call .venv\Scripts\activate.bat

echo.
echo [2/6] Instalando dependencias (pygame e pyinstaller)...
python -m pip install --upgrade pip >nul
python -m pip install pygame==2.6.0 pyinstaller

echo.
echo [3/6] Gerando os assets PNG...
python tools\gen_assets.py

echo.
echo [4/6] Compilando o executavel com PyInstaller...
pyinstaller --noconfirm --onefile --windowed --name CordelShooter ^
    --add-data "src;src" --add-data "tools;tools" main.py

echo.
echo [5/6] Montando a pasta de distribuicao (exe + assets)...
set OUT=dist\CordelShooter_entrega
if exist "%OUT%" rmdir /s /q "%OUT%"
mkdir "%OUT%"
copy /y dist\CordelShooter.exe "%OUT%\" >nul
xcopy /e /i /y asset "%OUT%\asset" >nul

echo.
echo [6/6] Gerando o ZIP de entrega...
powershell -Command "Compress-Archive -Path '%OUT%\*' -DestinationPath 'dist\CordelShooter_entrega.zip' -Force"

echo.
echo ===================================================================
echo  Pronto!
echo  - Executavel: %OUT%\CordelShooter.exe
echo  - ZIP de entrega: dist\CordelShooter_entrega.zip
echo ===================================================================
echo.
pause
