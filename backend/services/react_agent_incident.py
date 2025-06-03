from langgraph.prebuilt import create_react_agent
from backend.config.logger import logger, checkpointer
from backend.config.settings import settings

SYSTEM_PROMPT = """Tu es un expert en analyse d'incidents pour un backend. 
Tu peux appeler des outils pour t'aider à comprendre ce qui s'est passé.

Ton objectif est de diagnostiquer la cause probable d'un incident en t'aidant des logs et des corrélations de code si besoin.

Tu dois :
- analyser la situation,
- appeler les outils quand tu en as besoin (fetch_logs, fetch_correlations),
- conclure uniquement quand tu es raisonnablement certain.

"""


def fetch_logs_tool(incident_id: str):
    """
    Récupère les logs associés à un incident donné.
    """
    logger.info("🛠️ [Tool] Fetching incident logs...")

    if incident_id != "KDOEM45D":
        logger.warning("🚫 Incident inconnu : %s", incident_id)
        return "[Aucun log disponible pour l’incident {incident_id}]"

    return [
        "[2025-06-03 06:22:10,551] [INFO] [notification-service] Scheduled task: process_pending_notifications",
        "[2025-06-03 06:22:10,553] [INFO] [notification-service] Fetched 0 pending notifications",
        "[2025-06-03 06:27:10,560] [INFO] [notification-service] Scheduled task: process_pending_notifications",
        "[2025-06-03 06:27:10,562] [INFO] [notification-service] Fetched 0 pending notifications",
        "[2025-06-03 06:34:01,212] [INFO] [deploy-service] Deployed notification-service@v3.2.0 to prod-cluster",
    ]


def fetch_correlations_tool(incident_id: str):
    """
    Récupère les corrélations de commits et changements liés à un incident donné.
    """
    logger.info("🛠️ [Tool] Fetching correlations...")
    if incident_id != "KDOEM45D":
        logger.warning("🚫 Incident inconnu : %s", incident_id)
        return "Aucune corrélation disponible pour l’incident {incident_id}"

    return [
        {
            "commit_id": "ab12c9d",
            "author": "elambert",
            "file": "jobs/fetch_notifications.py",
            "change_summary": "Changed query filter from `status='queued'` to `status='pending'`",
            "suspicion_score": 0.92,
        },
        {
            "commit_id": "cd98f32",
            "author": "jsouidi",
            "file": "templates/email_template.html",
            "change_summary": "Updated email footer link style",
            "suspicion_score": 0.10,
        },
        {
            "commit_id": "e7711ca",
            "author": "rmartin",
            "file": "notification/config.yaml",
            "change_summary": "Disabled SMS fallback feature",
            "suspicion_score": 0.28,
        },
        {
            "commit_id": "f22ab18",
            "author": "elambert",
            "file": "tests/test_fetch_notifications.py",
            "change_summary": "Removed tests with status='queued'",
            "suspicion_score": 0.84,
        },
        {
            "commit_id": "cabbef1",
            "author": "kdeschamps",
            "file": "Dockerfile",
            "change_summary": "Upgraded alpine base image to 3.18",
            "suspicion_score": 0.35,
        },
    ]


def create_incident_analysis_agent():
    agent = create_react_agent(
        model=settings.openai_model_name,
        tools=[fetch_logs_tool, fetch_correlations_tool],
        prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )

    return agent
