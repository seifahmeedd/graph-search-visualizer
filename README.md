# Graph Searching System (Python) 🔎🧠

A full **Graph Searching system** built in **Python** with a **GUI** and **graph visualization**.
It supports both **Uninformed** and **Informed** search algorithms and highlights the final path on the graph.

---

## ✨ Features
- Choose a search algorithm from the GUI:
  - **Uninformed Search:** BFS, DFS, IDS, UCS
  - **Informed Search:** Greedy Best-First, A* (requires heuristic values)
- Input:
  - Graph nodes
  - Weighted edges
  - (Optional) heuristic values for informed search
- Output:
  - Found path (sequence of nodes)
  - Total path cost
  - Not-found message if no path exists
- Visualization:
  - Draws the graph
  - Highlights the path taken by the selected algorithm

---

## 🧰 Algorithms Included
### Uninformed Search
- Breadth-First Search (**BFS**)
- Depth-First Search (**DFS**)
- Iterative Deepening Search (**IDS**)
- Uniform Cost Search (**UCS**)

### Informed Search
- Greedy Best-First Search (**Greedy**)
- A* Search (**A\***)

---

## 🖥️ How to Run
### 1) Install dependencies
```bash
pip install -r requirements.txt
