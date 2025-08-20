# PyConnect-4

**As the name suggests, this is Connect-4, made in Python. There are two versions, CLI, where you play the game in a terminal, and GUI where you play in a PyGame GUI.**

### Both gamemodes feature:

Player vs Player (on the same device)
~~Player vs Player (LAN)~~
Player vs CPU (a minimax algorithm that is VERY strong)

A settings system, which allows the user to switch between tile display modes, as well as change the strength of the CPU.

## To-do list:

### Player vs Player (LAN):
    (take it out of maintenance)
    remember the last ip you played against. remember ip by hostname of pc?
        like remember all the ips youve played against and store the hostname - ip combo in a file so you can play against "t495" instead of 192.168.1.xxx
    stop more than 2 people joining one game (or implement a spectator system ig)
    make it so when people leave, the game actually ends instead of just sitting there / crashing.

### Player vs CPU:
    fix priorities, as sometimes it prefers a vertical 3 in a row instead of a horizontal win.