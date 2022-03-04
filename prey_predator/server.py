from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {
        "Color": "red",
        "Filled": "true",
        "Layer": 0,
        "r": 0.5,
    }

    if type(agent) is Sheep:
        portrayal["Shape"] = "sheep.jpg"
        # ... to be completed
        pass

    elif type(agent) is Wolf:
        portrayal["Shape"] = "wolf.webp"
        # ... to be completed
        pass

    elif type(agent) is GrassPatch:
        # ... to be completed
        portrayal['Shape'] = "grass.jpg"

        pass
    return portrayal


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#AA0000"},
     {"Label": "Sheep", "Color": "#666666"},
     {"Label": "Grass", "Color": "#00FF00"}, ]
)
model_params = {
    "initial_sheep": UserSettableParameter("slider", "Initial Wealth", value=100, min_value=1, max_value=10, description="Initial wealth"),
    "initial_wolves": UserSettableParameter("slider", "Initial Wealth", value=40, min_value=1, max_value=10, description="Initial wealth"),
    "initial_grass":  UserSettableParameter("slider", "Initial Wealth", value=50, min_value=1, max_value=10, description="Initial wealth"),
}

server = ModularServer(
    WolfSheep, [canvas_element,
                chart_element], "Prey Predator Model", model_params
)
server.port = 8521
