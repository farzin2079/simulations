from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import ListingSerialazer
from auctions.models import Listing

@api_view(['GET'])
def getRoute(request):
    
    routes = [
        { 'name': 'farzin'},
        { 'lastname': 'abbasi'},
        { 'birthyear': '2000'},
        { 'job': 'programmer'}
    ]
    
    return Response(routes)

@api_view(['GET'])
def getListings(request):
    listing = Listing.objects.all()
    serialazer = ListingSerialazer(listing, many=True)
    return Response(serialazer.data)

@api_view(['GEt'])
def getListing(request, id):
    listing = Listing.objects.get(pk=id)
    serializer = ListingSerialazer(listing, many=False)
    return Response(serializer.data)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def addcomment(request, pk):
    active = Listing.objects.get(id=pk)
    user = request.user
    data = request.data 
    
    print('DATA:', data)
    
    serializer = ListingSerialazer(active)
    return Response(serializer.data)