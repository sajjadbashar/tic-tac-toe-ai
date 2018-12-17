from enum import Enum, auto
from random import *

class Player(Enum):
    X = 1
    O = -1

class TicTacToe(object):

    winning_combos = (
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8],
        [2,4,6] )

    def __init__(self):
        self.board = [None for _ in range(0, 9)]
        self.start_index = randint(0,8)
        self.iter = 0

    def display(self):
        values = ["-" if x is None else x.name for x in self.board]
        string = []
        for i in range(0,9,3):
            row = []
            for j in range(i,i+3):
                row.append(values[j])
            string.append(" | ".join(row))
            string.append(5*"--")
        print ("\n".join(string))

    def solve_and_display(self, method="minimax"):
        self.make_move(Player.X, self.start_index)
        self.display()
        print("\n")
        if method == "minimax":
            player = Player.O
            _, next_move = self.minimax(player)
            while next_move is not None:
                self.make_move(player, next_move)
                self.display()
                print ("Node examined: " + str(self.iter))
                print("\n")
                self.iter = 0
                player = self.get_opponent_of(player)
                _, next_move = self.minimax(player)
        elif method == "alphabeta":
            player = Player.O
            _, next_move = self.alphabeta(player)
            while next_move is not None:
                self.make_move(player, next_move)
                self.display()
                print ("Node examined: " + str(self.iter))
                print("\n")
                self.iter = 0
                player = self.get_opponent_of(player)
                _, next_move = self.alphabeta(player)

    def reset(self):
        self.board = [None for _ in self.board]
        self.display()
    def get_available_moves(self):
        return [i for i, val in enumerate(self.board) if val is None]

    def make_move(self, player, position):
        self.board[position] = player

    def clear_move(self, position):
        self.board[position] = None

    def get_moves_for(self, player):
        return [i for i, val in enumerate(self.board) if val is player]

    def is_complete(self):
        return None not in self.board or self.winner() is not None

    def winner(self):
        for player in (Player.X, Player.O):
            moves = set(self.get_moves_for(player))
            for combo in TicTacToe.winning_combos:
                if set(combo).issubset(moves):
                    return player
        return None

    def x_won(self):
        return self.winner() is Player.X

    def o_won(self):
        return self.winner() is Player.O

    def draw(self):
        return self.winner() is None and self.is_complete() is True

    def get_opponent_of(self, player):
        return Player(player.value * -1)

    def minimax(self, player, depth = 0):
        self.iter += 1
        if self.is_complete():
            if self.x_won(): # Maximizing player win
                return 10 - depth, None
            elif self.draw(): # Game is a tie
                return 0, None
            elif self.o_won(): # Minimizing player win
                return -10 + depth, None

        if player is Player.X: # Maximizing player move
            best = float('-inf')
        else:
            best = float('inf') # Minimizing player move
        for move in self.get_available_moves():
            self.make_move(player, move)
            value, _ = self.minimax(self.get_opponent_of(player), depth+1)
            self.clear_move(move)
            if player is Player.X: # Maximizing player
                if value > best:
                    best, best_move = value, move
            else:
                if value < best: # Minimizing player
                    best, best_move = value, move
        return best, best_move

    def alphabeta(self, player, alpha=float('-inf'), beta=float('inf'), depth=0):
        self.iter += 1
        if self.is_complete():
            if self.x_won(): # Maximizing player win
                return 10 - depth, None
            elif self.draw(): # Game is a tie
                return 0, None
            elif self.o_won(): # Minimizing player win
                return -10 + depth, None

        if player is Player.X: # Maximizing player move
            best = float('-inf')
        else:
            best = float('inf') # Minimizing player move
        for move in self.get_available_moves():
            self.make_move(player, move)
            value, _ = self.alphabeta(self.get_opponent_of(player), alpha, beta, depth+1)
            self.clear_move(move)
            if player is Player.X: # Maximizing player
                if value > best:
                    best, best_move = value, move
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            else:
                if value < best: # Minimizing player
                    best, best_move = value, move
                beta = min(beta, best)
                if beta <= alpha:
                    break
        return best, best_move

tic = TicTacToe()
print("Solving with standard minimax: \n")
tic.solve_and_display(method="minimax")
tic.reset()
print("Solving with alpha-beta pruning: \n")
tic.solve_and_display(method="alphabeta")
