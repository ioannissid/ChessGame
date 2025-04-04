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
            ["wR","--","--","--","wK","--","--","wR"]]
        self.WHITETOMOVE = True
        self.MOVELOG=[]
        self.WKINGLOC= (7,4)
        self.BKINGLOC= (0,4)
        self.CHECKMATE= False
        self.STALEMATE= False
        self.INCHECK=False
        self.PINNED=[]
        self.CHECKS=[]
        self.ENPASSANTPOSSIBLE=() #coordinates for enpassant possible capture
        self.PAWNPROMOTION=False
        self.CURRENTCASTLERIGHTS=CASTLERIGHTS(True,True,True,True) #checks if the pawns have moved
        self.CASTLERIGHTSLOG=[CASTLERIGHTS(self.CURRENTCASTLERIGHTS.WKS,self.CURRENTCASTLERIGHTS.BKS,self.CURRENTCASTLERIGHTS.WQS,self.CURRENTCASTLERIGHTS.BQS)] #log of castlerights
        
        
    def MAKEMOVE(self,MOVE,PROMOTEDPIECE=None):
        self.BOARD[MOVE.STARTROW][MOVE.STARTCOL] = "--"
        self.BOARD[MOVE.ENDROW][MOVE.ENDCOL] = MOVE.PIECEMOV
        self.MOVELOG.append(MOVE) #Log move
        self.WHITETOMOVE=not self.WHITETOMOVE #switch turns
        if MOVE.PIECEMOV == 'wK':#kings position
            self.WKINGLOC = (MOVE.ENDROW,MOVE.ENDCOL)
        if MOVE.PIECEMOV == 'bK':
            self.BKINGLOC = (MOVE.ENDROW,MOVE.ENDCOL)
        if MOVE.PIECEMOV[1]=='P' and abs(MOVE.STARTROW-MOVE.ENDROW)==2:
            self.ENPASSANTPOSSIBLE=((MOVE.ENDROW+MOVE.STARTROW)//2,MOVE.ENDCOL)
        else:
            self.ENPASSANTPOSSIBLE=()
            
        if MOVE.ENPASSANT:
            self.BOARD[MOVE.STARTROW][MOVE.ENDCOL] ="--"
        
        if MOVE.PAWNPROMOTION:
            if PROMOTEDPIECE is None:
                PROMOTEDPIECE = 'Q'  # Default to Queen if no choice is made
            self.BOARD[MOVE.ENDROW][MOVE.ENDCOL] = MOVE.PIECEMOV[0] + PROMOTEDPIECE        

        if MOVE.ISCASTLE:
            self.BOARD[7,7] = "--"


#updating castle rights 
        self.UPDATECASTLERIGHTS(MOVE)
        self.CASTLERIGHTSLOG.append(CASTLERIGHTS(self.CURRENTCASTLERIGHTS.WKS,self.CURRENTCASTLERIGHTS.BKS,self.CURRENTCASTLERIGHTS.WQS,self.CURRENTCASTLERIGHTS.BQS)) #log of castlerights

        
        
        
   
   
   
   
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
            
            if MOVE.ENPASSANT:
                self.BOARD[MOVE.ENDROW][MOVE.ENDCOL] = '--' #leave the captured square blank
                self.BOARD[MOVE.STARTROW][MOVE.ENDCOL]=MOVE.PIECECAP
                self.ENPASSANTPOSSIBLE=(MOVE.ENDROW, MOVE.ENDCOL) # to be able to do it again after undo
             
            if MOVE.PIECEMOV[1] == 'P' and abs(MOVE.STARTROW - MOVE.ENDROW) == 2:
                self.ENPASSANTPOSSIBLE= ()
            
            self.CASTLERIGHTSLOG.pop() #removing the new castle rights from the move that is being undone
            self.CURRENTCASTLERIGHTS = self.CASTLERIGHTSLOG[-1]#setting the castle rights to the last one in the log 
            if MOVE.ISCASTLE:
                if MOVE.ENDCOL - MOVE.STARTCOL == 2:
                    self.BOARD[MOVE.ENDROW][7] = self.BOARD[MOVE.ENDROW][MOVE.ENDCOL-1]#undoing the rook
                    self.BOARD[MOVE.ENDROW][MOVE.ENDCOL-1] = "--" #delete old rook
                else:
                    self.BOARD[MOVE.ENDROW][0] = self.BOARD[MOVE.ENDROW][MOVE.ENDCOL+1]
                    self.BOARD[MOVE.ENDROW][MOVE.ENDCOL+1] = "--" #delete old rook
            
             
    def UPDATECASTLERIGHTS(self,MOVE):#update the castle rigts after it takes the move
        if MOVE.PIECECAP == 'wR':
            if MOVE.ENDCOL == 0:
                self.CURRENTCASTLERIGHTS.WQS = False
            elif MOVE.ENDCOL == 7:
                self.CURRENTCASTLERIGHTS.WKS = False
        if MOVE.PIECECAP == 'bR':
            if MOVE.ENDCOL == 0:
                self.CURRENTCASTLERIGHTS.BQS = False
            elif MOVE.ENDCOL == 7:
                self.CURRENTCASTLERIGHTS.BKS = False
        
        
        if MOVE.PIECEMOV == 'wK':
            self.CURRENTCASTLERIGHTS.WKS = False
            self.CURRENTCASTLERIGHTS.WQS = False
        elif MOVE.PIECEMOV == 'bK':
            self.CURRENTCASTLERIGHTS.BKS = False
            self.CURRENTCASTLERIGHTS.BQS = False
        elif MOVE.PIECEMOV == 'wR':
            if MOVE.STARTROW == 7:
                if MOVE.STARTCOL == 0:
                    self.CURRENTCASTLERIGHTS.WQS = False
                elif MOVE.STARTCOL == 7:
                    self.CURRENTCASTLERIGHTS.WKS = False
        elif MOVE.PIECEMOV == 'bR': 
                if MOVE.STARTROW == 0:
                    if MOVE.STARTCOL == 0:
                        self.CURRENTCASTLERIGHTS.BQS = False
                    elif MOVE.STARTCOL == 7:
                         self.CURRENTCASTLERIGHTS.BKS = False
                     
                    
                    
                    
    def GETVALIDMOVES(self):
      
        TEMPCASTLERIGHTS= CASTLERIGHTS(self.CURRENTCASTLERIGHTS.WKS,self.CURRENTCASTLERIGHTS.WQS,self.CURRENTCASTLERIGHTS.BKS,self.CURRENTCASTLERIGHTS.BQS)
        MOVES=[]
        self.INCHECK,self.PINNED,self.CHECKS = self.CHECKFORTHREATS() 
        
        if self.WHITETOMOVE:
            KROW=self.WKINGLOC[0]
            KCOL=self.WKINGLOC[1]
        else:
            KROW=self.BKINGLOC[0]
            KCOL=self.BKINGLOC[1]
        if self.INCHECK:
            if len(self.CHECKS)==1 :# only one check
                MOVES=self.GETPOSSIBLEMOVES()
                CHECK=self.CHECKS[0] #check info
                CHECKROW=CHECK[0]
                CHECKCOL=CHECK[1]
                PIECECHECK=self.BOARD[CHECKROW][CHECKCOL]
                VALIDS=[]
                if PIECECHECK[1]=='N':
                    VALID = [(CHECKROW,CHECKCOL)]
                else:  #squares between the king and attacker or the square of the attacker
                    for i in range (1,8):
                        VALID = (KROW+CHECK[2]* i, KCOL+CHECK[3]*i)
                        VALIDS.append(VALID)
                        if VALID[0] == CHECKROW and VALID[1]==CHECKCOL: #break cause we reached the threat
                            break
                for i in range(len(MOVES)-1,-1,-1):
                    if MOVES[i].PIECEMOV[1]!='K': #move doesnt move the king so it must block or capture
                        if not (MOVES[i].ENDROW,MOVES[i].ENDCOL) in VALIDS:
                            MOVES.remove(MOVES[i])
            else:
                self.GETKINGMOVES(KROW,KCOL,MOVES)
        else:
            MOVES = self.GETPOSSIBLEMOVES()                          
            if self.WHITETOMOVE:
                self.GETCASTLEMOVES(self.WKINGLOC[0],self.WKINGLOC[1],MOVES)
            else:
                self.GETCASTLEMOVES(self.BKINGLOC[0],self.BKINGLOC[1],MOVES)
        
        
        if len(MOVES) == 0:
            if self.INCHECK:
                self.CHECKMATE = True
            else:
                self.STALEMATE = True
        else:
            self.CHECKMATE = False
            self.STALEMATE = False
        self.CURRENTCASTLERIGHTS=TEMPCASTLERIGHTS
        return MOVES
    
    
    
    def CHECKFORTHREATS(self):
        PINNED =[]
        CHECKS=[]
        INCHECK=False
        if self.WHITETOMOVE:
            ENEMY="b"
            ALLY="w"
            STARTROW=self.WKINGLOC[0]
            STARTCOL=self.WKINGLOC[1]
        else:
            ENEMY="w"
            ALLY="b"
            STARTROW=self.BKINGLOC[0]
            STARTCOL=self.BKINGLOC[1]
        DIRECTIONS =((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)) #check from the king for pins and checks
        for i in range(len(DIRECTIONS)):
            DIR=DIRECTIONS[i]
            POSPIN=() #possible pin
            for j in range(1,8):#squares away
                ENDROW = STARTROW + DIR[0] * j
                ENDCOL = STARTCOL + DIR[1] * j
                if 0 <= ENDROW < 8 and 0 <= ENDCOL <8:
                    ENDPIECE= self.BOARD[ENDROW][ENDCOL]
                    if ENDPIECE[0] == ALLY and ENDPIECE[1]!='K': #checking if the ally is pinned
                        if POSPIN == ():
                            POSPIN = (ENDROW,ENDCOL,DIR[0],DIR[1])
                        else: # if the ally has another ally behind him
                            break
                    elif ENDPIECE[0]==ENEMY:
                        TYPE = ENDPIECE[1] #so i can check depending on piece for its type of pin
                        if (0 <= i <= 3 and TYPE == "R") or (4 <= i <= 7 and TYPE == "B") or (j == 1 and TYPE == "p" and ((TYPE == "w" and 6 <= i <= 7) or (TYPE == "b" and 4 <= i <= 5))) or (TYPE == "Q") or (j == 1 and TYPE == "K"):
                            if POSPIN == (): #if pospin == empty then that means there are no pieces in between so its a check
                                INCHECK=True
                                CHECKS.append((ENDROW,ENDCOL,DIR[0],DIR[1]))
                                break
                            else: #piece is blocking
                                PINNED.append(POSPIN)
                                break
                        else: #enemy not a threat 
                            break
                else:
                    break #out of bounds
        KDIRECTIONS = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)) #knight directions cause they dont really have common moveset with the rest of the pieces  
        for y in KDIRECTIONS:
            ENDROW = STARTROW + y[0] 
            ENDCOL = STARTCOL + y[1] 
            if 0 <= ENDROW < 8 and 0 <= ENDCOL <8:
                ENDPIECE= self.BOARD[ENDROW][ENDCOL]
                if ENDPIECE[0]==ENEMY and ENDPIECE[1] =='N':
                    INCHECK=True
                    CHECKS.append((ENDROW,ENDCOL,y[0],y[1]))
        return INCHECK,PINNED,CHECKS
    
    
    def SQUAREUNDERATTACK(self,ROW,COL):
        self.WHITETOMOVE = not self.WHITETOMOVE #switch to check if enemy can attack those squares
        ENEMYMOVES = self.GETPOSSIBLEMOVES()
        self.WHITETOMOVE = not self.WHITETOMOVE #switch turns back
        for MOVE in ENEMYMOVES:
            if MOVE.ENDROW == ROW and MOVE.ENDCOL == COL:
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
    
    
    def GETPAWNMOVES(self, i, j, MOVES):
        PINNED = False
        PINDIR = ()  # pin direction
        for x in range(len(self.PINNED) - 1, -1, -1):
            if self.PINNED[x][0] == i and self.PINNED[x][1] == j:
                PINNED = True
                PINDIR = (self.PINNED[x][2], self.PINNED[x][3])
                self.PINNED.remove(self.PINNED[x])
            break
        if self.WHITETOMOVE:
            MOVEAMOUNT = -1
            STARTROW = 6
            BACKROW = 0
            ENEMY = 'b'
        else:
            MOVEAMOUNT = 1
            STARTROW = 1
            BACKROW = 7
            ENEMY = 'w'
        PAWNPROMOTION = False

        if self.BOARD[i + MOVEAMOUNT][j] == "--":  # 1 square
            if not PINNED or PINDIR == (MOVEAMOUNT, 0):
                if i + MOVEAMOUNT == BACKROW:
                    PAWNPROMOTION = True
                MOVES.append(MOVE((i, j), (i + MOVEAMOUNT, j), self.BOARD, PAWNPROMOTION=PAWNPROMOTION))
                if i == STARTROW and self.BOARD[i + 2 * MOVEAMOUNT][j] == "--":  # 2 square
                    MOVES.append(MOVE((i, j), (i + 2 * MOVEAMOUNT, j), self.BOARD))

        if j - 1 >= 0:  # left capture
            if not PINNED or PINDIR == (MOVEAMOUNT, -1):
                if self.BOARD[i + MOVEAMOUNT][j - 1][0] == ENEMY:
                    if i + MOVEAMOUNT == BACKROW:  # backrank with capture
                        PAWNPROMOTION = True
                    MOVES.append(MOVE((i, j), (i + MOVEAMOUNT, j - 1), self.BOARD, PAWNPROMOTION=PAWNPROMOTION))
                if (i + MOVEAMOUNT, j - 1) == self.ENPASSANTPOSSIBLE:
                    MOVES.append(MOVE((i, j), (i + MOVEAMOUNT, j - 1), self.BOARD, ENPASSANT=True))

        if j + 1 <= 7:  # right capture
            if not PINNED or PINDIR == (MOVEAMOUNT, 1):
                if self.BOARD[i + MOVEAMOUNT][j + 1][0] == ENEMY:
                    if i + MOVEAMOUNT == BACKROW:  # backrank with capture
                        PAWNPROMOTION = True
                    MOVES.append(MOVE((i, j), (i + MOVEAMOUNT, j + 1), self.BOARD, PAWNPROMOTION=PAWNPROMOTION))
                if (i + MOVEAMOUNT, j + 1) == self.ENPASSANTPOSSIBLE:
                    MOVES.append(MOVE((i, j), (i + MOVEAMOUNT, j + 1), self.BOARD, ENPASSANT=True))

        
        
        
        
    def GETROOKMOVES(self,i,j,MOVES):
        PINNED=False
        PINDIR=() #pin direction
        for x in range (len(self.PINNED)-1,-1,-1):
            if self.PINNED[x][0]==i and self.PINNED[x][1]==j:
                PINNED=True
                PINDIR=(self.PINNED[x][2],self.PINNED[x][3])
                self.PINNED.remove(self.PINNED[x])
            break
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
                    if not PINNED or PINDIR==x or PINDIR==(-x[0],-x[1]): # move towards or away but still in pin line
                        ENDPIECE= self.BOARD[ENDROW][ENDCOL]
                        if ENDPIECE =="--":#free move
                            MOVES.append(MOVE((i,j),(ENDROW,ENDCOL),self.BOARD))
                        elif ENDPIECE[0] == ENEMY:#capture
                            MOVES.append(MOVE((i,j),(ENDROW,ENDCOL),self.BOARD))
                            break
                        else:
                            break #same color
                else:
                    break#offboard
                
    
    def GETBISHOPMOVES(self,i,j,MOVES):
        PINNED=False
        PINDIR=() #pin direction
        for x in range (len(self.PINNED)-1,-1,-1):
            if self.PINNED[x][0]==i and self.PINNED[x][1]==j:
                PINNED=True
                PINDIR=(self.PINNED[x][2],self.PINNED[x][3])
                self.PINNED.remove(self.PINNED[x])
            break
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
                    if not PINNED or PINDIR==x or PINDIR==(-x[0],-x[1]): # move towards or away but still in pin line
                        ENDPIECE= self.BOARD[ENDROW][ENDCOL]
                        if ENDPIECE =="--":#free move
                            MOVES.append(MOVE((i,j),(ENDROW,ENDCOL),self.BOARD))
                        elif ENDPIECE[0] == ENEMY:#capture
                            MOVES.append(MOVE((i,j),(ENDROW,ENDCOL),self.BOARD))
                            break
                        else:
                            break #same color
                else:
                    break#offboard
                   
                    
    def GETQUEENMOVES(self,i,j,MOVES):
        PINNED=False
        PINDIR=() #pin direction
        for x in range (len(self.PINNED)-1,-1,-1):
            if self.PINNED[x][0]==i and self.PINNED[x][1]==j:
                PINNED=True
                PINDIR=(self.PINNED[x][2],self.PINNED[x][3])
                self.PINNED.remove(self.PINNED[x])
            break
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
                    if not PINNED or PINDIR==x or PINDIR==(-x[0],-x[1]): # move towards or away but still in pin line
                        ENDPIECE= self.BOARD[ENDROW][ENDCOL]
                        if ENDPIECE =="--":#free move
                            MOVES.append(MOVE((i,j),(ENDROW,ENDCOL),self.BOARD))
                        elif ENDPIECE[0] == ENEMY:#capture
                            MOVES.append(MOVE((i,j),(ENDROW,ENDCOL),self.BOARD))
                            break
                        else:
                            break #same color
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
                    if ENDPIECE =="--" or ENDPIECE[0] == ENEMY:#free move
                        if ENEMY=='b': #placing the king in the end location to check for checks
                            self.WKINGLOC=(ENDROW,ENDCOL)
                        else:
                            self.BKINGLOC=(ENDROW,ENDCOL)
                        INCHECK,PINNED,CHECKS=self.CHECKFORTHREATS() #using only INCHECK cause king cant be pinned and having 3 vars because thats how many return
                        if not INCHECK:
                            MOVES.append(MOVE((i,j),(ENDROW,ENDCOL),self.BOARD))
                        if ENEMY=='b':
                            self.WKINGLOC=(i,j)
                        else:
                            self.BKINGLOC=(i,j)
        
    def GETKNIGHTMOVES(self,i,j,MOVES):
        PINNED=False #no need for directions since knights moves dont overlap with spaces it can get pinned
        for x in range (len(self.PINNED)-1,-1,-1):
            if self.PINNED[x][0]==i and self.PINNED[x][1]==j:
                PINNED=True
                self.PINNED.remove(self.PINNED[x])
            break
        DIRECTIONS = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        if self.WHITETOMOVE:
            ALLY='w'
        else:
            ALLY='b'
        for x in DIRECTIONS:
                ENDROW = i + x[0] 
                ENDCOL = j + x[1] 
                if 0 <= ENDROW < 8 and 0 <= ENDCOL <8:
                    if not PINNED:
                        ENDPIECE= self.BOARD[ENDROW][ENDCOL]
                        if ENDPIECE != ALLY:
                            MOVES.append(MOVE((i,j),(ENDROW,ENDCOL),self.BOARD))

                    
    def GETCASTLEMOVES(self,i,j,MOVES):#castle moves                    
        if self.SQUAREUNDERATTACK(i,j):
            return #cant castle while in check
        if (self.WHITETOMOVE and self.CURRENTCASTLERIGHTS.WKS) or (not self.WHITETOMOVE and self.CURRENTCASTLERIGHTS.BKS):  
            self.KINGSIDECASTLEMOVES(i,j,MOVES)
        if (self.WHITETOMOVE and self.CURRENTCASTLERIGHTS.WQS) or (not self.WHITETOMOVE and self.CURRENTCASTLERIGHTS.BQS):
            self.QUEENSIDECASTLEMOVES(i,j,MOVES)
        
        
        
        
    def KINGSIDECASTLEMOVES(self,i,j,MOVES):              
        if self.BOARD[i][j+1] == "--" and self.BOARD[i][j+2] == "--":
            if not self.SQUAREUNDERATTACK(i,j+1) and not self.SQUAREUNDERATTACK(i,j+2):
                MOVES.append(MOVE((i,j),(i,j+2),self.BOARD, ISCASTLE=True))


    def QUEENSIDECASTLEMOVES(self,i,j,MOVES):
        if self.BOARD[i][j-1] == "--" and self.BOARD[i][j-2] == "--" and self.BOARD[i][j-3] == "--":
            if not self.SQUAREUNDERATTACK(i,j-1) and not self.SQUAREUNDERATTACK(i,j-2):
                MOVES.append(MOVE((i,j),(i,j-2),self.BOARD, ISCASTLE=True))
                    
