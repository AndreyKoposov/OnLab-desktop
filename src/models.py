from pydantic import BaseModel


class OnLabResponse(BaseModel):
    """Response template"""
    content: list[dict]

class OnLabRequest(BaseModel):
    """Response template"""
    pr_name: str = ""
    pr_id: int = -1
    new_name: str = ""
    option: int = 0
