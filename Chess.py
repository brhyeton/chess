

import pygame
import numpy as np
import time
pygame.init()

class Piece:
    
    def __init__(self, colour, piece_type, location):
        self.colour = colour
        self.piece_type = piece_type
        self.image = pygame.image.load('' + colour + '_' + piece_type + '.png')
        self.location = location
        
        self.captured = False
        self.drag = False
        self.score = 0
        self.moved = False
        
        
        if self.colour == 'white':
            m = -1
        else:
            m = 1
            
        if piece_type == 'pawn':
            self.score = 1*m
        elif piece_type == 'rook':
            self.score = 5*m
        elif piece_type == 'knight' or piece_type == 'bishop':
            self.score = 3*m
        elif piece_type == 'queen':
            self.score = 8*m
        elif piece_type == 'king':
            self.score = 20*m
            
            
# class King(Piece):
#     def __init__(self, colour, piece_type, location):
        
            
        
        
def create_pieces():
    
    location = np.empty((32,2), dtype = int)
    for i in range(8):
        location[i] = [1*i,0]
        location[i+8] = [1*i,1]
        location[i+16] = [1*i,6]
        location[i+24] = [1*i,7]
        
    
    pieces = np.empty(32, dtype=Piece)
    pieces = [Piece('black', 'rook', location[0]), Piece('black', 'knight', location[1]), Piece('black', 'bishop', location[2]), Piece('black', 'queen', location[3]), Piece('black', 'king', location[4]), Piece('black', 'bishop', location[5]), Piece('black', 'knight', location[6]), Piece('black', 'rook', location[7]), 
              Piece('black', 'pawn', location[8]), Piece('black', 'pawn', location[9]), Piece('black', 'pawn', location[10]), Piece('black', 'pawn', location[11]), Piece('black', 'pawn', location[12]), Piece('black', 'pawn', location[13]), Piece('black', 'pawn', location[14]), Piece('black', 'pawn', location[15]),
              Piece('white', 'pawn', location[16]), Piece('white', 'pawn', location[17]), Piece('white', 'pawn', location[18]), Piece('white', 'pawn', location[19]), Piece('white', 'pawn', location[20]), Piece('white', 'pawn', location[21]), Piece('white', 'pawn', location[22]), Piece('white', 'pawn', location[23]), 
              Piece('white', 'rook', location[24]), Piece('white', 'knight', location[25]), Piece('white', 'bishop', location[26]), Piece('white', 'queen', location[27]), Piece('white', 'king', location[28]), Piece('white', 'bishop', location[29]), Piece('white', 'knight', location[30]), Piece('white', 'rook', location[31])]
    
    return pieces 

#Stuff that happens as it loads and doesnt need to update
pieces = create_pieces()
screen = pygame.display.set_mode([480, 480])
turn = 'White'
total_score = 0

def update_turn(turn):
    if turn == 'White':
        turn = 'Black'
    else:
        turn = 'White'
        
    return turn

def get_square(pos):
    x = int(np.floor(pos[0]/60))
    y = int(np.floor(pos[1]/60))
    
    label = str(chr(x + 96)) + str(9-y)

    return np.array([x,y])

def get_piece(square):
    for piece in pieces:
        if np.array_equal(piece.location, square):
            return piece

def update_pieces():
    for piece in pieces:
        if piece.captured == True:
            piece.location = np.array([10,10])
        if piece.drag == True:
            piece.location = (np.array(pygame.mouse.get_pos())-30)/60
            
def passed_over(sq1, sq2):
    if sq1[0] == sq2[0]:
        dist = abs(sq1[1] - sq2[1]) - 1
        squares = np.empty((dist,2))
        
        for i in range(dist):
            squares[i] = np.array([sq1[0], abs(max(sq1[1], sq2[1]) - i - 1)])
            
    if sq1[1] == sq2[1]:
        dist = abs(sq1[0] - sq2[0]) - 1
        squares = np.empty((dist,2))
        
        for i in range(dist):
            squares[i] = np.array([abs(max(sq2[0], sq1[0]) - i - 1), sq1[1]])    
            
    for a in range(8):
        if abs(sq1[0] - sq2[0]) == a and abs(sq1[1] - sq2[1]) == a:
            dist = abs(sq1[0] - sq2[0]) - 1
            squares = np.empty((dist,2))
            
            if sq2[0] > sq1[0] and sq2[1] > sq1[1]:
                for i in range(dist):
                    squares[i] = np.array([sq2[0] - i - 1, sq2[1] - i - 1])
            elif sq2[0] > sq1[0] and sq2[1] < sq1[1]:
                for i in range(dist):
                    squares[i] = np.array([sq2[0] + i - dist, sq1[1] - i - 1]) 
            elif sq2[0] < sq1[0] and sq2[1] < sq1[1]:
                for i in range(dist):
                    squares[i] = np.array([sq1[0] - i - 1, sq1[1] - i - 1]) 
            elif sq2[0] < sq1[0] and sq2[1] > sq1[1]:
                for i in range(dist):
                    squares[i] = np.array([sq1[0] + i - dist, sq2[1] - i - 1]) 
            
    return squares
            


