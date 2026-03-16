from pydantic import BaseModel


class OnLabResponse(BaseModel):
    """Response template"""
    content: list[dict] = []
    structure: dict = {}

class OnLabRequest(BaseModel):
    """Request template"""
    pr_name: str = ""
    pr_id: str = ""
    new_name: str = ""
    option: int = 0
    text: str = ""
    time: str = ""
    content: str = ""
    stage_id: int = -1
    name: str = ""
    category: str = ""
