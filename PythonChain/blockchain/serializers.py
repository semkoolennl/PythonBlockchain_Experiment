from rest_framework import serializers

class BlockchainSerializer(serializers.Serializer):
    chain = serializers.JSONField()


class ChainSerializer(serializers.Serializer):
    version = serializers.CharField(max_length=4)
    index = serializers.IntegerField()
    timestamp = serializers.DateTimeField()
    transactions = serializers.JSONField()
    dificulty_target = serializers.IntegerField()
    nonce = serializers.IntegerField()
    previous_hash = serializers.CharField(max_length=256)


class TransactionSerializer(serializers.Serializer):
    sender = serializers.CharField(max_length=256)
    recipient = serializers.CharField(max_length=256)
    amount = serializers.IntegerField()


    def create(self, validated_data):
        return validated_data

    
class NodeSerializer(serializers.Serializer):
    nodes = serializers.JSONField()
