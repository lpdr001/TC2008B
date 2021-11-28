from activity.agents import Car
from mesa import agent
from mesa.visualization.ModularVisualization import ModularServer
from .model import TwoWayIntersectionModel
from .agents import Car, Street, TrafficLight

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import UserSettableParameter

def agent_portrayal(agent):
    if agent is None:
        return
    
    portrayal = {"Filled": "true"}
    if type(agent) is Car:
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "cyan"
        portrayal["r"] = 0.3
        portrayal["Layer"] = 3

    elif type(agent) is Street:
        if (agent.type != "Non"):
            portrayal["Shape"] = "circle"
            portrayal["Color"] = "blue"
            portrayal["r"] = 0.4
            portrayal["Layer"] = 1
        else:
            return


    elif type(agent) is TrafficLight:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 2
        if (agent.status == 0):
            portrayal["Color"] = "green"
        elif (agent.status == 1):
            portrayal["Color"] = "red"
        else:
            portrayal["Color"] = "yellow"

    return portrayal

grid = CanvasGrid(agent_portrayal, 8, 8, 480, 480)
model_params = {
    "N": UserSettableParameter(
        "slider",
        "Number of agents",
        5,
        2,
        10,
        1,
        description="Choose how many cars to include in the model",
    ),
    "width":10,
    "height":10,
}

server = ModularServer(TwoWayIntersectionModel, [grid], "Two Way Intersection", model_params)
server.port = 8521