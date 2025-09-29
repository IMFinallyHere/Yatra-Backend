from django.urls import path
from yatra.views.user import RegisterView, Login, Refresh, UserList
from yatra.views.trip import TripFilterCreate, TripRUD, start_trip, end_trip, UserTripListCreate
from yatra.views.activity import ActivityFilterCreate, ActivityRUD, start_activity, end_activity
from yatra.views.bus import BusFilterCreate, BusUD, assign_users_to_bus

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', Login.as_view()),
    path('refresh/', Refresh.as_view()),
    path('trip/', TripFilterCreate.as_view()),
    path('trip/<int:pk>/', TripRUD.as_view()),
    path('trip/<int:pk>/activity/', ActivityFilterCreate.as_view()),
    path('trip/<int:pk>/start/', start_trip),
    path('trip/<int:pk>/end/', end_trip),
    path('activity/<int:pk>/', ActivityRUD.as_view()),
    path('activity/<int:pk>/start/', start_activity),
    path('activity/<int:pk>/end/', end_activity),
    path('trip/<int:pk>/bus/', BusFilterCreate.as_view()),
    path('bus/<int:pk>/', BusUD.as_view()),
    path('bus/<int:pk>/assign/', assign_users_to_bus),
    path('user/', UserList.as_view()),
    path('trip/<int:pk>/user/', UserTripListCreate.as_view()),

]