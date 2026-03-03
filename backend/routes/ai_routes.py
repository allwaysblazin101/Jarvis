from fastapi import APIRouter, Request
from core.brain import brain

router = APIRouter()

@router.post("/ai/think")
async def ai_think(request: Request):
    body = await request.json()
    result = await brain.think(body)
    return result
