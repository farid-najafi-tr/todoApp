from fastapi import APIRouter,Path,Depends,HTTPException,status,Query
from core.core.database import get_db
from sqlalchemy.orm import Session
# from core.schema import (
#     ...
# )
from core.models.users import User,Profile
from typing import List

router = APIRouter(
    tags= ["users"],
    prefix="/users"
)

