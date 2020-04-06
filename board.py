import itertools
from exceptions import MM3MoveException


class Board:
    board = []

    def __init__(self, state=None):
        self.name = "original"

        self.__adjacency = []
        # 0 1 2
        # 3 4 5
        # 6 7 8
        self.__adjacency.insert(0, [1, 3, 4])
        self.__adjacency.insert(1, [0, 2, 4])
        self.__adjacency.insert(2, [1, 4, 5])
        self.__adjacency.insert(3, [0, 4, 6])
        self.__adjacency.insert(4, [0, 1, 2, 3, 5, 6, 7, 8])
        self.__adjacency.insert(5, [2, 4, 8])
        self.__adjacency.insert(6, [3, 4, 7])
        self.__adjacency.insert(7, [6, 4, 8])
        self.__adjacency.insert(8, [4, 5, 7])
        # test adjacency symmetry
        for x in range(8):
            for y in range(8):
                # print(f"{x},{y} adjacent {'yes' if self.is_adjacent(x,y) else 'no'}")
                assert self.is_adjacent(x, y) == self.is_adjacent(
                    y, x
                ), f"Adjacency not symmetrical for {x} and {y}"

        self.reset()

        if state:
            self.board = state

    def __repr__(self):
        # return f"{self.board[0]},{self.board[1]},{self.board[2]}\n{self.board[3]},{self.board[4]},{self.board[5]}\n{self.board[6]},{self.board[7]},{self.board[8]}"
        return self.get_board_string()

    def reset(self):
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.unplayed_pieces = {1: 3, 2: 3}
        self.board_state_counts = {}

    def seen_state(self):
        try:
            self.board_state_counts[str(self.board)] += 1
        except KeyError:
            self.board_state_counts[str(self.board)] = 1

    def move(self, current_player, move_from, move_to):
        # if valid move
        # make move
        # else same player try again
        # print(f"Player{current_player} is moving fom {if(move_from):move_from+1} to {move_to+1})")

        assert (
            self.board[move_to] == 0
        ), f"{self.name} - Invalid Move - Player {current_player} tried to position {move_to+1}, which is occupied by player {self.board[move_to]}"

        if move_from is None:
            self.unplayed_pieces[current_player] -= 1
            # print(
            #    f"{self.name} - player {current_player} has {self.unplayed_pieces[current_player]} pieces still unplayed"
            # )
        else:
            assert (
                self.unplayed_pieces[current_player] == 0
            ), f"{self.name} - Invalid Move - Player {current_player} tried to move a piece at {move_from+1} but still has {self.unplayed_pieces[current_player]} unplayed pieces."
            # print(f"player {current_player} moving from {move_from+1}")
            assert (
                self.get_position(move_from) == current_player
            ), f"{self.name} - Invalid Move - Player {current_player} tried to move player {self.get_position(move_from)}'s piece from position {move_from+1}"
            # Check that player moving to an adjacent square
            assert self.is_adjacent(
                move_from, move_to
            ), f"{self.name} - Invalid Move - Player {current_player} tried to move to a non-adjacent position ({move_from+1} to {move_to+1})"

            self.set_position(move_from, 0)

        self.set_position(move_to, current_player)

    def get_unplayed_pieces(self, current_player):
        return self.unplayed_pieces[current_player]

    def get_position(self, position):
        return self.board[position]

    def is_adjacent(self, pos_1, pos_2):
        return pos_2 in self.__adjacency[pos_1]

    def set_position(self, position, player):
        assert (
            self.board[position] == 0 or player == 0
        ), f"{self.name} - Invalid Move - Player {player} tried to position indexd {position}, which is occupied by player {self.board[position]}"

        self.board[position] = player
        # print(f"{self.name} - setting {position} to {player}")
        self.seen_state()

    def get_board_string(self):
        def f(arg):
            return f"({arg})" if arg > 0 else "   "

        # ╭─────┬─────┬─────╮
        # │     │     │     │
        # │    1│    2│    3│
        # ├─────╲─────╱─────┤
        # │     │     │     │
        # │    4│    5│    6│
        # ├─────╱─────╲─────┤
        # │     │     │     │
        # │    7│    8│    9│
        # ╰─────┴─────┴─────╯
        return (
            f"╭─────┬─────┬─────╮\n"
            f"│ {f(self.board[0])} │ {f(self.board[1])} │ {f(self.board[2])} │\n"
            # f"| {f(self.board[0])} | {if_gt_zero(self.board[1])} | {if_gt_zero(self.board[2])} |\n"
            f"│    1│    2│    3│\n"
            f"├─────╲─────╱─────┤\n"
            f"│ {f(self.board[3])} │ {f(self.board[4])} │ {f(self.board[5])} │\n"
            f"│    4│    5│    6│\n"
            f"├─────╱─────╲─────┤\n"
            f"│ {f(self.board[6])} │ {f(self.board[7])} │ {f(self.board[8])} │\n"
            f"│    7│    8│    9│\n"
            f"╰─────┴─────┴─────╯\n"
        )

    def game_over(self, player=None):
        # check for stalemate
        try:
            if self.board_state_counts[str(self.board)] >= 5:
                return "draw"
        except KeyError:
            # if board has been reversed, we may look for states that didn't happen
            pass
        except Exception:
            raise
        winnable_sets = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ]
        game_won = False
        for ws in winnable_sets:
            if (
                self.board[ws[0]] > 0
                and self.board[ws[0]] == self.board[ws[1]] == self.board[ws[2]]
                and (player == self.board[ws[0]] or player == None)
            ):
                game_won = self.board[ws[0]]
        return game_won

    def get_legal_moves(self):

        # We're always player1 in Philadelphia
        if self.unplayed_pieces[1] > 0:
            # if we have unplayed pieces, any empty square is a valid move
            moves = []
            for i, position in enumerate(self.board):
                # print(f"{i} : {position}")
                if position == 0:
                    # print(f"Could place a piece at {i}")
                    moves.append([None, i])
        else:
            # if we have played all our pieces, we can move any piece to any adjacent empty square
            moves = []
            empty_pos = [i for i, x in enumerate(self.board) if x == 0]
            # print(f"empty squares are {empty_pos}")
            our_pos = [i for i, x in enumerate(self.board) if x == 1]

            for pos in our_pos:
                print(f"moves for {pos}:")
                adjacent_pos = self.__adjacency[pos]
                print(f"adjacent: {adjacent_pos}")
                empty_adjacent_pos = set(adjacent_pos).intersection(empty_pos)
                print(f"adjacent and empty: {empty_adjacent_pos}")
                moves_from_pos = list(itertools.product(*[[pos], empty_adjacent_pos]))
                print(f"Moves avail from this pos:  {moves_from_pos} ")
                moves.extend(moves_from_pos)

            # print(f"our squares are {our_pos}")
            # moves = list(itertools.product(*[our_pos, empty_pos]))

        print(f"{moves}")
        return moves

    def flip_player_perspective(self):
        # print("flipping")
        self.name = "flipped"
        # print(f"{self.board}")
        newboard = [1 if x == 2 else 2 if x == 1 else 0 for x in self.board]
        self.board = newboard
        # print(f"{self.board}")
        self.unplayed_pieces = {1: self.unplayed_pieces[2], 2: self.unplayed_pieces[1]}

    def rotate(self, clockwise_quarter_rotations):
        # there must be a really clever way but this is faster to
        for rots in range(clockwise_quarter_rotations):
            newboard = []
            rotated = [6, 3, 0, 7, 4, 1, 8, 5, 2]
            for i in rotated:
                newboard.append(self.board[i])
            self.board = newboard
