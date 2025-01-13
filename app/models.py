from pydantic import BaseModel, Field
from typing import Optional

class TaskRequest(BaseModel):
    task_name: str
    duration: int = Field(gt=0, description="Duration in seconds")

class TaskResponse(BaseModel):
    task_id: str
    status: str
    submitted_at: str
    duration: Optional[int] = None
    result: Optional[str] = None

