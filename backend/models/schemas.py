from pydantic import BaseModel, Field
from typing import Optional, TypedDict, Union, Literal


# Modèle de décision pour le routage
class RouteDecision(BaseModel):
    step: Literal["generic_chatbot", "incident_analysis"] = Field(
        ...,
        description="Détermine si la demande doit être routée vers 'generic_chatbot' ou 'incident_analysis'.",
    )


# Définition de l'état global
class OrchestratorState(TypedDict):
    question: str
    chat_id: str
    routing_decision: Literal["generic_chatbot", "incident_analysis"]
    final_response: Union[str, dict]


class Message(BaseModel):
    role: str
    content: str


class AskRequest(BaseModel):
    question: str
    user_id: Optional[str] = None
    chat_id: Optional[str] = None


class ChatRequest(BaseModel):
    user_id: str


class GenericChatbotAgentState(TypedDict):
    question: str
    response: str


class IncidentAnalysisAgentState(TypedDict):
    question: str
    response: str
    incident_id: str
