#Drive file with user input and displaying the gamestate.
import pygame as G #shortcut for game cause writing pygame over and over became tedious
import ChessEngine
import ChessAI
WIDTH = HEIGHT = 640 #pieces are 60x60
DIMENSION = 8 #board dimensions
SQ_SIZE= HEIGHT // DIMENSION #square size so it can be changed if i decide to change the size of the window so it can autochange
MAX_FPS = 120 # just in case i do animations
IMAGES = {}

def loadImage():
    PIECES = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for PIECE in PIECES:
        IMAGES[PIECE] = G.transform.scale(G.image.load("Image/" + PIECE + ".png"), (SQ_SIZE, SQ_SIZE))
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
    ANIMATE=False #flag for animation
    SQSELECTED = ()  # keeps tract  of the user's last click wit h no square initially
    PLAYERCLICKS = [] #keeps track of player clicks (2 clicks)
    GAMEOVER= False #flag for game over
    
    
    HUMANISWHITE= False #if the human is white or false if the human is playing black
    AIISWHITE= False #if the AI is white or false if the AI is playing black
    
    
    
    
    
    while RUNNING:
        
        HUMANTURN= (GAMESTATE.WHITETOMOVE and HUMANISWHITE) or (not GAMESTATE.WHITETOMOVE and AIISWHITE) #if its the human turn or not
        
        
        
    
        for I in G.event.get():
            if I.type == G.QUIT:
                RUNNING = False
            elif I.type == G.MOUSEBUTTONDOWN: # <------- START OF MOUSE HANDLING
                if not GAMEOVER and HUMANTURN:
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
                                ANIMATE = True 
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
                    ANIMATE=False
                    MOVEMADE=True
                    GAMEOVER=False
                if I.key== G.K_r: #reset with r
                    GAMESTATE=ChessEngine.GAMESTATE()
                    VALIDMOVES = GAMESTATE.GETVALIDMOVES()
                    SQSELECTED = ()
                    PLAYERCLICKS = []
                    MOVEMADE = False
                    ANIMATE=False
                    GAMEOVER=False
                if I.key== G.K_ESCAPE:
                    RUNNING=False
                    
                    
        #ai logic
        if not HUMANTURN and not GAMEOVER:
            AIMOVE= ChessAI.FINDBESTMOVEMINMAX(GAMESTATE,VALIDMOVES)
            if AIMOVE == None:
                AIMOVE = ChessAI.FINDRANDOMMOVE(VALIDMOVES)
            GAMESTATE.MAKEMOVE(AIMOVE)
            MOVEMADE=True
            ANIMATE=True
        
        
        
                   
                    
                    
        if MOVEMADE:
            if ANIMATE:   
                ANIMATEMOVE(GAMESTATE.MOVELOG[-1], SCREEN, GAMESTATE.BOARD, CLOCK) #animation of the move made
            
            VALIDMOVES = GAMESTATE.GETVALIDMOVES()
            MOVEMADE = False
            ANIMATE= False    
            
            
        DrawGameState(SCREEN,GAMESTATE,VALIDMOVES,SQSELECTED) 
        
        if GAMESTATE.CHECKMATE:
            GAMEOVER=True
            if GAMESTATE.WHITETOMOVE:
                DRAWTEXT(SCREEN, "Black wins by Checkmate",GAMESTATE)
            else:
                DRAWTEXT (SCREEN,"White wins by Checkmate",GAMESTATE)
        elif GAMESTATE.STALEMATE:
            GAMEOVER=True
            DRAWTEXT(SCREEN,"Stalemate",GAMESTATE)
            

        
        CLOCK.tick(MAX_FPS)
        G.display.flip()
     
     

