from fastapi import Request, HTTPException
from typing import List
from langgraph.graph import StateGraph, END

from backend.config.llm import get_llm
from backend.config.settings import settings
from backend.config.logger import logger
from langchain_core.messages import HumanMessage, SystemMessage
from backend.models.schemas import RouteDecision, OrchestratorState

# Import des sous-agents
from .generic_chatbot_agent import create_generic_chatbot_graph
from .react_agent_incident import create_incident_analysis_agent


# Routeur structuré via LLM
llm = get_llm()
router = llm.with_structured_output(RouteDecision)

# Initialisation unique des sous-graphes
generic_chatbot_graph = create_generic_chatbot_graph()
react_agent_incident = create_incident_analysis_agent()


# --- Fonctions internes ---
def get_orchestrator(request: Request) -> object:
    orchestrator = getattr(request.app.state, "orchestrator", None)
    if orchestrator is None:
        raise HTTPException(status_code=503, detail="Orchestrateur non initialisé")
    return orchestrator


def format_history(history: List[dict]) -> str:
    """Formate l'historique des messages pour le prompt"""
    if not history:
        return "Aucun historique précédent."

    lines = []
    for msg in history:
        role = msg.get("role", "utilisateur").capitalize()
        content = msg.get("content", "")
        lines.append(f"{role}: {content}")
    return "\n".join(lines)


def route_question(state: OrchestratorState) -> OrchestratorState:
    """Détermine la destination de la question (routeur)"""
    question = state["question"]
    logger.info(f"Router: question reçue: {question}")

    contextual_prompt = f"""
Tu es un routeur intelligent pour un système de support IT bancaire.

Ton objectif est de déterminer si la dernière question posée par l'utilisateur est liée à un **incident informatique** (même de manière implicite), ou s'il s'agit d'une question générale.

Question de l'utilisateur :
"{question}"

Réponds par l'une des deux catégories suivantes :
- incident_analysis : si la question est liée à un incident informatique (explicite ou implicite, par exemple : demande de suivi, détails, impact, avancement, etc.).
- generic_chatbot : si la question est administrative, sociale, ou sans rapport avec un incident.

Réponds uniquement par l’un des deux mots suivants, sans guillemets :
incident_analysis
generic_chatbot
""".strip()

    try:
        decision = router.invoke([SystemMessage(content=contextual_prompt)])
        logger.info(f"Router: décision de routage: {decision.step}")
        state["routing_decision"] = decision.step
    except Exception as e:
        logger.error(f"Erreur lors du routage: {e}", exc_info=True)
        state["routing_decision"] = "generic_chatbot"  # fallback

    return state


def invoke_generic_chatbot_agent(state: OrchestratorState) -> dict:
    logger.info("Invocation de l'agent generic_chatbot")
    final_agent_state = generic_chatbot_graph.invoke({"question": state["question"]})
    return {
        "final_response": final_agent_state.get("response", "Pas de réponse générée.")
    }


def invoke_incident_analysis_agent(state: OrchestratorState) -> dict:
    logger.info("Invocation de l'agent incident_analysis")
    final_agent_state = react_agent_incident.invoke(
        {"messages": [HumanMessage(content=state["question"])]},
        config={
            "recursion_limit": settings.recursion_limit,
            "configurable": {"thread_id": state.get("chat_id")},
        },
    )

    try:
        messages = final_agent_state.get("messages", [])
        if not messages:
            return {"final_response": "Aucune réponse générée."}

        last_msg = messages[-1].content
        # logger.info(f"Dernier message LLM: {last_msg}")

        if last_msg:
            return {"final_response": last_msg}
        else:
            return {"final_response": "Aucune conclusion n'a été générée."}

    except Exception:
        logger.exception("Erreur lors de la récupération de la réponse finale")
        return {"final_response": "Erreur lors du traitement de l'analyse d'incident."}


def fallback_node(state: OrchestratorState) -> dict:
    logger.warning("Fallback : demande non traitée")
    return {
        "final_response": "Désolé, je ne peux pas traiter ce type de demande pour le moment."
    }


# --- Décision de transition ---
def decide_next_node(state: OrchestratorState) -> str:
    decision = state.get("routing_decision")
    logger.info(f"Décision de routage: {decision}")
    if decision == "generic_chatbot":
        return "generic_chatbot_agent"
    if decision == "incident_analysis":
        return "incident_analysis_agent"
    return "fallback"


# --- Construction du graphe orchestrateur ---
def create_orchestrator_graph():
    workflow = StateGraph(OrchestratorState)

    workflow.add_node("router", route_question)
    workflow.add_node("generic_chatbot_agent", invoke_generic_chatbot_agent)
    workflow.add_node("incident_analysis_agent", invoke_incident_analysis_agent)
    workflow.add_node("fallback", fallback_node)

    workflow.set_entry_point("router")

    workflow.add_conditional_edges(
        "router",
        decide_next_node,
        {
            "generic_chatbot_agent": "generic_chatbot_agent",
            "incident_analysis_agent": "incident_analysis_agent",
            "fallback": "fallback",
        },
    )

    workflow.add_edge("generic_chatbot_agent", END)
    workflow.add_edge("incident_analysis_agent", END)
    workflow.add_edge("fallback", END)

    return workflow.compile()
