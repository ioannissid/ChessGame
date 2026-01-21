#Chess engine to calculate, play moves, save info and valid moves

import random

# Zobrist hashing tables for unique board state identifiers
class ZOBRIST:
    #Generates and manages Zobrist hashes for board positions
    def __init__(self):
        random.seed(42)  # Consistent seed for reproducibility
        self.PIECE_HASHES = {}  # [piece][row][col]
        self.SIDE_HASH = random.getrandbits(64)
        self.CASTLERIGHTS_HASHES = [random.getrandbits(64) for _ in range(16)]  # 2^4 combinations
        self.ENPASSANT_HASHES = [random.getrandbits(64) for _ in range(8)]  # for each file (column)
        
        # Initialize piece position hashes for all piece types and squares
        pieces = ["wp", "wN", "wB", "wR", "wQ", "wK", "bp", "bN", "bB", "bR", "bQ", "bK"]
        for piece in pieces:
            self.PIECE_HASHES[piece] = {}
            for row in range(8):
                self.PIECE_HASHES[piece][row] = {}
                for col in range(8):
                    self.PIECE_HASHES[piece][row][col] = random.getrandbits(64)
    
    def get_piece_hash(self, piece, row, col):
        #Get hash for a specific piece at a given position
        if piece == "--":
            return 0
        return self.PIECE_HASHES[piece][row][col]
    
    def get_castle_hash(self, wks, wqs, bks, bqs):
        #Get hash for castling rights
        index = (int(wks) << 3) | (int(wqs) << 2) | (int(bks) << 1) | int(bqs)
        return self.CASTLERIGHTS_HASHES[index]
    
    def get_enpassant_hash(self, ep_col):
        #Get hash for en passant file
        if ep_col == -1:
            return 0
        return self.ENPASSANT_HASHES[ep_col]

# Global Zobrist instance
ZOBRIST_INSTANCE = ZOBRIST()


