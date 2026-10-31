from langchain_core.messages import HumanMessage, SystemMessage
from config import USE_WEB_SEARCH, llm
from state import State
from utils import text_of


SYSTEM_PROMPT = (
    "You are a meticulous research analyst. Gather the key facts, figures, "
    "competing viewpoints and open questions on the topic. Output concise "
    "bullet notes, each with its source where available. No prose essay."
)

def researcher(state: State) -> dict:
    model = llm

    if USE_WEB_SEARCH:
        model = llm.bind_tools([{"type" : "web_search_preview"}])

    
    response = model.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Topic: {state['topic']}"),
    ])

    return {
        "research": text_of(response),
        "log": ["researcher: notes gathered"],
    }