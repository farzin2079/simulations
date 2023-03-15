from rest_framework.decorators import api_view
from rest_framework.response import Response

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