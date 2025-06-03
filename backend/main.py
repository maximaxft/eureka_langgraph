from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from backend.routes import ask
from backend.config.logger import logger
from backend.services.orchestrator import create_orchestrator_graph
import pathlib

# Dossier d'images
BASE_DIR = pathlib.Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR.parent / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
logger.debug(f"[DEBUG] Les images seront servies depuis: {IMAGES_DIR}")


# Lifespan (initialisation orchestrateur ici)
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.orchestrator = create_orchestrator_graph()
        logger.info("[STARTUP] Orchestrateur LangGraph initialisé avec succès.")
    except Exception as e:
        logger.error(
            "[STARTUP] Échec de l'initialisation de l'orchestrateur", exc_info=True
        )
        app.state.orchestrator = None
    yield
    # Cleanup possible ici


# Application FastAPI
app = FastAPI(lifespan=lifespan)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # À restreindre pour la production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes statiques
app.mount("/images", StaticFiles(directory=str(IMAGES_DIR)), name="images")

# Routes API
app.include_router(ask.router)


# Route de base
@app.get("/")
def read_root():
    return {
        "message": "Backend IA prêt."
        if app.state.orchestrator
        else "Backend IA démarré, mais orchestrateur non initialisé."
    }


@app.get("/health")
def health():
    if app.state.orchestrator:
        return {"status": "ok"}
    return {"status": "orchestrator not ready"}, 500
