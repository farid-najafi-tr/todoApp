from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import func,Boolean,String,Integer,DateTime
from core.core.database import Base


class Task_model(Base):
    __tablename__ = "tasks"
    
    id : Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    title : Mapped[str] = mapped_column(String(150),nullable=False)
    description : Mapped[str] = mapped_column(String(500),nullable=True)
    is_completed : Mapped[bool] = mapped_column(Boolean,default=False)
    created_at : Mapped[str] = mapped_column(DateTime,server_default=func.now())
    updated_at : Mapped[str] = mapped_column(DateTime,server_onupdate=func.now(),server_default=func.now())