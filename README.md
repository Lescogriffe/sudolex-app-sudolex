# Sudolex
**Intelligence documentaire locale** — Analyse de documents juridiques par IA locale

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Plateforme](https://img.shields.io/badge/plateforme-Windows%20%7C%20macOS-lightgrey)
![Licence](https://img.shields.io/badge/licence-Source%20Available-orange)

---

## Présentation

Sudolex analyse vos documents juridiques localement, sans envoyer aucune donnée dans le cloud.  
Audio, vidéo, PDF, Word, Excel — tout est transcrit et analysé par l'IA directement sur votre machine.

**Fonctionnalités :**
- Transcription audio/vidéo via Whisper (local)
- OCR automatique pour les PDF scannés
- Analyse séquentielle : résumé → analyse approfondie → synthèse globale
- 10 domaines juridiques avec prompts experts (Famille, Pénal, Immobilier…)
- Intervenants du dossier pour ancrer les identités
- Q&R conversationnel sur tout le dossier analysé
- Vue cumulative scrollable pendant l'analyse
- Thème sombre premium / clair classique
- Mise à jour automatique via GitHub

---

## Installation rapide

### Windows

1. Téléchargez la dernière [release](../../releases/latest)
2. Extrayez le dossier
3. Double-cliquez sur `install.bat`
4. Lancez avec `run.bat`

### macOS

```bash
# Téléchargez et extrayez la release, puis :
chmod +x install.sh && ./install.sh
./run.sh
```

---

## Prérequis

- **Python 3.10+** — [python.org](https://www.python.org/downloads/)
- **LM Studio** (recommandé) — [lmstudio.ai](https://lmstudio.ai)  
  *ou* modèle llama.cpp téléchargé automatiquement au premier lancement
- **FFmpeg** — pour les fichiers audio/vidéo
  - Windows : inclus dans le dossier `ffmpeg.exe`
  - macOS : `brew install ffmpeg`

---

## Moteurs IA supportés

| Moteur | Description |
|--------|-------------|
| **LM Studio** | Recommandé — interface graphique, tous modèles |
| **llama.cpp intégré** | Fallback automatique — téléchargement du modèle au premier lancement |

**Modèles recommandés :** deepseek-r1, Qwen 2.5 7B, Mistral 7B, Phi-3.5 Mini

---

## Structure du projet

```
sudolex/
├── main.py                      # Application principale
├── requirements.txt             # Dépendances Python
├── install.bat                  # Installation Windows
├── run.bat                      # Lancement Windows
├── install.sh                   # Installation macOS
├── run.sh                       # Lancement macOS
├── ffmpeg.exe                   # FFmpeg Windows (inclus)
├── sudolex_logo_white.png       # Logo thème sombre
├── sudolex_logo_black.png       # Logo thème clair
└── models/                      # Modèles GGUF (créé automatiquement)
```

---

## Licence

**Source Available** — Usage personnel gratuit.  
Usage commercial interdit sans accord écrit préalable.  
© 2026 Sudolex · sudolex.com
