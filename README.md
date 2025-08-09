# Minesweeper

A simple implementation of the classic Minesweeper game using the Textual TUI framework for Python.

## Installation

To run this game, you need to have Python installed. The dependencies are managed using `uv`.

1.  **Install `uv` (if you don't have it):**

    ```bash
    pip install uv
    ```

2.  **Install project dependencies:**

    ```bash
    uv pip install .
    ```

## How to Play

1.  **Run the game:**
    ```bash
    python main.py
    ```
2.  **Game Controls:**
    - **Navigate:** Use the mouse to select a cell.
    - **Reveal a cell:** Press the `space` bar to reveal a cell. If the cell contains a mine, the game is over. If the cell is empty, it will show the number of adjacent mines.
    - **Flag a cell:** Press the `f` key to place a flag on a cell you suspect contains a mine. Press `f` again to remove the flag.
    - **New Game:** Press the `n` key to start a new game at any time.
    - **Quit:** Press the `q` key to exit the game.

## Project Structure

- `main.py`: The main entry point of the application. It handles the game loop, user input, and rendering the game board using Textual.
- `board.py`: Contains the `Board` class, which manages the game logic, including placing mines, calculating adjacent mines, and handling cell reveals.
- `cell.py`: Defines the `Cell` class, representing a single cell on the game board.
- `minesweepers.css`: The CSS file for styling the Textual application.
- `pyproject.toml`: The project's configuration file.
- `uv.lock`: The lock file for the project's dependencies.

## Dependencies

- [Textual](https://textual.textualize.io/)

Enjoy the game!
