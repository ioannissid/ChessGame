#Drive file with user input and displaying the gamestate.
import pygame as G #shortcut for game cause writing pygame over and over became tedious
import ChessEngine
import ChessAI
from multiprocessing import Process, Queue
BOARD_WIDTH = BOARD_HEIGHT = 640 #pieces are 60x60
MOVELOGWIDTH = 320
MOVELOGHEIGHT = BOARD_HEIGHT
DIMENSION = 8 #board dimensions
SQ_SIZE= BOARD_HEIGHT // DIMENSION #square size so it can be changed if i decide to change the size of the window so it can autochange
MAX_FPS = 120 #for animations
IMAGES = {}

def loadImage():
    PIECES = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for PIECE in PIECES:
        IMAGES[PIECE] = G.transform.scale(G.image.load("Image/" + PIECE + ".png"), (SQ_SIZE, SQ_SIZE))
#main driver to deal with user input and graphics
def main():
    G.init()
    SCREEN = G.display.set_mode((BOARD_WIDTH+MOVELOGWIDTH, BOARD_HEIGHT))
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
    MOVELOGFONT = G.font.SysFont("Times New Roman", 16, True, False) 
    AIWORKING = False #flag for ai working
    MOVEFINDER = None 
    MOVEUNDONE = False #flag for move undone
    
    
    # both true = 2 humans , both false = 2 ai, one true and one false = human vs ai
    HUMANISWHITE= False #true = human is white false = ai is white
    HUMANISBLACK= False #true = human is black false = ai is black
    
    
    
    
    
    while RUNNING:
        
        HUMANTURN= (GAMESTATE.WHITETOMOVE and HUMANISWHITE) or (not GAMESTATE.WHITETOMOVE and HUMANISBLACK) #if its the human turn or not
        
        
        
    
        for I in G.event.get():
            if I.type == G.QUIT:
                RUNNING = False
            elif I.type == G.MOUSEBUTTONDOWN: #START OF MOUSE HANDLING
                if not GAMEOVER:
                    LOCATION = G.mouse.get_pos() 
                    COL = LOCATION[0] // SQ_SIZE
                    ROW = LOCATION[1] // SQ_SIZE
                    if SQSELECTED == (ROW, COL) or COL >= 8:  #same square pick or user clicked on the move log
                        SQSELECTED = ()  #deselecting
                        PLAYERCLICKS = []  #clear clicks
                    else:
                        SQSELECTED = (ROW, COL)
                        PLAYERCLICKS.append(SQSELECTED)  # append for both 1st and 2nd click
                    if len(PLAYERCLICKS) == 2 and HUMANTURN:
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
                    if AIWORKING:
                        
                        MOVEFINDER.terminate()
                        AIWORKING=False
                    MOVEUNDONE=True
                if I.key == G.K_r:  # reset with r
                    GAMESTATE = ChessEngine.GAMESTATE()
                    VALIDMOVES = GAMESTATE.GETVALIDMOVES()
                    SQSELECTED = ()
                    PLAYERCLICKS = []
                    MOVEMADE = False
                    ANIMATE = False
                    GAMEOVER = False
                    if MOVEFINDER is not None:
                        MOVEFINDER.terminate()
                    MOVEFINDER = None
                    AIWORKING = False
                    MOVEUNDONE = False
                    HUMANTURN = (GAMESTATE.WHITETOMOVE and HUMANISWHITE) or (not GAMESTATE.WHITETOMOVE and HUMANISBLACK) #recalculate the turn because it created a bug when the reset happended
                    continue
                if I.key== G.K_ESCAPE:
                    RUNNING=False
                    

        #ai logic
        if not HUMANTURN and not GAMEOVER and not MOVEUNDONE:
            if not AIWORKING:
                AIWORKING=True
                RQUEUE=Queue() #pass data between threads cause the dont share normally
                MOVEFINDER = Process(target=ChessAI.FINDBESTMOVE, args=(GAMESTATE,VALIDMOVES,RQUEUE))
                MOVEFINDER.start() #calls ai with the gamestate and valid moves

            if not MOVEFINDER.is_alive(): #if the ai is done thinking        
                AIMOVE = RQUEUE.get() #get the move from the ai
                if AIMOVE == None:
                    AIMOVE = ChessAI.FINDRANDOMMOVE(VALIDMOVES)
                GAMESTATE.MAKEMOVE(AIMOVE)
                MOVEMADE=True
                ANIMATE=True
                AIWORKING=False
        
        
        
                   
                    
                    
        if MOVEMADE:
            if ANIMATE:   
                ANIMATEMOVE(GAMESTATE.MOVELOG[-1], SCREEN, GAMESTATE.BOARD, CLOCK) #animation of the move made
            
            VALIDMOVES = GAMESTATE.GETVALIDMOVES()
            MOVEMADE = False
            ANIMATE= False    
            MOVEUNDONE=False
            
        DrawGameState(SCREEN,GAMESTATE,VALIDMOVES,SQSELECTED,MOVELOGFONT) 
        
        if GAMESTATE.CHECKMATE:
            GAMEOVER=True
            if GAMESTATE.WHITETOMOVE:
                DRAWENDGAMETEXT(SCREEN, "Black wins by Checkmate",GAMESTATE)
            else:
                DRAWENDGAMETEXT (SCREEN,"White wins by Checkmate",GAMESTATE)
        elif GAMESTATE.STALEMATE:
            GAMEOVER=True
            DRAWENDGAMETEXT(SCREEN,"Stalemate",GAMESTATE)
            

        
        CLOCK.tick(MAX_FPS)
        G.display.flip()
     
