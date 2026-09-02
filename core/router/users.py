from fastapi import(
    APIRouter,
    Path,
    Depends,
    HTTPException,
    status,
    Query
)
from core.schema import (
    UserCreateSchema,
    ProfileCreateSchema,
    ProfileResponseSchema,
    ProfileUpdateSchema,
    UserResponseSchema,
    UserUpdateSchema
)
from sqlalchemy.orm import (
    Session,
    load_only
)
from sqlalchemy.exc import IntegrityError
from typing import List
from core.core.database import get_db
from core.models.users import UserModel,ProfileModel
from sqlalchemy import and_


router = APIRouter(
    tags= ["users"],
    prefix="/users"
)

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_user(
    user_detail: UserCreateSchema,
    db: Session = Depends(get_db),
    ):
    profile_data = None
    if user_detail.profile is not None:
        profile_values = user_detail.profile.model_dump()
        if profile_values["website"] is not None:
            profile_values["website"] = str(profile_values["website"])
        profile_data = ProfileModel(**profile_values)
    
    new_user = UserModel(
        username=user_detail.username,
        email=user_detail.email,
        password=user_detail.password,
        phone_number=user_detail.phone_number,
        profile=profile_data,
        )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username, email, phone number or national ID already exists",
        )
    return {
        "message": "User created successfully",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "phone_number": new_user.phone_number,
            "status": new_user.status,
            "role": new_user.role,
            "profile": (
                {
                    "id": new_user.profile.id,
                    "first_name": new_user.profile.first_name,
                    "last_name": new_user.profile.last_name,
                    "bio": new_user.profile.bio,
                }
                if new_user.profile is not None
                else None
            ),
        },
    }

    
@router.get("/user/{user_id}",response_model=UserResponseSchema,status_code=status.HTTP_200_OK)
def get_user_detail_by_id(user_id : int, db : Session = Depends(get_db)):
    user_detail = db.query(UserModel).options(load_only(
        UserModel.id,
        UserModel.username,
        UserModel.email,
        UserModel.phone_number
        )).where(
            UserModel.id == user_id,
            UserModel.is_delete == False).one_or_none()
    if not user_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found!!!")
    return user_detail


@router.get("/all-users/",status_code=status.HTTP_200_OK)
def get_users(db : Session = Depends(get_db)):
    user_detail = db.query(UserModel).options(load_only(
        UserModel.id,
        UserModel.username,
        UserModel.email,
        UserModel.phone_number,
        )).all()
    if not user_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found!!!")
    return user_detail


@router.delete("/delete-user/{user_id}")
def delete_user_by_id(
    user_id: int,
    db: Session = Depends(get_db)
):
    find_user = db.query(UserModel).where(
            and_(UserModel.is_delete == False,
                 UserModel.id == user_id)).one_or_none()
    if find_user:
        find_user.soft_delete()
        db.commit()
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message" : "User not found!!"})


@router.patch("/update/user/detail/{user_id}")
def update_user_data(
    user_id: int,
    user_detail: UserUpdateSchema,
    db: Session = Depends(get_db)
):
    find_user = (
        db.query(UserModel).where(
            and_(UserModel.is_delete == False,
                 UserModel.id == user_id)).one_or_none()
    )
    if find_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    up_detail = user_detail.model_dump(exclude_unset=True)
    up_prof = up_detail.pop("profile", None)
    for key, value in up_detail.items():
        setattr(find_user, key, value)
    if up_prof is not None:
        if find_user.profile is None:
            find_user.profile = ProfileModel(**up_prof)
        else:
            for key, value in up_prof.items():
                setattr(find_user.profile, key, value)
    try:
        db.commit()
        db.refresh(find_user)
        return find_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Phone number or national ID already exists",
        )


@router.put("/update/user/{user_id}",
            response_model=UserResponseSchema,
            status_code=status.HTTP_200_OK
)
def replace_user_data(
    user_id: int,
    user_detail: UserUpdateSchema,
    db: Session = Depends(get_db)
):
    find_user = (
        db.query(UserModel)
        .filter(UserModel.id == user_id)
        .one_or_none()
    )

    if find_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    update_data = user_detail.model_dump()
    profile_data = update_data.pop("profile", None)
    for key, value in update_data.items():
        setattr(find_user, key, value)
    if profile_data is not None:
        if find_user.profile is None:
            find_user.profile = ProfileModel(**profile_data)
        else:
            for key, value in profile_data.items():
                setattr(find_user.profile, key, value)
    try:
        db.commit()
        db.refresh(find_user)
        return find_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Phone number or national ID already exists",
        )