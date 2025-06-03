from langchain_openai import ChatOpenAI
from .settings import settings


def get_llm(model_name=None, temperature=0.1):
    return ChatOpenAI(
        model=model_name or settings.openai_model_name,
        openai_api_key=settings.openai_api_key,
        temperature=temperature,
    )
