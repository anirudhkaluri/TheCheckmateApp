from rest_framework import serializers

#Another way to implement serializer
# class HelperSerializer(serializers.Serializer):
#     Queen=serializers.CharField(required=False)
#     Bishop=serializers.CharField(required=False)
#     Rook=serializers.CharField(required=False)
#     Knight=serializers.CharField(required=False)

# class PositionSerializer(serializers.Serializer):
#     positions=HelperSerializer()
#     #positions is a key, its value is a Dictionary
#     #positions field will be deserialized into a dictionary

class PositionSerializer(serializers.Serializer):
    positions=serializers.DictField(child=serializers.CharField())