def HIGHLIGHTSQUARES(SCREEN,GS,VALIDMOVES,SQSELECTED):               #Highlight the square
    if SQSELECTED != (): 
        ROW,COL=SQSELECTED #highlight the square selected by the user
        if GS.BOARD[ROW][COL][0] == ('w' if GS.WHITETOMOVE else 'b'): #first happens the whitetomove check and if its true the its w then the other one
            S=G.Surface((SQ_SIZE, SQ_SIZE)) #takes a xy in its constrcutor so needs 1 pair 
            S.set_alpha(100) #transparency of the  square range 0-255 the less means more transparency
            S.fill(G.Color("yellow")) #color of the square
            SCREEN.blit(S,(COL*SQ_SIZE,ROW*SQ_SIZE)) 
            S.fill(G.Color("yellow"))    #hightlight the squares that are valid moves
            for MOVE in VALIDMOVES:
                if MOVE.STARTROW == ROW and MOVE.STARTCOL == COL:
                    SCREEN.blit(S,(MOVE.ENDCOL*SQ_SIZE,MOVE.ENDROW*SQ_SIZE))
     




   

#Draw the BOARD and everything else
def DrawGameState(SCREEN,GAMESTATE,VALIDMOVES,SQSELECTED): 
    DrawBoard(SCREEN)
    HIGHLIGHTSQUARES(SCREEN,GAMESTATE,VALIDMOVES,SQSELECTED) #before the piecs so it doesnt cover them
    DrawPieces(SCREEN,GAMESTATE.BOARD)




def DrawBoard(SCREEN):
    global COLORS
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
            
               
               
               
               
               
               
               
def ANIMATEMOVE(MOVE,SCREEN,BOARD,CLOCK): #animation of the piece moving 
    global COLORS
    CR = MOVE.ENDROW-MOVE.STARTROW #change in row
    CC = MOVE.ENDCOL-MOVE.STARTCOL #change in column
    FPSQ= 10 #frames per square
    FPSC= (abs(CR) + abs(CC)) * FPSQ #frames per square for the whole move
    for FRAME in range(FPSC + 1): #to include the last frame
        ROW,COL=(MOVE.STARTROW + CR * FRAME / FPSC, MOVE.STARTCOL + CC * FRAME / FPSC)
        DrawBoard(SCREEN)
        DrawPieces(SCREEN,BOARD)
        COLOR= COLORS[(MOVE.ENDROW + MOVE.ENDCOL)%2] #erase the piece from the old square
        ENDSQUARE= G.Rect(MOVE.ENDCOL * SQ_SIZE, MOVE.ENDROW * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        G.draw.rect(SCREEN,COLOR,ENDSQUARE)
        if MOVE.PIECECAP!= "--": #if the piece is captured
            SCREEN.blit(IMAGES[MOVE.PIECECAP], ENDSQUARE)
        SCREEN.blit(IMAGES[MOVE.PIECEMOV], G.Rect(COL * SQ_SIZE, ROW * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        G.display.flip()
        CLOCK.tick(MAX_FPS)
        
        
def DRAWTEXT(SCREEN, TEXT, GAMESTATE):
    FONT = G.font.SysFont("Times New Roman", 48, True, False)  # font name, size, bold, italic
    if GAMESTATE.STALEMATE:
        TEXTOBJ = FONT.render(TEXT, 0, G.Color('Gold'))
    elif GAMESTATE.CHECKMATE:
        if GAMESTATE.WHITETOMOVE:
            TEXTOBJ = FONT.render(TEXT, 0, G.Color('Black'))
        else:
            TEXTOBJ = FONT.render(TEXT, 0, G.Color('White'))
    
    # Center the text
    TEXTLOC = G.Rect(0, 0, WIDTH, HEIGHT).move(
        WIDTH / 2 - TEXTOBJ.get_width() / 2, 
        HEIGHT / 2 - TEXTOBJ.get_height() / 2
    )
    
    # Draw a gray background rectangle behind the text
    BG_RECT = G.Rect(
        TEXTLOC.x - 10, TEXTLOC.y - 10,  # Add padding around the text
        TEXTOBJ.get_width() + 20, TEXTOBJ.get_height() + 20
    )
    G.draw.rect(SCREEN, G.Color('Gray'), BG_RECT)
    
    # Draw the text on top of the background
    SCREEN.blit(TEXTOBJ, TEXTLOC)
    
    
if __name__=="__main__":
    main()
