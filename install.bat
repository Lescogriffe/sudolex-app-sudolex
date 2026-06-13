@echo off
echo ================================================
echo   FileAnalyzer AI - Installation Windows
echo   (Version LM Studio)
echo ================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH.
    echo Telechargez Python 3.11+ sur https://python.org
    pause
    exit /b 1
)

echo [1/2] Mise a jour de pip...
python -m pip install --upgrade pip --quiet

echo [2/2] Installation des dependances Python...
echo      (easyocr + PyTorch : ~2 Go au premier telechargement)
echo      Patience, cela peut prendre plusieurs minutes...
echo.
pip install -r requirements.txt

echo.
echo ================================================
echo   Installation terminee !
echo.
echo   Assurez-vous que LM Studio est demarre et
echo   qu'un modele est charge avec le serveur local
echo   actif (http://localhost:1234).
echo.
echo   Lancez l'application avec run.bat
echo ================================================
echo.
pause
