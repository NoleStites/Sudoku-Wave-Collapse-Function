# Final Project: Wave Collapse Function

> My project proposal suggested that I was going to make a database; however, as I informed you, I chose this project instead.

## Description
What exactly is a wave collapse function?<br>
<br>
The best way to answer this is by using an example: a Sudoku board. Imagine an empty Sudoku board; it has 81 spaces, or tiles, and each tile has the option to store one of the numbers 1-9; this is called a tile's entropy or, in other words, the amount of options for a given tile in a grid. So, in the initial state, each tile has an entropy of 9 because each tile has 9 options of what can be stored there.<br>
<br>
Now Sudoku has rules of course, so if I assign a 1 to any given tile, then I can't go and assign a 1 to any tile in its row, column, or subsquare. You will find that all wave collapse functions rely on a set of rules to follow in order to determine which values can be adjacent to other values; in our case, we follow the rules of sudoku.<br>
<br>
A wave collapse function will always start as an empty board with every tile having all of the options (max entropy). The function will then repeatedly choose the tile with the least entropy (i.e the tile with the most value restrictions) and assign a value to it. After assigning a value to a tile, the entropy of adjacent tiles might be affected depending on the ruleset, so the next step would be to adjust the entropy of affected tiles accordingly.<br>
<br>
This loop continues until either all tiles have been assigned a value or the tiles remaining have no entropy (cannot be any value), meaning that the wave collapse function failed to generate a valid tile arrangement. It is totally fine if this happens; randomization is unpredictable and, in some cases, generates a broken grid. If it does, simply regenerate a new board.<br>
<br>
Wave collapse functions don't only apply to Sudoku; dungeons and terrain in games benefit from this too! Have you ever played a game like Minecraft where the terrain is different every time you load a new game? Or perhaps you are a dungeon crawler where the dungeon changes every time you go to it with new arrangements or rooms and treasure. These can all be generated using the wave collapse function! The ruleset and tiles are the key.

## Project Structure
My Sudoku generation algorithm is displayed and written to fit into an MVC application. I have separate packages for the Model, View, and Controller such that the View, when needing to make calculation, will send a request to the Controller, which then forwards the request to the Model to return the calculation result. Because of this layout, the View is only responsible for, well, the view; it onyl needs to concern itself with the GUI. The Controller is the middle-man and acts as the messenger between View and Model. The Model is solely responsible for making complication calculations and giving the results to the View when requested.<br>
<br>
Considering that a big part of a wave collapse function are the tiles in the grid I chose to make them their own package. This package contains the Tile object and a directory filled with all of the images display on the Sudoku board (the red numbers).<br>
<br>
As mentioned in the Description section, it is sometimes the case that the board needs to be generated multiple times before a valid one is returned; this is data that interested me quite a bit. I thought it might be handy to know just how many generation attempts were required, so I made a logger to log that for me. The logger has its own package for organization and reusability between projects.

## Design Patterns
Single Responsibility
: Stuff

Singleton
: Stuff

Facade
: Stuff

Flyweight
: Stuff

MVC
: Stuff

## Unittests
More info here.

## Setup Instructions
1. Clone the repository   
`$ git clone https://github.com/SOUComputerScience/final_project-NoleStites.git`
2. Change directories into the repo    
`$ cd final_project-NoleStites` 
3. Create a Python virtual environment    
`$ python -m venv env`   
`$ source env/bin/activate`     
4. Install the required packages     
`$ pip install -r requirements.txt` 
5. Run the app!    
`$ python3 app.py`   
6. Run the unittests    
`$ python -m unittest tests/test_Unit.py`   
