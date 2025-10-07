from mesa import Agent

class Obstacle(Agent):
    """
    Obstacle blocks movement (treated as impassable).
    """
    def __init__(self, pos, model):
        super().__init__(unique_id=f"obstacle_{pos[0]}_{pos[1]}", model=model)
        self.pos = pos
        self.blocks = True
