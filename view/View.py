from tkinter import *
from PIL import Image, ImageTk  # For resizing images
from controller.Controller import Controller
from tile.Tile import Tile
from math import isqrt
import os
from logger.logger import Logger
import datetime


class View():
    
    def __init__(self, controller: Controller):
        """
        Creates a view to be interacted with by the user and
        to display the Sudoku generation results.
        """
        self.controller = controller
        self.logger = Logger("./log.txt")

        # Initializing the root window
        self.root = Tk()
        self.root.title("Wave Collapse Function: Sudoku")
        self.root.configure(background="#404040")
        
        # BORROWED CODE (start)
        # Used to center the window so that it doesn't spawn in a random location every time.
        w = 900
        h = 948

        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()

        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y-50))
        # BORROWED CODE (end)

        
        # Generate a grid of tiles with the width of the grid being tiles_for_width tiles
        self.tiles_for_width = 9
        board_size = 900
        tile_size = board_size // self.tiles_for_width


        # Make a frame for the buttons
        self.button_frame = Frame(self.root, width=200, height=2, bg="blue")
        self.button_frame.pack()


        # Make the Generate, Reset, Gamify, and STOP buttons
        bg_color = "#262626"
        fg_color = "white"
        act_back = "#595959"
        act_fore = "white"

        button_generate = Button(self.button_frame, width=10, height=2, text="Generate", bg=bg_color, fg=fg_color, activebackground=act_back, activeforeground=act_fore, command=self.generateSudoku)
        button_generate.pack(side=LEFT)

        button_reset = Button(self.button_frame, width=10, height=2, text="Reset", bg=bg_color, fg=fg_color, activebackground=act_back, activeforeground=act_fore, command=self.generateEmptyBoard)
        button_reset.pack(side=LEFT)

        button_gamify = Button(self.button_frame, width=10, height=2, text="Gamify", bg=bg_color, fg=fg_color, activebackground=act_back, activeforeground=act_fore, command=self.gamify)
        button_gamify.pack(side=LEFT)

        button_stop = Button(self.button_frame, width=10, height=2, text="Stop", bg=bg_color, fg=fg_color, activebackground=act_back, activeforeground=act_fore, command=self.root.destroy)
        button_stop.pack(side=LEFT)


        # Make the frame for the Sudoku board
        self.sudokuBoard = Frame(self.root, width=board_size, height=board_size, bg="#8c8c8c")
        self.sudokuBoard.pack()
        self.tile_grid = self.populateGrid(tile_size) # Initialize grid with empty Tiles


        # Get a list of resized possible tile images (BLANK and 1-9)
        self.image_list = self.resizeImages(tile_size)

        # Initialize the Sudoku board as empty
        self.generateEmptyBoard()

        # Counter to keep track of how many generation attempts occured before success (for logging purposes)
        self.gen_attempts = 1

        # Initialize log file for this program run
        date = datetime.datetime.now()
        self.logger.log(f'\n\n{date.strftime("%c")}\n')
        self.logger.log("----------------------\n")

        # Start the program GUI
        self.root.mainloop()


    def gamify(self):
        """
        Will request the controller to choose a random set of
        51 tiles to make empty to allow the Sudoku puzzle to be playable.

        I can modify this in the future to allow for the number of
        removed Tiles to be chosen.
        """
        # Get list of Tile coordinates to clear
        clear_list = self.controller.getGamifyTiles(51, self.tile_grid)

        # Clear the tiles in the clear_list
        for x, y in clear_list:
            self.tile_grid[x][y].label['image'] = self.image_list[0]


    def generateEmptyBoard(self):
        """
        Initializes the sudoku board with empty images.
        """
        for x in range(self.tiles_for_width):
            for y in range(self.tiles_for_width):
                # Set the image of the current Tile to the blank image in our image_list
                self.tile_grid[x][y].label['image'] = self.image_list[0]
                self.tile_grid[x][y].entropy = [ num+1 for num in range(self.tiles_for_width)]
                self.tile_grid[x][y].collapsed = False


    def generateSudoku(self):
        """
        Will continue to get called until a Sudoku board is
        successfully generated (high probability).
        """

        # Start by clearing the board
        self.generateEmptyBoard()

        tiles_remaining = self.tiles_for_width * self.tiles_for_width

        # Continue this loop until every tile has collapsed
        while tiles_remaining > 0:
            # Get tuple containing random Tile object to populate and value to populate with
            tile_v = self.controller.randomTileAndValue(self.tile_grid)
            if tile_v == None:
                break   # No more uncollapsed Tiles, so the board is filled and the loop can end

            # Mark equivalent Tile in grid as collapsed and assign value to it
            x = tile_v[0].coord[0]
            y = tile_v[0].coord[1]

            self.tile_grid[x][y].collapsed = True
            self.tile_grid[x][y].label['image'] = self.image_list[tile_v[1]]

            # Propagate the entropy of affected Tiles
            self.propagateEntropy(self.tile_grid[x][y], tile_v[1])
            tiles_remaining -= 1

        # Verify that Sudoku board is completely filled in
        isFilled = self.verifyFilledBoard()
        if isFilled == 1: # Not filled
            self.gen_attempts += 1
            self.generateSudoku()
        

        # Log generation attempts to the log file and reset counter for next generation
        self.logger.log(f'Generation Attempts: {self.gen_attempts}\n')
        self.gen_attempts = 1

        self.root.mainloop() # Starts/runs the GUI (everything involving the GUI should come before this)


    def verifyFilledBoard(self):
        """
        Checks to see if the Sudoku board is completely filled in.
        If filled, return 0, otherwise return 1.
        """
        size = len(self.tile_grid)

        for column in range(size):
            for row in range(size):
                if self.tile_grid[column][row].collapsed == False:
                    return 1
        return 0

    
    def propagateEntropy(self, tile: Tile, value: int):
        """
        Will change the entropy of Tiles surrounding the given Tile based on
        the given value.
        """
        # Iterate through every Tile in the grid
        for column in range(self.tiles_for_width):
            for row in range(self.tiles_for_width):
                curr_tile = self.tile_grid[column][row]
                if (curr_tile.coord[0] == tile.coord[0]) or (curr_tile.coord[1] == tile.coord[1]) or (curr_tile.subsquare == tile.subsquare):
                    if curr_tile.entropy.count(value) != 0:
                        curr_tile.entropy.remove(value)
   

    def resizeImages(self, tile_size: int):
        """
        Create Image objects for each of the 10 images (BLANK, and 1-9),
        resize based on size of tile, and store in and return a list to be reused.
        """
        image_list = []

        # Special case: blank image
        image = Image.open(f"./tile/tile_images/tileBLANK.png")         # Open the image for editting
        image = image.resize((tile_size, tile_size), Image.ANTIALIAS)   # Resize the image based on the tile size
        image = ImageTk.PhotoImage(image)                               # Convert the image to a PhotoImage (tkinter compatable)
        image_list.append(image)

        # Images 1-9
        for num in range(9):
            image = Image.open(f"./tile/tile_images/tile{num+1}.png")
            image = image.resize((tile_size, tile_size), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(image)
            image_list.append(image)

        return image_list
   

    def populateGrid(self, tile_size: int):
        """
        Creates all of the Tile objects to put in the grid and initializes
        them with no image and max entropy. Returns the tile grid list.
        """
        tile_grid = []  # A two-dimensional list to contain the grid of tiles
        x_pos = 0
        for column in range(self.tiles_for_width):
            temp = []
            y_pos = 0
            for row in range(self.tiles_for_width):
                # Create a frame object
                temp_frame = Frame(self.sudokuBoard, width=tile_size, height=tile_size, bg="black", highlightbackground="blue", highlightthickness=1)
                temp_frame.place(x=x_pos, y=y_pos)

                # Create a label object
                temp_label = Label(temp_frame, bg="black")
                temp_label.place(x=0, y=0)

                # Calculate which subsquare the Tile is in
                sub_x = column // isqrt(self.tiles_for_width)
                sub_y = row // isqrt(self.tiles_for_width)
                subsquare_coord = (sub_x, sub_y)

                # Create the Tile object and add to list of Tiles
                new_tile = Tile(temp_frame, temp_label, subsquare_coord, self.tiles_for_width, column, row) # tiles_for_width used to initialize entropy
                temp.append(new_tile)
                y_pos += tile_size
            
            tile_grid.append(temp)
            y_pos = 0
            x_pos += tile_size

        return tile_grid