#Draw the BOARD and everything else
def DrawGameState(SCREEN,GAMESTATE,VALIDMOVES,SQSELECTED,MOVELOGFONT): 
    DrawBoard(SCREEN)
    HIGHLIGHTSQUARES(SCREEN,GAMESTATE,VALIDMOVES,SQSELECTED) #before the pieces so it doesnt cover them
    DrawPieces(SCREEN,GAMESTATE.BOARD)
    DRAWMOVELOG(SCREEN,GAMESTATE,MOVELOGFONT)

def DrawBoard(SCREEN):
    global COLORS
    COLORS=[(247, 203, 161),(77, 36, 0)]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = COLORS[(i + j) % 2] 
            G.draw.rect(SCREEN, color, G.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
            
            
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
     

    
def DrawPieces(SCREEN,BOARD):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            PIECE= BOARD[i][j]
            if PIECE != "--": #not empty
                SCREEN.blit(IMAGES[PIECE], G.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
               
def DRAWMOVELOG(SCREEN, GAMESTATE, MOVELOGFONT):
    MOVELOGREC = G.Rect(BOARD_WIDTH, 0, MOVELOGWIDTH, MOVELOGHEIGHT)
    COLORS = (150, 115, 72)  # Brown background
    G.draw.rect(SCREEN, COLORS, MOVELOGREC)
    MOVELOG = GAMESTATE.MOVELOG
    MOVETEXT = []
    
    for i in range(0, len(MOVELOG), 2):
        # Move number and white's move in white
        MOVESTRING = str(i//2 + 1) + "." 
        WHITEMOVE = str(MOVELOG[i]) + " "
        
        # If black moved, add their move in black
        BLACKMOVE = ""
        if i+1 < len(MOVELOG):
            BLACKMOVE = str(MOVELOG[i+1]) 
            
        MOVETEXT.append((MOVESTRING, WHITEMOVE, BLACKMOVE))
    
    MOVESPERROW = 3
    PADDING = 5
    TEXTY = PADDING
    LINESPACE = 2
    
    for i in range(0, len(MOVETEXT), MOVESPERROW):
        TEXT = ""
        for j in range(MOVESPERROW):
            if i+j < len(MOVETEXT):
                # Split each move into components
                MOVENUM, WMOVE, BMOVE = MOVETEXT[i+j]
                
                # Render move number in gray
                NUMOBJ = MOVELOGFONT.render(MOVENUM, True, G.Color('gray'))
                TEXTLOC = MOVELOGREC.move(PADDING + len(TEXT)*8, TEXTY)
                SCREEN.blit(NUMOBJ, TEXTLOC)
                
                # Render white's move in white
                WHITEOBJ = MOVELOGFONT.render(WMOVE, True, G.Color('white'))
                TEXTLOC = TEXTLOC.move(NUMOBJ.get_width(), 0)
                SCREEN.blit(WHITEOBJ, TEXTLOC)
                
                # Render black's move in dark gray (pure black might be hard to read)
                if BMOVE:
                    BLACKOBJ = MOVELOGFONT.render(BMOVE, True, (50, 50, 50))
                    TEXTLOC = TEXTLOC.move(WHITEOBJ.get_width(), 0)
                    SCREEN.blit(BLACKOBJ, TEXTLOC)
                
                TEXT += MOVENUM + WMOVE + BMOVE
                
        TEXTY += MOVELOGFONT.get_height() + LINESPACE
       
               
               
               
               
               
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
            if MOVE.ENPASSANT:
                ENPASSANTROW = MOVE.ENDROW +1  if MOVE.PIECEMOV[0] == 'w'else MOVE.ENDROW -1 
                ENDSQUARE= G.Rect(MOVE.ENDCOL * SQ_SIZE, ENPASSANTROW * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                
                
            SCREEN.blit(IMAGES[MOVE.PIECECAP], ENDSQUARE)
            
        SCREEN.blit(IMAGES[MOVE.PIECEMOV], G.Rect(COL * SQ_SIZE, ROW * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        G.display.flip()
        CLOCK.tick(MAX_FPS)
        
        
def DRAWENDGAMETEXT(SCREEN, TEXT, GAMESTATE):
    FONT = G.font.SysFont("Times New Roman", 48, True, False)  # font name, size, bold, italic
    if GAMESTATE.STALEMATE:
        TEXTOBJ = FONT.render(TEXT, 0, G.Color('Gold'))
    elif GAMESTATE.CHECKMATE:
        if GAMESTATE.WHITETOMOVE:
            TEXTOBJ = FONT.render(TEXT, 0, G.Color('Black'))
        else:
            TEXTOBJ = FONT.render(TEXT, 0, G.Color('White'))
    # Center the text
    TEXTLOC = G.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - TEXTOBJ.get_width() / 2, BOARD_HEIGHT / 2 - TEXTOBJ.get_height() / 2)
    BG_RECT = G.Rect(TEXTLOC.x - 10, TEXTLOC.y - 10,TEXTOBJ.get_width() + 20, TEXTOBJ.get_height() + 20)# Draw a background rectangle behind the text     
    G.draw.rect(SCREEN, G.Color('Gray'), BG_RECT) 
    SCREEN.blit(TEXTOBJ, TEXTLOC)# Draw the text on top of the background
    
    
if __name__=="__main__":
    main()
