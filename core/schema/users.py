from pydantic import BaseModel, Field, EmailStr, field_validator,AnyUrl, ValidationInfo
from typing import Optional

from datetime import date
from core.models.users import (
    EnGender
)


class ProfileCreateSchema(BaseModel):
    bio : Optional[str] = Field(default=None,
                                max_length=150)
    
    first_name : Optional[str] = Field(default=None,
                                       max_length=50)
    
    last_name : Optional[str] = Field(default=None,
                                      max_length=50)
    
    date_of_birth : Optional[date] = Field(default=None)
    
    gender : Optional[EnGender] = Field(default=None)
    
    website : Optional[AnyUrl] = Field(default=None,
                                       examples=["https://x.com/","https://faridnajafi.ir/"])
    
    address : Optional[str] = Field(default=None,
                                    max_length=300)
    
    postal_code : Optional[str] = Field(default=None,
                                        examples=["3562983462","2635924682"],
                                        description="postal_code",
                                        max_length=10,
                                        pattern=r"^\d{10}$")
    
    national_id : Optional[str] = Field(default=None,
                                        max_length=10,
                                        pattern=r"^\d{10}$")
    

class UserCreateSchema(BaseModel):
    username : str = Field(min_length=5,
                           max_length=50)
    
    email : EmailStr
    
    password : str = Field(min_length=8,
                           max_length=100)
    
    password_repeat : str = Field(min_length=8,
                                    max_length=100)
    
    phone_number : Optional[str] = Field(default=None,
                               pattern=r"^09[0-9]{9}$")
    
    profile : Optional[ProfileCreateSchema] = Field(default=None)
    
    @field_validator('password_repeat', mode='after')
    @classmethod
    def check_passwords_match(cls, value: str, info: ValidationInfo) -> str:
        if value != info.data['password']:
            raise ValueError('Passwords do not match')
        return value

class ProfileResponseSchema(BaseModel):
    bio : str
    first_name : str
    last_name : str
    date_of_birth : date
    gender : str
    website : str
    address : str
    postal_code : str
    national_id : str

class UserResponseSchema(BaseModel):
    username : str
    email : EmailStr
    phone_number : str
    profile : ProfileResponseSchema
    
    
class ProfileUpdateSchema(BaseModel):
    bio : Optional[str] = Field(default=None)
    first_name : Optional[str] = Field(default=None)
    last_name : Optional[str] = Field(default=None)
    date_of_birth : Optional[date] = Field(default=None)
    website : Optional[str] = Field(default=None)
    address : Optional[str] = Field(default=None)
    postal_code : Optional[str] = Field(default=None)
    national_id : Optional[str] = Field(default=None)
    gender : Optional[EnGender] = Field(default=None)

class UserUpdateSchema(BaseModel):
    phone_number : Optional[str] = Field(default=None)
    profile : Optional[ProfileUpdateSchema] = Field(default=None)