from fastapi import APIRouter

router = APIRouter()


@router.get("/exceptions")
def list_exception_tasks() -> dict[str, list[dict[str, str]]]:
    return {"items": []}


@router.get("/commands")
def list_commands() -> dict[str, list[dict[str, str]]]:
    return {"items": []}

