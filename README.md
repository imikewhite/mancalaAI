# mancalaAI

Instructions for running:

To choose the type of AI you wish to play against, you must change this line in play.py
	    match = Match(player1_type=HumanPlayer, player2_type=HillSearchAI)
	And change player2_type to either RandomAI, HillSearchAI or MinimaxAI

python play.py will start the game