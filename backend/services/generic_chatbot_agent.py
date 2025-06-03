from langgraph.graph import StateGraph, END, START
from openai import OpenAIError
from backend.models.schemas import GenericChatbotAgentState
from backend.config.logger import logger
from backend.config.llm import get_llm


# Fonction du nœud : appel au LLM
def generic_chatbot_node(state: GenericChatbotAgentState) -> dict:
    question = state["question"]
    logger.info("🔄 GenericChatbot: Traitement de la question : %s", question)

    try:
        prompt = f"""Tu es un assistant virtuel générique pour un service de support IT.
Réponds à la question suivante de manière concise et claire :

Question : "{question}"
Réponse :"""
        llm = get_llm()
        response = llm.invoke(prompt).content
        logger.info("✅ Réponse LLM obtenue : %s", response)

        return {"response": response}

    except OpenAIError as e:
        logger.error("❌ Erreur lors de l'appel au LLM : %s", str(e))
        return {
            "response": "Désolé, je n’ai pas pu traiter votre question pour le moment."
        }

    except Exception as e:
        logger.exception("💥 Erreur inattendue dans GenericChatbot")
        return {"response": "Une erreur technique est survenue dans l'agent générique."}


# Création du graphe
def create_generic_chatbot_graph():
    workflow = StateGraph(GenericChatbotAgentState)
    workflow.add_node("GenericChatbot", generic_chatbot_node)
    workflow.add_edge(START, "GenericChatbot")
    workflow.add_edge("GenericChatbot", END)
    return workflow.compile()
