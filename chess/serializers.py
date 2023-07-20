from rest_framework import serializers
from .utils.validMoves import get_coordinate_position



class PositionSerializer(serializers.Serializer):
    positions=serializers.DictField(child=serializers.CharField())
    def validate(self,attrs):
        positions_value=attrs.get('positions')
        valid_pieces={"Queen","Bishop","Knight","Rook"}
        for key,value in positions_value.items():
            if key not in valid_pieces:
                raise serializers.ValidationError("Invalid chess Pieces given in request data")
            if not len(value)==2:
                raise serializers.ValidationError("Invalid Position.Position on the grid must be of length 2")
            try:
                [x,y]=get_coordinate_position(value)
            except KeyError as e:
                raise serializers.ValidationError("Invalid position. Position must be of the form [A-H][1-8]")
        return attrs
