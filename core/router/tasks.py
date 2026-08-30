from fastapi import APIRouter,Path,Depends,HTTPException,status,Query
from core.core.database import get_db
from sqlalchemy.orm import Session
from core.schema import (
    Task_Update_Schema,
    Task_response_schema,
    Task_created_schema,
    Task_Patch_Update
)
from core.models.tasks import Task_model
from typing import List

router = APIRouter(
    tags= ["tasks"],
    prefix="/todo"
)

#region افزودن فیلتر های پیچیده به بخش task's

@router.get("/tasks/filter",response_model=List[Task_response_schema],status_code=status.HTTP_200_OK)
async def get_all_task_list_by_filtered(
    completed : bool = Query(None,description="filter tasks based on being completed or not"),
    limit:int = Query(10,gt=0,le=50,description="limiting the number of items to retrive"),
    offset:int = Query(0,gt=0,description="use for pagination"),
    db : Session = Depends(get_db)):
    query = db.query(Task_model)
    if completed is not None:
        query = query.filter_by(is_completed = completed)
    return query.limit(limit).offset(offset).all()

#endregion

@router.get("/tasks",response_model=List[Task_response_schema],status_code=status.HTTP_200_OK)
async def get_all_task_list(db : Session = Depends(get_db)):
    result = db.query(Task_model).all()
    return result

@router.get("/tasks/{task_id}",response_model=Task_response_schema,status_code=status.HTTP_200_OK)
def get_task_detail_by_id(task_id:int = Path(...,gt=0), db : Session = Depends(get_db)):
    get_task = db.query(Task_model).filter_by(id = task_id).first()
    if not get_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task is not found!")
    return get_task

@router.post("/tasks",response_model=Task_response_schema,status_code=status.HTTP_201_CREATED)
async def create_the_task(task_create : Task_created_schema, db : Session = Depends(get_db)):
    new_task = Task_model(
        title = task_create.title,
        description = task_create.description,
        is_completed = task_create.is_completed
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
    
@router.put("/tasks/{task_id}",status_code=status.HTTP_200_OK)
async def update_task_detail(task_detail: Task_Update_Schema,task_id:int = Path(...,gt=0), db : Session = Depends(get_db)):
    find_task = db.query(Task_model).filter_by(id = task_id).one_or_none()
    if not find_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task is not found!")
    for field, value in task_detail.model_dump(exclude_unset=True).items():
        setattr(find_task,field,value)
    db.commit()
    db.refresh(find_task)
    return find_task

@router.patch("/tasks/{task_id}",response_model=Task_response_schema,status_code=status.HTTP_200_OK)
async def updating_task_detail(task_detail : Task_Patch_Update, task_id: int = Path(...,gt=0), db : Session = Depends(get_db)):
    find_task = db.query(Task_model).filter_by(id = task_id).one_or_none()
    if not find_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task is not found!")
    for field, value in task_detail.model_dump(exclude_unset=True).items():
        setattr(find_task,field,value)
    db.commit()
    db.refresh(find_task)
    return find_task

@router.delete("/tasks/{task_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_by_id(task_id:int = Path(...,gt=0), db : Session = Depends(get_db)):
    find_task = db.query(Task_model).filter_by(id = task_id).one_or_none()
    if not find_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task is not found!")
    db.query(Task_model).filter_by(id = task_id).delete()
    db.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT)