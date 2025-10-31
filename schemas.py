# from pydantic import BaseModel, EmailStr
# from typing import Optional

# # ---------- User ----------
# class UserCreate(BaseModel):
#     username: str
#     email: EmailStr
#     # password: str

# class UserOut(BaseModel):
#     id: int
#     username: str
#     email: EmailStr

#     class Config:
#         orm_mode = True

# # ---------- Task ----------
# class TaskCreate(BaseModel):
#     title: str
#     description: Optional[str] = None
#     status: Optional[str] = "pending"

# class TaskUpdate(BaseModel):
#     title: Optional[str] = None
#     description: Optional[str] = None
#     status: Optional[str] = None

# class TaskOut(BaseModel):
#     id: int
#     title: str
#     description: Optional[str]
#     status: str
#     owner_id: int

#     class Config:
#         orm_mode = True




from pydantic import BaseModel, EmailStr
from typing import Optional


# -------------------------
# User Schemas
# -------------------------
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True   # ✅ Pydantic v2 compatible


# -------------------------
# Task Schemas
# -------------------------
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "Pending"   # Default status


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class TaskOut(TaskBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True   # ✅ Pydantic v2 compatible
