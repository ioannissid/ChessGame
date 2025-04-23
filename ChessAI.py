import random


PIECESCORE={'p': 1, 'R': 5, 'N': 3, 'B': 3, 'Q': 9, 'K': 0} #piece values

WKNIGHTSCORES = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

BKNIGHTSCORES = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

WBISHOPSCORES = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

BBISHOPSCORES = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],  
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

WROOKSCORES = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

BROOKSCORES = [[0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]]



WQUEENSCORES = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

BQUEENSCORES = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

WPAWNSCORES = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

BPAWNSCORES = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]


PIECEPOSITIONVALUES = {
    "wN": WKNIGHTSCORES,
    "bN": BKNIGHTSCORES,
    "wB": WBISHOPSCORES,
    "bB": BBISHOPSCORES,
    "wR": WROOKSCORES,
    "bR": BROOKSCORES,
    "wQ": WQUEENSCORES,
    "bQ": BQUEENSCORES,
    "wp": WPAWNSCORES,
    "bp": BPAWNSCORES,}


CHECKMATESCORE=1000 #score for checkmate
STALEMATESCORE=0 #score for stalemate
MAXDEPTH = 4





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
  
 
def FINDBESTMOVE(GAMESTATE,VALIDMOVES,RQUEUE):
    global NEXTMOVE,COUNTER
    COUNTER = 0
    NEXTMOVE= None #set next move to none
    random.shuffle(VALIDMOVES) #shuffle the moves to avoid bias in the AI
    #FINDMINMAXMOVE(GAMESTATE,VALIDMOVES,MAXDEPTH,GAMESTATE.WHITETOMOVE) #find the best move using minmax algorithm
    FINDNEGA_ALPHA_BETAMOVE(GAMESTATE,VALIDMOVES,MAXDEPTH,-CHECKMATESCORE,CHECKMATESCORE,1 if GAMESTATE.WHITETOMOVE else -1) #find the best move using negamax algorithm
    print("COUNTER: ",COUNTER)
    RQUEUE.put(NEXTMOVE) #put the next move in the queue
 
  
  
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
    if GAMESTATE.CHECKMATE:
        return -CHECKMATESCORE * TURNMULTI
    if GAMESTATE.STALEMATE:
        return STALEMATESCORE
    if DEPTH==0:
        return TURNMULTI *BOARDSCORE(GAMESTATE) #return the score of the board based on the material value of the pieces on the board
    
        
    
    
    MAXSCORE= -CHECKMATESCORE
    for PMOVE in VALIDMOVES:
        GAMESTATE.MAKEMOVE(PMOVE)
        NEXTMOVES= GAMESTATE.GETVALIDMOVES()
        SCORE = -FINDNEGA_ALPHA_BETAMOVE(GAMESTATE,NEXTMOVES,DEPTH-1,-BETA,-ALPHA,-TURNMULTI) 
        GAMESTATE.UNDOMOVE()
        if SCORE>  MAXSCORE:
            MAXSCORE = SCORE
            if DEPTH == MAXDEPTH:
                NEXTMOVE = PMOVE
                print(PMOVE,SCORE)
        ALPHA= max(ALPHA,SCORE) #update the alpha value
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
    for ROW in range(len(GAMESTATE.BOARD)):
        for COL in range(len(GAMESTATE.BOARD[ROW])):
            SQUARE= GAMESTATE.BOARD[ROW][COL]
            if SQUARE!= "--":
                PIECEPOSITION=0
                if SQUARE[1] != 'K':
                    PIECEPOSITION = PIECEPOSITIONVALUES[SQUARE][ROW][COL] * 5
                if SQUARE[0] == 'w': 
                    SCORE += PIECESCORE[SQUARE[1]] + PIECEPOSITION  #add the score of the piece and its position value
                elif SQUARE[0] == 'b':
                    SCORE -= PIECESCORE[SQUARE[1]] + PIECEPOSITION  #subtract the score of the piece and its position value
    
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