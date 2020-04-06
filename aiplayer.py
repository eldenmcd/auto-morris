from player import Player
from random import randint
from board import Board
import random
import copy
import pickle


class AIPlayer(Player):
    def __init__(self, name):
        self.__state_memory_pickle_fname = name + "_aiplayer_state_memory.pkl"
        try:
            f = open(
                self.__state_memory_pickle_fname, "rb"
            )  # 'r' for reading; can be omitted
            self.__state_memory = pickle.load(f)  # load file content as mydict
            f.close()
        except FileNotFoundError:
            self.__state_memory = {}
        except Exception as err:
            raise (err)

        self.current_game_memory = []
        self.current_game_memory_opp = []
        self.learning_rate = 0.2
        super().__init__(name)

    def get_state_memory(self, key):

        try:
            return self.__state_memory[key]
        except KeyError:
            self.__state_memory[key] = random.uniform(0, 1)
            return self.__state_memory[key]

    def set_state_memory(self, key, value):

        self.__state_memory[self.hash_board(key)] = value

    def commit_state_memory(self):
        # print(self.__state_memory)
        pickle.dump(self.__state_memory, open(self.__state_memory_pickle_fname, "wb"))

    def get_move(self, board, player_number):

        # We get a board with p1 and p2 indications and whether we are player 1 or 2.
        # To simplify, we want to always see us = 1, so if we are player 2, flip all states going in?
        # choose your own adventure - What states can we move to, and which is best?
        move_from = None
        move_to = None
        if player_number == 2:
            board.flip_player_perspective()

        # print(self.hash_board(board.board))
        moves = board.get_legal_moves()
        post_move_states = []
        for move in moves:
            # print("move: ")
            # print(f"{move}")
            newboard = copy.deepcopy(board)
            newboard.move(1, move[0], move[1])
            post_move_states.append(newboard)
            print(f"I could move {move[0]} to {move[1]}:")
            print(newboard)
            print(
                f"I like it {self.get_state_memory(self.hash_board(newboard.board))*100:.2f}%\n\n"
            )

        # print("I could go to these boards:")
        # print(f"{post_move_states}")

        scores = []
        for i, state in enumerate(post_move_states):
            scores.append(self.get_state_memory(self.hash_board((state.board))))

        i_max_score = max(range(len(scores)), key=scores.__getitem__)
        if scores.count(i_max_score) > 0:
            max_scoring_moves = []
            for i, score in enumerate(scores):
                if score == i_max_score:
                    max_scoring_moves.append(i)
            max_scoring_move = moves[random.choice(max_scoring_moves)]
        else:

            max_scoring_move = moves[i_max_score]

        # print("I like this option")
        # print(f"{i_max_score}")
        # print(f"{post_move_states[i_max_score]}")
        # print(f"{moves[i_max_score]}")
        move_from = max_scoring_move[0]
        move_to = max_scoring_move[1]

        # for i, state in enumerate(post_move_states):

        # if state.game_won():
        #   print("I like this option:")
        #   print(f"{i}")
        #   print(f"{state}")
        #   print(f"{moves[i]}")
        #   move_from = moves[i][0]
        #   move_to = moves[i][1]

        # if move_to is None:

        # move_from, move_to = random.choice(moves)

        # temp get expected state we chose
        newboard = copy.deepcopy(board)
        newboard.move(1, move_from, move_to)
        self.current_game_memory.append(newboard.board)
        self.current_game_memory_opp.append(board.board)
        print(f"AI {self.name} wants to move from {move_from} to {move_to}.")

        return move_from, move_to

    def post_game(self, board, player_number):
        # Did we win?
        won = board.game_over(player_number)
        if won == "draw":
            reward = 0.1
            won_string = "lost"
        elif won == player_number:
            reward = 1
            won_string = "won"
        else:
            reward = 0
            # Push the winning move to the opposition state stack if we lost
            self.current_game_memory_opp.append(board.board)
            won_string = "lost"

        print(f"AI {self.name} learning from my moves")
        print(f"Game {won_string}  in {len(self.current_game_memory)} turns")
        # update each state to add the difference between next state and this state * learning rate

        self.learn_from_moves(self.current_game_memory, reward)

        print(f"AI {self.name} learning from my opponent's moves")
        board.flip_player_perspective()

        won = board.game_over(player_number)
        if won == "draw":
            reward = 0.1
        elif won == player_number:
            reward = 1
        else:
            reward = 0
        won_string = "won" if won else "lost"
        print(f"Game {won_string}  in {len(self.current_game_memory_opp)} turns")

        self.learn_from_moves(self.current_game_memory_opp, reward)
        self.current_game_memory_opp = []
        self.current_game_memory = []

    def learn_from_moves(self, state_memory, reward):
        next_state_score = reward
        state_memory.reverse()
        for state in state_memory:
            board = Board()
            board.board = state
            print(board)
            hash = self.hash_board(state)

            # print(f"Hash: {hash}")
            state_score = self.get_state_memory(hash)
            print(f"estimation for this board is {state_score:.3f}")
            print(f"Need to drift score toward {next_state_score:.3f} ")
            new_state_score = (
                state_score + (next_state_score - state_score) * self.learning_rate
            )
            self.set_state_memory(hash, new_state_score)
            print(f"new score is {new_state_score:.3f}")
            next_state_score = new_state_score
            # state_score = state score + (reward  + discount_factor * est_optimal_future_value - state_score)
        self.commit_state_memory()

    def hash_board(self, board_state):
        # board is symmetrical 4 ways so find the largest hash of the 4 rotated versions of this state
        rotations = []
        board = Board(board_state)
        # print(f"{str(board.board)}")
        for i in range(4):
            rotations.append(str(board.board))
            board.rotate(1)
            # print(f"{str(board.board)}")
        return max(rotations)
