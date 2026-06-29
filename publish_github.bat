@echo off
REM ===================================================================
REM  Inicializa o repositorio git nesta pasta e publica no GitHub.
REM  Rode este arquivo de dentro de D:\projs\CordelShooter.
REM  Requisitos: git e GitHub CLI (gh). Faca login antes:  gh auth login
REM ===================================================================
setlocal
cd /d "%~dp0"
set REPO=CordelShooter

echo.
echo [0/5] Verificando ferramentas...
where git >nul 2>&1 || (echo ERRO: git nao encontrado no PATH. & pause & exit /b 1)
where gh  >nul 2>&1 || (echo ERRO: GitHub CLI ^(gh^) nao encontrado no PATH. & pause & exit /b 1)

if exist ".git" (
    echo AVISO: ja existe um repositorio .git aqui. Pulando o git init.
) else (
    echo.
    echo [1/5] Inicializando o repositorio git...
    git init -b main 2>nul || (git init & git branch -M main)
)

REM identidade local (fallback, caso o git global nao esteja configurado)
git config user.email >nul 2>&1 || git config user.email "celiomarcos@gmail.com"
git config user.name  >nul 2>&1 || git config user.name  "Celio Marcos"

echo.
echo [2/5] Adicionando arquivos e criando o commit...
git add .
git commit -m "Cordel Shooter - demo de jogo 2D em Python/Pygame" 2>nul

echo.
echo [3/5] Criando o repositorio no GitHub e publicando...
gh repo create %REPO% --public --source=. --remote=origin --push
if errorlevel 1 (
    echo.
    echo AVISO: o gh nao concluiu. Causas comuns:
    echo   - Nao esta logado:  rode  gh auth login  e tente de novo.
    echo   - O repo %REPO% ja existe na sua conta. Nesse caso rode:
    echo       git remote add origin https://github.com/SEU_USUARIO/%REPO%.git
    echo       git push -u origin main
    pause
    exit /b 1
)

echo.
echo [4/5] Remotos configurados:
git remote -v

echo.
echo [5/5] Concluido! Repositorio publicado: %REPO% ^(publico^)
echo.
pause
