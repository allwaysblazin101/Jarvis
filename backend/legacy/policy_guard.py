class PolicyGuard:

    def approve(self, action_data):
        action = action_data["action"]

        # Block high risk
        if action_data["score"] < 0:
            return False

        # Require manual approval for trades
        if action["type"] == "buy_asset":
            print("Manual approval required for trade.")
            return False

        return True
