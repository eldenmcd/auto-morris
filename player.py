# generate random integer values
from random import seed
from random import randint
import random
from board import Board

# f

# seed random number generator
# print("~=seeding=~")
# seed(1)


class Player(object):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_player(name):
        if name == "human":
            return HumanPlayer(name)
        if name == "random":
            return RandomPlayer(name)
        else:
            from aiplayer import AIPlayer

            return AIPlayer(name)

    def post_game(self, board, player_number):
        won = board.game_over(player_number)
        won_string = "won" if won == player_number else "lost/drawn"
        reaction = "proud" if won else "ashamed"
        print(f"I, {self.name} am {reaction} to have {won_string} this game.")


class HumanPlayer(Player):
    def get_move(self, board, player_number):
        # if the current player has pieces not yet played, get a move to pos.
        # If they have no pieces left, get from and to

        unplayed_pieces = board.get_unplayed_pieces(player_number)
        if unplayed_pieces > 0:
            move_from = None
            try:
                move_to = input(f"Player {player_number}, what is your move? ")
            except Exception as err:
                raise
            try:
                move_to = int(move_to)
            except:
                raise AssertionError(
                    f"Invalid move - please enter an integer, not {move_to}"
                )

            # humans don't understand counting from 0
            move_to -= 1
        else:
            try:
                move_from = (
                    int(input(f"Player {player_number}, which piece to move? ")) - 1
                )
                assert (
                    board.get_position(move_from) == player_number
                ), "Invalid move - you can only move your own pieces!"
                move_to = (
                    int(
                        input(
                            f"Player {player_number}, move from {move_from+1} to where? "
                        )
                    )
                    - 1
                )
            except Exception as err:
                raise

        return move_from, move_to


class RandomPlayer(Player):
    def get_move(self, board, player_number):
        if player_number == 2:
            board.flip_player_perspective()
        moves = board.get_legal_moves()
        move_from, move_to = random.choice(moves)
        print(f"{self.name} wants to move from {move_from} to {move_to}. hur hur")

        return move_from, move_to
