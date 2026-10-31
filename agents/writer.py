from langchain_core.messages import HumanMessage, SystemMessage

from config import llm
from state import Critique, State
from utils import text_of

SSYSTEM_PROMPT = (
    "You are a sharp, clear writer. Write a ~500-word article in Markdown "
    "using ONLY the research notes provided. Lead with the main insight and "
    "end with a short takeaway. Preserve the certainty of each claim exactly: "
    "a projection or estimate in the notes must stay a projection, never a fact. "
    "Avoid hype words such as 'revolutionize', 'pivotal' and 'transform'. "
    "When revising, fix every point in the feedback and change nothing else."
)


def writer(state: State) -> dict:
    critique = state.get("critique")

    if critique is None:
        task = "write the first draft"
    else:
        task = {
            "Revise the previous draft to address the editors feedback.\n\n"
            f"Previous DRAFT:\n{state['draft']}\n\n"
            f"EDITOR FEEDBACK (score{critique.score}/10): \n{critique.feedback}"

        }

        task = (
            "Revise the previous draft to address the editor's feedback.\n\n"
            f"PREVIOUS DRAFT:\n{state['draft']}\n\n"
            f"EDITOR FEEDBACK (score {critique.score}/10):\n{critique.feedback}"
        )

    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=(
            f"TOPIC: {state['topic']}\n\n"
            f"RESEARCH NOTES:\n{state['research']}\n\n"
            f"{task}"
        )),
    ])
    
    revisions = state.get("revisions", 0) + (0 if critique is None else 1)
    label = "first draft" if critique is None else f"revision {revisions}"

    return {
        "draft": text_of(response),
        "revisions": revisions,
        "log": [f"writer: {label}"],
    }