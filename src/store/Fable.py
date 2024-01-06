class Fable :

    # Constructor setting id and story
    def __init__(self, 
                 uuid: int, 
                 votes: int, 
                 text: str,
                 name: str,
                 unicorn: int,
                 spotify_url: str
                 ) :
        
        self.uuid = uuid
        self.votes = votes
        self.text = text
        self.name = name
        self.unicorn = unicorn
        self.spotify_url = spotify_url

    # Convert fable object to dictionary
    def dictify(self) -> dict :
        return {
            "uuid" : self.uuid,
            "votes" : self.votes,
            "text" : self.text,
            "name" : self.name,
            "unicorn" : self.unicorn,
            "spotify_url" : self.spotify_url
        }