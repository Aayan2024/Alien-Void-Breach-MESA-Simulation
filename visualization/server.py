"""
server.py - Mesa visualization server for Void Breach with fog-of-war portrayal.
Run:
    python -m visualization.server
Then open http://127.0.0.1:8521/
"""
# --- Import handling for different Mesa versions ---
try:
    from mesa.visualization import ModularServer
except ImportError:
    from mesa.visualization.ModularVisualization import ModularServer

from mesa.visualization.modules import CanvasGrid, ChartModule
from model import VoidBreachModel
from visualization.charts import population_chart

def agent_portrayal(agent):
    """Defines how each agent type is drawn on the grid, with fog-of-war support."""
    if agent is None:
        return

    cls = agent.__class__.__name__
    x, y = agent.pos
    model = agent.model

    # helper booleans
    visible = (x, y) in getattr(model, "visible_cells", set())
    explored = (x, y) in getattr(model, "explored_cells", set())

    # TERRAIN: draw a rectangle but change appearance based on fog/explored
    if cls == "TerrainTile":
        cost = getattr(agent, "movement_cost", 1.0)
        # base color for visible tiles
        if visible:
            gray = int(220 - min(cost * 40, 160))
            color = f"rgb({gray},{gray},{gray})"
        elif explored:
            # dimmed version for explored but not currently visible
            gray = int(120 - min(cost * 20, 80))
            color = f"rgb({gray},{gray},{gray})"
        else:
            # completely unseen -> black/dark
            color = "rgb(0,0,0)"

        return {
            "Shape": "rect",
            "Color": color,
            "Layer": 0,
            "w": 1,
            "h": 1,
            "Filled": "true",
        }

    # OBSTACLE: show only if explored or visible (obstacle silhouette)
    if cls == "Obstacle":
        if not explored and not visible:
            return None
        return {
            "Shape": "rect",
            "Color": "#2E2E2E" if visible else "#111111",
            "Layer": 1,
            "w": 1,
            "h": 1,
            "Filled": "true",
        }

    # RIFT / VOIDSPAWN / NATIVE: only render when visible
    if cls == "Rift":
        if not visible:
            return None
        return {
            "Shape": "circle",
            "r": 0.7,
            "Color": "#9C27B0",
            "Layer": 3,
            "Filled": "true",
        }

    if cls == "Voidspawn":
        if not visible:
            return None
        return {
            "Shape": "circle",
            "r": 0.5,
            "Color": "#E53935",
            "Layer": 4,
            "Filled": "true",
        }

    if cls == "Native":
        if not visible:
            return None
        return {
            "Shape": "circle",
            "r": 0.4,
            "Color": "#4CAF50",
            "Layer": 5,
            "Filled": "true",
        }

    return None


# Grid setup
GRID_WIDTH = 30
GRID_HEIGHT = 30
canvas_element = CanvasGrid(agent_portrayal, GRID_WIDTH, GRID_HEIGHT, 600, 600)

# Chart setup (from visualization/charts.py)
chart_element = population_chart()

# Combine modules into a ModularServer
server = ModularServer(
    VoidBreachModel,
    [canvas_element, chart_element],
    "VOID BREACH: Alien Invasion Simulation",
    {
        "width": GRID_WIDTH,
        "height": GRID_HEIGHT,
        "initial_natives": 25,
        "initial_voidspawns": 6,
        "obstacle_fraction": 0.05,
        # vision and rift params can be tweaked here
        "native_vision": 5,
        "void_vision": 6,
        "rift_spawn_interval": 30,
        "rift_accelerate": True,
    },
)

server.port = 8521  # default Mesa port

if __name__ == "__main__":
    print("Starting visualization server... Open http://127.0.0.1:8521/")
    server.launch()
