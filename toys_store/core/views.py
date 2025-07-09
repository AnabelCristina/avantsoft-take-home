from django.db.models import Count
from .models import Client
from .serializers import ClientCustomSerializer, ClientSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def create_client(request, pk):
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def list_clients(request):
    name = request.GET.get('name')
    email = request.GET.get('email')

    queryset = Client.objects.all()

    if name:
        queryset = queryset.filter(name__icontains=name)
    if email:
        queryset = queryset.filter(email__icontains=email)

    serializer = ClientSerializer(queryset, many=True)
    
    duplicated_names = (
        Client.objects
        .values('name')
        .annotate(name_count=Count('name'))
        .filter(name_count__gt=1)
        .values_list('name', flat=True)
    )

    for client in queryset:
        client.is_duplicated = client.name in duplicated_names

    # Serializa com o formato personalizado
    serializer = ClientCustomSerializer(queryset, many=True)

    # Monta a resposta no formato esperado
    response_data = {
        "data": {
            "clientes": serializer.data
        },
        "meta": {
            "registroTotal": queryset.count(),
            "pagina": 1  # se quiser, pode calcular com parâmetros de paginação
        },
        "redundante": {
            "status": "ok"
        }
    }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_client(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response({'error': '404', 'message':'client not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClientSerializer(client, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_client(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response({'error': '404', 'message':'client not found.'}, status=status.HTTP_404_NOT_FOUND)

    client.delete()
    return Response({'message': 'success.'}, status=status.HTTP_204_NO_CONTENT)