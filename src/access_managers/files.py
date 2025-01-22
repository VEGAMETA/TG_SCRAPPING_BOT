from . import AccessManager

class FileManager(AccessManager):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def add_data(self, file_name, data) -> None:
        with open(file_name, 'a', encoding='utf-8') as file:
            file.write(data)
    
    @classmethod
    def get_data(self, file_name) -> list[str]:
        with open(file_name, encoding='utf-8') as file: 
            return file.readlines()
