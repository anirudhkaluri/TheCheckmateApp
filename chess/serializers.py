from rest_framework import serializers

class PositionSerializer(serializers.Serializer):
    positions=serializers.DictField(child=serializers.CharField())
    #positions is a key, its value is a Dictionary
    #positions field will be deserialized into a dictionary
