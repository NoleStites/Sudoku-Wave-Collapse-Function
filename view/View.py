from tkinter import *
from PIL import Image, ImageTk  # For resizing images
from controller.Controller import Controller
from view.Tile import Tile


class View():
    
    def __init__(self, controller: Controller):
        """
        Creates a view to be interacted with by the user and
        to display the Sudoku generation results.
        """

        # Initializing the root window
        self.root = Tk()
        self.root.title("Wave Collapse Function: Sudoku")
        self.root.configure(background="#404040")


        # BORROWED CODE (start)
        # Used to center the window so that it doesn't spawn in a random location every time.
        w = 900
        h = 1000

        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()

        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        # BORROWED CODE (end)


        # Make the frame for the Sudoku board
        board_size = 900
        self.sudokuBoard = Frame(self.root, width=board_size, height=board_size, bg="#8c8c8c")
        self.sudokuBoard.pack(expand=True)


        # Generate a grid of tiles with the width of the grid being tiles_for_width tiles
        tiles_for_width = 9
        tile_size = board_size // tiles_for_width
        tile_grid = self.populateGrid(tiles_for_width, tile_size) # Initialize grid with empty Tiles


        # Get a list of resized possible tile images (BLANK and 1-9)
        image_list = self.resizeImages(tile_size)

        
        # Testing picture displaying
        for i in range(9):
            for j in range(9):
                tile_grid[i][j].label['image'] = image_list[i+1]


        self.root.mainloop() # Starts/runs the GUI (everything involving the GUI should come before this)

    
    def resizeImages(self, tile_size: int):
        """
        Create Image objects for each of the 10 images (BLANK, and 1-9),
        resize based on size of tile, and store in and return a list to be reused.
        """
        image_list = []

        # Special case: blank image
        image = Image.open(f"./tiles/tileBLANK.png")                    # Open the image for editting
        image = image.resize((tile_size, tile_size), Image.ANTIALIAS)   # Resize the image based on the tile size
        image = ImageTk.PhotoImage(image)                               # Convert the image to a PhotoImage (tkinter compatable)
        image_list.append(image)

        # Images 1-9
        for num in range(9):
            image = Image.open(f"./tiles/tile{num+1}.png")
            image = image.resize((tile_size, tile_size), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(image)
            image_list.append(image)

        return image_list
   

    def populateGrid(self, tiles_for_width: int, tile_size: int):
        """
        Creates all of the Tile objects to put in the grid and initializes
        them with no image and max entropy. Returns the tile grid list.
        """
        tile_grid = []  # A two-dimensional list to contain the grid of tiles
        x_pos = 0
        for column in range(tiles_for_width):
            temp = []
            y_pos = 0
            for row in range(tiles_for_width):
                # Create a frame object
                temp_frame = Frame(self.sudokuBoard, width=tile_size, height=tile_size, bg="black", highlightbackground="blue", highlightthickness=1)
                temp_frame.place(x=x_pos, y=y_pos)

                # Create a label object
                temp_label = Label(temp_frame, bg="black")
                temp_label.place(x=0, y=0)

                # Create the Tile object and add to list of Tiles
                new_tile = Tile(temp_frame, temp_label, tiles_for_width) # tiles_for_width used to initialize entropy
                temp.append(new_tile)
                y_pos += tile_size
            
            tile_grid.append(temp)
            y_pos = 0
            x_pos += tile_size

        return tile_grid

