from fastapi import APIRouter

router = APIRouter(
    tags= ["tasks"],
    prefix="/todo"
)

@router.get("/tasks")
async def get_all_task_list():
    return []


@router.get("/tasks/{task_id}")
def get_task_detail_by_id(task_id:int):
    return []