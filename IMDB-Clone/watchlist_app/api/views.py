from django.shortcuts import get_object_or_404
from rest_framework.views import APIView # ye class based view ke liye use hota h
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly,AllowAny,IsAdminUser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle,ScopedRateThrottle #throttling ke liye impot kiya
from django_filters.rest_framework import DjangoFilterBackend 

from rest_framework import filters 
from watchlist_app.api.permissions import IsAdminOrReadOnly,IsReviewUserOrReadOnly
# from rest_framework import mixins
from watchlist_app.models import WatchList, StreamPlatform,Review
from watchlist_app.api.serializers import (WatchListSerializer,StreamPlatformSerializer,
                                           ReviewSerializer)
from watchlist_app.api.throttling import ReviewCreateThrottle,ReviewListThrottle
from watchlist_app.api.pagination import WatchListPagination ,WatchListLOPagination,WatchListCPagination



class UserReview(generics.ListAPIView):
    # review aayge 
    # queryset = Review.objects.all() 
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle,AnonRateThrottle]

    # def get_queryset(self): # dekh is method se tu review/admin likh then hit to ajayga username
    #     Username=self.kwargs['username']  #yaha wo username fetch kiya url se
    #     return Review.objects.filter(review_user__username=Username) #dekh yaha mene filter kiya wo review jiske review_user

    def get_queryset(self):
        Username=self.request.query_params.get('username',None) #dekh yaha mene parameter fetch kiya h url ke username m username
        # present h mene whi fetch kiya ke bhai parameter dede jo url m h  
        return Review.objects.filter(review_user__username=Username)
    

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes=[IsAuthenticated]
 
    throttle_classes=[ReviewCreateThrottle] 
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk=self.kwargs.get('pk') #yaha menen id nikali movie ki url se
        movie = WatchList.objects.get(pk=pk)
        any_user=self.request.user
        new_queryset=Review.objects.filter(watchlist=movie,review_user=any_user)
        if new_queryset.exists():
            raise ValidationError("You already reviewed this movie")
        
        if movie.number_rating ==0 :
            movie.avg_rating = serializer.validated_data['rating']
        else :
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating']) / 2
        movie.number_rating += 1
        serializer.save(watchlist=movie,review_user=any_user)
        #daal diya

class ReviewList(generics.ListAPIView):#iss view se ham sirf review dekhenge review create krne k liye
    # ham alag se view function banayge
   # queryset = Review.objects.all() 
   #dekh iss queryset se saare reviews mil rhe h to hame apna custom query set likhna parega
    serializer_class = ReviewSerializer
   
    throttle_classes=[ReviewListThrottle,AnonRateThrottle] 

    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['review_user__username','active']   
    def get_queryset(self):
        pk=self.kwargs.get('pk') 
        
        return Review.objects.filter(watchlist=pk)
    

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer   
    permission_classes=[IsReviewUserOrReadOnly]
    # permission_classes = [IsAuthenticatedOrReadOnly] #class based view m aese likhega but 
    #permission_classes=[IsAuthenticated]
    # throttle_classes=[UserRateThrottle,AnonRateThrottle] #mene iss function m mention kiya h to bas issi mlgega

    throttle_classes=[ScopedRateThrottle] 
    throttle_scope='review-detail'




# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all() #queryset and serializer_class ye sab predefined attribute 
#     # name h isse change nahi kr sakta
#     serializer_class = ReviewSerializer
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all() #queryset and serializer_class ye sab predefined attribute 
#     # name h isse change nahi kr sakta
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)



class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes=[IsAdminOrReadOnly]
#VIEWSETS AND ROUTERS
# class StreamPlatformVS(viewsets.ViewSet):
#     
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True,context={'request': request})
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         platform = get_object_or_404(queryset, pk=pk)#yaha platform ki jgh teri mrzi jo naam lkhna h likh
#         serializer = StreamPlatformSerializer(platform,context={'request': request})
# #ye context={'request': request} becoz of hyperlinkedmodel serializer bas 
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data,context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StreamPlatformAV(APIView):
    permission_classes=[IsAdminOrReadOnly]
    def get(self, request):
        platform=StreamPlatform.objects.all()
        serializer=StreamPlatformSerializer(platform,many=True,context={'request': request})

        return Response(serializer.data)
    
    def post(self, request):
        serializer=StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
         return Response(serializer.errors)


class StreamPlatformDetailAV(APIView):
    permission_classes=[IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
          platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error':'Stream Platform not found'} , status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform,context={'request': request})
        return Response(serializer.data)

    def put(self, request,pk):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk):
        movie = StreamPlatform.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
          
     

class WatchListGV(generics.ListAPIView):
    queryset=WatchList.objects.all()
    serializer_class = WatchListSerializer
    #filter_backends=[DjangoFilterBackend]
    #filterset_fields=['title','Platform__name'] #platform ka name 
    
   # filter_backends=[filters.SearchFilter]
   # search_fields=['title','Platform__name'] 
    #search_fields=['title','=Platform__name'] #ISSE WHI AAYGA JISME EXACT PLATFORM NAME MATCH HOGA
   # search_fields=['^title','Platform__name'] #isse whi matching start se hogi khi se bhi nhi match krne lgega like upr jaise tha line 217 m
#AB ORDRING DEKH AB DATA TUJHE ASCENDING YA DESCING M MILEGA 
    # filter_backends=[filters.OrderingFilter]
    # ordering_fields=['avg_rating'] #isme ascending hoti h avg rating chhota then bada waala show hoga yaha jo bhi iss view ko call krega
    # waha simple /?ordering=naam likh jiske base pr ordering krni h  
    # ordering_fields=['-avg_rating'] agar ye likhega to bade se chhota aayga 
    # pagination_class=WatchListPagination #mene isme pagination lgaya h bas issi view m yaha Page number pagination likha tha is m jake dekh
    # pagination_class=WatchListLOPagination #yaha limit offset pagination use kiya h
    pagination_class=WatchListCPagination #dekh cursor pagination likhega to upar wala line 226 ko comment krna zruri h becoz iss pagination
    # me data created ke according milta h to ham alag se koi aur order nhi laga skte data ka 


class WatchListAV(APIView):
    permission_classes=[IsAdminOrReadOnly]#dekh ye permission lagaya m mtlb admin can update and delete but
    # can read only 
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WatchDetailAV(APIView):
    permission_classes=[IsAdminOrReadOnly] #dekh ye permission lagaya m mtlb admin can update and delete but
    # can read only 
    def get(self, request, pk):
        try:
          movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error':'Movie not found'} , status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request,pk):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
          
     