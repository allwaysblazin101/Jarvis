class GoalSystem:

    def evaluate(self, world):

        goals = []

        # Financial goal
        if world.state.get("financial"):
            goals.append("financial_awareness")
            goals.append("sync_banking")

        # Email optimization goal
        if world.state.get("email_load", 0) > 20:
            goals.append("optimize_inbox")

        return goals
