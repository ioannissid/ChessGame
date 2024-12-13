#Chess engine to calculate, play moves, save info and valid moves

class GAMESTATE():
    def __init__(self):
        #2d list of the board
        #pieces are based on official chess annotation
        #w=white,b=black,R=Rook,N=Knight(to avoid confusion with king),B=Bishop,Q=Queen,K=King, - = empty space
        self.BOARD = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.WHITETOMOVE = True
        self.MOVELOG=[]
        self.WKINGLOC= (7,4)
        self.BKINGLOC= (0,4)
        self.CHECKMATE= False
        self.STALEMATE= False
        
    def MAKEMOVE(self,MOVE):
        self.BOARD[MOVE.STARTROW][MOVE.STARTCOL] = "--"
        self.BOARD[MOVE.ENDROW][MOVE.ENDCOL] = MOVE.PIECEMOV
        self.MOVELOG.append(MOVE) #Log move
        self.WHITETOMOVE=not self.WHITETOMOVE #switch turns
        if MOVE.PIECEMOV == 'wK':#kings position
            self.WKINGLOC = (MOVE.ENDROW,MOVE.ENDCOL)
        if MOVE.PIECEMOV == 'bK':
            self.BKINGLOC = (MOVE.ENDROW,MOVE.ENDCOL)
    
    def UNDOMOVE(self):
        if len(self.MOVELOG) != 0:
            MOVE = self.MOVELOG.pop()
            self.BOARD[MOVE.STARTROW][MOVE.STARTCOL] = MOVE.PIECEMOV
            self.BOARD[MOVE.ENDROW][MOVE.ENDCOL] = MOVE.PIECECAP
            self.WHITETOMOVE = not self.WHITETOMOVE # switch turns back
            if MOVE.PIECEMOV == 'wK': #kings position
                self.WKINGLOC = (MOVE.STARTROW,MOVE.STARTCOL)
            if MOVE.PIECEMOV == 'bK':
                self.BKINGLOC = (MOVE.STARTROW,MOVE.STARTCOL)
                
    def GETVALIDMOVES(self):
        MOVES=self.GETPOSSIBLEMOVES()
        for i in range(len(MOVES)-1,-1,-1): # going backwards to avoid bugs after removing items and shifting them (1st -1 is to go to last element, 2nd -1 is to show the first and 3rd -1 is the increment) python handles underflow like that
            self.MAKEMOVE(MOVES[i])
            self.WHITETOMOVE = not self.WHITETOMOVE
            if self.INCHECK():
                MOVES.remove(MOVES[i])
            self.WHITETOMOVE = not self.WHITETOMOVE
            self.UNDOMOVE()
        if len(MOVES)==0:       #checking for stalemate and checkmate plus returning them to false if the move gets undone
            if self.INCHECK():
                self.CHECKMATE=True
            else:
                self.STALEMATE=True
        else:
            self.CHECKMATE=False
            self.STALEMATE=False
        return MOVES
    def INCHECK(self): #if the user is in check
        if self.WHITETOMOVE:
            return self.UNDERATTACK(self.WKINGLOC[0],self.WKINGLOC[1])
        else:
            return self.UNDERATTACK(self.BKINGLOC[0],self.BKINGLOC[1])
        
    
    def UNDERATTACK(self,i,j): #if the enemy can attack the square i,j
        self.WHITETOMOVE = not self.WHITETOMOVE #switching to opponent
        OPPMOVES = self.GETPOSSIBLEMOVES() #generate opponents move
        self.WHITETOMOVE = not self.WHITETOMOVE#switch back
        for MOVE in OPPMOVES:
            if MOVE.ENDROW == i and MOVE.ENDCOL == j: #square is under attack
                return True
        return False
        
        
    def GETPOSSIBLEMOVES(self):
        MOVES= []
        for i in range(len(self.BOARD)): #ROWS
            for j in range(len(self.BOARD[i])): #COLLUMNS
                COLOR = self.BOARD[i][j][0]
                if (COLOR=='w'and self.WHITETOMOVE) or (COLOR=='b' and not self.WHITETOMOVE):
                    PIECE = self.BOARD[i][j][1]
                    if PIECE == 'P':
                        self.GETPAWNMOVES(i,j,MOVES)
                    elif PIECE == 'R':
                        self.GETROOKMOVES(i,j,MOVES)
                    elif PIECE =="N":
                        self.GETKNIGHTMOVES(i,j,MOVES)
                    elif PIECE =="B":
                        self.GETBISHOPMOVES(i,j,MOVES)
                    elif PIECE =="Q":
                        self.GETQUEENMOVES(i,j,MOVES)
                    elif PIECE =="K":
                        self.GETKINGMOVES(i,j,MOVES)
        return MOVES
    
    
    def GETPAWNMOVES(self,i,j,MOVES):
        if self.WHITETOMOVE:
            if self.BOARD[i-1][j]== "--":#1 up
                MOVES.append(MOVE((i,j),(i-1,j),self.BOARD))
                if i==6 and self.BOARD[i-2][j]=="--":#2 up
                    MOVES.append(MOVE((i,j),(i-2,j),self.BOARD))
            if j-1>=0:#capture left
                if self.BOARD[i-1][j-1][0]=='b': #capture
                   MOVES.append(MOVE((i,j),(i-1,j-1),self.BOARD)) 
            if j+1<=7:#capture right
                if self.BOARD[i-1][j+1][0]=='b':
                    MOVES.append(MOVE((i,j),(i-1,j+1),self.BOARD))
        else:
            if self.BOARD[i+1][j]== "--":#1 down
                MOVES.append(MOVE((i,j),(i+1,j),self.BOARD))
                if i==1 and self.BOARD[i+2][j]=="--":#2 down
                    MOVES.append(MOVE((i,j),(i+2,j),self.BOARD))
            if j-1>=0:#capture left
                if self.BOARD[i+1][j-1][0]=='w': #capture
                   MOVES.append(MOVE((i,j),(i+1,j-1),self.BOARD)) 
            if j+1<=7:#capture right
                if self.BOARD[i+1][j+1][0]=='w':
                    MOVES.append(MOVE((i,j),(i+1,j+1),self.BOARD))
           
    def GETROOKMOVES(self,i,j,MOVES):
        DIRECTIONS = ((-1,0),(0,-1),(1,0),(0,1))
        if self.WHITETOMOVE:
            ENEMY='b'
        else:
            ENEMY='w'
        for x in DIRECTIONS:
            for z in range(1,8):
                ENDROW = i + x[0] * z
                ENDCOL = j + x[1] * z
                if 0 <= ENDROW < 8 and 0 <= ENDCOL <8:
                    ENDPIECE= self.BOARD[ENDROW][ENDCOL]
                    if ENDPIECE =="--":#free move
                        MOVES.append(MOVE((i,j),(ENDROW,ENDCOL),self.BOARD))
                    elif ENDPIECE[0] == ENEMY:#capture
                        MOVES.append(MOVE((i,j),(ENDROW,ENDCOL),self.BOARD))
                        break#same color piece
                else:
                    break#offboard
    
    def GETBISHOPMOVES(self,i,j,MOVES):
        DIRECTIONS = ((-1,-1),(-1,1),(1,-1),(1,1))
        if self.WHITETOMOVE:
            ENEMY='b'
        else:
            ENEMY='w'
        for x in DIRECTIONS:
            for z in range(1,8):
                ENDROW = i + x[0] * z
                ENDCOL = j + x[1] * z
                if 0 <= ENDROW < 8 and 0 <= ENDCOL <8:
                    ENDPIECE= self.BOARD[ENDROW][ENDCOL]
                    if ENDPIECE =="--":#free move
                        MOVES.append(MOVE((i,j),(ENDROW,ENDCOL),self.BOARD))
                    elif ENDPIECE[0] == ENEMY:#capture
                        MOVES.append(MOVE((i,j),(ENDROW,ENDCOL),self.BOARD))
                        break#same color piece
                else:
                    break#offboard
    
    def GETQUEENMOVES(self,i,j,MOVES):
        DIRECTIONS = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,+1),(1,-1),(1,0),(1,1))
        if self.WHITETOMOVE:
            ENEMY='b'
        else:
            ENEMY='w'
        for x in DIRECTIONS:
            for z in range(1,8):
                ENDROW = i + x[0] * z
                ENDCOL = j + x[1] * z
                if 0 <= ENDROW < 8 and 0 <= ENDCOL <8:
                    ENDPIECE= self.BOARD[ENDROW][ENDCOL]
                    if ENDPIECE =="--":#free move
                        MOVES.append(MOVE((i,j),(ENDROW,ENDCOL),self.BOARD))
                    elif ENDPIECE[0] == ENEMY:#capture
                        MOVES.append(MOVE((i,j),(ENDROW,ENDCOL),self.BOARD))
                        break#same color piece
                else:
                    break#offboard
    
    def GETKINGMOVES(self,i,j,MOVES):
        DIRECTIONS = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,+1),(1,-1),(1,0),(1,1))
        if self.WHITETOMOVE:
            ENEMY='b'
        else:
            ENEMY='w'
        for x in DIRECTIONS:
                ENDROW = i + x[0] 
                ENDCOL = j + x[1] 
                if 0 <= ENDROW < 8 and 0 <= ENDCOL <8:
                    ENDPIECE= self.BOARD[ENDROW][ENDCOL]
                    if ENDPIECE =="--":#free move
                        MOVES.append(MOVE((i,j),(ENDROW,ENDCOL),self.BOARD))
                    elif ENDPIECE[0] == ENEMY:#capture
                        MOVES.append(MOVE((i,j),(ENDROW,ENDCOL),self.BOARD))
  
        
    def GETKNIGHTMOVES(self,i,j,MOVES):
        DIRECTIONS = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        if self.WHITETOMOVE:
            ALLY='w'
        else:
            ALLY='b'
        for x in DIRECTIONS:
                ENDROW = i + x[0] 
                ENDCOL = j + x[1] 
                if 0 <= ENDROW < 8 and 0 <= ENDCOL <8:
                    ENDPIECE= self.BOARD[ENDROW][ENDCOL]
                    if ENDPIECE != ALLY:
                        MOVES.append(MOVE((i,j),(ENDROW,ENDCOL),self.BOARD))

                    
        
    
