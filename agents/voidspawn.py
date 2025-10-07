from mesa import Agent
from algorithms.astar import astar_search
import random

class Voidspawn(Agent):
    """
    Predator: uses A* to hunt nearest Native.
    Moves one step along A* path each tick.
    """
    def __init__(self, pos, model):
        super().__init__(unique_id=f"void_{pos[0]}_{pos[1]}", model=model)
        self.pos = pos
        self.attack_range = 1
        # vision range from model default
        self.vision_range = getattr(model, "void_vision", 6)

    def step(self):
        # find nearest native
        natives = [a for a in self.model.schedule.agents if a.__class__.__name__ == "Native"]
        if not natives:
            # roam randomly if no natives
            self._random_move()
            return

        # compute Manhattan distances and pick nearest
        def manhattan(a_pos, b_pos):
            return abs(a_pos[0]-b_pos[0]) + abs(a_pos[1]-b_pos[1])

        natives_sorted = sorted(natives, key=lambda n: manhattan(self.pos, n.pos))
        target_native = natives_sorted[0]
        # if adjacent -> attack
        if manhattan(self.pos, target_native.pos) <= self.attack_range:
            # remove the native from schedule and grid
            try:
                self.model.grid.remove_agent(target_native)
            except Exception:
                pass
            try:
                self.model.schedule.remove(target_native)
            except Exception:
                pass
            return

        # else compute A* path to target_native.pos
        path = astar_search(self.model, start=self.pos, goal=target_native.pos)
        # move one step along path if possible (path includes start)
        if path and len(path) >= 2:
            next_pos = path[1]
            self.model.grid.move_agent(self, next_pos)
            self.pos = next_pos
        else:
            # fallback: random walk
            self._random_move()

    def _random_move(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        if neighbors:
            self.model.grid.move_agent(self, random.choice(neighbors))
