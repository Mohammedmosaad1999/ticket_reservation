
from django.contrib import admin
from django.urls import include, path 
from rest_framework import routers
from tickets import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('guest', views.viewsets_guests, basename='guest')
router.register('movie', views.viewsets_movies, basename='movie')
router.register('reservation', views.viewsets_reservations, basename='reservation')


urlpatterns = [
    path('admin/', admin.site.urls),

    #1
    path('django/jsonresponsenomodel/' , views.no_rest_no_model),

    #2
    path('django/jsonresponsefrommodel/' , views.no_rest_from_model),

    #3
    path('rest/fbv/guest/' , views.FBV_list),
    path('rest/fbv/guest/<int:pk>/' , views.FVB_pk),

    #4
    path('rest/cbv/guest/', views.CBV_list.as_view()),
    path('rest/cbv/guest/<int:pk>/', views.CBV_pk.as_view()),

    #5
    path('rest/mixins/guest/', views.mixins_list.as_view()),
    path('rest/mixins/guest/<int:pk>/', views.mixins_pk.as_view()),

    #6
    path('rest/generics/guest/', views.generics_list.as_view()),
    path('rest/generics/guest/<int:pk>/', views.generics_pk.as_view()),

    #7
    path('rest/viewsets/', include(router.urls)),
    path('rest/viewsets/guest/', include(router.urls)),
    path('rest/viewsets/movie/', include(router.urls)),
    path('rest/viewsets/reservation/', include(router.urls)),

    #8
    path('fbv/findmovie/', views.find_movie),

    #9
    path('fbv/newreservation/', views.new_reservation),

    #10 rest_auth_url
    path('api-auth/',include('rest_framework.urls')),

    #11 token authentication
    path('api-token-auth/',obtain_auth_token),

    #12 post auther editor
    path('rest/generics/post/<int:pk>/', views.post_pk.as_view()),
    # path('rest/generics/post/', views.post_list.as_view()),

]
