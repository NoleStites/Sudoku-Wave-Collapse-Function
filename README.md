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

### MVC
I don't even know if this is considered a design pattern, but it at least deserves an honourable mention. I used MVC as way to organization the major parts
are my program. I know how complicated a GUI can be to implement, so separating the code into a View for the things to display, a Model as a place to make he more complicated calculation, and a Controller to allow communication between the two was a great way to go. Doing this also allows for isolation between different key components of the program, making debugging a lot easier.

### Single Responsibility
Despite organizing my program using MVC, I still ran into issues with cluttered code. The View, specifically, can be quite complicated with all of the frames and buttons that might need to be implemented; code start to get long after a short while. After I noticed this, I decided to cut my View initializer into more organized piece through the use of additional methods in the View class. Originally, my View's initializer was doing a few rather large things, so I took these tasks and put them in their own methods. Not only did this enforce bettwe isolation but it also made my code significantly more readable.

### Singleton
I implemented a logger responsible for recording data about the number of generation attempts spent on making a board. As I have learned with loggers in general, it is a good idea to make your logger object a Singleton as to avoid two loggers writing to a single file at the same time. I especially wanted to make my logger with a Singleton design because it was important to me that my data not be corrupted.

### Facade
Facades are quite useful in that they take something complicated and abstract it away, providing you with a user-friendly interface to interact with the complexity of what lies beneath. My code is large, complicated, and perhaps a bit confusing to look at. Someone looking at it might think "where do I even start?" Well this is no more! By using a friendly GUI interface, the user can simply interact with any one of five buttons I have on display. Each button does a ton of stuff behind the scenes, but that is all abstracted away into a few buttons. My GUI is a facade between the user and my complex code.

### Flyweight
This is perhaps the most exciting design pattern I used. Perhaps let's start with a preface: each Sudoku board has 81 squares; this might be considered a lot, or maybe not, but my program was crafted in such a manner as to allow for expansion of the board. I tested on a board size of 16,900 squares and having that many squares is definitely possible. Beyond the number of squares, consider that each square would have to contain an entire Python object, each object having an image stored in it; that's a lot of images! I have images for the numbers 1-9 so that they can be displayed on the board, but what I have done is implement the Flyweight pattern such that I have a list with nine objects representing the nine images I have. Now each square, rather than having their own object and image, share a single object in my Flyweight list. This way there would only be 9 objects in the board, not 16,900.

## Unittests
So, about the unittests: it was hard to find methods to test. Every one of the methods in my program is either too attached to the tkinter library to test or involves generating and returning random things, which is practically impossible to test. I managed to find a couple things to test, however, so I hope that can be enough. I completely understand if it isn't, of course.<br>
<br>
The first method I tested is my Model's method for finding and returning a list of tiles that are both uncollapsed (i.e haven't been assigned a value) and have the lowest entropy. This is a major part of my program as this method is called every time through my while loop until every tile has a value.<br>
<br>
The second, and final, thing that I tested was my logger implementation. I wanted to verify that my logger's Singleton design acted properly and did not allow more than one instance of a Logger object at a time. Unlike my Singleton logger test in the Singleton lab, I have implemented a thread-safe version.

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

GUI Buttons:
- **Generate**: generates a filled Sudoku board instantly
- **Animate**: generates a filled Sudoku board by animating how the wave collapse function works
- **Gamify**: turns a filled Sudoku board into a playable Sudoku by removing 51 squares
- **Reset**: clears the Sudoku board
- **Stop**: terminates the program
