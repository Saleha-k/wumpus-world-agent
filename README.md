# 🐍 Wumpus World - Knowledge-Based Agent

An intelligent agent that navigates the **Wumpus World environment** using **propositional logic** and **resolution-based inference** to make safe decisions.

---

## 📋 Overview

The **Wumpus World** is a classic AI problem where an agent must navigate a cave filled with pits and a deadly Wumpus creature.

This project implements a **knowledge-based agent** that:
- Uses logical inference to deduce safe paths  
- Avoids hazards intelligently  
- Never relies on luck — every move is logically justified  

---

## ✨ Features

- 🧠 **Knowledge-Based Agent**  
  Uses propositional logic to represent and reason about the world  

- 🔍 **Resolution Inference**  
  Implements resolution refutation for logical entailment  

- 🖥️ **Real-time Visualization**  
  Interactive grid showing:
  - Agent position  
  - Visited cells  
  - Percepts  

- 🎮 **Multiple Control Modes**  
  - Manual (step-by-step)  
  - Autonomous exploration  

- 📊 **Performance Metrics**  
  Tracks:
  - Inference steps  
  - Resolution calls  
  - Visited cells  
  - Score  

- 🌬️ **Percept Tracking**  
  Displays:
  - Breeze (near pits)  
  - Stench (near Wumpus)  

- ⚙️ **Configurable Environment**  
  Adjustable:
  - Grid size  
  - Number of pits  

---

## 🎮 How It Works

### 🧩 Agent Logic

1. **Perception**  
   The agent detects:
   - `BREEZE` → Adjacent pit  
   - `STENCH` → Adjacent Wumpus  

2. **Knowledge Update**  
   Percepts are stored in the **Knowledge Base (KB)** as logical clauses  

3. **Inference**  
   A **resolution algorithm** is used to infer safe cells  

4. **Decision Making**  
   - Move to a **proven safe cell**  
   - If none exists → explore the **closest frontier**  

---

## 📐 Logical Rules

```
B(i,j) → ∃ adjacent P(i,j)        (Breeze ⇒ adjacent pit)
S(i,j) → ∃ adjacent W(i,j)        (Stench ⇒ adjacent Wumpus)

¬B(i,j) → ∀ adjacent ¬P(i,j)      (No breeze ⇒ no adjacent pits)
¬S(i,j) → ∀ adjacent ¬W(i,j)      (No stench ⇒ no adjacent Wumpus)

Safe(i,j) → ¬P(i,j) ∧ ¬W(i,j)     (Safe ⇒ no pit and no Wumpus)
```

---

## 🚀 Installation

### 📌 Prerequisites

- Python 3.8 or higher  
- Flask  

---

### ⚙️ Setup Instructions

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/wumpus-world-kb-agent.git
cd wumpus-world-kb-agent
```

#### 2. Install Dependencies

```bash
pip install flask
```

#### 3. Run the Application

```bash
python app.py
```

#### 4. Open in Browser

```
http://localhost:5000
```

---

## 📁 Project Structure

```
wumpus-world-kb-agent/
│
├── app.py              # Flask backend (KB + agent logic)
├── templates/
│   └── index.html     # Main UI
├── static/
│   ├── style.css      # Styling (simple, solid colors)
│   └── script.js      # Frontend logic
└── README.md          # Documentation
```

---

## 🧠 Strategy Note

If no safe cell can be logically proven, the agent:
> Falls back to exploring the closest frontier cell.

---
