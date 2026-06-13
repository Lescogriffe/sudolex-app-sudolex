@echo off
setlocal enabledelayedexpansion

echo ================================================
echo   FileAnalyzer AI — Build PyInstaller
echo ================================================
echo.

REM ── Vérifications préalables ────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python introuvable dans le PATH.
    pause & exit /b 1
)

pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] PyInstaller non detecte — installation...
    pip install pyinstaller
    if errorlevel 1 (
        echo [ERREUR] Echec installation PyInstaller.
        pause & exit /b 1
    )
)

if not exist "main.py" (
    echo [ERREUR] main.py introuvable.
    echo          Lancez build.bat depuis le dossier du projet.
    pause & exit /b 1
)

if not exist "ffmpeg.exe" (
    echo [ATTENTION] ffmpeg.exe introuvable dans ce dossier.
    echo             La transcription audio/video ne fonctionnera pas dans l'exe.
    echo             Appuyez sur une touche pour continuer quand meme, ou fermez pour annuler.
    pause
)

REM ── Nettoyage des anciens builds ────────────────
echo [1/4] Nettoyage des anciens builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
echo      OK

REM ── UPX (optionnel — réduit la taille) ─────────
echo [2/4] Verification UPX (compression)...
upx --version >nul 2>&1
if errorlevel 1 (
    echo      UPX non installe — build sans compression.
    echo      Pour l'installer : https://github.com/upx/upx/releases
) else (
    echo      UPX detecte — compression activee.
)

REM ── Build ────────────────────────────────────────
echo [3/4] Lancement du build (peut prendre 5-15 minutes)...
echo       Soyez patient, PyTorch et EasyOCR sont volumineux.
echo.

pyinstaller fileanalyzer.spec

if errorlevel 1 (
    echo.
    echo [ERREUR] Le build a echoue.
    echo          Lisez les messages ci-dessus pour identifier le probleme.
    echo          Conseil : verifiez que toutes les dependances sont installees
    echo          avec :  pip install -r requirements.txt
    pause & exit /b 1
)

REM ── Résultat ─────────────────────────────────────
echo.
echo [4/4] Verification du resultat...
if exist "dist\FileAnalyzer AI\FileAnalyzer AI.exe" (
    echo.
    echo ================================================
    echo   BUILD REUSSI !
    echo.
    echo   Executable : dist\FileAnalyzer AI\FileAnalyzer AI.exe
    echo.
    echo   Pour distribuer l'application, zippez le
    echo   dossier complet :  dist\FileAnalyzer AI\
    echo.
    echo   RAPPEL : l'utilisateur doit avoir installe
    echo   LM Studio separement (https://lmstudio.ai)
    echo ================================================
) else (
    echo [ATTENTION] L'exe n'est pas ou attendu.
    echo             Verifiez le dossier dist\
)

echo.
pause