def check_legal(piece, sq1, sq2):
    legal = False
    
    if piece is not None:
        
        #Checks if the piece has moved at all.
        if np.array_equal(sq1, sq2):
            legal = False
        else:
        
            if piece.piece_type == 'knight':
                #Knight Movement
                if abs(sq1[0] - sq2[0]) == 1 and abs(sq1[1] - sq2[1]) == 2  or abs(sq1[0] - sq2[0]) == 2 and abs(sq1[1] - sq2[1]) == 1:
                    legal = True
                        
            if piece.piece_type == 'rook':
                #Rook Movement
                if sq1[0] == sq2[0] or sq1[1] == sq2[1]:
                    legal = True
                    
                    #Checks if a piece is in the way of movement
                    for square in passed_over(sq1, sq2):
                        if not get_piece(square) == None:
                            legal = False
                            break
                        
            if piece.piece_type == 'bishop':
                #Bishop Movement
                for a in range(8):
                    if abs(sq1[0] - sq2[0]) == a and abs(sq1[1] - sq2[1]) == a:
                        legal = True
                        
                        #Checks if a piece is in the way of movement
                        for square in passed_over(sq1, sq2):
                            if not get_piece(square) == None:
                                legal = False
                                break
            
            if piece.piece_type == 'queen':
                #Queen Movement                
                for a in range(8):
                    if abs(sq1[0] - sq2[0]) == a and abs(sq1[1] - sq2[1]) == a or sq1[0] == sq2[0] or sq1[1] == sq2[1]:
                        legal = True
                        
                        #Checks if a piece is in the way of movement
                        for square in passed_over(sq1, sq2):
                            if not get_piece(square) == None:
                                legal = False
                                break
                            
            if piece.piece_type == 'king':
                #King Movement
                if abs(sq1[0] - sq2[0]) == 1 and abs(sq1[1] - sq2[1]) == 0 or abs(sq1[0] - sq2[0]) == 0 and abs(sq1[1] - sq2[1]) == 1 or abs(sq1[0] - sq2[0]) == 1 and abs(sq1[1] - sq2[1]) == 1:
                    legal = True
                
                #Castling. Initial check is to see if the king has moved
                if piece.moved == False and sq2[0] == 2 or piece.moved == False and sq2[0] == 6:
                    #Get rook which is to be castled
                    if sq1[0] > sq2[0]:
                        rook = get_piece(np.array([0,sq1[1]]))
                        m = -1
                    elif sq1[0] < sq2[0]:
                        rook = get_piece(np.array([7,sq1[1]]))
                        m = 1
                    
                    #Check if rook has moved
                    if rook.moved == False:
                        legal = True
                        for square in passed_over(sq1, rook.location):
                            if not get_piece(square) == None:
                                legal = False
                                break
                            
                    #Move Rook if legal
                    if legal == True:
                        rook.location = sq2 - m*np.array([1,0])

        
            for capture in pieces:
                
                #Checks to see if a piece trying to be captured is of the same colour
                if np.array_equal(sq2, capture.location) and capture.colour == piece.colour:
                    legal = False
                    break
                
                if piece.piece_type == 'pawn':
                    
                    #Checks which direction it must be going
                    if piece.colour == 'white':
                        m = 1
                    else:
                        m = -1
                        
                    #Normal forward movement for pawn
                    if sq1[1] - sq2[1] == 2*m and sq1[0] == sq2[0] and sq1[1] == 6 or sq1[1] - sq2[1] == 2*m and sq1[0] == sq2[0] and sq1[1] == 1 or sq1[1] - sq2[1] == 1*m and sq1[0] == sq2[0]:
                        if np.array_equal(sq2, capture.location):
                            legal = False
                            break
                        legal = True
                
                    #Diagonal Taking movement
                    if np.array_equal(sq2, capture.location) and sq1[1] - sq2[1] == 1*m and abs(sq1[0] - sq2[0]) == 1:
                        legal = True
                        
    return legal

def check_check():
    #Need this to somehow check if the king is being targeted, if there are any possible moves to block the target.
    print('check check')
            



#Stuff that needs to update
running = True
clicked_piece = None
while running:
    #System Tings
    pygame.time.delay(10)
    pygame.display.set_caption('Chess. {} to play. Score: {}'.format(turn, total_score))

    #Fill screen with white colour
    screen.fill((250, 250, 220))

    #Draw on the black sqaures
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(screen, (170, 160, 100), pygame.Rect(120*i+60, 120*j, 60, 60))
            pygame.draw.rect(screen, (170, 160, 100), pygame.Rect(120*i, 120*j+60, 60, 60))
            
    #Draw on the pieces in their locations
    for piece in pieces:
        screen.blit(piece.image, piece.location*60)
    
    #Wait for events to occur such as click down or up
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        #Stuff that needs to happen when mouse clicked down
        if event.type == pygame.MOUSEBUTTONDOWN:
            square = get_square(pygame.mouse.get_pos())
            starting_square = square
            clicked_piece = get_piece(square)
            if clicked_piece is not None:
                if turn.lower() == clicked_piece.colour:
                    clicked_piece.drag = True
                else:
                    clicked_piece = None
            
        #Stuff that needs to happen when mouse clicked up
        if event.type == pygame.MOUSEBUTTONUP:
            square = get_square(pygame.mouse.get_pos())
            ending_square = square
            
            before = time.time()
            legal = check_legal(clicked_piece, starting_square, ending_square)
            
            #Find piece underneath and calls it 'captured'
            captured_piece = get_piece(square)
            if captured_piece is not None and clicked_piece is not None and legal:
                captured_piece.captured = True
                total_score += captured_piece.score
                
            #'drops' clicked piece on that square
            if clicked_piece is not None:
                clicked_piece.location = square
                clicked_piece.drag = False
                #Updates the turn once a piece has been dropped.
                if legal:
                    turn = update_turn(turn)
                    clicked_piece.moved = True
                else:
                    clicked_piece.location = starting_square
            after = time.time()
            #print(after-before)
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                print('Turn Swapped')
                turn = update_turn(turn)
                
            if event.key == pygame.K_n:
                pieces = create_pieces()
                print('New Game')
                turn = 'White'
            
            #Reset variables.
            captured_piece = None
            clicked_piece = None
               
    
    #Things that needs to be checked every loop
    update_pieces()
    
    
    pygame.display.flip()
            
pygame.quit()