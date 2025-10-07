"""
model.py - Mesa model for Void Breach with fog-of-war (visibility) support.
"""
import random
import os
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from agents.terrain_tile import TerrainTile
from agents.obstacle import Obstacle
from agents.native import Native
from agents.voidspawn import Voidspawn
from agents.rift import Rift

# ensure data directory
os.makedirs("data/logs", exist_ok=True)

def count_agents(model, agent_type):
    return sum(1 for a in model.schedule.agents if isinstance(a, agent_type))

def count_natives(model): return count_agents(model, Native)
def count_voidspawns(model): return count_agents(model, Voidspawn)

class VoidBreachModel(Model):
    def __init__(self, width=30, height=30, initial_natives=20, initial_voidspawns=5,
                 obstacle_fraction=0.05, seed=None,
                 native_vision=5, void_vision=6,
                 rift_spawn_interval=30, rift_accelerate=True):
        super().__init__()
        if seed is not None:
            random.seed(seed)
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.running = True
        self.width = width
        self.height = height

        # Vision settings (used by agents and visibility)
        self.native_vision = native_vision
        self.void_vision = void_vision

        # Rift/spawn settings
        self.rift_spawn_interval = rift_spawn_interval
        self.rift_accelerate = rift_accelerate

        # sets for fog-of-war
        self.visible_cells = set()    # cells visible this tick
        self.explored_cells = set()   # cells seen at least once

        # create terrain - uniform default with occasional high-cost tiles
        self._create_terrain(default_cost=1.0, high_cost_prob=0.08, high_cost=3.0)

        # obstacles
        num_cells = width * height
        num_obstacles = int(num_cells * obstacle_fraction)
        self._scatter_obstacles(num_obstacles)

        # rifts (a few)
        for _ in range(max(1, int(initial_voidspawns/2))):
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            rift = Rift((x, y), self, spawn_interval=self.rift_spawn_interval)
            self.grid.place_agent(rift, (x, y))
            self.schedule.add(rift)

        # place Voidspawns
        for _ in range(initial_voidspawns):
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            vs = Voidspawn((x, y), self)
            self.grid.place_agent(vs, (x, y))
            self.schedule.add(vs)

        # place Natives
        for _ in range(initial_natives):
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            nat = Native((x, y), self)
            self.grid.place_agent(nat, (x, y))
            self.schedule.add(nat)

        # Data collector
        self.data_collector = DataCollector(
            model_reporters={"Natives": count_natives, "Voidspawns": count_voidspawns}
        )

        # initial visibility computation
        self.compute_visibility()
        # initial collect
        self.data_collector.collect(self)

    def _create_terrain(self, default_cost=1.0, high_cost_prob=0.08, high_cost=3.0):
        """Place TerrainTile objects on every cell with movement_cost attribute."""
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                cost = default_cost
                if self.random.random() < high_cost_prob:
                    cost = high_cost
                terrain = TerrainTile((x, y), self, movement_cost=cost)
                self.grid.place_agent(terrain, (x, y))
                # Not scheduling terrain (they are static), but they exist on grid cell.

    def _scatter_obstacles(self, num_obstacles):
        placed = 0
        attempts = 0
        while placed < num_obstacles and attempts < num_obstacles * 10:
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            # check if only terrain exists at that cell (no obstacle already)
            cell = self.grid.get_cell_list_contents((x, y))
            if not any(isinstance(a, Obstacle) for a in cell):
                obs = Obstacle((x, y), self)
                self.grid.place_agent(obs, (x, y))
                # obstacles can be scheduled if you want them dynamic; here they are static
                placed += 1
            attempts += 1

    def compute_visibility(self):
        """Compute visible cells (radius-based) and update explored_cells."""
        visible = set()
        # consider Natives and Voidspawns as vision sources
        for a in self.schedule.agents:
            cls = a.__class__.__name__
            if cls == "Native":
                vr = getattr(a, "vision_range", self.native_vision)
            elif cls == "Voidspawn":
                vr = getattr(a, "vision_range", self.void_vision)
            else:
                continue
            (ax, ay) = a.pos
            # square / Chebyshev neighborhood for vision
            x0 = max(0, ax - vr)
            x1 = min(self.width - 1, ax + vr)
            y0 = max(0, ay - vr)
            y1 = min(self.height - 1, ay + vr)
            for x in range(x0, x1 + 1):
                for y in range(y0, y1 + 1):
                    visible.add((x, y))
        self.visible_cells = visible
        # update explored set
        self.explored_cells.update(visible)

    def step(self):
        self.schedule.step()
        # after agents moved / acted, recompute visibility for next draw
        self.compute_visibility()
        self.data_collector.collect(self)
        # stop condition: no natives or no voidspawns
        if count_natives(self) == 0 or count_voidspawns(self) == 0:
            self.running = False

    def get_results_df(self):
        return self.data_collector.get_model_vars_dataframe().reset_index().rename(columns={"index": "Step"})
