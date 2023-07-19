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

    possible_moves=get_all_possible_moves(slug,slug_position)
    

    return []


def get_slug_position(slug,board):
    cmap={"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8}
    position=board[slug]
    return (int(board[slug][1]),cmap[board[slug][0]])

#returns a list of all possible positions for slug assuming there is no other piece on the board
def get_all_possible_moves(slug,starting_position):
    possible_moves=[]
    if slug=="Queen":
        add_positions(starting_position,possible_moves,diagonal)
        add_positions(starting_position,possible_moves,horizontal)
        add_positions(starting_position,possible_moves,vertical)
    elif slug=="Bishop":
        add_positions(starting_position,possible_moves,diagonal)
    elif slug=="Rook":
        add_positions(starting_position,possible_moves,horizontal)
        add_positions(starting_position,possible_moves,vertical)
    elif slug=="Knight":
        add_positions(starting_position,possible_moves,knight)
    return possible_moves




