#Chess engine to calculate, play moves, save info and valid moves
class GAMESTATE():
    def __init__(self):
        #2d list of the board
        #pieces are based on official chess annotation
        #w=white,b=black,R=Rook,N=Knight(to avoid confusion with king),B=Bishop,Q=Queen,K=King, - = empty space
        self.BOARD = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["-","-","-","-","-","-","-","-","-",],
            ["-","-","-","-","-","-","-","-","-",],
            ["-","-","-","-","-","-","-","-","-",],
            ["-","-","-","-","-","-","-","-","-",],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.WHITETOMOVE = True
        self.MOVELOG=[]
        
    def MAKEMOVE(self,MOVE):
        self.BOARD[MOVE.STARTROW][MOVE.STARTCOL] = "-"
        self.BOARD[MOVE.ENDROW][MOVE.ENDCOL] = MOVE.PIECEMOV
        self.MOVELOG.append(MOVE) #Log move
        self.WHITETOMOVE=not self.WHITETOMOVE #switch turns
        
class MOVE(): 
    #chess dictionary to map keys to values
    RANKSTOROWS= {"1" : 7, "2":6, "3":5, "4":4,
                  "5":3,"6":2,"7":1,"8":0}
    ROWSTORANKS= {i: j for j, i in RANKSTOROWS.items()}
    FILESTOCOLS={"a":0,"b":1,"c":2,"d":3,
                 "e":4,"f":5,"g":6,"h":7}
    COLSTOFILES={i:j for j, i in FILESTOCOLS.items()}
    def __init__(self,START,END,BOARD): #starting square ,ending square and board state
        self.STARTROW= START[0] #initial selected row
        self.STARTCOL= START[1] #initial selected collumn
        self.ENDROW= END[0] #last selected row
        self.ENDCOL= END[1] #last selected collumn
        self.PIECEMOV =BOARD[self.STARTROW][self.STARTCOL]#piece moved
        self.PIECECAP= BOARD[self.ENDROW][self.ENDCOL]#piece captured

    def GETCHESSNOTATION(self):
       return self.GETRANKFILE(self.STARTROW,self.STARTCOL) + self.GETRANKFILE(self.ENDROW,self.ENDCOL)
        
    def GETRANKFILE(self,RANK,COL):
        return self.COLSTOFILES[COL]+self.ROWSTORANKS[RANK]