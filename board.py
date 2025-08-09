import random

from cell import Cell


class Board:
    def __init__(self, width: int, height: int, num_mines: int):
        self.width = width
        self.height = height
        self.num_mimes = num_mines
        self.grid: list[list[Cell]] = []
        self.game_over = False
        self.game_won = False
        self._setup_board()
        self._place_mines()
        self._calculate_adjacent_mines()

    def _setup_board(self):
        self.grid = [[Cell() for _ in range(self.width)] for _ in range(self.height)]

    def _place_mines(self):
        mine_places = 0
        while mine_places < self.num_mimes:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            if not self.grid[x][y].is_mine:
                self.grid[x][y].is_mine = True
                mine_places += 1

    def _calculate_adjacent_mines(self):
        for x in range(self.width):
            for y in range(self.height):
                if not self.grid[x][y].is_mine:
                    count = 0
                    for neighbour_y in range(y - 1, y + 2):
                        for neighbour_x in range(x - 1, x + 2):
                            if (
                                0 <= neighbour_y < self.height
                                and 0 <= neighbour_x < self.width
                                and self.grid[neighbour_x][neighbour_y].is_mine
                            ):
                                count += 1
                    self.grid[x][y].adjacent_mines = count

    def toggle_flag(self, x: int, y: int):
        if self.game_over:
            return

        cell = self.grid[x][y]
        if not cell.is_revealed:
            cell.toggle_flag()

    def reveal_cell(self, x: int, y: int):
        if self.game_over:
            return

        cell = self.grid[x][y]
        if not cell.reveal():
            return

        if cell.is_mine:
            self.game_over = True
            self.game_won = False

            for row in self.grid:
                for c in row:
                    if c.is_mine:
                        c.is_revealed = True
            return

        if cell.adjacent_mines == 0:
            self._reveal_all_adjacent_empty_cells(x, y)

        self.check_win_condition()

    def _reveal_all_adjacent_empty_cells(self, x: int, y: int):
        for neighbour_y in range(y - 1, y + 2):
            for neighbour_x in range(x - 1, x + 2):
                if 0 <= neighbour_y < self.height and 0 <= neighbour_x < self.width:
                    neighbour_cell = self.grid[neighbour_x][neighbour_y]
                    if not neighbour_cell.is_revealed and not neighbour_cell.is_flagged:
                        neighbour_cell.reveal()
                        if neighbour_cell.adjacent_mines == 0:
                            self._reveal_all_adjacent_empty_cells(
                                neighbour_x, neighbour_y
                            )

    def check_win_condition(self):
        if self.game_over:
            return

        all_cells = sum(
            1
            for row in self.grid
            for cell in row
            if not cell.is_mine and not cell.is_revealed
        )

        if all_cells == 0:
            self.game_won = True
            self.game_over = True
