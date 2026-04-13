# 📄 MD to PDF Pro - Contexte du Projet

## 🎯 Objectif
Createur de documents PDF haute qualité à partir de fichiers ou de texte Markdown. Ce micro-SaaS est conçu pour être utilisé par des humains (UI) et par des IA (API & MCP).

## 🛠 Tech Stack
- **Backend** : Python 3.11+ avec Flask & FastMCP.
- **Moteur PDF** : `fpdf2` (Solution Pure Python, robuste et rapide).
- **Formatage** : Markdown (via la bibliothèque `markdown`).
- **Frontend** : HTML5 / CSS3 (Design Glassmorphism).

## 📁 Structure du Projet
- `/backend/app.py` : Serveur Web Flask (UI + API).
- `/backend/mcp_server.py` : Serveur MCP pour Agents IA.
- `/backend/converter.py` : Logique de conversion partagée.
- `/backend/pdfs` : Stockage des fichiers générés.

## 🚀 Lancement Web
- `pip install -r requirements.txt`
- `python backend/app.py` (Port 5001)

## 🔗 Endpoints API (v1)
- `GET /` : Interface Web.
- `POST /api/v1/convert` : Accepte JSON `{"markdown": "..."}` ou un fichier via le champ `file`.

---

## 🤖 Support IA (MCP)
Le projet supporte le **Model Context Protocol**. Cela permet à des agents IA (Claude, etc.) d'appeler l'outil `convert_markdown_to_pdf` directement.

### Configuration Claude Desktop :
```json
"mcpServers": {
  "inspirify-pdf": {
    "command": "python",
    "args": ["c:/prog/apps/md-to-pdf/backend/mcp_server.py"]
  }
}
```

### Outils exposés :
- `convert_markdown_to_pdf(content: str)` : Génère un PDF à partir d'une chaîne de caractères et renvoie le chemin du fichier.
