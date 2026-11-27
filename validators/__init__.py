def status_icon(status):

    if status == "NEW":
        return "🔵 NEW"

    if status == "VALIDATED":
        return "🟢 VALIDATED"

    if status == "REJECTED":
        return "🔴 REJECTED"

    if status == "BOOKED":
        return "🟠 BOOKED"

    if status == "PAID":
        return "✅ PAID"

    return status