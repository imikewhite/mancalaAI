if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from mancala import Match, HumanPlayer
from ai_profiles import HillSearchAI, MinimaxAI, RandomAI
from board import InvalidMove
import random
import time
import os

FILENAME = "data_rm.csv"

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
	for i in range(25):
		start = time.time()

		scores, moves = run_game(p1_type, p2_type)

		p1_score, p2_score = scores

		elapsed = time.time() - start

		if p1_score > p2_score:
			if p1_type is RandomAI and p2_type is RandomAI:
				winner = "Player1"
			else:
				winner = type_to_string(p1_type)
		else:
			if p1_type is RandomAI and p2_type is RandomAI:
				winner = "Player2"
			else:
				winner = type_to_string(p2_type)


		score = str(p1_score[0]) + " - " + str(p2_score[0])
		diff = p1_score[0] - p2_score[0]
		line = type_to_string(p1_type)+ "," + type_to_string(p2_type) +","+ str(winner) + "," + score + "," + str(abs(diff)) + "," + str(int(elapsed)) + "," + str(moves) +"\n"

		write_to_file(line)


if __name__ == '__main__':

	print os.path.isfile(FILENAME)


	if not os.path.isfile(FILENAME):

		with open(FILENAME, "w+") as c:
			c.write("Player1,Player2,Winner,Score,Diff,Time,NumTurns\n")

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