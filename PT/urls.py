from django.urls import path

from .views import SearchResultList, PlantDetails, Login

urlpatterns = [
    path('searchResultList', SearchResultList.as_view(), name='SearchResultPlantList'),
    path('plantDetails', PlantDetails.as_view(), name='PlantDetails'),
    path('Login', Login.as_view(), name='Login')
