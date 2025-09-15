# PyConnect-4

**PyConnect-4** is, as the name suggests, a Python implementation of the classic Connect-4 game.  
It comes with **two game modes**:  

- **CLI**: Play directly in the terminal.  
- **GUI**: Play using a PyGame graphical interface.  

---

## Features

Both game modes include:  

- Player vs Player (on the same device)  
- ~~Player vs Player (LAN)~~ *(currently under maintenance)*  
- Player vs CPU (uses a strong minimax algorithm)  
- Settings system (adjust display mode and CPU strength)  

---

## To-Do List

### Player vs Player (LAN)

- Take it out of maintenance.  
- Remember the last IP you played against:  
  - Optionally store IP by hostname.  
  - Keep a file with all previously played hostname–IP pairs to allow connecting using the computers hostname like `t495` instead of `192.168.1.xxx`.  
- Prevent more than 2 people from joining a single game (or consider adding a spectator mode).  
- Make sure the game ends properly when players leave, instead of freezing or crashing.  

### Player vs CPU

- better eval heuristics
- order allowedMoves to try more promising moves first
- cache / transposition table (avoid rechecking already evaled positions)
- if a move results in a win, immediately return without recursion
- MAYBE refactor to a bitboard approach (MUCH MUCH faster cuz bitwise operations)
- parallel operations

### GUI

- Add the CPU
- animations


(Cement-4, PyConnect-4 + Dementris where you forget the tiles lmao)
