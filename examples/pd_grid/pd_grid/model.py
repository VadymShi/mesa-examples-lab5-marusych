import mesa
from mesa import Model, DataCollector
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from .agent import PDAgent

class PdGrid(Model):
    """Model class for iterated, spatial prisoner's dilemma model."""

    activation_regimes = ["Sequential", "Random", "Simultaneous"]
    payoff = {("C", "C"): 1, ("C", "D"): 0, ("D", "C"): 1.6, ("D", "D"): 0}

    def __init__(self, width=50, height=50, activation_order="Random", seed=None):
        super().__init__(seed)

        if activation_order not in self.activation_regimes:
            raise ValueError(f"Invalid activation order: {activation_order}")

        self.activation_order = activation_order
        self.grid = SingleGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)  # Додаємо план

        # Create agents with unique IDs
        for unique_id, (x, y) in enumerate((x, y) for x in range(width) for y in range(height)):
            agent = PDAgent(self, unique_id)  # Передача унікального ID
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)  # Додаємо агента до плану

        self.datacollector = DataCollector(
            {
                "Cooperating_Agents": lambda m: len([a for a in m.schedule.agents if a.isCooperating])
            }
        )

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        match self.activation_order:
            case "Sequential":
                self.schedule.step()
            case "Random":
                self.schedule.step()
            case "Simultaneous":
                self.schedule.step()
                for agent in self.schedule.agents:
                    agent.advance()
            case _:
                raise ValueError(f"Unknown activation order: {self.activation_order}")

        self.datacollector.collect(self)

    def run(self, n):
        """Run the model for n steps."""
        for _ in range(n):
            self.step()
