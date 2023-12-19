import Location

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
        self.spotted_where = spotted_where
        self.spotted_when = spotted_when
        self.reported_by = reported_by
        self.description = description