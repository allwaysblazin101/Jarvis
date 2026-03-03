class DecisionEngine:

    def generate_actions(self, world, goals):

        actions = []

        if "optimize_inbox" in goals:
            actions.append({"type": "clean_email"})

        if "financial_awareness" in goals:
            actions.append({"type": "analyze_finances"})

        if "sync_banking" in goals:
            actions.append({"type": "sync_plaid"})

        return actions

    def score(self, simulations):
        scored = []

        for sim in simulations:
            score = sim.get("expected_return", 0) - sim.get("risk", 0)
            scored.append({
                "action": sim["action"],
                "score": score
            })

        return scored
