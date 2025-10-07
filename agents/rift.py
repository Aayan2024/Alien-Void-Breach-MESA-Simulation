from mesa import Agent
import random
from agents.voidspawn import Voidspawn

class Rift(Agent):
    """
    Rift periodically spawns Voidspawns at its location.
    spawn_interval: initial ticks between spawns (provided from model)
    rift_accelerate: if True, interval will slowly reduce after each spawn
    """
    def __init__(self, pos, model, spawn_interval=30):
        super().__init__(unique_id=f"rift_{pos[0]}_{pos[1]}", model=model)
        self.pos = pos
        # allow rift-specific spawn interval, but default to model-wide setting
        self.spawn_interval = spawn_interval if spawn_interval is not None else getattr(model, "rift_spawn_interval", 30)
        self._tick = 0
        self.min_interval = 5  # lower bound for acceleration

    def step(self):
        self._tick += 1
        if self._tick >= self.spawn_interval:
            self._tick = 0
            vs = Voidspawn(self.pos, self.model)
            self.model.grid.place_agent(vs, self.pos)
            self.model.schedule.add(vs)
            # optional acceleration: reduce spawn_interval gradually
            if getattr(self.model, "rift_accelerate", False):
                # reduce the interval by 1 each spawn down to min_interval
                if self.spawn_interval > self.min_interval:
                    self.spawn_interval = max(self.min_interval, self.spawn_interval - 1)
