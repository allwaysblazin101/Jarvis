async def proactive_life_analysis(
    emails,
    finances,
    schedule
):

    suggestions = []

    if len(emails) > 10:
        suggestions.append("You may have unread email overload")

    if finances == "High spending month":
        suggestions.append("Reduce discretionary purchases")

    if not schedule:
        suggestions.append("Add workout schedule")

    return suggestions
