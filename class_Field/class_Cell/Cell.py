class Cell:
    coords = []
    status = "blank"
    ship = None

    def __init__(self, status, coords, ship):
        self.status = status
        self.coords = coords
        self.ship = ship