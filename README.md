# 🧠 Void Breach

**Void Breach** is an **agent-based alien invasion simulation** built in **Python** using the [Mesa](https://mesa.readthedocs.io/) framework.  
It models intelligent predator–prey dynamics between human *Natives* and alien *Voidspawns* on a terrain-based grid world, featuring pathfinding, terrain costs, obstacles, fog of war, and dynamic rift spawning.

---

## 🚀 Features

### 🎯 Intelligent Agent Behavior
- **Voidspawn (Alien) agents** hunt Natives using **A\*** pathfinding.
- **Native agents** dynamically **flee** from Voidspawn using A\* in reverse (minimizing threat distance).
- Planned expansion for **Q-Learning** to evolve adaptive fleeing behavior for Native leaders.

### 🌍 Dynamic Environment
- **Terrain tiles** with **variable movement costs**, influencing pathfinding difficulty.
- **Obstacles** block movement and create realistic choke points.
- **Rift portals** periodically spawn new Voidspawn, simulating an expanding invasion.
- Optional **fog of war** system where Natives and Voidspawn have limited vision ranges.

yaml
Copy code

---

## 🧠 Simulation Logic Overview

| Component | Role |
|------------|------|
| **`Voidspawn`** | Predator agents using A\* to hunt visible Natives intelligently. |
| **`Native`** | Prey agents using A\* to flee from nearby Voidspawn; future versions learn adaptively via Q-Learning. |
| **`Rift`** | Periodically spawns new Voidspawn agents, increasing invasion difficulty. |
| **`Obstacle`** | Blocks movement for both species. |
| **`TerrainTile`** | Adds movement cost variations (e.g., plains, hills, lava, water). |
| **`Fog of War`** | Hides unexplored or unseen tiles for each faction. |

---

## 🧰 Tech Stack

- **Python 3.10+**
- **Mesa** – agent-based modeling framework
- **NumPy** – grid and cost computations
- **Matplotlib / Mesa Charts** – real-time analytics
- **Optional Future** – Q-Learning via `numpy` or `torch`

---

## 🕹️ How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<yourusername>/VoidBreach.git
   cd VoidBreach
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Start the simulation:

bash
Copy code
python -m visualization.server
Open the simulation in your browser (usually auto-opens at):

cpp
Copy code
http://127.0.0.1:8521
Click ▶ Start to begin, ⏸ Stop to pause, and observe:

Blue dots (Natives) moving to avoid Red dots (Voidspawn)

Obstacles and terrain tiles affecting movement

Rift portals spawning new invaders over time

Live statistics (population, survival rate, rift activity)

📊 Example Features 
Feature	Status
A* pathfinding	
Terrain costs	
Obstacle support	
Fog of War	
Rift spawning	

Project Highlights

This project demonstrates:

Pathfinding algorithms like A* in a living simulation.

Emergent multi-agent behavior under dynamic rules.

Data-driven AI modeling with potential for reinforcement learning.

Modular and extensible Python codebase, suitable for research, coursework, or game prototyping.
