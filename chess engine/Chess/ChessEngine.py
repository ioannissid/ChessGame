#Chess engine to calculate, play moves, save info and valid moves
class GameState():
    def __init__(self):
        #2d list of the board
        #pieces are based on official chess annotation
        #w=white,b=black,R=Rook,N=Knight(to avoid confusion with king),B=Bishop,Q=Queen,K=King, - = empty space
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["-","-","-","-","-","-","-","-","-",],
            ["-","-","-","-","-","-","-","-","-",],
            ["-","-","-","-","-","-","-","-","-",],
            ["-","-","-","-","-","-","-","-","-",],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.whiteToMove = True
        self.moveLog=[]