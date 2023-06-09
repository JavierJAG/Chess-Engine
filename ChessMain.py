#User imput and current GameState Objetct.
import pygame as p
import ChessEngine 

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION #SquareSize
MAX_FPS = 15
IMAGES = {}

"""
Initialize a global dictionary of images, it will be called only 1 time because it is an expensive task
"""
def load_images():
    pieces =["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("ChessPieces/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        
        # we can acces an image by saying [IMAGE("wp")]


#This will handle user input and update the graphics

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #Flag variable for when a move is made
    load_images()
    running = True
    sqSelected = () #No square is selected at first, tracks last click,  (tuple(row,col))
    playerClicks = [] #keep track of clicks (two tuples:[(6,4)(4,4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #Mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): #The user clicks same square twice
                    sqSelected = () #deselect
                    playerClicks = []#clear player click
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) #Append both clicks
                if len(playerClicks) == 2:  #After second click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = () #Reset clicks
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]

            #Key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #Undo when "z" is pressed
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
            
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

#The actual graphics
def drawGameState(screen, gs):
    drawSquares(screen) #Draw squares
    drawPieces(screen, gs.board) #draw pieces on top of squares

def drawSquares(screen):
    colors = [p.Color("pink"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)) #scree.blit allows to overlap the surface of the canvas

if __name__ == "__main__":
    main()