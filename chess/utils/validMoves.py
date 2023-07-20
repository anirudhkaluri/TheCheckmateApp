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
def get_valid_moves(board:dict[str,str],slug:str)->list[str]:

    #returns a list [x,y] x->row y->column
    slug_position=get_coordinate_position(board[slug])
    #remove the slug from the board. remaining pieces are opponents
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
def get_coordinate_position(position:str)->list[int]:
        return [row_map[position[1]],column_map[position[0]]]



#returns a list of all possible positions for slug ASSUMING OTHER PIECES DONT ATTACK BUT CAN OBSTRUCT
def get_all_possible_moves(slug:str,starting_position:list,board:dict[str,str])->list[list[int]]:
    possible_moves=[]
    if slug=="Queen":
        #3 possible directions for queen
        add_positions(slug,starting_position,possible_moves,[diagonal,horizontal,vertical],board)
    elif slug=="Bishop":
        #only diagonal for bishop
        add_positions(slug,starting_position,possible_moves,[diagonal],board)
    elif slug=="Rook":
        #horizontal and vertical directions possible for rook
        add_positions(slug,starting_position,possible_moves,[horizontal,vertical],board)
    elif slug=="Knight":
        #Knight for knight
        add_positions(slug,starting_position,possible_moves,[knight],board)
    return possible_moves


#adds positions based on the direction rules given at the beginning of the file
#axes is a list of axis across which the slug can move. it is a list of lists. 
#If the slug is a queen, the axes are diagonal, horizontal, vertical
#all the possible moves are stored in possible_moves list
def add_positions(slug:str,starting_position:list[int],possible_moves:list[int],axes:list[tuple],board:dict[str,str])->None:
    #for each direction the axes, see what all positions are possible for the slug
    for direction in axes:
        #movement[0] means move movement[0] length in x direction, movement[1] in y direction
        for movement in direction:
            position=list(starting_position)
            #start moving/jumping in that direction
            position[0]=position[0]+movement[0]
            position[1]=position[1]+movement[1]
            if slug=="Knight":
                #Knight just jumps once, checking if the jump is within the board
                if check_limit(position):
                    possible_moves.append(list(position))
                    continue
            else:
                #Rook,Queen,Bishop can keep moving in a straight line. So keep moving in that direction
                while check_limit(position) and not obstruction_exists(starting_position,position,board):
                    possible_moves.append(list(position))
                    position[0]=position[0]+movement[0]
                    position[1]=position[1]+movement[1]
                continue


#checks if the (x,y) coordinate is within the board 
def check_limit(position:list[int])->bool:
    if position[0]<1 or position[0]>8 or position[1]<1 or position[1]>8 :
        return False
    return True

#given a set of possible_moves, return only those moves which wont be attacked by pieces on the board 
def check_attack_on_positions(possible_moves:list[list[int]],board:dict[str,str])->list[list[int]]:
    attack_positions=[] #stores all positions that can be attacked
    for piece,piece_position in board.items():
        position1= get_coordinate_position(piece_position)
        for target_position in possible_moves:
            #if a direct move exists from position1 to target_position without obstruction, target_position can be attacked
            if direct_move_exists(piece,position1,target_position,board):
                attack_positions.append(target_position)
    #remove all the positions that can be attacked from possible_moves. They are the valid moves
    valid_moves=[sublist for sublist in possible_moves if sublist not in attack_positions]
    return valid_moves

#checks whether a PIECE can travel from position1 to  position2 in ONE MOVE WITHOUT OBSTRUCTION
def direct_move_exists(piece:str,position1:list[int],position2:list[int],board:dict[str,str])->bool:
    same_position=bool(position1[0]==position2[0] and position1[1]==position2[1])
    if same_position:
        return False
    #check if position1 and position2 are on same diagonal or row or column
    same_diagonal=bool(abs(position1[0]-position2[0])==abs(position1[1]-position2[1]))
    same_row= bool(position1[0]-position2[0]==0) 
    same_column=bool(position1[1]-position2[1]==0)
    #check if there is any obstuction b/w position1 and position2 due to other pieces on the board
    obstruction=bool(obstruction_exists(position1,position2,board))
    if piece=="Queen" and (same_diagonal or same_row or same_column) and not obstruction: #for queen we check diagonal, row, column
        return True
    elif piece=="Bishop" and same_diagonal and not obstruction: #for bishop we check only diagonal
        return True
    elif piece=="Rook" and (same_row or same_column) and not obstruction: #for rook we check row and column 
        return True
    elif piece=="Knight": 
        for item in knight:
            if position1[0]+item[0]==position2[0] and position1[1]+item[1]==position2[1]: #since knight jumps over pieces no need to check for obstruction
                return True
    return False


#checks whether an obstruction exists between two positions- position1 and position2
def obstruction_exists(position1:list[int],position2:list[int],board:dict[str,str])->bool:
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