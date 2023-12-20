class Location :
    
    def __init__(self, name: str, lat: str, lon: str) :
        self.name = name
        self.lat = lat
        self.lon = lon


    def __str__(self) -> str:
        return f'Location: {self.name} ({self.lat}, {self.lon})'