class GAMESTATE:
    def __init__(self):
        #2d list of the board
        #w=white,b=black,R=Rook,N=Knight(to avoid confusion with king),B=Bishop,Q=Queen,K=King, -- = empty space
        self.BOARD = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.MOVEFUNCTIONS = {"p": self.GETPAWNMOVES, "R": self.GETROOKMOVES, "N": self.GETKNIGHTMOVES,
                              "B": self.GETBISHOPMOVES, "Q": self.GETQUEENMOVES, "K": self.GETKINGSMOVES}
        self.WHITETOMOVE = True
        self.MOVELOG = []
        self.WKINGLOC = (7, 4)
        self.BKINGLOC = (0, 4)
        self.CHECKMATE = False
        self.STALEMATE = False
        self.INCHECK = False
        self.PINNED = []
        self.CHECKS = []
        self.ENPASSANTPOSSIBLE = ()  #coordinates for enpassant possible capture
        self.ENPASSANTPOSSIBLELOG = [self.ENPASSANTPOSSIBLE]
        self.CURRENTCASTLERIGHTS = CASTLERIGHTS(True, True, True, True) #checks if the pieces moved
        self.CASTLERIGHTSLOG = [CASTLERIGHTS(self.CURRENTCASTLERIGHTS.WKS, self.CURRENTCASTLERIGHTS.BKS,
                                               self.CURRENTCASTLERIGHTS.WQS, self.CURRENTCASTLERIGHTS.BQS)]
        self.CASTLEDWHITE = False
        self.CASTLEDBLACK = False
        self.MOVECOUNT = 0
        self.LASTMOVE = None
        self.BOARD_HASH = self.CALCULATE_BOARD_HASH()  # Unique identifier for this board state
        self.BOARD_HASH_LOG = [self.BOARD_HASH]  # Log of all board hashes
        self.HALFMOVE_CLOCK = 0  # Counts moves since last pawn move or capture (for 50-move rule)
        

    def CALCULATE_BOARD_HASH(self):
        """Calculate Zobrist hash for current board position"""
        hash_value = 0
        
        # Hash all pieces on the board
        for row in range(8):
            for col in range(8):
                piece = self.BOARD[row][col]
                hash_value ^= ZOBRIST_INSTANCE.get_piece_hash(piece, row, col)
        
        # Hash whose turn it is
        if not self.WHITETOMOVE:
            hash_value ^= ZOBRIST_INSTANCE.SIDE_HASH
        
        # Hash castling rights
        hash_value ^= ZOBRIST_INSTANCE.get_castle_hash(
            self.CURRENTCASTLERIGHTS.WKS,
            self.CURRENTCASTLERIGHTS.WQS,
            self.CURRENTCASTLERIGHTS.BKS,
            self.CURRENTCASTLERIGHTS.BQS
        )
        
        # Hash en passant possibility
        if self.ENPASSANTPOSSIBLE:
            ep_col = self.ENPASSANTPOSSIBLE[1]
            hash_value ^= ZOBRIST_INSTANCE.get_enpassant_hash(ep_col)
        else:
            hash_value ^= ZOBRIST_INSTANCE.get_enpassant_hash(-1)
        
        return hash_value
    
    def TO_FEN(self):
    
    #    Convert current board state to FEN (Forsyth-Edwards Notation).
        
    #    FEN format: "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
        
    #    Components:
    #    1. Piece placement (from white's perspective)
    #    2. Active color (w or b)
    #    3. Castling rights (KQkq)
    #    4. En passant target square
    #    5. Halfmove clock (for 50-move rule)
    #    6. Fullmove number
        
    #    Returns:
    #        FEN string representing current position
        # 1. Build piece placement string
        fen_board = []
        for row in self.BOARD:
            fen_row = ""
            empty_count = 0
            
            for square in row:
                if square == "--":
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    # Convert piece: wp → P, bp → p, wN → N, bN → n, etc.
                    # Note: lowercase letter = black, uppercase = white
                    color = square[0]  # 'w' or 'b'
                    piece_type = square[1]  # 'p', 'N', 'B', 'R', 'Q', 'K'
                    
                    if color == 'w':
                        fen_row += piece_type.upper()  # Uppercase for white
                    else:
                        fen_row += piece_type.lower()  # Lowercase for black
            
            if empty_count > 0:
                fen_row += str(empty_count)
            
            fen_board.append(fen_row)
        
        fen_piece_placement = "/".join(fen_board)
        
        # 2. Active color
        fen_color = "w" if self.WHITETOMOVE else "b"
        
        # 3. Castling rights
        fen_castling = ""
        if self.CURRENTCASTLERIGHTS.WKS:
            fen_castling += "K"
        if self.CURRENTCASTLERIGHTS.WQS:
            fen_castling += "Q"
        if self.CURRENTCASTLERIGHTS.BKS:
            fen_castling += "k"
        if self.CURRENTCASTLERIGHTS.BQS:
            fen_castling += "q"
        if not fen_castling:
            fen_castling = "-"
        
        # 4. En passant target square
        if self.ENPASSANTPOSSIBLE:
            ep_row = self.ENPASSANTPOSSIBLE[0]
            ep_col = self.ENPASSANTPOSSIBLE[1]
            # Convert to chess notation
            fen_ep = chr(ord('a') + ep_col) + str(8 - ep_row)
        else:
            fen_ep = "-"
        
        # 5 & 6. Halfmove clock and fullmove number
        fen_halfmove = str(self.HALFMOVE_CLOCK)
        fen_fullmove = str((len(self.MOVELOG) // 2) + 1)
        
        # Combine all components
        fen = f"{fen_piece_placement} {fen_color} {fen_castling} {fen_ep} {fen_halfmove} {fen_fullmove}"
        
        return fen

    def MAKEMOVE(self, MOVE):

        self.BOARD[MOVE.STARTROW][MOVE.STARTCOL] = "--"
        self.BOARD[MOVE.ENDROW][MOVE.ENDCOL] = MOVE.PIECEMOV
        self.MOVELOG.append(MOVE)  #Log move
        self.WHITETOMOVE = not self.WHITETOMOVE #switch turns
        if MOVE.PIECEMOV == "wK":#kings position
            self.WKINGLOC = (MOVE.ENDROW, MOVE.ENDCOL)
        elif MOVE.PIECEMOV == "bK":
            self.BKINGLOC = (MOVE.ENDROW, MOVE.ENDCOL)
        if MOVE.ISPAWNPROMOTION:
            self.BOARD[MOVE.ENDROW][MOVE.ENDCOL] = MOVE.PIECEMOV[0] + "Q" # Default to Queen for the time being
        if MOVE.ENPASSANT:
            self.BOARD[MOVE.STARTROW][MOVE.ENDCOL] = "--"  #capturing
        if MOVE.PIECEMOV[1] == "p" and abs(MOVE.STARTROW - MOVE.ENDROW) == 2:  #only if pawn moves 2
            self.ENPASSANTPOSSIBLE = ((MOVE.STARTROW + MOVE.ENDROW) // 2, MOVE.STARTCOL)
        else:
            self.ENPASSANTPOSSIBLE = ()

        if MOVE.ISCASTLE:
            if MOVE.ENDCOL - MOVE.STARTCOL == 2:  # king-side castle 
                self.BOARD[MOVE.ENDROW][MOVE.ENDCOL - 1] = self.BOARD[MOVE.ENDROW][MOVE.ENDCOL + 1]  #rook goes to new square
                self.BOARD[MOVE.ENDROW][MOVE.ENDCOL + 1] = '--'  #erase old rook
            else:  # queen-side castle 
                self.BOARD[MOVE.ENDROW][MOVE.ENDCOL + 1] = self.BOARD[MOVE.ENDROW][
                    MOVE.ENDCOL - 2]  #rook goes to new square
                self.BOARD[MOVE.ENDROW][MOVE.ENDCOL - 2] = '--'  #erase old rook
            if self.WHITETOMOVE:
                self.CASTLEDWHITE = True
            else:
                self.CASTLEDBLACK = True

        self.ENPASSANTPOSSIBLELOG.append(self.ENPASSANTPOSSIBLE)
        #updating castle rights 
        self.UPDATECASTLERIGHTS(MOVE)
        self.CASTLERIGHTSLOG.append(CASTLERIGHTS(self.CURRENTCASTLERIGHTS.WKS, self.CURRENTCASTLERIGHTS.BKS,
                                                   self.CURRENTCASTLERIGHTS.WQS, self.CURRENTCASTLERIGHTS.BQS))
        self.MOVECOUNT += 1
        self.LASTMOVE = MOVE
        
        # Update halfmove clock for 50-move rule and 3-fold repetition
        if MOVE.PIECECAP != "--" or MOVE.PIECEMOV[1] == "p":
            self.HALFMOVE_CLOCK = 0  # Reset on pawn move or capture
        else:
            self.HALFMOVE_CLOCK += 1
        
        # Update board hash
        self.BOARD_HASH = self.CALCULATE_BOARD_HASH()
        self.BOARD_HASH_LOG.append(self.BOARD_HASH)

    def UNDOMOVE(self):
        if len(self.MOVELOG) != 0:  #make sure that there is a MOVE to undo
            MOVE = self.MOVELOG.pop()
            self.BOARD[MOVE.STARTROW][MOVE.STARTCOL] = MOVE.PIECEMOV
            self.BOARD[MOVE.ENDROW][MOVE.ENDCOL] = MOVE.PIECECAP
            self.WHITETOMOVE = not self.WHITETOMOVE  ## switch turns back
            #update the king's position
            if MOVE.PIECEMOV == "wK":
                self.WKINGLOC = (MOVE.STARTROW, MOVE.STARTCOL)
            elif MOVE.PIECEMOV == "bK":
                self.BKINGLOC = (MOVE.STARTROW, MOVE.STARTCOL)
            #undo en passant 
            if MOVE.ENPASSANT:
                self.BOARD[MOVE.ENDROW][MOVE.ENDCOL] = "--"  #leave landing square blank
                self.BOARD[MOVE.STARTROW][MOVE.ENDCOL] = MOVE.PIECECAP

            self.ENPASSANTPOSSIBLELOG.pop()
            self.ENPASSANTPOSSIBLE = self.ENPASSANTPOSSIBLELOG[-1]

            self.CASTLERIGHTSLOG.pop()  #removing the new castle rights from the move that is being undone
            self.CURRENTCASTLERIGHTS = self.CASTLERIGHTSLOG[-1]  # set the current castle rights to the last one in the list
            # undo the castle MOVE
            if MOVE.ISCASTLE:
                if MOVE.ENDCOL - MOVE.STARTCOL == 2:  # king-side
                    self.BOARD[MOVE.ENDROW][MOVE.ENDCOL + 1] = self.BOARD[MOVE.ENDROW][MOVE.ENDCOL - 1]
                    self.BOARD[MOVE.ENDROW][MOVE.ENDCOL - 1] = '--'
                else:  # queen-side
                    self.BOARD[MOVE.ENDROW][MOVE.ENDCOL - 2] = self.BOARD[MOVE.ENDROW][MOVE.ENDCOL + 1]
                    self.BOARD[MOVE.ENDROW][MOVE.ENDCOL + 1] = '--'
            self.CHECKMATE = False
            self.STALEMATE = False
            
            # Restore board hash
            self.BOARD_HASH_LOG.pop()
            self.BOARD_HASH = self.BOARD_HASH_LOG[-1]

    def UPDATECASTLERIGHTS(self, MOVE):
        if MOVE.PIECECAP == "wR":
            if MOVE.ENDCOL == 0:  #left rook
                self.CURRENTCASTLERIGHTS.WQS = False
            elif MOVE.ENDCOL == 7:  #right rook
                self.CURRENTCASTLERIGHTS.WKS = False
        elif MOVE.PIECECAP == "bR":
            if MOVE.ENDCOL == 0:  #left rook
                self.CURRENTCASTLERIGHTS.BQS = False
            elif MOVE.ENDCOL == 7:  #right rook
                self.CURRENTCASTLERIGHTS.BKS = False

        if MOVE.PIECEMOV == 'wK':
            self.CURRENTCASTLERIGHTS.WQS = False
            self.CURRENTCASTLERIGHTS.WKS = False
        elif MOVE.PIECEMOV == 'bK':
            self.CURRENTCASTLERIGHTS.BQS = False
            self.CURRENTCASTLERIGHTS.BKS = False
        elif MOVE.PIECEMOV == 'wR':
            if MOVE.STARTROW == 7:
                if MOVE.STARTCOL == 0:  #left rook
                    self.CURRENTCASTLERIGHTS.WQS = False
                elif MOVE.STARTCOL == 7:  #right rook
                    self.CURRENTCASTLERIGHTS.WKS = False
        elif MOVE.PIECEMOV == 'bR':
            if MOVE.STARTROW == 0:
                if MOVE.STARTCOL == 0:  #left rook
                    self.CURRENTCASTLERIGHTS.BQS = False
                elif MOVE.STARTCOL == 7:  #right rook
                    self.CURRENTCASTLERIGHTS.BKS = False

    def IS_INSUFFICIENT_MATERIAL(self):
        #Check for insufficient material draw conditions
        piece_count = {}
        for row in self.BOARD:
            for square in row:
                if square != "--":
                    piece_type = square[1]
                    piece_count[piece_type] = piece_count.get(piece_type, 0) + 1
        
        # Only kings on board
        if len(piece_count) == 1 and "K" in piece_count:
            return True
        
        # King vs King + Knight
        if len(piece_count) == 2 and "K" in piece_count and "N" in piece_count and piece_count["N"] == 1:
            return True
        
        # King vs King + Bishop
        if len(piece_count) == 2 and "K" in piece_count and "B" in piece_count and piece_count["B"] == 1:
            return True
        
        return False
    
    def IS_THREEFOLD_REPETITION(self):
        #Check for threefold repetition draw condition
        current_hash = self.BOARD_HASH
        repetition_count = 0
        
        for hash_value in self.BOARD_HASH_LOG:
            if hash_value == current_hash:
                repetition_count += 1
        
        return repetition_count >= 3
    
    def IS_FIFTYMOVE_RULE(self):
        #Check for 50-move rule draw condition
        return self.HALFMOVE_CLOCK >= 100  # 100 halfmoves = 50 full moves

    def GETVALIDMOVES(self):

        TEMPCASTLERIGHTS = CASTLERIGHTS(self.CURRENTCASTLERIGHTS.WKS, self.CURRENTCASTLERIGHTS.BKS,
                                          self.CURRENTCASTLERIGHTS.WQS, self.CURRENTCASTLERIGHTS.BQS)
        MOVES = []
        self.INCHECK, self.PINNED, self.CHECKS = self.CHECKFORTHREATS()

        if self.WHITETOMOVE:
            KROW = self.WKINGLOC[0]
            KCOL = self.WKINGLOC[1]
        else:
            KROW = self.BKINGLOC[0]
            KCOL = self.BKINGLOC[1]
        if self.INCHECK:
            if len(self.CHECKS) == 1:  # only one check
                MOVES = self.GETPOSSIBLEMOVES()
                CHECK = self.CHECKS[0]  # check information
                CHECKROW = CHECK[0]
                CHECKCOL = CHECK[1]
                PIECECHECK = self.BOARD[CHECKROW][CHECKCOL]
                VALIDS = []  #squares that pieces can move to
                #if knight, must capture the knight or MOVE your king, other pieces can be blocked
                if PIECECHECK[1] == "N":
                    VALIDS = [(CHECKROW, CHECKCOL)]
                else:
                    for i in range(1, 8):
                        VALID = (KROW + CHECK[2] * i,KCOL + CHECK[3] * i) 
                        VALIDS.append(VALID)
                        if VALID[0] == CHECKROW and VALID[1] == CHECKCOL:  # break cause we reached threat
                            break
                for i in range(len(MOVES) - 1, -1, -1):  
                    if MOVES[i].PIECEMOV[1] != "K":  #MOVE doesn't MOVE king so it must block or capture
                        if not (MOVES[i].ENDROW,
                                MOVES[i].ENDCOL) in VALIDS:  #MOVE doesn't block or capture PIECE
                            MOVES.remove(MOVES[i])
            else:  # double CHECK, king has to MOVE
                self.GETKINGSMOVES(KROW, KCOL, MOVES)
        else:  # not in CHECK - all MOVES are fine
            MOVES = self.GETPOSSIBLEMOVES()
            if self.WHITETOMOVE:
                self.GETCASTLEMOVES(self.WKINGLOC[0], self.WKINGLOC[1], MOVES)
            else:
                self.GETCASTLEMOVES(self.BKINGLOC[0], self.BKINGLOC[1], MOVES)

        if len(MOVES) == 0:
            if self.INCHECK:
                self.CHECKMATE = True
            else:
                self.STALEMATE = True
        else:
            self.CHECKMATE = False
            self.STALEMATE = False
        
        # Check for other draw conditions (only if no checkmate/stalemate yet)
        if not self.CHECKMATE and not self.STALEMATE:
            if self.IS_INSUFFICIENT_MATERIAL():
                self.STALEMATE = True  # Insufficient material = draw
            elif self.IS_THREEFOLD_REPETITION():
                self.STALEMATE = True  # 3-fold repetition = draw
            elif self.IS_FIFTYMOVE_RULE():
                self.STALEMATE = True  # 50-move rule = draw

        self.CURRENTCASTLERIGHTS = TEMPCASTLERIGHTS
        return MOVES

    def INCHECK(self):
        #is the player in check
        if self.WHITETOMOVE:
            return self.SQUAREUNDERATTACK(self.WKINGLOC[0], self.WKINGLOC[1])
        else:
            return self.SQUAREUNDERATTACK(self.BKINGLOC[0], self.BKINGLOC[1])

    def SQUAREUNDERATTACK(self, ROW, COL):
        #is the square under any kind of attack
        self.WHITETOMOVE = not self.WHITETOMOVE  # switch to opponent's point of view
        opponents_moves = self.GETPOSSIBLEMOVES()
        self.WHITETOMOVE = not self.WHITETOMOVE
        for MOVE in opponents_moves:
            if MOVE.ENDROW == ROW and MOVE.ENDCOL == COL:  # SQUARE is under attack
                return True
        return False

    def GETPOSSIBLEMOVES(self):
        MOVES = []
        for i in range(len(self.BOARD)):
            for j in range(len(self.BOARD[i])):
                TURN = self.BOARD[i][j][0]
                if (TURN == "w" and self.WHITETOMOVE) or (TURN == "b" and not self.WHITETOMOVE):
                    PIECE = self.BOARD[i][j][1]
                    self.MOVEFUNCTIONS[PIECE](i, j, MOVES)  # calls appropriate MOVE function based on PIECE type
        return MOVES

    def CHECKFORTHREATS(self):
        PINNED = []  # squares pinned and the direction its pinned from
        CHECKS = []  # squares where enemy is applying a checks
        INCHECK = False
        if self.WHITETOMOVE:
            ENEMY = "b"
            ALLY = "w"
            STARTROW = self.WKINGLOC[0]
            STARTCOL = self.WKINGLOC[1]
        else:
            ENEMY = "w"
            ALLY = "b"
            STARTROW = self.BKINGLOC[0]
            STARTCOL = self.BKINGLOC[1]
        # CHECK outwards from king for pins and checks
        DIRECTIONS = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(DIRECTIONS)):
            DIR = DIRECTIONS[j]
            POSPIN = ()  # reset possible pin
            for i in range(1, 8):
                ENDROW = STARTROW + DIR[0] * i
                ENDCOL = STARTCOL + DIR[1] * i
                if 0 <= ENDROW <= 7 and 0 <= ENDCOL <= 7:
                    ENDPIECE = self.BOARD[ENDROW][ENDCOL]
                    if ENDPIECE[0] == ALLY and ENDPIECE[1] != "K":
                        if POSPIN == ():  # first allied piece could be pinned
                            POSPIN = (ENDROW, ENDCOL, DIR[0], DIR[1])
                        else:  # 2nd allied piece - no CHECK or pin from this direction
                            break
                    elif ENDPIECE[0] == ENEMY:
                        TYPE = ENDPIECE[1]
                        if (
                            (0 <= j <= 3 and TYPE == "R") or
                            (4 <= j <= 7 and TYPE == "B") or
                            (i == 1 and TYPE == "p" and ((ENEMY == "w" and 6 <= j <= 7) or (ENEMY == "b" and 4 <= j <= 5))) or
                            (TYPE == "Q") or
                            (i == 1 and TYPE == "K")
                            ):
                            if POSPIN == ():  # no PIECE blocking, so CHECK
                                INCHECK = True
                                CHECKS.append((ENDROW, ENDCOL, DIR[0], DIR[1]))
                                break
                            else:  # PIECE blocking so pin
                                PINNED.append(POSPIN)
                                break
                        else:  # enemy PIECE not applying CHECKS
                            break
                else:
                    break  # off BOARD
        # CHECK for knight CHECKS
        KDIRECTIONS = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for MOVE in KDIRECTIONS:
            ENDROW = STARTROW + MOVE[0]
            ENDCOL = STARTCOL + MOVE[1]
            if 0 <= ENDROW <= 7 and 0 <= ENDCOL <= 7:
                ENDPIECE = self.BOARD[ENDROW][ENDCOL]
                if ENDPIECE[0] == ENEMY and ENDPIECE[1] == "N":  # enemy knight attacking a king
                    INCHECK = True
                    CHECKS.append((ENDROW, ENDCOL, MOVE[0], MOVE[1]))
        return INCHECK, PINNED, CHECKS

    def GETPAWNMOVES(self, ROW, COL, MOVES):
        #get pawn moves
        PINNED = False
        PINDIR = () #pin direction
        for i in range(len(self.PINNED) - 1, -1, -1):
            if self.PINNED[i][0] == ROW and self.PINNED[i][1] == COL:
                PINNED = True
                PINDIR = (self.PINNED[i][2], self.PINNED[i][3])
                self.PINNED.remove(self.PINNED[i])
                break

        if self.WHITETOMOVE:
            MOVEAMOUNT = -1
            STARTROW = 6
            ENEMY = "b"
            KROW, KCOL = self.WKINGLOC
        else:
            MOVEAMOUNT = 1
            STARTROW = 1
            ENEMY = "w"
            KROW, KCOL = self.BKINGLOC

        if self.BOARD[ROW + MOVEAMOUNT][COL] == "--":  # 1 SQUARE
            if not PINNED or PINDIR == (MOVEAMOUNT, 0):
                MOVES.append(MOVE((ROW, COL), (ROW + MOVEAMOUNT, COL), self.BOARD))
                if ROW == STARTROW and self.BOARD[ROW + 2 * MOVEAMOUNT][COL] == "--":  # 2 SQUARE
                    MOVES.append(MOVE((ROW, COL), (ROW + 2 * MOVEAMOUNT, COL), self.BOARD))
        if COL - 1 >= 0:  # capture to the left
            if not PINNED or PINDIR == (MOVEAMOUNT, -1):
                if self.BOARD[ROW + MOVEAMOUNT][COL - 1][0] == ENEMY:
                    MOVES.append(MOVE((ROW, COL), (ROW + MOVEAMOUNT, COL - 1), self.BOARD))
                if (ROW + MOVEAMOUNT, COL - 1) == self.ENPASSANTPOSSIBLE:
                    ATTACKING = BLOCKING = False
                    if KROW == ROW:
                        if KCOL < COL:  # king is left of the pawn ,inside: between king and the pawn ,outside: between pawn and border
                            INSIDERANGE = range(KCOL + 1, COL - 1)
                            OUTSIDERANGE = range(COL + 1, 8)
                        else:  # king right of the pawn
                            INSIDERANGE = range(KCOL - 1, COL, -1)
                            OUTSIDERANGE = range(COL - 2, -1, -1)
                        for i in INSIDERANGE:
                            if self.BOARD[ROW][i] != "--":  # some PIECE beside en-passant pawn blocks
                                BLOCKING = True
                        for i in OUTSIDERANGE:
                            SQUARE = self.BOARD[ROW][i]
                            if SQUARE[0] == ENEMY and (SQUARE[1] == "R" or SQUARE[1] == "Q"):
                                ATTACKING = True
                            elif SQUARE != "--":
                                BLOCKING = True
                    if not ATTACKING or BLOCKING:
                        MOVES.append(MOVE((ROW, COL), (ROW + MOVEAMOUNT, COL - 1), self.BOARD, ENPASSANT=True))
        if COL + 1 <= 7:  # capture to the right
            if not PINNED or PINDIR == (MOVEAMOUNT, +1):
                if self.BOARD[ROW + MOVEAMOUNT][COL + 1][0] == ENEMY:
                    MOVES.append(MOVE((ROW, COL), (ROW + MOVEAMOUNT, COL + 1), self.BOARD))
                if (ROW + MOVEAMOUNT, COL + 1) == self.ENPASSANTPOSSIBLE:
                    ATTACKING = BLOCKING = False
                    if KROW == ROW:
                        if KCOL < COL:  # king is left of the pawn
                            INSIDERANGE = range(KCOL + 1, COL)
                            OUTSIDERANGE = range(COL + 2, 8)
                        else:  # king right of the pawn
                            INSIDERANGE = range(KCOL - 1, COL + 1, -1)
                            OUTSIDERANGE = range(COL - 1, -1, -1)
                        for i in INSIDERANGE:
                            if self.BOARD[ROW][i] != "--":  # some PIECE beside en-passant pawn blocks
                                BLOCKING = True
                        for i in OUTSIDERANGE:
                            SQUARE = self.BOARD[ROW][i]
                            if SQUARE[0] == ENEMY and (SQUARE[1] == "R" or SQUARE[1] == "Q"):
                                ATTACKING = True
                            elif SQUARE != "--":
                                BLOCKING = True
                    if not ATTACKING or BLOCKING:
                        MOVES.append(MOVE((ROW, COL), (ROW + MOVEAMOUNT, COL + 1), self.BOARD, ENPASSANT=True))

    def GETROOKMOVES(self, ROW, COL, MOVES):

        PINNED = False
        PINDIR = ()
        for i in range(len(self.PINNED) - 1, -1, -1):
            if self.PINNED[i][0] == ROW and self.PINNED[i][1] == COL:
                PINNED = True
                PINDIR = (self.PINNED[i][2], self.PINNED[i][3])
                if self.BOARD[ROW][COL][1] != "Q":  #because i call it for the queen moves as well
                    self.PINNED.remove(self.PINNED[i])
                break

        DIRECTIONS = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        ENEMY = "b" if self.WHITETOMOVE else "w"
        for DIR in DIRECTIONS:
            for i in range(1, 8):
                ENDROW = ROW + DIR[0] * i
                ENDCOL = COL + DIR[1] * i
                if 0 <= ENDROW <= 7 and 0 <= ENDCOL <= 7:  # check for moves inside the boundary
                    if not PINNED or PINDIR == DIR or PINDIR == (
                            -DIR[0], -DIR[1]):
                        ENDPIECE = self.BOARD[ENDROW][ENDCOL]
                        if ENDPIECE == "--":  #empty space is valid
                            MOVES.append(MOVE((ROW, COL), (ENDROW, ENDCOL), self.BOARD))
                        elif ENDPIECE[0] == ENEMY:  #capture enemy piece
                            MOVES.append(MOVE((ROW, COL), (ENDROW, ENDCOL), self.BOARD))
                            break
                        else:  #friendly piece
                            break
                else:  #off BOARD
                    break

    def GETKNIGHTMOVES(self, ROW, COL, MOVES):
        #get the knight moves
        PINNED = False
        for i in range(len(self.PINNED) - 1, -1, -1):
            if self.PINNED[i][0] == ROW and self.PINNED[i][1] == COL:
                PINNED = True
                self.PINNED.remove(self.PINNED[i])
                break

        KDIRECTIONS = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2),(1, -2))  #up/left up/right right/up right/down down/left down/right left/up left/down
        ALLY = "w" if self.WHITETOMOVE else "b"
        for M in KDIRECTIONS:
            ENDROW = ROW + M[0]
            ENDCOL = COL + M[1]
            if 0 <= ENDROW <= 7 and 0 <= ENDCOL <= 7:
                if not PINNED:
                    ENDPIECE = self.BOARD[ENDROW][ENDCOL]
                    if ENDPIECE[0] != ALLY:  #so its either enemy PIECE or empty SQUARE
                        MOVES.append(MOVE((ROW, COL), (ENDROW, ENDCOL), self.BOARD))

    def GETBISHOPMOVES(self, ROW, COL, MOVES):
        PINNED = False
        PINDIR = ()
        for i in range(len(self.PINNED) - 1, -1, -1):
            if self.PINNED[i][0] == ROW and self.PINNED[i][1] == COL:
                PINNED = True
                PINDIR = (self.PINNED[i][2], self.PINNED[i][3])
                if self.BOARD[ROW][COL][1] != "Q":  # Keep pin info for queens
                    self.PINNED.remove(self.PINNED[i])
                break
            break

        DIRECTIONS = ((-1, -1), (-1, 1), (1, 1), (1, -1))  #diagonals: up/left up/right down/right down/left
        ENEMY = "b" if self.WHITETOMOVE else "w"
        for DIR in DIRECTIONS:
            for i in range(1, 8):
                ENDROW = ROW + DIR[0] * i
                ENDCOL = COL + DIR[1] * i
                if 0 <= ENDROW <= 7 and 0 <= ENDCOL <= 7:  
                    if not PINNED or PINDIR == DIR or PINDIR== (-DIR[0], -DIR[1]):
                        ENDPIECE = self.BOARD[ENDROW][ENDCOL]
                        if ENDPIECE == "--":  
                            MOVES.append(MOVE((ROW, COL), (ENDROW, ENDCOL), self.BOARD))
                        elif ENDPIECE[0] == ENEMY:
                            MOVES.append(MOVE((ROW, COL), (ENDROW, ENDCOL), self.BOARD))
                            break
                        else:  # friendly PIECE
                            break
                else:  # off BOARD
                    break

    def GETQUEENMOVES(self, ROW, COL, MOVES):
        #queen moves are a combination of rook and bishop moves
        self.GETBISHOPMOVES(ROW, COL, MOVES)
        self.GETROOKMOVES(ROW, COL, MOVES)

    def GETKINGSMOVES(self, ROW, COL, MOVES):
        ROWMOVES = (-1, -1, -1, 0, 0, 1, 1, 1)
        COLMOVES = (-1, 0, 1, -1, 1, -1, 0, 1)
        ALLY = "w" if self.WHITETOMOVE else "b"
        for i in range(8):
            ENDROW = ROW + ROWMOVES[i]
            ENDCOL = COL + COLMOVES[i]
            if 0 <= ENDROW <= 7 and 0 <= ENDCOL <= 7:
                ENDPIECE = self.BOARD[ENDROW][ENDCOL]
                if ENDPIECE[0] != ALLY:  #not an ally PIECE - empty or enemy
                    #place king on end SQUARE and CHECK for CHECKS
                    if ALLY == "w":
                        self.WKINGLOC = (ENDROW, ENDCOL)
                    else:
                        self.BKINGLOC = (ENDROW, ENDCOL)
                    INCHECK, PINNED, CHECKS = self.CHECKFORTHREATS()
                    if not INCHECK:
                        MOVES.append(MOVE((ROW, COL), (ENDROW, ENDCOL), self.BOARD))
                    #place king back on original location
                    if ALLY == "w":
                        self.WKINGLOC = (ROW, COL)
                    else:
                        self.BKINGLOC = (ROW, COL)

    def GETCASTLEMOVES(self, ROW, COL, MOVES):
        #valid castling moves
        if self.SQUAREUNDERATTACK(ROW, COL):
            return  #can't castle while in check
        if (self.WHITETOMOVE and self.CURRENTCASTLERIGHTS.WKS) or (
                not self.WHITETOMOVE and self.CURRENTCASTLERIGHTS.BKS):
            self.KINGSIDECASTLEMOVES(ROW, COL, MOVES)
        if (self.WHITETOMOVE and self.CURRENTCASTLERIGHTS.WQS) or (
                not self.WHITETOMOVE and self.CURRENTCASTLERIGHTS.BQS):
            self.QUEENSIDECASTLEMOVES(ROW, COL, MOVES)

    def KINGSIDECASTLEMOVES(self, ROW, COL, MOVES):
        if self.BOARD[ROW][COL + 1] == '--' and self.BOARD[ROW][COL + 2] == '--':
            if not self.SQUAREUNDERATTACK(ROW, COL + 1) and not self.SQUAREUNDERATTACK(ROW, COL + 2):
                MOVES.append(MOVE((ROW, COL), (ROW, COL + 2), self.BOARD, ISCASTLE=True))

    def QUEENSIDECASTLEMOVES(self, ROW, COL, MOVES):
        if self.BOARD[ROW][COL - 1] == '--' and self.BOARD[ROW][COL - 2] == '--' and self.BOARD[ROW][COL - 3] == '--':
            if not self.SQUAREUNDERATTACK(ROW, COL - 1) and not self.SQUAREUNDERATTACK(ROW, COL - 2):
                MOVES.append(MOVE((ROW, COL), (ROW, COL - 2), self.BOARD, ISCASTLE=True))


