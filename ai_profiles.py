""" Module for Mancala AI Profiles. """

from random import choice
from os import sys

from mancala import Player, reverse_index
from constants import AI_NAME, P1_PITS, P2_PITS, AI_DEPTH, HILLCLIMB
from tree import Node
import copy

class AIPlayer(Player):
    """ Base class for an AI Player """
    def __init__(self, number, board, name=AI_NAME):
        """ Initializes an AI profile. """
        super(AIPlayer, self).__init__(number, board, name)

    @property
    def pits(self):
        """ Shortcut to AI pits. """
        if self.number == 1:
            return self.board.board[P1_PITS]
        else:
            return self.board.board[P2_PITS]

    @property
    def eligible_moves(self):
        """ Returns a list of integers representing eligible moves. """
        eligible_moves = []
        for i in range(len(self.pits)):
            if not self.pits[i] == 0:
                eligible_moves.append(i)
        return eligible_moves

    @property
    def eligible_free_turns(self):
        """ Returns a list of indexes representing eligible free turns. """

        free_turn_indices = range(1, 7)
        free_turn_indices.reverse()

        elig_free_turns = []

        for i in range(0, 6):
            if self.pits[i] == free_turn_indices[i]:
                elig_free_turns.append(1)
            else:
                elig_free_turns.append(0)

        return elig_free_turns

    def _think(self):
        """ Slight delay for thinking. """
        import time
        print "AI is thinking..."
        time.sleep(0.5)

class RandomAI(AIPlayer):
    """ AI Profile that randomly selects from eligible moves. """

    def get_next_move(self):
        """ Returns next AI move based on profile. """

        self._think()

        return choice(self.eligible_moves)

class VectorAI(AIPlayer):
    """ AI Profile using a simple vector decision method. """

    def get_next_move(self):
        """ Use an reverse indices vector to optimize for free turns. """

        self._think()

        reverse_indices = range(0, 6)
        reverse_indices.reverse()

        # First optimize for free moves.
        for i in reverse_indices:
            if self.eligible_free_turns[i] == 1:
                if self.pits[i] == reverse_index(i) + 1:
                    print "VectorAI, mode 1, playing: " + str(i)
                    return i
        # Then clear out inefficient pits.
        for i in reverse_indices:
            if self.pits[i] > reverse_index(i) + 1:
                print "VectorAI, mode 2, playing: " + str(i)
                return i
        # Finally, select a random eligible move.
        print "VectorAI, mode 3, playing an eligible move."
        return choice(self.eligible_moves)

#Here is a simple minimax AI without pruning, maybe plan to prune with above tree idea
class MinimaxAI(AIPlayer):
    """AI Profile Uses a Simple minimax algorthim"""


    def __init__(self, num, b):
        super(MinimaxAI, self).__init__(num, b)
        self.depth = AI_DEPTH


    def get_pits_for_board(self, board, number):
        if number == 1:
            return board[P1_PITS]
        else:
            return board[P2_PITS]

    def get_eligible_for_board(self, board, number):
        eligible_moves = []
        pits = self.get_pits_for_board(board, number)
        for i in range(len(pits)):
            if not (pits[i] == 0):
                eligible_moves.append(i)
        return eligible_moves


    def flip_number(self, number):
        if number == 1:
            return 2
        else:
            return 1

    def build_game_tree(self, depth, board, is_max, number):
        cpy = copy.deepcopy(board)
        r = Node(cpy, is_max, None)

        if depth == 0 :
            return r

        el_moves = self.get_eligible_for_board(cpy, number)
        for move in el_moves:
            new_board, free_move = self.board._dummy_move_stones(number, move, cpy)
            r_num = number if free_move else self.flip_number(number)
            ci = self.build_game_tree(depth-1, new_board, (is_max if free_move else not is_max), r_num)
            ci.set_move(move)
            r.add_child(ci)       

        return r

    def get_next_move(self):
        self._think()

        cpy = copy.deepcopy(self.board.board)
        tree = self.build_game_tree(AI_DEPTH, cpy, True, self.number)
        score, move = self.minimax(tree)
        return move


    def evaluate_board(self, node):

        ai_win = False
        p_win = False

        if set(node.value[P2_PITS]) == set([0]):
            ai_win = True
        #If either player is empty.
        elif set(node.value[P1_PITS]) == set([0]):
            p_win =  True
        #else game is not over
        else:
            ai_win = False
            p_win = False
        if node.max:
            score = node.value[3][0] - node.value[1][0]
        else:
            score = node.value[1][0] - node.value[3][0]

        if ai_win:
            score = 150
        elif p_win:
            score = -150

        return score


    def minimax(self, node):
        if len(node.children) == 0:
            #Leaf, eval board
            score = self.evaluate_board(node)
            return score, node.move
        else:
            if node.max:
                best = -sys.maxint - 1
                best_move = None
                for child in node.children:
                    next, next_move = self.minimax(child)
                    best = next if next >= best else best
                    best_move = child.move if next >= best else best_move
                return best, best_move
            else:
                best = sys.maxint
                best_move = None
                for child in node.children:
                    next, next_move = self.minimax(child)
                    best = next if next <= best else best
                    best_move = child.move if next <= best else best_move
                return best, best_move

class HillSearchAI(AIPlayer):

    def __init__(self, num, b):
        super(HillSearchAI, self).__init__(num, b)
        self.depth = HILLCLIMB


    def get_pits_for_board(self, board, number):
        if number == 1:
            return board[P1_PITS]
        else:
            return board[P2_PITS]

    def get_eligible_for_board(self, board, number):
        eligible_moves = []
        pits = self.get_pits_for_board(board, number)
        for i in range(len(pits)):
            if not (pits[i] == 0):
                eligible_moves.append(i)
        return eligible_moves


    def flip_number(self, number):
        if number == 1:
            return 2
        else:
            return 1

    def build_game_tree(self, depth, board, is_max, number):
        cpy = copy.deepcopy(board)
        r = Node(cpy, is_max, None)

        if depth == 0 :
            return r

        el_moves = self.get_eligible_for_board(cpy, number)
        for move in el_moves:
            new_board, free_move = self.board._dummy_move_stones(number, move, cpy)
            r_num = number if free_move else self.flip_number(number)
            new_depth = depth - 1 if not free_move else depth
            ci = self.build_game_tree(new_depth, new_board, (is_max if free_move else not is_max), r_num)
            ci.set_move(move)
            r.add_child(ci)       

        return r


    def get_next_move(self):
        self._think()

        cpy = copy.deepcopy(self.board.board)
        tree = self.build_game_tree(HILLCLIMB, cpy, True, self.number)
        score, move = self.minimax(tree)
        return move


    def evaluate_board(self, node):
        if node.max:
            score = node.value[3][0] - node.value[1][0]
        else:
            score = node.value[1][0] - node.value[3][0]

        return abs(score)


    def minimax(self, node):
        if len(node.children) == 0:
            #Leaf, eval board
            score = self.evaluate_board(node)
            return score, node.move
        else:
            if node.max:
                best = -sys.maxint - 1
                best_move = None
                for child in node.children:
                    next, next_move = self.minimax(child)
                    best = next if next >= best else best
                    best_move = child.move if next >= best else best_move
                return best, best_move
            else:
                best = sys.maxint
                best_move = None
                for child in node.children:
                    next, next_move = self.minimax(child)
                    best = next if next <= best else best
                    best_move = child.move if next <= best else best_move
                return best, best_move