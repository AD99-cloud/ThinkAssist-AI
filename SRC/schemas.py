from pydantic import BaseModel
from typing import List


class SourceReference(BaseModel):
    document: str
    page: int


class AssistantResponse(BaseModel):
    answer: str
    grounded: bool
    sources: List[SourceReference]