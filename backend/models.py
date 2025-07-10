from pydantic import BaseModel
from typing import List, Optional

class BlueskyPost(BaseModel):
    user: str
    text: str
    query: str
    timestamp: str
    location: List[str] = []
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    disaster_type: str = ""