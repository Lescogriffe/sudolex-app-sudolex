#!/bin/bash
# Sudolex — Installation macOS
echo "======================================"
echo "  Sudolex — Installation macOS"
echo "======================================"

# Vérification Python
if ! command -v python3 &>/dev/null; then
    echo "Python 3 non trouvé. Installez-le depuis https://python.org"
    exit 1
fi

PYTHON_VER=$(python3 -c "import sys; print(sys.version_info.minor)")
if [ "$PYTHON_VER" -lt 10 ]; then
    echo "Python 3.10+ requis. Version actuelle : 3.$PYTHON_VER"
    exit 1
fi

echo "Python OK — installation des dépendances..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

# FFmpeg via Homebrew si absent
if ! command -v ffmpeg &>/dev/null; then
    echo ""
    echo "FFmpeg non trouvé (requis pour audio/vidéo)."
    if command -v brew &>/dev/null; then
        echo "Installation via Homebrew..."
        brew install ffmpeg
    else
        echo "Installez Homebrew puis relancez : /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        echo "Puis : brew install ffmpeg"
    fi
fi

echo ""
echo "Installation terminée. Lancez Sudolex avec : ./run.sh"
