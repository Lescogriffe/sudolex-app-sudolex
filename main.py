#!/usr/bin/env python3
"""
Sudolex — Intelligence documentaire locale
Analyse de documents juridiques par IA locale · sudolex.com
"""
import sys, json, subprocess
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# ── Version & repo GitHub ─────────────────────────────────────────────────────
APP_VERSION = "1.0.0"
GITHUB_REPO = "Lescogriffe/sudolex-app-sudolex"   # ← mettre à jour avec ton vrai repo

# ── Palette Dark Premium ─────────────────────────────────────────────────────
BG      = "#0D1117"; SURFACE = "#161B22"; CARD = "#21262D"
ACCENT  = "#2563EB"; ACCENT2 = "#1D4ED8"; ACCENT3 = "#60A5FA"
TEXT    = "#E6EDF3"; TDIM    = "#8B949E"
OK      = "#3FB950"; WARN = "#F0A030"; ERR = "#F85149"; BORDER = "#30363D"

# Palette Light Classic
LIGHT = {
    "BG":"#F0F4F8","SURFACE":"#FFFFFF","CARD":"#E8EEF5",
    "ACCENT":"#2563EB","ACCENT2":"#1D4ED8","ACCENT3":"#3B82F6",
    "TEXT":"#1A202C","TDIM":"#718096",
    "OK":"#38A169","WARN":"#C05621","ERR":"#C53030","BORDER":"#CBD5E0",
}

def build_style(t):
    """Construit le stylesheet complet depuis un dictionnaire de couleurs."""
    A,A2,A3 = t["ACCENT"],t["ACCENT2"],t["ACCENT3"]
    BG_,S,C,TX,TD,BO = t["BG"],t["SURFACE"],t["CARD"],t["TEXT"],t["TDIM"],t["BORDER"]
    E = t["ERR"]
    return f"""
QMainWindow,QWidget{{background:{BG_};color:{TX};
    font-family:'Segoe UI','SF Pro Display','Helvetica Neue',Arial,sans-serif;font-size:13px;}}
QSplitter::handle{{background:{BO};width:1px;}}
QScrollArea{{border:none;background:transparent;}}
QScrollBar:vertical{{background:transparent;width:6px;border-radius:3px;margin:0;}}
QScrollBar::handle:vertical{{background:{BO};border-radius:3px;min-height:30px;}}
QScrollBar::handle:vertical:hover{{background:{TD};}}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{{height:0px;}}
QScrollBar:horizontal{{background:transparent;height:6px;border-radius:3px;}}
QScrollBar::handle:horizontal{{background:{BO};border-radius:3px;}}
QPushButton{{
    background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 {A3},stop:1 {A});
    color:white;border:none;border-radius:8px;
    padding:9px 20px;font-size:13px;font-weight:600;
}}
QPushButton:hover{{
    background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #93C5FD,stop:1 {A3});
}}
QPushButton:pressed{{background:{A2};padding-top:10px;padding-bottom:8px;}}
QPushButton:disabled{{background:{C};color:{TD};border:1px solid {BO};}}
QPushButton#secondary{{
    background:{C};color:{TX};
    border:1px solid {BO};border-radius:8px;
}}
QPushButton#secondary:hover{{background:{S};border-color:{TD};}}
QPushButton#danger{{
    background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #FC8181,stop:1 {E});
    color:white;border:none;border-radius:8px;
}}
QPushButton#danger:hover{{
    background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #FEB2B2,stop:1 #FC8181);
}}
QTextEdit{{
    background:{S};border:1px solid {BO};border-radius:8px;
    padding:12px;color:{TX};font-size:13px;
}}
QTextEdit:focus{{border-color:{A};}}
QTabWidget::pane{{border:1px solid {BO};border-radius:10px;background:{S};top:-1px;}}
QTabBar::tab{{
    background:transparent;color:{TD};
    padding:8px 18px;border-radius:6px;margin-right:2px;
    font-weight:500;font-size:12px;
}}
QTabBar::tab:selected{{background:{A};color:white;font-weight:600;}}
QTabBar::tab:hover:!selected{{background:{C};color:{TX};}}
QComboBox{{
    background:{S};border:1px solid {BO};border-radius:8px;
    padding:7px 12px;color:{TX};font-size:13px;
}}
QComboBox:hover{{border-color:{A};}}
QComboBox QAbstractItemView{{
    background:{C};border:1px solid {BO};border-radius:6px;
    selection-background-color:{A};padding:4px;
}}
QProgressBar{{background:{C};border:none;border-radius:3px;height:4px;}}
QProgressBar::chunk{{
    background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {A},stop:1 {A3});
    border-radius:3px;
}}
QGroupBox{{
    border:1px solid {BO};border-radius:10px;margin-top:16px;
    padding:14px;color:{TX};font-weight:600;
}}
QGroupBox::title{{subcontrol-origin:margin;left:12px;padding:0 6px;color:{A3};}}
QLabel#h1{{font-size:22px;font-weight:700;}}
QLabel#h2{{font-size:14px;font-weight:700;}}
QLabel#dim{{color:{TD};font-size:11px;}}
QLineEdit{{
    background:{S};border:1px solid {BO};border-radius:8px;
    padding:8px 12px;color:{TX};font-size:13px;
}}
QLineEdit:focus{{border-color:{A};}}
QRadioButton{{color:{TX};spacing:10px;font-size:12px;font-weight:500;}}
QRadioButton::indicator{{
    width:16px;height:16px;border-radius:8px;border:2px solid {BO};background:{S};
}}
QRadioButton::indicator:checked{{background:{A};border-color:{A};}}
QToolTip{{
    background:{C};color:{TX};border:1px solid {BO};
    border-radius:6px;padding:6px 10px;font-size:12px;
}}
"""

STYLE = build_style({
    "BG":BG,"SURFACE":SURFACE,"CARD":CARD,
    "ACCENT":ACCENT,"ACCENT2":ACCENT2,"ACCENT3":ACCENT3,
    "TEXT":TEXT,"TDIM":TDIM,"OK":OK,"WARN":WARN,"ERR":ERR,"BORDER":BORDER,
})

# ── Vérificateur de mise à jour GitHub ───────────────────────────────────────
class UpdateCheckerWorker(QThread):
    """Vérifie silencieusement si une nouvelle version est disponible sur GitHub."""
    update_available = pyqtSignal(str, str)  # (version, url_release)

    def run(self):
        try:
            import requests
            r = requests.get(
                f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest",
                timeout=5,
                headers={"Accept": "application/vnd.github.v3+json",
                         "User-Agent": f"Sudolex/{APP_VERSION}"}
            )
            if r.status_code != 200:
                return
            data    = r.json()
            latest  = data.get('tag_name', '').lstrip('v')
            url     = data.get('html_url', '')
            if latest and url and self._is_newer(latest):
                self.update_available.emit(latest, url)
        except Exception:
            pass   # silencieux — pas de connexion, timeout, etc.

    @staticmethod
    def _is_newer(latest: str) -> bool:
        def parse(v):
            try: return tuple(int(x) for x in v.strip().split('.'))
            except: return (0,)
        return parse(latest) > parse(APP_VERSION)

# ── Types fichiers ──────────────────────────────────────────────────────────
VIDEO_EXT = {'.mp4','.mkv','.avi','.mov','.wmv','.flv','.webm','.m4v','.ts'}
AUDIO_EXT = {'.mp3','.wav','.m4a','.flac','.ogg','.aac','.wma','.opus'}
DOC_EXT   = {'.pdf','.docx','.xlsx','.xls','.txt','.md','.csv','.rtf','.pptx'}
ICONS     = {'video':'🎬','audio':'🎵','document':'📄','unknown':'📁'}

# ── Détection moteur IA ──────────────────────────────────────────────────────
def detect_lmstudio():
    """Retourne True si LM Studio répond sur localhost:1234."""
    try:
        import requests
        r = requests.get("http://localhost:1234/v1/models", timeout=3)
        return r.status_code == 200
    except Exception:
        return False

# ── Catalogue modèles llama.cpp ──────────────────────────────────────────────
LLAMACPP_MODELS = [
    {
        'id':       'phi35-mini',
        'name':     'Phi-3.5 Mini — Recommandé',
        'size':     '2.2 Go',
        'ram':      '4 Go RAM minimum',
        'desc':     'Rapide, léger, excellent en français. Idéal pour débuter.',
        'url':      'https://huggingface.co/bartowski/Phi-3.5-mini-instruct-GGUF/resolve/main/Phi-3.5-mini-instruct-Q4_K_M.gguf',
        'filename': 'phi-3.5-mini-instruct-Q4_K_M.gguf',
    },
    {
        'id':       'mistral7b',
        'name':     'Mistral 7B Instruct',
        'size':     '4.1 Go',
        'ram':      '8 Go RAM minimum',
        'desc':     'Excellent rapport qualité/vitesse. Très bon en analyse juridique.',
        'url':      'https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf',
        'filename': 'mistral-7b-instruct-v0.2.Q4_K_M.gguf',
    },
    {
        'id':       'qwen25-7b',
        'name':     'Qwen 2.5 7B Instruct',
        'size':     '4.7 Go',
        'ram':      '8 Go RAM minimum',
        'desc':     'Très bon en français et multilangue. Recommandé pour les dossiers complexes.',
        'url':      'https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m.gguf',
        'filename': 'qwen2.5-7b-instruct-q4_k_m.gguf',
    },
    {
        'id':       'deepseek-r1-8b',
        'name':     'DeepSeek R1 8B',
        'size':     '5.0 Go',
        'ram':      '10 Go RAM minimum',
        'desc':     'Excellent en raisonnement et analyse approfondie.',
        'url':      'https://huggingface.co/bartowski/DeepSeek-R1-0528-Qwen3-8B-GGUF/resolve/main/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf',
        'filename': 'DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf',
    },
]

def get_models_dir():
    """Dossier de stockage des modèles GGUF (à côté de l'exe ou du script)."""
    base = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent
    d = base / 'models'
    d.mkdir(exist_ok=True)
    return d

# Cache global du modèle llama.cpp chargé
_llama_instance   = None
_llama_model_path = None

# Cache global Whisper — évite le rechargement à chaque fichier audio/vidéo
_whisper_instance   = None
_whisper_model_size = None

def get_file_type(path):
    ext = Path(path).suffix.lower()
    if ext in VIDEO_EXT: return 'video'
    if ext in AUDIO_EXT: return 'audio'
    if ext in DOC_EXT:   return 'document'
    return 'unknown'

def human_size(b):
    if b < 1024: return f"{b} o"
    if b < 1024**2: return f"{b/1024:.1f} Ko"
    return f"{b/1024**2:.1f} Mo"

# ── Extracteurs ─────────────────────────────────────────────────────────────
def extract_pdf(path):
    try:
        import fitz
        doc = fitz.open(path)
        text = "".join(p.get_text() for p in doc); doc.close()
        return text.strip()
    except ImportError: return "[PyMuPDF non installe -> pip install pymupdf]"
    except Exception as e: return f"[Erreur PDF: {e}]"

def extract_docx(path):
    try:
        from docx import Document
        return "\n".join(p.text for p in Document(path).paragraphs if p.text.strip())
    except ImportError: return "[python-docx non installe -> pip install python-docx]"
    except Exception as e: return f"[Erreur DOCX: {e}]"

def extract_xlsx(path):
    try:
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        lines = []
        for ws in wb.worksheets:
            lines.append(f"=== {ws.title} ===")
            for row in ws.iter_rows(values_only=True):
                cells = [str(c) for c in row if c is not None]
                if cells: lines.append("\t".join(cells))
        return "\n".join(lines)
    except ImportError: return "[openpyxl non installe -> pip install openpyxl]"
    except Exception as e: return f"[Erreur XLSX: {e}]"

def extract_document(path):
    ext = Path(path).suffix.lower()
    if ext == '.pdf':            return extract_pdf(path)
    if ext == '.docx':           return extract_docx(path)
    if ext in ('.xlsx','.xls'): return extract_xlsx(path)
    try: return Path(path).read_text(encoding='utf-8', errors='replace')
    except Exception as e: return f"[Erreur lecture: {e}]"

# ── Workers ──────────────────────────────────────────────────────────────────
class TranscriptionWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(str)
    error    = pyqtSignal(str)
    def __init__(self, path, model_size="base", language="fr"):
        super().__init__()
        self.path = path; self.model_size = model_size; self.language = language
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def run(self):
        global _whisper_instance, _whisper_model_size
        try:
            if _whisper_instance is None or _whisper_model_size != self.model_size:
                self.progress.emit("Chargement du modele Whisper...")
                from faster_whisper import WhisperModel
                _whisper_instance   = WhisperModel(self.model_size, device="cpu", compute_type="int8")
                _whisper_model_size = self.model_size
            else:
                self.progress.emit("Modele Whisper deja en memoire...")
            if self._cancelled: return
            self.progress.emit("Transcription en cours...")
            lang = None if self.language == "auto" else self.language
            segments, _ = _whisper_instance.transcribe(self.path, language=lang, beam_size=5)
            # Vérification du flag entre chaque segment (faster-whisper est un générateur)
            parts = []
            for s in segments:
                if self._cancelled: return
                parts.append(s.text)
            self.finished.emit(" ".join(parts).strip())
        except ImportError:
            self.error.emit("faster-whisper non installe.\npip install faster-whisper\nFFmpeg requis pour les videos.")
        except Exception as e:
            if not self._cancelled:
                self.error.emit(f"Erreur transcription:\n{e}")

class PDFOCRWorker(QThread):
    """OCR pour PDF scannes — utilise easyocr (aucune install systeme requise)."""
    progress = pyqtSignal(str)
    finished = pyqtSignal(str)
    error    = pyqtSignal(str)
    def __init__(self, path, language="fr"):
        super().__init__()
        self.path = path; self.language = language
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def run(self):
        try:
            import fitz
        except ImportError:
            self.error.emit("PyMuPDF non installe → pip install pymupdf"); return
        try:
            import easyocr, numpy as np
        except ImportError:
            self.error.emit("easyocr non installe.\nRelancez install.bat ou :\npip install easyocr"); return
        try:
            self.progress.emit("Chargement du moteur OCR (premiere fois peut etre long)...")
            lang = self.language if self.language != "auto" else "fr"
            reader = easyocr.Reader([lang, 'en'] if lang != 'en' else ['en'], gpu=False, verbose=False)
            doc = fitz.open(self.path)
            total = len(doc)
            parts = []
            for i, page in enumerate(doc):
                if self._cancelled: doc.close(); return
                self.progress.emit(f"OCR page {i+1}/{total}...")
                pix = page.get_pixmap(dpi=200)
                img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
                if pix.n == 4: img = img[:, :, :3]
                result = reader.readtext(img, detail=0, paragraph=True)
                parts.append("\n".join(result) if result else "")
            doc.close()
            if not self._cancelled:
                self.finished.emit("\n\n".join(parts).strip())
        except Exception as e:
            if not self._cancelled:
                self.error.emit(f"Erreur OCR:\n{e}")

class BatchExtractionWorker(QThread):
    """Extraction batch de documents avec OCR automatique pour les PDF scannes."""
    progress = pyqtSignal(str)
    file_done = pyqtSignal(str, str)
    finished = pyqtSignal(dict)
    error    = pyqtSignal(str)
    def __init__(self, files_info, ocr_language="fr"):
        super().__init__()
        self.files_info = files_info; self.ocr_language = ocr_language
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def run(self):
        results = {}; ocr_reader = None
        for path, info in self.files_info.items():
            if self._cancelled: break                          # ← stop entre fichiers
            if info['type'] in ('video','audio'): continue
            name = info['name']
            if info.get('content','').strip():
                results[path] = info['content']; continue
            self.progress.emit(f"Extraction : {name}...")
            text = extract_document(path)
            if not text.strip() and Path(path).suffix.lower() == '.pdf':
                self.progress.emit(f"PDF scanne detecte : {name} — lancement OCR...")
                try:
                    import fitz, easyocr, numpy as np
                    if ocr_reader is None:
                        self.progress.emit("Chargement du moteur OCR...")
                        lang = self.ocr_language if self.ocr_language != "auto" else "fr"
                        ocr_reader = easyocr.Reader([lang, 'en'] if lang != 'en' else ['en'], gpu=False, verbose=False)
                    doc = fitz.open(path); total = len(doc); parts = []
                    for i, page in enumerate(doc):
                        if self._cancelled: doc.close(); break  # ← stop entre pages OCR
                        self.progress.emit(f"OCR {name} — page {i+1}/{total}")
                        pix = page.get_pixmap(dpi=200)
                        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
                        if pix.n == 4: img = img[:, :, :3]
                        result = ocr_reader.readtext(img, detail=0, paragraph=True)
                        parts.append("\n".join(result) if result else "")
                    if not self._cancelled:
                        doc.close()
                    text = "\n\n".join(parts).strip()
                except ImportError:
                    self.progress.emit(f"OCR non disponible pour {name} (easyocr manquant)")
                except Exception as e:
                    self.progress.emit(f"OCR echoue pour {name}: {e}")
            if not self._cancelled and text.strip():
                results[path] = text
                self.file_done.emit(path, text)
        if not self._cancelled:
            self.finished.emit(results)

class LMStudioWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(str)
    error    = pyqtSignal(str)
    PROMPTS = {
        # Quand ctx_block est vide : structure générique.
        # Quand ctx_block contient un prompt de domaine : la structure vient du contexte,
        # le prompt n'impose pas ses propres headers pour éviter les conflits.
        "summary": (
            "{ctx_block}"
            "Fais un résumé clair et structuré du texte suivant{ctx_hint}. "
            "Si un cadre d'analyse est défini dans les instructions ci-dessus, applique-le. "
            "Sinon, utilise des titres ## et des listes à puces.\n\n"
            "TEXTE :\n{text}\n\nRÉSUMÉ :"
        ),
        "deep": (
            "{ctx_block}"
            "Analyse en profondeur le texte suivant{ctx_hint}. "
            "Applique strictement le cadre d'analyse défini dans les instructions ci-dessus. "
            "Si aucun cadre n'est défini, structure en : "
            "## Thèmes principaux / ## Points clés / ## Insights / ## Points d'attention / ## Conclusion.\n\n"
            "TEXTE :\n{text}\n\nANALYSE :"
        ),
        "global": (
            "{ctx_block}"
            "Tu dois produire une synthèse globale de plusieurs documents{ctx_hint}. "
            "Applique le cadre d'analyse défini dans les instructions ci-dessus si présent. "
            "Sinon, structure en : "
            "## Vue d'ensemble / ## Liens et cohérence entre documents / "
            "## Points clés communs / ## Contradictions ou divergences / ## Conclusions.\n\n"
            "ANALYSES INDIVIDUELLES :\n{text}\n\nSYNTHÈSE GLOBALE :"
        ),
        "qa": (
            "{ctx_block}"
            "Sur la base du texte suivant{ctx_hint}, réponds précisément à la question posée. "
            "Appuie-toi sur les éléments factuels du texte. "
            "Si un cadre d'analyse est défini ci-dessus, intègre-le dans ta réponse.\n\n"
            "TEXTE :\n{text}\n\nQUESTION : {question}\n\nRÉPONSE :"
        ),
    }
    BASE_URL = "http://localhost:1234/v1"
    # Limites de caractères par tâche
    # Règle : prompt + réponse ≤ contexte LM Studio (souvent 16k tokens)
    # 1 token ≈ 4 caractères → 16000 tokens ≈ 64000 caractères total
    # On réserve ~8000 tokens pour la réponse → il reste ~8000 tokens pour le prompt
    # Prompt système + texte utilisateur ≈ 32 000 caractères max
    TEXT_LIMITS = {
        "summary": 8000,    # résumé    — ~1 200 mots analysés
        "deep":    10000,   # analyse   — ~1 500 mots analysés
        "global":  20000,   # synthèse globale (plusieurs analyses)
        "qa":      6000,    # Q&R
    }
    # Tokens réservés pour la réponse
    RESPONSE_TOKENS = {
        "summary": 2048,
        "deep":    4096,
        "global":  8192,
        "qa":      2048,
    }
    # Instruction de langue injectée dans chaque prompt selon les paramètres utilisateur
    LANG_INSTRUCTIONS = {
        'fr':   'Réponds toujours en français.',
        'en':   'Always answer in English.',
        'nl':   'Antwoord altijd in het Nederlands.',
        'es':   'Responde siempre en español.',
        'de':   'Antworte immer auf Deutsch.',
        'it':   'Rispondi sempre in italiano.',
        'pt':   'Responda sempre em português.',
        'ar':   'أجب دائمًا باللغة العربية.',
        'zh':   '请始终用中文回答。',
        'auto': '',   # auto-détection : pas d'instruction, l'IA suit la langue du document
    }

    def __init__(self, text, model, task, question="", context="",
                 engine="lmstudio", model_path="", lang_code="fr"):
        super().__init__()
        limit = self.TEXT_LIMITS.get(task, 6000)
        self.text = text[:limit]; self.model = model
        self.task = task; self.question = question; self.context = context.strip()
        self.engine = engine
        self.model_path = model_path
        self.lang_code  = lang_code
        self._session   = None   # session requests — fermable via cancel()
        self._cancelled = False

    def cancel(self):
        """Ferme la session HTTP en cours — interrompt la requête LM Studio."""
        self._cancelled = True
        if self._session:
            try: self._session.close()
            except: pass

    def run(self):
        if self.engine == 'llamacpp':
            self._run_llamacpp()
        else:
            self._run_lmstudio()

    def _build_prompt(self):
        if self.context:
            ctx_block = f"CONTEXTE UTILISATEUR:\n{self.context}\n\n"
            ctx_hint  = " (en tenant compte du contexte fourni)"
        else:
            ctx_block = ""; ctx_hint = ""
        prompt = self.PROMPTS[self.task].format(
            text=self.text, question=self.question,
            ctx_block=ctx_block, ctx_hint=ctx_hint
        )
        # Instruction de langue — injectée à la fin pour avoir la priorité
        lang_instr = self.LANG_INSTRUCTIONS.get(self.lang_code, '')
        if lang_instr:
            prompt = f"{lang_instr}\n\n{prompt}"
        return prompt

    def _run_llamacpp(self):
        global _llama_instance, _llama_model_path
        try:
            from llama_cpp import Llama
        except ImportError:
            self.error.emit("llama-cpp-python non installe.\nRelancez l'assistant de configuration.")
            return
        try:
            self.progress.emit("Chargement du modele en memoire...")
            if _llama_instance is None or _llama_model_path != self.model_path:
                _llama_instance  = Llama(
                    model_path=self.model_path,
                    n_ctx=8192, n_threads=4, verbose=False
                )
                _llama_model_path = self.model_path
            prompt = self._build_prompt()
            self.progress.emit("Generation en cours...")
            resp = _llama_instance(prompt, max_tokens=0, stop=[], echo=False)
            self.finished.emit(resp['choices'][0]['text'].strip())
        except Exception as e:
            self.error.emit(f"Erreur moteur local:\n{e}")

    # Timeouts par tâche (secondes)
    # deepseek-r1 et autres modèles raisonnants peuvent prendre très longtemps
    TIMEOUTS = {
        "summary": 600,   # 10 min — résumé rapide
        "deep":    1800,  # 30 min — raisonnement étendu sur gros document
        "global":  1800,  # 30 min — synthèse multi-documents
        "qa":      300,   # 5 min  — question courte
    }

    def _run_lmstudio(self):
        # Import en dehors du bloc try principal pour permettre la re-vérification
        try:
            import requests as _req
        except ImportError:
            self.error.emit("Le package 'requests' n'est pas installe.\npip install requests")
            return

        timeout = self.TIMEOUTS.get(self.task, 900)
        prompt  = self._build_prompt()
        payload = {
            "model":    self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }
        if self.task in self.RESPONSE_TOKENS:
            payload["max_tokens"] = self.RESPONSE_TOKENS[self.task]

        # Retry automatique : LM Studio (surtout les modèles reasoning) libère ses
        # slots entre deux requêtes. La reconnexion immédiate peut échouer pendant
        # cette micro-transition (~1-6 s). On réessaie 3× avec backoff exponentiel.
        max_retries, wait = 3, 3
        for attempt in range(max_retries):
            if self._cancelled: return                         # ← annulation demandée
            try:
                if attempt > 0:
                    self.progress.emit(
                        f"Tentative {attempt + 1}/{max_retries} — "
                        f"attente {wait // 2}s avant reconnexion..."
                    )
                    import time; time.sleep(wait // 2)

                self.progress.emit(f"Traitement avec {self.model}...")
                self._session = _req.Session()                 # session fermable via cancel()
                resp = self._session.post(
                    f"{self.BASE_URL}/chat/completions",
                    json=payload, timeout=timeout
                )
                resp.raise_for_status()
                data    = resp.json()
                content = data['choices'][0]['message']['content']
                if not content or not content.strip():
                    self.error.emit(
                        "LM Studio a retourne une reponse vide.\n"
                        "Le modele a peut-etre depasse sa memoire ou arrete la generation.\n"
                        "Essayez de recharger le modele dans LM Studio."
                    )
                    return
                self.finished.emit(content)
                return  # succès

            except _req.exceptions.ConnectionError:
                if self._cancelled: return                     # ← fermeture intentionnelle
                # Vérifier si LM Studio est vraiment down ou juste en transition
                lm_running = False
                try:
                    _req.get(f"{self.BASE_URL}/models", timeout=3)
                    lm_running = True
                except Exception:
                    pass

                if lm_running and attempt < max_retries - 1:
                    # LM Studio tourne mais est en micro-transition entre deux requêtes
                    self.progress.emit(
                        f"LM Studio en cours de reinitialisation des slots "
                        f"({attempt + 1}/{max_retries}) — nouvelle tentative dans {wait}s..."
                    )
                    import time; time.sleep(wait)
                    wait *= 2  # backoff : 3 s → 6 s
                    continue
                elif lm_running:
                    self.error.emit(
                        f"Connexion interrompue pendant la generation.\n"
                        f"LM Studio tourne mais a coupe la connexion (manque de memoire ?\n"
                        f"generation interrompue en interne ?).\n"
                        f"Redemarrez LM Studio et relancez l'analyse.\n"
                        f"Modele: {self.model}"
                    )
                else:
                    self.error.emit(
                        f"LM Studio n'est pas lance.\n"
                        f"Demarrez LM Studio et activez le serveur local.\n"
                        f"Modele: {self.model}"
                    )
                return

            except _req.exceptions.Timeout:
                mins = timeout // 60
                self.error.emit(
                    f"Generation trop longue (timeout > {mins} min).\n"
                    f"Le modele {self.model} avec raisonnement peut etre tres lent "
                    f"sur de longs documents.\n"
                    f"Solutions possibles :\n"
                    f"  - Reduire la taille du document\n"
                    f"  - Utiliser un modele plus rapide (ex: qwen2.5-7b-instruct)\n"
                    f"  - Augmenter la limite dans les parametres LM Studio"
                )
                return

            except Exception as e:
                msg = str(e)
                if "404" in msg or "not found" in msg.lower():
                    self.error.emit(
                        f"Modele '{self.model}' non charge dans LM Studio.\n"
                        f"Chargez-le d'abord dans LM Studio."
                    )
                else:
                    self.error.emit(f"Erreur LM Studio:\n{msg}")
                return

class DirectSynthesisWorker(QThread):
    """Worker pour la synthese globale directe."""
    finished = pyqtSignal(str)
    error    = pyqtSignal(str)
    progress = pyqtSignal(str)
    def __init__(self, prompt, model, engine="lmstudio", model_path=""):
        super().__init__()
        self._prompt     = prompt
        self._model      = model
        self._engine     = engine
        self._model_path = model_path
        self._session    = None
        self._cancelled  = False

    def cancel(self):
        self._cancelled = True
        if self._session:
            try: self._session.close()
            except: pass

    def run(self):
        if self._engine == 'llamacpp':
            self._run_llamacpp()
        else:
            self._run_lmstudio()

    def _run_llamacpp(self):
        global _llama_instance, _llama_model_path
        try:
            from llama_cpp import Llama
        except ImportError:
            self.error.emit("llama-cpp-python non installe.\nRelancez l'assistant de configuration.")
            return
        try:
            self.progress.emit("Chargement du modele en memoire...")
            if _llama_instance is None or _llama_model_path != self._model_path:
                _llama_instance   = Llama(model_path=self._model_path,
                                          n_ctx=8192, n_threads=4, verbose=False)
                _llama_model_path = self._model_path
            self.progress.emit("Generation en cours...")
            resp = _llama_instance(self._prompt, max_tokens=0, stop=[], echo=False)
            self.finished.emit(resp['choices'][0]['text'].strip())
        except Exception as e:
            self.error.emit(f"Erreur moteur local:\n{e}")

    def _run_lmstudio(self):
        try:
            import requests as _req
        except ImportError:
            self.error.emit("Le package 'requests' n'est pas installe.")
            return

        payload = {
            "model":    self._model,
            "messages": [{"role": "user", "content": self._prompt}],
            "temperature": 0.7,
            "max_tokens": 8192
        }

        # Même logique de retry que LMStudioWorker : les modèles reasoning libèrent
        # leurs slots entre requêtes, ce qui cause des ConnectionError transitoires.
        max_retries, wait = 3, 3
        for attempt in range(max_retries):
            if self._cancelled: return                         # ← annulation demandée
            try:
                if attempt > 0:
                    import time; time.sleep(wait // 2)

                self.progress.emit(f"Generation en cours avec {self._model}...")
                self._session = _req.Session()                 # session fermable via cancel()
                resp = self._session.post(
                    "http://localhost:1234/v1/chat/completions",
                    json=payload,
                    timeout=1800
                )
                resp.raise_for_status()
                data    = resp.json()
                content = data['choices'][0]['message']['content']
                if not content or not content.strip():
                    self.error.emit(
                        "LM Studio a retourne une reponse vide.\n"
                        "Rechargez le modele et relancez la synthese."
                    )
                    return
                self.finished.emit(content)
                return  # succès

            except _req.exceptions.ConnectionError:
                if self._cancelled: return                     # ← fermeture intentionnelle
                lm_running = False
                try:
                    _req.get("http://localhost:1234/v1/models", timeout=3)
                    lm_running = True
                except Exception:
                    pass

                if lm_running and attempt < max_retries - 1:
                    self.progress.emit(
                        f"LM Studio en reinitialisation des slots "
                        f"({attempt + 1}/{max_retries}) — nouvelle tentative dans {wait}s..."
                    )
                    import time; time.sleep(wait)
                    wait *= 2
                    continue
                elif lm_running:
                    self.error.emit(
                        "Connexion interrompue pendant la generation.\n"
                        "LM Studio a peut-etre manque de memoire.\n"
                        "Redemarrez LM Studio et relancez la synthese."
                    )
                else:
                    self.error.emit(
                        "LM Studio n'est pas lance.\n"
                        "Demarrez LM Studio et activez le serveur local."
                    )
                return

            except _req.exceptions.Timeout:
                self.error.emit(
                    "Generation trop longue (timeout > 30 min).\n"
                    "Reduisez le nombre ou la taille des documents,\n"
                    "ou utilisez un modele plus rapide."
                )
                return

            except Exception as e:
                self.error.emit(f"Erreur LM Studio:\n{e}")
                return


class LMStudioListWorker(QThread):
    finished = pyqtSignal(list)
    BASE_URL = "http://localhost:1234/v1"
    def run(self):
        try:
            import requests
            resp = requests.get(f"{self.BASE_URL}/models", timeout=5)
            resp.raise_for_status()
            data = resp.json()
            names = [m['id'] for m in data.get('data', [])]
            self.finished.emit(names)
        except Exception:
            self.finished.emit([])

# ── Workers installation / téléchargement ───────────────────────────────────
class LlamaCppInstallWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)   # (success, message)
    def run(self):
        try:
            self.progress.emit("Installation de llama-cpp-python...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "llama-cpp-python",
                 "--extra-index-url", "https://abetlen.github.io/llama-cpp-python/whl/cpu"],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                # Fallback : installation standard sans accélération
                self.progress.emit("Tentative installation standard...")
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "llama-cpp-python"],
                    capture_output=True, text=True
                )
            if result.returncode == 0:
                self.finished.emit(True, "llama-cpp-python installe avec succes.")
            else:
                self.finished.emit(False, f"Echec installation :\n{result.stderr[-500:]}")
        except Exception as e:
            self.finished.emit(False, str(e))


