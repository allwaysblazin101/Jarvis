class WorldModel:

    def __init__(self):
        self.state = {
            "financial": {
                "cash_balance": 0,
                "portfolio_value": 0,
                "risk_tolerance": 0.5
            },
            "opportunities": [],
            "threats": [],
            "history": []
        }

    def update(self, perception: dict):
        for key, value in perception.items():
            self.state[key] = value

    def store_outcome(self, action, result):
        self.state["history"].append({
            "action": action,
            "result": result
        })
