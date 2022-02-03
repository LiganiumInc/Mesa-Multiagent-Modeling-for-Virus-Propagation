from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid, SingleGrid
from mesa.time import RandomActivation
import random

from .agent import Cellule


class TissuAttack(Model):
    """
    Modèle simple de propagation d'un virus dans un Tissu.
    """

    def __init__(self, height, width, density,resistance_density,virulence):
        """
        Create a new forest fire model.

        Args:
            height, width: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """
        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(height, width, torus=False)

        self.density = density
        self.virulence = virulence
        self.resistance_density = resistance_density

        self.datacollector = DataCollector(
            {
                "Safe": lambda m: self.count_type(m, "Safe"),
                "Infected": lambda m: self.count_type(m, "Infected"),
                "Dead": lambda m: self.count_type(m, "Dead"),
                "Immunise": lambda m: self.count_type(m, "Immunise"),
            }
        )

        # Place a tree in each cell with Prob = density
        for (contents, x, y) in self.grid.coord_iter():
            if random.random() < self.density:
                
                if random.random() < self.resistance_density:
                    cell_resistance = random.randint(virulence + 1,10)
                else:
                    cell_resistance = random.randint(1,virulence-1)

                # cell_resistance = 4

                # Create a cellule
                new_cellule = Cellule((x, y), self,cell_resistance)
                # Set all trees in the first column on fire.
                if 0 < x <4  and y > 45:
                    new_cellule.condition = "Infected"
                self.grid._place_agent((x, y), new_cellule)
                self.schedule.add(new_cellule)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Halt if no more Infected
        if self.count_type(self, "Infected") == 0:
            self.running = False

    @staticmethod
    def count_type(model, cell_condition):
        """
        Helper method to count cellules in a given condition in a given model.
        """
        count = 0
        for cellule in model.schedule.agents:
            if cellule.condition == cell_condition:
                count += 1
        return count
