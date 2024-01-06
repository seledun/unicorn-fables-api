class Location :
    
    # Constructor setting name, lat and lon
    def __init__(self, name: str, lat: str, lon: str) :
        self.name = name
        self.lat = lat
        self.lon = lon

    # String representation of location
    def __str__(self) -> str:
        return f'Location: {self.name} ({self.lat}, {self.lon})'