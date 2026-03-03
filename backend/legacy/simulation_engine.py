class SimulationEngine:

    def simulate(self, action, world):

        # Non-financial actions get neutral score
        if action["type"] in ["clean_email", "sync_plaid"]:
            return {
                "action": action,
                "expected_return": 0.1,
                "risk": 0.01
            }

        if action["type"] == "analyze_finances":
            return {
                "action": action,
                "expected_return": 0.2,
                "risk": 0.05
            }

        return {
            "action": action,
            "expected_return": 0,
            "risk": 0
        }
