class Cell:
    def __init__(self, is_mine: bool = False):
        self.is_mine = is_mine
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def reveal(self):
        if not self.is_flagged:
            self.is_revealed = True
            return True
        return False

    def toggle_flag(self):
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged

    def __rerp__(self):
        return f"Cell(mine={self.is_mine}, revealed={self.is_revealed}, flagged={self.is_flagged}, adjacent={self.adjacent_mines})"

    def __str__(self):
        return f"Cell(mine={self.is_mine}, revealed={self.is_revealed}, flagged={self.is_flagged}, adjacent={self.adjacent_mines})"
