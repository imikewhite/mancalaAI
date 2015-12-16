""" Module for Mancala AI Profiles. """

from random import choice
from os import sys

from mancala import Player, reverse_index
from constants import AI_NAME, P1_PITS, P2_PITS

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

#Here is a simple minimax AI without pruning, maybe plan to prune with above tree idea
class MinimaxAI(AIPlayer):
    """AI Profile Uses a Simple minimax algorthim"""
    #Checks value of each move and returns the index of the best avaliable move
    def get_next_move(self):
        self._think()
        #List of pairs, first entry is index for move, second is its value
        move_scores =[]
        #fill move_scores using minimax
        for move in self.eligible_moves:
            new_board, free_move_bool = self.board._move_stones(self.number, move)
            self.board.board = new_board
            benefit = self.minimax(4,True,0)
            move_scores.append((move,benefit))
        #variable to be replaced by correct choice
        choice = -sys.maxint-1
        #Get choice with the highest score
        for choices in move_scores:
            if choices[1] > choice:
                choice = choices[0]
        #make that move
        return choice


    #returns a score for a certain move....Heuristic based on advantage, not 
    #necessarily fastest path to winning goal
    def minimax(self, depth, maximizingPlayer, score):
        #If we've gone deep enough or if game is over at this points
        #Might want to return score + a certain number if its a winner to give
        #such states a higher value and - points if puts other player in winning state
        if depth == 0 or self._winner():
            # Return value for this move (difference in pits)
            return score
        # If we are trying to maximize the score
        if maximizingPlayer:
            bestValue = -sys.maxint-1
            #Go through all moves and get best move
            for child in self.eligible_moves:
                new_board, free_move_bool = self.board._move_stones(self.number, child)
                if free_move_bool:
                    isMax = True
                else:
                    isMax = False
                #Current players pit scores
                if self.number == 1:
                    newest_score = self.board.board[1][0] - self.board.board[3][0]
                else:
                    newest_score = self.board.board[3][0] - self.board.board[1][0]
                self.board.board = new_board
                val = self.minimax(depth - 1, isMax, newest_score)
                bestValue = max(bestValue, val)
            #return score of move
            return bestValue
        #We are trying to minimize the score
        else:
            bestValue = sys.maxint
            for child in self.eligible_moves:
                new_board, free_move_bool = self.board._move_stones(self.number, child)
                if free_move_bool:
                    isMax = False
                else:
                    isMax = True
                #Current players pit scores
                if self.number == 1:
                    newest_score = self.board.board[1][0] - self.board.board[3][0]
                else:
                    newest_score = self.board.board[3][0] - self.board.board[1][0]
                self.board.board = new_board
                val = self.minimax(depth - 1, isMax, newest_score)
                bestValue = max(bestValue, val)
            #return score of move
            return bestValue

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