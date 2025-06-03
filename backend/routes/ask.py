from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import uuid
import asyncio
from backend.services.orchestrator import get_orchestrator
from backend.config.logger import logger
from backend.models.schemas import AskRequest, ChatRequest

router = APIRouter()


@router.post("/new-chat")
async def get_or_create_chat(req: ChatRequest):
    # Crée un nouveau chat_id
    # On utilisera le user_id plus tard pour le lié aux chat_ids
    chat_id = str(uuid.uuid4())

    return {"chat_id": chat_id}


@router.post("/ask")
async def ask_bot(request: AskRequest, orchestrator=Depends(get_orchestrator)):
    try:
        chat_id = request.chat_id or str(uuid.uuid4())
        user_id = request.user_id or "anonymous"

        logger.info(
            f"[ASK] user_id: {user_id} | chat_id: {chat_id} | question: {request.question}"
        )

        orchestrator_input = {
            "question": request.question,
            "chat_id": chat_id,
        }

        loop = asyncio.get_event_loop()
        final_state = await loop.run_in_executor(
            None, orchestrator.invoke, orchestrator_input
        )

        answer = final_state.get("final_response", "Aucune réponse trouvée.")

        return {"answer": answer, "chat_id": chat_id}
    except Exception as e:
        logger.error("[ERREUR /ask]", exc_info=True)
        return JSONResponse(status_code=500, content={"error": "Erreur interne."})
