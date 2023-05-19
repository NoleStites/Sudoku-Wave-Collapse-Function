
class Logger():
    """
    This class is used to log any desired content to a given file.
    """
    def __init__(self, file_path: str):
        # File path of the file to write to
        self.file_path = file_path

    def log(self, string_to_log: str):
        """
        Takes in a string and appends it to the given file.
        """
        # Open the file and write to it
        open_file = open(self.file_path, "a")
        open_file.write(string_to_log)

        # Done writing so close file
        open_file.close()
