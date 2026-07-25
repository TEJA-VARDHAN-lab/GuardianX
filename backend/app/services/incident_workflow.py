from app.models.enums import IncidentStatus


ALLOWED_TRANSITIONS = {
    IncidentStatus.DETECTED: [
        IncidentStatus.VERIFIED,
        IncidentStatus.RESOLVED,
    ],

    IncidentStatus.VERIFIED: [
        IncidentStatus.RESPONDING,
        IncidentStatus.RESOLVED,
    ],

    IncidentStatus.RESPONDING: [
        IncidentStatus.CONTAINED,
        IncidentStatus.RESOLVED,
    ],

    IncidentStatus.CONTAINED: [
        IncidentStatus.RESOLVED,
    ],

    IncidentStatus.RESOLVED: [],
}


def can_transition(
    current_status: str,
    new_status: str,
) -> bool:

    try:
        current = IncidentStatus(current_status)
        new = IncidentStatus(new_status)

        return new in ALLOWED_TRANSITIONS[current]

    except ValueError:
        return False