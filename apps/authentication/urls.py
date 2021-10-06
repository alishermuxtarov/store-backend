from django.urls import path

from .views import LoginView, RegisterView

urlpatterns = [
    path('sign_in/', LoginView.as_view(), name='sign_in'),
    path('sign_up/', RegisterView.as_view(), name='sign_up'),
]
