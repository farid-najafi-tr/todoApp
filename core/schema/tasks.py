from pydantic import BaseModel, Field,ConfigDict
from typing import Optional
from datetime import datetime

from core.models.tasks import Task_Grading_Enum as TaskEnum

class TaskBase_schema(BaseModel):
    title : str = Field(...,max_length=150,min_length=5,description="Title of the task")
    description : Optional[str] = Field(None,max_length=500,description="description of the task")
    is_completed : bool = Field(default=False,description="state of the task")
    grading: TaskEnum = TaskEnum.medium

class Task_response_schema(TaskBase_schema):
    id : int = Field(...,description="unique identifier of the object")
    created_at: datetime = Field(None,description="creation date and time of the object")
    updated_at: datetime = Field(None,description="updating date and time of the object")
    user_id_fk : int
    model_config = ConfigDict(from_attributes=True)
    
class Task_created_schema(TaskBase_schema):
    pass

class Task_Update_Schema(TaskBase_schema):
    pass
    
class Task_Patch_Update(BaseModel):
    title : Optional[str] = Field(None,max_length=150,min_length=5,description="Title of the task")
    description : Optional[str] = Field(None,max_length=500,description="description of the task")
    is_completed : Optional[bool] = Field(default=False,description="state of the task")
    