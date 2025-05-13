import random
import MaterialScore

CHECKMATESCORE = 1000000  # Increased to ensure it's prioritized
STALEMATESCORE = 0
MAXDEPTH = 4 # Reduced depth for faster computation
OPENING_RANDOMIZATION = 0.1  # 10% random variation in opening phase


def FINDRANDOMMOVE(VALIDMOVES):
    return VALIDMOVES[random.randint(0,len(VALIDMOVES)-1)] #randomly select a move from the list of valid moves -1 to avoid index out of range error
 
def ORDERMOVES(GAMESTATE, MOVES):#Orders moves to improve alpha-beta pruning efficiency
    
    MOVEVALUES = []
    for MOVE in MOVES:
        MOVEVALUE = 0
        # Base move value for developing pieces with randomization
        if MOVE.PIECEMOV[1] != 'P' and GAMESTATE.MOVECOUNT < 10:
            MOVEVALUE += 50 + random.randint(-10, 10)  # Add small random variation
            
        if MOVE.ISCASTLE:
            MOVEVALUE += 2000
            
        if MOVE.PIECECAP != "--":
            MOVEVALUE = 200 * MaterialScore.PIECESCORE[MOVE.PIECECAP[1]]
            
        if MOVE.ISPAWNPROMOTION:
            MOVEVALUE += MaterialScore.PIECESCORE['Q'] * 90
            
        
        if MOVE.PIECEMOV in MaterialScore.PIECEPOSITIONVALUES:# Add slight randomization to positional scores in opening
            position_value = MaterialScore.PIECEPOSITIONVALUES[MOVE.PIECEMOV][MOVE.ENDROW][MOVE.ENDCOL]
            if GAMESTATE.MOVECOUNT < 10:
                position_value += random.randint(-2, 2)  # Small random variation in opening
            MOVEVALUE += position_value * 5
            
        
        if hasattr(GAMESTATE, 'LASTMOVE') and GAMESTATE.LASTMOVE and MOVE.PIECEMOV == GAMESTATE.LASTMOVE.PIECEMOV:# Penalize repeated moves
            MOVEVALUE -= 100
            
        MOVEVALUES.append((MOVE, MOVEVALUE))
    
    return [x[0] for x in sorted(MOVEVALUES, key=lambda x: x[1], reverse=True)]


def FINDBESTMOVE(GAMESTATE, VALIDMOVES, RQUEUE):
    global NEXTMOVE
    NEXTMOVE = None
    
    
    if GAMESTATE.MOVECOUNT < 10 and random.random() < OPENING_RANDOMIZATION:# Add randomization in opening phase (first 10 moves)
        NEXTMOVE = FINDRANDOMMOVE(VALIDMOVES)
        RQUEUE.put(NEXTMOVE)
        return
    
    
    for MOVE in VALIDMOVES:# First check for immediate checkmates
        GAMESTATE.MAKEMOVE(MOVE)
        if GAMESTATE.CHECKMATE:
            NEXTMOVE = MOVE
            GAMESTATE.UNDOMOVE()
            RQUEUE.put(NEXTMOVE)
            return
        GAMESTATE.UNDOMOVE()
    
    
    ORDEREDMOVES = ORDERMOVES(GAMESTATE, VALIDMOVES)# If no immediate checkmate, do regular search with ordered moves
    FINDNEGA_ALPHA_BETAMOVE(GAMESTATE, ORDEREDMOVES, MAXDEPTH, -CHECKMATESCORE, CHECKMATESCORE, 
                           1 if GAMESTATE.WHITETOMOVE else -1)
    RQUEUE.put(NEXTMOVE)


def FINDNEGA_ALPHA_BETAMOVE(GAMESTATE, VALIDMOVES, DEPTH, ALPHA, BETA, TURNMULTI):
    global NEXTMOVE
    
    if GAMESTATE.CHECKMATE:
        return -CHECKMATESCORE 
    if DEPTH == 0:
        return TURNMULTI * BOARDSCORE(GAMESTATE)
    
    MAXSCORE = -CHECKMATESCORE
    for MOVE in VALIDMOVES:
        GAMESTATE.MAKEMOVE(MOVE)
        SCORE = -FINDNEGA_ALPHA_BETAMOVE(GAMESTATE, GAMESTATE.GETVALIDMOVES(), 
                                        DEPTH-1, -BETA, -ALPHA, -TURNMULTI)
        GAMESTATE.UNDOMOVE()
        
        if SCORE > MAXSCORE:
            MAXSCORE = SCORE
            if DEPTH == MAXDEPTH:
                NEXTMOVE = MOVE
        
        ALPHA = max(ALPHA, SCORE)
        if ALPHA >= BETA:
            break
            
    return MAXSCORE


def BOARDSCORE(GAMESTATE):
    if GAMESTATE.CHECKMATE:
        if GAMESTATE.WHITETOMOVE:
            return -CHECKMATESCORE
        else:
            return CHECKMATESCORE
    elif GAMESTATE.STALEMATE:
        return STALEMATESCORE
    
    SCORE = 0
    
    
    CASTLEDWHITE = getattr(GAMESTATE, 'CASTLEDWHITE', False)# Safely check for castling attributes
    CASTLEDBLACK = getattr(GAMESTATE, 'CASTLEDBLACK', False)
    MOVECOUNT = getattr(GAMESTATE, 'MOVECOUNT', 0)
    
    
    if GAMESTATE.WHITETOMOVE:# Add strong castling evaluation with safe attribute access
        
        if not CASTLEDWHITE and MOVECOUNT > 10:# Penalize not castling in mid-game
            SCORE -= 500
        
        if MOVECOUNT < 10 and hasattr(GAMESTATE, 'CURRENTCASTLERIGHTS'):# Bonus for keeping castling rights early game
            if GAMESTATE.CURRENTCASTLERIGHTS.WKS:
                SCORE += 150
            if GAMESTATE.CURRENTCASTLERIGHTS.WQS:
                SCORE += 150
    else:
        
        if not CASTLEDBLACK and MOVECOUNT > 10:# Same for black
            SCORE += 500
        if MOVECOUNT < 10 and hasattr(GAMESTATE, 'CURRENTCASTLERIGHTS'):
            if GAMESTATE.CURRENTCASTLERIGHTS.BKS:
                SCORE -= 150
            if GAMESTATE.CURRENTCASTLERIGHTS.BQS:
                SCORE -= 150
    
    for ROW in range(len(GAMESTATE.BOARD)):
        for COL in range(len(GAMESTATE.BOARD[ROW])):
            SQUARE= GAMESTATE.BOARD[ROW][COL]
            if SQUARE!= "--":
                PIECEPOSITION=0
                if SQUARE[1] != 'K':
                    PIECEPOSITION = MaterialScore.PIECEPOSITIONVALUES[SQUARE][ROW][COL]
                if SQUARE[0] == 'w': 
                    SCORE += MaterialScore.PIECESCORE[SQUARE[1]] + PIECEPOSITION #add the score of the piece and its position value
                elif SQUARE[0] == 'b':
                    SCORE -= MaterialScore.PIECESCORE[SQUARE[1]] + PIECEPOSITION
    
    return SCORE #return the score of the board based on the material value of the pieces on the board

