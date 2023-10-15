from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root() -> str:
    return "hello world"
