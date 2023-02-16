# ai project[0] tictactoe
# dana conley
# oct. 11, 2022

# !/usr/bin/python3
import math

import numpy as np
import argparse

class TicTacToe:
    def __init__(self, board=None, player=1) -> None:
        if board is None:
            self.board = self.init_board()
        else:
            self.board = board
        self.player = player

    def init_board(self):
        return np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

    def print_board(self):
        print(self.board)

    # check which player has won (or if it's a draw)
    def eval_win(self, board, player):
        # if win is in a row
        for i in range(3):
            if board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != 0:
                if board[i][1] == 1:  # player -1 wins
                    return 1
                else:  # player 1 wins
                    return -1

            # if win is in a column
            if board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] != 0:
                if board[1][i] == 1:  # player -1 wins
                    return 1
                else:  # player 1 wins
                    return -1

        # if win is in first diagonal
        if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != 0:
            if board[1][1] == 1:  # player -1 wins
                return 1
            else:  # player 1 wins
                return -1

        # if win is in second diagonal
        if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] != 0:
            if board[1][1] == 1:
                return 1
            else:
                return -1

        # if empty spaces left
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    return 2

        # if ending in draw
        return 0

    def eval_tie(self, board, player):
        board[2][2] = -player
        board[1][2] = player
        board[2][1] = player
        board[0][1] = -player
        return board

    # check if board is empty
    def board_empty(self):
        empty = 0
        # check if board is empty (all spaces are 0)
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    empty = empty
                if self.board[i][j] != 0:
                    empty = empty + 1
        # board is empty
        if empty == 0:
            return 1
        # board is not empty
        else:
            return 0

    def board_full(self):
        board = self.board
        # check if board is full (all spaces are not 0)
        full = 0
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    full = full
                elif board[i][j] == 1 or board[i][j] == -1:
                    full = full + 1

        # board is full
        if full == 9:
            return 1
        # board is not full
        else:
            return 0

    def minimax(self, board, player, is_maximizing):
        win = self.eval_win(board, is_maximizing)
        if win != 2:
            return win

        scores = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:    # if space is available
                    board[i][j] = player    # test if player makes this move
                    scores.append(self.minimax(board, -player, is_maximizing))    # evaluate minimax
                    board[i][j] = 0     # reset space to empty
        return max(scores) if player == is_maximizing else min(scores)

    def take_turn(self, board, player):
        best_score = -100
        best_row = None
        best_column = None

        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:    # if space is available
                    board[i][j] = player    # test if player makes this move
                    if self.eval_win(board, player) == 1:
                        return board
                    if self.eval_win(board, player) == -1:
                        return board
                    score = self.minimax(board, -player, player)    # evaluate minimax
                    board[i][j] = 0     # reset space to empty
                    if score > best_score:
                        best_score = score  # find best minimax score
                        best_row = i
                        best_column = j
        board[best_row][best_column] = player   # make optimal move
        return board

    def play_game(self):
        board = self.board
        player = self.player
        if board[1][1] == 1:
            board = self.eval_tie(board, self.player)
        while self.eval_win(board, self.player) == 2:
            board = self.take_turn(board, player)
            player = -player

        return board, self.eval_win(board, self.player)

def load_board(filename):
    return np.loadtxt(filename)

# def save_board( self, filename ):
# 	np.savetxt( filename, self.board, fmt='%d')

def main():
    parser = argparse.ArgumentParser(description='Play tic tac toe')
    parser.add_argument('-f', '--file', default=None, type=str, help='load board from file')
    parser.add_argument('-p', '--player', default=1, type=int, choices=[1, -1],
                        help='player that playes first, 1 or -1')
    args = parser.parse_args()

    board = load_board(args.file) if args.file else None
    testcase = np.array([[0, 0, 0],
                         [0, 0, 0],
                         [0, 0, 0]])
    ttt = TicTacToe(testcase, args.player)
    # ttt.print_board()
    b, p = ttt.play_game()
    print("final board: \n{}".format(b))
    print("winner: player {}".format(p))


if __name__ == '__main__':
    main()
