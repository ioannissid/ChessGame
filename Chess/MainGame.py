#Drive file with user input and displaying the gamestate.
import pygame as G #shortcut for game cause writing pygame over and over became tedious
import ChessEngine
HEIGHT = WIDTH = 640 #pieces are 60x60
DIMENSION = 8 #board dimensions
SQ_SIZE= HEIGHT // DIMENSION #square size so it can be changed if i decide to change the size of the window so it can autochange
MAX_FPS = 15 # just in case i do animations
IMAGES = {}

def LoadImage():
    PIECES= ['wP','wR','wN','wB','wQ','wK','bP','bR','bN','bB','bK','bQ']
    for PIECE in PIECES:
        IMAGES[PIECE]=G.transform.scale(G.image.load("Chess/Image/"+PIECE+".png"),(SQ_SIZE,SQ_SIZE))


def GET_PROMOTION_CHOICE(SCREEN, COLOR):    #Displays promotion choices as images and returns the chosen piece.

    CHOICES = ['Q', 'R', 'B', 'N']
    RECTS = []
    BUTTON_WIDTH = SQ_SIZE  # Use square size for button width
    BUTTON_HEIGHT = SQ_SIZE  # Use square size for button height
    START_X = WIDTH // 2 - (BUTTON_WIDTH * len(CHOICES)) // 2
    START_Y = HEIGHT // 2

    for I, CHOICE in enumerate(CHOICES):
        X = START_X + I * BUTTON_WIDTH
        Y = START_Y
        RECT = G.Rect(X, Y, BUTTON_WIDTH, BUTTON_HEIGHT)
        RECTS.append(RECT)

    while True:
        for EVENT in G.event.get():
            if EVENT.type == G.QUIT:
                G.quit()
                exit()
            if EVENT.type == G.MOUSEBUTTONDOWN:
                for I, RECT in enumerate(RECTS):
                    if RECT.collidepoint(EVENT.pos):
                        return CHOICES[I]  # Return the chosen piece

        # Draw the promotion choices
        G.draw.rect(SCREEN, (255, 255, 255), (START_X - 10, START_Y - 10, BUTTON_WIDTH * len(CHOICES) + 20, BUTTON_HEIGHT + 20))  # Clear area
        for I, CHOICE in enumerate(CHOICES):
            G.draw.rect(SCREEN, (200, 200, 200), RECTS[I])  # Button background
            PIECE_IMAGE = IMAGES[COLOR + CHOICE]  # Get the piece image
            SCREEN.blit(PIECE_IMAGE, RECTS[I])  # Blit the image onto the button

        G.display.flip()

def GET_AI_PROMOTION_CHOICE(GAMESTATE, MOVE):

    # This is a placeholder for a more sophisticated AI.

    return 'Q'

#Main driver to deal with user input and graphics
def main():
    G.init()
    SCREEN= G.display.set_mode((WIDTH,HEIGHT))
    CLOCK=G.time.Clock()
    SCREEN.fill(G.Color("white"))
    GAMESTATE= ChessEngine.GAMESTATE()
    LoadImage()# only once
    RUNNING = True
    SQSELECTED=() # keeps tract  of the user's last click
    PLAYERCLICKS= [] # keeps tract of the total clicks so it can move the pieces
    VALIDMOVES = GAMESTATE.GETVALIDMOVES()
    MOVEMADE = False #flag for when a move is made
    HUMANPLAYSWHITE = True  # Or False, depending on your game setup

    while RUNNING:
        for I in G.event.get():
            if I.type==G.QUIT:
                RUNNING=False
            elif I.type == G.MOUSEBUTTONDOWN: # <------- START OF MOUSE HANDLING
                LOCATION = G.mouse.get_pos()
                COL = LOCATION[0]//SQ_SIZE
                ROW = LOCATION[1]//SQ_SIZE
                if SQSELECTED== (ROW,COL): #same square pick
                    SQSELECTED =() # deselecting
                    PLAYERCLICKS= []
                else:
                    SQSELECTED= (ROW,COL)
                    PLAYERCLICKS.append(SQSELECTED)
                if len(PLAYERCLICKS) == 2:
                    MOVE = ChessEngine.MOVE(PLAYERCLICKS[0], PLAYERCLICKS[1], GAMESTATE.BOARD)
                    MOVE.PAWNPROMOTION = MOVE.IsPawnPromotion()  # ADD THIS LINE!
                    print (MOVE.GETCHESSNOTATION()) # debug
                    print(f"MOVE.PAWNPROMOTION after IsPawnPromotion: {MOVE.PAWNPROMOTION}")  # Debug print

                    # Check if it's the human player's turn
                    if (GAMESTATE.WHITETOMOVE and HUMANPLAYSWHITE) or (not GAMESTATE.WHITETOMOVE and not HUMANPLAYSWHITE):
                        SHOW_PROMOTION_POPUP = True  # Human player's turn
                    else:
                        SHOW_PROMOTION_POPUP = False  # AI's turn

                    for J in range(len(VALIDMOVES)):
                        if MOVE == VALIDMOVES[J]:
                            print("Move is valid") #debug
                            if MOVE.PAWNPROMOTION and SHOW_PROMOTION_POPUP:  # Only show popup for human
                                PROMOTED_PIECE = GET_PROMOTION_CHOICE(SCREEN, MOVE.PIECEMOV[0]) # Use correct case
                                GAMESTATE.MAKEMOVE(MOVE, PROMOTEDPIECE=PROMOTED_PIECE)
                            elif MOVE.PAWNPROMOTION and not SHOW_PROMOTION_POPUP:  # AI promotes
                                PROMOTED_PIECE = GET_AI_PROMOTION_CHOICE(GAMESTATE, MOVE)  # Get AI choice
                                GAMESTATE.MAKEMOVE(MOVE, PROMOTEDPIECE=PROMOTED_PIECE)
                            else:
                                GAMESTATE.MAKEMOVE(MOVE)
                            MOVEMADE = True
                            SQSELECTED = ()
                            PLAYERCLICKS = []
                if not MOVEMADE:
                    PLAYERCLICKS = [SQSELECTED]
            elif I.type==G.KEYDOWN:
                if I.key== G.K_BACKSPACE: #undo with backspace
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
        G.display.flip()
        

#Draw the board and everything else
def DrawGameState(SCREEN,GAMESTATE): 
    DrawBoard(SCREEN)
    DrawPieces(SCREEN,GAMESTATE.BOARD)

def DrawBoard(SCREEN):
    COLORS=[(247, 203, 161),(77, 36, 0)]
    for I in range(DIMENSION):
        for J in range(DIMENSION):
            COLOR = COLORS[(I + J) % 2] 
            G.draw.rect(SCREEN, COLOR, G.Rect(J * SQ_SIZE, I * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
def DrawPieces(SCREEN,BOARD):
    for I in range(DIMENSION):
        for J in range(DIMENSION):
            PIECE= BOARD[I][J]
            if PIECE != "--": #not empty
               SCREEN.blit(IMAGES[PIECE],G.Rect(J*SQ_SIZE,I*SQ_SIZE,SQ_SIZE,SQ_SIZE)) 
            
                
if __name__=="__main__":
    main()