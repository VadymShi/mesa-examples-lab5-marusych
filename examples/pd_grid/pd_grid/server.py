import mesa
from .model import PdGrid
from .portrayal import portrayPDAgent

# Створення елемента Canvas для відображення агента
canvas_element = mesa.visualization.CanvasGrid(portrayPDAgent, 250, 250, 500, 500)

# Параметри моделі
model_params = {
    "width": 250,  # Ширина моделі
    "height": 250,  # Висота моделі
    "activation_order": mesa.visualization.Choice(
        "Activation regime",
        value="Random",
        choices=PdGrid.activation_regimes,
    ),
}

# Ініціалізація сервера
server = mesa.visualization.ModularServer(
    PdGrid,
    [canvas_element],
    "Prisoner's Dilemma",
    model_params,
)
