# Changelog — Sudolex

Toutes les versions notables sont documentées ici.  
Format : [version] - date · description

---

## [1.0.0] - 2026-06-12 · Première version publique

### Analyse de documents
- Analyse séquentielle complète : transcription Whisper → résumé → analyse approfondie → synthèse globale
- OCR automatique pour les PDF scannés (EasyOCR)
- Vue cumulative scrollable pendant l'analyse batch
- Extraction texte : PDF, Word, Excel, TXT, CSV, Markdown

### Intelligence Artificielle
- Moteur LM Studio (détection automatique au démarrage)
- Moteur llama.cpp intégré (fallback avec téléchargement auto du modèle)
- 10 domaines juridiques avec prompts experts à 4 niveaux d'analyse
- Prompts multilingues (FR, EN, NL, ES, DE, IT, PT, AR, ZH)
- Q&R conversationnel avec historique sur tout le dossier

### Interface
- Design dark premium / light classic avec toggle
- Logo Sudolex coordonné selon le thème
- Intervenants du dossier (ancrage des identités dans les prompts)
- Contexte / Instructions libre pour l'IA
- Annulation de l'analyse en cours (interruption HTTP + flags)

### Système
- Mise à jour automatique via GitHub Releases
- Filtrage automatique des fichiers fantômes macOS (`._*`)
- Cache Whisper global (rechargement unique)
- Retry automatique sur ConnectionError LM Studio (backoff 3s/6s)
- Export TXT complet (contenu + résumés + analyses + Q&R)

---

## À venir

### [1.1.0] — Export PDF/Word formaté
### [1.2.0] — Compatibilité macOS (.dmg)
### [2.0.0] — Version Pro (multi-dossiers, dataset LoRA, API)
