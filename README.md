# Battleship_Project

Proposal:
Our team members are Russell Deady, John Ronzo, Andrew Franklin, Randy Toyberman, and Tyler Flaherty. The title of our project is Dynamic Fighting Ships. We hope to program a battleship-styled game where you can move your ships in-between every turn. We plan on utilizing the pygame library to do this. We plan to  have two people focus on the GUI, two people focusing on the mechanics of the game, and one person focusing on the networking.

Project Design:
There are several Battleship games written in Python with some using the Pygame library. We will extended the current state of the art for those that use Pygame by introducing a rule change that allows players to move their ships during the game. We will also implement a multiplayer feature with socket programming that allows for a multiplayer experience. There are also many python games that incorporate a multiplayer aspect as well as an AI component that allows users to play alone. Out goal is to combine these two philosophies into a multiplayer battleship game. 

Libraries: Pygame, Socket, Random, Pygame-ai

- Multiplayer: Randy
- GUI: Russell, Tyler
- Mechanics: John, Andrew

Status Report 1: For the backend mechanics, we have finalized our descision to use Pygame for most of the functionality and well as Pygame-ai for one player games. We also progammed the initial Pygame interface which the rest of the game will be built on. We have also begun to research as much as we can about the Pygame library to get the most functionality out of it.

As for the multiplayer functionality, we have setup a basic network and server which currently functions to establish a connection between clients running on the same network. In addition to this, research has been started on sending information between clients in order to send and recieve game moves and to update game data over the network.

We have also began the initial setup of the back-end part of the game that sets up each players gameboard with some other functions such as placing a ship in a given location, checking whether a ship exists in a given position. These features will be developed further on that will allow players to choose where they want to shoot and allow players to customize where they want their ships.
