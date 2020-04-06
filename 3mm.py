import argparse

from mm3 import MM3


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "player1",
        help="The name of player 1. 'human' is a special name denoting a human input, no AI player.",
    )
    parser.add_argument(
        "player2",
        help="The name of player 2. 'human' is a special name denoting a human input, no AI player.",
    )
    parser.add_argument("--num_games", help="number of games to play")

    args = parser.parse_args()
    # print(args.player1)

    MM3(args.player1, args.player2, args.num_games)


if __name__ == "__main__":
    main()
