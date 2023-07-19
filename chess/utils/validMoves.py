# MOVE RULES
#queen travels diagonal, horizontal,vertical
#Bishop travels diagonal
#Rook travels horizontal,vertical
#knight travels Knight
diagonal=[(1,1),(-1,-1),(-1,1),(1,-1)]
horizontal=[(-1,0),(1,0)]
vertical=[(0,1),(0,-1)]
knight=[(2,-1),(2,1),(-2,-1),(-2,1),(1,-2),(-1,-2),(1,2),(-1,2)]

#RETURNS VALID MOVES
def get_valid_moves(board,slug):
    
    slug=slug.title()

    #returns a tuple (x,y) x->row y->column
    slug_position=get_slug_position(slug,board)
    #pop slug from the board
    board.pop(slug)
    #get a list of all possible moves as if no other piece is on the board except the slug
    possible_moves=get_all_possible_moves(slug,slug_position)
    

    return []

#returns position of slug in tuple form (row,column)
def get_slug_position(slug,board):
    cmap={"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8}
    position=board[slug]
    return (int(board[slug][1]),cmap[board[slug][0]])

#returns a list of all possible positions for slug assuming there is no other piece on the board
def get_all_possible_moves(slug,starting_position):
    possible_moves=[]
    if slug=="Queen":
        #3 possible directions for queen
        add_positions(slug,starting_position,possible_moves,[diagonal,horizontal,vertical])
    elif slug=="Bishop":
        #only diagonal for bishop
        add_positions(slug,starting_position,possible_moves,[diagonal])
    elif slug=="Rook":
        #horizontal and vertical for rook
        add_positions(slug,starting_position,possible_moves,[horizontal,vertical])
    elif slug=="Knight":
        #knight for knight
        add_positions(slug,starting_position,possible_moves,[knight])
    return possible_moves

#adds positions based on the direction rules at the beginning of the file
def add_positions(starting_position,possible_moves,directions):
    for direction in directions:
        for item in direction:
            pos=starting_position
            pos[0]=pos[0]+item[0]
            pos[1]=pos[1]+item[1]
            if slug=="Knight":
                if check_limit(pos):
                    possible_moves.append(tuple(pos))
                    continue
            else:
                while check_limit(pos):
                    possible_moves.append(tuple(pos))
                    pos[0]=pos[0]+item[0]
                    pos[1]=pos[1]+item[1]
                continue





