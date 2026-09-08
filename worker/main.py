import json

from app.core.redis import redis_client
from app.queue.jobs import QUEUE_NAME

from worker.config import MAX_RETRIES, DLQ_QUEUE
from worker.idempotency import already_processed, mark_processed
from worker.metric_processor import process_metric


def process_job(job: dict):
    job_type = job.get("type")
    payload = job.get("payload", {})

    if job_type == "PROCESS_METRIC":
        metric_id = payload.get("metric_id")

        process_metric(metric_id)

    else:
        raise ValueError(
            f"Unknown job type: {job_type}"
        )


def move_to_dlq(job: dict):
    redis_client.lpush(
        DLQ_QUEUE,
        json.dumps(job),
    )

    print(
        f"Job {job['id']} moved to DLQ"
    )


def retry_job(job: dict):
    job["attempts"] = job.get("attempts", 0) + 1

    if job["attempts"] >= MAX_RETRIES:
        move_to_dlq(job)
        return

    redis_client.lpush(
        QUEUE_NAME,
        json.dumps(job),
    )

    print(
        f"Retrying job {job['id']} "
        f"(attempt {job['attempts']})"
    )


def main():
    print("Worker started...")

    while True:

        result = redis_client.brpop(
            QUEUE_NAME,
            timeout=0,
        )

        _, raw_job = result

        job = json.loads(raw_job)

        job_id = job["id"]

        if already_processed(job_id):
            print(
                f"Skipping already processed job: {job_id}"
            )
            continue

        try:

            print(
                f"Processing job {job['id']}"
            )

            process_job(job)

            mark_processed(job_id)

            print(
                f"Job {job['id']} completed successfully"
            )

        except Exception as exc:

            print(
                f"Job {job['id']} failed: {exc}"
            )

            retry_job(job)


if __name__ == "__main__":
    main()