class ModelDownloadWorker(QThread):
    progress  = pyqtSignal(str, int)   # (message, pourcentage 0-100)
    finished  = pyqtSignal(bool, str)  # (success, path_or_error)
    def __init__(self, url, dest_path):
        super().__init__()
        self.url = url; self.dest_path = dest_path
    def run(self):
        try:
            import requests
            self.progress.emit("Connexion au serveur...", 0)
            r = requests.get(self.url, stream=True, timeout=30)
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))
            downloaded = 0
            with open(self.dest_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total:
                            pct = int(downloaded * 100 / total)
                            mb  = downloaded / 1024 / 1024
                            self.progress.emit(f"Téléchargement... {mb:.0f} Mo", pct)
            self.finished.emit(True, str(self.dest_path))
        except Exception as e:
            # Nettoyage fichier partiel
            try: Path(self.dest_path).unlink(missing_ok=True)
            except: pass
            self.finished.emit(False, str(e))


# ── Assistant de configuration (premier lancement / pas de LM Studio) ────────
LANGUAGES = [
    ('fr', '🇫🇷  Français'),
    ('en', '🇬🇧  English'),
    ('es', '🇪🇸  Español'),
    ('de', '🇩🇪  Deutsch'),
    ('pt', '🇧🇷  Português'),
    ('it', '🇮🇹  Italiano'),
    ('nl', '🇳🇱  Nederlands'),
    ('ar', '🇸🇦  العربية'),
]

class SetupWizard(QDialog):
    engine_ready = pyqtSignal(str, str, str)  # (engine, model_path, language_code)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuration — FileAnalyzer AI")
        self.setFixedSize(680, 600)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self._selected_model    = LLAMACPP_MODELS[0]
        self._selected_language = 'fr'
        self._install_worker    = None
        self._download_worker   = None
        self._build()

    def _build(self):
        lay = QVBoxLayout(self); lay.setContentsMargins(28, 24, 28, 20); lay.setSpacing(16)

        # Titre
        title = QLabel("🤖  Configuration du moteur IA")
        title.setStyleSheet("font-size:20px; font-weight:700;")
        sub = QLabel("LM Studio n'a pas été détecté. Choisissez comment alimenter l'IA.")
        sub.setStyleSheet(f"color:{TDIM}; font-size:13px;")
        lay.addWidget(title); lay.addWidget(sub)

        # Séparateur
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color:{BORDER};"); lay.addWidget(sep)

        # ── Option A : LM Studio ──────────────────────────────
        grp_lms = QGroupBox("Option A — LM Studio (déjà installé)")
        lms_lay = QVBoxLayout(grp_lms); lms_lay.setSpacing(8)
        lms_info = QLabel("Démarrez LM Studio, chargez un modèle et activez le serveur local,\n"
                          "puis cliquez sur Réessayer.")
        lms_info.setStyleSheet(f"color:{TDIM}; font-size:12px;")
        self.btn_retry = QPushButton("🔄  Réessayer la connexion LM Studio")
        self.btn_retry.clicked.connect(self._retry_lmstudio)
        lms_lay.addWidget(lms_info); lms_lay.addWidget(self.btn_retry)
        lay.addWidget(grp_lms)

        # ── Option B : Moteur intégré ─────────────────────────
        grp_llm = QGroupBox("Option B — Moteur intégré (recommandé, aucun logiciel tiers)")
        llm_lay = QVBoxLayout(grp_llm); llm_lay.setSpacing(10)

        llm_info = QLabel("Choisissez un modèle à télécharger une seule fois.\n"
                          "L'IA fonctionnera directement sans rien d'autre à installer.")
        llm_info.setStyleSheet(f"color:{TDIM}; font-size:12px;")
        llm_lay.addWidget(llm_info)

        # Sélecteur de modèle
        for m in LLAMACPP_MODELS:
            btn = QRadioButton(f"{m['name']}  —  {m['size']}  —  {m['ram']}")
            btn.setToolTip(m['desc'])
            if m == LLAMACPP_MODELS[0]: btn.setChecked(True)
            btn.toggled.connect(lambda checked, model=m: self._select_model(model) if checked else None)
            llm_lay.addWidget(btn)

        # Vérifier si un modèle est déjà téléchargé
        already = self._find_existing_model()
        if already:
            note = QLabel(f"✅  Modèle trouvé localement : {Path(already).name}")
            note.setStyleSheet(f"color:{OK}; font-size:11px;")
            llm_lay.addWidget(note)

        self.btn_install = QPushButton("⬇  Installer le moteur et télécharger le modèle")
        self.btn_install.clicked.connect(self._start_install)
        llm_lay.addWidget(self.btn_install)

        if already:
            self.btn_use_existing = QPushButton("▶  Utiliser le modèle déjà téléchargé")
            self.btn_use_existing.setStyleSheet(f"background:{OK};")
            self.btn_use_existing.clicked.connect(lambda: self._finish_llamacpp(already))
            llm_lay.addWidget(self.btn_use_existing)

        lay.addWidget(grp_llm)

        # ── Sélection de la langue ────────────────────────────
        grp_lang = QGroupBox("Langue de travail (transcription & analyse)")
        lang_lay = QHBoxLayout(grp_lang); lang_lay.setSpacing(8)
        self.lang_combo = QComboBox()
        for code, label in LANGUAGES:
            self.lang_combo.addItem(label, code)
        self.lang_combo.setCurrentIndex(0)  # Français par défaut
        self.lang_combo.currentIndexChanged.connect(
            lambda i: setattr(self, '_selected_language', self.lang_combo.itemData(i))
        )
        lang_lbl = QLabel("Langue :")
        lang_lbl.setStyleSheet(f"color:{TDIM};")
        lang_lay.addWidget(lang_lbl); lang_lay.addWidget(self.lang_combo); lang_lay.addStretch()
        lay.addWidget(grp_lang)

        # ── Barre de progression ──────────────────────────────
        self.prog_lbl = QLabel(""); self.prog_lbl.setStyleSheet(f"color:{TDIM}; font-size:12px;")
        self.prog_lbl.hide()
        self.prog_bar = QProgressBar(); self.prog_bar.setFixedHeight(8)
        self.prog_bar.setRange(0, 100); self.prog_bar.hide()
        lay.addWidget(self.prog_lbl); lay.addWidget(self.prog_bar)

        lay.addStretch()

    def _select_model(self, model):
        self._selected_model = model

    def _find_existing_model(self):
        """Cherche un fichier .gguf déjà téléchargé dans le dossier models/."""
        d = get_models_dir()
        for m in LLAMACPP_MODELS:
            p = d / m['filename']
            if p.exists() and p.stat().st_size > 100_000_000:  # > 100 Mo = valide
                return str(p)
        return None

    def _retry_lmstudio(self):
        self.btn_retry.setEnabled(False)
        self.btn_retry.setText("Connexion en cours...")
        QTimer.singleShot(500, self._check_lmstudio)

    def _check_lmstudio(self):
        if detect_lmstudio():
            self.engine_ready.emit('lmstudio', '', self._selected_language)
            self.accept()
        else:
            self.btn_retry.setEnabled(True)
            self.btn_retry.setText("🔄  Réessayer la connexion LM Studio")
            QMessageBox.warning(self, "Non détecté",
                "LM Studio ne répond toujours pas.\n"
                "Vérifiez qu'il est lancé et que le serveur local est activé\n"
                "(bouton vert dans LM Studio → Local Server).")

    def _start_install(self):
        self.btn_install.setEnabled(False)
        self.btn_retry.setEnabled(False)
        self.prog_lbl.show(); self.prog_bar.show()
        self.prog_bar.setRange(0, 0)  # mode indéterminé pendant l'install

        self._install_worker = LlamaCppInstallWorker()
        self._install_worker.progress.connect(lambda m: self.prog_lbl.setText(m))
        self._install_worker.finished.connect(self._on_install_done)
        self._install_worker.start()

    def _on_install_done(self, success, msg):
        if not success:
            self.prog_lbl.hide(); self.prog_bar.hide()
            self.btn_install.setEnabled(True); self.btn_retry.setEnabled(True)
            QMessageBox.critical(self, "Erreur installation", msg)
            return
        self.prog_lbl.setText("Installation OK — Téléchargement du modèle...")
        self.prog_bar.setRange(0, 100)
        m = self._selected_model
        dest = get_models_dir() / m['filename']
        self._download_worker = ModelDownloadWorker(m['url'], str(dest))
        self._download_worker.progress.connect(self._on_dl_progress)
        self._download_worker.finished.connect(self._on_dl_done)
        self._download_worker.start()

    def _on_dl_progress(self, msg, pct):
        self.prog_lbl.setText(msg)
        self.prog_bar.setValue(pct)

    def _on_dl_done(self, success, path_or_err):
        if not success:
            self.prog_lbl.hide(); self.prog_bar.hide()
            self.btn_install.setEnabled(True); self.btn_retry.setEnabled(True)
            QMessageBox.critical(self, "Erreur téléchargement", path_or_err)
            return
        self._finish_llamacpp(path_or_err)

    def _finish_llamacpp(self, model_path):
        self.engine_ready.emit('llamacpp', model_path, self._selected_language)
        self.accept()


# ── Dialog choix de modele ───────────────────────────────────────────────────
class ModelPickerDialog(QDialog):
    POPULAR = [
        ("mistral-7b",          "Mistral 7B",       "~4 Go",  "Excellent rapport qualite/vitesse - recommande"),
        ("llama-3-8b",          "Llama 3 8B",       "~5 Go",  "Tres bon pour l'analyse de documents"),
        ("llama-3.1-8b",        "Llama 3.1 8B",     "~5 Go",  "Version amelioree de Llama 3"),
        ("deepseek-r1-8b",      "DeepSeek R1 8B",   "~5 Go",  "Excellent en raisonnement et analyse"),
        ("deepseek-r1-14b",     "DeepSeek R1 14B",  "~9 Go",  "Plus puissant, necessite plus de RAM"),
        ("deepseek-r1-32b",     "DeepSeek R1 32B",  "~20 Go", "Tres puissant, necessite beaucoup de RAM"),
        ("phi-3-mini",          "Phi-3 Mini",       "~2 Go",  "Leger et rapide, bon pour les petites configs"),
        ("phi-4",               "Phi-4",            "~9 Go",  "Excellent modele de Microsoft"),
        ("gemma-2-9b",          "Gemma 2 9B",       "~6 Go",  "Modele Google tres performant"),
        ("qwen2.5-7b",          "Qwen 2.5 7B",      "~5 Go",  "Excellent en multilangue dont le francais"),
        ("qwen2.5-14b",         "Qwen 2.5 14B",     "~9 Go",  "Tres puissant en analyse"),
        ("mixtral-8x7b",        "Mixtral 8x7B",     "~26 Go", "Tres puissant, necessite beaucoup de RAM"),
        ("openhermes-2.5",      "OpenHermes 2.5",   "~4 Go",  "Optimise pour les instructions"),
        ("neural-chat",         "Neural Chat",      "~4 Go",  "Optimise pour la conversation"),
        ("codellama",           "Code Llama",       "~4 Go",  "Specialise dans l'analyse de code"),
    ]

    def __init__(self, current_model, parent=None):
        super().__init__(parent)
        self.chosen_model = current_model
        self.setWindowTitle("Choisir le modele IA")
        self.setMinimumSize(720, 600)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self._build()
        self._load_installed()

    def _build(self):
        lay = QVBoxLayout(self); lay.setContentsMargins(20,20,20,16); lay.setSpacing(12)

        title = QLabel("🤖  Choisissez votre modele IA"); title.setObjectName("h1")
        sub = QLabel("Selectionnez un modele installe ou choisissez-en un a installer.")
        sub.setObjectName("dim")
        lay.addWidget(title); lay.addWidget(sub)

        self.search = QLineEdit(); self.search.setPlaceholderText("Rechercher un modele...")
        self.search.textChanged.connect(self._filter)
        lay.addWidget(self.search)

        self.tabs = QTabWidget()

        # Tab installes
        self.inst_container = QWidget()
        self.inst_lay = QVBoxLayout(self.inst_container)
        self.inst_lay.setContentsMargins(4,4,4,4); self.inst_lay.setSpacing(4)
        self.inst_loading = QLabel("Chargement des modeles installes...")
        self.inst_loading.setObjectName("dim"); self.inst_loading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inst_lay.addWidget(self.inst_loading); self.inst_lay.addStretch()
        inst_scroll = QScrollArea(); inst_scroll.setWidgetResizable(True)
        inst_scroll.setWidget(self.inst_container); inst_scroll.setFrameShape(QFrame.Shape.NoFrame)

        # Tab populaires
        self.pop_container = QWidget()
        self.pop_lay = QVBoxLayout(self.pop_container)
        self.pop_lay.setContentsMargins(4,4,4,4); self.pop_lay.setSpacing(4)
        for row in self.POPULAR:
            self.pop_lay.addWidget(self._make_card(*row))
        self.pop_lay.addStretch()
        pop_scroll = QScrollArea(); pop_scroll.setWidgetResizable(True)
        pop_scroll.setWidget(self.pop_container); pop_scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.tabs.addTab(inst_scroll, "✅  Installes")
        self.tabs.addTab(pop_scroll,  "📦  Populaires")
        lay.addWidget(self.tabs, 1)

        # Saisie manuelle
        mg = QGroupBox("Ou saisissez un nom de modele manuellement")
        mgl = QHBoxLayout(mg)
        self.manual = QLineEdit(); self.manual.setPlaceholderText("ex: identifiant du modele charge dans LM Studio...")
        self.manual.setText(self.chosen_model)
        btn_m = QPushButton("Utiliser"); btn_m.setFixedWidth(100)
        btn_m.clicked.connect(lambda: self._select(self.manual.text().strip()))
        mgl.addWidget(self.manual,1); mgl.addWidget(btn_m)
        lay.addWidget(mg)

        note = QLabel(
            "Les modeles charges dans LM Studio apparaissent dans l'onglet <b>Installes</b>.  |  "
            "Telechargez vos modeles depuis <a href='https://lmstudio.ai' style='color:#0078d4'>lmstudio.ai</a>"
        )
        note.setOpenExternalLinks(True); note.setObjectName("dim"); note.setWordWrap(True)
        lay.addWidget(note)

        btns = QHBoxLayout()
        cancel = QPushButton("Annuler"); cancel.setObjectName("secondary"); cancel.clicked.connect(self.reject)
        self.ok_btn = QPushButton(f"Utiliser  {self.chosen_model}")
        self.ok_btn.clicked.connect(self.accept)
        btns.addStretch(); btns.addWidget(cancel); btns.addWidget(self.ok_btn)
        lay.addLayout(btns)

    def _make_card(self, model_id, name, size, desc, installed=False):
        card = QFrame()
        card.setStyleSheet(f"QFrame{{background:{CARD};border-radius:8px;}} QFrame:hover{{background:#484848;}}")
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        card.setProperty("model_id", model_id)
        card.setProperty("search_text", f"{name} {model_id} {desc}".lower())
        # Clic n'importe ou sur la carte → selectionne le modele
        card.mousePressEvent = lambda e, m=model_id: self._select(m)
        cl = QHBoxLayout(card); cl.setContentsMargins(12,8,12,8)
        info = QVBoxLayout(); info.setSpacing(2)
        badge = "✅ " if installed else ""
        n = QLabel(f"{badge}<b>{name}</b>  <span style='color:{TDIM};font-size:11px;'>({model_id})</span>")
        n.setStyleSheet("font-size:13px;")
        d = QLabel(f"{desc}  •  RAM : {size}"); d.setStyleSheet(f"color:{TDIM}; font-size:11px;")
        info.addWidget(n); info.addWidget(d)
        btn = QPushButton("Selectionner"); btn.setFixedWidth(120)
        btn.clicked.connect(lambda _, m=model_id: self._select(m))
        cl.addLayout(info,1); cl.addWidget(btn)
        return card

    def _load_installed(self):
        w = LMStudioListWorker(); w.finished.connect(self._on_installed); w.start(); self._lw = w

    def _on_installed(self, models):
        for i in reversed(range(self.inst_lay.count())):
            item = self.inst_lay.itemAt(i)
            if item and item.widget(): item.widget().deleteLater()

        if not models:
            lbl = QLabel("Aucun modele charge, ou LM Studio n'est pas lance.\nDemarrez LM Studio et chargez un modele.")
            lbl.setObjectName("dim"); lbl.setAlignment(Qt.AlignmentFlag.AlignCenter); lbl.setWordWrap(True)
            self.inst_lay.addWidget(lbl); self.inst_lay.addStretch(); return

        pop_map = {p[0]: p for p in self.POPULAR}
        for m in models:
            # LM Studio model IDs can be paths like "publisher/model-name"
            # Try exact match, then basename, then fuzzy match on POPULAR keys
            base = m.split('/')[-1].lower()
            info = pop_map.get(m)
            if not info:
                for key, val in pop_map.items():
                    if key in m.lower() or key in base:
                        info = val; break
            if info:
                card = self._make_card(m, info[1], info[2], info[3], installed=True)
            else:
                card = self._make_card(m, m, "?", "Modele installe localement", installed=True)
            self.inst_lay.addWidget(card)
        self.inst_lay.addStretch()

        if models and self.chosen_model not in models:
            self._select(models[0])

    def _select(self, model_id):
        if not model_id: return
        self.chosen_model = model_id
        self.manual.setText(model_id)
        # Afficher un nom court dans le bouton si l'ID est trop long
        display = model_id if len(model_id) <= 40 else "..." + model_id[-37:]
        self.ok_btn.setText(f"Utiliser  {display}")
        # Surbrillance de la carte selectionnee dans les deux onglets
        for container in (self.inst_container, self.pop_container):
            for i in range(container.layout().count()):
                item = container.layout().itemAt(i)
                if not item or not item.widget(): continue
                w = item.widget()
                mid = w.property("model_id")
                if mid == model_id:
                    w.setStyleSheet(f"QFrame{{background:{ACCENT};border-radius:8px;}} QFrame:hover{{background:{ACCENT2};}}")
                else:
                    w.setStyleSheet(f"QFrame{{background:{CARD};border-radius:8px;}} QFrame:hover{{background:#484848;}}")

    def _filter(self, text):
        text = text.lower()
        for i in range(self.pop_lay.count()):
            item = self.pop_lay.itemAt(i)
            if item and item.widget():
                w = item.widget(); st = w.property("search_text") or ""
                w.setVisible(text in st if text else True)

    def get_model(self): return self.chosen_model


# ── Mode Selector ───────────────────────────────────────────────────────────
class ModeSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background:{SURFACE}; border-radius:10px;")
        lay = QVBoxLayout(self); lay.setContentsMargins(12,10,12,10); lay.setSpacing(8)

        top = QHBoxLayout()
        icon = QLabel("⚡"); icon.setStyleSheet("font-size:14px;")
        title = QLabel("Mode d'analyse"); title.setStyleSheet("font-weight:700; font-size:12px;")
        top.addWidget(icon); top.addWidget(title); top.addStretch()
        lay.addLayout(top)

        self.btn_full = QRadioButton("Analyse complete")
        self.btn_full.setToolTip("Resume + analyse approfondie par document + synthese globale")
        self.btn_full.setChecked(True)

        self.btn_global = QRadioButton("Synthese globale directe")
        self.btn_global.setToolTip("Extrait le contenu de tous les docs et genere une synthese globale en une seule etape — plus rapide")

        sub_full   = QLabel("Resume · Analyse par doc · Synthese")
        sub_global = QLabel("Contenu brut → Synthese globale directement")
        sub_full.setStyleSheet(f"color:{TDIM}; font-size:10px; margin-left:22px;")
        sub_global.setStyleSheet(f"color:{TDIM}; font-size:10px; margin-left:22px;")

        lay.addWidget(self.btn_full); lay.addWidget(sub_full)
        lay.addWidget(self.btn_global); lay.addWidget(sub_global)

    def is_full(self): return self.btn_full.isChecked()

# ── Drop Zone ────────────────────────────────────────────────────────────────
class DropZone(QWidget):
    files_dropped = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setFixedHeight(110)        # hauteur fixe compacte
        self.dragging = False
        lay = QVBoxLayout(self); lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setContentsMargins(8, 6, 8, 6); lay.setSpacing(4)
        top_row = QHBoxLayout(); top_row.setSpacing(8)
        icon = QLabel("📂"); icon.setStyleSheet("font-size:22px;")
        texts = QVBoxLayout(); texts.setSpacing(1)
        main = QLabel("Glissez vos fichiers ici")
        main.setStyleSheet("font-size:13px; font-weight:600;")
        sub = QLabel("Vidéo • Audio • PDF • Word • Excel • Texte • Dossiers")
        sub.setObjectName("dim"); sub.setStyleSheet(f"color:{TDIM}; font-size:10px;")
        texts.addWidget(main); texts.addWidget(sub)
        btn = QPushButton("Parcourir…"); btn.setFixedSize(100, 28)
        btn.setCursor(Qt.CursorShape.PointingHandCursor); btn.clicked.connect(self._browse)
        top_row.addWidget(icon); top_row.addLayout(texts, 1); top_row.addWidget(btn)
        lay.addLayout(top_row)

    def _browse(self):
        # Proposer fichiers OU dossier
        menu = QMenu()
        menu.setStyleSheet(f"QMenu{{background:#383838;color:white;border:1px solid #454545;border-radius:6px;padding:4px;}}"
                           f"QMenu::item{{padding:8px 20px;}} QMenu::item:selected{{background:#0078d4;}}")
        act_files  = menu.addAction("📄  Selectionner des fichiers")
        act_folder = menu.addAction("📁  Selectionner un dossier entier")
        action = menu.exec(self.mapToGlobal(self.rect().center()))
        if action == act_files:
            files, _ = QFileDialog.getOpenFileNames(self, "Selectionner des fichiers", "",
                "Fichiers supportes (*.mp4 *.mkv *.avi *.mov *.mp3 *.wav *.m4a *.flac *.pdf *.docx *.xlsx *.txt *.md *.csv)")
            if files: self.files_dropped.emit(files)
        elif action == act_folder:
            folder = QFileDialog.getExistingDirectory(self, "Selectionner un dossier")
            if folder: self.files_dropped.emit(self._scan_folder(folder))

    def _scan_folder(self, folder):
        supported = {'.mp4','.mkv','.avi','.mov','.wmv','.flv','.webm','.m4v','.ts',
                     '.mp3','.wav','.m4a','.flac','.ogg','.aac','.wma','.opus',
                     '.pdf','.docx','.xlsx','.xls','.txt','.md','.csv','.rtf','.pptx'}
        files = []
        for p in Path(folder).rglob('*'):
            if p.is_file() and p.suffix.lower() in supported:
                files.append(str(p))
        return files

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls(): e.accept(); self.dragging = True; self.update()
    def dragLeaveEvent(self, e): self.dragging = False; self.update()
    def dropEvent(self, e):
        self.dragging = False; self.update()
        all_paths = []
        for u in e.mimeData().urls():
            if not u.isLocalFile(): continue
            p = Path(u.toLocalFile())
            if p.is_dir():
                all_paths.extend(self._scan_folder(str(p)))
            else:
                all_paths.append(str(p))
        if all_paths: self.files_dropped.emit(all_paths)
    def paintEvent(self, e):
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = QColor(ACCENT) if self.dragging else QColor(BORDER)
        p.setPen(QPen(color, 2, Qt.PenStyle.DashLine))
        bg = QColor(ACCENT); bg.setAlpha(30 if self.dragging else 0); p.setBrush(bg)
        p.drawRoundedRect(self.rect().adjusted(3,3,-3,-3), 10, 10)


# ── File Card ────────────────────────────────────────────────────────────────
class FileCard(QFrame):
    analyze_requested = pyqtSignal(str)
    remove_requested  = pyqtSignal(str)
    selected          = pyqtSignal(str)
    def __init__(self, info):
        super().__init__(); self.info = info
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setCursor(Qt.CursorShape.PointingHandCursor); self._build(); self._set_style(False)
    def _build(self):
        lay = QHBoxLayout(self); lay.setContentsMargins(10,8,10,8); lay.setSpacing(10)
        icon = QLabel(ICONS[self.info['type']]); icon.setStyleSheet("font-size:20px;"); icon.setFixedWidth(28)
        il = QVBoxLayout(); il.setSpacing(2)
        self.name_lbl = QLabel(self.info['name']); self.name_lbl.setStyleSheet("font-weight:600; font-size:13px;")
        meta = QLabel(f"{self.info['type'].capitalize()} · {self.info['size']}"); meta.setObjectName("dim")
        il.addWidget(self.name_lbl); il.addWidget(meta)
        self.status_lbl = QLabel("—"); self.status_lbl.setStyleSheet(f"color:{TDIM}; font-size:11px; min-width:80px;")
        self.status_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        ba = QPushButton("▶"); ba.setFixedSize(30,30); ba.setCursor(Qt.CursorShape.PointingHandCursor)
        ba.clicked.connect(lambda: self.analyze_requested.emit(self.info['path']))
        br = QPushButton("✕"); br.setObjectName("secondary"); br.setFixedSize(30,30)
        br.setCursor(Qt.CursorShape.PointingHandCursor)
        br.clicked.connect(lambda: self.remove_requested.emit(self.info['path']))
        lay.addWidget(icon); lay.addLayout(il,1); lay.addWidget(self.status_lbl); lay.addWidget(ba); lay.addWidget(br)
    def _set_style(self, sel):
        bg = ACCENT2 if sel else CARD; hv = '#005a9e' if sel else '#484848'
        self.setStyleSheet(f"FileCard{{background:{bg};border-radius:8px;}} FileCard:hover{{background:{hv};}}")
    def set_selected(self, v): self._set_style(v)
    def set_status(self, t, c=TDIM):
        self.status_lbl.setText(t); self.status_lbl.setStyleSheet(f"color:{c}; font-size:11px; min-width:80px;")
    def mousePressEvent(self, e): self.selected.emit(self.info['path']); super().mousePressEvent(e)


# ── Log Panel ────────────────────────────────────────────────────────────────
class LogPanel(QWidget):
    def __init__(self):
        super().__init__(); self.setFixedHeight(158); self._build()

    def _build(self):
        lay = QVBoxLayout(self); lay.setContentsMargins(0,0,0,0); lay.setSpacing(0)

        hdr = QWidget(); hdr.setFixedHeight(30)
        hdr.setStyleSheet(f"background:{SURFACE}; border-top:1px solid {BORDER};")
        hl = QHBoxLayout(hdr); hl.setContentsMargins(14,0,14,0)

        self.spin_lbl = QLabel(""); self.spin_lbl.setFixedWidth(18)
        self.spin_lbl.setStyleSheet(f"color:{ACCENT}; font-size:13px;")
        title = QLabel("Journal d'activite"); title.setStyleSheet(f"color:{TDIM}; font-size:12px; font-weight:600;")
        self.model_badge = QLabel(""); self.model_badge.setStyleSheet(f"color:{ACCENT}; font-size:11px; font-weight:700;")
        clr = QLabel("Effacer"); clr.setStyleSheet(f"color:{TDIM}; font-size:11px;")
        clr.setCursor(Qt.CursorShape.PointingHandCursor); clr.mousePressEvent = lambda e: self.log_view.clear()

        hl.addWidget(self.spin_lbl); hl.addWidget(title); hl.addSpacing(14)
        hl.addWidget(self.model_badge); hl.addStretch(); hl.addWidget(clr)

        self.log_view = QTextEdit(); self.log_view.setReadOnly(True)
        self.log_view.setStyleSheet(f"""
            QTextEdit {{
                background:#141414; border:none; padding:6px 14px; color:#c8c8c8;
                font-family:'Consolas','Courier New',monospace; font-size:12px;
            }}
        """)

        self._frames = ["◐","◓","◑","◒"]; self._fi = 0
        self._timer = QTimer(); self._timer.timeout.connect(self._tick); self._timer.setInterval(110)

        lay.addWidget(hdr); lay.addWidget(self.log_view, 1)

    def _tick(self):
        self._fi = (self._fi+1) % len(self._frames)
        self.spin_lbl.setText(self._frames[self._fi])

    def set_model(self, model):
        self.model_badge.setText(f"Modele actif : {model}")

    def log(self, msg, level="info"):
        ts = datetime.now().strftime("%H:%M:%S")
        cfg = {
            "info":    ("#a0a0a0", "·"),
            "step":    ("#0078d4", "▶"),
            "success": ("#4caf50", "✓"),
            "warning": ("#ff9800", "⚡"),
            "error":   ("#e74c3c", "✗"),
            "ai":      ("#9c6ef5", "🤖"),
        }
        color, icon = cfg.get(level, ("#a0a0a0","·"))
        html = (f'<span style="color:#484848;">[{ts}]</span> '
                f'<span style="color:{color}; font-weight:bold;">{icon}</span> '
                f'<span style="color:{color};">{msg}</span>')
        self.log_view.append(html)
        sb = self.log_view.verticalScrollBar(); sb.setValue(sb.maximum())

    def set_busy(self, busy):
        if busy: self._timer.start(); self.spin_lbl.setText(self._frames[0])
        else: self._timer.stop(); self.spin_lbl.setText("")


# ── Result Panel ─────────────────────────────────────────────────────────────
class ResultPanel(QWidget):
    ask_question    = pyqtSignal(str, str, list)  # (context, question, history)
    global_requested = pyqtSignal()
    def __init__(self):
        super().__init__()
        # Contenus cumulatifs — remplis pendant l'analyse batch
        self._acc_content  = ''
        self._acc_summary  = ''
        self._acc_analysis = ''
        self._build()
    def _build(self):
        lay = QVBoxLayout(self); lay.setContentsMargins(0,0,0,0); lay.setSpacing(10)
        hdr = QHBoxLayout()
        self.title_lbl = QLabel("Selectionnez un fichier et cliquez sur  ▶"); self.title_lbl.setObjectName("dim")
        self.export_btn = QPushButton("Exporter"); self.export_btn.setObjectName("secondary")
        self.export_btn.setFixedWidth(100); self.export_btn.clicked.connect(self._export)
        hdr.addWidget(self.title_lbl,1); hdr.addWidget(self.export_btn)
        self.prog_lbl = QLabel(); self.prog_lbl.setObjectName("dim"); self.prog_lbl.hide()
        self.prog_bar = QProgressBar(); self.prog_bar.setRange(0,0); self.prog_bar.setFixedHeight(5); self.prog_bar.hide()
        self.tabs = QTabWidget()
        self.trans_edit    = self._edit(True,  "Transcription / contenu extrait...")
        self.summary_edit  = self._edit(False, "Resume genere par l'IA...")
        self.analysis_edit = self._edit(False, "Analyse approfondie par l'IA...")
        # ── Onglet Q&R — conversation persistante ────────────────
        qa = QWidget(); ql = QVBoxLayout(qa); ql.setContentsMargins(8,8,8,8); ql.setSpacing(6)

        # Barre d'outils conversation
        qa_toolbar = QHBoxLayout()
        self._qa_scope_btn = QPushButton("📂  Tout le dossier")
        self._qa_scope_btn.setCheckable(True); self._qa_scope_btn.setChecked(True)
        self._qa_scope_btn.setToolTip("Actif : questions sur tous les documents analysés\n"
                                      "Inactif : questions sur le document affiché uniquement")
        self._qa_scope_btn.setFixedHeight(28)
        self._qa_scope_btn.setStyleSheet(
            f"QPushButton{{background:{ACCENT};color:white;border:none;border-radius:5px;"
            f"font-size:11px;padding:0 10px;}}"
            f"QPushButton:!checked{{background:{CARD};color:{TDIM};border:1px solid {BORDER};}}"
            f"QPushButton:hover{{background:{ACCENT2};}}"
        )
        qa_clr = QPushButton("🗑  Effacer la conversation")
        qa_clr.setObjectName("secondary"); qa_clr.setFixedHeight(28)
        qa_clr.clicked.connect(self._clear_qa)
        qa_toolbar.addWidget(QLabel("Portée :"))
        qa_toolbar.addWidget(self._qa_scope_btn)
        qa_toolbar.addStretch()
        qa_toolbar.addWidget(qa_clr)
        ql.addLayout(qa_toolbar)

        # Historique de la conversation
        self._qa_history = []   # liste de dict {role, content}
        self.qa_history_view = QTextEdit()
        self.qa_history_view.setReadOnly(True)
        self.qa_history_view.setStyleSheet(
            f"QTextEdit{{background:#181818;border:1px solid {BORDER};border-radius:8px;"
            f"padding:10px;color:{TEXT};font-size:13px;}}"
        )
        self.qa_history_view.setPlaceholderText(
            "💬  Posez une question sur votre dossier.\n\n"
            "L'IA a accès à tous les documents analysés et se souvient de vos échanges précédents."
        )
        ql.addWidget(self.qa_history_view, 1)

        # Zone de saisie
        input_row = QHBoxLayout(); input_row.setSpacing(8)
        self.qa_input = QTextEdit()
        self.qa_input.setPlaceholderText("Posez votre question ici… (Entrée pour envoyer, Maj+Entrée pour nouvelle ligne)")
        self.qa_input.setFixedHeight(72)
        self.qa_input.setStyleSheet(
            f"QTextEdit{{background:{SURFACE};border:1px solid {ACCENT};border-radius:8px;"
            f"padding:8px;color:{TEXT};font-size:13px;}}"
        )
        self.qa_input.installEventFilter(self)
        send_btn = QPushButton("➤"); send_btn.setFixedSize(72, 72)
        send_btn.setStyleSheet(
            f"QPushButton{{background:{ACCENT};color:white;border:none;border-radius:8px;"
            f"font-size:20px;}} QPushButton:hover{{background:{ACCENT2};}}"
        )
        send_btn.clicked.connect(self._send_qa)
        input_row.addWidget(self.qa_input, 1); input_row.addWidget(send_btn)
        ql.addLayout(input_row)
        # Onglet Synthese Globale
        global_w = QWidget(); gl = QVBoxLayout(global_w); gl.setContentsMargins(8,8,8,8); gl.setSpacing(8)
        global_hdr = QHBoxLayout()
        global_info = QLabel("Synthese de toutes les analyses approfondies de vos documents.")
        global_info.setObjectName("dim"); global_info.setWordWrap(True)
        self.global_btn = QPushButton("🌐  Lancer la synthese globale")
        self.global_btn.setFixedWidth(220)
        self.global_btn.clicked.connect(self._request_global)
        global_hdr.addWidget(global_info,1); global_hdr.addWidget(self.global_btn)
        self.global_edit = self._edit(False, "Lancez la synthese globale apres avoir analyse plusieurs documents...\n\nL'IA va croiser toutes les analyses individuelles pour en extraire une vue d'ensemble coherente.")
        gl.addLayout(global_hdr); gl.addWidget(self.global_edit,1)

        self.tabs.addTab(self.trans_edit,    "📝 Contenu")
        self.tabs.addTab(self.summary_edit,  "📋 Resume")
        self.tabs.addTab(self.analysis_edit, "🔍 Analyse")
        self.tabs.addTab(global_w,           "🌐 Synthese Globale")
        self.tabs.addTab(qa,                 "💬 Q&R")
        lay.addLayout(hdr); lay.addWidget(self.prog_lbl); lay.addWidget(self.prog_bar); lay.addWidget(self.tabs,1)

    @staticmethod
    def _edit(editable=False, ph=""):
        e = QTextEdit(); e.setReadOnly(not editable); e.setPlaceholderText(ph); return e

    def show_progress(self, msg): self.prog_lbl.setText(f"⏳  {msg}"); self.prog_lbl.show(); self.prog_bar.show()
    def hide_progress(self): self.prog_lbl.hide(); self.prog_bar.hide()
    def set_file(self, info):
        self.title_lbl.setText(f"📄  {info['name']}")
        self.trans_edit.setPlainText(info.get('content',''))
        self.summary_edit.setMarkdown(info.get('summary',''))
        self.analysis_edit.setMarkdown(info.get('analysis',''))
    def set_content(self, t): self.trans_edit.setPlainText(t); self.tabs.setCurrentIndex(0)
    def set_summary(self, t): self.summary_edit.setMarkdown(t); self.tabs.setCurrentIndex(1)
    def set_analysis(self, t): self.analysis_edit.setMarkdown(t); self.tabs.setCurrentIndex(2)
    def set_global(self, t): self.global_edit.setMarkdown(t); self.tabs.setCurrentIndex(3)
    def _request_global(self): self.global_requested.emit()

    def reset_accumulated(self):
        """Remet à zéro les vues cumulatives au démarrage d'un nouveau batch."""
        self._acc_content = self._acc_summary = self._acc_analysis = ''
        self.trans_edit.setPlainText('')
        self.summary_edit.setMarkdown('')
        self.analysis_edit.setMarkdown('')
        self.title_lbl.setText("Analyse en cours...")

    def append_to_tab(self, tab_key: str, filename: str, text: str):
        """Ajoute du contenu à un onglet avec en-tête fichier — vue cumulative scrollable."""
        sep = f"\n---\n## 📄  {filename}\n\n"
        if tab_key == 'content':
            self._acc_content += sep + text
            self.trans_edit.setPlainText(self._acc_content.lstrip())
            self._scroll_to_bottom(self.trans_edit)
            self.tabs.setCurrentIndex(0)
            self.title_lbl.setText(f"📝  Transcriptions / Extractions — {filename}")
        elif tab_key == 'summary':
            self._acc_summary += sep + text
            self.summary_edit.setMarkdown(self._acc_summary.lstrip())
            self._scroll_to_bottom(self.summary_edit)
            self.tabs.setCurrentIndex(1)
            self.title_lbl.setText(f"📋  Résumés — {filename}")
        elif tab_key == 'analysis':
            self._acc_analysis += sep + text
            self.analysis_edit.setMarkdown(self._acc_analysis.lstrip())
            self._scroll_to_bottom(self.analysis_edit)
            self.tabs.setCurrentIndex(2)
            self.title_lbl.setText(f"🔍  Analyses — {filename}")

    @staticmethod
    def _scroll_to_bottom(edit):
        sb = edit.verticalScrollBar(); sb.setValue(sb.maximum())
    def get_content(self): return self.trans_edit.toPlainText()
    def get_qa_scope_all(self): return self._qa_scope_btn.isChecked()

    def eventFilter(self, obj, event):
        """Entrée = envoyer, Maj+Entrée = nouvelle ligne dans qa_input."""
        if obj is self.qa_input and event.type() == QEvent.Type.KeyPress:
            # En PyQt6, l'event est déjà un QKeyEvent quand le type est KeyPress
            if (event.key() == Qt.Key.Key_Return
                    and not (event.modifiers() & Qt.KeyboardModifier.ShiftModifier)):
                self._send_qa()
                return True
        return super().eventFilter(obj, event)

    def _send_qa(self):
        q = self.qa_input.toPlainText().strip()
        if not q: return
        c = self.get_content()
        if not c and not self._qa_history:
            QMessageBox.warning(self, "Aucun contenu",
                "Analysez d'abord au moins un fichier avant de poser une question.")
            return
        self.qa_input.clear()
        self._qa_history.append({'role': 'user', 'content': q})
        self._render_qa_history()
        self.ask_question.emit(c, q, list(self._qa_history))

    def _render_qa_history(self, pending=True):
        """Affiche l'historique en HTML dans qa_history_view."""
        html = ""
        for msg in self._qa_history:
            if msg['role'] == 'user':
                html += (
                    f"<div style='margin:8px 0 4px 0;'>"
                    f"<span style='color:#7ec8e3;font-weight:700;font-size:12px;'>Vous</span><br>"
                    f"<span style='background:#2a2a3a;border-radius:6px;padding:6px 10px;"
                    f"display:inline-block;max-width:90%;'>{msg['content']}</span></div>"
                )
            else:
                content = msg['content'].replace('\n', '<br>')
                html += (
                    f"<div style='margin:4px 0 12px 0;'>"
                    f"<span style='color:#7ed6a0;font-weight:700;font-size:12px;'>IA</span><br>"
                    f"<span style='background:#1e2e1e;border-radius:6px;padding:6px 10px;"
                    f"display:inline-block;max-width:95%;'>{content}</span></div>"
                )
        if pending and self._qa_history and self._qa_history[-1]['role'] == 'user':
            html += "<div style='color:#888;font-style:italic;margin:4px 8px;'>⏳  Génération de la réponse…</div>"
        self.qa_history_view.setHtml(f"<body style='font-family:sans-serif;font-size:13px;'>{html}</body>")
        # Scroll to bottom
        sb = self.qa_history_view.verticalScrollBar()
        sb.setValue(sb.maximum())

    def add_qa_answer(self, answer):
        """Appelé par MainWindow quand la réponse arrive."""
        self._qa_history.append({'role': 'assistant', 'content': answer})
        self._render_qa_history(pending=False)

    def _clear_qa(self):
        self._qa_history.clear()
        self.qa_history_view.clear()

    # Garde la compatibilité avec l'ancien code qui appelait set_qa_answer
    def set_qa_answer(self, t): self.add_qa_answer(t)
    def _export(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Exporter", f"analyse_{datetime.now():%Y%m%d_%H%M%S}.txt", "Texte (*.txt)")
        if not path: return

        # Reconstruction de la conversation Q&R depuis l'historique
        qa_text = ""
        for msg in self._qa_history:
            if msg['role'] == 'user':
                qa_text += f"Question : {msg['content']}\n\n"
            else:
                qa_text += f"Réponse : {msg['content']}\n\n{'─'*40}\n\n"

        sections = [
            ("CONTENU",           self.trans_edit.toPlainText()),
            ("RESUME",            self.summary_edit.toPlainText()),
            ("ANALYSE",           self.analysis_edit.toPlainText()),
            ("SYNTHESE GLOBALE",  self.global_edit.toPlainText()),
            ("CONVERSATION Q&R",  qa_text.strip()),
        ]
        with open(path, 'w', encoding='utf-8') as f:
            first = True
            for title, content in sections:
                if not content.strip():
                    continue
                if not first:
                    f.write("\n\n")
                f.write(f"{'='*60}\n=== {title} ===\n{'='*60}\n\n")
                f.write(content)
                first = False
        QMessageBox.information(self, "Exporte", f"Sauvegarde :\n{path}")


# ── Domaines juridiques avec prompts experts ────────────────────────────────
LEGAL_DOMAINS = [
    {
        'id': 'famille',
        'label': '👨‍👩‍👧  Famille',
        'desc': 'Divorce, garde, pension, adoption, succession familiale',
        'prompt': (
            "Tu es un expert senior en droit de la famille ET en psychologie judiciaire, "
            "spécialisé dans l'analyse de conflits conjugaux et parentaux complexes. "
            "Tu as une expérience avancée dans la détection de manipulation, de victimisation inversée "
            "et de stratégies d'évitement des responsabilités parentales.\n\n"
            "CADRE D'ANALYSE OBLIGATOIRE — structure ta réponse en 4 niveaux :\n\n"
            "1. FAITS OBJECTIFS : Ce qui est documenté, daté, vérifiable. "
            "Sépare strictement les faits des interprétations. "
            "Identifie qui parle, à qui, dans quel contexte et dans quel intérêt.\n\n"
            "2. MÉCANISMES DÉTECTÉS : Analyse psychologique et comportementale. "
            "Recherche : victimisation inversée (DARVO), chantage affectif, dramatisation stratégique, "
            "manipulation par les enfants, déresponsabilisation parentale, "
            "instrumentalisation des tiers, menaces sans suite, double discours. "
            "Cite les passages précis du document qui illustrent chaque mécanisme.\n\n"
            "3. CONTRADICTIONS ET INCOHÉRENCES : Compare ce qui est dit avec ce qui est fait. "
            "Identifie les contradictions internes, les affirmations non étayées, "
            "les silences significatifs sur les responsabilités réelles, "
            "notamment envers les enfants (besoins médicaux, scolaires, financiers).\n\n"
            "4. EXPLOITABILITÉ JURIDIQUE : Classe chaque élément en : "
            "EXPLOITABLE (preuve, aveu, engagement), CONTEXTUEL (utile mais non décisif), "
            "ou NON EXPLOITABLE (rhétorique pure). "
            "Identifie les articles du Code civil applicables (autorité parentale, "
            "pension alimentaire, résidence habituelle, prestation compensatoire). "
            "Signale les éléments qui renforcent ou affaiblissent la position de chaque partie."
        ),
    },
    {
        'id': 'immobilier',
        'label': '🏠  Immobilier',
        'desc': 'Achat/vente, bail, copropriété, construction, litige locatif',
        'prompt': (
            "Tu es un expert senior en droit immobilier et en contentieux locatif, "
            "spécialisé dans la détection des clauses abusives, des vices cachés "
            "et des stratégies dilatoires dans les litiges immobiliers.\n\n"
            "CADRE D'ANALYSE OBLIGATOIRE — structure ta réponse en 4 niveaux :\n\n"
            "1. FAITS OBJECTIFS : Identifie le type de document (bail, promesse, acte, courrier), "
            "les parties, les biens concernés, les dates et les montants. "
            "Distingue les obligations contractuelles des engagements verbaux non formalisés.\n\n"
            "2. RISQUES ET ANOMALIES : Détecte les clauses illicites ou abusives, "
            "les manquements aux obligations légales (diagnostics, décence du logement, "
            "état des lieux), les tentatives de contournement de la loi (Alur, Elan, "
            "loi du 6/7/1989), les vices de forme susceptibles d'entraîner la nullité.\n\n"
            "3. RAPPORT DE FORCE ET STRATÉGIES : Analyse qui a l'avantage juridique actuel, "
            "quelles sont les stratégies dilatoires potentielles, "
            "les délais qui jouent pour ou contre chaque partie, "
            "les preuves manquantes qui fragilisent un dossier.\n\n"
            "4. EXPLOITABILITÉ JURIDIQUE : Actions concrètes disponibles, "
            "délais légaux impératifs (prescription, recours), "
            "juridictions compétentes (tribunal judiciaire, commission de conciliation, "
            "tribunal administratif pour HLM). "
            "Cite les textes : loi du 6/7/1989, Code de la construction, loi Alur."
        ),
    },
    {
        'id': 'travail',
        'label': '💼  Travail',
        'desc': 'Licenciement, contrat, harcèlement, prud\'hommes, rupture',
        'prompt': (
            "Tu es un expert senior en droit du travail et en contentieux prud'homal, "
            "spécialisé dans la détection du harcèlement, des licenciements abusifs "
            "et des stratégies d'évitement de la responsabilité employeur.\n\n"
            "CADRE D'ANALYSE OBLIGATOIRE — structure ta réponse en 4 niveaux :\n\n"
            "1. FAITS OBJECTIFS : Nature du lien de travail, type de contrat, "
            "chronologie des événements, éléments documentés (courriers, emails, "
            "attestations, fiches de paie). Sépare rigoureusement faits et ressentis.\n\n"
            "2. INFRACTIONS ET ANOMALIES : Identifie les manquements potentiels : "
            "procédure de licenciement viciée, harcèlement moral ou sexuel (L1152-1, L1153-1), "
            "discrimination (L1132-1), non-paiement des heures, violation du droit au repos, "
            "modification unilatérale du contrat. "
            "Signale les pressions, intimidations ou représailles documentées.\n\n"
            "3. STRATÉGIES ET RAPPORT DE FORCE : Qui a initié quoi et pourquoi. "
            "Détecte les tentatives de déstabilisation du salarié, "
            "les mises en scène disciplinaires préparant un licenciement, "
            "ou au contraire les comportements du salarié susceptibles de fragiliser son dossier.\n\n"
            "4. EXPLOITABILITÉ JURIDIQUE : Délais de prescription prud'homale, "
            "éléments constituant un dossier solide vs insuffisant, "
            "indemnités potentiellement réclamables (barème Macron ou hors barème si nullité), "
            "opportunité d'une saisine du CPH, de l'inspection du travail ou du défenseur des droits."
        ),
    },
    {
        'id': 'penal',
        'label': '⚖️  Pénal',
        'desc': 'Infractions, procédure pénale, plainte, défense',
        'prompt': (
            "Tu es un expert senior en droit pénal et en procédure pénale française, "
            "spécialisé dans l'analyse des infractions, la qualification des faits "
            "et la détection des stratégies de défense ou d'accusation.\n\n"
            "CADRE D'ANALYSE OBLIGATOIRE — structure ta réponse en 4 niveaux :\n\n"
            "1. FAITS OBJECTIFS : Chronologie précise, protagonistes, lieux, "
            "éléments matériels documentés. Identifie ce qui relève du constat "
            "vs ce qui relève de l'interprétation ou du témoignage non corroboré.\n\n"
            "2. QUALIFICATION PÉNALE : Pour chaque fait suspect, analyse : "
            "l'élément légal (texte applicable), l'élément matériel (acte commis), "
            "l'élément intentionnel (dol général ou spécial). "
            "Qualifie : crime, délit ou contravention. "
            "Évalue la solidité des charges et les risques de requalification.\n\n"
            "3. STRATÉGIES ET FAILLES : Détecte les incohérences dans les témoignages, "
            "les contradictions entre déclarations, les éléments de preuve potentiellement "
            "irrecevables (obtention illicite, nullité de procédure), "
            "les circonstances aggravantes ou atténuantes non exploitées.\n\n"
            "4. EXPLOITABILITÉ JURIDIQUE : Délais de prescription pénale, "
            "voies de recours (plainte simple, plainte avec constitution de partie civile, "
            "citation directe), juridictions compétentes (tribunal de police, "
            "tribunal correctionnel, cour d'assises). "
            "Cite le Code pénal et le Code de procédure pénale."
        ),
    },
    {
        'id': 'affaires',
        'label': '🏢  Affaires',
        'desc': 'Société, contrat commercial, faillite, concurrence',
        'prompt': (
            "Tu es un expert senior en droit des affaires, droit des sociétés "
            "et en contentieux commercial, spécialisé dans l'analyse des contrats complexes, "
            "des procédures collectives et des conflits entre associés.\n\n"
            "CADRE D'ANALYSE OBLIGATOIRE — structure ta réponse en 4 niveaux :\n\n"
            "1. FAITS OBJECTIFS : Nature juridique des entités, structure capitalistique, "
            "obligations contractuelles précises, dates et montants. "
            "Identifie les engagements fermes vs les engagements de moyens.\n\n"
            "2. RISQUES ET ANOMALIES : Détecte les clauses léonines, "
            "les conflits d'intérêts non déclarés, les actes de gestion anormaux, "
            "les signes précurseurs de difficultés (cessation de paiements, "
            "actif insuffisant), les abus de majorité ou de minorité, "
            "les pratiques anticoncurrentielles.\n\n"
            "3. RESPONSABILITÉS ET STRATÉGIES : Qui engage sa responsabilité, "
            "personnelle ou solidaire. Détecte les tentatives de dilution de responsabilité, "
            "les montages visant à organiser l'insolvabilité, "
            "les stratégies de rétention d'information ou de contournement contractuel.\n\n"
            "4. EXPLOITABILITÉ JURIDIQUE : Actions disponibles (nullité, résiliation, "
            "action en responsabilité, action paulienne, déclaration de cessation des paiements). "
            "Délais et juridictions (tribunal de commerce, tribunal judiciaire). "
            "Cite le Code de commerce et le Code civil."
        ),
    },
    {
        'id': 'succession',
        'label': '📜  Succession',
        'desc': 'Testament, héritage, notariat, indivision, donation',
        'prompt': (
            "Tu es un expert senior en droit des successions, des libéralités "
            "et en fiscalité successorale, spécialisé dans les conflits entre héritiers "
            "et la détection des manœuvres frauduleuses ou des captations d'héritage.\n\n"
            "CADRE D'ANALYSE OBLIGATOIRE — structure ta réponse en 4 niveaux :\n\n"
            "1. FAITS OBJECTIFS : Identifie le de cujus, les héritiers légaux et leurs rangs, "
            "l'existence d'un testament (authentique ou olographe), "
            "les donations antérieures et leur date, la composition de l'actif successoral.\n\n"
            "2. ANOMALIES ET RISQUES DE CONTESTATION : Détecte les atteintes à la réserve héréditaire, "
            "les testaments potentiellement viciés (hors formes, captation de volonté, "
            "rédaction sous influence), les donations déguisées, "
            "les recelements successoraux, les conflits d'intérêts du notaire ou d'un héritier.\n\n"
            "3. DYNAMIQUES FAMILIALES ET STRATÉGIES : Identifie les rapports de force entre héritiers, "
            "les tentatives d'écarter certains héritiers, "
            "les blocages d'indivision utilisés comme levier, "
            "les manipulations d'un héritier sur le défunt en fin de vie.\n\n"
            "4. EXPLOITABILITÉ JURIDIQUE : Action en réduction, action en recel successoral, "
            "demande de rapport des donations, contestation du testament. "
            "Délais de prescription (5 ans pour la réduction). "
            "Cite les articles du Code civil (720 à 892). "
            "Fiscalité : abattements, taux, déclaration dans les 6 mois."
        ),
    },
    {
        'id': 'fiscal',
        'label': '💰  Fiscal',
        'desc': 'Impôts, contrôle fiscal, redressement, TVA, ISF',
        'prompt': (
            "Tu es un expert senior en droit fiscal français et en contentieux fiscal, "
            "spécialisé dans les procédures de redressement, la détection de la fraude "
            "et la défense des contribuables face à l'administration fiscale.\n\n"
            "CADRE D'ANALYSE OBLIGATOIRE — structure ta réponse en 4 niveaux :\n\n"
            "1. FAITS OBJECTIFS : Identifie le type d'imposition en cause, "
            "les périodes fiscales concernées, les montants, "
            "les documents officiels (avis de redressement, proposition de rectification, "
            "mise en demeure). Distingue les erreurs déclaratives des omissions délibérées.\n\n"
            "2. RISQUES ET IRRÉGULARITÉS : Évalue la solidité du redressement ou de la situation. "
            "Détecte les vices de procédure (non-respect des délais, "
            "insuffisance de motivation, violation du contradictoire), "
            "les qualifications abusives (acte anormal de gestion, abus de droit). "
            "Identifie les risques de pénalités et leur taux (40% mauvaise foi, 80% manœuvres).\n\n"
            "3. ARGUMENTS DE DÉFENSE ET STRATÉGIES : Quels moyens opposer à l'administration. "
            "Doctrine administrative favorable (rescrits, réponses ministérielles, "
            "BOFiP), jurisprudence applicable, "
            "possibilités de transaction ou de modération des pénalités.\n\n"
            "4. EXPLOITABILITÉ JURIDIQUE : Délais de réclamation (31/12 de la 2e année suivant la mise en recouvrement), "
            "voies de recours (réclamation préalable, tribunal administratif, CAA, CE), "
            "opportunité du recours hiérarchique ou de la saisine du Médiateur des finances. "
            "Cite le CGI et le Livre des procédures fiscales (LPF)."
        ),
    },
    {
        'id': 'consommation',
        'label': '🛒  Consommation',
        'desc': 'Litiges, remboursement, garanties, crédit, démarchage',
        'prompt': (
            "Tu es un expert senior en droit de la consommation et en pratiques commerciales déloyales, "
            "spécialisé dans la détection des clauses abusives, "
            "des arnaques au démarchage et des litiges de garantie.\n\n"
            "CADRE D'ANALYSE OBLIGATOIRE — structure ta réponse en 4 niveaux :\n\n"
            "1. FAITS OBJECTIFS : Identifie le type de relation commerciale, "
            "les produits ou services concernés, les dates (commande, livraison, signalement), "
            "les montants et les preuves d'achat disponibles.\n\n"
            "2. INFRACTIONS ET ANOMALIES : Détecte les clauses abusives (liste noire et grise, "
            "R212-1 et R212-2 Code de la consommation), les pratiques commerciales trompeuses "
            "(L121-1 et suivants), les violations du droit de rétractation (L221-18, "
            "14 jours pour la vente à distance), les abus dans le crédit à la consommation "
            "(TAEG, assurances imposées), les refus injustifiés de garantie légale (2 ans).\n\n"
            "3. RAPPORT DE FORCE ET STRATÉGIES DU PROFESSIONNEL : "
            "Identifie les tactiques d'épuisement du consommateur (délais anormaux, "
            "renvois répétés, refus de prise en charge non motivés), "
            "les conditions générales de vente utilisées comme bouclier abusif, "
            "les tentatives de substituer la garantie commerciale à la garantie légale.\n\n"
            "4. EXPLOITABILITÉ JURIDIQUE : Démarches graduées (mise en demeure, médiation, "
            "saisine du médiateur de la consommation — obligatoire avant le tribunal), "
            "action de groupe si problème systémique, signalement DGCCRF. "
            "Évalue l'opportunité d'une procédure judiciaire vs un règlement amiable."
        ),
    },
    {
        'id': 'administratif',
        'label': '🏛️  Administratif',
        'desc': 'Recours, permis, marchés publics, fonction publique',
        'prompt': (
            "Tu es un expert senior en droit administratif et en contentieux administratif, "
            "spécialisé dans les recours contre les décisions de l'administration, "
            "les marchés publics et les litiges de la fonction publique.\n\n"
            "CADRE D'ANALYSE OBLIGATOIRE — structure ta réponse en 4 niveaux :\n\n"
            "1. FAITS OBJECTIFS : Identifie l'acte administratif en cause "
            "(décision, arrêté, refus implicite, contrat administratif), "
            "l'autorité émettrice, la date, les destinataires et les effets juridiques. "
            "Distingue les actes unilatéraux des actes contractuels.\n\n"
            "2. ILLÉGALITÉS ET VICES : Analyse selon les 4 cas d'ouverture du recours pour excès de pouvoir : "
            "incompétence, vice de forme, violation de la loi, détournement de pouvoir. "
            "Détecte les erreurs de droit, les erreurs manifestes d'appréciation, "
            "le défaut de motivation (loi du 11/7/1979), la méconnaissance du contradictoire.\n\n"
            "3. STRATÉGIES ET PRESSIONS ADMINISTRATIVES : "
            "Identifie les pratiques dilatoires de l'administration, "
            "les décisions tardives ou implicites, les pressions sur les agents "
            "ou administrés, les incohérences entre décisions du même service.\n\n"
            "4. EXPLOITABILITÉ JURIDIQUE : Délais IMPÉRATIFS (2 mois pour le REP, "
            "computation précise depuis la notification/publication). "
            "Voies de recours (recours gracieux/hiérarchique, TA, CAA, CE, CADA pour l'accès aux documents). "
            "Référé suspension si urgence (L521-1 CJA). "
            "Évalue les chances de succès et l'opportunité d'un recours préalable obligatoire (RAPO)."
        ),
    },
    {
        'id': 'international',
        'label': '🌍  International / Expatrié',
        'desc': 'Droit international privé, offshore, trust, expatriation',
        'prompt': (
            "Tu es un expert senior en droit international privé, en fiscalité internationale "
            "et en droit des situations transfrontalières, spécialisé dans les conflits "
            "de lois et de juridictions, les structures offshore et l'expatriation.\n\n"
            "CADRE D'ANALYSE OBLIGATOIRE — structure ta réponse en 4 niveaux :\n\n"
            "1. FAITS OBJECTIFS : Identifie les éléments d'extranéité "
            "(nationalités, domiciles, lieux des actes/biens/événements), "
            "les juridictions potentiellement compétentes et les lois potentiellement applicables. "
            "Identifie les conventions internationales en jeu (La Haye, bilatérales, UE).\n\n"
            "2. CONFLITS ET RISQUES : Détecte les conflits de juridictions, "
            "les risques de double imposition ou de double non-imposition, "
            "les structures potentiellement requalifiables (trust, holding, "
            "société fictive), les risques de fraude fiscale internationale "
            "(échange automatique d'informations CRS/FATCA), "
            "les problèmes de reconnaissance et d'exécution de jugements étrangers.\n\n"
            "3. STRATÉGIES TRANSFRONTALIÈRES : Identifie si des montages ont été mis en place "
            "pour soustraire des biens ou des revenus à une juridiction, "
            "les stratégies de forum shopping, les tentatives d'utiliser "
            "une juridiction favorable pour contourner des droits acquis dans une autre.\n\n"
            "4. EXPLOITABILITÉ JURIDIQUE : Loi applicable selon les règlements européens "
            "(Rome I et II, Bruxelles I bis, règlement successions 650/2012). "
            "Obligations déclaratives françaises (comptes étrangers, trusts, "
            "participations dans des entités étrangères). "
            "Délais de prescription allongés en matière internationale. "
            "Évalue l'opportunité d'une procédure amiable préalable ou d'une saisine directe."
        ),
    },
]

# ── Widget sélecteur de domaine ──────────────────────────────────────────────
class DomainSelector(QWidget):
    domain_selected = pyqtSignal(str, str)   # (domain_id, prompt_text)

    def __init__(self):
        super().__init__()
        self._active = None
        self._build()

    def _build(self):
        lay = QVBoxLayout(self); lay.setContentsMargins(0, 0, 0, 0); lay.setSpacing(4)

        # En-tête avec toggle collapse
        hdr = QHBoxLayout(); hdr.setSpacing(6)
        self._toggle_btn = QPushButton("▾  ⚖️  Domaine juridique")
        self._toggle_btn.setCheckable(True); self._toggle_btn.setChecked(True)
        self._toggle_btn.setStyleSheet(
            f"QPushButton{{background:transparent;color:{TEXT};border:none;"
            f"font-size:13px;font-weight:700;text-align:left;padding:0;}}"
            f"QPushButton:hover{{color:{ACCENT};}}"
        )
        self._toggle_btn.clicked.connect(self._toggle)
        rst = QLabel("Réinitialiser")
        rst.setStyleSheet(f"color:{TDIM}; font-size:11px;")
        rst.setCursor(Qt.CursorShape.PointingHandCursor)
        rst.mousePressEvent = lambda e: self._reset()
        hdr.addWidget(self._toggle_btn, 1); hdr.addWidget(rst)
        lay.addLayout(hdr)

        # Grille 2 colonnes directement sur _body — pas de scroll area imbriquée
        # (c'est le panneau gauche global qui est scrollable)
        self._body = QWidget()
        gl = QGridLayout(self._body)
        gl.setSpacing(5); gl.setContentsMargins(0, 2, 0, 4)

        self._buttons = {}
        for i, d in enumerate(LEGAL_DOMAINS):
            parts = d['label'].split('  ')
            short = f"{parts[0]} {parts[1].strip()}" if len(parts) > 1 else d['label']
            btn = QPushButton(short)
            btn.setCheckable(True)
            btn.setFixedHeight(30)
            btn.setToolTip(f"<b>{d['label'].strip()}</b><br><small>{d['desc']}</small>")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(self._btn_style(False))
            btn.clicked.connect(lambda checked, dom=d: self._on_click(dom))
            self._buttons[d['id']] = btn
            gl.addWidget(btn, i // 2, i % 2)

        # Minimum height calculé : 5 rangées × 30px + 4 espacements × 5px + marges = 180px
        rows = (len(LEGAL_DOMAINS) + 1) // 2
        self._body.setMinimumHeight(rows * 30 + (rows - 1) * 5 + 6)

        lay.addWidget(self._body)

    def _toggle(self):
        visible = self._toggle_btn.isChecked()
        self._body.setVisible(visible)
        arrow = "▾" if visible else "▸"
        txt = self._toggle_btn.text()
        self._toggle_btn.setText(arrow + txt[1:])

    def _btn_style(self, active):
        if active:
            return (
                f"QPushButton{{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,"
                f"stop:0 {ACCENT3},stop:1 {ACCENT});"
                f"color:white;border:none;border-radius:7px;"
                f"font-size:11px;font-weight:700;padding:0 6px;}}"
                f"QPushButton:hover{{background:{ACCENT3};}}"
            )
        return (
            f"QPushButton{{background:{CARD};color:{TEXT};"
            f"border:1px solid {BORDER};border-radius:7px;"
            f"font-size:11px;font-weight:500;padding:0 6px;}}"
            f"QPushButton:hover{{background:{SURFACE};border-color:{ACCENT};"
            f"color:{ACCENT3};}}"
        )

    def _on_click(self, domain):
        if self._active and self._active != domain['id']:
            old = self._buttons.get(self._active)
            if old: old.setChecked(False); old.setStyleSheet(self._btn_style(False))
        btn = self._buttons[domain['id']]
        if self._active == domain['id']:
            btn.setChecked(False); btn.setStyleSheet(self._btn_style(False))
            self._active = None
            self.domain_selected.emit('', '')
        else:
            btn.setChecked(True); btn.setStyleSheet(self._btn_style(True))
            self._active = domain['id']
            self.domain_selected.emit(domain['id'], domain['prompt'])

    def _reset(self):
        for btn in self._buttons.values():
            btn.setChecked(False); btn.setStyleSheet(self._btn_style(False))
        self._active = None
        self.domain_selected.emit('', '')


# ── Persona Editor — cases par intervenant ───────────────────────────────────
class PersonaEditor(QWidget):
    """
    Une case par intervenant : Nom + description libre.
    Le bloc est injecté en tête du prompt pour ancrer les identités.
    """
    def __init__(self):
        super().__init__()
        self._rows = []
        self._build()

    def _build(self):
        lay = QVBoxLayout(self); lay.setContentsMargins(0, 0, 0, 0); lay.setSpacing(4)

        hdr = QHBoxLayout(); hdr.setSpacing(6)
        self._toggle_btn = QPushButton("▸  👥  Intervenants du dossier")
        self._toggle_btn.setCheckable(True); self._toggle_btn.setChecked(False)
        self._toggle_btn.setStyleSheet(
            f"QPushButton{{background:transparent;color:{TEXT};border:none;"
            f"font-size:13px;font-weight:700;text-align:left;padding:0;}}"
            f"QPushButton:hover{{color:{ACCENT};}}"
        )
        self._toggle_btn.clicked.connect(self._toggle)

        add_lbl = QLabel("＋ Ajouter")
        add_lbl.setStyleSheet(f"color:{ACCENT3}; font-size:11px; font-weight:600;")
        add_lbl.setCursor(Qt.CursorShape.PointingHandCursor)
        add_lbl.mousePressEvent = lambda e: self._add_row()

        hdr.addWidget(self._toggle_btn, 1); hdr.addWidget(add_lbl)
        lay.addLayout(hdr)

        self._body = QWidget()
        self._rows_lay = QVBoxLayout(self._body)
        self._rows_lay.setContentsMargins(0, 4, 0, 2); self._rows_lay.setSpacing(6)
        self._body.setVisible(False)
        lay.addWidget(self._body)

    def _toggle(self):
        visible = self._toggle_btn.isChecked()
        self._body.setVisible(visible)
        arrow = "▾" if visible else "▸"
        txt = self._toggle_btn.text()
        self._toggle_btn.setText(arrow + txt[1:])

    def _add_row(self, name="", desc=""):
        # Auto-ouvrir
        if not self._toggle_btn.isChecked():
            self._toggle_btn.setChecked(True); self._toggle()

        row_w = QWidget()
        row_w.setStyleSheet(
            f"QWidget{{background:{CARD};border-radius:8px;}}"
        )
        row_lay = QHBoxLayout(row_w)
        row_lay.setContentsMargins(8, 6, 6, 6); row_lay.setSpacing(6)

        # Nom
        name_e = QLineEdit(); name_e.setPlaceholderText("Prénom Nom")
        name_e.setText(name); name_e.setFixedWidth(110)
        name_e.setStyleSheet(
            f"QLineEdit{{background:{SURFACE};border:1px solid {BORDER};"
            f"border-radius:6px;padding:4px 8px;font-size:12px;font-weight:600;}}"
            f"QLineEdit:focus{{border-color:{ACCENT};}}"
        )

        # Séparateur visuel
        sep = QLabel("·"); sep.setStyleSheet(f"color:{TDIM}; font-size:14px;")

        # Description libre
        desc_e = QLineEdit()
        desc_e.setPlaceholderText("qui est-il dans l'histoire ?")
        desc_e.setText(desc)
        desc_e.setStyleSheet(
            f"QLineEdit{{background:{SURFACE};border:1px solid {BORDER};"
            f"border-radius:6px;padding:4px 8px;font-size:12px;}}"
            f"QLineEdit:focus{{border-color:{ACCENT};}}"
        )

        # Supprimer
        rm = QPushButton("✕"); rm.setFixedSize(22, 22)
        rm.setStyleSheet(
            f"QPushButton{{background:transparent;color:{TDIM};border:none;"
            f"font-size:11px;}} QPushButton:hover{{color:{ERR};}}"
        )
        rm.clicked.connect(lambda: self._remove_row(row_w))

        row_lay.addWidget(name_e)
        row_lay.addWidget(sep)
        row_lay.addWidget(desc_e, 1)
        row_lay.addWidget(rm)

        self._rows.append({'widget': row_w, 'name': name_e, 'desc': desc_e})
        self._rows_lay.addWidget(row_w)

    def _remove_row(self, row_w):
        self._rows = [r for r in self._rows if r['widget'] != row_w]
        row_w.deleteLater()

    def get_persona_block(self) -> str:
        entries = []
        for r in self._rows:
            name = r['name'].text().strip()
            desc = r['desc'].text().strip()
            if name:
                entries.append(f"- {name}{' : ' + desc if desc else ''}")
        if not entries:
            return ""
        return "INTERVENANTS DU DOSSIER :\n" + "\n".join(entries) + "\n\n"

    def clear(self):
        for r in self._rows: r['widget'].deleteLater()
        self._rows.clear()


# ── Main Window ──────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Sudolex {APP_VERSION}")
        self.setMinimumSize(1050, 700); self.resize(1280, 820)
        self.files = {}; self.file_cards = {}; self.selected = None; self.workers = []
        self._analyze_queue    = []    # file d'attente séquentielle
        self._cancel_requested = False # drapeau d'annulation utilisateur
        self.settings = {
            'lmstudio_model': 'mistral',
            'whisper_model':  'base',
            'language':       'fr',
            'engine':         '',          # 'lmstudio' | 'llamacpp' | ''
            'llamacpp_model': '',          # chemin complet du .gguf
        }
        self._load_settings(); self._build(); self._set_icon()
        QTimer.singleShot(400, self._detect_engine)
        # Vérification mise à jour — différée de 3s pour ne pas bloquer le démarrage
        QTimer.singleShot(3000, self._check_update)

    def _build(self):
        central = QWidget(); self.setCentralWidget(central)
        root = QVBoxLayout(central); root.setContentsMargins(0,0,0,0); root.setSpacing(0)

        # ── Header Sudolex ───────────────────────────────────────────────────
        hdr = QWidget(); hdr.setFixedHeight(62)
        hdr.setStyleSheet(
            f"background:{SURFACE};"
            f"border-bottom:1px solid {BORDER};"
        )
        hl = QHBoxLayout(hdr); hl.setContentsMargins(20, 0, 20, 0); hl.setSpacing(0)

        # Logo + subtitle
        logo_w = QWidget(); logo_lay = QVBoxLayout(logo_w)
        logo_lay.setContentsMargins(0,0,0,0); logo_lay.setSpacing(2)

        # Logo PNG (blanc en dark, noir en light) — fallback texte si fichier absent
        self._logo_lbl = QLabel()
        self._logo_lbl.setFixedHeight(36)
        self._load_logo_image(self.settings.get('theme', 'dark'))

        logo_sub = QLabel("Intelligence documentaire locale")
        logo_sub.setStyleSheet(
            f"color:{TDIM};font-size:9px;font-weight:500;letter-spacing:1.8px;"
        )
        logo_lay.addWidget(self._logo_lbl); logo_lay.addWidget(logo_sub)

        # Modèle actif
        self.model_lbl = QLabel(f"Modèle : {self.settings['lmstudio_model']}")
        self.model_lbl.setStyleSheet(
            f"color:{ACCENT3};font-size:11px;font-weight:600;"
            f"padding:4px 10px;background:{CARD};"
            f"border-radius:12px;border:1px solid {BORDER};"
        )
        self.model_lbl.setCursor(Qt.CursorShape.PointingHandCursor)
        self.model_lbl.setToolTip("Cliquer pour changer de modèle")
        self.model_lbl.mousePressEvent = lambda e: self._show_model_picker()

        # Statut
        self.stat_lbl = QLabel("Prêt"); self.stat_lbl.setObjectName("dim")

        # Bouton toggle thème
        self._theme_mode = self.settings.get('theme', 'dark')
        self._btn_theme = QPushButton("☀" if self._theme_mode == 'dark' else "🌙")
        self._btn_theme.setObjectName("secondary")
        self._btn_theme.setFixedSize(36, 36)
        self._btn_theme.setToolTip("Basculer thème clair / sombre")
        self._btn_theme.clicked.connect(self._toggle_theme)

        btn_mdl = QPushButton("Changer modèle")
        btn_mdl.setObjectName("secondary"); btn_mdl.setFixedWidth(130)
        btn_mdl.clicked.connect(self._show_model_picker)
        btn_cfg = QPushButton("⚙")
        btn_cfg.setObjectName("secondary"); btn_cfg.setFixedSize(36, 36)
        btn_cfg.setToolTip("Paramètres"); btn_cfg.clicked.connect(self._open_settings)

        hl.addWidget(logo_w)
        hl.addSpacing(18); hl.addWidget(self.model_lbl)
        hl.addStretch()
        hl.addWidget(self.stat_lbl); hl.addSpacing(12)
        hl.addWidget(self._btn_theme); hl.addSpacing(6)
        hl.addWidget(btn_mdl); hl.addSpacing(6); hl.addWidget(btn_cfg)

        # ── Bandeau mise à jour (caché par défaut) ──────────────────────────
        self._update_bar = QWidget(); self._update_bar.setVisible(False)
        self._update_bar.setStyleSheet(
            f"background:qlineargradient(x1:0,y1:0,x2:1,y2:0,"
            f"stop:0 {ACCENT2},stop:1 {ACCENT});"
        )
        ub_lay = QHBoxLayout(self._update_bar)
        ub_lay.setContentsMargins(16, 6, 16, 6); ub_lay.setSpacing(12)
        self._update_lbl = QLabel("🆕  Nouvelle version disponible")
        self._update_lbl.setStyleSheet("color:white; font-size:12px; font-weight:600;")
        self._update_url = ""
        btn_dl = QPushButton("Télécharger")
        btn_dl.setStyleSheet(
            "QPushButton{background:white;color:#1D4ED8;border:none;"
            "border-radius:6px;padding:4px 14px;font-weight:700;font-size:11px;}"
            "QPushButton:hover{background:#EFF6FF;}"
        )
        btn_dl.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(self._update_url)))
        btn_close = QPushButton("✕")
        btn_close.setStyleSheet(
            "QPushButton{background:transparent;color:rgba(255,255,255,180);"
            "border:none;font-size:14px;padding:0 4px;}"
            "QPushButton:hover{color:white;}"
        )
        btn_close.setFixedSize(24, 24)
        btn_close.clicked.connect(lambda: self._update_bar.setVisible(False))
        ub_lay.addWidget(self._update_lbl); ub_lay.addStretch()
        ub_lay.addWidget(btn_dl); ub_lay.addWidget(btn_close)

        # Corps
        body = QSplitter(Qt.Orientation.Horizontal); body.setChildrenCollapsible(False)

        left = QWidget(); left.setMinimumWidth(300); left.setMaximumWidth(460)
        ll = QVBoxLayout(left); ll.setContentsMargins(12,12,12,12); ll.setSpacing(8)

        lbl = QLabel("📁  Fichiers"); lbl.setObjectName("h2")
        self.drop_zone = DropZone(); self.drop_zone.files_dropped.connect(self._add_files)

        # ── Partie centrale scrollable ──────────────────────────────────────
        # Mode, domaines, contexte et liste de fichiers sont dans un seul
        # QScrollArea : garantit que tout est accessible sur petits écrans
        # sans jamais rogner les boutons de domaine.
        inner_w = QWidget()
        inner_lay = QVBoxLayout(inner_w)
        inner_lay.setContentsMargins(0, 0, 0, 0); inner_lay.setSpacing(8)

        self.mode_sel = ModeSelector()
        self.domain_sel = DomainSelector()
        self.domain_sel.domain_selected.connect(self._on_domain_selected)

        # ── Intervenants (Dramatis Personae) ────────────────────────────────
        self.persona_editor = PersonaEditor()

        ctx_hdr = QHBoxLayout()
        ctx_lbl = QLabel("Contexte / Instructions pour l'IA")
        ctx_lbl.setStyleSheet("font-size:13px; font-weight:700;")
        ctx_clr = QLabel("Effacer")
        ctx_clr.setStyleSheet(f"color:{TDIM}; font-size:11px;")
        ctx_clr.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ctx_edit = QTextEdit()
        self.ctx_edit.setFixedHeight(80)
        self.ctx_edit.setPlaceholderText(
            "Decrivez ici le contexte pour orienter l\'analyse...\n\n"
            "Exemples :\n"
            "- Dossier juridique : analyser les droits et recours de Mme X\n"
            "- Contrat de bail : reperer les clauses abusives\n"
            "- Reunion : extraire les decisions et actions a suivre"
        )
        self.ctx_edit.setStyleSheet(
            f"QTextEdit{{background:{SURFACE};border:1px solid {ACCENT};border-radius:8px;"
            f"padding:10px;color:{TEXT};font-size:12px;}}"
        )
        ctx_clr.mousePressEvent = lambda e: self.ctx_edit.clear()
        ctx_hdr.addWidget(ctx_lbl, 1); ctx_hdr.addWidget(ctx_clr)

        self.cards_area = QWidget(); self.cards_lay = QVBoxLayout(self.cards_area)
        self.cards_lay.setContentsMargins(0,0,0,0); self.cards_lay.setSpacing(4)
        self.cards_lay.addStretch()
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setWidget(self.cards_area); scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setMinimumHeight(0)

        inner_lay.addWidget(self.mode_sel)
        inner_lay.addWidget(self.domain_sel)
        inner_lay.addWidget(self.persona_editor)
        inner_lay.addLayout(ctx_hdr)
        inner_lay.addWidget(self.ctx_edit)
        inner_lay.addWidget(scroll, 1)

        # Scroll area qui enveloppe toute la partie centrale
        left_scroll = QScrollArea()
        left_scroll.setWidget(inner_w)
        left_scroll.setWidgetResizable(True)
        left_scroll.setFrameShape(QFrame.Shape.NoFrame)
        left_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # ── Boutons (toujours visibles en bas) ──────────────────────────────
        bl = QHBoxLayout()
        self.btn_all = QPushButton("▶  Tout analyser"); self.btn_all.clicked.connect(self._analyze_all)
        self.btn_cancel = QPushButton("⏹  Annuler")
        self.btn_cancel.setObjectName("danger"); self.btn_cancel.setVisible(False)
        self.btn_cancel.clicked.connect(self._cancel_analysis)
        btn_clr = QPushButton("Vider"); btn_clr.setObjectName("secondary"); btn_clr.clicked.connect(self._clear_all)
        bl.addWidget(self.btn_all); bl.addWidget(self.btn_cancel); bl.addWidget(btn_clr)

        ll.addWidget(lbl)
        ll.addWidget(self.drop_zone)
        ll.addWidget(left_scroll, 1)
        ll.addLayout(bl)

        right = QWidget(); rl = QVBoxLayout(right); rl.setContentsMargins(12,12,12,12)
        self.result_panel = ResultPanel()
        self.result_panel.ask_question.connect(self._run_qa)
        self.result_panel.global_requested.connect(self._run_global_analysis)
        rl.addWidget(self.result_panel)

        body.addWidget(left); body.addWidget(right); body.setSizes([340,940])

        # Log panel
        self.log_panel = LogPanel()
        self.log_panel.set_model(self.settings['lmstudio_model'])
        self.log_panel.log("FileAnalyzer AI demarre", "success")
        self.log_panel.log("Glissez des fichiers ou cliquez sur 'Parcourir'", "info")

        root.addWidget(hdr); root.addWidget(self._update_bar)
        root.addWidget(body,1); root.addWidget(self.log_panel)

    def _set_icon(self):
        pm = QPixmap(32,32); pm.fill(QColor(ACCENT)); self.setWindowIcon(QIcon(pm))

    def _on_domain_selected(self, domain_id, prompt):
        """Injecte silencieusement le prompt expert dans la zone de contexte."""
        if not domain_id:
            # Réinitialisation : vider le contexte si c'était un prompt auto
            if hasattr(self, '_domain_prompt_active') and self._domain_prompt_active:
                self.ctx_edit.clear()
            self._domain_prompt_active = False
            return
        self.ctx_edit.setPlainText(prompt)
        self._domain_prompt_active = True
        # Trouver le nom du domaine pour le log
        name = next((d['label'] for d in LEGAL_DOMAINS if d['id'] == domain_id), domain_id)
        self.log_panel.log(f"Domaine : {name} — prompt expert activé", "step")

    # ── Détection / configuration du moteur IA ───────────────────────────────
    def _detect_engine(self):
        engine = self.settings.get('engine', '')
        # Si le moteur est déjà configuré et valide, on l'utilise directement
        if engine == 'lmstudio' and detect_lmstudio():
            self._apply_engine('lmstudio', '', self.settings.get('language', 'fr'))
            self._show_model_picker()
            return
        if engine == 'llamacpp':
            mp = self.settings.get('llamacpp_model', '')
            if mp and Path(mp).exists():
                self._apply_engine('llamacpp', mp)
                return
        # Sinon : tenter LM Studio en silence, sinon ouvrir le wizard
        if detect_lmstudio():
            self._apply_engine('lmstudio', '', self.settings.get('language', 'fr'))
            self._show_model_picker()
        else:
            self._open_setup_wizard()

    def _open_setup_wizard(self):
        dlg = SetupWizard(self)
        dlg.engine_ready.connect(self._apply_engine)
        dlg.exec()

    def _apply_engine(self, engine, model_path, language='fr'):
        self.settings['engine'] = engine
        self.settings['language'] = language
        if engine == 'llamacpp':
            self.settings['llamacpp_model'] = model_path
            name = Path(model_path).stem if model_path else '—'
            self.model_lbl.setText(f"Modele local : {name}")
            self.log_panel.set_model(name)
            self.log_panel.log(f"Moteur : llama.cpp  |  {name}  |  Langue : {language}", "success")
        else:
            self.model_lbl.setText(f"Modele : {self.settings['lmstudio_model']}")
            self.log_panel.set_model(self.settings['lmstudio_model'])
            self.log_panel.log(f"Moteur : LM Studio  |  Langue : {language}", "success")
        self._save_settings()

    def _make_worker(self, text, task, question="", context=""):
        """Instancie le bon worker selon le moteur configuré."""
        engine     = self.settings.get('engine', 'lmstudio')
        model      = self.settings['lmstudio_model']
        model_path = self.settings.get('llamacpp_model', '')
        lang_code  = self.settings.get('language', 'fr')
        # Préfixer le contexte avec le bloc Intervenants si renseigné
        persona_block = self.persona_editor.get_persona_block()
        full_context  = (persona_block + context).strip() if persona_block else context
        return LMStudioWorker(text, model, task,
                              question=question, context=full_context,
                              engine=engine, model_path=model_path,
                              lang_code=lang_code)

    def _show_model_picker(self):
        dlg = ModelPickerDialog(self.settings['lmstudio_model'], self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            model = dlg.get_model()
            if model:
                self.settings['lmstudio_model'] = model
                self.model_lbl.setText(f"Modele : {model}")
                self.log_panel.set_model(model)
                self.log_panel.log(f"Modele change : {model}", "success")
                self._save_settings()

    def _check_update(self):
        """Lance la vérification silencieuse de mise à jour GitHub."""
        w = UpdateCheckerWorker()
        w.update_available.connect(self._show_update_banner)
        w.start(); self._update_worker = w

    def _show_update_banner(self, version, url):
        """Affiche le bandeau de mise à jour."""
        self._update_url = url
        self._update_lbl.setText(
            f"🆕  Sudolex {version} est disponible  —  vous utilisez {APP_VERSION}"
        )
        self._update_bar.setVisible(True)
        self.log_panel.log(f"Mise a jour disponible : v{version}", "warning")

    def _load_logo_image(self, mode):
        """Charge le logo PNG selon le thème — fallback texte si fichier absent."""
        base = Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(__file__).parent
        fname = 'sudolex_logo_white.png' if mode == 'dark' else 'sudolex_logo_black.png'
        logo_path = base / fname
        if logo_path.exists():
            pm = QPixmap(str(logo_path))
            pm = pm.scaledToHeight(36, Qt.TransformationMode.SmoothTransformation)
            self._logo_lbl.setPixmap(pm)
            self._logo_lbl.setFixedWidth(pm.width())
            self._logo_lbl.setText('')
        else:
            # Fallback : texte si PNG absent
            col_sudo = TEXT if mode == 'dark' else '#1A202C'
            self._logo_lbl.setText(
                f'<span style="font-size:20px;font-weight:800;color:{col_sudo};">Sudo</span>'
                f'<span style="font-size:20px;font-weight:800;color:{ACCENT};">lex</span>'
            )
            self._logo_lbl.setTextFormat(Qt.TextFormat.RichText)

    def _toggle_theme(self):
        """Bascule entre thème sombre premium et thème clair classique."""
        self._theme_mode = 'light' if self._theme_mode == 'dark' else 'dark'
        self._btn_theme.setText("☀" if self._theme_mode == 'dark' else "🌙")
        self._load_logo_image(self._theme_mode)   # logo coordonné avec le thème
        self._apply_theme(self._theme_mode)
        self.settings['theme'] = self._theme_mode
        self._save_settings()

    def _apply_theme(self, mode):
        palette = LIGHT if mode == 'light' else {
            "BG":BG,"SURFACE":SURFACE,"CARD":CARD,
            "ACCENT":ACCENT,"ACCENT2":ACCENT2,"ACCENT3":ACCENT3,
            "TEXT":TEXT,"TDIM":TDIM,"OK":OK,"WARN":WARN,"ERR":ERR,"BORDER":BORDER,
        }
        QApplication.instance().setStyleSheet(build_style(palette))

    def _track_worker(self, w):
        """Enregistre un worker et le retire de la liste dès qu'il se termine."""
        self.workers.append(w)
        def _cleanup(*_):
            QTimer.singleShot(0, lambda: self.workers.remove(w) if w in self.workers else None)
        try: w.finished.connect(lambda *a: _cleanup())
        except Exception: pass
        try: w.error.connect(lambda *a: _cleanup())
        except Exception: pass
        return w

    def _finish_bulk_analysis(self):
        """Restaure l'état des boutons après une analyse ou synthèse groupée."""
        self.btn_all.setEnabled(True)
        self.btn_cancel.setVisible(False)

    def _add_files(self, paths):
        skipped_mac = []
        for path in paths:
            if path in self.files: continue
            p = Path(path)

            # Fichiers fantômes macOS (AppleDouble / resource forks) : ._nomfichier
            # Créés automatiquement lors de copies vers FAT/NTFS — aucun contenu utile.
            if p.name.startswith('._'):
                skipped_mac.append(p.name)
                continue

            ftype = get_file_type(path)
            if ftype == 'unknown': continue
            info = {'path':path,'name':p.name,'type':ftype,'size':human_size(p.stat().st_size),'content':'','summary':'','analysis':''}
            self.files[path] = info
            card = FileCard(info)
            card.analyze_requested.connect(self._analyze_file)
            card.remove_requested.connect(self._remove_file)
            card.selected.connect(self._select_file)
            self.file_cards[path] = card
            self.cards_lay.insertWidget(self.cards_lay.count()-1, card)
            self.log_panel.log(f"Fichier ajoute : {p.name}  ({ftype}, {info['size']})", "info")

        if skipped_mac:
            self.log_panel.log(
                f"⚠ {len(skipped_mac)} fichier(s) macOS ignores (._*) — "
                f"métadonnées systeme sans contenu utile.", "warning"
            )
        self._update_status()

    def _remove_file(self, path):
        if path in self.file_cards:
            w = self.file_cards.pop(path); self.cards_lay.removeWidget(w); w.deleteLater()
        name = Path(path).name; self.files.pop(path, None)
        if self.selected == path: self.selected = None
        self.log_panel.log(f"Fichier retire : {name}", "info"); self._update_status()

    def _clear_all(self):
        for p in list(self.file_cards): self._remove_file(p)

    def _select_file(self, path):
        for p,c in self.file_cards.items(): c.set_selected(p==path)
        self.selected = path; self.result_panel.set_file(self.files[path])

    def _analyze_file(self, path, on_complete=None):
        info = self.files[path]; card = self.file_cards[path]; ftype = info['type']
        is_batch = on_complete is not None   # True = lancé depuis la file séquentielle

        # Pendant le batch : on surbrille juste la carte sans écraser les vues cumulatives.
        # En analyse individuelle (clic ▶ sur une carte) : on affiche les données du fichier.
        if is_batch:
            for p, c in self.file_cards.items(): c.set_selected(p == path)
            self.selected = path
        else:
            self._select_file(path)

        self.log_panel.log(f"─── Debut analyse : {info['name']} ───", "step")
        self.log_panel.set_busy(True)

        if ftype in ('video','audio'):
            card.set_status("Transcription...", WARN)
            self.result_panel.show_progress("Chargement Whisper...")
            self.log_panel.log(f"Modele Whisper : {self.settings['whisper_model']} | Langue : {self.settings['language']}", "info")
            w = TranscriptionWorker(path, self.settings['whisper_model'], self.settings['language'])
            w.progress.connect(lambda m: (self.result_panel.show_progress(m), self.log_panel.log(m,"info")))
            w.finished.connect(lambda t, p=path, cb=on_complete: self._after_transcription(t, p, cb))
            w.error.connect(lambda e, c=card: self._on_error(e,c))
            self._track_worker(w); w.start()
        else:
            card.set_status("Extraction...", WARN)
            self.log_panel.log(f"Extraction {Path(path).suffix.upper()}...", "step")
            self.result_panel.show_progress("Extraction du contenu...")
            text = extract_document(path)

            # PDF scanné → 0 mots → lancer OCR automatiquement
            if not text.strip() and Path(path).suffix.lower() == '.pdf':
                card.set_status("OCR...", WARN)
                self.log_panel.log("PDF scanne detecte — lancement de l'OCR...", "warning")
                self.result_panel.show_progress("OCR du PDF en cours...")
                ocr_lang = self.settings.get('language', 'fr')
                w = PDFOCRWorker(path, language=ocr_lang)
                w.progress.connect(lambda m: (self.result_panel.show_progress(m), self.log_panel.log(m, "info")))
                w.finished.connect(lambda t, p=path, cb=on_complete: self._after_ocr(t, p, cb))
                w.error.connect(lambda e, c=card: self._on_error(e, c))
                self._track_worker(w); w.start()
                return

            info['content'] = text
            # Batch → cumul ; individuel → remplace
            if is_batch:
                self.result_panel.append_to_tab('content', info['name'], text)
            else:
                self.result_panel.set_content(text)
            card.set_status("Extrait ✓", OK)
            self.log_panel.log(f"Extraction OK : {len(text.split())} mots", "success")
            self._run_summary(path, on_complete=on_complete)

    def _after_transcription(self, text, path, on_complete=None):
        self.files[path]['content'] = text
        self.result_panel.append_to_tab('content', self.files[path]['name'], text)
        card = self.file_cards.get(path)
        if card: card.set_status("Transcrit ✓", OK)
        self.log_panel.log(f"Transcription OK : {len(text.split())} mots", "success")
        self._run_summary(path, on_complete=on_complete)

    def _after_ocr(self, text, path, on_complete=None):
        self.files[path]['content'] = text
        self.result_panel.append_to_tab('content', self.files[path]['name'], text)
        card = self.file_cards.get(path)
        if card: card.set_status("OCR ✓", OK)
        self.log_panel.log(f"OCR OK : {len(text.split())} mots", "success")
        self._run_summary(path, on_complete=on_complete)

    def _run_summary(self, path, on_complete=None):
        text = self.files[path].get('content','')
        if not text.strip():
            self.result_panel.hide_progress(); self.log_panel.set_busy(False)
            if on_complete: on_complete()
            return
        self.result_panel.show_progress("Generation du resume...")
        self.log_panel.log("Resume en cours...", "ai")
        ctx = self.ctx_edit.toPlainText().strip()
        w = self._make_worker(text, "summary", context=ctx)
        w.progress.connect(lambda m: self.log_panel.log(m,"ai"))
        w.finished.connect(lambda r, p=path, cb=on_complete: self._after_summary(r, p, cb))
        w.error.connect(lambda e: self._on_error(e, self.file_cards.get(path)))
        self._track_worker(w); w.start()

    def _after_summary(self, summary, path, on_complete=None):
        self.files[path]['summary'] = summary
        self.result_panel.append_to_tab('summary', self.files[path]['name'], summary)
        self.log_panel.log("Resume genere", "success")
        self.result_panel.show_progress("Analyse approfondie...")
        self.log_panel.log("Analyse approfondie en cours...", "ai")
        ctx = self.ctx_edit.toPlainText().strip()
        w = self._make_worker(self.files[path]['content'], "deep", context=ctx)
        w.progress.connect(lambda m: self.log_panel.log(m,"ai"))
        w.finished.connect(lambda r, p=path, cb=on_complete: self._after_analysis(r, p, cb))
        w.error.connect(lambda e: self._on_error(e, self.file_cards.get(path)))
        self._track_worker(w); w.start()

    def _after_analysis(self, analysis, path, on_complete=None):
        self.files[path]['analysis'] = analysis
        name = self.files[path]['name']
        self.result_panel.append_to_tab('analysis', name, analysis)
        self.result_panel.hide_progress()
        card = self.file_cards.get(path)
        if card: card.set_status("Analyse ✓", OK)
        self.log_panel.log(f"Analyse complete : {name}", "success")
        self.log_panel.set_busy(False); self._update_status()
        if on_complete:
            on_complete()

    def _run_qa(self, current_text, question, history):
        """Lance une question en mode conversation avec contexte de tout le dossier."""
        # ── Construction du contexte ──────────────────────────
        scope_all = self.result_panel.get_qa_scope_all()
        if scope_all and self.files:
            parts = []
            for path, info in self.files.items():
                name     = info['name']
                analysis = info.get('analysis', '').strip()
                content  = info.get('content',  '').strip()
                # Priorité à l'analyse ; sinon contenu brut
                text = analysis if analysis else content
                if text:
                    parts.append(f"=== {name} ===\n{text[:4000]}")
            context_text = "\n\n".join(parts) if parts else current_text
        else:
            context_text = current_text

        if not context_text.strip():
            QMessageBox.warning(self, "Aucun contenu",
                "Analysez d'abord au moins un document avant de poser des questions.")
            return

        # Limite globale adaptée au contexte LM Studio (réservation de tokens pour la réponse)
        MAX_CTX_CHARS = 24000
        context_text = context_text[:MAX_CTX_CHARS]

        # ── Construction du prompt avec historique ────────────
        ctx_prefix = self.ctx_edit.toPlainText().strip()
        domain_hint = f"{ctx_prefix}\n\n" if ctx_prefix else ""

        # On construit les messages pour la conversation
        history_text = ""
        # On prend les N-1 derniers échanges (sauf la question actuelle déjà dans history)
        prev_exchanges = [m for m in history[:-1] if m['role'] in ('user','assistant')]
        if prev_exchanges:
            history_text = "\nHISTORIQUE DE LA CONVERSATION:\n"
            for m in prev_exchanges[-6:]:  # max 3 échanges précédents
                role = "Utilisateur" if m['role'] == 'user' else "Assistant"
                history_text += f"{role}: {m['content'][:500]}\n"

        full_context = (
            f"{domain_hint}"
            f"Tu es un assistant juridique expert. Réponds en français de manière claire et structurée.\n"
            f"Base ta réponse UNIQUEMENT sur les documents fournis ci-dessous.\n\n"
            f"DOCUMENTS DU DOSSIER:\n{context_text}\n"
            f"{history_text}\n"
            f"Question actuelle: {question}\n\nRéponse:"
        )

        self.result_panel.show_progress("Recherche de la réponse…")
        self.log_panel.log(f"Question : {question[:80]}", "step")
        self.log_panel.set_busy(True)

        engine     = self.settings.get('engine', 'lmstudio')
        model      = self.settings['lmstudio_model']
        model_path = self.settings.get('llamacpp_model', '')

        w = DirectSynthesisWorker(full_context, model,
                                  engine=engine, model_path=model_path)
        w.progress.connect(lambda m: self.log_panel.log(m, "ai"))
        w.finished.connect(lambda r: (
            self.result_panel.add_qa_answer(r),
            self.result_panel.hide_progress(),
            self.log_panel.log("Réponse générée", "success"),
            self.log_panel.set_busy(False)
        ))
        w.error.connect(lambda e: (
            self._on_error(e),
            self.result_panel.hide_progress()
        ))
        self._track_worker(w); w.start()

    def _run_global_analysis(self):
        analyses = []
        for path, info in self.files.items():
            a = info.get('analysis','').strip()
            if a:
                analyses.append(f"=== {info['name']} ===\n{a}")
        if not analyses:
            QMessageBox.warning(self, "Aucune analyse", "Analysez d'abord au moins un document avec ▶.")
            return
        combined = "\n\n".join(analyses)
        n = len(analyses)
        ctx = self.ctx_edit.toPlainText().strip()
        self.result_panel.show_progress(f"Synthese globale de {n} document(s)...")
        self.log_panel.log(f"Synthese globale de {n} analyse(s)...", "step")
        self.log_panel.set_busy(True)
        w = self._make_worker(combined, "global", context=ctx)
        w.progress.connect(lambda m: (self.result_panel.show_progress(m), self.log_panel.log(m,"ai")))
        w.finished.connect(lambda r: (
            self.result_panel.set_global(r),
            self.result_panel.hide_progress(),
            self.log_panel.log("Synthese globale terminee","success"),
            self.log_panel.set_busy(False)
        ))
        w.error.connect(self._on_error)
        self._track_worker(w); w.start()

    def _analyze_all(self):
        if not self.files:
            QMessageBox.warning(self, "Aucun fichier", "Ajoutez d'abord des fichiers.")
            return
        self._cancel_requested = False
        self.btn_all.setEnabled(False)
        self.btn_cancel.setVisible(True)
        self.result_panel.reset_accumulated()   # vider les vues cumulatives
        if self.mode_sel.is_full():
            self.log_panel.log(f"Analyse complete de {len(self.files)} fichier(s)...", "step")
            # Traitement séquentiel pour ne pas surcharger LM Studio
            self._analyze_queue = list(self.files.keys())
            self._process_next_in_queue()
        else:
            self.log_panel.log(f"Synthese globale directe de {len(self.files)} fichier(s)...", "step")
            self._run_global_direct()

    def _process_next_in_queue(self):
        """Lance l'analyse du prochain fichier dans la file (mode séquentiel)."""
        if self._cancel_requested or not self._analyze_queue:
            if not self._cancel_requested:
                self.log_panel.log("Toutes les analyses individuelles sont terminees.", "success")
            self._analyze_queue.clear()
            self._finish_bulk_analysis()
            return
        path = self._analyze_queue.pop(0)
        if path in self.files:
            self._analyze_file(path, on_complete=self._process_next_in_queue)

    def _run_global_direct(self):
        self.log_panel.set_busy(True)
        # Marquer audio/video comme ignores
        files_to_extract = {}
        for path, info in self.files.items():
            card = self.file_cards.get(path)
            if info['type'] in ('video','audio'):
                self.log_panel.log(f"Ignore (audio/video requiert mode complet) : {info['name']}", "warning")
                if card: card.set_status("Ignore", TDIM)
                continue
            if card: card.set_status("Extraction...", WARN)
            files_to_extract[path] = info

        if not files_to_extract:
                self.log_panel.set_busy(False)
                self._finish_bulk_analysis()
                QMessageBox.warning(self, "Aucun contenu", "Aucun document a extraire.\nNote : audio/video requiert le mode Analyse complete.")
                return

        ocr_lang = self.settings.get('language', 'fr')
        self.result_panel.show_progress("Extraction des documents...")
        self.log_panel.log("Extraction batch (avec OCR si necessaire)...", "step")

        def on_file_done(path, text):
            self.files[path]['content'] = text
            card = self.file_cards.get(path)
            if card: card.set_status("Extrait ✓", OK)
            self.log_panel.log(f"Contenu extrait : {self.files[path]['name']} ({len(text.split())} mots)", "success")

        def on_batch_done(results):
            if not results:
                self.log_panel.set_busy(False)
                self.result_panel.hide_progress()
                self._finish_bulk_analysis()
                QMessageBox.warning(self, "Aucun contenu",
                    "Impossible d'extraire le contenu.\nRelancez install.bat pour installer l'OCR (easyocr).")
                return
            contents = []
            for path, text in results.items():
                name = self.files[path]['name']
                contents.append(f"=== {name} ===\n{text[:2000]}")
            self._run_global_synthesis(contents)

        w = BatchExtractionWorker(files_to_extract, ocr_language=ocr_lang)
        w.progress.connect(lambda m: (self.result_panel.show_progress(m), self.log_panel.log(m, "info")))
        w.file_done.connect(on_file_done)
        w.finished.connect(on_batch_done)
        w.error.connect(self._on_error)
        self._track_worker(w); w.start()

    def _run_global_synthesis(self, contents):
        """Lance la synthese une fois tous les contenus extraits."""
        model      = self.settings['lmstudio_model']
        engine     = self.settings.get('engine', 'lmstudio')
        model_path = self.settings.get('llamacpp_model', '')
        ctx    = self.ctx_edit.toPlainText().strip()
        n      = len(contents)
        combined = "\n\n".join(contents)
        ctx_block = f"CONTEXTE UTILISATEUR:\n{ctx}\n\n" if ctx else ""
        ctx_hint  = " (en tenant compte du contexte fourni)" if ctx else ""

        prompt = (
            f"{ctx_block}"
            f"Tu es un expert en analyse transversale{ctx_hint}. "
            f"Analyse directement l'ensemble de ces {n} documents et fournis une synthese globale en francais :\n"
            f"## Vue d'ensemble\n## Points cles communs\n## Liens entre les documents\n"
            f"## Points d'attention\n## Conclusions et recommandations\n\n"
            f"DOCUMENTS:\n{combined[:12000]}\n\nSYNTHESE GLOBALE:"
        )

        self.result_panel.show_progress(f"Synthese globale directe de {n} doc(s)...")
        self.log_panel.log("Synthese globale directe en cours...", "ai")

        w = DirectSynthesisWorker(prompt, model, engine=engine, model_path=model_path)
        w.progress.connect(lambda m: (self.result_panel.show_progress(m), self.log_panel.log(m,"ai")))
        w.finished.connect(lambda r: (
            self.result_panel.set_global(r),
            self.result_panel.tabs.setCurrentIndex(3),
            self.result_panel.hide_progress(),
            self.log_panel.log(f"Synthese globale directe terminee ({n} docs)","success"),
            self.log_panel.set_busy(False),
            self._finish_bulk_analysis()
        ))
        w.error.connect(self._on_error)
        self._track_worker(w); w.start()

    def _cancel_analysis(self):
        """Annule la file d'analyse et interrompt le worker en cours."""
        self._cancel_requested = True
        self._analyze_queue.clear()
        # Interrompre les workers actifs (HTTP session close + flags)
        for w in list(self.workers):
            if hasattr(w, 'cancel'):
                w.cancel()
        self.result_panel.hide_progress()
        self.log_panel.set_busy(False)
        self.log_panel.log("Analyse annulee par l'utilisateur.", "warning")
        self._finish_bulk_analysis()

    def _on_error(self, msg, card=None):
        self.result_panel.hide_progress(); self.log_panel.set_busy(False)
        self._analyze_queue.clear()
        self._finish_bulk_analysis()
        if card: card.set_status("Erreur ✗", ERR)
        self.log_panel.log(f"ERREUR : {msg.splitlines()[0]}", "error")
        QMessageBox.critical(self, "Erreur", msg)

    def _open_settings(self):
        dlg = QDialog(self); dlg.setWindowTitle("Parametres Whisper"); dlg.setFixedSize(380,220)
        dlg.setWindowFlags(dlg.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        lay = QVBoxLayout(dlg); lay.setContentsMargins(20,20,20,16); lay.setSpacing(14)
        lay.addWidget(QLabel("Parametres de transcription"))
        g = QGroupBox("Faster-Whisper"); f = QFormLayout(g); f.setSpacing(10)
        wc = QComboBox(); wc.addItems(["tiny","base","small","medium","large-v3"])
        wc.setCurrentText(self.settings.get('whisper_model','base'))
        lc = QComboBox(); lc.addItems(["fr","en","es","de","it","pt","ar","zh","ja","auto"])
        lc.setCurrentText(self.settings.get('language','fr'))
        f.addRow("Modele Whisper :", wc); f.addRow("Langue :", lc)
        lay.addWidget(g); lay.addStretch()
        btns = QHBoxLayout()
        c = QPushButton("Annuler"); c.setObjectName("secondary"); c.clicked.connect(dlg.reject)
        s = QPushButton("Enregistrer")
        def save():
            self.settings['whisper_model'] = wc.currentText()
            self.settings['language'] = lc.currentText()
            self._save_settings()
            self.log_panel.log(f"Whisper: {wc.currentText()} | Langue: {lc.currentText()}", "success")
            dlg.accept()
        s.clicked.connect(save)
        btns.addStretch(); btns.addWidget(c); btns.addWidget(s); lay.addLayout(btns); dlg.exec()

    def _update_status(self):
        n = len(self.files)
        self.stat_lbl.setText(f"{n} fichier{'s' if n>1 else ''}" if n else "Pret")

    def _settings_path(self): return Path.home()/".fileanalyzer_ai.json"
    def _save_settings(self):
        try: self._settings_path().write_text(json.dumps(self.settings), encoding='utf-8')
        except: pass
    def _load_settings(self):
        try:
            p = self._settings_path()
            if p.exists(): self.settings.update(json.loads(p.read_text(encoding='utf-8')))
        except: pass


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("FileAnalyzer AI")
    app.setStyle("Fusion"); app.setStyleSheet(STYLE)
    win = MainWindow(); win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
