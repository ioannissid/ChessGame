import random


PIECESCORE={'p': 1, 'R': 5, 'N': 3, 'B': 3, 'Q': 9, 'K': 0} #piece values
CHECKMATESCORE=1000 #score for checkmate
STALEMATESCORE=0 #score for stalemate
MAXDEPTH = 3





def FINDRANDOMMOVE(VALIDMOVES):
    return VALIDMOVES[random.randint(0,len(VALIDMOVES)-1)] #randomly select a move from the list of valid moves -1 to avoid index out of range error
    
    
def FINDGREEDYMOVE(GAMESTATE,VALIDMOVES): #find the best move using greedy algorithm legacy
    TURN = 1 if GAMESTATE.WHITETOMOVE else -1 #turn is 1 for white and -1 for black
    
    
    OPPMINMAXSCORE= CHECKMATESCORE #set max to checkmate score
    
    
    random.shuffle(VALIDMOVES) #shuffle the opponent moves to avoid bias in the AI
    BESTPMOVE = None #set best move to none
    for PMOVE in VALIDMOVES:
        GAMESTATE.MAKEMOVE(PMOVE)
        OPPONENTMOVES= GAMESTATE.GETVALIDMOVES() #get the valid moves of the opponent
        if GAMESTATE.STALEMATE:
            OPPMAXSCORE=STALEMATESCORE
        elif GAMESTATE.CHECKMATE:
            OPPMAXSCORE= -CHECKMATESCORE
        else:
            OPPMAXSCORE= -CHECKMATESCORE #finding opponents best move
            for OMOVE in OPPONENTMOVES:
                GAMESTATE.MAKEMOVE(OMOVE)
                GAMESTATE.GETVALIDMOVES() #get the valid moves of the opponent
                if GAMESTATE.CHECKMATE:
                    SCORE = CHECKMATESCORE 
                elif GAMESTATE.STALEMATE:
                    SCORE = STALEMATESCORE
                else:
                    SCORE = -TURN * MATERIALSCORE(GAMESTATE.BOARD) #score based on the material value of the pieces on the board
                if SCORE > OPPMAXSCORE:
                    OPPMAXSCORE = SCORE
                
                GAMESTATE.UNDOMOVE() #undo the opponent's move    
        if OPPMINMAXSCORE > OPPMAXSCORE:
            OPPMINMAXSCORE = OPPMAXSCORE
            BESTPMOVE = PMOVE
        GAMESTATE.UNDOMOVE()
    return BESTPMOVE
  
 
def FINDBESTMOVE(GAMESTATE,VALIDMOVES):
    global NEXTMOVE,COUNTER
    COUNTER = 0
    NEXTMOVE= None #set next move to none
    random.shuffle(VALIDMOVES) #shuffle the moves to avoid bias in the AI
    #FINDMINMAXMOVE(GAMESTATE,VALIDMOVES,MAXDEPTH,GAMESTATE.WHITETOMOVE) #find the best move using minmax algorithm
    FINDNEGA_ALPHA_BETAMOVE(GAMESTATE,VALIDMOVES,MAXDEPTH,-CHECKMATESCORE,CHECKMATESCORE,1 if GAMESTATE.WHITETOMOVE else -1) #find the best move using negamax algorithm
    print("COUNTER: ",COUNTER)
    return NEXTMOVE
 
  
  
def FINDMINMAXMOVE(GAMESTATE,VALIDMOVES,DEPTH,WHITETOMOVE):
    global NEXTMOVE,COUNTER
    COUNTER += 1
    if DEPTH==0:
        return MATERIALSCORE(GAMESTATE.BOARD)
    
    random.shuffle(VALIDMOVES) #shuffle the moves to avoid bias in the AI
    if WHITETOMOVE:
        MAXSCORE= -CHECKMATESCORE
        for PMOVE in VALIDMOVES:
            GAMESTATE.MAKEMOVE(PMOVE)
            NEXTMOVES= GAMESTATE.GETVALIDMOVES() #get the valid moves of the opponent
            SCORE = FINDMINMAXMOVE(GAMESTATE,NEXTMOVES,DEPTH-1,False) 
            if SCORE > MAXSCORE:
                MAXSCORE = SCORE
                if DEPTH == MAXDEPTH:
                    NEXTMOVE = PMOVE
            GAMESTATE.UNDOMOVE()
        return MAXSCORE #return the max score of the move made by the player
            
            
    else:
        MINSCORE= CHECKMATESCORE
        for PMOVE in VALIDMOVES:
            GAMESTATE.MAKEMOVE(PMOVE)
            NEXTMOVES = GAMESTATE.GETVALIDMOVES() 
            SCORE = FINDMINMAXMOVE(GAMESTATE,NEXTMOVES,DEPTH-1,True)
            if SCORE < MINSCORE:
                MINSCORE = SCORE
                if DEPTH == MAXDEPTH:
                    NEXTMOVE = PMOVE
            GAMESTATE.UNDOMOVE()
        return MINSCORE #return the min score of the move made by the opponent
        
    
    
    
    
