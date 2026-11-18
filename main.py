"""
Project: Python Sudoku Solver using Recursive Backtracking
Author: Raja Jain (Enrollment No.: 23100BTCSE15035)
Repository: https://github.com/rajajainds/python-Suduko
Description: Solves any valid 9x9 Sudoku puzzle using constraint-pruned depth-first backtracking.
"""

import time
from typing import List, Optional, Tuple

Board = List[List[int]]


def validate_board_dimensions(board: Board) -> bool:
    """
    Validates that the input board is a well-formed 9x9 integer matrix
    containing only digits in the range 0..9 (where 0 denotes an empty cell).
    """
    if not isinstance(board, list) or len(board) != 9:
        return False
    for row in board:
        if not isinstance(row, list) or len(row) != 9:
            return False
        for val in row:
            if not isinstance(val, int) or val < 0 or val > 9:
                return False
    return True


def print_board(board: Board) -> None:
    """
    Renders the 9x9 Sudoku matrix in a clean, human-readable ASCII grid
    with horizontal and vertical dividers separating the nine 3x3 subgrids.
    """
    for row_idx in range(len(board)):
        if row_idx % 3 == 0 and row_idx != 0:
            print("- - - - - - - - - - - -")

        row_tokens = []
        for col_idx in range(len(board[0])):
            if col_idx % 3 == 0 and col_idx != 0:
                row_tokens.append("|")
            cell_val = board[row_idx][col_idx]
            row_tokens.append(str(cell_val) if cell_val != 0 else ".")
        print(" ".join(row_tokens))


def find_empty(board: Board) -> Optional[Tuple[int, int]]:
    """
    Scans the 9x9 matrix in row-major order to locate the next unassigned cell (value == 0).
    Returns:
        (row, col) tuple of the first empty cell found, or None if the board is completely filled.
    """
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return (row, col)
    return None


def is_valid(board: Board, num: int, pos: Tuple[int, int]) -> bool:
    """
    Checks whether placing candidate digit `num` (1..9) at `pos = (row, col)`
    satisfies all three Sudoku invariants:
      1. Row uniqueness
      2. Column uniqueness
      3. 3x3 subgrid box uniqueness
    """
    row, col = pos

    # 1. Verify horizontal row constraint
    for c in range(9):
        if board[row][c] == num and c != col:
            return False

    # 2. Verify vertical column constraint
    for r in range(9):
        if board[r][col] == num and r != row:
            return False

    # 3. Verify 3x3 subgrid box constraint using integer floor division
    box_start_row = (row // 3) * 3
    box_start_col = (col // 3) * 3

    for r in range(box_start_row, box_start_row + 3):
        for c in range(box_start_col, box_start_col + 3):
            if board[r][c] == num and (r, c) != pos:
                return False

    return True


class SudokuSolver:
    """
    Encapsulates the recursive backtracking solver with instrumentation counters
    to track recursive calls and backtrack steps for algorithmic analysis.
    """

    def __init__(self, board: Board) -> None:
        if not validate_board_dimensions(board):
            raise ValueError("Invalid Sudoku board: expected a 9x9 matrix of integers 0-9.")
        self.board: Board = [row[:] for row in board]
        self.recursive_calls: int = 0
        self.backtracks: int = 0

    def is_initial_board_consistent(self) -> bool:
        """Verifies that pre-filled clues do not violate any Sudoku constraint."""
        for r in range(9):
            for c in range(9):
                val = self.board[r][c]
                if val != 0:
                    self.board[r][c] = 0
                    valid = is_valid(self.board, val, (r, c))
                    self.board[r][c] = val
                    if not valid:
                        return False
        return True

    def solve(self) -> bool:
        """
        Recursively solves the Sudoku puzzle in-place using depth-first backtracking.
        Returns True if a valid complete assignment is found, False otherwise.
        """
        self.recursive_calls += 1
        empty_pos = find_empty(self.board)

        # Base case: no empty cells remain -> puzzle solved
        if empty_pos is None:
            return True

        row, col = empty_pos

        for candidate in range(1, 10):
            if is_valid(self.board, candidate, (row, col)):
                # Tentative assignment
                self.board[row][col] = candidate

                # Recurse to fill remaining cells
                if self.solve():
                    return True

                # Backtrack: undo tentative assignment upon downstream dead-end
                self.board[row][col] = 0
                self.backtracks += 1

        return False


def run_demo() -> None:
    """Driver function demonstrating puzzle execution, timing, and verification."""
    sample_puzzle: Board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    print("Initial Unsolved Sudoku Grid:")
    print_board(sample_puzzle)

    solver = SudokuSolver(sample_puzzle)
    if not solver.is_initial_board_consistent():
        print("Error: Initial puzzle contains conflicting clues.")
        return

    start_time = time.perf_counter()
    solved = solver.solve()
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    if solved:
        print("\nSolved Sudoku Grid:")
        print_board(solver.board)
        print(f"\nSolved in {elapsed_ms:.2f} ms | Recursive Calls: {solver.recursive_calls} | Backtracks: {solver.backtracks}")
    else:
        print("\nNo valid solution exists for the given Sudoku configuration.")


if __name__ == "__main__":
    run_demo()
