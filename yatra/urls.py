from django.urls import path
from yatra.views.user import RegisterView, Login, Refresh

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('refresh/', Refresh.as_view(), name='login'),

]