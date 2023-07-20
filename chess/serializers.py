from rest_framework import serializers
from .utils.validMoves import get_coordinate_position



class PositionSerializer(serializers.Serializer):
    positions=serializers.DictField(child=serializers.CharField())
    slug=serializers.CharField()

    #custom validation
    #Exception messages are self-descriptive
    def validate(self,attrs):
        valid_pieces={"Queen","Bishop","Knight","Rook"} #set of valid pieces that can be on the baord 
        attrs['slug']=attrs.get('slug').title()  #to make sure the slug is formatted in the correct way.

        board=attrs.get('positions') #the board configurations
        slug=attrs.get('slug') #the slug received from the url

        set_of_positions=set()
        set_of_pieces=set()

        for piece,position in board.items():
            
            if piece not in valid_pieces:
                raise serializers.ValidationError("No such chess pieces. Invalid chess Pieces given in request data")
            if not len(position)==2:
                raise serializers.ValidationError("Invalid Position.Position on the grid must be of length 2")
            try:
                [x,y]=get_coordinate_position(position) #uses map. implementation in .utils.validMoves
            except KeyError as e:
                raise serializers.ValidationError("Invalid position. Position must be of the form [A-H][1-8]")
            if position in set_of_positions:
                raise serializers.ValidationError("Two pieces cant be at the same time in the same position")
            if piece in set_of_pieces:
                raise serializers.ValidationError("There cant be two pieces of same type.")
            set_of_pieces.add(piece)
            set_of_positions.add(position)
    
        if slug not in valid_pieces or slug not in board:
            raise serializers.ValidationError("Invalid slug. Provide a slug present on the board")
        
        return attrs
