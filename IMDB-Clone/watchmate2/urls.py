from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('watch/', include('watchlist_app.api.urls')),
    path('api-auth/',include('rest_framework.urls')), #ye by default drf hame provide krta h
# ke webapi m login logout aajayga top right m dekh 
    path('account/', include('user_app.api.urls')),
]
