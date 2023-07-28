from rest_framework import serializers

class CustomerPayloadSerializer(serializers.Serializer):
    customer_id = serializers.CharField()

# class PackDataSerializer(serializers.Serializer):
