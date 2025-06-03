# Présentation Chatbot IA

Ce projet propose un chatbot intelligent pour présenter l'équipe, ses objectifs, et le concept d'Intelligent Digital Twins, à partir des documents du dossier `docs` et d'images associées.

## Structure du projet

- `frontend/` : Interface web (React)
- `backend/`  : API et moteur IA (FastAPI)
- `docs/`     : Documents de présentation (Markdown)
- `images/`   : Images à afficher lors de la présentation

## Prérequis

- Python 3.8+
- Node.js 16+
- npm ou yarn

## Installation

### 1. Configuration du backend

```bash
# Se placer dans le répertoire du projet (remplacez par votre chemin si nécessaire)
cd ~/Documents/eureka_langgraph

# Créer un environnement virtuel
python3 -m venv venv  # Utilisez python3 sur Mac/Linux

# Activer l'environnement virtuel
# Sur Mac/Linux :
source venv/bin/activate
# Sur Windows :
# .\venv\Scripts\activate

# Installer les dépendances Python
pip install -r backend/requirements.txt
```

### 2. Configuration du frontend

```bash
# Se placer dans le dossier frontend
cd frontend

# Installer les dépendances Node.js
npm install
```

## Lancement de l'application

### 1. Démarrer le serveur backend

Dans un terminal :

```bash
# Activer l'environnement virtuel si ce n'est pas déjà fait
source venv/bin/activate  # Sur Mac/Linux
# ou venv\Scripts\activate sur Windows

# Lancer le serveur FastAPI
uvicorn backend.main:app --reload
```

### 2. Démarrer le serveur frontend

Dans un autre terminal :

```bash
# Se placer dans le dossier frontend
cd frontend

# Démarrer le serveur de développement
npm run dev
```

## Accès à l'application

- **Interface utilisateur** : Ouvrez votre navigateur à l'adresse indiquée par Vite (généralement `http://localhost:5173`)
- **API Backend** : L'API sera disponible sur `http://localhost:8000`
- **Documentation de l'API** : `http://localhost:8000/docs` (Swagger UI)

## Configuration

### Variables d'environnement

Créez un fichier `.env` à la racine du projet avec les variables nécessaires :

```env
# Clé API OpenAI
OPENAI_API_KEY=votre_cle_api_openai

# Configuration du backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Configuration du frontend
VITE_API_URL=http://localhost:8000
```

## Personnalisation

- Ajoutez vos documents dans le dossier `docs/` (format Markdown)
- Ajoutez vos images dans le dossier `images/`
- Modifiez les styles dans le dossier `frontend/src/`
- Personnalisez les prompts dans le code du backend

## Déploiement

Pour un environnement de production, il est recommandé d'utiliser :
- Gunicorn ou Uvicorn avec gestionnaire de processus (PM2, Supervisor) pour le backend
- Build de production pour le frontend avec `npm run build`
- Serveur web comme Nginx pour servir les fichiers statiques et faire du reverse proxy
