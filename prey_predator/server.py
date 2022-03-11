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
        portrayal["Layer"] = 1
        if fast:
            portrayal["Color"] = "blue"
        else:
            portrayal["Shape"] = "sheep.jpg"

    elif isinstance(agent, Wolf):
        portrayal["Layer"] = 2
        if fast:
            portrayal["Color"] = "red"
        else:
            portrayal["Shape"] = "wolf.webp"

    elif isinstance(agent, GrassPatch):
        portrayal["Layer"] = 0
        portrayal["Shape"] = "rect"
        portrayal["w"] = 1.0
        portrayal["h"] = 1.0
        if agent.alive:
            if fast:
                portrayal["Color"] = "#48bf53f0"

            else:
                portrayal["Shape"] = "grass.jpg"
        else:
            portrayal["Color"] = "#91f086f0"
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
        "Initial Number of Sheeps",
        value=100,
        min_value=1,
        max_value=200,
        description="Initial Sheeps",
    ),
    "initial_wolves": UserSettableParameter(
        "slider",
        "Initial Number of Wolves",
        value=50,
        min_value=1,
        max_value=200,
        description="Initial Wolves",
    ),
    "initial_wolf_enery": UserSettableParameter(
        "slider",
        "Initial Wolves energy",
        value=3,
        min_value=1,
        max_value=100,
        description="Initial Wolves Energy",
    ),
    "initial_sheep_energy": UserSettableParameter(
        "slider",
        "Initial Sheeps Energy",
        value=10,
        min_value=1,
        max_value=100,
        description="Initial Sheeps Energy",
    ),
    "wolf_gain_from_food": UserSettableParameter(
        "slider",
        "Wolf gain of food",
        value=20,
        min_value=1,
        max_value=200,
        description="Wolf food gain",
    ),
    "sheep_reproduce": UserSettableParameter(
        "slider",
        "Proba to multiply a sheep",
        value=0.04,
        min_value=0,
        max_value=1,
        step=0.01,
        description="Probability to reproduce for sheeps",
    ),
    "wolf_reproduce": UserSettableParameter(
        "slider",
        "Proba to multiply a wolf",
        value=0.05,
        min_value=0,
        max_value=1,
        step=0.01,
        description="Probability to reproduce wolves",
    ),
    "width": 20,
    "height": 20,
}
canvas_element = CanvasGrid(
    wolf_sheep_portrayal, model_params["width"], model_params["height"], 500, 500
)

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
