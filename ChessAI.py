import random


PIECESCORE={'p': 1, 'R': 5, 'N': 3, 'B': 3, 'Q': 9, 'K': 0} #piece values
CHECKMATESCORE=1000 #score for checkmate
STALEMATESCORE=0 #score for stalemate






def FINDRANDOMMOVE(VALIDMOVES):
    return VALIDMOVES[random.randint(0,len(VALIDMOVES)-1)] #randomly select a move from the list of valid moves -1 to avoid index out of range error
    
    
def FINDGREEDYMOVE(GAMESTATE,VALIDMOVES):
    TURN = 1 if GAMESTATE.WHITETOMOVE else -1 #turn is 1 for white and -1 for black
    
    
    OPPMINMAXSCORE= CHECKMATESCORE #set max to checkmate score
    
    
    
    BESTPMOVE = None #set best move to none
    for PMOVE in VALIDMOVES:
        GAMESTATE.MAKEMOVE(PMOVE)
        OPPONENTMOVES= GAMESTATE.GETVALIDMOVES() #get the valid moves of the opponent
        random.shuffle(VALIDMOVES) #shuffle the opponent moves to avoid bias in the AI
        OPPMAXSCORE= -CHECKMATESCORE #finding opponents best move
        for OMOVE in OPPONENTMOVES:
            GAMESTATE.MAKEMOVE(OMOVE)
            if GAMESTATE.CHECKMATE:
                SCORE = -TURN *CHECKMATESCORE #- because it theckecks for the opponent
            elif GAMESTATE.STALEMATE:
                SCORE = STALEMATESCORE
            else:
                SCORE = -TURN * MATERIALSCORE(GAMESTATE.BOARD)
            if SCORE > OPPMAXSCORE:
                OPPMAXSCORE = SCORE
            
            GAMESTATE.UNDOMOVE() #undo the opponent's move    
        if OPPMINMAXSCORE > OPPMAXSCORE:
            OPPMINMAXSCORE = OPPMAXSCORE
            BESTPMOVE = PMOVE
        GAMESTATE.UNDOMOVE()
    return BESTPMOVE
    
def MATERIALSCORE(BOARD):
    SCORE=0
    for ROW in BOARD:
        for SQUARE in ROW:
            if SQUARE[0] == 'w':
                SCORE += PIECESCORE[SQUARE[1]]
            elif SQUARE[0] == 'b':
                SCORE -= PIECESCORE[SQUARE[1]]
    return SCORE #return the score of the board based on the material value of the pieces on the board