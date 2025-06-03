import logging
import sys
from langgraph.checkpoint.memory import InMemorySaver


def get_logger(name: str = "chatbot"):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )
    return logging.getLogger(name)

logger = get_logger()

checkpointer = InMemorySaver()
