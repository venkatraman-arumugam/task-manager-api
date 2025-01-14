from typing import List, Optional
from pydantic import BaseModel, Field


class TaskRequest(BaseModel):
    task_name: str
    duration: int = Field(gt=0, description="Duration in seconds")


class TaskResponse(BaseModel):
    task_id: str
    task_name: str
    status: str
    submitted_at: str
    duration: Optional[int] = None
    result: Optional[str] = None


class TaskPaginationRequest(BaseModel):
    page: int = Field(1, gt=0, description="Page number (must be greater than 0)")
    page_size: int = Field(
        10, gt=0, description="Number of tasks per page (must be greater than 0)"
    )

class PaginationMetadata(BaseModel):
    current_page: int
    page_size: int
    total_tasks: int
    total_pages: int


class TaskPaginationResponse(BaseModel):
    tasks: List[TaskResponse]
    pagination: PaginationMetadata
