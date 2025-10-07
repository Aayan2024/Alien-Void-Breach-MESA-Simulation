from mesa import Agent

class TerrainTile(Agent):
    """
    Static terrain tile that holds movement_cost.
    Multiple terrain tiles may coexist in a cell but model places one per cell.
    """
    def __init__(self, pos, model, movement_cost=1.0):
        super().__init__(unique_id=f"terrain_{pos[0]}_{pos[1]}", model=model)
        self.pos = pos
        self.movement_cost = float(movement_cost)
