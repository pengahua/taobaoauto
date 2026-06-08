from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.init_db import init_db
from app.db.session import get_db
from app.repositories.exception_tasks import ExceptionTaskRepository
from app.schemas.tasks import ExceptionTask, ExceptionTaskList

router = APIRouter()


@router.get("/exceptions", response_model=ExceptionTaskList)
def list_exception_tasks(db: Session = Depends(get_db)) -> ExceptionTaskList:
    init_db()
    repository = ExceptionTaskRepository(db)
    repository.seed_defaults()
    db.commit()
    records = repository.list_open()
    return ExceptionTaskList(
        items=[
            ExceptionTask(
                id=record.id,
                type=record.type,
                title=record.title,
                severity=record.severity,
                owner_role=record.owner_role,
                next_action=record.next_action,
            )
            for record in records
        ]
    )


@router.get("/commands")
def list_commands() -> dict[str, list[dict[str, str]]]:
    return {"items": []}
