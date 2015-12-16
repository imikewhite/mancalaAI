class Node(object):

	def __init__(self, value, is_max):
		self.value = value
		self.max = is_max
		self.num_children = 0
		self.children = []

	def add_child(self, c):
		self.num_children += 1
		self.children.append(c)

	def print_value(self, board):
		return "   %d  %d  %d  %d  %d  %d\n %d                    %d\n   %d  %d  %d  %d  %d  %d\n" % (
               # Player 2 pits in top row
               board[2][5], board[2][4], board[2][3],
               board[2][2], board[2][1], board[2][0],
               # Player 2 & 1 stores in middle row
               board[3][0], board[1][0],
               # Player 1 pits on bottom row
               board[0][0], board[0][1], board[0][2],
               board[0][3], board[0][4], board[0][5])

	def print_tree(self, level):
		tabs = "\t"*level
		ret = tabs + (self.print_value(self.value)) +"\n"
		for child in self.children:
			ret += child.print_tree(level+1)
		return ret
