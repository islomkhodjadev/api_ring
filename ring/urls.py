from django.urls import path
from .views import (RegisterLoginView,
Login, AssitantView, RetrieveToken, TextView, VoiceView)


urlpatterns = [
    path("register/", RegisterLoginView.as_view()),
    path("login/", Login.as_view()),
    path("newToken/", RetrieveToken.as_view()),
    path("asisstant/", AssitantView.as_view()),
    path("asisstant/<str:name>/", AssitantView.as_view()), 
    path("text/", TextView.as_view()),
    path("voice/<str:assistant>/", VoiceView.as_view())
]
