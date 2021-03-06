class Node(object):

	def __init__(self, value, is_max, move):
		self.value = value
		self.max = is_max
		self.move = move
		self.num_children = 0
		self.children = []

	def add_child(self, c):
		self.num_children += 1
		self.children.append(c)

	def set_move(self, m):
		self.move = m

	def print_value(self, board, sep):
		return " %s%d  %d  %d  %d  %d  %d\n %s%d                    %d\n  %s%d  %d  %d  %d  %d  %d\n" % (
               # Player 2 pits in top row
               sep, board[2][5], board[2][4], board[2][3],
               board[2][2], board[2][1], board[2][0],
               # Player 2 & 1 stores in middle row
               sep, board[3][0], board[1][0],
               # Player 1 pits on bottom row
               sep, board[0][0], board[0][1], board[0][2],
               board[0][3], board[0][4], board[0][5])

	def print_tree(self, level):
		tabs = "\t"*level
		ret = (self.print_value(self.value, tabs)) +"\n"
		for child in self.children:
			ret += child.print_tree(level+1)
		return ret
		# ret = tabs + str(self.move) + "\n"
		# for child in self.children:
		# 	ret += child.print_tree(level+1)
		# return ret