class CASTLERIGHTS:
    def __init__(self, WKS, BKS, WQS, BQS):
        self.WKS = WKS
        self.BKS = BKS
        self.WQS = WQS
        self.BQS = BQS


class MOVE:
    #chess dictionary to map keys to values
    RANKSTOROWS = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    ROWSTORANKS = {v: k for k, v in RANKSTOROWS.items()}
    FILESTOCOLS = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    COLSTOFILES = {v: k for k, v in FILESTOCOLS.items()}

    def __init__(self, START, END, BOARD, ENPASSANT=False, ISCASTLE=False):
        self.STARTROW = START[0]#initial selected row
        self.STARTCOL = START[1]#initial selected column
        self.ENDROW = END[0]#final selected row
        self.ENDCOL = END[1]#final selected column
        self.PIECEMOV = BOARD[self.STARTROW][self.STARTCOL]#piece moved
        self.PIECECAP = BOARD[self.ENDROW][self.ENDCOL]#piece captured

        self.ISPAWNPROMOTION = (self.PIECEMOV == "wp" and self.ENDROW == 0) or (
                self.PIECEMOV == "bp" and self.ENDROW == 7) #pawn promotion

        self.ENPASSANT = ENPASSANT        #en passant
        
        if self.ENPASSANT:
            self.PIECECAP = "wp" if self.PIECEMOV == "bp" else "bp"
      
        self.ISCASTLE = ISCASTLE #castle 
        

        self.ISCAPTURE = self.PIECECAP != "--"
        self.MOVEID = self.STARTROW * 1000 + self.STARTCOL * 100 + self.ENDROW * 10 + self.ENDCOL

    def __eq__(self, other):

        if isinstance(other, MOVE):
            return self.MOVEID == other.MOVEID
        return False

    def GETCHESSNOTATION(self):
        if self.ISPAWNPROMOTION:
            return self.GETRANKFILE(self.ENDROW, self.ENDCOL) + "Q"
        if self.ISCASTLE:
            if self.ENDCOL == 2:
                return "0-0-0" #long castle
            else:
                return "0-0" #short castle
        if self.ENPASSANT:
            return self.GETRANKFILE(self.STARTROW, self.STARTCOL)[0] + "x" + self.GETRANKFILE(self.ENDROW,
                                                                                                self.ENDCOL) + " e.p."
        if self.PIECECAP != "--":
            if self.PIECEMOV[1] == "p":
                return self.GETRANKFILE(self.STARTROW, self.STARTCOL)[0] + "x" + self.GETRANKFILE(self.ENDROW,
                                                                                                    self.ENDCOL)
            else:
                return self.PIECEMOV[1] + "x" + self.GETRANKFILE(self.ENDROW, self.ENDCOL)
        else:
            if self.PIECEMOV[1] == "p":
                return self.GETRANKFILE(self.ENDROW, self.ENDCOL)
            else:
                return self.PIECEMOV[1] + self.GETRANKFILE(self.ENDROW, self.ENDCOL)


    def GETRANKFILE(self, ROW, COL):
        return self.COLSTOFILES[COL] + self.ROWSTORANKS[ROW]

    def __str__(self):
        if self.ISCASTLE:
            return "0-0" if self.ENDCOL == 6 else "0-0-0"

        END = self.GETRANKFILE(self.ENDROW, self.ENDCOL)

        if self.PIECEMOV[1] == "p":
            if self.ISCAPTURE:
                return self.COLSTOFILES[self.STARTCOL] + "x" + END
            else:
                return END + "Q" if self.ISPAWNPROMOTION else END

        MOVESTRING = self.PIECEMOV[1]
        if self.ISCAPTURE:
            MOVESTRING += "x"
        return MOVESTRING + END