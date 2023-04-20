class Ship:

    def __init__(self, coords, status):
        self.coords = coords
        self.status = status
        self.hp = len(coords)