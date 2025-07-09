from rest_framework import serializers
from .models import Client, Sale

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ['id']

    def validate_email(self, value):
        if Client.objects.filter(email=value).exists():
            raise serializers.ValidationError("E-mail already in use.")
        return value
                                      

class SaleSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=False, read_only=True)
    class Meta:
        model = Sale
        fields = '__all__'
        read_only_fields = ['id']

class ClientCustomSerializer(serializers.Serializer):
    info = serializers.SerializerMethodField()
    estatisticas = serializers.SerializerMethodField()
    duplicado = serializers.SerializerMethodField()

    def get_info(self, obj):
        return {
            "nomeCompleto": obj.name,
            "detalhes": {
                "email": obj.email,
                "nascimento": obj.dob.strftime('%Y-%m-%d') if obj.dob else None
            }
        }

    def get_estatisticas(self, obj):
        sales = obj.sale_set.all()
        return {
            "vendas": SaleSerializer(sales, many=True).data
        }

    def get_duplicado(self, obj):
        if getattr(obj, 'is_duplicated', False):
            return {"nomeCompleto": obj.name}
        return None

