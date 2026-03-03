import asyncio
from core.world_model import WorldModel
from core.goal_system import GoalSystem
from core.simulation_engine import SimulationEngine
from core.decision_engine import DecisionEngine
from core.policy_guard import PolicyGuard


class JarvisBrain:

    def __init__(self):
        self.world = WorldModel()
        self.goals = GoalSystem()
        self.simulator = SimulationEngine()
        self.decision_engine = DecisionEngine()
        self.policy = PolicyGuard()

    async def think(self, perception: dict):
        """
        Master Cognitive Loop
        """

        # 1. Perceive
        self.world.update(perception)

        # 2. Reevaluate goals
        active_goals = self.goals.evaluate(self.world)

        # 3. Generate possible actions
        possible_actions = self.decision_engine.generate_actions(self.world, active_goals)

        if not possible_actions:
            return {"status": "no_action"}

        # 4. Simulate outcomes
        simulated = []
        for action in possible_actions:
            result = self.simulator.simulate(action, self.world)
            simulated.append(result)

        # 5. Score expected value
        scored = self.decision_engine.score(simulated)

        # 6. Select best action
        best_action = max(scored, key=lambda x: x["score"])

        # 7. Apply policy guard
        if not self.policy.approve(best_action):
            return {"status": "blocked_by_policy", "reason": "Risk or permission violation"}

        # 8. Execute
        execution_result = await self.decision_engine.execute(best_action)

        # 9. Learn
        self.world.store_outcome(best_action, execution_result)

        return {
            "status": "executed",
            "action": best_action,
            "result": execution_result
        }


brain = JarvisBrain()
