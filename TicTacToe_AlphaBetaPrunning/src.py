# -*- coding: utf-8 -*-

import math

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
        self.ai_player = 'O'
        self.human_player = 'X'
        self.memo = {}  #  Memoization cache

    # ------------------ UI ------------------
    def print_board(self):
        print("\n")
        for i in range(0, 9, 3):
            print(f" {self.board[i]} | {self.board[i+1]} | {self.board[i+2]} ")
            if i < 6:
                print("---+---+---")
        print("\n")

    def print_board_with_numbers(self):
        print("\n")
        for i in range(0, 9, 3):
            print(f" {i} | {i+1} | {i+2} ")
            if i < 6:
                print("---+---+---")
        print("\n")

    # ------------------ Helpers ------------------
    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def make_move(self, position, player):
        if self.board[position] == ' ':
            self.board[position] = player
            if self.check_winner(self.board, player):
                self.current_winner = player
            return True
        return False

    def check_winner(self, board, player):
        # Rows
        for i in range(0, 9, 3):
            if all(board[i + j] == player for j in range(3)):
                return True

        # Columns
        for i in range(3):
            if all(board[i + j * 3] == player for j in range(3)):
                return True

        # Diagonals
        if all(board[i] == player for i in [0, 4, 8]):
            return True
        if all(board[i] == player for i in [2, 4, 6]):
            return True

        return False

    def is_full(self, board):
        return ' ' not in board

    def get_empty_positions(self, board):
        return [i for i, spot in enumerate(board) if spot == ' ']

    # ------------------ MINIMAX (Optimized) ------------------
    def minimax(self, board, depth, is_maximizing, alpha, beta):
        key = tuple(board)

        #  Memoization
        if key in self.memo:
            return self.memo[key]

        # Terminal states
        if self.check_winner(board, self.ai_player):
            return 10 - depth
        elif self.check_winner(board, self.human_player):
            return -10 + depth
        elif self.is_full(board):
            return 0

        # Move ordering (center > corners > edges)
        priority = [4, 0, 2, 6, 8, 1, 3, 5, 7]
        moves = [pos for pos in priority if board[pos] == ' ']

        if is_maximizing:
            max_eval = -math.inf

            for pos in moves:
                new_board = board.copy()
                new_board[pos] = self.ai_player

                eval = self.minimax(new_board, depth + 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)

                if beta <= alpha:
                    break  #  PRUNING

            self.memo[key] = max_eval
            return max_eval

        else:
            min_eval = math.inf

            for pos in moves:
                new_board = board.copy()
                new_board[pos] = self.human_player

                eval = self.minimax(new_board, depth + 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)

                if beta <= alpha:
                    break  # PRUNING

            self.memo[key] = min_eval
            return min_eval

    # ------------------ BEST MOVE ------------------
    def get_best_move(self):
        best_score = -math.inf
        best_move = None

        priority = [4, 0, 2, 6, 8, 1, 3, 5, 7]

        for pos in priority:
            if self.board[pos] == ' ':
                new_board = self.board.copy()
                new_board[pos] = self.ai_player

                score = self.minimax(new_board, 0, False, -math.inf, math.inf)

                if score > best_score:
                    best_score = score
                    best_move = pos

        return best_move


# ------------------ GAME LOOP ------------------
def play_game():
    game = TicTacToe()

    print("=" * 40)
    print(" TIC-TAC-TOE (UNBEATABLE AI) ")
    print("=" * 40)

    game.print_board_with_numbers()

    while True:
        choice = input("Who goes first? (1=Human, 2=AI): ").strip()
        if choice in ['1', '2']:
            human_turn = choice == '1'
            break

    while game.empty_squares():
        if human_turn:
            game.print_board()

            while True:
                try:
                    move = int(input("Your move (0-8): "))
                    if move in game.available_moves():
                        break
                    else:
                        print("Invalid move!")
                except:
                    print("Enter a number!")

            game.make_move(move, game.human_player)

            if game.current_winner:
                game.print_board()
                print("YOU WIN  (Impossible!)")
                return

            human_turn = False

        else:
            print("AI thinking...")
            move = game.get_best_move()
            game.make_move(move, game.ai_player)

            print(f"AI plays at {move}")

            if game.current_winner:
                game.print_board()
                print("AI WINS ")
                return

            human_turn = True

        if not game.empty_squares():
            game.print_board()
            print("DRAW ")
            return


if __name__ == "__main__":
    play_game()