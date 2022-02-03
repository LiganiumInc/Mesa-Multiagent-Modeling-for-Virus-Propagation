from mesa import Agent


class Cellule(Agent):
    """
    A tree cell.

    Attributes:
        x, y: Grid coordinates
        condition: Can be "Safe", "Infected", "Immunise" or "Dead"
        unique_id: (x,y) tuple.

    unique_id isn't strictly necessary here, but it's good
    practice to give one to each agent anyway.
    """

    def __init__(self, pos, model,resistance):
        """
        Create a new cellule.
        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Safe"
        self.resistance = resistance

    def step(self):
        """
        If the cellule is infected, spread it to Safe cellules nearby.
        """
        if self.condition == "Infected":
            for neighbor in self.model.grid.neighbor_iter(self.pos):
                if neighbor.condition == "Safe":
                    neighbor.condition = "Infected"
            
            # self.condition = "Dead"
            if self.model.virulence > self.resistance:
                self.condition = "Dead"
            else:
                self.condition = "Immunise"
                # Ce qui ne nous tue pas nous rend plus fort