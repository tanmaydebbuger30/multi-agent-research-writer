from langchain_core.messages import HumanMessage, SystemMessage

from config import llm
from state import Critique, State

SYSTEM_PROMPT = (
    "You are a demanding editor. Judge the draft ONLY against the research notes "
    "provided: accuracy, claims not supported by the notes, hype or vague language, "
    "clarity and structure. Do not ask for facts, statistics or topics that are "
    "not in the notes; the writer cannot add them. Approve only if it scores 8 or "
    "higher. Feedback must be concrete and actionable using the notes alone."
)
def critic(state: State) -> dict:
    judge = llm.with_structured_output(Critique)

    result: Critique = judge.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=(
            f"RESEARCH NOTES:\n{state['research']}\n\n"
            f"DRAFT:\n{state['draft']}"
        )),
    ])

    verdict = "approved" if result.approved else "needs revision"
    return {
        "critique": result,
        "log": [f"critic: {result.score}/10, {verdict}\n     feedback: {result.feedback[:300]}"],
    }