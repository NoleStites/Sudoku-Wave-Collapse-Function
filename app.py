from model.Model import Model 
from view.View import View
from controller.Controller import Controller


class App:

    def __init__(self):
        # create a model to be called by the controller
        self.model = Model()
        
        # create a controller for view and model to interact with
        self.controller = Controller(self.model)

        # create a view and place it on the root window
        self.view = View(self.controller)


if __name__ == '__main__':
    app = App()
