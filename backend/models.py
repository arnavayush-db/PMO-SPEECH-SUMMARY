from pydantic import BaseModel
from typing import Optional

class Speech(BaseModel):
    id: int
    date: str
    title: str
    content: str
    summary: str
    image_uri: Optional[str] = None
    url: Optional[str] = None
    # Add any additional fields as needed