import sys
# DIRECTION RULES
#Queen travels diagonal, horizontal,vertical
#Bishop travels diagonal
#Rook travels horizontal,vertical
#Knight travels Knight
diagonal=[(1,1),(-1,-1),(-1,1),(1,-1)]
horizontal=[(-1,0),(1,0)]
vertical=[(0,1),(0,-1)]
knight=[(2,-1),(2,1),(-2,-1),(-2,1),(1,-2),(-1,-2),(1,2),(-1,2)]
column_map={"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8}
row_map={"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8}
reverse_map={1:"A",2:"B",3:"C",4:"D",5:"E",6:"F",7:"G",8:"H"} #for converting numerica coordinates to chess terminology

#RETURNS VALID MOVES
def get_valid_moves(board,slug):
    slug=slug.title()
    #returns a list [x,y] x->row y->column
    slug_position=get_coordinate_position(board[slug])
    #pop slug from the board
    board.pop(slug)
    #get a list of all possible moves as if no other piece is on the board except the slug
    possible_moves=get_all_possible_moves(slug,slug_position,board)
    #check if the remaining of the board can attack those possible positions/moves and return only valid moves/positions
    valid_moves=check_attack_on_positions(possible_moves,board) 
    #convert coordinate points to chess terminology  
    answer=[]
    for item in valid_moves:
        answer.append(str(reverse_map[item[1]])+str(item[0]))
    return answer

#returns position of slug in list form [row,column]
def get_coordinate_position(position):
        return [row_map[position[1]],column_map[position[0]]]



#returns a list of all possible positions for slug assuming there is no other piece on the board
def get_all_possible_moves(slug,starting_position,board):
    possible_moves=[]
    if slug=="Queen":
        #3 possible directions for queen
        add_positions(slug,starting_position,possible_moves,[diagonal,horizontal,vertical],board)
    elif slug=="Bishop":
        #only diagonal for bishop
        add_positions(slug,starting_position,possible_moves,[diagonal],board)
    elif slug=="Rook":
        #horizontal and vertical for rook
        add_positions(slug,starting_position,possible_moves,[horizontal,vertical],board)
    elif slug=="Knight":
        #knight for knight
        add_positions(slug,starting_position,possible_moves,[knight],board)
    return possible_moves


#adds positions based on the direction rules at the beginning of the file
def add_positions(slug,starting_position,possible_moves,directions,board):
    for direction in directions:
        for item in direction:
            pos=list(starting_position)
            pos[0]=pos[0]+item[0]
            pos[1]=pos[1]+item[1]
            if slug=="Knight":
                if check_limit(pos):
                    possible_moves.append(list(pos))
                    continue
            else:
                while check_limit(pos) and not obstruction_exists(starting_position,pos,board):
                    possible_moves.append(list(pos))
                    pos[0]=pos[0]+item[0]
                    pos[1]=pos[1]+item[1]
                continue


#checks if the (x,y) coordinate is within the board 
def check_limit(position):
    if position[0]<1 or position[0]>8 or position[1]<1 or position[1]>8 :
        return False
    return True

#given a set of possible positions in possible_moves, return only those moves which wont be attacked
def check_attack_on_positions(possible_moves,board):
    attack_positions=[]
    for piece,piece_position in board.items():
        from_position=[int(piece_position[1]),column_map[piece_position[0]]]
        for to_position in possible_moves:
            if direct_move_exists(piece,from_position,to_position,board):
                attack_positions.append(to_position)
    valid_moves=[sublist for sublist in possible_moves if sublist not in attack_positions]
    return valid_moves

#checks whether a piece can travel from one position to another position in one move
def direct_move_exists(piece,from_position,to_position,board):
    same_position=bool(from_position[0]==to_position[0] and from_position[1]==to_position[1])
    if same_position:
        return False
    same_diagonal=bool(abs(from_position[0]-to_position[0])==abs(from_position[1]-to_position[1]))
    same_row= bool(from_position[0]-to_position[0]==0) 
    same_column=bool(from_position[1]-to_position[1]==0)
    obstruction=bool(obstruction_exists(from_position,to_position,board))
    if piece=="Queen" and (same_diagonal or same_row or same_column) and not obstruction:
        return True
    elif piece=="Bishop" and same_diagonal and not obstruction:
        return True
    elif piece=="Rook" and (same_row or same_column) and not obstruction:
        return True
    elif piece=="Knight":
        for item in knight:
            if from_position[0]+item[0]==to_position[0] and from_position[1]+item[1]==to_position[1]:
                return True
    return False


#checks whether an obstruction exists between two positions- position1 and position2
def obstruction_exists(position1,position2,board):
    #iterate over the pieces on the board board
    for key,value in board.items():
        position3 = get_coordinate_position(board[key])
        if  (position3[0]==position2[0] and position3[1]==position2[1]) or (position3[0]==position1[0] and position3[1]==position1[1]):
            continue
        else:
            x1=float(position1[0])
            y1=float(position1[1])
            x2=float(position2[0])
            y2=float(position2[1])
            x3=float(position3[0])
            y3=float(position3[1])
            slope1=(y2-y1)/(x2-x1) if x2!=x1 else sys.maxsize
            slope2=(y3-y2)/(x3-x2) if x3!=x2 else sys.maxsize
            xmax= position1[0] if x1>x2 else position2[0]
            xmin=position1[0] if x1<x2 else position2[0]
            ymax= position1[1] if y1>y2 else position2[1]
            ymin= position1[1] if y1<y2 else position2[1]
            #If slopes are equal and if position3's coordinate in between position 1 and position 2's, then obstruction exists
            if slope1==slope2 and (position3[0] in range(xmin,xmax+1)) and (position3[1] in range(ymin,ymax+1)):
                return True
    return False