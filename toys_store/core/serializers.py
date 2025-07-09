from rest_framework import serializers
from .models import Client, Sale

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

    def validate_email(self, value):
        if Client.objects.filter(email=value).exists():
            raise serializers.ValidationError("E-mail already in use.")
        return value
                                      

class SaleSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=False, read_only=True)
    class Meta:
        model = Sale
        fields = '__all__'
