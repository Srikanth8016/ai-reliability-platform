from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.alert_rule import AlertRule
from app.repositories.alert_repository import create_alert, get_active_alert
from app.services.incident_automation import create_incident_from_alert


def threshold_exceeded(
    value: float,
    operator: str,
    threshold: float,
) -> bool:

    if operator == ">":
        return value > threshold

    if operator == ">=":
        return value >= threshold

    if operator == "<":
        return value < threshold

    if operator == "<=":
        return value <= threshold

    return False


def evaluate_alert_rule(
    db: Session,
    rule: AlertRule,
    metric_value: float,
):

    exceeded = threshold_exceeded(
        metric_value,
        rule.operator,
        rule.threshold,
    )

    if not exceeded:
        return None

    alert_name = f"{rule.metric_name} threshold exceeded"

    existing_alert = get_active_alert(
        db,
        rule.service_id,
        alert_name,
    )

    if existing_alert:
        return existing_alert

    alert = Alert(
        service_id=rule.service_id,
        name=alert_name,
        message=(
            f"{rule.metric_name} value "
            f"{metric_value} crossed "
            f"threshold {rule.threshold}"
        ),
        severity=rule.severity,
        status="ACTIVE",
    )

    alert = create_alert(db, alert)

    create_incident_from_alert(
        db,
        alert,
    )

    return alert
