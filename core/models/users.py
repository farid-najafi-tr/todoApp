from sqlalchemy import (
    Integer,
    String,
    DateTime,
    Boolean,
    Enum as SqlEnum,
    Text
)
from sqlalchemy.sql import func
from core.core.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from enum import Enum
from datetime import date

from typing import Optional


def enum_values(enum_class: type[Enum]) -> list[str]:
    """Persist an enum's values instead of its Python member names."""
    return [member.value for member in enum_class]

# Enum sections
class EnUserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"
    BLOCKED = "blocked"
    
class EnUserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"
    SUPER_ADMIN = "super_admin"

class EnPermissionLevel(str, Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    FULL = "full"

class EnGender(str,Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


#table's and relationship sections
class User(Base):
    __tablename__ = "tblUsers"
    
    id : Mapped[int] = mapped_column(Integer,autoincrement=True,primary_key=True,index=True)
    
    username : Mapped[str] = mapped_column(
        String(50),
        index=True,
        unique=True,
        nullable=False)
    
    email : Mapped[str] = mapped_column(
        String(250),
        nullable=False,
        unique=True)
    
    password : Mapped[str] = mapped_column(
        String(500),
        nullable=False)
    
    phone_number: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        unique=True)
    
    created_at : Mapped[date] = mapped_column(
        DateTime(True),
        server_default=func.now())
    
    updated_at : Mapped[date] = mapped_column(
        DateTime(True),
        nullable=True,
        server_onupdate=func.now())
    
    status : Mapped[EnUserStatus] = mapped_column(
        SqlEnum(EnUserStatus, values_callable=enum_values),
        default=EnUserStatus.PENDING,
        nullable=False,
        server_default=EnUserStatus.PENDING.value)
    
    role: Mapped[EnUserRole] = mapped_column(
        SqlEnum(EnUserRole, values_callable=enum_values),
        default=EnUserRole.USER,
        nullable=False,
        server_default=EnUserRole.USER.value)
    
    permission_level : Mapped[EnPermissionLevel] = mapped_column(
        SqlEnum(EnPermissionLevel, values_callable=enum_values),
        default=EnPermissionLevel.READ,
        nullable=False,
        server_default=EnPermissionLevel.READ.value)
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False)
    
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False)
    
    is_delete: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True)
    
    last_login: Mapped[Optional[date]] = mapped_column(
        DateTime(True),
        nullable=True)
    
    deleted_at: Mapped[Optional[date]] = mapped_column(
        DateTime(True),
        nullable=True)
    
    profile: Mapped[Optional["Profile"]] = relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="all,delete-orphan",
        single_parent=True,
        lazy="joined")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', role={self.role})>"
    
    def __str__(self) -> str:
        return f"{self.username} ({self.email})"
    
    def soft_delete(self) -> None:
        self.is_delete = True
        self.deleted_at = func.now()
    
    def is_admin(self) -> bool:
        return self.role in [EnUserRole.ADMIN, EnUserRole.SUPER_ADMIN]
    
    def has_permission(self, required_level: EnPermissionLevel) -> bool:
        permission_order = {
            EnPermissionLevel.READ: 1,
            EnPermissionLevel.WRITE: 2,
            EnPermissionLevel.DELETE: 3,
            EnPermissionLevel.FULL: 4,
        }
        return permission_order[self.permission_level] >= permission_order[required_level]
    
    
class Profile(Base):
    __tablename__ = "tblProfile"

    id: Mapped[int] = mapped_column(
        Integer,
        autoincrement=True,
        primary_key=True,
        index=True
    )

    bio: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    profile_url: Mapped[Optional[str]] = mapped_column(
        String(250),
        nullable=True
    )
    
    national_id : Mapped[Optional[str]] = mapped_column(
            String(10),
            unique=True,
            nullable=True
        )
    
    first_name : Mapped[str] = mapped_column(
            String(50),
            nullable=True)

    last_name : Mapped[str] = mapped_column(
        String(50),
        nullable=True)
    
    date_of_birth: Mapped[Optional[date]] = mapped_column(
        DateTime(True),
        nullable=True
    )
    
    gender: Mapped[Optional[EnGender]] = mapped_column(
        SqlEnum(EnGender, values_callable=enum_values),
        nullable=True)

    website: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True
    )
    
    postal_code : Mapped[Optional[str]] = mapped_column(
                    String(10),
                    nullable=True
                )
    
    address: Mapped[Optional[str]] = mapped_column(
            Text,
            nullable=True
        )

    user_id_fk: Mapped[int] = mapped_column(
        ForeignKey("tblUsers.id", ondelete="CASCADE"),
        unique=True,  
        nullable=False 
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="profile",
        single_parent=True
    )

    def __repr__(self) -> str:
        return f"<Profile(id={self.id}, user_id={self.user_id_fk})>"

    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.last_name or ""