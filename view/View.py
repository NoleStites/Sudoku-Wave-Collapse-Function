from controller.Controller import Controller
from logger.logger import Logger
from tile.Tile import Tile
from math import isqrt, floor   # For the square root and floor functions
from tkinter import *
import datetime                 # For getting the date and time for the logs
import time                     # For delaying in order to achieve animation
import os                       # For getting the dimensions of the user's screen
from PIL import Image, ImageTk  # For resizing images
from snapshot.Snapshot import Snapshot
from colorama import Fore, Style    # For colorizing debugging output


class View():
    
    def __init__(self, controller: Controller):
        """
        Creates a view to be interacted with by the user and
        to display the Sudoku generation results.
        """
        self.program_start = True # Buttons run command when GUI is being made; this avoids that
        self.controller = controller
        self.logger = Logger("./log.txt")
        print("\nChoose your Sudoku size:")
        print("- 4x4   (enter \'4\')")
        print("- 9x9   (enter \'9\')   (STANDARD)")
        print("- 16x16 (enter \'16\')")
        print("- 25x25 (enter \'25\')  (MAY TAKE LONG; IF SO, TRY AGAIN)")
        print("- 36x36 (enter \'36\')  (NOT IN OUR LIFETIME)")
        print("- 49x49 (enter \'49\')  (\"\")")
        self.tiles_for_width = int(input("\nChoice: "))
        self.subsquares_along_width = isqrt(self.tiles_for_width)
        print()

        # Verify that input if valid
        if self.tiles_for_width not in [4, 9, 16, 25, 36, 49]:
            raise Exception("Invalid Board Size!")

        # Determine ideal animation speed
        if self.tiles_for_width == 4:
            self.animation_speed = 0.1
        elif self.tiles_for_width == 9:
            self.animation_speed = 0.03
        elif self.tiles_for_width == 16:
            self.animation_speed = 0.009
        elif self.tiles_for_width == 25:
            self.animation_speed = 0.003
        elif self.tiles_for_width == 36:
            self.animation_speed = 0.001
        elif self.tiles_for_width == 49:
            self.animation_speed = 0.001


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
        board_size = 900
        tile_size = board_size // self.tiles_for_width


        # Make a frame for the buttons
        self.button_frame = Frame(self.root, width=200, height=2, bg="blue")
        self.button_frame.pack()


        # Make the Generate, Animate, Gamify, Reset, and Stop buttons
        bg_color = "#262626"
        fg_color = "white"
        act_back = "#595959"
        act_fore = "white"

        button_generate = Button(self.button_frame, width=10, height=2, text="Generate", bg=bg_color, fg=fg_color, activebackground=act_back, activeforeground=act_fore, command=self.generateSudoku)
        button_generate.pack(side=LEFT)

        button_animate = Button(self.button_frame, width=10, height=2, text="Animate", bg=bg_color, fg=fg_color, activebackground=act_back, activeforeground=act_fore, command=self.generateWithAnimation)
        button_animate.pack(side=LEFT)

        button_step_generate = Button(self.button_frame, width=10, height=2, text="Step Generate", bg=bg_color, fg=fg_color, activebackground=act_back, activeforeground=act_fore, command=self.generateWithSteps)
        button_step_generate.pack(side=LEFT)

        self.wait_var = IntVar()
        self.button_next_step = Button(self.button_frame, width=10, height=2, text="Next Step", bg=bg_color, fg=fg_color, activebackground=act_back, activeforeground=act_fore, command=lambda: self.wait_var.set(1)) # The lambda function is borrowed from an external source.
        self.button_next_step.pack(side=LEFT)

        button_gamify = Button(self.button_frame, width=10, height=2, text="Gamify", bg=bg_color, fg=fg_color, activebackground=act_back, activeforeground=act_fore, command=self.gamify)
        button_gamify.pack(side=LEFT)

        button_reset = Button(self.button_frame, width=10, height=2, text="Reset", bg=bg_color, fg=fg_color, activebackground=act_back, activeforeground=act_fore, command=self.generateEmptyBoard)
        button_reset.pack(side=LEFT)

        button_stop = Button(self.button_frame, width=10, height=2, text="Stop", bg=bg_color, fg=fg_color, activebackground=act_back, activeforeground=act_fore, command=self.terminate)
        button_stop.pack(side=LEFT)


        # Make the frame for the Sudoku board
        self.sudokuBoard = Frame(self.root, width=board_size, height=board_size, bg="#8c8c8c")
        self.sudokuBoard.pack()
        self.subsquare_grid = self.makeSubsquares(board_size)
        self.tile_grid = self.populateGrid(tile_size) # Initialize grid with empty Tiles

        # Get a list of resized possible tile images (BLANK and 1-9)
        self.image_list = self.resizeImages(tile_size)

        # Initialize the Sudoku board as empty
        self.generateEmptyBoard()

        # Initialize log file for this program run
        date = datetime.datetime.now()
        self.logger.log(f'\n\n{date.strftime("%c")}\n')
        self.logger.log("----------------------\n")

        # Keep track of the history for backtracking
        # Stack entries are Snapshot objects with the following variables:
        """
        self.collapsed_tile     # The Tile that was collapsed during that step in the generation
        self.collapsed_values   # A list of values that have been tried for this Tile
        """
        self.history = []

        # Start the program GUI
        self.program_start = False
        self.root.mainloop()


    def generateWithAnimation(self):
        """
        A preliminary method between button press and Sudoku generation
        special for the animation button. Because you cant seem to pass
        parameters through button commands, this method will be responsible
        for passing a flag to generateSudoku to allow animation to occur.
        """
        self.generateSudoku(animation_flag=1)


    def generateWithSteps(self):
        """
        A preliminary method between button press and Sudoku generation.
        Allows a user to go through the generation step-by-step.
        """
        self.generateSudoku(step_flag=1)


    def gamify(self):
        """
        Will request the controller to choose a random set of
        tiles equivalent to 63% of the total number of tiles 
        to make empty to allow the Sudoku puzzle to be playable.

        I can modify this in the future to allow for the number of
        removed Tiles to be chosen based on difficulty.
        """
        # Determine how many tiles is 63% of total tiles (ideal for good game)
        total_tiles = self.tiles_for_width * self.tiles_for_width
        num_tiles_to_remove = floor(total_tiles * 0.63)

        # Get list of Tile coordinates to clear
        clear_list = self.controller.getGamifyTiles(num_tiles_to_remove, self.tile_grid)

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
                self.tile_grid[x][y].value = None
                self.tile_grid[x][y].entropy = [ num+1 for num in range(self.tiles_for_width)]
                self.tile_grid[x][y].collapsed = False


    def generateSudoku(self, animation_flag=0, step_flag=0):
        """
        Will continue to get generate until a Sudoku board is
        successfully generated (probability decreases rapidly
        as the board size increases).
        """
        if self.program_start: # Dont run if the GUI is laoding up
            return 0

        start = True # To make the first collapsed Tile be in the center
        backtracking = False # To keep track if we choose the Tile to collapse or not
        self.history = []

        # Start by clearing the board
        self.generateEmptyBoard()

        # Continue this loop until every tile has collapsed
        while True:
            """
            Choosing the tile based on if this is the first time running the method,
            if we are actively backtracking, or if we are proceeding normally.
            """
            if start: # Start with collapsing the Tile in the center
                x = self.tiles_for_width // 2
                y = self.tiles_for_width // 2
                chosen_tile = self.tile_grid[x][y]

            elif backtracking:
                chosen_tile = last_snapshot.collapsed_tile

            else: # Get tuple containing random Tile object to populate and value to populate with
                chosen_tile = self.controller.randomTile(self.tile_grid)

            if chosen_tile == None:
                break   # No more uncollapsed Tiles, so the board is filled and the loop can end

            
            if step_flag == 1 and not(start): # Wait for the Next Step button to be pressed before continuing
                self.root.update()
                self.button_next_step.wait_variable(self.wait_var)
                self.wait_var.set(0)
            
            start = False

            """
            Choosing the value to assign to the Tile based on if we are backtracking
            or if we are proceeding normally.
            """
            if backtracking:
                chosen_value = self.controller.randomValue(chosen_tile, last_snapshot.collapsed_values)

            else:
                chosen_value = self.controller.randomValue(chosen_tile)

            if chosen_value == None: # After exclusions, no entropy can be chosen; time to backtrack.
                # Extract the last snapshot and the coord and value
                if step_flag == 1:
                    self.button_next_step.wait_variable(self.wait_var)
                    self.wait_var.set(0)

                last_snapshot = self.history[-1]
                self.history.pop(-1)
                backtrack_tile = last_snapshot.collapsed_tile
                entropy_val_to_reverse = backtrack_tile.value

                # Reset the Tile that needs to be changed
                backtrack_tile.collapsed = False
                backtrack_tile.label['image'] = self.image_list[0]
                backtrack_tile.value = None

                # Go through the Tile grid and restore the entropy from the last snapshot
                self.reverseEntropy(backtrack_tile, entropy_val_to_reverse)
                backtracking = True

                if step_flag == 1:
                    self.button_next_step.wait_variable(self.wait_var)
                    self.wait_var.set(0)

                continue

            # Mark equivalent Tile in grid as collapsed and assign value to it
            if not(start):
                x = chosen_tile.coord[0]
                y = chosen_tile.coord[1]
            self.tile_grid[x][y].collapsed = True
            self.tile_grid[x][y].label['image'] = self.image_list[chosen_value]
            self.tile_grid[x][y].value = chosen_value

            # Add the new change to history
            if backtracking:
                last_snapshot.collapsed_values.append(chosen_value)
                self.history.append(last_snapshot)
            else:
                self.history.append(Snapshot(chosen_tile, chosen_value))

            backtracking = False

            # Backtrack if a tile will have zero entropy after propagation
            if self.searchZeroEntropyPropagation(chosen_tile, chosen_value) == 1:
                if step_flag == 1:
                    self.button_next_step.wait_variable(self.wait_var)
                    self.wait_var.set(0)

                # Acquire the latest snapshot for backtracking
                last_snapshot = self.history[-1]
                self.history.pop(-1)

                # Reset the Tile that needs to be changed
                self.tile_grid[x][y].collapsed = False
                self.tile_grid[x][y].label['image'] = self.image_list[0]
                self.tile_grid[x][y].value = None

                # Start the cycle again with new exclusions for the values
                backtracking = True
                continue


            # Propagate the entropy of affected Tiles
            self.propagateEntropy(chosen_tile, chosen_value)
            
            # For animation, wait a small amount of time before moving to the next Tile
            if animation_flag == 1: # Perform animation
                time.sleep(self.animation_speed)
                self.root.update()

        self.logGridEntropyCount()


    def searchCollapsed(self):
        """
        Returns the number of collapsed Tiles in the grid.
        """
        size = len(self.tile_grid)
        collapsed_count = 0
        for column in range(size):
            for row in range(size):
                curr_tile = self.tile_grid[row][column]
                if curr_tile.collapsed:
                    collapsed_count += 1
        return collapsed_count



    def logGridValues(self, doPrint=0):
        """
        Prints the values in the grid in the log file for reference.
        """
        size = len(self.tile_grid)
        self.logger.log("\n")
        if doPrint:
            print()
        for column in range(size):
            row_contents = []
            for row in range(size):
                curr_tile = self.tile_grid[row][column]
                if curr_tile.value != None:
                    row_contents.append(curr_tile.value)
                else:
                    row_contents.append(".")
            self.logger.log(f'{row_contents}\n')
            if doPrint:
                print(row_contents)


    def logGridEntropyCount(self, doPrint=0):
        """
        Prints the size of entropy of each Tile in the grid
        in the log file for reference.

        Non-zero values in the result means that the grid
        returned doesn't conform to the rules of Sudoku.
        """
        size = len(self.tile_grid)
        self.logger.log("\n")
        if doPrint:
            print()
        for column in range(size):
            row_contents = []
            for row in range(size):
                curr_tile = self.tile_grid[row][column]
                row_contents.append(len(curr_tile.entropy))

            self.logger.log(f'{row_contents}\n')
            if doPrint:
                print(row_contents)


    def logGridEntropyValues(self):
        """
        Prints the entropy values of each Tile in the grid
        in the log file and terminal for reference.
        """
        size = len(self.tile_grid)
        subsquare_size = int(isqrt(size))
        print()

        for column in range(size):
            row_contents = []
            for row in range(size):
                curr_tile = self.tile_grid[row][column]

                entropy_string = ""

                # Print entropy values by leaving a space in the numberline where value is absent
                for num_counter in range(1, size+1):
                    if curr_tile.entropy.count(num_counter) > 0:
                        entropy_string += (Fore.RED + str(num_counter) + Style.DIM + Style.RESET_ALL)
                    else:
                        entropy_string += (Fore.RED + "." + Style.DIM + Style.RESET_ALL)
                
                if (row+1) % subsquare_size == 0:
                    entropy_string += '|'
                else:
                    entropy_string += ' '
                row_contents.append(entropy_string)

            # Print horizontal subsquare dividers
            if column % subsquare_size == 0:
                divider = ""
                for i in range((size*size) + size):
                    divider += "="
                print(divider)
            
            # Print current row of Tile entropies
            row_string = ""
            curr_tile_num = 1
            for tile in row_contents:
                row_string += tile
            
            print(row_string)
        print(divider)


    def reverseEntropy(self, tile: Tile, entropy_value: int):
        """
        Given a reference Tile and a value, this method will add to all
        necessary Tile's entropy lists the value of entropy_value.
        For going back in time for backtracking.
        """
        size = len(self.tile_grid)

        # Acquire a list of rows, columns, and subsquares that shouldn't be reversed
        exclude_columns = []
        exclude_rows = []
        exclude_subsquares = []

        for column in range(size):
            for row in range(size):
                curr_tile = self.tile_grid[column][row]
                if curr_tile.value == entropy_value:
                    exclude_columns.append(curr_tile.coord[0])
                    exclude_rows.append(curr_tile.coord[1])
                    exclude_subsquares.append(curr_tile.subsquare)

        # Reverse the entropy of Tiles not included in the constraints of the row, column, and subsquare lists
        for column in range(size):
            for row in range(size):
                curr_tile = self.tile_grid[column][row]
                if (curr_tile.coord[0] == tile.coord[0]) or (curr_tile.coord[1] == tile.coord[1]) or (curr_tile.subsquare == tile.subsquare):
                    if (exclude_columns.count(curr_tile.coord[0]) == 0) and (exclude_rows.count(curr_tile.coord[1]) == 0) and (exclude_subsquares.count(curr_tile.subsquare) == 0):
                        if curr_tile.entropy.count(entropy_value) == 0:
                            curr_tile.entropy.append(entropy_value)

    
    def searchZeroEntropyPropagation(self, tile, propagation_value: int):
        """
        Given a Tile soon to be collapsed and a value to ignore, searches the board to see
        if any Tile has zero entropy. If so, return 1, else return 0.
        """
        size = len(self.tile_grid)

        for column in range(size):
            for row in range(size):

                curr_tile = self.tile_grid[column][row]

                if (curr_tile.coord[0] == tile.coord[0]) or (curr_tile.coord[1] == tile.coord[1]) or (curr_tile.subsquare == tile.subsquare):
                    if curr_tile.collapsed == False:
                        if (len(curr_tile.entropy) == 0):
                            print("This case shouldn't happen. We should be catching at length 1.")
                            raise Exception("0 Entropy.")
                            return 1
                        elif (len(curr_tile.entropy) == 1) and (curr_tile.entropy.count(propagation_value) > 0):
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
        image = image.resize((tile_size, tile_size), Image.LANCZOS)   # Resize the image based on the tile size
        image = ImageTk.PhotoImage(image)                               # Convert the image to a PhotoImage (tkinter compatable)
        image_list.append(image)

        # Images 1-9
        for num in range(self.tiles_for_width):
            image = Image.open(f"./tile/tile_images/tile{num+1}.png")
            image = image.resize((tile_size, tile_size), Image.LANCZOS)
            image = ImageTk.PhotoImage(image)
            image_list.append(image)

        return image_list
   

    def populateGrid(self, tile_size: int):
        """
        Creates all of the Tile objects to put in the grid and initializes
        them with no image and max entropy. Returns the tile grid list.
        """
        #tile_size = tile_size-2
        tile_grid = []  # A two-dimensional list to contain the grid of tiles
        x_pos = 0
        prev_sub_x = 0
        for column in range(self.tiles_for_width):
            temp = []
            y_pos = 0
            prev_sub_y = 0
            for row in range(self.tiles_for_width):
                # Calculate which subsquare the Tile is in
                sub_x = column // isqrt(self.tiles_for_width)
                sub_y = row // isqrt(self.tiles_for_width)
                subsquare_coord = (sub_x, sub_y)

                # Check if we have moved down to a new subsquare
                if sub_y != prev_sub_y:
                    prev_sub_y = sub_y
                    y_pos = 0
                if sub_x != prev_sub_x:
                    prev_sub_x = sub_x
                    x_pos = 0

                # Create a frame object
                temp_frame = Frame(self.subsquare_grid[sub_x][sub_y], width=tile_size, height=tile_size, bg="black", highlightbackground="#000066", highlightthickness=1)
                temp_frame.place(x=x_pos, y=y_pos)

                # Create a label object
                temp_label = Label(temp_frame, bg="black")
                temp_label.place(x=0, y=0)

                # Create the Tile object and add to list of Tiles
                new_tile = Tile(temp_frame, temp_label, subsquare_coord, self.tiles_for_width, column, row) # tiles_for_width used to initialize entropy
                temp.append(new_tile)
                y_pos += tile_size
            
            tile_grid.append(temp)
            y_pos = 0
            x_pos += tile_size

        return tile_grid


    def terminate(self):
        """
        Shuts down the app.
        """
        self.wait_var.set(2)
        self.root.destroy()


    def makeSubsquares(self, board_size):
        """
        Populates the Sudoku grid with subsquares and returns a two-dimensional list containing
        all subsquare Frame objects.

        self.sudokuBoard = Frame(self.root, width=board_size, height=board_size, bg="#8c8c8c")
        self.sudokuBoard.pack()
        """
        subsquare_size = board_size // self.subsquares_along_width

        # Create each subsquare frame and store in a two-dimensional list
        subsquare_grid = []
        x_pos = 0
        for column in range(self.subsquares_along_width):
            temp = []
            y_pos = 0
            for row in range(self.subsquares_along_width):
                new_frame = Frame(self.sudokuBoard, width=subsquare_size, height=subsquare_size, bg="black", highlightbackground="blue", highlightthickness=2)
                #new_frame = Frame(self.sudokuBoard, width=subsquare_size, height=subsquare_size, bg="black")
                new_frame.place(x=x_pos, y=y_pos)
                temp.append(new_frame)
                y_pos += subsquare_size

            subsquare_grid.append(temp)
            y_pos = 0
            x_pos += subsquare_size

        return subsquare_grid

