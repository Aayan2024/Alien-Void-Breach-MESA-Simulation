from mesa import Agent
from algorithms.astar import astar_search
import random
import math

class Native(Agent):
    """
    Prey: flees from nearest Voidspawn using A*.
    Has vision_range set from the model defaults.
    """
    def __init__(self, pos, model, leader=False):
        super().__init__(unique_id=f"native_{pos[0]}_{pos[1]}", model=model)
        self.pos = pos
        self.leader = leader
        # future: q-table etc
        self.q_table = {}
        # vision range from model preference
        self.vision_range = getattr(model, "native_vision", 5)

    def step(self):
        # find nearest voidspawn
        voids = [a for a in self.model.schedule.agents if a.__class__.__name__ == "Voidspawn"]
        if not voids:
            # wander randomly if no predator
            self._random_move()
            return

        # nearest voidspawn
        def manhattan(a_pos, b_pos):
            return abs(a_pos[0]-b_pos[0]) + abs(a_pos[1]-b_pos[1])

        nearest_void = min(voids, key=lambda v: manhattan(self.pos, v.pos))

        # generate candidate goals: corners + random samples
        candidates = [
            (0, 0),
            (0, self.model.height-1),
            (self.model.width-1, 0),
            (self.model.width-1, self.model.height-1)
        ]
        # add random samples
        for _ in range(12):
            candidates.append((self.random.randrange(self.model.width), self.random.randrange(self.model.height)))

        # evaluate candidates: must be reachable (A* returns path)
        best = None
        best_score = -math.inf
        for cand in candidates:
            # skip if out of bounds
            if cand[0] < 0 or cand[0] >= self.model.width or cand[1] < 0 or cand[1] >= self.model.height:
                continue
            path = astar_search(self.model, start=self.pos, goal=cand)
            if not path:
                continue
            # score = distance from predator at goal minus path length penalty
            dist = manhattan(cand, nearest_void.pos)
            score = dist - 0.5 * len(path)  # encourage reachable but far positions
            if score > best_score:
                best_score = score
                best = (cand, path)

        if best is None:
            # cannot find path to any candidate -> random move
            self._random_move()
            return

        target, path = best
        # move one step along path (if path len >= 2)
        if len(path) >= 2:
            next_pos = path[1]
            self.model.grid.move_agent(self, next_pos)
            self.pos = next_pos
        else:
            # already at the target
            pass

    def _random_move(self):
        # include Moore neighborhood for more natural movement
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        if neighbors:
            self.model.grid.move_agent(self, random.choice(neighbors))
