
#Drive file with user input and displaying the gamestate.
import pygame
import ChessEngine
HEIGHT = WIDTH = 640 #pieces are 60x60
DIMENSION = 8 #board dimensions
SQ_SIZE= HEIGHT // DIMENSION #square size so it can be changed if i decide to change the size of the window so it can autochange
MAX_FPS = 15 # just in case i do animations
IMAGES = {}

def LoadImage():
    PIECES= ['wP','wR','wN','wB','wQ','wK','bP','bR','bN','bB','bK','bQ']
    for PIECE in PIECES:
        IMAGES[PIECE]=pygame.transform.scale(pygame.image.load("chess/Image/"+PIECE+".png"),(SQ_SIZE,SQ_SIZE))

#Main driver to deal with user input and graphics
def main():
    pygame.init()
    SCREEN= pygame.display.set_mode((WIDTH,HEIGHT))
    CLOCK=pygame.time.Clock()
    SCREEN.fill(pygame.Color("white"))
    GAMESTATE= ChessEngine.GameState()
    LoadImage()# only once
    RUNNING = True
    while RUNNING:
        for i in pygame.event.get():
            if i.type==pygame.QUIT:
                RUNNING=False
        DrawGameState(SCREEN,GAMESTATE)
        CLOCK.tick(MAX_FPS)
        pygame.display.flip()
        

#Draw the board and everything else
def DrawGameState(SCREEN,GAMESTATE): 
    DrawBoard(SCREEN)
    DrawPieces(SCREEN,GAMESTATE.board)

def DrawBoard(SCREEN):
    COLORS=[(247, 203, 161),(77, 36, 0)]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            COLOR = COLORS[(i + j) % 2] 
            pygame.draw.rect(SCREEN, COLOR, pygame.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    print("Board drawn")
    
def DrawPieces(SCREEN,BOARD):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            PIECE= BOARD[i][j]
            if PIECE != "-": #not empty
               SCREEN.blit(IMAGES[PIECE],pygame.Rect(j*SQ_SIZE,i*SQ_SIZE,SQ_SIZE,SQ_SIZE)) 
            
                
if __name__=="__main__":
    main()







