from ast import List
import operator

from typing import Annotated, TypedDict
from pydantic import BaseModel, Field


class Critique(BaseModel) : 
    approved: bool = Field(description="True only if the draft is ready to publish as-is")
    score: int = Field(ge=1, le=10, description="Overall quality, 1-10")
    feedback: str = Field(description="Specific, actionable revision notes")

class State(TypedDict) : 
    topic : str
    research : str
    draft : str
    critique : Critique | None
    revisions: int
    log : Annotated[list[str], operator.add]