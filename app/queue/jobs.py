import json
import uuid

from app.core.redis import redis_client

QUEUE_NAME = "reliability:jobs"


def enqueue_job(job_type: str, payload: dict):
    job = {
        "id": str(uuid.uuid4()),
        "type": job_type,
        "payload": payload,
        "attempts": 0,
    }

    redis_client.lpush(
        QUEUE_NAME,
        json.dumps(job),
    )

    return job