def FINDNEGAMOVE(GAMESTATE,VALIDMOVES,DEPTH,TURNMULTI): #find the best move using negamax algorithm
    global NEXTMOVE
    if DEPTH==0:
        return TURNMULTI *BOARDSCORE(GAMESTATE) #return the score of the board based on the material value of the pieces on the board
    random.shuffle(VALIDMOVES) #shuffle the moves to avoid bias in the AI
    MAXSCORE= -CHECKMATESCORE
    for PMOVE in VALIDMOVES:
        GAMESTATE.MAKEMOVE(PMOVE)
        NEXTMOVES= GAMESTATE.GETVALIDMOVES()
        SCORE = -FINDNEGAMOVE(GAMESTATE,NEXTMOVES,DEPTH-1,-TURNMULTI) 
        if SCORE>  MAXSCORE:
            MAXSCORE = SCORE
            if DEPTH == MAXDEPTH:
                NEXTMOVE = PMOVE
        
        GAMESTATE.UNDOMOVE()
    return MAXSCORE #return the max score of the move made by the player
    
    
 
def FINDNEGA_ALPHA_BETAMOVE(GAMESTATE,VALIDMOVES,DEPTH,ALPHA,BETA,TURNMULTI): #find the best move using negamax algorithm
    global NEXTMOVE, COUNTER
    COUNTER += 1
    if DEPTH==0:
        return TURNMULTI *BOARDSCORE(GAMESTATE) #return the score of the board based on the material value of the pieces on the board
    
        
    
    
    MAXSCORE= -CHECKMATESCORE
    for PMOVE in VALIDMOVES:
        GAMESTATE.MAKEMOVE(PMOVE)
        NEXTMOVES= GAMESTATE.GETVALIDMOVES()
        SCORE = -FINDNEGA_ALPHA_BETAMOVE(GAMESTATE,NEXTMOVES,DEPTH-1,-BETA,-ALPHA,-TURNMULTI) 
        if SCORE>  MAXSCORE:
            MAXSCORE = SCORE
            if DEPTH == MAXDEPTH:
                NEXTMOVE = PMOVE
        GAMESTATE.UNDOMOVE()
        if MAXSCORE >=ALPHA:
            ALPHA = MAXSCORE
        if ALPHA >= BETA:
            break
        
    return MAXSCORE #return the max score of the move made by the player
 
    
    

def BOARDSCORE(GAMESTATE): #positive score for white and negative score for black
    if GAMESTATE.CHECKMATE:
        if GAMESTATE.WHITETOMOVE:
            return -CHECKMATESCORE
        else:
            return CHECKMATESCORE
    elif GAMESTATE.STALEMATE:
        return STALEMATESCORE
    
    SCORE=0
    for ROW in GAMESTATE.BOARD:
        for SQUARE in ROW:
            if SQUARE[0] == 'w':
                SCORE += PIECESCORE[SQUARE[1]]
            elif SQUARE[0] == 'b':
                SCORE -= PIECESCORE[SQUARE[1]]
    
    return SCORE #return the score of the board based on the material value of the pieces on the board    

  
def MATERIALSCORE(BOARD):
    SCORE=0
    for ROW in BOARD:
        for SQUARE in ROW:
            if SQUARE[0] == 'w':
                SCORE += PIECESCORE[SQUARE[1]]
            elif SQUARE[0] == 'b':
                SCORE -= PIECESCORE[SQUARE[1]]
    
    return SCORE #return the score of the board based on the material value of the pieces on the board