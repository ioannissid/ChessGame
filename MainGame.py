#Drive file with user input and displaying the gamestate.
import pygame as G #shortcut for game cause writing pygame over and over became tedious
import ChessEngine
WIDTH = HEIGHT = 640 #pieces are 60x60
DIMENSION = 8 #board dimensions
SQ_SIZE= HEIGHT // DIMENSION #square size so it can be changed if i decide to change the size of the window so it can autochange
MAX_FPS = 15 # just in case i do animations
IMAGES = {}

def loadImage():
    PIECES = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for PIECE in PIECES:
        IMAGES[PIECE] = G.transform.scale(G.image.load("ChessGame/Chess/Image/" + PIECE + ".png"), (SQ_SIZE, SQ_SIZE))
#main driver to deal with user input and graphics
def main():
    G.init()
    SCREEN = G.display.set_mode((WIDTH , HEIGHT))
    CLOCK = G.time.Clock()
    SCREEN.fill(G.Color("white"))
    GAMESTATE = ChessEngine.GAMESTATE()
    VALIDMOVES = GAMESTATE.GETVALIDMOVES()
    MOVEMADE = False  #flag for when a move is made
    loadImage()  #so it happens only once
    RUNNING = True
    SQSELECTED = ()  # keeps tract  of the user's last click wit h no square initially
    PLAYERCLICKS = [] #keeps track of player clicks (2 clicks)
    while RUNNING:
        for I in G.event.get():
            if I.type == G.QUIT:
                RUNNING = False
            elif I.type == G.MOUSEBUTTONDOWN: # <------- START OF MOUSE HANDLING
                LOCATION = G.mouse.get_pos() 
                COL = LOCATION[0] // SQ_SIZE
                ROW = LOCATION[1] // SQ_SIZE
                if SQSELECTED == (ROW, COL) or COL >= 8:  #same square pick
                    SQSELECTED = ()  #deselecting
                    PLAYERCLICKS = []  #clear clicks
                else:
                    SQSELECTED = (ROW, COL)
                    PLAYERCLICKS.append(SQSELECTED)  # append for both 1st and 2nd click
                if len(PLAYERCLICKS) == 2:
                    MOVE = ChessEngine.MOVE(PLAYERCLICKS[0], PLAYERCLICKS[1], GAMESTATE.BOARD)
                    for i in range(len(VALIDMOVES)):
                        if MOVE == VALIDMOVES[i]:
                            GAMESTATE.MAKEMOVE(VALIDMOVES[i])
                            MOVEMADE = True
                            SQSELECTED = ()  #reset user clicks
                            PLAYERCLICKS = []
                    if not MOVEMADE:
                        PLAYERCLICKS = [SQSELECTED]
                        
                        
                        
                        
            elif I.type==G.KEYDOWN:
                if I.key== G.K_BACKSPACE: #undo with backspace
                    if len(GAMESTATE.MOVELOG) != 0:
                        print("MOVE has been undone")
                    else:
                        print("Original Positions")
                    GAMESTATE.UNDOMOVE()
                    MOVEMADE=True
                    
        if MOVEMADE:
            VALIDMOVES = GAMESTATE.GETVALIDMOVES()
            MOVEMADE = False
        DrawGameState(SCREEN,GAMESTATE)
        CLOCK.tick(MAX_FPS)
        G.display.flip()
        

#Draw the BOARD and everything else
def DrawGameState(SCREEN,GAMESTATE): 
    DrawBoard(SCREEN)
    DrawPieces(SCREEN,GAMESTATE.BOARD)

def DrawBoard(SCREEN):
    COLORS=[(247, 203, 161),(77, 36, 0)]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = COLORS[(i + j) % 2] 
            G.draw.rect(SCREEN, color, G.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
def DrawPieces(SCREEN,BOARD):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            PIECE= BOARD[i][j]
            if PIECE != "--": #not empty
                SCREEN.blit(IMAGES[PIECE], G.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
                
if __name__=="__main__":
    main()