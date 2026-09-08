from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.metric import Metric
from app.repositories.alert_rule_repository import get_alert_rules
from app.services.alert_engine import evaluate_alert_rule


def process_metric(metric_id: int):
    db = SessionLocal()

    try:
        metric = db.execute(
            select(Metric).where(
                Metric.id == metric_id
            )
        ).scalar_one_or_none()

        if not metric:
            raise ValueError(
                f"Metric {metric_id} not found"
            )

        print(
            f"Processing metric #{metric.id}: "
            f"{metric.name}={metric.value}"
        )

        rules = get_alert_rules(
            db,
            service_id=metric.service_id,
        )

        matching_rules = [
            rule
            for rule in rules
            if rule.metric_name == metric.name
        ]

        if not matching_rules:
            print(
                f"No alert rules found for "
                f"{metric.name}"
            )
            return

        for rule in matching_rules:
            alert = evaluate_alert_rule(
                db,
                rule,
                metric.value,
            )

            if alert:
                print(
                    f"Alert active: "
                    f"#{alert.id} {alert.name}"
                )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
