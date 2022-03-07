import os


class FileWR:
    # write and red with file
    def __init__(self):
        pass
    
    def verify_exist(self, file_location):
        if not os.path.isfile(file_location):
            self.write(file_location)
        
    def write(self, file_location, data="0"):
        with open(file_location, 'w') as f:
            f.write(str(data))
    
    def read(self, file_location):
        self.verify_exist(file_location)
        
        with open(file_location, 'r') as f:
            data = f.read()
        return data
