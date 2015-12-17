if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from mancala import Match, HumanPlayer
from ai_profiles import HillSearchAI, MinimaxAI, RandomAI
from board import InvalidMove
import random
import time
import os

FILENAME = "data.csv"

def write_to_file(line):
	with open(FILENAME, "a+") as f:
		f.write(line)

def type_to_string(t):
	if t is HillSearchAI:
		return "HillSearch"
	elif t is MinimaxAI:
		return "Minimax"
	elif t is RandomAI:
		return "Random"
	else:
		print t
		return "Unknown Type"


def run_game(p1_type, p2_type):
	match = Match(player1_type=p1_type, player2_type=p2_type)
	a,b = match.handle_next_move(0)
	return a, b

def run_games(p1_type, p2_type):
	for i in range(100):
		start = time.time()

		winner, moves = run_game(p1_type, p2_type)

		elapsed = time.time() - start

		line = type_to_string(p1_type)+ "," + type_to_string(p2_type) +",P"+ str(winner) + "," + str(int(elapsed)) + "," + str(moves) +"\n"

		write_to_file(line)


if __name__ == '__main__':

	print os.path.isfile(FILENAME)
	

	if not os.path.isfile(FILENAME):

		with open(FILENAME, "w+") as c:
			c.write("Player1,Player2,Winner,Time,NumTurns\n")

	p1 = sys.argv[1]
	p2 = sys.argv[2]
	if p1=="R":
		p1_type = RandomAI
	elif p1=="M":
		p1_type = MinimaxAI
	elif p1=="H":
		p1_type = HillSearchAI
	else:
		raise InvalidMove

	if p2=="R":
		p2_type = RandomAI
	elif p2=="M":
		p2_type = MinimaxAI
	elif p2=="H":
		p2_type = HillSearchAI
	else:
		raise InvalidMove

	run_games(p1_type, p2_type)