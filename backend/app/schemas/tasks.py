from pydantic import BaseModel


class ExceptionTask(BaseModel):
    id: str
    type: str
    title: str
    severity: str
    owner_role: str
    next_action: str


class ExceptionTaskList(BaseModel):
    items: list[ExceptionTask]

