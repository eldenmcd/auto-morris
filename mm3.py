from board import Board
from player import Player
import copy
import random


class MM3:
    board = Board()

    def __init__(self, player1, player2, num_games=1):
        print("init")

        self.max_invalid_turns = 3
        self.invalid_moves_in_a_row = 0
        self.players = {1: Player.get_player(player1), 2: Player.get_player(player2)}
        print(type(self.players[1]))
        print(type(self.players[2]))

        self.players[1].wins = 0
        self.players[2].wins = 0
        self.draws = 0
        try:
            num_games = int(num_games)
        except TypeError:
            num_games = 1

        for game_i in range(1, num_games + 1):
            print("\n\n\n\n\n")
            print(f"game #{game_i}")
            self.new_game()

        print(f"Final scores:")
        print(f"{self.players[1].name}: {self.players[1].wins}")
        print(f"{self.players[2].name}: {self.players[2].wins}")

    def new_game(self):
        self.board.reset()
        self.current_player = random.choice([1, 2])
        self.next_turn()

    def swap_player(self):
        if self.current_player == 1:
            self.current_player = 2
        elif self.current_player == 2:
            self.current_player = 1
        else:
            raise Exception(f"invalid player {self.current_player}")

    def get_move_old(self):
        # if the current player has pieces not yet played, get a move to pos.
        # If they have no pieces left, get from and to
        unplayed_pieces = self.board.get_unplayed_pieces(self.current_player)
        if unplayed_pieces > 0:
            move_from = None
            try:
                move_to = int(
                    input(f"Player {self.current_player}, what is your move? ")
                )
            except Exception as err:
                raise
        else:
            try:
                move_from = int(
                    input(f"Player {self.current_player}, which piece to move? ")
                )
                assert (
                    self.board.get_position(move_from - 1) == self.current_player
                ), "Invalid move - you can only move your own pieces!"
                move_to = int(
                    input(
                        f"Player {self.current_player}, move from {move_from} to where? "
                    )
                )
            except Exception as err:
                raise
        return move_from, move_to

    def get_move(self):

        move_from, move_to = self.players[self.current_player].get_move(
            copy.deepcopy(self.board), self.current_player
        )

        print(
            f"Player {self.current_player} wants to move from {move_from} to {move_to}"
        )
        return move_from, move_to

    def next_turn(self):
        print(self.board)
        print(str(self.board.board))
        print("next turn:")
        if self.invalid_moves_in_a_row > self.max_invalid_turns:
            print(f"Too many invalid turns from player{self.current_player}")
            exit()
        try:
            move_from, move_to = self.get_move()

            self.board.move(
                self.current_player, None if move_from is None else move_from, move_to
            )
            self.invalid_moves_in_a_row = 0
            print(f"{self.board.name}")
        except AssertionError as err:
            print(err)
            print("Invalid move!")
            self.invalid_moves_in_a_row += 1
            self.next_turn()
        except Exception as err:
            raise err

        result = self.board.game_over()
        if result:
            print("Game Over!")
            print(self.board)
            if result == "draw":
                print(
                    f"The game was a draw through threefold repetition. You are both terrible."
                )
                self.draws += 1
            else:

                print(f"Congratulations Player {self.current_player}")
                self.players[self.current_player].wins += 1

            self.players[1].post_game(self.board, 1)
            self.players[2].post_game(self.board, 2)
            print("====")
            print("====")
        else:
            self.swap_player()
            self.next_turn()
