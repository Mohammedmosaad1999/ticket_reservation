from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from .models import Guest, Movie, Reservation , Post
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer , PostSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework import mixins, generics, viewsets
from rest_framework.authentication import TokenAuthentication

from .permissions import IsAutherOrReadOnly, IsAuther 


# without rest framework and without model
def no_rest_no_model(request):
    guests = [
        {
            'id': 1,
            'name': 'Guest 1',
            'mobile': '1234567890'
        },
        {
            'id': 2,
            'name': 'Guest 2',
            'mobile': '0987654321'
        }
    ]
    return JsonResponse(guests, safe=False)

# no rest framework but with model data default django
def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        'guests': list(data.values('name', 'mobile'))
    }
    return JsonResponse(response)

# rest framework with model data
# list == GET
# create == POST
# pk query == GET
# update == PUT
# delete == DELETE

# 3 function based views
# 3.1 list and create
@api_view(['GET', 'POST'])
def FBV_list(request):
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 3.2 retrieve, update and destroy
@api_view(['GET', 'PUT', 'DELETE'])
def FVB_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 4 cbv class based views
# 4.1 list and create (get and post)
class CBV_list(APIView):
    def get(self, request):
        guest = Guest.objects.all()
        serializer = GuestSerializer(guest, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 4.2 retrieve, update and destroy (get, put and delete)
class CBV_pk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            return None

    def get(self, request, pk):
        guest = self.get_object(pk)
        if guest is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    def put(self, request, pk):
        guest = self.get_object(pk)
        if guest is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk)
        if guest is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 5 mixins and generics views
class mixins_list(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)

# 6 GENERIC VIEWS
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]


class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]


# 7 viewsets and routers
class viewsets_guests(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class viewsets_movies(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    backend_filter = filters.SearchFilter
    search_fields = ['hall', 'movie']

class viewsets_reservations(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


#8 find movie using fbv
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        hall=request.data['hall'],
        movie=request.data['movie'])
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)



#9 create new reservation using fbv   
@api_view(['POST'])


def new_reservation(request):
    movie =Movie.objects.get(
        hall=request.data['hall'],
        movie=request.data['movie']
    )

    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()

    return Response(status=status.HTTP_201_CREATED)


#10 post auther editor

class post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAutherOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class post_list(generics.ListCreateAPIView):
    permission_classes = [IsAuther]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(auther=self.request.user)
