from .models import Client
from .serializers import ClientSerializer
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
    return Response(serializer.data, status=status.HTTP_200_OK)