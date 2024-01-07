from .Location import Location

class Unicorn :
    def __init__ (
            self, 
            uuid: int,
            image: str, 
            name: str,
            spotted_when: str,
            description: str,
            reported_by: str,
            spotted_where: Location,  
        ) : 

        self.uuid = uuid
        self.image = image
        self.name = name
        self.spotted_when = spotted_when
        self.description = description
        self.reported_by = reported_by
        self.spotted_where = spotted_where

    # String representation of the Unicorn class
    def __str__(self) -> str:
        return f"Unicorn: {self.name} ({self.uuid}) ({self.spotted_when}) ({self.description}) ({self.reported_by}) ({self.spotted_where.__str__()}) ({self.image})\n"