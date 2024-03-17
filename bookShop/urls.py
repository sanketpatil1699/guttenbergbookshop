from django.urls import path,include
from . import views


urlpatterns = [
    path('getBooksData/',views.getBooksData, name='getBooksData')
]
