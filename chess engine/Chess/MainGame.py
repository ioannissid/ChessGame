#Drive file with user input and displaying the gamestate.
import pygame
import ChessEngine
HEIGHT = WIDTH = 640 #pieces are 60x60
DIMENSION = 8 #board dimensions
SQ_SIZE= HEIGHT // DIMENSION #square size so it can be changed if i decide to change the size of the window so it can autochange
#MAX_FPS = 15 just in case i do animations
IMAGES = {}
#loading images but only once at start to avoid lagging
def LoadImage():
    PIECES= ['wP','wR','wN','wB','wQ','bP','bR','bN','bB','bK','bQ']
    for PIECE in PIECES:
        IMAGES[PIECE]=pygame.transform.scale(pygame.image.load("images/"+PIECE+".png"),(SQ_SIZE,SQ_SIZE))

#Main driver to deal with user input and graphics
def main():
    pygame.init()
    screen= pygame.display.set_mode((WIDTH,HEIGHT))
    clock=pygame.time.Clock
    screen.fill(pygame.Color("white"))
    GameState= ChessEngine.GameState()
    print(GameState.board)
    
main()