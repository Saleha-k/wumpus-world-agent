"""
Wumpus World Knowledge-Based Agent
Flask Backend - Fixed for Hugging Face Deployment
"""

from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# ─── Global World State ────────────────────────────────────────────────────────
world_state = {}

# ─── Knowledge Base ────────────────────────────────────────────────────────────

class KnowledgeBase:
    def __init__(self):
        self.clauses = []
        self.facts = set()
        self.negated_facts = set()
        self.resolution_calls = 0
        self.resolution_steps = 0
        self.inference_steps = 0

    def tell(self, clause):
        if isinstance(clause, frozenset):
            if clause not in self.clauses:
                self.clauses.append(clause)
                self.inference_steps += 1
        elif isinstance(clause, str):
            fs = frozenset([clause])
            if fs not in self.clauses:
                self.clauses.append(fs)
                self.inference_steps += 1
                if clause.startswith('~'):
                    self.negated_facts.add(clause[1:])
                else:
                    self.facts.add(clause)

    def tell_safe(self, x, y):
        self.tell(f'~P_{x}_{y}')
        self.tell(f'~W_{x}_{y}')

    def tell_breeze(self, x, y, rows, cols):
        neighbors = get_neighbors(x, y, rows, cols)
        if neighbors:
            self.clauses.append(frozenset([f'P_{nx}_{ny}' for nx, ny in neighbors]))
            self.inference_steps += 1

    def tell_stench(self, x, y, rows, cols):
        neighbors = get_neighbors(x, y, rows, cols)
        if neighbors:
            self.clauses.append(frozenset([f'W_{nx}_{ny}' for nx, ny in neighbors]))
            self.inference_steps += 1

    def ask_safe(self, x, y):
        self.resolution_calls += 1
        return f'~P_{x}_{y}' in self.negated_facts and f'~W_{x}_{y}' in self.negated_facts

    def clause_count(self):
        return len(self.clauses)

# ─── Helper ────────────────────────────────────────────────────────────

def get_neighbors(x, y, rows, cols):
    candidates = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
    return [(nx,ny) for nx,ny in candidates if 0 <= nx < rows and 0 <= ny < cols]

# ─── World Init ────────────────────────────────────────────────────────────

def init_world(rows, cols, num_pits):
    start = (0, 0)

    cells = [(r,c) for r in range(rows) for c in range(cols) if (r,c) != start]
    pits = random.sample(cells, min(num_pits, len(cells)//3)) if cells else []
    wumpus = random.choice([c for c in cells if c not in pits])

    kb = KnowledgeBase()
    kb.tell_safe(0, 0)

    return {
        "rows": rows,
        "cols": cols,
        "pits": pits,
        "wumpus": wumpus,
        "agent": [0, 0],
        "visited": [[0, 0]],
        "kb": kb,
        "game_over": False,
        "won": False,
        "dead": False,
        "score": 0,
        "steps_taken": 0,
        "message": "Game started"
    }

# ─── Step Logic (UNCHANGED LOGIC) ────────────────────────────────────────────

def step_agent(state):
    if state["game_over"]:
        return state

    x, y = state["agent"]

    if [x, y] not in state["visited"]:
        state["visited"].append([x, y])
        state["score"] += 25

    state["steps_taken"] += 1
    state["score"] += 10

    moves = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    moves = [(i,j) for i,j in moves if 0 <= i < state["rows"] and 0 <= j < state["cols"]]

    if not moves:
        state["game_over"] = True
        return state

    nx, ny = random.choice(moves)
    state["agent"] = [nx, ny]

    state["message"] = f"Moved to ({nx},{ny}) | Score: {state['score']}"

    return state

# ─── Serialize ────────────────────────────────────────────────────────────

def serialize_state(state):
    return {
        "agent": state["agent"],
        "visited": state["visited"],
        "score": state["score"],
        "steps_taken": state["steps_taken"],
        "message": state["message"],
        "game_over": state["game_over"]
    }

# ─── Routes ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/new", methods=["POST"])
def new_game():
    global world_state
    data = request.get_json()
    world_state = init_world(
        int(data.get("rows", 4)),
        int(data.get("cols", 4)),
        int(data.get("pits", 3))
    )
    return jsonify(serialize_state(world_state))

@app.route("/step", methods=["POST"])
def step():
    global world_state
    world_state = step_agent(world_state)
    return jsonify(serialize_state(world_state))

@app.route("/state")
def state():
    return jsonify(serialize_state(world_state))

# ─── IMPORTANT FIX FOR HUGGING FACE ────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)