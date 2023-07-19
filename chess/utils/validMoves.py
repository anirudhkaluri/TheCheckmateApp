
def get_valid_moves(board,slug):
    
    slug=slug.title()

    #returns a tuple (x,y) x->row y->column
    slug_position=get_slug_position(slug,board)
    #pop slug from the board
    board.pop(slug)
    

    return []


def get_slug_position(slug,board):
    cmap={"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8}
    position=board[slug]
    return (int(board[slug][1]),cmap[board[slug][0]])

