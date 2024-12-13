
#Drive file with user input and displaying the gamestate.
import pygame as g #shortcut for game cause writing pygame over and over became tedious
import ChessEngine
HEIGHT = WIDTH = 640 #pieces are 60x60
DIMENSION = 8 #board dimensions
SQ_SIZE= HEIGHT // DIMENSION #square size so it can be changed if i decide to change the size of the window so it can autochange
MAX_FPS = 15 # just in case i do animations
IMAGES = {}

def LoadImage():
    PIECES= ['wP','wR','wN','wB','wQ','wK','bP','bR','bN','bB','bK','bQ']
    for PIECE in PIECES:
        IMAGES[PIECE]=g.transform.scale(g.image.load("chess/Image/"+PIECE+".png"),(SQ_SIZE,SQ_SIZE))

#Main driver to deal with user input and graphics
def main():
    g.init()
    SCREEN= g.display.set_mode((WIDTH,HEIGHT))
    CLOCK=g.time.Clock()
    SCREEN.fill(g.Color("white"))
    GAMESTATE= ChessEngine.GAMESTATE()
    LoadImage()# only once
    RUNNING = True
    SQSELECTED=() # keeps tract  of the user's last click
    PLAYERCLICKS= [] # keeps tract of the total clicks so it can move the pieces
    VALIDMOVES = GAMESTATE.GETVALIDMOVES()
    MOVEMADE = False #flag for when a move is made
    while RUNNING:
        for i in g.event.get():
            if i.type==g.QUIT:
                RUNNING=False
            elif i.type == g.MOUSEBUTTONDOWN: # <------- START OF MOUSE HANDLING
                LOCATION = g.mouse.get_pos()
                COL = LOCATION[0]//SQ_SIZE
                ROW = LOCATION[1]//SQ_SIZE
                if SQSELECTED== (ROW,COL): #same square pick
                    SQSELECTED =() # deselecting
                    PLAYERCLICKS= []
                else:
                    SQSELECTED= (ROW,COL)
                    PLAYERCLICKS.append(SQSELECTED)
                if len(PLAYERCLICKS)==2 : #2nd click
                    MOVE = ChessEngine.MOVE(PLAYERCLICKS[0],PLAYERCLICKS[1],GAMESTATE.BOARD)
                    print (MOVE.GETCHESSNOTATION()) # debug
                    if MOVE in VALIDMOVES:
                        GAMESTATE.MAKEMOVE(MOVE)
                        MOVEMADE=True
                        SQSELECTED =() #resetting clicks
                        PLAYERCLICKS= []
                    else:
                        PLAYERCLICKS=[SQSELECTED]
            elif i.type==g.KEYDOWN:
                if i.key== g.K_BACKSPACE: #undo with backspace
                    if len(GAMESTATE.MOVELOG) != 0:
                        print("Move has been undone")
                    else:
                        print("Original Positions")
                    GAMESTATE.UNDOMOVE()
                    MOVEMADE=True
                    
        if MOVEMADE:
            VALIDMOVES =GAMESTATE.GETVALIDMOVES() # only doing after a valid move to not create the same list every frame           
            MOVEMADE=False
        DrawGameState(SCREEN,GAMESTATE)
        CLOCK.tick(MAX_FPS)
        g.display.flip()
        

#Draw the board and everything else
def DrawGameState(SCREEN,GAMESTATE): 
    DrawBoard(SCREEN)
    DrawPieces(SCREEN,GAMESTATE.BOARD)

def DrawBoard(SCREEN):
    COLORS=[(247, 203, 161),(77, 36, 0)]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            COLOR = COLORS[(i + j) % 2] 
            g.draw.rect(SCREEN, COLOR, g.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
def DrawPieces(SCREEN,BOARD):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            PIECE= BOARD[i][j]
            if PIECE != "--": #not empty
               SCREEN.blit(IMAGES[PIECE],g.Rect(j*SQ_SIZE,i*SQ_SIZE,SQ_SIZE,SQ_SIZE)) 
            
                
if __name__=="__main__":
    main()







