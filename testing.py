from tree import Node
from board import Board
from ai_profiles import MinimaxAI

def test_tree():
	board = Board()
	ai = MinimaxAI(2, board)
	tree = ai.build_game_tree(3, board.board, True, 2)


	print "FINAL:"
	print tree.print_tree(0)


if __name__ == '__main__':
	test_tree()