from datetime import datetime

from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    publish_time: datetime = Field(default=datetime.now())
    comment_content: str
    user_id: int
    medicine_id: int


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    pass


class Comment(CommentBase):
    id: int

    class Config:
        orm_mode = True