class CASTLERIGHTS(): 
    def __init__(self,WKS,WQS,BKS,BQS):
        self.WKS=WKS
        self.WQS=WQS
        self.BKS=BKS
        self.BQS=BQS     
    
class MOVE(): 
    #chess dictionary to map keys to values
    RANKSTOROWS= {"1" : 7, "2":6, "3":5, "4":4,"5":3,"6":2,"7":1,"8":0}
    ROWSTORANKS= {i: j for j, i in RANKSTOROWS.items()}
    FILESTOCOLS={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    COLSTOFILES={i:j for j, i in FILESTOCOLS.items()}
    def __init__(self,START,END,BOARD,PAWNPROMOTION=False, ENPASSANT=False, ISCASTLE=False): #starting square ,ending square and board state and an optional parameter that changes depending on if its given value or not
        self.STARTROW= START[0] #initial selected row
        self.STARTCOL= START[1] #initial selected collumn
        self.ENDROW= END[0] #last selected row
        self.ENDCOL= END[1] #last selected collumn
        self.PIECEMOV =BOARD[self.STARTROW][self.STARTCOL]#piece moved
        self.PIECECAP= BOARD[self.ENDROW][self.ENDCOL]#piece captured
        self.PAWNPROMOTION = PAWNPROMOTION #doing it here to avoid writing it in 6 spots
           
        self.ENPASSANT=ENPASSANT
        if self.ENPASSANT:
            self.PIECECAP= 'bP' if self.PIECEMOV=='wP' else 'wP'
        
        self.MOVEID= self.STARTROW * 1000 + self.STARTCOL *100 + self.ENDROW*10+self.ENDCOL #unique
        self.ISCASTLE=ISCASTLE
        
        
    def __eq__(self,OTHER):
        if isinstance(OTHER,MOVE):
            return self.MOVEID == OTHER.MOVEID
        return False
    def GETCHESSNOTATION(self):
       return self.GETRANKFILE(self.STARTROW,self.STARTCOL) + self.GETRANKFILE(self.ENDROW,self.ENDCOL)
        
    def GETRANKFILE(self,RANK,COL):
        return self.COLSTOFILES[COL]+self.ROWSTORANKS[RANK]
    def IsPawnPromotion(self):  # ADD THIS METHOD
        if self.PIECEMOV[1] == 'P':  # It's a pawn move
            if (self.PIECEMOV[0] == 'w' and self.ENDROW == 0) or \
               (self.PIECEMOV[0] == 'b' and self.ENDROW == 7):  # Reached back rank
                return True
        return False