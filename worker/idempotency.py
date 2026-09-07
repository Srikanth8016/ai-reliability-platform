from app.core.redis import redis_client


def already_processed(job_id: str) -> bool:
    return redis_client.exists(
        f"reliability:processed:{job_id}"
    ) == 1


def mark_processed(job_id: str):
    redis_client.set(
        f"reliability:processed:{job_id}",
        "1",
        ex=86400,
    )
