from fastapi import APIRouter

from app.core.redis import redis_client

router = APIRouter(
    prefix="/redis",
    tags=["Redis"],
)


@router.get("/test")
def test_redis():
    redis_client.set("test", "Redis is working")
    value = redis_client.get("test")
    return {"redis": value}
