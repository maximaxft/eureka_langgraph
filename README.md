# Présentation Chatbot IA

Ce projet propose un chatbot intelligent pour présenter l'équipe, ses objectifs, et le concept d'Intelligent Digital Twins, illustré par un exemple d'incident généré nommé **KDOEM45D**. Le chatbot est capable de répondre aussi bien aux questions générales qu'aux questions spécifiques liées à cet incident, démontrant ainsi ses capacités de routage des requêtes

## Structure du projet

- `frontend/` : Interface web (React)  
- `backend/` : API et moteur IA (FastAPI)  
  - `config/`  
  - `main.py`  
  - `models/`  
  - `requirements.txt`  
  - `routes/`  
  - `services/`  
- `docs/` : Documents de présentation (Markdown)  
- `images/` : Images à afficher lors de la présentation  

---

## Endpoints backend

Le backend expose deux endpoints principaux :  

- **`/new-chat`** : Pour récupérer l’ID de session d’un nouveau chat.  
- **`/ask`** : Pour poser des questions au backend.  

---

## Architecture du backend

Le backend utilise un **graphe LangGraph** structuré en deux sous-graphes :  

1. **Sous-graphe Agent ReAct** :  
   - Dispose de deux outils :  
     - Un outil pour récupérer les logs en lien avec un incident.  
     - Un outil pour récupérer les changements corrélés à l’incident.  
   - Gère les questions en lien avec les incidents via cet agent.  

2. **Sous-graphe général** :  
   - Répond aux questions générales, hors contexte incident.  

Pour la gestion des conversations, on utilise une **InMemorySaver** afin de stocker la conversation en cours.

---

## Prérequis

- Python 3.8+  
- Node.js 16+  
- npm ou yarn  

---

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

---

### Remarque pour les tests

Pour tester l'application, vous pouvez faire référence à l'incident **KDOEM45D**, qui est un exemple utilisé dans notre démonstration.  

Nous avons généré :  
- Les logs d'une erreur en lien avec cet incident.  
- La liste des changements corrélés à cet incident.  

Cela vous permettra de tester le fonctionnement de l'agent ReAct et des outils associés au traitement des incidents.

## Configuration

### Variables d'environnement

Créez un fichier `.env` à la racine du projet avec les variables nécessaires :

```env
# Clé API OpenAI
OPENAI_API_KEY=votre_cle_api_openai
OPENAI_MODEL_NAME="gpt-4o-mini"

# Le nombre maximum de boucle que l'agent peut faire
RECURSION_LIMIT=5

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

