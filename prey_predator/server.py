from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


def wolf_sheep_portrayal(agent, fast=True):
    """Display function."""
    if agent is None:
        return

    portrayal = {
        "Shape": "circle",
        "Color": "red",
        "Filled": "false",
        "Layer": 0,
        "r": 0.5,
    }

    if isinstance(agent, Sheep):
        portrayal['Layer'] = 1
        if fast:
            portrayal['Color'] = "blue"
        else:
            portrayal["Shape"] = "sheep.jpg"

    elif isinstance(agent, Wolf):
        portrayal['Layer'] = 2
        if fast:
            portrayal['Color'] = "red"
        else:
            portrayal["Shape"] = "wolf.webp"

    elif isinstance(agent, GrassPatch):
        portrayal['Layer'] = 0
        if agent.alive:
            if fast:
                portrayal['Color'] = "#00ff00f0"
                portrayal['Shape'] = "rect"
                portrayal['w'] = 1.
                portrayal['h'] = 1.
            else:
                portrayal["Shape"] = "grass.jpg"
        else:
            portrayal["Shape"] = "None"
    return portrayal


chart_element = ChartModule(
    [
        {"Label": "Wolves", "Color": "#AA0000"},
        {"Label": "Sheep", "Color": "#666666"},
        # {"Label": "Grass", "Color": "#00FF00"},
    ]
)
model_params = {
    "initial_sheep": UserSettableParameter(
        "slider",
        "Initial Wealth",
        value=100,
        min_value=1,
        max_value=10,
        description="Initial wealth",
    ),
    "initial_wolves": UserSettableParameter(
        "slider",
        "Initial Wealth",
        value=40,
        min_value=1,
        max_value=10,
        description="Initial wealth",
    ),
    "width": 50,
    "height": 50,
}
canvas_element = CanvasGrid(
    wolf_sheep_portrayal, model_params["width"], model_params["height"], 500, 500
)

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
