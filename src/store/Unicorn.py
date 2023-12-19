class Unicorn :
    
    def __init__ (
            self, 
            uuid: int,
            image: str, 
            name: str,
            place_name: str,
            place_lon: float,
            place_lat: float,
            spotted_when: str            
        ) : 
        
        self.uuid = uuid
        self.image = image
        self.name = name
        self.place_name = place_name
        self.place_lon = place_lon
        self.place_lat = place_lat
        self.spotted_when = spotted_when