class MOVE(): 
    #chess dictionary to map keys to values
    RANKSTOROWS= {"1" : 7, "2":6, "3":5, "4":4,"5":3,"6":2,"7":1,"8":0}
    ROWSTORANKS= {i: j for j, i in RANKSTOROWS.items()}
    FILESTOCOLS={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    COLSTOFILES={i:j for j, i in FILESTOCOLS.items()}
    def __init__(self,START,END,BOARD): #starting square ,ending square and board state
        self.STARTROW= START[0] #initial selected row
        self.STARTCOL= START[1] #initial selected collumn
        self.ENDROW= END[0] #last selected row
        self.ENDCOL= END[1] #last selected collumn
        self.PIECEMOV =BOARD[self.STARTROW][self.STARTCOL]#piece moved
        self.PIECECAP= BOARD[self.ENDROW][self.ENDCOL]#piece captured
        self.MOVEID= self.STARTROW * 1000 + self.STARTCOL *100 + self.ENDROW*10+self.ENDCOL #unique
        #print(self.MOVEID) #debug
        
    def __eq__(self,OTHER):
        if isinstance(OTHER,MOVE):
            return self.MOVEID == OTHER.MOVEID
        return False
    def GETCHESSNOTATION(self):
       return self.GETRANKFILE(self.STARTROW,self.STARTCOL) + self.GETRANKFILE(self.ENDROW,self.ENDCOL)
        
    def GETRANKFILE(self,RANK,COL):
        return self.COLSTOFILES[COL]+self.ROWSTORANKS[RANK]