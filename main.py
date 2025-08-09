from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.events import Click
from textual.message import Message
from textual.widgets import Button, Label, Static

from board import Board
from cell import Cell as GameCell


class CellClicked(Message):
    def __init__(self, x: int, y: int, event_button: int):
        self.x = x
        self.y = y
        self.event_button = event_button
        super().__init__()


class Cell(Static):
    can_focus = True

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        super().__init__("", classes="cell")

    def update_display(self, cell_data: GameCell) -> None:
        self.remove_class(*self.classes)
        self.add_class("cell")

        if cell_data.is_revealed:
            self.add_class("revealed")

            if cell_data.is_mine:
                self.update("💣")
                self.add_class("mine")
            elif cell_data.adjacent_mines > 0:
                self.update(str(cell_data.adjacent_mines))
                self.add_class(f"c{cell_data.adjacent_mines}")
        elif cell_data.is_flagged:
            self.update(" 🚩")
            self.add_class("flagged")
        else:
            self.update("")
            self.add_class("hidden")

    def on_click(self, event: Click) -> None:
        self.focus()

    def on_key(self, event: Click) -> None:
        if event.key == "space":
            self.post_message(CellClicked(self.x, self.y, 1))
        if event.key == "f":
            self.post_message(CellClicked(self.x, self.y, 2))


class MineSweepers(App):
    CSS_PATH = "minesweepers.css"
    BINDINGS = [
        ("n", "new_game", "New Game"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, width: int = 5, height: int = 5, mines: int = 7):
        self.board_width = width
        self.board_height = height
        self.mines = mines
        self.board = Board(self.board_width, self.board_height, self.mines)
        self.grid_container = None
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label("Minesweepers", id="title")
        yield Label(
            "Left-click to focus, Press 'space' for reveal, 'f' for flag",
            id="instructions",
        )
        yield Label("Press 'n' for a new game, 'q' to quit", id="bindings")
        yield Label("", id="status")

        self.grid_container = Grid(id="game-grid")
        yield self.grid_container

        yield Button("New Game", id="new_game_button")

    def on_mount(self) -> None:
        self.setup_grid()

    def setup_grid(self) -> None:
        if self.grid_container:
            self.grid_container.remove_children()

        self.grid_container.styles.grid_size_columns = self.board_width
        self.grid_container.styles.grid_size_rows = self.board_height
        self.grid_container.styles.width = self.board_width * 6
        self.grid_container.styles.height = self.board_width * 3

        for y in range(self.board_height):
            for x in range(self.board_width):
                cell_widget = Cell(x, y)
                cell_widget.update_display(self.board.grid[x][y])
                self.grid_container.mount(cell_widget)

    def refresh_grid(self):
        cells = self.query(Cell)
        for cell_widget in cells:
            cell_widget.update_display(self.board.grid[cell_widget.x][cell_widget.y])

        if self.board.game_won:
            self.query_one("#status").update("Congratulations! You won!")
        elif self.board.game_over:
            self.query_one("#status").update("Game Over! You hit a mine!")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "new_game_button":
            self.action_new_game()

    def action_new_game(self):
        self.board = Board(self.board_width, self.board_height, self.mines)
        self.setup_grid()
        self.query_one("#status").update("New game started!")

    def on_cell_clicked(self, message: CellClicked) -> None:
        x, y = message.x, message.y
        event_button = message.event_button

        if event_button == 1:
            self.board.reveal_cell(x, y)
        elif event_button == 2:
            self.board.toggle_flag(x, y)

        self.refresh_grid()


if __name__ == "__main__":
    MineSweepers().run()
