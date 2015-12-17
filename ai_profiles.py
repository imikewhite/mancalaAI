""" Module for Mancala AI Profiles. """

from random import choice
from os import sys

from mancala import Player, reverse_index
from constants import AI_NAME, P1_PITS, P2_PITS, AI_DEPTH
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
        time.sleep(3)

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


# class MinimaxAI(AIPlayer):
#     # Must resturn the index of the move to be take
#     def get_next_move(self):
#         next_move = self.current_turn.get_next_move()
#         try:
#             self.board.board, free_move_earned = self.board._move_stones(self.current_turn.number, next_move)
#         except InvalidMove:
#             # Check whether game was won by AI.
#             if self._check_for_winner():
#                 import sys
#                 sys.exit()
#             self.handle_next_move()

#         # Check whether game was won.
#         if self._check_for_winner():
#             import sys
#             sys.exit()

#         # Check whether free move was earned
#         if free_move_earned:
#             self.handle_next_move()
#         else:
#             self._swap_current_turn()
#             self.handle_next_move()
#         #Get all the available moves,
#         #Find the value for each of those moves
#             #call minimax with that move and a depth, have it make that move given
#         #Take the highest valued move















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


    #Checks value of each move and returns the index of the best avaliable move
    # def get_next_move(self):
    #     self._think()
    #     #List of pairs, first entry is index for move, second is its value
    #     move_scores = []
    #     #fill move_scores using minimax
    #     for move in self.eligible_moves:
    #         new_board, free_move = self.board._dummy_move_stones(self.number, move, self.board.board)
    #         benefit = self.minimax(4, free_move, new_board)
    #         move_scores.append((move,benefit))
    #     #variable to be replaced by correct choice
    #     choice = -sys.maxint-1
    #     #Get choice with the highest score
    #     for choices in move_scores:
    #         if choices[1] > choice:
    #             choice = choices[0]
    #     #make that move
    #     return choice


    def get_next_move(self):
        self._think()

        cpy = copy.deepcopy(self.board.board)
        tree = self.build_game_tree(AI_DEPTH, cpy, True, 2)
        score, move = self.minimax(tree)
        return move


    def evaluate_board(self, node):

        if node.max:
            score = node.value[3][0] - node.value[1][0]
        else:
            score = node.value[1][0] - node.value[3][0]
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


    # def minimax(self, depth, maximizingPlayer, move_to_be_made):
    #     print "Here is the depth: ", depth
    #     self.board.board, free_move_bool = self.board._move_stones(self.number, move_to_be_made)
    #     if not free_move_bool:
    #         maximizingPlayer = not maximizingPlayer
    #     #If we've gone deep enough or if game is over at this points
    #     #Might want to return score + a certain number if its a winner to give
    #     #such states a higher value and - points if puts other player in winning state
    #     if depth == 0 or self._winner():
    #         # Return value for this move (difference in pits)
    #         if self.number == 1:
    #             score = self.board.board[1][0] - self.board.board[3][0]
    #         else:
    #             score = self.board.board[3][0] - self.board.board[1][0]
    #         return score
    #     # If we are trying to maximize the score
    #     if maximizingPlayer:
    #         bestValue = -sys.maxint-1
    #         #Go through all moves and get best move
    #         old_board = self.board.board
    #         for child in self.eligible_moves:
    #             val = self.minimax(depth - 1, maximizingPlayer,child)
    #             bestValue = max(bestValue, val)
    #             self.board.board = old_board
    #         #return score of move
    #         return bestValue
    #     #We are trying to minimize the score
    #     else:
    #         bestValue = sys.maxint
    #         old_board = self.board.board
    #         for child in self.eligible_moves:
    #             val = self.minimax(depth - 1, maximizingPlayer,child)
    #             bestValue = min(bestValue, val)
    #             self.board.board = old_board
    #         #return score of move
    #         return bestValue

    def _winner(self):
        """ Checks for winner"""
        # If all the pits are 0 then no more moves and the game is over
        if set(self.board.board[P2_PITS]) == set([0]):
            return True
        #If either player is empty.
        elif set(self.board.board[P1_PITS]) == set([0]):
            return True
        #else game is not over
        else:
            return False