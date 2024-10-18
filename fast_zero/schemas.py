from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from fast_zero.models import TodoState


class MessageSchema(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDBSchema(UserSchema):
    id: int


class UserPublicSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UsersListSchema(BaseModel):
    users: list[UserPublicSchema]


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    username: str | None = None


class TodoUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoPublicSchema(TodoSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class TodoListSchema(BaseModel):
    todos: list[TodoPublicSchema]


class FilterPageSchema(BaseModel):
    offset: int = 0
    limit: int = 100


class FilterTodoSchema(FilterPageSchema):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
