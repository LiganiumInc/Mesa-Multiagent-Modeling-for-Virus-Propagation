from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .model import TissuAttack

COLORS = {"Safe": "Orange", "Infected": "Red", "Dead": "Black","Immunise":"Green"}


def Tissu_Attack_portrayal(cellule):
    if cellule is None:
        return
    # portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    portrayal = {"Shape": "circle", "r":0.5, "Filled": "true", "Layer": 0}
    (x, y) = cellule.pos
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[cellule.condition]
    return portrayal


canvas_element = CanvasGrid(Tissu_Attack_portrayal, 50, 50, 500, 500)
cellule_chart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)
pie_chart = PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()],
    canvas_height=400, canvas_width=800
)

model_params = {
    "height": 50,
    "width": 50,
    "density": UserSettableParameter("slider", "cellule density", 0.65, 0.01, 1.0, 0.01),
    "resistance_density" : UserSettableParameter("slider", "Resistance Density", 0.2, 0.01, 1.0, 0.01) ,
    "virulence" : UserSettableParameter("slider", "Virulence Level", 4, 1, 10, 1)
}
server = ModularServer(
    TissuAttack, [canvas_element, cellule_chart, pie_chart], "Propagation de virus dans un Tissu Cellulaire", model_params
)
