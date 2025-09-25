from django.urls import path
from yatra.views.user import RegisterView, Login, Refresh
from yatra.views.trip import TripFilterCreate, TripRUD
from yatra.views.activity import ActivityFilterCreate

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', Login.as_view()),
    path('refresh/', Refresh.as_view()),
    path('trip/', TripFilterCreate.as_view()),
    path('trip/<int:pk>/', TripRUD.as_view()),
    path('trip/<int:pk>/activity/', ActivityFilterCreate.as_view()),

]