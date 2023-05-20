# Final Project: Wave Collapse Function

> My project proposal suggested I was going to make a database, however, as I informed you, I chose this project instead.

### Description
What exactly is a wave collapse function?<br>
<br?
The best way to answer this is by using an example: a Sudoku board. Imagine an empty Sudoku board; it has 81 spaces, or tiles, and each tile has the option to store one of the numbers 1-9; this is called a tile's entropy or, in other words, the amount of options for a given tile in a grid. So, in the initial state, each tile has an entropy of 9 because each tile has 9 options of what can be stored there.<br>
<br>
Now Sudoku has rules of course, so if I assign a 1 to any given tile, then I can't go and assign a 1 to any tile in its row, column, or subsquare. You will find that all wave collapse functions rely on a set of rules to follow in order to determine which values can be adjacent to other values; in our case, we follow the rules of sudoku.<br>
<br>
A wave collapse function will always start as an empty board with every tile having all of the options (max entropy). The function will then repeatedly choose the tile with the least entropy (i.e the tile with the most value restrictions) and assign a value to it. After assigning a value to a tile, the entropy of adjacent tiles might be affected depending on the ruleset, so the next step would be to adjust the entropy of affected tiles accordingly.
<br>
This loop continues until either all tiles have been assigned a value or the tiles remaining have no entropy (cannot be any value), meaning that the wave collapse function failed to generate a valid tile arrangement. It is totally fine if this happens; randomization is unpredictable and, in some cases, generates a broken grid. If it does, simply regenerate a new board.<br>
<br>
Wave collapse functions don't only apply to Sudoku; dungeons and terrain in games benefit from this too! Have you ever played a game like Minecraft where the terrain is different every time you load a new game? Or perhaps you are a dungeon crawler where the dungeon changes every time you go to it with new arrangements or rooms and treasure. These can all be generated using the wave collapse function! The ruleset and tiles are the key.

### Project Structure
More info here.

### Design Patterns
More info here.

### Unittests
More info here.

### Setup Instructions
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
