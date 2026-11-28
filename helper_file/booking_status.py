# utils/status_helper.py

STATUS_NEW = "NIEUW"
STATUS_VALIDATED = "GOEDGEKEURD"
STATUS_REJECTED = "AFGEKEURD"
STATUS_BOOKED = "GEBOEKT"
STATUS_PAID = "BETAALD"


def get_status_label(status: str) -> str:
    """
    Geeft een status weer met icoon.
    """

    labels = {
        STATUS_NEW: "🔵 NIEUW",
        STATUS_VALIDATED: "🟢 GOEDGEKEURD",
        STATUS_REJECTED: "🔴 AFGEKEURD",
        STATUS_BOOKED: "🟠 GEBOEKT",
        STATUS_PAID: "✅ BETAALD"
    }

    return labels.get(status, f"❓ {status}")


def get_status_color(status: str) -> str:
    """
    Geeft de kleur van een status terug.
    """

    colors = {
        STATUS_NEW: "blauw",
        STATUS_VALIDATED: "groen",
        STATUS_REJECTED: "rood",
        STATUS_BOOKED: "oranje",
        STATUS_PAID: "donkergroen"
    }

    return colors.get(status, "grijs")


def is_editable(status: str) -> bool:
    """
    Bepaalt of een factuur nog aangepast mag worden.
    """

    return status in [
        STATUS_NEW,
        STATUS_REJECTED
    ]


def can_be_booked(status: str) -> bool:
    """
    Alleen gevalideerde facturen mogen geboekt worden.
    """

    return status == STATUS_VALIDATED


def can_be_paid(status: str) -> bool:
    """
    Alleen geboekte facturen mogen betaald worden.
    """

    return status == STATUS_BOOKED


def get_next_status(status: str) -> str | None:
    """
    Geeft de volgende status in de workflow.
    """

    workflow = {
        STATUS_NEW: STATUS_VALIDATED,
        STATUS_VALIDATED: STATUS_BOOKED,
        STATUS_BOOKED: STATUS_PAID
    }

    return workflow.get(status)


def get_allowed_transitions(status: str) -> list[str]:
    """
    Geeft alle toegestane vervolgstappen.
    """

    transitions = {
        STATUS_NEW: [
            STATUS_VALIDATED,
            STATUS_REJECTED
        ],

        STATUS_REJECTED: [
            STATUS_VALIDATED
        ],

        STATUS_VALIDATED: [
            STATUS_BOOKED
        ],

        STATUS_BOOKED: [
            STATUS_PAID
        ],

        STATUS_PAID: []
    }

    return transitions.get(status, [])