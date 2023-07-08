from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import (WatchListAV,WatchDetailAV,StreamPlatformAV,
                                    StreamPlatformDetailAV,ReviewCreate,ReviewList,
                                    ReviewDetail,StreamPlatformVS,UserReview,WatchListGV)

router=DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/', WatchDetailAV.as_view(), name='movie-detail'),
    path('',include(router.urls)),
    path('list2/', WatchListGV.as_view(), name='watch-list'),
    #path('stream/', StreamPlatformAV.as_view(), name='stream-list'),
    #path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name='streamplatform-detail'),
    #path('review/', ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    # dekh above links se hame reviews milenge but hame stream ke corresponding saare reviews chahiye
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),#ye url uss movie ke corresponding
    # review likhwaayga 
    path('<int:pk>/review/', ReviewList.as_view(), name='review-list'),# isse har moview ke corresponding
    # review dekh skte h 
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'), #issse ham 
    # individual review dekh skte h 
    #path('reviews/<str:username>/', UserReview.as_view(), name='user-review-detail'), #jo bhi review ke baad likhega wo username m jaayga
    path('reviews/', UserReview.as_view(), name='user-review-detail'), #jo bhi review ke baad likhega wo username m jaayga jaake iska view dekh

]